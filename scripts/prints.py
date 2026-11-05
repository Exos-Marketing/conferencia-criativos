"""prints.py — print da revisão de posicionamento: a peça com a interface do Instagram desenhada por cima.

uso: ~/.exos-whisper/bin/python -I prints.py <spec.json>

Painéis por peça (um ou mais):
  stories  9:16 · régua da casa: 250 px em cima, 340 px embaixo
  reels    9:16 · guias de mercado: 14% em cima, 35% embaixo, 6% nas laterais; nome do perfil, legenda, botão e ícones
  feed     4:5  · margem de 45 px e o corte da grade 3:4 do perfil
Caixas em px do arquivo original; cor por item: vermelho (coberto), amarelo (no limite), verde (livre).
Spec de exemplo no EXAMPLES.md. Saída: <saida>/<nome> (PNG), pronta para anexar na task.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HELV = "/System/Library/Fonts/Helvetica.ttc"
CORES = {"vermelho": (235, 45, 45), "amarelo": (245, 170, 0), "verde": (40, 170, 80)}
INK, MUTED = (28, 28, 30), (90, 90, 96)
PW = 600                      # largura de cada painel
SC = PW / 1080                # escala da interface (desenhada em coordenadas de 1080 de largura)


def font(size, bold=False):
    for i in range(8):
        try:
            f = ImageFont.truetype(HELV, size, index=i)
        except OSError:
            break
        estilo = f.getname()[1].lower()
        if bold and estilo == "bold":
            return f
        if not bold and estilo in ("regular", "roman", "medium"):
            return f
    return ImageFont.truetype(HELV, size)


# ---------------------------------------------------------------- desenho da interface (coordenadas 1080 de largura)

def shade(lay, box):
    x0, y0, x1, y1 = [round(v * SC) for v in box]
    w, h = x1 - x0, y1 - y0
    patch = Image.new("RGBA", (w, h), (0, 0, 0, 120))
    pd = ImageDraw.Draw(patch)
    for k in range(-h, w, 12):                    # hachura diagonal, só dentro da faixa
        pd.line((k, 0, k + h, h), fill=(255, 255, 255, 40), width=1)
    lay.alpha_composite(patch, (x0, y0))


def limit(d, y, label, side="right", above=False, ph=None):
    yy = round(y * SC)
    d.line((0, yy, PW, yy), fill=(255, 214, 10, 255), width=2)
    f = font(15, True)
    tw = d.textlength(label, font=f)
    xa = PW - tw - 14 if side == "right" else 4
    ya = yy - 22 if above else yy + 3
    d.rounded_rectangle((xa, ya, xa + tw + 10, ya + 19), 4, fill=(255, 214, 10, 235))
    d.text((xa + 5, ya + 1), label, font=f, fill=(0, 0, 0, 255))


def vlimit(d, x, label, h):
    xx = round(x * SC)
    d.line((xx, 0, xx, h), fill=(255, 214, 10, 255), width=2)
    if label:
        f = font(15, True)
        tw = d.textlength(label, font=f)
        d.rounded_rectangle((xx + 4, 6, xx + tw + 14, 25), 4, fill=(255, 214, 10, 235))
        d.text((xx + 9, 7), label, font=f, fill=(0, 0, 0, 255))


def wtext(d, xy, s, size, bold=False):
    x, y = xy
    f = font(max(9, round(size * SC)), bold)
    d.text((x * SC + 1, y * SC + 1), s, font=f, fill=(0, 0, 0, 160))
    d.text((x * SC, y * SC), s, font=f, fill=(255, 255, 255, 255))


def circle(d, cx, cy, r, w=2, fill=None):
    d.ellipse(((cx - r) * SC, (cy - r) * SC, (cx + r) * SC, (cy + r) * SC),
              outline=(255, 255, 255, 255), width=w, fill=fill)


def ui_stories(lay, d, perfil, h):
    shade(lay, (0, 0, 1080, 250))
    shade(lay, (0, 1580, 1080, 1920))
    d.rounded_rectangle((24 * SC, 22 * SC, 1056 * SC, 29 * SC), 2, fill=(255, 255, 255, 230))
    circle(d, 80, 104, 36, 2, fill=(200, 200, 200, 200))
    wtext(d, (132, 74), perfil, 32, True)
    wtext(d, (132, 114), "Patrocinado", 28)
    wtext(d, (930, 80), "...", 40, True)
    wtext(d, (1012, 80), "X", 38)
    wtext(d, (528, 1688), "^", 40, True)
    d.rounded_rectangle((380 * SC, 1740 * SC, 700 * SC, 1812 * SC), round(36 * SC), fill=(255, 255, 255, 240))
    f = font(round(34 * SC), True)
    tw = d.textlength("Saiba mais", font=f)
    d.text((540 * SC - tw / 2, 1758 * SC), "Saiba mais", font=f, fill=(20, 20, 20, 255))
    limit(d, 250, "250 px")
    limit(d, 1580, "340 px", above=True)


def ui_reels(lay, d, perfil, h):
    shade(lay, (0, 0, 1080, 269))
    shade(lay, (0, 1248, 1080, 1920))
    shade(lay, (0, 269, 65, 1248))
    shade(lay, (1015, 269, 1080, 1248))
    wtext(d, (44, 74), "Reels", 46, True)
    d.rounded_rectangle((984 * SC, 82 * SC, 1040 * SC, 124 * SC), 4, outline=(255, 255, 255, 255), width=2)
    for y in (1120, 1260, 1400, 1540):            # curtir, comentar, compartilhar, mais
        circle(d, 1010, y, 32, 3)
    circle(d, 70, 1522, 32, 2, fill=(200, 200, 200, 200))
    wtext(d, (118, 1494), f"{perfil}  ·  Seguir", 30, True)
    wtext(d, (118, 1532), "Patrocinado", 26)
    wtext(d, (40, 1584), "Legenda do anúncio, primeira linha... mais", 28)
    wtext(d, (40, 1628), "Áudio original", 26)
    d.rounded_rectangle((30 * SC, 1688 * SC, 1050 * SC, 1760 * SC), round(14 * SC), fill=(255, 255, 255, 235))
    f = font(round(34 * SC), True)
    d.text((62 * SC, 1706 * SC), "Saiba mais", font=f, fill=(20, 20, 20, 255))
    d.text((1000 * SC, 1706 * SC), ">", font=f, fill=(20, 20, 20, 255))
    limit(d, 269, "14% · 269 px")
    limit(d, 1248, "35% · 672 px", "left")


def ui_feed(lay, d, perfil, h):
    hh = h / SC                                   # altura em coordenadas de 1080
    corte = (1080 - hh * 0.75) / 2                # grade 3:4 do perfil
    shade(lay, (0, 0, corte, hh))
    shade(lay, (1080 - corte, 0, 1080, hh))
    vlimit(d, 45, "45 px", h)
    vlimit(d, 1035, "", h)
    limit(d, 45, "45 px")
    limit(d, hh - 45, "45 px", above=True)
    f = font(14, True)
    d.text((4, h - 22), f"grade 3:4: ~{corte:.0f} px", font=f, fill=(255, 255, 255, 255))


PAINEIS = {
    "stories": ("STORIES · régua da casa", ui_stories),
    "reels": ("REELS · zona de 35% embaixo", ui_reels),
    "feed": ("FEED · margem de 45 px e grade 3:4", ui_feed),
}


def mark(d, n, box, cor, k):
    x0, y0, x1, y1 = [v * k for v in box]
    d.rectangle((x0, y0, x1, y1), outline=cor + (255,), width=4)
    r = 13
    cx, cy = x0 + 4, y0 + 4
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=cor + (255,), outline=(255, 255, 255, 255), width=2)
    f = font(16, True)
    tw = d.textlength(str(n), font=f)
    d.text((cx - tw / 2, cy - 9), str(n), font=f, fill=(255, 255, 255, 255))


def painel(img, tipo, itens, perfil):
    ph = round(PW * img.height / img.width)
    base = img.resize((PW, ph), Image.LANCZOS).convert("RGBA")
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    PAINEIS[tipo][1](lay, d, perfil, ph)
    k = PW / img.width
    for n, box, cor, _ in itens:
        mark(d, n, box, CORES[cor], k)
    return Image.alpha_composite(base, lay).convert("RGB")


def wrap(d, s, f, width):
    linhas, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            linhas.append(cur)
            cur = w
    if cur:
        linhas.append(cur)
    return linhas


SUB = ("Revisão de posicionamento: a peça com a interface do Instagram desenhada por cima (faixas hachuradas = área que a "
       "interface cobre). Vermelho = fica coberto · Amarelo = no limite · Verde = livre. Medidas em px no arquivo original.")
SUB_FEED = ("Revisão de posicionamento: a peça com as linhas de 45 px e o corte da grade 3:4 do perfil (faixas hachuradas). "
            "Vermelho = fora da margem · Amarelo = no limite · Verde = livre. Medidas em px no arquivo original.")
NOTA_916 = ("Régua da casa para 1080x1920 de anúncio: Stories (nada nos 250 px de cima nem nos 340 px de baixo). O painel do "
            "Reels usa as margens dos guias de mercado (14% em cima, 35% embaixo, 6% nas laterais); a página oficial do Meta "
            "só abre no navegador. Interface desenhada em esquema: a posição exata varia com o aparelho.")
NOTA_FEED = ("Régua da casa para 1080x1350: texto, selo e logo a 45 px das bordas. No feed a imagem vai de borda a borda da "
             "tela; na grade do perfil (3:4) o Instagram corta as faixas hachuradas dos lados.")


def compor(peca, base_dir, saida, perfil):
    img = Image.open(os.path.join(base_dir, peca["arquivo"])).convert("RGB")
    tipos = [t for t in ("feed", "stories", "reels") if t in peca]
    M, G = 34, 30
    W = M * 2 + PW * len(tipos) + G * (len(tipos) - 1)
    W = max(W, 900)
    d0 = ImageDraw.Draw(Image.new("RGB", (W, 10)))
    fT, fS, fP, fL = font(30, True), font(19), font(19, True), font(17)
    sub = wrap(d0, SUB_FEED if tipos == ["feed"] else SUB, fS, W - 2 * M)
    nota = wrap(d0, NOTA_FEED if tipos == ["feed"] else NOTA_916, fL, W - 2 * M)
    legs = [[(n, CORES[c], wrap(d0, txt, fL, PW - 40)) for n, _, c, txt in peca[t]["itens"]] for t in tipos]
    leg_h = max(sum(len(ls) * 23 + 10 for _, _, ls in lg) for lg in legs)
    ph = round(PW * img.height / img.width)
    H = M + 44 + len(sub) * 26 + 18 + 40 + ph + 18 + leg_h + 16 + len(nota) * 23 + M
    can = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(can)
    d.text((M, M), peca["titulo"], font=fT, fill=INK)
    y = M + 44
    for ln in sub:
        d.text((M, y), ln, font=fS, fill=MUTED)
        y += 26
    y += 18
    for i, t in enumerate(tipos):
        x = M + i * (PW + G)
        spec = peca[t]
        d.text((x, y), spec.get("titulo", PAINEIS[t][0]), font=fP, fill=INK)
        selo, cor = spec["selo"]
        cw = d.textlength(selo, font=fP) + 22
        d.rounded_rectangle((x + PW - cw, y - 4, x + PW, y + 24), 12, fill=CORES[cor])
        d.text((x + PW - cw + 11, y - 1), selo, font=fP, fill="white")
        can.paste(painel(img, t, spec["itens"], perfil), (x, y + 40))
        yy = y + 40 + ph + 18
        for n, c, linhas in legs[i]:
            d.ellipse((x, yy + 1, x + 22, yy + 23), fill=c)
            fb = font(14, True)
            tw = d.textlength(str(n), font=fb)
            d.text((x + 11 - tw / 2, yy + 4), str(n), font=fb, fill="white")
            for ln in linhas:
                d.text((x + 32, yy + 2), ln, font=fL, fill=INK)
                yy += 23
            yy += 10
    y = y + 40 + ph + 18 + leg_h + 16
    for ln in nota:
        d.text((M, y), ln, font=fL, fill=MUTED)
        y += 23
    out = os.path.join(saida, peca["nome"])
    can.save(out, optimize=True)
    return out, can.size


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    spec_path = os.path.abspath(sys.argv[1])
    base_dir = os.path.dirname(spec_path)
    spec = json.load(open(spec_path))
    saida = os.path.join(base_dir, spec.get("saida", "prints"))
    os.makedirs(saida, exist_ok=True)
    for peca in spec["pecas"]:
        out, size = compor(peca, base_dir, saida, spec.get("perfil", "perfil.da.expert"))
        print(out, size)


if __name__ == "__main__":
    main()
