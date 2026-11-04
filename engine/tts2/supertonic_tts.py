"""Voz v8 (04/11/2026, elegida por Carlos: voz 5 = Supertonic 3, sid 4, 'que respete más las pausas').

Se sintetiza frase a frase con silencio exacto entre frases. Dentro de la frase, '...' en comas y dos puntos hace parar
al modelo y luego se ajustan esos huecos a PAUSES. No se sintetiza por cláusulas: en la prueba con Whisper los trozos
cortos salían mal ('sin parpadear' -> 'sin papaya').
"""
import os, re
import numpy as np

BASE = "/home/claude/tts2/sherpa-onnx-supertonic-3-tts-int8-2026-05-11/"
SID = 4
STEPS = 20
# Duración mínima del silencio por signo (s). Solo se alarga, nunca se acorta.
PAUSES = {",": 0.30, ";": 0.38, ":": 0.38, "—": 0.30, ".": 0.55, "?": 0.55, "!": 0.50, "…": 0.60}
FRAME = 0.005  # s
MIN_GAP = 0.12  # s; por debajo son oclusivas, no pausas
MIN_WORDS = 3
RETRIES = 3
RATE = 15.5  # letras por segundo de voz a speed 1,1, medido en frases largas
_tts = None


def available():
    return os.path.exists(BASE + "vector_estimator.int8.onnx")


def _engine():
    global _tts
    if _tts is None:
        import sherpa_onnx as so
        cfg = so.OfflineTtsConfig(model=so.OfflineTtsModelConfig(
            supertonic=so.OfflineTtsSupertonicModelConfig(
                duration_predictor=BASE + "duration_predictor.int8.onnx",
                text_encoder=BASE + "text_encoder.int8.onnx",
                vector_estimator=BASE + "vector_estimator.int8.onnx",
                vocoder=BASE + "vocoder.int8.onnx",
                tts_json=BASE + "tts.json",
                unicode_indexer=BASE + "unicode_indexer.bin",
                voice_style=BASE + "voice.bin"),
            num_threads=2, provider="cpu"))
        _tts = so.OfflineTts(cfg)
    return _tts


# ------------------------------------------------------------------ números y unidades a palabras
UNITS = [(r"\bkm/h\b", "kilómetros por hora"), (r"\bm/s\b", "metros por segundo"), (r"\bkm\b", "kilómetros"),
         (r"\bcm\b", "centímetros"), (r"\bmm\b", "milímetros"), (r"\bkg\b", "kilos"), (r"°\s?C\b", " grados"),
         (r"\s?%", " por ciento"), (r"\s?€", " euros"), (r"\s?\$", " dólares"), (r"\s?×\s?", " por ")]


def normalize(text):
    from num2words import num2words
    t = text.replace("...", "…")

    def num(m):
        s = m.group(0)
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):  # 1.668 = mil seiscientos
            return num2words(int(s.replace(".", "")), lang="es")
        if re.fullmatch(r"\d+,\d+", s):
            a, b = s.split(",")
            return f"{num2words(int(a), lang='es')} coma {num2words(int(b), lang='es')}"
        return num2words(int(s), lang="es")

    t = re.sub(r"\d{1,3}(?:\.\d{3})+|\d+,\d+|\d+", num, t)
    for pat, rep in UNITS:
        t = re.sub(pat, " " + rep if not rep.startswith(" ") else rep, t)
    return re.sub(r"\s+", " ", t).strip()


# ------------------------------------------------------------------ pausas
def mark_pauses(text, style="puntos"):
    """Hace que el propio modelo pare en comas y dos puntos, sin cortar el audio. Con '...' deja huecos de 0,3-0,45 s
    en el sitio correcto; a posteriori solo se ajustan esos huecos. Cortar por posición estimada caía a mitad de
    palabra ('metáfora en mi|tes')."""
    if style == "puntos":
        return re.sub(r"\s*[,;:—]+(?=\s)", "...", text)
    return text


def _gaps(a, sr, minlen=MIN_GAP):
    """Silencios internos de al menos minlen s: (inicio, fin) en muestras. Las oclusivas (p, t, k) dan <0,1 s."""
    hop = int(FRAME * sr)
    n = len(a) // hop
    if n == 0:
        return []
    rms = np.sqrt(np.mean(a[: n * hop].reshape(n, hop) ** 2, axis=1))
    quiet = rms < max(0.012, 0.035 * np.percentile(rms, 95))
    out, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if i > 0 and j < n and (j - i) * FRAME >= minlen:
                out.append((i * hop, j * hop))
            i = j
        else:
            i += 1
    return out


def stretch_pauses(a, sr, text):
    """text = texto ORIGINAL normalizado. Alarga hasta PAUSES los huecos reales del modelo, en orden. Nunca corta voz:
    si un signo no tiene hueco, se queda como está y se anota. Devuelve (audio, informe)."""
    marks = [(m.start(), m.group(0)[0]) for m in re.finditer(r"[,;:—.?!…]+(?=\s)", text)]
    gaps = _gaps(a, sr)
    if not marks or not gaps:
        return a, [(ch, None, None) for _, ch in marks]
    # Sobran huecos: se queda con los más largos. Faltan: cada hueco busca su signo más cercano por posición.
    letters = np.cumsum([c.isalnum() for c in text])
    total = max(1, int(letters[-1]))
    exp = [letters[p] / total for p, _ in marks]
    if len(gaps) > len(marks):
        gaps = sorted(sorted(gaps, key=lambda g: g[0] - g[1])[: len(marks)])
    assign = {}
    if len(gaps) == len(marks):
        assign = {i: i for i in range(len(gaps))}
    else:
        free = set(range(len(marks)))
        for gi, (s, e) in enumerate(gaps):
            pos = (s + e) / 2 / len(a)
            mi = min(free, key=lambda k: abs(exp[k] - pos))
            free.discard(mi)
            assign[gi] = mi
    report = {i: (ch, None, None) for i, (_, ch) in enumerate(marks)}
    out, cur = [], 0
    for gi, (s, e) in enumerate(gaps):
        mi = assign[gi]
        ch = marks[mi][1]
        want, have = int(PAUSES[ch] * sr), e - s
        report[mi] = (ch, round(have / sr, 3), round(max(have, want) / sr, 3))
        if have < want:
            out += [a[cur:e], np.zeros(want - have, np.float32)]
            cur = e
    out.append(a[cur:])
    return np.concatenate(out), [report[i] for i in sorted(report)]


def _sentences(text):
    """Frases completas. Las de 1-2 palabras ('Comenta.') van con la siguiente, porque solas el modelo las pronuncia mal."""
    parts = [x.strip() for x in re.findall(r"[^.?!…]+[.?!…]*", text) if re.search(r"\w", x)]
    out, buf = [], ""
    for x in parts:
        buf = (buf + " " + x).strip()
        if len(buf.split()) >= MIN_WORDS:
            out.append(buf)
            buf = ""
    if buf:
        if out:
            out[-1] += " " + buf
        else:
            out.append(buf)
    return out


def _trim(a, sr):
    idx = np.flatnonzero(np.abs(a) > 0.012 * (np.abs(a).max() + 1e-9))
    return a[max(0, idx[0] - int(0.02 * sr)): idx[-1] + int(0.05 * sr)] if len(idx) else a


def synth(text, speed=1.1, sid=SID, steps=STEPS, style="puntos"):
    """Sintetiza frase a frase con un silencio exacto entre ellas; dentro de cada frase para el propio modelo.
    Devuelve (audio float32, sample_rate, informe de pausas)."""
    import sherpa_onnx as so
    clean = normalize(text)
    g = so.GenerationConfig()
    g.sid, g.num_steps, g.speed = sid, steps, speed
    g.extra["lang"] = "es"
    out, report, sr = [], [], 44100
    for sent in _sentences(clean):
        # El modelo atropella las frases cortas: si va más rápido que el ritmo objetivo, se regenera más despacio.
        g.speed = speed
        target = RATE * speed / 1.1
        for _ in range(3):
            r = _engine().generate(mark_pauses(sent, style), g)
            a = np.array(r.samples, dtype=np.float32)
            if not len(a):
                raise RuntimeError("Supertonic no generó audio")
            sr = r.sample_rate
            a = _trim(a, sr)
            quiet = sum(e - s for s, e in _gaps(a, sr))
            rate = sum(c.isalnum() for c in sent) / max(0.2, (len(a) - quiet) / sr)
            if rate <= target * 1.06 or g.speed <= 0.6:
                break
            g.speed = max(0.6, g.speed * target / rate)
        b, rep = stretch_pauses(a, sr, sent)
        # El modelo no es determinista: si se ha saltado una pausa, se reintenta y se queda la toma con menos huecos sin hacer.
        for _ in range(RETRIES):
            if not any(x[1] is None for x in rep):
                break
            r = _engine().generate(mark_pauses(sent, style), g)
            a2 = _trim(np.array(r.samples, dtype=np.float32), sr)
            b2, rep2 = stretch_pauses(a2, sr, sent)
            if sum(x[1] is None for x in rep2) < sum(x[1] is None for x in rep):
                b, rep = b2, rep2
        last = sent.rstrip()[-1]
        out += [b, np.zeros(int(PAUSES.get(last, PAUSES["."]) * sr), np.float32)]
        report += rep + [(last, "frase", PAUSES.get(last, PAUSES["."]))]
    return np.concatenate(out[:-1]), sr, report[:-1]
