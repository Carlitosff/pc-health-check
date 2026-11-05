"""1303 MITO 3D (chicle.js): 'si te tragas un chicle, 7 años en el estómago'.
Fuentes: Julia Zumpano (Cleveland Clinic) en Live Science 17/06/2024: ~40 h; Nancy McGreal, gastroenteróloga, Duke Health 27/08/2013: 'in all the upper endoscopies… I have yet to see a wad of gum';
gum base sin enzimas (Duke, SciAm); Mark Larson, Mayo Clinic 07/09/2018; Milov et al., Pediatrics 1998: 3 niños con bloqueos (SciAm, Live Science). Origen: desconocido (SciAm)."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE, clamp
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F
V = dict(slug="1303_chicle_7_anos", accent=0xFFFF6FB8, drone=0.03, mood="luz", send="ENVÍASELO A QUIEN TE LO DECÍA", reveal=("s3", "CUÁNTO TARDA"),
         rehook=("s4", "ESPERA… OJO CON ESTO"), segs=[
    dict(id="h", who="nar", say="Si te tragas un chicle, se queda siete años en tu estómago. Eso te dijeron.", cap="¿*7 AÑOS* en tu estómago?", hold=0.1),
    dict(id="s1", who="nar", cut=True, say="Tu abuela te lo juraba, y nadie sabe de dónde salió ese cuento.", cap="Te lo juraban… | y nadie sabe *de dónde salió*", hold=0.5),
    dict(id="s2", who="nar", cut=True, say="Es verdad que tu cuerpo no puede digerir la base del chicle. Pero eso no significa que se quede pegado.", cap="No se *digiere*… | pero NO se queda *pegado*", hold=0.2),
    dict(id="s3", who="nar", cut=True, say="Sale como todo lo demás, en unas cuarenta horas. Y una gastroenteróloga de Duke nunca ha visto uno en sus endoscopias.", cap="Sale en unas *40 HORAS*. | Duke: *ni uno* en sus endoscopias", hold=0.2),
    dict(id="s4", who="nar", cut=True, say="Eso sí, una revista médica de mil novecientos noventa y ocho describe tres niños con bloqueos por chicle. Muchos seguidos, no.", cap="1998: *3 niños* | con *bloqueos*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="¿Cuántos te has tragado tú? Comenta tu número, y mándaselo a quien te lo decía.", cap="¿Cuántos te has tragado? | *COMENTA* tu número"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s3":
        K.tag(c, W / 2, 1770, "CLEVELAND CLINIC · DUKE", lt - 1.6, accent=GOLD, size=40)
    if sid == "s4":
        K.tag(c, W / 2, 1770, "PEDIATRICS, 1998", lt - 1.0, accent=RED, size=44)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "chicle.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "chicle.js", overlay=overlay)
