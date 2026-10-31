"""TTS local con voces Piper (VITS, grabadas de locutores reales) en onnxruntime + espeak-ng.
Sintetiza por cláusulas y las une con pausas naturales."""
import os, re, json, subprocess, numpy as np, onnxruntime as ort
BASE = os.path.dirname(os.path.abspath(__file__))
_m = {}

def model(name):
    if name not in _m:
        d = f"{BASE}/vits-piper-{name}"
        so = ort.SessionOptions(); so.intra_op_num_threads = 2
        sess = ort.InferenceSession(f"{d}/{name}.onnx", so, providers=["CPUExecutionProvider"])
        cfg = json.load(open(f"{d}/{name}.onnx.json"))
        _m[name] = (sess, cfg)
    return _m[name]

def phonemes(text, voice):
    out = subprocess.run(["espeak-ng", "-q", "--ipa=3", "-v", voice, "--", text], capture_output=True, text=True).stdout
    return " ".join(out.replace("_", "").split())

PAUSE = {",": 0.12, ";": 0.2, ":": 0.2, ".": 0.26, "?": 0.28, "!": 0.26, "…": 0.36}

def _gen(sess, cfg, ph, sid, length, noise=0.667, noise_w=0.8):
    idm = cfg["phoneme_id_map"]
    ids = list(idm["^"]) + list(idm["_"])
    for ch in ph:
        if ch in idm:
            ids += idm[ch] + idm["_"]
    ids += idm["$"]
    feed = {"input": np.array([ids], np.int64), "input_lengths": np.array([len(ids)], np.int64),
            "scales": np.array([noise, length, noise_w], np.float32)}
    if cfg.get("num_speakers", 1) > 1:
        feed["sid"] = np.array([sid], np.int64)
    return sess.run(None, feed)[0].reshape(-1).astype(np.float32)

def synth(text, name="es_ES-sharvard-medium", sid=0, speed=1.0, noise=0.667, noise_w=0.8):
    sess, cfg = model(name)
    sr = cfg["audio"]["sample_rate"]
    text = text.replace("...", "…")
    parts = re.findall(r"[^,;:.?!…]+[,;:.?!…]*", text)
    out = []
    for p in parts:
        p = p.strip()
        if not re.search(r"\w", p):
            continue
        punct = p[-1] if p[-1] in PAUSE else ""
        ph = phonemes(p, cfg["espeak"]["voice"])
        if punct and not ph.endswith(punct):
            ph += punct
        x = _gen(sess, cfg, ph, sid, 1.0 / speed, noise, noise_w)
        idx = np.where(np.abs(x) > 0.01 * np.abs(x).max())[0]
        if len(idx):
            x = x[max(0, idx[0] - int(0.015 * sr)): idx[-1] + int(0.05 * sr)]
        n = min(len(x) // 2, int(0.008 * sr))
        if n:
            x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
        out += [x, np.zeros(int(PAUSE.get(punct, 0.06) * sr), np.float32)]
    y = np.concatenate(out[:-1]) if out else np.zeros(1, np.float32)
    return y, sr


def synth_sentences(text, name="es_ES-davefx-medium", sid=0, speed=1.0, noise=0.72, noise_w=0.95):
    """Voz v4 (31/10): síntesis por FRASE completa (no por cláusula). Piper mantiene la curva de entonación a través
    de las comas en vez de cerrar cada trozo con tono descendente (eso sonaba a robot leyendo listas). Más variación
    (noise/noise_w) y pausas de frase un poco más largas."""
    sess, cfg = model(name)
    sr = cfg["audio"]["sample_rate"]
    text = text.replace("...", "…")
    parts = re.findall(r"[^.?!…]+[.?!…]*", text)
    out = []
    for p in parts:
        p = p.strip()
        if not re.search(r"\w", p):
            continue
        punct = p[-1] if p[-1] in PAUSE else ""
        ph = phonemes(p, cfg["espeak"]["voice"])
        x = _gen(sess, cfg, ph, sid, 1.0 / speed, noise, noise_w)
        idx = np.where(np.abs(x) > 0.01 * np.abs(x).max())[0]
        if len(idx):
            x = x[max(0, idx[0] - int(0.015 * sr)): idx[-1] + int(0.06 * sr)]
        n = min(len(x) // 2, int(0.008 * sr))
        if n:
            x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
        out += [x, np.zeros(int({"?": 0.34, ".": 0.32, "!": 0.3, "…": 0.42}.get(punct, 0.1) * sr), np.float32)]
    y = np.concatenate(out[:-1]) if out else np.zeros(1, np.float32)
    return y, sr
