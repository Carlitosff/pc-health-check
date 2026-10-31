"""Locución local (Kokoro) encajada en los tramos del vídeo + subtítulos y boca sincronizados."""
import hashlib, os, sys, wave
import numpy as np

sys.path.insert(0, "/home/claude/tts")
import kokoro_tts  # noqa: E402
sys.path.insert(0, "/home/claude/tts2")
import piper_tts  # noqa: E402
from engine import Captions, SR  # noqa: E402

CACHE = "/home/claude/tiktok/vo_cache"
os.makedirs(CACHE, exist_ok=True)
BASE_SPEED = 1.18
MAX_SPEED = 1.55


def _synth_cached(text, voice, speed):
    key = hashlib.md5(f"{text}|{voice}|{speed:.3f}".encode()).hexdigest()[:16]
    path = f"{CACHE}/{key}.npy"
    if os.path.exists(path):
        return np.load(path)
    if voice.startswith("piperS:"):  # v4: síntesis por frase completa (entonación natural)
        _, name, sid = voice.split(":")
        y, sr = piper_tts.synth_sentences(text, name, int(sid), speed)
        n = int(len(y) * 24000 / sr)
        a = np.interp(np.linspace(0, len(y) - 1, n), np.arange(len(y)), y).astype(np.float32)
        a = a / (np.abs(a).max() + 1e-9) * 0.9
    elif voice.startswith("piper:"):
        # voz Piper (locutor real): "piper:<modelo>:<speaker>" -> remuestreo a 24 kHz
        _, name, sid = voice.split(":")
        y, sr = piper_tts.synth(text, name, int(sid), speed)
        n = int(len(y) * 24000 / sr)
        a = np.interp(np.linspace(0, len(y) - 1, n), np.arange(len(y)), y).astype(np.float32)
        a = a / (np.abs(a).max() + 1e-9) * 0.9
    else:
        a, _ = kokoro_tts.synth(text, voice=voice, speed=speed)
        a = a.astype(np.float32)
    # recortar silencios de los extremos
    thr = 0.01
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx):
        a = a[max(0, idx[0] - 600): idx[-1] + 1200]
    np.save(path, a)
    return a


def _resample(a, sr_in=24000, sr_out=SR):
    n = int(len(a) * sr_out / sr_in)
    x = np.linspace(0, len(a) - 1, n)
    return np.interp(x, np.arange(len(a)), a)


def build(lines, voice="em_alex", lead=0.05):
    """lines: (inicio, fin, subtitulo_con_|, texto_hablado).

    Devuelve (vo_44k, captions, envelope_fn, word_times)."""
    total = max(b for (_, b, _, _) in lines) + 1
    vo = np.zeros(int(total * SR))
    items = []
    report = []
    for (a, b, cap, spoken) in lines:
        slot = b - a - lead - 0.12
        speed = BASE_SPEED
        aud = _synth_cached(spoken, voice, speed)
        d = len(aud) / 24000
        if d > slot:
            speed = min(MAX_SPEED, speed * d / slot * 1.02)
            aud = _synth_cached(spoken, voice, speed)
            d = len(aud) / 24000
        report.append((spoken, round(speed, 2), round(d, 2), round(slot, 2)))
        start = a + lead
        sig = _resample(aud)
        i = int(start * SR)
        j = min(len(vo), i + len(sig))
        vo[i:j] += sig[: j - i]
        # subtítulos: trozos separados por |, tiempos por proporción de caracteres
        chunks = [c.strip() for c in cap.split("|") if c.strip()]
        allw = []
        for ci, ch in enumerate(chunks):
            for w in ch.split():
                allw.append((ci, w))
        tot_chars = sum(len(w.strip("*")) + 1 for _, w in allw)
        acc = 0
        times = []
        for _, w in allw:
            times.append(start + d * acc / tot_chars)
            acc += len(w.strip("*")) + 1
        # cada trozo se ve desde su primera palabra hasta la primera del siguiente (o fin del tramo)
        k = 0
        for ci, ch in enumerate(chunks):
            n = len(ch.split())
            t_in = times[k] - 0.08
            t_out = times[k + n] - 0.04 if k + n < len(times) else b
            items.append((max(a, t_in) if ci else a, t_out, ch, [tt for tt in times[k:k + n]]))
            k += n
    caps = Captions([(x[0], x[1], x[2]) for x in items], y=400, size=86)
    # sustituir tiempos de palabra por los reales de la locución
    for it, x in zip(caps.items, items):
        it["times"] = x[3][: len(it["words"])]
        while len(it["times"]) < len(it["words"]):
            it["times"].append(it["times"][-1] if it["times"] else it["a"])
    # envolvente para mover la boca
    hop = SR // 60
    rms = np.sqrt(np.convolve(vo ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    rms = rms / (np.percentile(rms[rms > 1e-4], 95) + 1e-9) if np.any(rms > 1e-4) else rms

    def env(t):
        i = int(t * 60)
        if 0 <= i < len(rms):
            v = rms[i]
            return float(min(1.0, max(0.0, (v - 0.08) * 1.4)))
        return 0.0

    for r in report:
        print(f"  speed {r[1]:.2f}  {r[2]:.2f}s/{r[3]:.2f}s  {r[0]}")
    return vo, caps, env


def word_time(caps, word):
    for it in caps.items:
        for (w, _), tt in zip(it["words"], it["times"]):
            if word.lower() in w.lower():
                return tt
    return None
