"""1503 MITO 3D (zanahoria.js): 'come zanahoria, que verás en la oscuridad'.
Fuentes: Smithsonian Magazine, 'A WWII Propaganda Campaign Popularized the Myth That Carrots Help You See in the Dark' (John Cunningham, RAF, 'Cat's Eyes'; en 1940 primer piloto británico en derribar un avión con radar A.I. a bordo; 20 derribos, 19 de noche; el Ministerio de Información atribuyó los éxitos a comer mucha zanahoria para esconder el radar; la falta de vitamina A causa ceguera nocturna; más zanahoria no mejora la vista de una persona sana, NYT 2005)."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; ORANGE = 0xFFFF7A1A
V = dict(slug="1503_mito_zanahoria", accent=ORANGE, drone=0.025, mood="misterio", send="ENVÍASELO A QUIEN TE LAS DABA POR ESO",
         rehook=("s3", "ESPERA… EL SECRETO ERA OTRO"), reveal=("s4", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="Cómete la zanahoria, que verás en la oscuridad. Te engañaron, y fue a propósito.", cap="¿Zanahoria para ver de noche? *TE ENGAÑARON*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Ese mito lo extendió el gobierno británico en la Segunda Guerra Mundial, para esconder un secreto.", cap="Lo extendió | el *gobierno británico*, | en la *Segunda Guerra Mundial*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Su piloto John Cunningham derribaba aviones de noche, y le llamaban Ojos de Gato.", cap="*John Cunningham*: | derribos *de noche*. | Le llamaban *Ojos de Gato*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Decían que era por comer mucha zanahoria, pero el secreto era un radar nuevo que llevaba en el avión.", cap="¿Zanahorias? | No: un *RADAR* | en el avión", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Si te falta vitamina A, sí ves peor de noche. Pero si ya comes normal, comer más zanahoria no te hace ver mejor.", cap="Sin *vitamina A*, ves peor. | Comer *MÁS*… | *no ayuda*", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Cómetela igual, porque es muy sana, y envíaselo a quien te las daba por eso.", cap="¿Quién te lo decía? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1":
        K.tag(c, W / 2, 1770, "MINISTERIO DE INFORMACIÓN · REINO UNIDO", lt - 1.2, accent=GOLD, size=34)
    if sid == "s2":
        K.tag(c, W / 2, 1770, "RAF · 1940 · 19 DERRIBOS DE NOCHE", lt - 1.0, accent=GOLD, size=38)
    if sid == "s4":
        K.tag(c, W / 2, 1790, "FUENTE: SMITHSONIAN MAGAZINE", lt - 1.0, accent=WHITE, size=32)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "zanahoria.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "zanahoria.js", overlay=overlay)
