"""regua.py — passa as réguas de posicionamento nas linhas do OCR e procura linha de 1 px na borda.

uso: ~/.exos-whisper/bin/python -I regua.py <ocr.json>

Formatos (réguas no REFERENCE.md):
  4:5  (1080x1350)  texto a 45 px das bordas; informa o corte da grade 3:4 do perfil
  9:16 (1080x1920)  Stories: nada em y<250 nem y>1580 (régua da casa)
                    Reels: 14% em cima, 35% embaixo, 6% nas laterais; nome do perfil e legenda a partir de y≈1450;
                    coluna de ícones em x>960 entre y≈1080 e 1580
  2560x1440         YouTube: área segura 1546x423 no centro (x 507–2053, y 508–931)
  outros            só as menores margens
A caixa do OCR erra alguns px e não vê placa/caixa atrás do texto: confirme no pixel antes de cobrar.
"""
import json
import os
import sys

import numpy as np
from PIL import Image


def no_pixel(a, box, lado):
    """Borda real do texto/placa naquele lado: primeiro px que destoa (>80 em RGB) do fundo encostado na borda."""
    H, W = a.shape[:2]
    x0, y0, x1, y1 = box
    r0, r1 = max(0, y0 - 3), min(H, y1 + 3)
    c0, c1 = max(0, x0 - 3), min(W, x1 + 3)
    if lado in ("esq", "dir"):
        faixa = a[r0:r1]
        ref = np.median(faixa[:, :6] if lado == "esq" else faixa[:, -6:], axis=(0, 1))
        dif = (np.abs(faixa - ref).sum(axis=2) > 80).sum(axis=0) >= 2
        cols = np.where(dif)[0]
        if not len(cols):
            return None
        return int(cols.min()) if lado == "esq" else int(W - 1 - cols.max())
    faixa = a[:, c0:c1]
    ref = np.median(faixa[:6] if lado == "topo" else faixa[-6:], axis=(0, 1))
    dif = (np.abs(faixa - ref).sum(axis=2) > 80).sum(axis=1) >= 2
    rows = np.where(dif)[0]
    if not len(rows):
        return None
    return int(rows.min()) if lado == "topo" else int(H - 1 - rows.max())


def borda(path):
    if not os.path.exists(path):
        return "arquivo não encontrado"
    a = np.asarray(Image.open(path).convert("L")).astype(float)
    saltos = {"esq": abs(a[:, 0] - a[:, 1]).mean(), "dir": abs(a[:, -1] - a[:, -2]).mean(),
              "topo": abs(a[0] - a[1]).mean(), "base": abs(a[-1] - a[-2]).mean()}
    ruins = [f"{k} ({v:.0f})" for k, v in saltos.items() if v > 30]
    return "linha de 1 px em: " + ", ".join(ruins) if ruins else "ok"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    dados = json.load(open(sys.argv[1]))
    for path, r in dados.items():
        d = r["corr"]
        W, H, L = d["w"], d["h"], d["lines"]
        print(f"\n### {os.path.basename(path)}  ({W}x{H})")
        if not L:
            print("  sem texto no OCR")
        margens = [(ln["box"][0], ln["box"][1], W - ln["box"][2], H - ln["box"][3], ln["text"]) for ln in L]
        if L:
            print("  menores margens: esq %d · topo %d · dir %d · base %d" % tuple(min(m[i] for m in margens) for i in range(4)))
        if abs(W / H - 0.8) < 0.01:
            corte = (W - H * 0.75) / 2
            lim = 45 * W / 1080
            a = np.asarray(Image.open(path).convert("RGB")).astype(int) if os.path.exists(path) else None
            for ln, (e, t, dd, b, txt) in zip(L, margens):
                perto = {k: v for k, v in (("esq", e), ("topo", t), ("dir", dd), ("base", b)) if v < lim + 6}
                if not perto:
                    continue
                medidas = []
                for lado, v in perto.items():
                    px = no_pixel(a, ln["box"], lado) if a is not None else None
                    real = px if px is not None else v
                    medidas.append((lado, v, px, real))
                if all(real >= lim for _, _, _, real in medidas):
                    continue
                det = ", ".join(f"{lado} OCR {v} → pixel {px if px is not None else '?'}" for lado, v, px, _ in medidas)
                print(f"  ABAIXO DE 45 px: {txt!r} ({det}) — dar zoom: ponta de serifa itálica não conta")
            print(f"  grade 3:4 do perfil corta ~{corte:.0f} px de cada lado")
        elif abs(W / H - 9 / 16) < 0.01:
            k = H / 1920
            for ln in L:
                x0, y0, x1, y1 = ln["box"]
                st, re_ = [], []
                if y0 < 250 * k:
                    st.append("faixa de cima")
                if y1 > 1580 * k:
                    st.append("faixa do botão")
                if y0 < 269 * k:
                    re_.append("14% de cima")
                if y1 > 1450 * k:
                    re_.append("atrás do nome do perfil/legenda")
                elif y1 > 1248 * k:
                    re_.append("dentro dos 35% de baixo")
                if x1 > 960 * W / 1080 and y1 > 1080 * k and y0 < 1580 * k:
                    re_.append("coluna de ícones")
                if x0 < 65 * W / 1080 or x1 > 1015 * W / 1080:
                    re_.append("6% das laterais")
                if st or re_:
                    print(f"  y {y0}-{y1} x {x0}-{x1} {ln['text']!r}")
                    if st:
                        print(f"      STORIES: {', '.join(st)}")
                    if re_:
                        print(f"      reels: {', '.join(re_)}")
        elif (W, H) == (2560, 1440):
            for ln in L:
                x0, y0, x1, y1 = ln["box"]
                if x0 < 507 or x1 > 2053 or y0 < 508 or y1 > 931:
                    print(f"  FORA DA ÁREA SEGURA DO YOUTUBE: {ln['text']!r} {ln['box']}")
        print(f"  borda: {borda(path)}")


if __name__ == "__main__":
    main()
