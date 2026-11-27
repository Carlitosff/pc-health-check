"""3503 MITO 3D (perro.js): '¿Tu perro pone cara de culpable porque sabe que lo ha hecho mal?' → NO.
Fuente: Alexandra Horowitz, Barnard College (Nueva York), 'Disambiguating the "guilty look": Salient prompts to a familiar dog behaviour',
Behavioural Processes 81(3): 447 (2009); ScienceDaily 11/06/2009: los dueños salían tras prohibir al perro comerse una golosina; a veces se les
decía que se la había comido aunque no fuera verdad ('What the owners were told, however, often did not correlate with reality');
'Dogs looked most "guilty" if they were admonished by their owners'; los obedientes reñidos 'looked more "guilty" than those that had, in fact,
eaten the treat'; 'the dog's guilty look is a response to the owner's behavior'. (No se dice el número de perros: no verificado en la fuente leída.)"""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; RED = 0xFFFF6A4A; GREEN = 0xFF4ADE80
V = dict(slug="3503_mito_perro_culpable", accent=GOLD, drone=0.02, mood="luz", send="ENVÍASELO A QUIEN RIÑE A SU PERRO",
         dare=("s1", "MÁNDASELO A QUIEN TENGA PERRO", 1840), vote=("s3", ("SÍ", "NO"), 1, 1580),
         rehook=("s3", "ESPERA… ESTE PERRO NO HIZO NADA"), reveal=("s3", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Tu perro pone esta cara de culpable porque sabe que ha hecho algo malo?",
         cap="¿Tu perro *SABE* que lo hizo mal?", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="En dos mil nueve, la científica Alexandra Horowitz puso a prueba esa cara con perros y sus dueños.",
         cap="Lo midieron | en *2009*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="El dueño le prohibía tocar una galleta y salía de la sala, y luego le contaban si se la había comido, a veces mintiendo.",
         cap="A veces | *LE MENTÍAN* al dueño", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y las caras más culpables no eran de los que se la comieron, sino de los que recibían la bronca siendo inocentes.",
         cap="Más culpable: | *EL QUE RECIBE LA BRONCA*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Esa cara es una reacción a tu enfado, no una confesión de lo que ha hecho.",
         cap="Reacciona *A TU ENFADO*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta qué rompió tu perro la última vez, y envíaselo a alguien que riñe a su perro.",
         cap="¿Qué rompió tu perro? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 3.0:
        K.tag(c, W / 2, 1840, "A. HOROWITZ · BEHAVIOURAL PROCESSES · 2009", lt - 3.0, accent=WHITE, size=30)
    if sid == "s2" and lt > 4.0:
        K.pill(c, W / 2, 1580, "LA GALLETA SE LA LLEVABAN ELLOS", 42, bg=0xEE000000, fg=GOLD, scale=K.ease_back(K.prog(lt, 4.0, 4.3)))
    if sid == "s4" and lt > .8:
        K.pill(c, W / 2, 1580, "MÁS BRONCA = MÁS CARA DE CULPA", 44, bg=0xEE000000, fg=RED, scale=K.ease_back(K.prog(lt, .8, 1.1)))


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1), {k: round(v[0], 1) for k, v in K.plan(V)["tl"].items()})
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "perro.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "perro.js", overlay=overlay, keep=True)
