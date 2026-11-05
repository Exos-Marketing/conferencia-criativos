"""vid_diff.py — compara o vídeo novo com o editado aprovado de referência (mesmo ADS, mesmo formato).

uso: ~/.exos-whisper/bin/python -I vid_diff.py <novo.mp4> <referência.mp4> <saida.json>

Vídeo: quadro a quadro em cinza a 1/8 da resolução, alinhado pelo índice do quadro (com checagem de defasagem
pela luminância média). Marca os trechos em que mais de 0,3% da imagem muda (|diferença| > 30).
Áudio: mono 16 kHz, defasagem por correlação, diferença por janela de 1 s em dB relativo ao sinal,
janelas quase mudas (< -90 dBFS, "mídia offline") e loudness integrado de cada um.
"""
import json
import subprocess
import sys

import numpy as np


def probe(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", p],
                         capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout
    j = json.loads(out)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    num, den = map(int, v["avg_frame_rate"].split("/"))
    return {
        "dur": float(j["format"]["duration"]), "w": v["width"], "h": v["height"], "fps": num / den,
        "vcodec": v["codec_name"], "pix": v.get("pix_fmt"), "nb_frames": int(v.get("nb_frames") or 0),
        "kbps": round(int(j["format"].get("bit_rate", 0)) / 1000),
        "vkbps": round(int(v.get("bit_rate", 0) or 0) / 1000),
        "acodec": a and a["codec_name"], "asr": a and int(a["sample_rate"]), "ach": a and a["channels"],
        "color": [v.get("color_space"), v.get("color_transfer"), v.get("color_primaries"), v.get("color_range")],
    }


def quadros(p, w, h):
    cmd = ["ffmpeg", "-v", "error", "-i", p, "-vf", f"scale={w}:{h}:flags=area,format=gray",
           "-f", "rawvideo", "-"]
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL)
    n = w * h
    while True:
        buf = pr.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w)
    pr.wait()


def audio(p):
    cmd = ["ffmpeg", "-v", "error", "-i", p, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    out = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL).stdout
    return np.frombuffer(out, np.float32)


def loudness(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-vn", "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL).stderr
    i = r.rfind("Integrated loudness:")
    try:
        return float(r[i:].split("I:")[1].split("LUFS")[0])
    except Exception:
        return None


def trechos(flags, fps, gap=3):
    """Índices marcados -> trechos [ini, fim] em segundos, juntando buracos de até `gap` quadros."""
    idx = np.where(flags)[0]
    if not len(idx):
        return []
    out, ini, ant = [], idx[0], idx[0]
    for i in idx[1:]:
        if i > ant + gap:
            out.append((ini, ant))
            ini = i
        ant = i
    out.append((ini, ant))
    return [[round(a / fps, 2), round((b + 1) / fps, 2), int(a), int(b)] for a, b in out]


def main():
    v26, v25, saida = sys.argv[1:4]
    p26, p25 = probe(v26), probe(v25)
    res = {"v26": p26, "v25": p25}

    # vídeo
    w = p26["w"] // 8
    h = p26["h"] // 8
    mad, frac, lum26, lum25 = [], [], [], []
    calor = np.zeros((h, w), np.int32)
    g25 = quadros(v25, w, h)
    for a in quadros(v26, w, h):
        try:
            b = next(g25)
        except StopIteration:
            lum26.append(float(a.mean()))
            continue
        d = np.abs(a.astype(np.int16) - b.astype(np.int16))
        m = d > 30
        mad.append(float(d.mean()))
        frac.append(float(m.mean()))
        if m.mean() > 0.003:
            calor += m
        lum26.append(float(a.mean()))
        lum25.append(float(b.mean()))
    for b in g25:
        lum25.append(float(b.mean()))
    fps = p26["fps"]
    res["frames"] = {"n26": len(lum26), "n25": len(lum25)}
    l26, l25 = np.array(lum26), np.array(lum25)
    # defasagem pela luminância média (±60 quadros)
    melhor = None
    n = min(len(l26), len(l25)) - 130
    for lag in range(-60, 61):
        x = l26[60 + lag:60 + lag + n] if lag >= 0 else l26[60 + lag:60 + lag + n]
        y = l25[60:60 + n]
        if len(x) != len(y) or len(x) < 10:
            continue
        e = float(np.abs(x - y).mean())
        if melhor is None or e < melhor[1]:
            melhor = (lag, e)
    res["lag_quadros"] = melhor
    frac = np.array(frac)
    res["mad_mediana"] = round(float(np.median(mad)), 3)
    res["frac_mediana"] = round(float(np.median(frac)), 5)
    res["trechos_mudados"] = trechos(frac > 0.003, fps)
    res["trechos_detalhe"] = []
    for t in res["trechos_mudados"]:
        seg = frac[t[2]:t[3] + 1]
        res["trechos_detalhe"].append({"ini": t[0], "fim": t[1], "frac_max": round(float(seg.max()), 4),
                                       "frac_media": round(float(seg.mean()), 4)})
    np.save(saida.replace(".json", "_calor.npy"), calor)
    np.save(saida.replace(".json", "_frac.npy"), frac)

    # áudio
    a26, a25 = audio(v26), audio(v25)
    sr = 16000
    k = min(len(a26), len(a25), sr * 30)
    best = None
    for lag in range(-1600, 1601, 4):  # ±100 ms
        x = a26[max(0, lag):max(0, lag) + k - 1700]
        y = a25[max(0, -lag):max(0, -lag) + k - 1700]
        c = float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-9))
        if best is None or c > best[1]:
            best = (lag, c)
    lag = best[0]
    x = a26[max(0, lag):]
    y = a25[max(0, -lag):]
    m = min(len(x), len(y))
    x, y = x[:m], y[:m]
    jan = []
    for i in range(0, m - sr + 1, sr):
        s = y[i:i + sr]
        dd = x[i:i + sr] - s
        rs = float(np.sqrt((s ** 2).mean()) + 1e-12)
        rd = float(np.sqrt((dd ** 2).mean()) + 1e-12)
        jan.append(20 * np.log10(rd / rs))
    jan = np.array(jan)
    rms26 = np.array([20 * np.log10(np.sqrt((a26[i:i + sr] ** 2).mean()) + 1e-12)
                      for i in range(0, len(a26) - sr + 1, sr)])
    res["audio"] = {
        "dur26": round(len(a26) / sr, 2), "dur25": round(len(a25) / sr, 2),
        "lag_ms": lag / 16, "corr": round(best[1], 4),
        "dif_rel_db_mediana": round(float(np.median(jan)), 1),
        "janelas_dif_acima_-20db": [int(i) for i in np.where(jan > -20)[0]],
        "janelas_mudas_26": [int(i) for i in np.where(rms26 < -90)[0]],
        "lufs26": loudness(v26), "lufs25": loudness(v25),
    }
    json.dump(res, open(saida, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
