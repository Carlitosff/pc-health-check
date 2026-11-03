"""Control de calidad del mp4 final (v13, 03/11). Mide lo que el ojo no ve en una preview.
Motivo: 901 (147 vistas, view rate 46%) y la Ñ (177, 50%) murieron en los 3 primeros segundos con el mismo motor que da 1.800.
Uso: python3 qa.py archivo.mp4 [más.mp4] [--steady]  -> OK / FALLO por vídeo; código de salida 1 si algo falla.
  - duración 25–38 s, 1080x1920, audio presente, sin saturar (pico < -0.3 dB) y sin ser inaudible (media > -30 dB)
  - movimiento: tramos >1,2 s sin cambio apreciable (suma de diferencias por píxel), salvo con --steady
  - gancho: movimiento en los 3 primeros segundos y contraste del frame 0 (desviación de luminancia)"""
import json, re, subprocess, sys
import numpy as np


def probe(f):
    o = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", f]))
    v = next(s for s in o["streams"] if s["codec_type"] == "video")
    return float(o["format"]["duration"]), int(v["width"]), int(v["height"]), any(s["codec_type"] == "audio" for s in o["streams"])


def gray_frames(f, w=108, h=192, fps=10):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", f, "-vf", f"fps={fps},scale={w}:{h},format=gray", "-f", "rawvideo", "-"])
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)


def audio(f):
    e = subprocess.run(["ffmpeg", "-i", f, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", e).group(1)), float(re.search(r"max_volume: (-?[\d.]+)", e).group(1))


def check(f, steady=False):
    bad, info = [], {}
    dur, w, h, has_a = probe(f)
    info["dur"] = round(dur, 1)
    if not 25 <= dur <= 38.6:
        bad.append(f"duración {dur:.1f}s fuera de 25–38")
    if (w, h) != (1080, 1920):
        bad.append(f"resolución {w}x{h}")
    if not has_a:
        bad.append("sin audio")
    else:
        mean, peak = audio(f)
        info["audio"] = (mean, peak)
        if peak > -0.3:
            bad.append(f"audio saturado (pico {peak} dB)")
        if mean < -30:
            bad.append(f"audio muy bajo (media {mean} dB)")
    g = gray_frames(f)
    d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
    info["mov_medio"] = round(float(d.mean()), 2)
    info["mov_3s"] = round(float(d[:30].mean()), 2)
    info["contraste_f0"] = round(float(g[0].std()), 1)
    if info["contraste_f0"] < 18:
        bad.append(f"frame 0 sin contraste ({info['contraste_f0']})")
    if not steady:
        if info["mov_3s"] < 0.25:
            bad.append(f"gancho casi quieto ({info['mov_3s']})")
        still = run = 0
        for x in d:
            run = run + 1 if x < 0.06 else 0
            still = max(still, run)
        info["quieto_max_s"] = still / 10
        if still > 12:
            bad.append(f"{still / 10:.1f}s seguidos sin movimiento")
    return bad, info


if __name__ == "__main__":
    steady = "--steady" in sys.argv
    rc = 0
    for f in [a for a in sys.argv[1:] if not a.startswith("--")]:
        bad, info = check(f, steady)
        print(("OK   " if not bad else "FALLO"), f.split("/")[-1], info, "; ".join(bad))
        rc |= bool(bad)
    sys.exit(rc)
