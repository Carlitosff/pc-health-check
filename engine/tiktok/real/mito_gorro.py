"""1403 MITO 3D (gorro.js): 'por la cabeza se va casi todo el calor'.
Fuentes: Vreeman y Carroll, BMJ dic-2008 (grough 19/12/2008: manual de supervivencia del US Army '40 to 45 per cent'; trajes árticos; en bañador 'only 10 per cent'; Live Science 01/02/2013: 'at most 7 percent to 10 percent'; cabeza ≈7 % de la superficie)."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; RED = 0xFFFF3B4A
V = dict(slug="1403_mito_gorro", accent=RED, drone=0.025, mood="misterio", send="ENVÍASELO A QUIEN TE LO REPETÍA",
         rehook=("s3", "ESPERA… MIRA CÓMO LO MIDIERON"), reveal=("s4", "EL TRUCO"), segs=[
    dict(id="h", who="nar", say="Ponte el gorro, que se te va el calor por la cabeza. Te engañaron.", cap="¿Todo el calor por la cabeza? *TE ENGAÑARON*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Por la cabeza pierdes como mucho un diez por ciento, más o menos lo que le toca por su tamaño.", cap="Por la cabeza: | *como mucho un 10%*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="El mito viene de un manual del ejército de Estados Unidos, que hablaba de casi la mitad.", cap="Manual del ejército: | *40–45%*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y salió de pruebas de frío extremo, con trajes árticos y solo la cabeza fuera.", cap="Trajes árticos: | todo tapado… | menos la *CABEZA*", hold=0.2),
    dict(id="s4", who="nar", cut=True, say="Claro, el calor se iba por el único sitio que quedaba. En bañador, por la cabeza solo se iría un diez por ciento.", cap="En *bañador*: | solo un *10%*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Ponte el gorro igual, que abriga, y envíaselo a quien te lo repetía.", cap="¿Quién te lo repetía? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1":
        K.tag(c, W / 2, 1770, "BMJ 2008 · VREEMAN Y CARROLL", lt - 1.0, accent=GOLD, size=40)
    if sid == "s4" and lt > 3.0:
        hc.big(c, "10%", W / 2, 1650, 150, GOLD, 1.0, 0.0, outline=12)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "gorro.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "gorro.js", overlay=overlay)
