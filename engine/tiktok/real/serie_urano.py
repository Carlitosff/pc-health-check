"""3104 SERIE 3D (urano.js): ¿Y si la Tierra estuviera tumbada como Urano? Parte 20 de ¿QUÉ PASARÍA SI…? (prometida en la 19).
EarthSky (Deborah Byrd, 'Seasons of Uranus'): 'Uranus's axis is tilted at 98 degrees!', 'Its year is 84 Earth-years long', un polo 'faces the sun
continuously for 21 years'; timeanddate ('Uranus: The Sideways Planet'): 'a tilt of around 97.8 degrees', 'about 84 Earth years'.
Cálculo propio (Tierra con oblicuidad 98° ≡ 82° retrógrada, Madrid 40,4° N, sin refracción): en el solsticio el Sol a medianoche está a
φ + δ − 90 = 32,4° de altura; el Sol no se pone mientras δ > 49,6° → ~81 días; simétrico en invierno, ~81 días sin salir. El guion dice 'unos ochenta'."""
import sys, math
import numpy as np
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; CYAN = 0xFF4DE3FF
phi, eps = 40.4, 180 - 98
mid = phi + eps - 90
L = np.linspace(0, 2 * np.pi, 365250, endpoint=False)
dec = np.degrees(np.arcsin(np.sin(np.radians(eps)) * np.sin(L)))
days_up, days_dark = (dec > 90 - phi).mean() * 365.25, (dec < -(90 - phi)).mean() * 365.25
assert round(mid) == 32 and 78 < days_up < 83 and 78 < days_dark < 83, (mid, days_up, days_dark)
V = dict(slug="3104_tierra_tumbada_como_urano", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 20",
         send="ENVÍASELO A QUIEN NO PUEDE DORMIR CON LUZ", dare=("s3", "PREGÚNTALE SI AGUANTARÍA", 1840),
         rehook=("s3", "ESPERA… MIRA LA HORA"), reveal=("s4", "EL INVIERNO"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra estuviera tumbada, como Urano? En Madrid habría casi tres meses sin noche.",
         cap="¿Y si la Tierra se *TUMBA*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Urano gira casi de lado, con el eje inclinado noventa y ocho grados.",
         cap="Urano: | *98 grados*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Con la Tierra así, en junio todo el hemisferio norte miraría al Sol sin parar.",
         cap="En junio, el norte | *MIRA AL SOL*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="En Madrid, a medianoche, el Sol seguiría a unos treinta grados de altura, durante unos ochenta días seguidos.",
         cap="Medianoche: | *SOL A 32°*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Y en invierno serían otros ochenta días sin amanecer, a oscuras, como en el Polo Norte.",
         cap="*80 días* | sin amanecer", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta si aguantarías ochenta días sin noche. En la parte veintiuno, la Tierra gira al revés.",
         cap="¿Aguantarías? *COMENTA* | Parte 21: *AL REVÉS*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 1.5:
        K.tag(c, W / 2, 1840, "URANO: 98° · EARTHSKY / TIMEANDDATE", lt - 1.5, accent=CYAN, size=30)
    if sid == "s3" and lt > 2.0:
        K.tag(c, W / 2, 1840, f"CÁLCULO PROPIO: {mid:.0f}° · {days_up:.0f} DÍAS", lt - 2.0, accent=GOLD, size=32)


JOB = dict(mid=round(mid, 1))
if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "urano.js", stills=sys.argv[2].split(","), extra_job=JOB)
    else:
        v3d_run.run3d(V, "urano.js", overlay=overlay, extra_job=JOB, keep=True)
