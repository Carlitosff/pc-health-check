"""3603 MITO 3D (pez.js): '¿Tu pez de colores lo olvida todo a los tres segundos?' → NO.
Fuentes: Mental Floss (Matt Soniak, 24/05/2010): 'In a 2003 study at the School of Psychology at the University of Plymouth, fish were trained to
push a lever to earn a food reward', 'When the lever was fixed to work only for one hour a day, the fish learned to activate it at the correct time';
Discover Wildlife (BBC Wildlife): 'In experiments at Plymouth University ... learned to push a lever in order to get food', 'goldfish can retain
memories for at least three months'. Mental Floss (Technion, Israel): peces entrenados con un sonido de comida; 'Five months later ... the sound was
broadcast over a loudspeaker in the sea and the fish returned'. (No se da el nombre del investigador de Plymouth: no verificado.)"""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; RED = 0xFFFF6A4A; GREEN = 0xFF4ADE80; CYAN = 0xFF8FD0FF
V = dict(slug="3603_mito_pez_3_segundos", accent=GOLD, drone=0.02, mood="luz", send="ENVÍASELO A QUIEN TENGA UN PEZ",
         dare=("s1", "MÁNDASELO A QUIEN TENGA PECERA", 1840), vote=("s3", ("SÍ", "NO"), 1, 1580),
         rehook=("s2", "ESPERA… AHORA SOLO FUNCIONA UNA HORA"), reveal=("s3", "LA RESPUESTA"),
         sfx=[("s1", 1.6, "click", .18), ("s1", 5.0, "click", .18), ("h", .4, "bubble", .12), ("h", 1.6, "bubble", .1), ("cta", .6, "bubble", .12)],
         segs=[
    dict(id="h", who="nar", say="¿De verdad tu pez de colores lo olvida todo a los tres segundos?",
         cap="¿Tu pez lo olvida todo *EN 3 SEGUNDOS*?", hold=0.25),
    dict(id="s1", who="nar", cut=True, say="En dos mil tres, en la Universidad de Plymouth, enseñaron a unos peces a empujar una palanca para comer.",
         cap="Plymouth, *2003*: | una *PALANCA* con comida", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Luego, la palanca solo funcionaba una hora al día, y aprendieron a empujarla justo a esa hora.",
         cap="Solo funcionaba | *UNA HORA AL DÍA*", hold=0.25),
    dict(id="s3", who="nar", cut=True, say="Si lo olvidara todo en tres segundos, no sabría qué hora es. Y pueden recordar cosas al menos tres meses.",
         cap="Recuerdan | *AL MENOS 3 MESES*", hold=0.25),
    dict(id="s4", who="nar", cut=True, say="En Israel, otros peces aprendieron a acudir a un sonido, y cinco meses después, en el mar, volvieron al oírlo.",
         cap="Cinco meses después, | *VOLVIERON AL SONIDO*", hold=0.25),
    dict(id="cta", who="nar", cut=True, say="Comenta cuántos años tiene tu pez, y envíaselo a quien tenga uno en casa.",
         cap="¿Cuántos años tiene el tuyo? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; d = sg["b"] - sg["a"]
    if sid == "s1" and lt > 2.6:
        K.tag(c, W / 2, 1840, "UNIVERSIDAD DE PLYMOUTH · 2003", lt - 2.6, accent=WHITE, size=32)
    if sid == "s2" and lt > 1.2:
        K.pill(c, W / 2, 1580, "VERDE = FUNCIONA · 1 HORA AL DÍA", 42, bg=0xEE000000, fg=GREEN, scale=K.ease_back(K.prog(lt, 1.2, 1.5)))
    if sid == "s4" and lt > 2.4:
        K.pill(c, W / 2, 1580, "5 MESES DESPUÉS", 52, bg=0xEE000000, fg=CYAN, scale=K.ease_back(K.prog(lt, 2.4, 2.7)))
        K.tag(c, W / 2, 1840, "TECHNION, ISRAEL · VÍA MENTAL FLOSS", lt - 2.4, accent=WHITE, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1), {k: round(v[0], 1) for k, v in K.plan(V)["tl"].items()})
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "pez.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "pez.js", overlay=overlay, keep=True)
