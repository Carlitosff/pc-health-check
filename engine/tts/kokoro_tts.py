"""TTS local con Kokoro-82M (ONNX q8) + espeak-ng para fonemas en español."""
import json, subprocess, sys, re
import numpy as np, onnxruntime as ort, wave

BASE = "/home/claude/tts/"
VOCAB = json.load(open(BASE + "config.json"))["vocab"]
_sess = None


def session():
    global _sess
    if _sess is None:
        so = ort.SessionOptions(); so.intra_op_num_threads = 2
        _sess = ort.InferenceSession(BASE + "kokoro-q8.onnx", so, providers=["CPUExecutionProvider"])
    return _sess


def phonemize(text, lang="es"):
    out = subprocess.run(["espeak-ng", "-q", "--ipa=3", "-v", lang, "--", text], capture_output=True, text=True).stdout
    ph = " ".join(out.split())
    ph = ph.replace("_", "")
    # conservar la puntuación del texto original para la prosodia
    return ph


def phonemize_keep_punct(text, lang="es"):
    parts = re.split(r"([¡¿!?.,;:…—])", text)
    res = ""
    for p in parts:
        if not p.strip():
            continue
        if re.fullmatch(r"[¡¿!?.,;:…—]", p):
            if p in "¡¿":
                continue
            res = res.rstrip() + p + " "
        else:
            res += phonemize(p, lang) + " "
    return res.strip()


def synth(text, voice="em_alex", speed=1.15, lang="es", out=None):
    ph = phonemize_keep_punct(text, lang)
    ids = [VOCAB[c] for c in ph if c in VOCAB][:510]
    vs = np.fromfile(BASE + f"node_modules/kokoro-js/voices/{voice}.bin", dtype=np.float32).reshape(-1, 1, 256)
    style = vs[len(ids)]
    toks = np.array([[0, *ids, 0]], dtype=np.int64)
    sess = session()
    names = [i.name for i in sess.get_inputs()]
    feed = {names[0]: toks, names[1]: style, names[2]: np.array([speed], dtype=np.float32)}
    audio = sess.run(None, feed)[0].reshape(-1)
    if out:
        a = np.clip(audio, -1, 1)
        with wave.open(out, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes((a * 32767).astype(np.int16).tobytes())
    return audio, ph


PAUSES = {",": 0.24, ";": 0.32, ":": 0.32, ".": 0.44, "?": 0.48, "!": 0.42, "…": 0.55}


def synth_paced(text, voice="em_santa", speed=1.0, lang="es"):
    """Voz v5 (31/10, elegida por Carlos: em_santa): síntesis por cláusula CON su puntuación (Kokoro mantiene el tono
    de continuación en las comas) + silencios explícitos para que se respeten comas y puntos."""
    text = text.replace("...", "…")
    parts = re.findall(r"[^,;:.?!…]+[,;:.?!…]*", text)
    out = []
    for p in parts:
        p = p.strip()
        if not re.search(r"\w", p):
            continue
        a, _ = synth(p, voice=voice, speed=speed, lang=lang)
        a = a.astype(np.float32)
        idx = np.where(np.abs(a) > 0.012 * (np.abs(a).max() + 1e-9))[0]
        if len(idx):
            a = a[max(0, idx[0] - 240): idx[-1] + 720]
        n = min(len(a) // 2, 192)
        if n:
            a[:n] *= np.linspace(0, 1, n); a[-n:] *= np.linspace(1, 0, n)
        punct = p[-1] if p[-1] in PAUSES else ""
        out += [a, np.zeros(int(PAUSES.get(punct, 0.08) * 24000), np.float32)]
    return (np.concatenate(out[:-1]) if out else np.zeros(1, np.float32)), None


if __name__ == "__main__":
    a, ph = synth(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "em_alex", out=sys.argv[3] if len(sys.argv) > 3 else "/tmp/claude-0/t.wav")
    print(ph); print(len(a) / 24000, "s")
