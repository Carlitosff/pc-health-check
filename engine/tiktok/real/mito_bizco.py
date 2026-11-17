"""2503 MITO 3D (bizco.js): 'si te pones bizco, te quedas así'.
Fuentes: American Academy of Ophthalmology, 'Five vision myths' (aao.org): 'crossing the eyes won't force them to stay that way'; los ojos
desviados pueden venir de enfermedad, vista sin corregir o daño en músculos o nervios. UT Austin 'Think Twice' (Nathan Ngo, 29/04/2023):
'Using these muscles to cross your eyes is a form of exercise and is not harmful'; 'Once you uncross your eyes and give them time to rest, they will feel normal'.
Mirar un dedo que se acerca a la nariz = convergencia (los mismos músculos de mirar de cerca)."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
V = dict(slug="2503_mito_bizco", accent=GOLD, drone=0.03, mood="luz", badge=None, send="ENVÍASELO A QUIEN SE PONE BIZCO",
         rehook=("s3", "ESPERA… ¿Y LA MOLESTIA?"), reveal=("s4", "LO QUE SÍ IMPORTA"), dare=("s2", "HAZLO CON UN AMIGO"), segs=[
    dict(id="h", who="nar", say="¿Te decían que si te ponías bizco te quedabas así para siempre? No es verdad.",
         cap="¿Si te pones *BIZCO* te quedas así?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="La Academia Americana de Oftalmología lo dice claro: cruzar los ojos no hace que se queden cruzados.",
         cap="Oftalmólogos: | *NO* se quedan así", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Haz la prueba: acerca un lápiz a tu nariz y míralo. Ya estás bizco, y al apartarlo vuelves a la normalidad.",
         cap="Acerca un lápiz | a tu *NARIZ*… | y míralo", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Usas los mismos músculos que para mirar de cerca. Si molesta, es cansancio, y al descansar se pasa.",
         cap="¿Molesta? | Es *CANSANCIO*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="El estrabismo de verdad tiene otras causas, como una vista sin corregir, y lo revisa un oftalmólogo.",
         cap="El estrabismo real | tiene *OTRAS* causas", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta si te lo decían en casa, y envíaselo a quien siempre se pone bizco.",
         cap="¿Te lo decían? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 2.4:
        K.tag(c, W / 2, 1800, "AMERICAN ACADEMY OF OPHTHALMOLOGY", lt - 2.4, accent=WHITE, size=30)
    if sid == "s3" and lt > 2.2:
        K.tag(c, W / 2, 1800, "UNIV. DE TEXAS · ABRIL 2023", lt - 2.2, accent=GOLD, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "bizco.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "bizco.js", overlay=overlay)
