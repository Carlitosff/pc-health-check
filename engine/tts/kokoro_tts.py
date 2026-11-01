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


# ---------------------------------------------------------------- v6 (01/11 noche): voz menos plana
# Carlos: em_santa sigue sonando 'plana/robótica' y no le convence el timbre.
# (1) modelo Kokoro v1.0 COMPLETO fp32 (kokoro-v1.0.onnx, GitHub thewh1teagle/kokoro-onnx) en vez del q8 cuantizado
#     (la cuantización mete aspereza metálica);
# (2) síntesis por FRASE entera (hasta . ? !), no por cláusula: Kokoro hace la curva de entonación de toda la frase
#     (antes cada trozo empezaba y acababa con el mismo tono -> 'lectura');
# (3) las comas siguen respetándose: se buscan los huecos de silencio internos y se ALARGAN hasta el mínimo pedido;
# (4) timbre: mezcla de estilos 'em_santa+em_alex@0.4' (vector de estilo interpolado).
_sess32 = None


def session32():
    global _sess32
    if _sess32 is None:
        so = ort.SessionOptions(); so.intra_op_num_threads = 2
        _sess32 = ort.InferenceSession(BASE + "kokoro-v1.0.onnx", so, providers=["CPUExecutionProvider"])
    return _sess32


def _style(voice, n):
    """voice: 'em_santa' o mezcla 'em_santa+em_alex@0.4' (peso de la 2ª)."""
    def load(v):
        return np.fromfile(BASE + f"node_modules/kokoro-js/voices/{v}.bin", dtype=np.float32).reshape(-1, 1, 256)
    if "+" in voice:
        a, rest = voice.split("+")
        b, w = (rest.split("@") + ["0.5"])[:2]
        w = float(w)
        return (1 - w) * load(a)[n] + w * load(b)[n]
    return load(voice)[n]


def synth32(text, voice="em_santa", speed=1.0, lang="es"):
    ph = phonemize_keep_punct(text, lang)
    ids = [VOCAB[c] for c in ph if c in VOCAB][:510]
    sess = session32()
    names = [i.name for i in sess.get_inputs()]
    feed = {names[0]: np.array([[0, *ids, 0]], dtype=np.int64), names[1]: _style(voice, len(ids)),
            names[2]: np.array([speed], dtype=np.float32)}
    return sess.run(None, feed)[0].reshape(-1).astype(np.float32)


def _stretch_gaps(a, n_commas, min_gap=0.22, sr=24000):
    """Alarga los n huecos internos más largos (las comas) hasta min_gap s."""
    if n_commas <= 0 or len(a) < sr // 4:
        return a
    env = np.convolve(np.abs(a), np.ones(240) / 240, mode="same")
    quiet = env < 0.02 * env.max()
    gaps, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if i > sr * 0.15 and j < len(a) - sr * 0.15 and (j - i) > 0.03 * sr:
                gaps.append((j - i, i, j))
            i = j
        else:
            i += 1
    gaps = sorted(sorted(gaps, reverse=True)[:n_commas], key=lambda g: g[1])
    out, last = [], 0
    for ln, i, j in gaps:
        mid = (i + j) // 2
        out.append(a[last:mid])
        extra = int(min_gap * sr) - ln
        if extra > 0:
            out.append(np.zeros(extra, np.float32))
        last = mid
    out.append(a[last:])
    return np.concatenate(out)


def synth_natural(text, voice="em_santa+em_alex@0.4", speed=1.0, lang="es"):
    text = text.replace("...", "…")
    sents = re.findall(r"[^.?!…]+[.?!…]*", text)
    out = []
    for s in sents:
        s = s.strip()
        if not re.search(r"\w", s):
            continue
        a = synth32(s, voice=voice, speed=speed, lang=lang)
        idx = np.where(np.abs(a) > 0.012 * (np.abs(a).max() + 1e-9))[0]
        if len(idx):
            a = a[max(0, idx[0] - 240): idx[-1] + 720]
        a = _stretch_gaps(a, len(re.findall(r"[,;:]", s)))
        n = min(len(a) // 2, 192)
        a[:n] *= np.linspace(0, 1, n); a[-n:] *= np.linspace(1, 0, n)
        out += [a, np.zeros(int(PAUSES.get(s[-1], 0.3) * 24000), np.float32)]
    return (np.concatenate(out[:-1]) if out else np.zeros(1, np.float32)), None
