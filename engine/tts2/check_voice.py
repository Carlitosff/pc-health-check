"""Control de la locución sin oírla: Whisper transcribe cada segmento y avisa de los que se entienden mal.
Uso: from check_voice import check; check(V["segs"]). Devuelve [(coincidencia, texto, transcripción)] por debajo de MIN.
Whisper falla algo en frases cortas: un aviso significa 'reescribe la frase y repite', no que esté mal seguro."""
import difflib, re, sys
sys.path.insert(0, "/home/claude/tts2")
import supertonic_tts as S

BASE = "/home/claude/tts2/sherpa-onnx-whisper-base/base-"
MIN = 0.8
_r = None


def _norm(t):
    return re.sub(r"[^\wáéíóúñü ]", " ", S.normalize(t.replace("x", " por ")).lower()).split()


def check(segs, speed=1.1):
    global _r
    import sherpa_onnx as so
    if _r is None:
        _r = so.OfflineRecognizer.from_whisper(encoder=BASE + "encoder.int8.onnx", decoder=BASE + "decoder.int8.onnx",
                                               tokens=BASE + "tokens.txt", language="es", task="transcribe", num_threads=2)
    bad = []
    for sg in segs:
        t = sg.get("say")
        if not t:
            continue
        a, sr, _ = S.synth(t, speed=speed)
        s = _r.create_stream()
        s.accept_waveform(sr, a)
        _r.decode_stream(s)
        h = s.result.text.strip()
        ref, hyp = _norm(t), _norm(h)
        m = sum(b.size for b in difflib.SequenceMatcher(None, ref, hyp).get_matching_blocks()) / max(1, len(ref))
        if m < MIN:
            bad.append((round(m, 2), t, h))
    return bad
