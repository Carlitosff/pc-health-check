"""2604 SERIE 3D (caida.js): ¿Y si la Tierra se parara en su órbita? Parte 15 de ¿QUÉ PASARÍA SI…? (prometida en la parte 14).
Universe Today (Fraser Cain, 08/07/2016, cifras de Dave Rothstein, Cornell 'Ask an Astronomer'): 'the whole journey would take about 65 days',
'It would take 41 days to cross the orbit of Venus, and on day 57, we'd cross the orbit of Mercury'. Smithsonian (Smart News, con cálculos de
Aatish Bhatia en Wired) da 'about 64 days'. Cálculo propio de caída libre radial desde 1 UA: t = (π/2)·√(r³/2GM) = 64,6 días; Venus (0,723 UA)
día 41,2; Mercurio (0,387 UA) día 57,0; a los 30 días solo hemos caído un 14 % (r = 0,86 UA). Velocidad orbital ≈ 30 km/s (2π·1 UA / 1 año).
Desde la órbita de Mercurio el Sol se ve 1/0,387 = 2,6 veces más grande."""
import math, sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
GM, AU = 1.32712440018e20, 1.495978707e11
tff = math.pi / 2 * math.sqrt(AU ** 3 / (2 * GM)) / 86400
def t_of(x):
    e = math.acos(math.sqrt(x)); return tff * 2 / math.pi * (e + math.sin(e) * math.cos(e))
assert round(tff) == 65 and round(t_of(.723)) == 41 and round(t_of(.387)) == 57 and abs(t_of(.86) - 30) < .3
assert round(2 * math.pi * AU / (365.25 * 86400) / 1000) == 30 and round(1 / .387, 1) == 2.6
V = dict(slug="2604_tierra_se_para_en_su_orbita", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 15",
         send="ENVÍASELO A QUIEN DIGA QUE NO PASA NADA", rehook=("s3", "ESPERA… AHORA VA MUY RÁPIDO"), reveal=("s4", "EL FINAL"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra se parara en su órbita? Caeríamos al Sol en unos sesenta y cinco días.",
         cap="¿Y si la Tierra *SE PARA*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Vamos de lado a treinta kilómetros por segundo, y por eso no caemos. Si frenamos, el Sol tira de nosotros.",
         cap="Vamos de lado | a *30 km/s*. | Si frenamos, *caemos*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="El primer mes casi no se nota: solo hacemos un catorce por ciento del camino.",
         cap="Primer mes: | solo un *14 %*", hold=0.2),
    dict(id="s3", who="nar", cut=True, say="Luego caemos cada vez más deprisa: el día cuarenta y uno pasamos la órbita de Venus, y el cincuenta y siete, la de Mercurio.",
         cap="Día *41*: Venus. | Día *57*: Mercurio", hold=0.2),
    dict(id="s4", who="nar", cut=True, say="Y el día sesenta y cinco, la Tierra se estrella contra el Sol.",
         cap="Día *65*: | *CHOQUE*", hold=0.7),
    dict(id="cta", who="nar", cut=True, say="Sígueme para la parte dieciséis: el Sol se vuelve un agujero negro. ¿Qué harías tú en esos días?",
         cap="*Parte 16*: | el Sol, *agujero negro*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s3" and lt > 1.0:
        K.tag(c, W / 2, 1840, "UNIVERSE TODAY · 2016 · Y CÁLCULO PROPIO", lt - 1.0, accent=WHITE, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "caida.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "caida.js", overlay=overlay, keep=True)
