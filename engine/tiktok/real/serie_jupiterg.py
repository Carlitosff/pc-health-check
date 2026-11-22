"""3004 SERIE 3D (jupiterg.js): ¿Y si la Tierra tuviera la gravedad de Júpiter? Parte 19 de ¿QUÉ PASARÍA SI…? (prometida en la 18).
NASA NSSDC, Jupiter Fact Sheet: 'Gravity (mean, 1 bar) (m/s2): 25.92' frente a Tierra 9.82; 'Surface Pressure: >>1000 bars' (no hay
superficie sólida: el valor es a 1 bar, en lo alto de las nubes). Cálculo propio (la Tierra igual de grande, solo cambia g): ×2,64;
80 kg → 211 kg; salto de 50 cm → 19 cm (h ∝ 1/g); un vaso desde 1,5 m tarda 0,55 s → 0,34 s (t = √(2h/g))."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; GREEN = 0xFF4ADE80; CYAN = 0xFF4DE3FF
g0, g1 = 9.82, 25.92
ratio = g1 / g0; kg = 80 * ratio; jump = 50 / ratio; t0 = math.sqrt(2 * 1.5 / g0); t1 = math.sqrt(2 * 1.5 / g1)
assert round(ratio, 1) == 2.6 and round(kg) == 211 and round(jump) == 19 and round(t0, 2) == .55 and round(t1, 2) == .34 and t1 < t0 / 1.5
V = dict(slug="3004_tierra_gravedad_de_jupiter", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 19",
         send="ENVÍASELO A QUIEN SE QUEJA DE LA BÁSCULA", dare=("s2", "RETA A UN AMIGO A CALCULARLO", 1840),
         rehook=("s3", "ESPERA… ¿Y SI SE TE CAE?"), reveal=("s4", "EL PROBLEMA"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra tuviera la gravedad de Júpiter? En la báscula, ochenta kilos marcarían doscientos once.",
         cap="¿Y con la gravedad *DE JÚPITER*?", hold=0.1),
    dict(id="s1", who="nar", cut=True, say="En lo alto de sus nubes, la gravedad es dos veces y media la de aquí, y todo pesaría muchísimo más.",
         cap="Gravedad *×2,6*", hold=0.1),
    dict(id="s2", who="nar", cut=True, say="Tu salto de cincuenta centímetros se quedaría en diecinueve, y casi no despegarías del suelo.",
         cap="*50 cm* → *19 cm*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y si se te cae un vaso, llegaría al suelo en un tercio de segundo, sin tiempo para cogerlo.",
         cap="El vaso cae en | *un tercio de segundo*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Pero en Júpiter de verdad ni podrías ponerte de pie, porque no tiene suelo: es gas y nubes.",
         cap="Júpiter | *NO TIENE SUELO*", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="Multiplica tu peso por dos coma seis y coméntalo. En la parte veinte, la Tierra tumbada como Urano.",
         cap="Tu peso *×2,6*: | *COMENTA* | Parte 20: *URANO*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 2.2:
        K.tag(c, W / 2, 1840, "JÚPITER: 25,92 m/s² · TIERRA: 9,82 · NASA", lt - 2.2, accent=WHITE, size=30)
    if sid == "s2" and lt > 3.0:
        K.tag(c, W / 2, 1840, "MISMO SALTO · CÁLCULO PROPIO", lt - 3.0, accent=WHITE, size=30)
    if sid == "s3" and lt > .8:
        K.tag(c, W / 2, 1840, "DESDE 1,5 m: 0,55 s → 0,34 s", lt - .8, accent=GOLD, size=32)
    if sid == "s4" and lt > 2.6:
        K.tag(c, W / 2, 1840, "NASA: PRESIÓN EN LA 'SUPERFICIE' > 1.000 BAR", lt - 2.6, accent=GREEN, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "jupiterg.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "jupiterg.js", overlay=overlay, keep=True)
