"""2303 MITO 3D (pelo.js): '¿salir con el pelo mojado te resfría?' → tu madre tenía MEDIA razón.
El resfriado lo causa un virus (sin virus no hay resfriado). Estudio de los pies fríos: Claire Johnson y Ron Eccles, Common Cold Centre, Universidad de Cardiff,
'Acute cooling of the feet and the onset of common cold symptoms', Family Practice, nov. 2005 (PubMed 16286463). HealthDay (Robert Preidt, 14/11/2005):
'180 volunteers… soak their feet in ice-cold water or place them in an empty bowl for 20 minutes'; '29 percent developed cold symptoms over the next four to five days,
compared to 9 percent'; 'many people are mildly infected but show no symptoms'; 'a pronounced constriction of the blood vessels in the nose and shuts off the warm blood
that supplies the white cells'; 'the dormant infection has taken hold'. No hay estudio con el pelo mojado: el guion lo dice ('algo parecido')."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; ICE = 0xFF4DE3FF
V = dict(slug="2303_mito_pelo_mojado_resfriado", accent=GOLD, drone=0.03, mood="misterio", badge=None, send="ENVÍASELO A QUIEN SALE CON EL PELO MOJADO",
         rehook=("s3", "ESPERA… MIRA EL RESULTADO"), reveal=("s4", "LA EXPLICACIÓN"), segs=[
    dict(id="h", who="nar", say="¿Salir con el pelo mojado te resfría? Te dijeron que sí, pero la respuesta es más rara.",
         cap="¿Salir con el pelo *MOJADO* te resfría?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="El frío solo no te resfría, porque el resfriado lo causa un virus.",
         cap="Lo causa un *VIRUS*", hold=0.15),
    dict(id="s2", who="nar", cut=True, say="Pero en dos mil cinco, en Cardiff, la mitad de ciento ochenta voluntarios metió los pies en agua helada.",
         cap="Cardiff, 2005: | *PIES* en agua helada", hold=0.15),
    dict(id="s3", who="nar", cut=True, say="En los cinco días siguientes se resfrió el veintinueve por ciento de ellos, y solo el nueve por ciento de los demás.",
         cap="*29 %* | frente a | *9 %*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Muchos ya llevaban el virus dormido, y el frío cierra los vasos de la nariz y le deja vía libre.",
         cap="El virus ya estaba: | el frío le *ABRE LA PUERTA*", hold=0.25),
    dict(id="cta", who="nar", cut=True, say="Tu madre tenía media razón. Comenta si te lo decía, y envíaselo a quien sale con el pelo mojado.",
         cap="¿Te lo decían? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2" and lt > 2.6:
        K.tag(c, W / 2, 1840, "JOHNSON Y ECCLES · FAMILY PRACTICE · 2005", lt - 2.6, accent=WHITE, size=30)
    if sid == "s3" and lt > 2.0:
        K.tag(c, W / 2, 1840, "20 MINUTOS CON LOS PIES EN AGUA HELADA", lt - 2.0, accent=ICE, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "pelo.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "pelo.js", overlay=overlay)
