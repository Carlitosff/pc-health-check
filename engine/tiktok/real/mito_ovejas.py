"""1903 MITO 3D (ovejas.js): 'contar ovejas te ayuda a dormir'.
Fuente: Harvey, A. G. y Payne, S. (2002), 'The management of unwanted pre-sleep thoughts in insomnia: distraction with imagery versus general
distraction', Behaviour Research and Therapy 40(3): 267-277, Departamento de Psicología Experimental, Universidad de Oxford. Insomnes en tres grupos
(imaginar una escena tranquila, contar ovejas / distracción general, nada). Mental Floss (Matt Soniak, 21/04/2010): 'they fell asleep 20 minutes sooner,
on average, than they did when sheep counting or doing nothing' y 'took longer than usual to fall asleep on the nights they were instructed to count sheep'.
Gizmodo (Lily Hay Newman, 15/12/2013): 50 insomnes en tres grupos; Harvey: 'Picturing an engaging scene takes up more brain space than the same dirty old sheep.'"""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; GREEN = 0xFF4ADE80
V = dict(slug="1903_mito_contar_ovejas", accent=GOLD, drone=0.03, mood="luz", badge=None, send="ENVÍASELO A QUIEN CUENTA OVEJAS",
         rehook=("s3", "ESPERA… LAS OVEJAS PIERDEN"), reveal=("s4", "LO QUE SÍ FUNCIONA"), segs=[
    dict(id="h", who="nar", say="Te dijeron que contar ovejas te ayuda a dormir. Pues te engañaron.", cap="¿Contar ovejas te ayuda a *DORMIR*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="En el año dos mil dos, en la Universidad de Oxford, lo probaron con personas que tenían insomnio.",
         cap="*Oxford, 2002*: | lo probaron con | *insomnes*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Unas noches contaban ovejas, otras imaginaban una playa tranquila, y otras no hacían nada.",
         cap="*Ovejas*, | una *playa*… | o *nada*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Contando ovejas tardaban más de lo normal en dormirse, porque es tan aburrido que no frena las preocupaciones.",
         cap="Con ovejas: | *TARDABAN MÁS*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Imaginando la playa, se dormían unos veinte minutos antes, porque esa escena te ocupa la cabeza entera.",
         cap="Con la playa: | *20 minutos antes*", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Comenta qué imaginas tú para dormirte, y envíaselo a quien todavía cuenta ovejas.",
         cap="¿Qué imaginas tú? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 1.0:
        K.tag(c, W / 2, 1790, "HARVEY Y PAYNE · BEHAV RES THER 2002", lt - 1.0, accent=GOLD, size=32)
    if sid == "s4" and lt > 1.0:
        K.tag(c, W / 2, 1790, "UNIVERSIDAD DE OXFORD", lt - 1.0, accent=GREEN, size=36)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "ovejas.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "ovejas.js", overlay=overlay)
