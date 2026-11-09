"""1703 MITO 3D (agua.js): ¿8 vasos de agua al día? Te lo contaron a medias.
Fuente: nota de prensa de Dartmouth Medical School (08/08/2002) sobre la revisión invitada de Heinz Valtin en American Journal of Physiology:
no encontró estudios que respaldaran el '8x8'; la recomendación de la Food and Nutrition Board era ~1 ml por caloría y la frase siguiente decía
'most of this quantity is contained in prepared foods'; 'caffeinated drinks, such as most coffee, tea and soft drinks, may indeed be counted'.
Matiz de seguridad en el guion: adulto sano; con calor o deporte, más."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
BLUE = 0xFF3FB4FF; GOLD = 0xFFFFC23A
V = dict(slug="1703_mito_ocho_vasos", accent=BLUE, drone=0.02, mood="luz", badge=None, send="ENVÍASELO A QUIEN VA CON LA BOTELLA",
         rehook=("s2", "ESPERA… FALTA UNA FRASE"), reveal=("s3", "LA FRASE"), segs=[
    dict(id="h", who="nar", say="¿Tienes que beber ocho vasos de agua al día? Te lo contaron a medias.", cap="¿*8 VASOS* de agua al día?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="En dos mil dos, el fisiólogo Heinz Valtin buscó de dónde salía, y no encontró ningún estudio que lo respaldara.",
         cap="*2002*: Heinz Valtin | buscó las pruebas… | y *no encontró ninguna*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Lo más parecido era una recomendación de un mililitro por caloría, y justo después venía una frase que nadie copió.",
         cap="*1 ml* por caloría… | y una frase | que *nadie copió*", hold=0.2),
    dict(id="s3", who="nar", cut=True, say="Decía que la mayor parte de esa agua ya va en la comida. Y el café o el té, también cuentan.",
         cap="La mayor parte | ya va *EN LA COMIDA*. | Café y té *cuentan*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Para un adulto sano, beber cuando tienes sed suele bastar, y con calor o deporte, más.",
         cap="Adulto sano: | bebe *cuando tengas sed*. | Calor o deporte: *más*", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="Envíaselo a quien va con la botella a todas partes, y comenta cuántos vasos bebes tú.", cap="¿Cuántos bebes tú? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 1.0:
        K.tag(c, W / 2, 1780, "DARTMOUTH · AM J PHYSIOL · 2002", lt - 1.0, accent=GOLD, size=36)
    if sid == "s3" and lt > 0.8:
        K.tag(c, W / 2, 1780, "«MOST OF THIS QUANTITY IS CONTAINED IN PREPARED FOODS»", lt - 0.8, accent=GOLD, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "agua.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "agua.js", overlay=overlay)
