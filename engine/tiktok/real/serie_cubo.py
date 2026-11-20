"""2804 SERIE 3D (cubo.js): ¿Y si la Tierra fuera un cubo? Parte 17 de ¿QUÉ PASARÍA SI…? (prometida en la parte 16).
Jesse Berezovsky (profesor de Física, Case Western Reserve University; Gizmodo 31/12/2013, desde Quora): 'you would perceive that you were
standing on a slope', 'all the way up to about 50 degrees from the horizontal'; océanos en 'a lens shape' en el centro de cada cara; 'the large
majority of the cube's surface is outside the atmosphere'; zona habitable 'a narrow ring around the oceans'. Ask a Mathematician (09/05/2011):
'Something the size of the Earth, however, is doomed to be hella round' ('the planet is pulled into a sphere').
Cálculo propio (cubo de densidad uniforme con la misma masa y volumen que la Tierra, 48³ masas puntuales): inclinación de la gravedad por la
diagonal de una cara 0° en el centro → 22° a mitad → 44,7° al 90 % → 50,8° casi en la esquina; peso 0,99 → 0,68."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import numpy as np
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A


def _tilt(f, n=32):
    c = (np.arange(n) + .5) / n - .5
    X, Y, Z = np.meshgrid(c, c, c, indexing='ij'); P = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    p = np.array([f * .5, f * .5, .504]); d = P - p; r = np.linalg.norm(d, axis=1); v = (d / r[:, None] ** 3).sum(0)
    return np.degrees(np.arccos(-v[2] / np.linalg.norm(v)))


assert _tilt(0) < .5 and 40 < _tilt(.9) < 49 and 46 < _tilt(.97) < 56   # 'unos cincuenta grados' cerca de las esquinas
V = dict(slug="2804_tierra_cubo", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 17",
         send="ENVÍASELO A QUIEN QUIERA VIVIR EN UN CUBO", rehook=("s3", "ESPERA… ¿Y EL MAR?"), reveal=("s5", "EL FINAL"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra fuera un cubo? Caminarías siempre cuesta arriba, aunque el suelo sea plano.",
         cap="¿Y si la Tierra fuera *UN CUBO*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="La gravedad tiraría hacia el centro del cubo, y no hacia tus pies.",
         cap="La gravedad tira | hacia *EL CENTRO*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Cada cara parecería una cuesta, y junto a las esquinas tendría casi cincuenta grados.",
         cap="Junto a las esquinas: | *~50° DE CUESTA*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Los océanos rodarían cuesta abajo, hasta formar un mar redondo en el centro de cada cara.",
         cap="6 caras: *6 MARES*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Las esquinas quedarían sin aire, y solo se podría vivir junto a cada mar.",
         cap="Solo se vive | en un *ANILLO*", hold=0.3),
    dict(id="s5", who="nar", cut=True, say="Pero su propia gravedad lo aplastaría, hasta volverlo otra vez una esfera.",
         cap="Su gravedad | lo vuelve *UNA ESFERA*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Sígueme para la parte dieciocho, la gravedad de la Luna, y comenta en qué cara vivirías.",
         cap="*Parte 18*: | la gravedad *de la Luna*"),
])


TILT = [(0, 0), (.1, 4.2), (.2, 8.7), (.3, 12.9), (.4, 17.4), (.5, 22), (.6, 26.7), (.7, 32.1), (.8, 37.8), (.9, 44.7), (.97, 50.8)]  # = cubo.js


def _ss(a, b, x):
    x = min(1, max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x)


def tilt_at(f):
    f = min(.97, max(0, f))
    for (a, ta), (b, tb) in zip(TILT, TILT[1:]):
        if f <= b:
            return ta + (tb - ta) * (f - a) / (b - a)
    return 50.8


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; d = sg["b"] - sg["a"]
    if sid in ("s1", "s2"):   # mismo recorrido que cubo.js: f = fracción de la diagonal de la cara
        f = .12 * _ss(.6, d, lt) if sid == "s1" else .12 + .83 * _ss(.2, d - .4, lt)
        a = tilt_at(f)
        K.pill(c, W / 2, 1560, f"CUESTA: {round(a)}°", 64, bg=0xEE10131F, fg=0xFFFFC23A if a < 40 else 0xFFFF4D5E)
    if sid == "s2" and lt > 1.0:
        K.tag(c, W / 2, 1840, "JESSE BEREZOVSKY · CASE WESTERN · 2013", lt - 1.0, accent=WHITE, size=30)
    if sid == "s1" and lt > 1.0:
        K.tag(c, W / 2, 1840, "MISMA MASA Y VOLUMEN (CÁLCULO PROPIO)", lt - 1.0, accent=WHITE, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "cubo.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "cubo.js", overlay=overlay, keep=True)
