"""1604 SERIE 3D (anillos.js): ¿Y si la Tierra tuviera anillos? Parte 5 de ¿QUÉ PASARÍA SI…?
Física: anillos en el plano del ecuador → desde 40° N se ven como un arco hacia el sur; de noche la parte fuera de la sombra de la Tierra sigue iluminada;
en invierno el Sol está al otro lado del ecuador y los anillos dan sombra al hemisferio de invierno (como en Saturno).
Dato real: Monash University, Andy Tomkins et al., Earth and Planetary Science Letters (sept. 2024): hace 466 M años, 21 cráteres de impacto, todos a menos de 30° del ecuador;
un asteroide roto dentro del límite de Roche habría formado un anillo; 'could have cast a shadow' y contribuido al enfriamiento del Hirnantiense (especulación, no se dice)."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
V = dict(slug="1604_tierra_con_anillos", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 5", send="ENVÍASELO A QUIEN LE GUSTE MIRAR EL CIELO",
         rehook=("s3", "ESPERA… Y EN INVIERNO"), reveal=("s4", "PASÓ DE VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra tuviera anillos como Saturno? Desde España, los verías así.", cap="La Tierra con *ANILLOS*: así los verías desde España", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Estarían encima del ecuador, así que desde Madrid serían un arco enorme hacia el sur.", cap="Sobre el *ecuador*: | desde Madrid, | un *arco hacia el sur*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="De noche seguirían brillando con el Sol, menos donde les cae la sombra de la Tierra.", cap="De noche *brillan*… | menos donde cae | la *sombra de la Tierra*", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="Y en invierno, su sombra caería sobre tu mitad del planeta, y haría todavía más frío.", cap="En invierno, | su *sombra* cae | sobre *tu mitad*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Y puede que ya pasara. Un estudio de dos mil veinticuatro cree que hace cuatrocientos sesenta y seis millones de años tuvimos uno, por veintiún cráteres junto al ecuador.", cap="Hace *466 millones* de años: | *21 cráteres*, | todos cerca del *ecuador*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Sígueme, que en la parte seis acercamos la Luna hasta que se rompe. Comenta si querrías anillos.", cap="*Parte 6*: la Luna | se acerca… | ¿Anillos? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s4" and lt > 4.0:
        hc.big(c, "21 CRÁTERES", W / 2, 1560, 110, 0xFFFF4D6D, 1.0, 0.0, outline=12)
    if sid == "s4" and lt > 1.0:
        K.tag(c, W / 2, 1790, "MONASH UNIVERSITY · EARTH AND PLANETARY SCIENCE LETTERS · 2024", lt - 1.0, accent=GOLD, size=28)
    if sid == "s3" and lt > 1.2:
        K.tag(c, W / 2, 1790, "COMO EN SATURNO: SOMBRA EN EL HEMISFERIO DE INVIERNO", lt - 1.2, accent=GOLD, size=28)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "anillos.js", stills=sys.argv[2].split(","))
    elif sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    else:
        v3d_run.run3d(V, "anillos.js", overlay=overlay)
