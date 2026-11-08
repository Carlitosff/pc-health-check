"""1602 RETO 3D (plegado.js): ¿qué color queda enfrente del rojo al doblar esta plantilla? Respuesta CALCULADA: simulación del plegado con
el mismo árbol de bisagras que usa la escena (BFS desde la cara base) y assert de que salen 6 caras distintas y de cuál es la opuesta."""
import sys
import numpy as np
sys.path.insert(0, "/home/claude/tiktok/real"); sys.path.insert(0, "/tmp")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A


def _rot(ax, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]]) if ax == 'x' else np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def fold(net, base):
    idx = {tuple(c): i for i, c in enumerate(net)}; par = {base: None}; order = [base]; q = [base]
    while q:
        u = q.pop(0)
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = idx.get((net[u][0] + d[0], net[u][1] + d[1]))
            if v is not None and v not in par:
                par[v] = (u, d); order.append(v); q.append(v)
    assert len(order) == 6
    T = {base: (np.eye(3), np.zeros(3))}
    for v in order[1:]:
        u, d = par[v]; R, o = T[u]
        Rl = {(1, 0): _rot('z', np.pi / 2), (-1, 0): _rot('z', -np.pi / 2), (0, 1): _rot('x', -np.pi / 2), (0, -1): _rot('x', np.pi / 2)}[d]
        hv = np.array([d[0] * .5, 0, d[1] * .5])
        T[v] = (R @ Rl, o + R @ (hv + Rl @ hv))
    return {i: np.round(T[i][1], 6) for i in T}


NET = [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [3, 2]]
NAMES = ["ROJO", "AZUL", "AMARILLO", "VERDE", "MORADO", "BLANCO"]
COLS = ["#ff2d3f", "#2f6bff", "#ffd400", "#2ecc5a", "#9b4dff", "#f4f4f4"]
BASE = 2
C = fold(NET, BASE)
assert len({tuple(v) for v in C.values()}) == 6
cc = np.array([0, .5, 0])
opp = {i: j for i in C for j in C if np.allclose(C[i] - cc, -(C[j] - cc))}
ANS = opp[0]; assert NAMES[ANS] == "VERDE", NAMES[ANS]
for b in range(6):  # la respuesta no depende de qué cara se deje fija
    Cb = fold(NET, b); ob = {i: j for i in Cb for j in Cb if np.allclose(Cb[i] + Cb[j], 2 * np.array([0, .5, 0]))}
    assert ob[0] == ANS
V = dict(slug="1602_reto_plegado_cubo", accent=GOLD, drone=0.02, mood="epico", send="RETA A UN AMIGO: ¿QUÉ COLOR ES?",
         rehook=("s3", "MIRA CÓMO SE DOBLA"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Si doblas esta plantilla y haces un cubo, ¿qué color queda enfrente del rojo?", cap="¿Qué color queda *ENFRENTE* del rojo?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Cada cuadrado es una cara del cubo, y el amarillo se queda abajo, sin moverse.", cap="Cada cuadrado, | *una cara*. | El amarillo, *abajo*", hold=0.4),
    dict(id="s2", who="nar", cut=True, say="Tienes cinco segundos. ¿Enfrente del rojo queda el azul, el verde o el morado?", cap="¿*AZUL*, *VERDE* | o *MORADO*?", hold=3.0),
    dict(id="s3", who="nar", cut=True, say="Vamos a doblarla, cara a cara, y fíjate bien en dónde acaba el rojo.", cap="Vamos a *doblarla*… | mira *el rojo*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="El rojo acaba en un lado, y justo en el lado contrario, enfrente, queda el verde.", cap="Enfrente del rojo: | *EL VERDE*", hold=0.8),
    dict(id="cta", who="nar", cut=True, say="Comenta qué color dijiste tú, y reta a un amigo a ver si lo saca a la primera.", cap="¿Qué dijiste tú? | *COMENTA* tu color"),
])
JOB = dict(net=NET, cols=COLS, base=BASE, red=0, answer=ANS)


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; d = sg["b"] - sg["a"]
    if sid == "s2":
        n = max(1, 5 - int(lt / max(.1, d) * 5))
        hc.big(c, str(n), W * .84, 1700, 190, GOLD, 1.0, 0.0, outline=14)
    if sid == "s4" and lt > d * .82:
        hc.big(c, "¡EL VERDE!", W / 2, 1640, 130, 0xFF4ADE80, 1.0, 0.0, outline=14)
    if sid == "s4" and 1.2 < lt < d * .8:
        K.tag(c, W / 2, 1790, "PLEGADO CALCULADO: CARA A CARA", lt - 1.2, accent=GOLD, size=36)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "plegado.js", stills=sys.argv[2].split(","), extra_job=JOB)
    elif sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    else:
        v3d_run.run3d(V, "plegado.js", overlay=overlay, extra_job=JOB)
