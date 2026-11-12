"""2003 MITO 3D (arana.js): 'te tragas 8 arañas al año mientras duermes'.
Fuentes: Scientific American ('Do People Really Swallow 8 Spiders a Year While They Sleep?'): Rod Crawford, conservador de arácnidos del Burke Museum
de Seattle: 'Vibrations are a big slice of spiders' sensory universe'; 'A slumbering person breathes, has a beating heart and perhaps snores, all of which
create vibrations that warn spiders of danger'; 'A sleeping person is not something a spider would willingly approach'. Mental Floss (Matt Soniak,
06/06/2013): con Crawford 'the number of ingested creepy crawlies drops right to zero'; el supuesto origen (columna de Lisa Holst, PC Professional 1993)
'The columnist, the column and the magazine don't seem to exist'; 'The story about how the story got made up may itself be made up'.
El guion dice 'prácticamente cero' y 'la revista que se cita como origen no aparece por ningún sitio'."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; GREEN = 0xFF4ADE80
V = dict(slug="2003_mito_ocho_aranas", accent=GOLD, drone=0.03, mood="misterio", badge=None, send="ENVÍASELO A QUIEN LE DAN MIEDO",
         rehook=("s3", "ESPERA… MIRA LA ARAÑA"), reveal=("s4", "DE DÓNDE SALIÓ"), segs=[
    dict(id="h", who="nar", say="Te han dicho que cada año te tragas ocho arañas mientras duermes. Es mentira.", cap="¿Te tragas *8 ARAÑAS* al año durmiendo?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Rod Crawford, experto en arañas del Museo Burke de Seattle, dice que la cifra real es prácticamente cero.",
         cap="Museo Burke, Seattle: | prácticamente *CERO*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Mientras duermes, respiras, te late el corazón y a veces roncas, y todo eso hace vibrar la cama.",
         cap="Respiras, *te late el corazón*, | *roncas*…", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Las arañas notan esas vibraciones con las patas, y para ellas eres un peligro enorme, así que se alejan.",
         cap="La araña *lo nota*… | y *SE VA*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y lo más curioso es que la revista que se cita como origen del dato no aparece por ningún sitio.",
         cap="El origen: | una revista | que *NO APARECE*", hold=0.45),
    dict(id="cta", who="nar", cut=True, say="Comenta si te lo creías, y envíaselo a quien le dan miedo las arañas.", cap="¿Te lo creías? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2" and lt > 1.2:
        K.tag(c, W / 2, 1800, "CADA LATIDO HACE VIBRAR LA CAMA", lt - 1.2, accent=GOLD, size=36)
    if sid == "s3" and lt > 1.0:
        K.tag(c, W / 2, 1800, "LAS ARAÑAS 'OYEN' CON LAS PATAS", lt - 1.0, accent=WHITE, size=36)
    if sid == "s4" and lt > 2.0:
        K.tag(c, W / 2, 1800, "SCIENTIFIC AMERICAN · MENTAL FLOSS 2013", lt - 2.0, accent=WHITE, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "arana.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "arana.js", overlay=overlay)
