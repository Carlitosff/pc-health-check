"""Motor v23 (12/11/2026): ILUSIONES AUDITIVAS procedurales, sincronizadas con la imagen.
shepard_risset(dur, ...) genera el glissando de Shepard–Risset (sonido que parece subir sin fin): N componentes separados una octava que suben
juntos; la amplitud de cada uno sigue una campana en frecuencia logarítmica, así que el más agudo se apaga mientras entra uno grave sin que se note.
layers(t, ...) devuelve, para el instante t, las mismas posiciones (0..1 en el eje log) y amplitudes que suenan: la imagen (barras, hélice) enseña
EXACTAMENTE lo que se oye. Base: Roger N. Shepard, JASA 36(12), 1964 (tonos discretos) y Jean-Claude Risset, JASA 46, 1969 (versión continua).
Uso: core.run(V, scene, OUT, extra_audio=ilusion_audio.mixer_hook(gain_fn)) — gain_fn(t_array) decide cuándo suena y a qué volumen."""
import numpy as np

SR = 44100


def _amp(pos, width=0.18):
    # campana en el eje log (pos 0..1): 0 en los extremos, 1 en el centro
    return np.exp(-0.5 * ((pos - 0.5) / width) ** 2) * np.clip(np.minimum(pos, 1 - pos) * 12, 0, 1)


def layers(t, n=8, rate=1 / 7.0, direction=1):
    """posiciones 0..1 y amplitudes de los n componentes en el instante t (rate = octavas por segundo)."""
    ph = (direction * rate * t) % 1.0
    pos = (np.arange(n) + ph) / n
    return pos, _amp(pos)


def shepard_risset(dur, f_lo=40.0, n=8, rate=1 / 7.0, direction=1, sr=SR):
    t = np.arange(int(dur * sr)) / sr
    out = np.zeros_like(t)
    ph = (direction * rate * t) % 1.0
    for k in range(n):
        pos = (k + ph) / n                      # 0..1 en n octavas
        f = f_lo * 2.0 ** (pos * n)
        # fase integrada por tramos (pos salta de 1 a 0 justo cuando la amplitud es 0: el salto no se oye)
        phase = 2 * np.pi * np.cumsum(f) / sr
        out += _amp(pos) * np.sin(phase)
    out /= np.max(np.abs(out)) + 1e-9
    return out


def mixer_hook(gain_fn, level=0.32, **kw):
    def extra(m, P):
        sig = shepard_risset(P["total"], **kw)
        tt = np.arange(len(sig)) / SR
        g = gain_fn(tt)
        n = min(len(m.buf), len(sig))
        m.buf[:n] += sig[:n] * g[:n] * level
    return extra


if __name__ == "__main__":
    # prueba: la señal final es casi idéntica a la del principio (una vuelta completa = 1/rate segundos)
    s = shepard_risset(14.0)
    a, b = s[:SR], s[int(7.0 * SR):int(8.0 * SR)]
    print("correlación con el inicio tras 1 ciclo:", round(float(np.corrcoef(a, b)[0, 1]), 3))
