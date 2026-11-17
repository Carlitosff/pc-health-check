"""2504 SERIE 3D (hueca.js): ¿Y si la Tierra estuviera hueca? Parte 14 de ¿QUÉ PASARÍA SI…? (prometida en la parte 13: 'la Tierra está hueca por dentro').
Fuentes: Edmond Halley, artículo de 1692: 'Earth consists of a shell about 800 km thick' con dos esferas concéntricas y un núcleo (Frank Jacobs, 01/03/2007, reimpreso en UCSB Geography).
Teorema de la cáscara (Newton, Principia, 1687): fuera de una cáscara esférica la gravedad es la de toda su masa en el centro → misma masa = mismo peso en la superficie;
dentro de la cáscara la fuerza neta es cero → flotas. Britannica 'Earth: The interior': 'the crust, which accounts for a mere 0.4 percent of Earth's mass'.
Cálculo propio: solo la corteza → g × 0,004 → 80 kg marcan 0,32 kg (unos 300 gramos)."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; CYAN = 0xFF4DE3FF
assert round(80 * 0.004, 2) == 0.32
V = dict(slug="2504_tierra_hueca", accent=GOLD, drone=0.03, mood="misterio", badge="¿QUÉ PASARÍA SI…? · PARTE 14", send="ENVÍASELO A QUIEN CREE QUE ESTÁ HUECA",
         rehook=("s3", "ESPERA… Y DENTRO"), reveal=("s4", "¿Y SI LA VACIAMOS?"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra estuviera hueca por dentro? Súbete a la báscula y mira lo que marca.", cap="¿Y si la Tierra estuviera *HUECA*?", hold=0.1),
    dict(id="s1", who="nar", cut=True, say="En mil seiscientos noventa y dos, el astrónomo Edmond Halley la imaginó así, con esferas dentro de la corteza.",
         cap="*1692*: Halley la imaginó | con *ESFERAS* dentro", hold=0.1),
    dict(id="s2", who="nar", cut=True, say="Con toda la masa en la corteza, la báscula marcaría lo mismo, ochenta kilos.",
         cap="Toda la masa en la corteza: | *80 kg*, igual", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero si bajaras por un agujero hasta el hueco, flotarías en cualquier sitio, sin arriba ni abajo.",
         cap="Dentro del hueco: | *FLOTAS*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y si solo quedara la corteza de verdad, que pesa un cero coma cuatro por ciento del total, marcarías unos trescientos gramos.",
         cap="Solo la corteza (*0,4 %*): | pesarías *300 g*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Sígueme para la parte quince, la Tierra se para. Comenta qué harías flotando.",
         cap="*Parte 15*: | la Tierra se *PARA*. | ¿Qué harías flotando? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2" and lt > 2.4:
        K.tag(c, W / 2, 1840, "MISMA MASA = MISMO PESO", lt - 2.4, accent=WHITE, size=30)
    if sid == "s3" and lt > 2.0:
        K.tag(c, W / 2, 1840, "NEWTON · PRINCIPIA · 1687", lt - 2.0, accent=WHITE, size=30)
    if sid == "s1" and lt > 2.4:
        K.tag(c, W / 2, 1840, "CORTEZA DE ~800 km SEGÚN HALLEY", lt - 2.4, accent=WHITE, size=30)
    if sid == "s4" and lt > 2.6:
        K.tag(c, W / 2, 1840, "BRITANNICA · CÁLCULO PROPIO", lt - 2.6, accent=WHITE, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "hueca.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "hueca.js", overlay=overlay)
