"""ocr.py — OCR da Apple Vision com caixas em px (origem no canto superior esquerdo).

uso: ~/.exos-whisper/bin/python -I ocr.py <saida.json> <img1> [<img2> ...]

Roda duas vezes por imagem: com correção de idioma ("corr", melhor para acento em caixa alta) e sem ("raw").
A caixa do Vision erra alguns px: margem no limite se confirma no pixel antes de virar ajuste.
"""
import json
import sys

import Vision
from Foundation import NSURL
from PIL import Image


def ocr(path, correcao):
    W, H = Image.open(path).size
    req = Vision.VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    req.setRecognitionLanguages_(["pt-BR", "en-US"])
    req.setUsesLanguageCorrection_(correcao)
    h = Vision.VNImageRequestHandler.alloc().initWithURL_options_(NSURL.fileURLWithPath_(path), None)
    h.performRequests_error_([req], None)
    linhas = []
    for o in req.results() or []:
        c = o.topCandidates_(1)[0]
        bb = o.boundingBox()
        x0, y0 = bb.origin.x * W, (1 - bb.origin.y - bb.size.height) * H
        linhas.append({"text": c.string(), "conf": round(float(c.confidence()), 2),
                       "box": [round(x0), round(y0), round(x0 + bb.size.width * W), round(y0 + bb.size.height * H)]})
    linhas.sort(key=lambda r: (r["box"][1], r["box"][0]))
    return {"w": W, "h": H, "lines": linhas}


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    res = {p: {"corr": ocr(p, True), "raw": ocr(p, False)} for p in sys.argv[2:]}
    json.dump(res, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
    for p, r in res.items():
        d = r["corr"]
        print(f"\n### {p.split('/')[-1]}  ({d['w']}x{d['h']})")
        for ln in d["lines"]:
            x0, y0, x1, y1 = ln["box"]
            m = f"E{x0} T{y0} D{d['w'] - x1} B{d['h'] - y1}"
            print(f"  [{x0:4},{y0:4},{x1:4},{y1:4}] {m:24} {ln['conf']:.2f} | {ln['text']}")
        print("  sem correção:", " / ".join(ln["text"] for ln in r["raw"]["lines"]))


if __name__ == "__main__":
    main()
