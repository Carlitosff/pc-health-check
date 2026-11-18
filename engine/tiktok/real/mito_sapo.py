"""2603 MITO 3D (sapo.js): '¿Si tocas un sapo te salen verrugas?' → falso, con media razón.
Wonderopolis (National Center for Families Learning, 'Do toads really give you warts?'): 'it's nothing more than a myth that you can get warts
from picking up a toad'; 'Warts are actually caused by viruses from the human papillomavirus (HPV) family'; 'They can be passed from one person to
another by close physical contact'; los bultos 'are actually glands that make and release toxins that help toads defend themselves'.
Glándulas parotoides (detrás de los ojos) = las grandes de los sapos (Wikipedia 'Parotoid gland'). Lavarse las manos: consejo general, no cifra."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
V = dict(slug="2603_mito_sapo_verrugas", accent=GOLD, drone=0.02, mood="luz", send="ENVÍASELO A QUIEN TE LO DECÍA",
         rehook=("s3", "ESPERA… MEDIA RAZÓN"), reveal=("s2", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Te dijeron de pequeño que si tocabas un sapo te salían verrugas? Pues no es verdad, pero tampoco lo toques.",
         cap="¿Tocar un sapo da *VERRUGAS*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Las verrugas las causa un virus humano, el del papiloma, y se pasan de una persona a otra, no de un sapo.",
         cap="Las causa un *VIRUS HUMANO*: | el del papiloma", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Y esos bultos del sapo no son verrugas: son glándulas de su piel.",
         cap="Esos bultos | son *GLÁNDULAS*", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Las dos más grandes, detrás de los ojos, sueltan una sustancia tóxica para que nadie se lo coma.",
         cap="Sueltan una sustancia | *TÓXICA*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Así que verrugas no, pero si lo tocas, lávate las manos y no te las lleves a la boca ni a los ojos.",
         cap="Verrugas *NO*… | pero *lávate las manos*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta si a ti también te lo decían, y envíaselo a quien te lo decía.",
         cap="¿A ti te lo decían? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2" and lt > .9:
        K.tag(c, W / 2, 1720, "NO SON VERRUGAS: SON GLÁNDULAS", lt - .9, accent=0xFF4DE3FF, size=40)
    if sid == "s3" and lt > .8:
        K.tag(c, W / 2, 1720, "GLÁNDULAS PAROTOIDES: SUELTAN TÓXICOS", lt - .8, accent=0xFFFF8A3A, size=38)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "sapo.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "sapo.js", overlay=overlay)
