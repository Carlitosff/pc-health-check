"""1304 SERIE 3D (luna.js): ¿Y si desaparece la Luna? Parte 2 de ¿QUÉ PASARÍA SI…?
Fuentes: The Star/dpa 24/07/2026 (Martin Knapmeyer, DLR: el Sol tira 'about half as strong'; noches 'considerably darker'; especies que se guían por la Luna; el eje 'could fluctuate wildly').
ScienceABC: 'roughly a third of the tidal range'. Laskar, Joutel & Robutel, Nature 1993 (0–85°, caótico; hay cálculos posteriores más moderados, por eso 'DISCUTIDO')."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE, clamp
GOLD = 0xFFFFC23A
V = dict(slug="1304_si_desaparece_la_luna", accent=GOLD, drone=0.03, mood="misterio", badge="¿QUÉ PASARÍA SI…? · PARTE 2", send="ENVÍASELO A UN AMIGO",
         rehook=("s3", "ESPERA… LO PEOR VA LENTO"), segs=[
    dict(id="h", who="nar", say="Esta noche desaparece la Luna. Y lo peor no es quedarte a oscuras.", cap="Esta noche *DESAPARECE* la Luna", hold=0.1),
    dict(id="s1", who="nar", cut=True, say="Las noches serían mucho más oscuras, y muchos animales que se guían por su luz se quedarían perdidos.", cap="Noches *mucho más oscuras* | y animales *perdidos*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Pero mira el mar. Las mareas se quedarían en un tercio, porque ya solo empujaría el Sol.", cap="Mareas: *UN TERCIO* | Solo empuja el *Sol*", hold=0.5),
    dict(id="s3", who="nar", cut=True, say="Y lo peor llega despacio. La Luna mantiene casi fijo el eje de la Tierra, y sin ella, según un cálculo de hace décadas, se tambalearía sin control.",
         cap="La Luna sujeta | el *EJE* de la Tierra. | Sin ella, *se tambalea*", hold=0.2),
    dict(id="s4", who="nar", cut=True, say="A lo largo de millones de años, tendrías veranos e inviernos extremos.", cap="*Millones de años* | de estaciones *EXTREMAS*", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="Sígueme, porque en la parte tres saltamos todos a la vez. Comenta qué crees que pasaría.", cap="*Parte 3*: saltamos | *TODOS a la vez*. | ¿Qué pasaría? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2":
        K.tag(c, W / 2, 1745, "DE ESTO… A ESTO: UN TERCIO", lt - 2.4, accent=0xFF40FFE0, size=46)
    if sid == "s3":
        K.tag(c, W / 2, 1770, "LASKAR, NATURE 1993 · DISCUTIDO", lt - 2.6, accent=GOLD, size=38)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "luna.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "luna.js", overlay=overlay)
