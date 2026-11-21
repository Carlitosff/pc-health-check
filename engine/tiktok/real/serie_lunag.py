"""2904 SERIE 3D (lunag.js): ¿Y si la Tierra tuviera la gravedad de la Luna? Parte 18 de ¿QUÉ PASARÍA SI…? (prometida en la 17: 'la gravedad de la Luna').
NASA Glenn (Beginner's Guide to Aeronautics, 'Moon', act. 07/07/2025): gravedad media en la superficie 1,62 m/s² = 0,165 g.
OpenStax Astronomy 9.1: 'about one-sixth Earth's surface gravity—too low to retain an atmosphere'; 'the lower the gravity, the easier it is
for the gas to leak away into space'. Cálculo propio (la Tierra igual de grande, solo cambia g a 1,62): 80 kg en la báscula → 13 kg;
salto de 50 cm → 3,0 m (h ∝ 1/g); un vaso desde 1,5 m tarda 0,55 s → 1,36 s (t = √(2h/g), ×2,46). Canasta de baloncesto: aro a 3,05 m."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; GREEN = 0xFF4ADE80
g0, g1 = 9.81, 1.62
kg = 80 * g1 / g0; jump = 0.5 * g0 / g1; t0 = math.sqrt(2 * 1.5 / g0); t1 = math.sqrt(2 * 1.5 / g1)
assert round(kg) == 13 and round(jump, 1) == 3.0 and round(t0, 2) == .55 and round(t1, 2) == 1.36 and round(g0 / g1) == 6 and t1 / t0 > 2
V = dict(slug="2904_tierra_gravedad_de_la_luna", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 18",
         send="ENVÍASELO A QUIEN SE QUEJA DE LA BÁSCULA", dare=("s2", "RETA A UN AMIGO A SALTAR", 1840),
         rehook=("s3", "ESPERA… ¿Y SI SE TE CAE?"), reveal=("s4", "EL PROBLEMA"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra tuviera la gravedad de la Luna? Súbete a la báscula: ochenta kilos marcarían trece.",
         cap="¿Y con la gravedad *DE LA LUNA*?", hold=0.1),
    dict(id="s1", who="nar", cut=True, say="La gravedad de la Luna es unas seis veces más débil, así que todo pesaría seis veces menos.",
         cap="Gravedad *÷6*", hold=0.1),
    dict(id="s2", who="nar", cut=True, say="Tu salto de cincuenta centímetros llegaría a tres metros, casi hasta el aro de una canasta.",
         cap="*50 cm* → *3 METROS*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y si se te cae un vaso, tardaría más del doble en llegar al suelo.",
         cap="Un vaso tarda | *más del doble*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Pero con tan poca gravedad, el aire se escaparía al espacio con más facilidad: por eso la Luna casi no tiene.",
         cap="El *AIRE* | se escaparía", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="Sígueme: en la parte diecinueve, la gravedad de Júpiter. Comenta hasta dónde saltarías.",
         cap="*Parte 19*: | gravedad de *JÚPITER*. | ¿Cuánto saltarías? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 2.2:
        K.tag(c, W / 2, 1840, "LUNA: 1,62 m/s² · TIERRA: 9,81 · NASA", lt - 2.2, accent=WHITE, size=30)
    if sid == "s2" and lt > 3.2:
        K.tag(c, W / 2, 1840, "MISMO SALTO · CÁLCULO PROPIO", lt - 3.2, accent=WHITE, size=30)
    if sid == "s3" and lt > .8:
        K.tag(c, W / 2, 1840, "DESDE 1,5 m: 0,55 s → 1,36 s", lt - .8, accent=GOLD, size=32)
    if sid == "s4" and lt > 2.6:
        K.tag(c, W / 2, 1840, "OPENSTAX: 'DEMASIADO BAJA PARA RETENER ATMÓSFERA'", lt - 2.6, accent=GREEN, size=26)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "lunag.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "lunag.js", overlay=overlay, keep=True)
