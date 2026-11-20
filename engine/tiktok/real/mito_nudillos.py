"""2803 MITO 3D (nudillos.js): '¿Crujirte los dedos te da artrosis?' → un médico lo probó en sus propias manos más de 60 años.
Improbable Research (05/11/2009, 'Interview with Dr. Knuckle-cracker'): Donald Unger se crujió 'the knuckles of his left hand — but never
cracking the knuckles of his right hand — every day for more than sixty (60) years'; 2009 Ig Nobel de Medicina. The Tech (MIT, 02/10/2009):
'He had defied his mother's words' y su frase 'Mother, you were wrong!'. The Conversation ('Monday's medical myth: cracking your knuckles
causes arthritis'): carta en Arthritis and Rheumatism (1998); 'right hand remained arthritis-free throughout his life. And so did his left';
el ruido: 'the brief formation of a bubble of gases' que 'rapidly implodes'. Es una sola persona: se dice tal cual en el guion."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
V = dict(slug="2803_mito_crujirse_los_dedos", accent=GOLD, drone=0.02, mood="misterio", send="ENVÍASELO A QUIEN SE LOS CRUJE",
         rehook=("s3", "ESPERA… ¿60 AÑOS?"), reveal=("s4", "EL RESULTADO"), dare=("s2", "ENVÍASELO A QUIEN TE RIÑE", 1840),
         segs=[
    dict(id="h", who="nar", say="¿Crujirte los dedos provoca artrosis? Un médico lo probó en sus manos durante sesenta años.",
         cap="¿Crujirte los dedos *DA ARTROSIS*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Su madre le decía que si se crujía los dedos acabaría con artrosis.",
         cap="Su madre | se lo *REPETÍA*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Así que Donald Unger se crujió solo los dedos de la mano izquierda, y nunca los de la derecha.",
         cap="Solo la *IZQUIERDA*, | nunca la *DERECHA*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Lo hizo cada día durante más de sesenta años, y luego comparó las dos manos.",
         cap="*Más de 60 años* | cada día", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Ninguna de las dos tenía artrosis, y en dos mil nueve ganó el premio Ig Nobel de Medicina.",
         cap="*NINGUNA* tenía artrosis", hold=0.4),
    dict(id="s5", who="nar", cut=True, say="El crujido es solo una burbuja de gas que revienta dentro de la articulación.",
         cap="El ruido: | una *BURBUJA DE GAS*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta si te crujes los dedos, y envíaselo a quien te reñía por hacerlo.",
         cap="¿Te los crujes? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s4" and lt > 1.0:
        K.tag(c, W / 2, 1840, "DONALD UNGER · IG NOBEL DE MEDICINA 2009", lt - 1.0, accent=GOLD, size=32)
    if sid == "s5" and lt > 1.0:
        K.tag(c, W / 2, 1840, "UNA SOLA PERSONA · CARTA EN ARTHRITIS & RHEUMATISM, 1998", lt - 1.0, accent=WHITE, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "nudillos.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "nudillos.js", overlay=overlay, keep=True)
