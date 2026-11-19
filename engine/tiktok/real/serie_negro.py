"""2704 SERIE 3D (negro.js): ¿Y si el Sol se convirtiera en un agujero negro? Parte 16 de ¿QUÉ PASARÍA SI…? (prometida en la parte 15).
NASA Imagine the Universe (Black holes, educadores): 'the only thing that would change would be the Earth's temperature. The gravity we feel
here on Earth from the black hole Sun would not change'. IFLScience (James Felton, 24/04/2024, citando a la NASA): 'Earth's orbit around the
Sun would be unchanged'; 'would shrink down to just 3 kilometers (1.9 miles) in radius'; 'The Sun is simply too small to form a black hole'.
Cálculo propio: radio de Schwarzschild 2GM/c² = 2,95 km; la luz tarda 1 UA / c = 499 s = 8 min 19 s (≈ 8 min 20 s)."""
import math, sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
GM, C, AU = 1.32712440018e20, 299792458.0, 1.495978707e11
rs = 2 * GM / C ** 2
assert round(rs / 1000) == 3 and 2900 < rs < 3000
assert 495 < AU / C < 505            # 8 min 19 s
V = dict(slug="2704_sol_agujero_negro", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 16",
         send="ENVÍASELO A QUIEN CREA QUE NOS TRAGARÍA", rehook=("s2", "ESPERA… NO NOS TRAGA"), reveal=("s4", "EL FINAL"), segs=[
    dict(id="h", who="nar", say="¿Y si el Sol se convirtiera de golpe en un agujero negro? ¿Nos tragaría?",
         cap="¿Y si el Sol fuera un *AGUJERO NEGRO*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Todo el Sol, que mide setecientos mil kilómetros, quedaría en una bola de solo tres de radio.",
         cap="De *700.000 km* | a solo *3 km*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Y lo raro es que la Tierra no caería: tendría la misma masa, así que seguiría dando vueltas igual.",
         cap="La Tierra *NO CAE*. | Misma masa, *misma órbita*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Lo que sí se apaga es la luz: a los ocho minutos, sería de noche para siempre, y todo se helaría.",
         cap="*8 minutos* después: | noche *PARA SIEMPRE*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Tranquilo: nuestro Sol es demasiado pequeño para convertirse en un agujero negro.",
         cap="El Sol *NO PUEDE*: | es *demasiado pequeño*", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Sígueme para la parte diecisiete: ¿y si la Tierra fuera un cubo? Comenta qué echarías de menos, la luz o el calor.",
         cap="*Parte 17*: | ¿y si la Tierra fuera *un cubo*?"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2" and lt > 1.2:
        K.tag(c, W / 2, 770, "NASA · IMAGINE THE UNIVERSE", lt - 1.2, accent=WHITE, size=30)
    if sid == "s1" and lt > 1.0:
        K.tag(c, W / 2, 1840, "RADIO DE SCHWARZSCHILD: 2,95 KM (CÁLCULO PROPIO)", lt - 1.0, accent=WHITE, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "negro.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "negro.js", overlay=overlay, keep=True)
