"""2203 MITO 3D (leer.js): 'leer con poca luz te estropea la vista'.
Fuente: Vreeman y Carroll, 'Medical myths', BMJ (número de Navidad, 22/12/2007); nota de Indiana University en ScienceDaily (21/12/2007):
'The study authors found no evidence that reading in dim light causes permanent eye damage'; 'eye strain can occur in dim light, causing some
temporarily decreased acuity'; 'after rest the eyes return to their full potential'. Aaron Carroll y Rachel Vreeman, Indiana University School of Medicine."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
V = dict(slug="2203_mito_leer_con_poca_luz", accent=GOLD, drone=0.03, mood="misterio", badge=None, send="ENVÍASELO A QUIEN LEE DE NOCHE",
         rehook=("s3", "ESPERA… LO QUE SÍ PASA"), reveal=("s4", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="Te dijeron que leer con poca luz te estropea la vista para siempre. Pues no es verdad.",
         cap="¿Leer a oscuras te *ESTROPEA* la vista?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Dos médicos de Indiana lo revisaron en el British Medical Journal, en dos mil siete, y no encontraron ningún daño permanente.",
         cap="*BMJ 2007*: | *NINGÚN* daño permanente", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Lo que sí pasa es que los ojos se cansan con poca luz, y durante un rato ves un poco peor.",
         cap="Lo que sí pasa: | ojos *CANSADOS*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero en cuanto descansas un rato, tus ojos vuelven a ver exactamente igual que antes.",
         cap="Descansas… | y ves *IGUAL*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Así que leer en la cama con una linterna no te dejó ciego, como mucho te dejó sin dormir.",
         cap="No te dejó ciego: | te dejó *SIN DORMIR*", hold=0.45),
    dict(id="cta", who="nar", cut=True, say="Comenta si te lo decían en casa, y envíaselo a quien lee hasta las tantas.",
         cap="¿Te lo decían? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 2.4:
        K.tag(c, W / 2, 1800, "VREEMAN Y CARROLL · BMJ · DIC. 2007", lt - 2.4, accent=WHITE, size=30)
    if sid == "s3" and lt > 1.8:
        K.tag(c, W / 2, 1800, "EL CANSANCIO ES TEMPORAL", lt - 1.8, accent=GOLD, size=34)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "leer.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "leer.js", overlay=overlay)
