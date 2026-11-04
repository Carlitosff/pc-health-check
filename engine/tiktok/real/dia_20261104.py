"""Producción 04/11/2026 (1201–1204) — motor v15: v3d/bloques.js (mundo de bloques reutilizable con sombras), v3d_run.py.
  1201 ILUSIÓN EN DIRECTO: stepping feet (Stuart Anstis, Neural Networks 2003 según Wikipedia; 'Footsteps and inchworms').
       Azul sobre blanco = alto contraste, parece más rápido; sobre negro, más lento; amarillo al revés. Sin rayas desaparece.
       Bloque de ancho = 2 rayas: sus dos bordes caen a la vez sobre el mismo color.
  1202 RETO: cubo 4x4x4 pintado por fuera: 8 esquinas (3 caras), 24 aristas (2), 24 caras (1), 8 sin pintura. assert por enumeración.
  1203 MITO 3D (playa.js, en v3d_run): corte de digestión. Cruz Roja americana 2011 (IFLScience, Science Focus); hidrocución (SEMES vía eldiario.es 03/08/2023; Xataka 13/06/2026, Ángel Jimeno Aranda).
  1204 SERIE 3D (frena.js): ¿Y si la Tierra frena? 1.668 km/h en el ecuador (Astronomy, feb 2026), V=1668·cos(lat) → 40,4°N ≈ 1.270 km/h; estructuras, polos (Astronomy, Science Notes); 6 meses de día (Smithsonian NASM 31/01/2018)."""
import math, sys, itertools
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text, glow
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; BLUE = 0xFF0A1C8E; YEL = 0xFFF7E400; CYAN = 0xFF7DE8FF


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 1201 pies que andan
SW, BW, BH = 54, 108, 130
Y0, Y1, LANE1, LANE2 = 730, 1700, 775, 965
SPEED = 116
_L1, _L2 = LANE1, LANE2


def feet_x(t):
    span = W - BW - 2 * 27
    u = (t * SPEED) % (2 * span)
    return 27 + (u if u < span else 2 * span - u)


def s_pies(c, t, P, V):
    sid, lt, d = seg(P, t)
    a2 = P["tl"]["s2"][0]; a3 = P["tl"]["s3"][0]
    # aparición de rayas: 1 con rayas, 0 gris liso
    if sid in ("h", "s1"): on = 1.0
    elif sid == "s2": on = 1 - clamp((lt - 1.15) / 0.5)
    elif sid == "s3": on = clamp((lt - 0.2) / 0.5)
    else: on = 1.0
    c.clear(0xFF0A0B10)
    GR = 0xFF8A8A8A
    c.drawRect(skia.Rect.MakeLTRB(0, Y0, W, Y1), fill(GR))
    if on > 0:
        for i in range(0, W // SW + 2):
            col = 0xFFFFFFFF if i % 2 == 0 else 0xFF000000
            c.drawRect(skia.Rect.MakeXYWH(i * SW, Y0, SW, Y1 - Y0), fill(with_alpha(col, on)))
    x = feet_x(t)
    # los bloques van centrados y suben en el CTA para que no los tape el botón de seguir
    up = K.smooth((t - P["tl"]["cta"][0]) / 0.5)
    dy = 240 * (1 - up)
    LANE1, LANE2 = _L1 + dy, _L2 + dy
    if sid == "s2" and on < 0.4:
        a = clamp((0.4 - on) / 0.4)
        c.drawRect(skia.Rect.MakeXYWH(x + BW / 2 - 4, LANE1, 8, LANE2 - LANE1 + BH), fill(with_alpha(RED, a)))
        c.drawRect(skia.Rect.MakeXYWH(x - 3, LANE1 - 40, BW + 6, 8), fill(with_alpha(RED, a)))
        c.drawRect(skia.Rect.MakeXYWH(x - 3, LANE2 + BH + 32, BW + 6, 8), fill(with_alpha(RED, a)))
    c.drawRect(skia.Rect.MakeXYWH(x, LANE1, BW, BH), fill(BLUE))
    c.drawRect(skia.Rect.MakeXYWH(x, LANE2, BW, BH), fill(YEL))
    if sid == "s4":
        K.tag(c, W / 2, 1790, "STUART ANSTIS, 2003", lt - 0.6, accent=GOLD, size=44)


V1201 = dict(slug="1201_pies_a_la_vez", accent=GOLD, drone=0.015, scene=s_pies, mood="misterio", steady=True, clean=True,
             send="ENVÍASELA: ¿A LA VEZ O POR TURNOS?", rehook=("s3", "MÍRALOS OTRA VEZ"), reveal=("s2", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Estos dos van a la vez, o por turnos?", cap="¿Van a la *VEZ* o por *TURNOS*?", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Míralos. Uno pisa, luego el otro. Como dos pies andando.", cap="Uno *pisa*… | luego el *otro*", hold=2.0),
    dict(id="s2", who="nar", cut=True, say="Ahora quito las rayas. Van exactamente a la vez. Siempre.", cap="Quito las *RAYAS*… | Van *A LA VEZ*. Siempre", hold=2.0),
    dict(id="s3", who="nar", cut=True, say="Vuelvo a ponerlas. Ya lo sabes, y tu cerebro sigue cayendo.", cap="Ya lo *sabes*… | y sigues *cayendo*", hold=2.0),
    dict(id="s4", who="nar", cut=True, say="Es el contraste. El azul, sobre blanco, parece correr, y sobre negro, frenar. El amarillo, al revés.",
         cap="Azul sobre *blanco*: *corre* | Sobre *negro*: *frena* | Amarillo, *al revés*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Envíasela a alguien, y que te diga: ¿a la vez, o por turnos? Y comenta qué viste tú.",
         cap="¿Qué viste tú? | *COMENTA*"),
])

# ============================ 1202 cubo pintado
N = 4
CUBES = [(i, j, k) for i in range(N) for j in range(N) for k in range(N)]


def painted(ix):
    return sum(v in (0, N - 1) for v in ix)


COUNTS = {p: sum(1 for q in CUBES if painted(q) == p) for p in range(4)}
assert COUNTS == {3: 8, 2: 24, 1: 24, 0: 8} and len(CUBES) == 64
FACES = [((1, 0, 0), [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)]), ((-1, 0, 0), [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)]),
         ((0, 1, 0), [(0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)]), ((0, -1, 0), [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)]),
         ((0, 0, 1), [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]), ((0, 0, -1), [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)])]
PAINT, WOOD = np.array([238, 36, 52.]), np.array([236, 200, 150.])


def rgb(v, a=1.0):
    v = np.clip(v, 0, 255)
    return skia.Color4f(float(v[0]) / 255, float(v[1]) / 255, float(v[2]) / 255, a).toColor()


def cube_world(c, t, P, boom, vis, cx=W / 2, cy=1230, sz=118):
    ry = 0.785 + 0.42 * math.sin(t * 0.55)
    rx = 0.52 + 0.06 * math.sin(t * 0.8)
    cr, sr, cx_, sx_ = math.cos(ry), math.sin(ry), math.cos(rx), math.sin(rx)
    def rot(p):
        x, y, z = p
        x, z = x * cr + z * sr, -x * sr + z * cr
        y, z = y * cx_ - z * sx_, y * sx_ + z * cx_
        return x, y, z
    polys = []
    m = (N - 1) / 2
    for q in CUBES:
        a = vis(q)
        if a < 0.02:
            continue
        off = [(v - m) * (1 + boom * 0.72) for v in q]
        for nrm, vs in FACES:
            nx, ny, nz = rot(nrm)
            if nz < 0.02:
                continue
            ext = any((nrm[d] == 1 and q[d] == N - 1) or (nrm[d] == -1 and q[d] == 0) for d in range(3))
            pts, zsum = [], 0
            for v in vs:
                x, y, z = rot([off[d] + v[d] - 0.5 for d in range(3)])
                persp = 1 / (1 - z * 0.035)
                pts.append((cx + x * sz * persp, cy - y * sz * persp))
                zsum += z
            shade = 0.56 + 0.44 * max(0, nz * 0.55 + ny * 0.6 + 0.2)
            polys.append((zsum / 4, pts, (PAINT if ext else WOOD) * shade, a))
    polys.sort(key=lambda e: e[0])
    for _, pts, col, a in polys:
        pa = skia.Path(); pa.moveTo(*pts[0])
        for p in pts[1:]:
            pa.lineTo(*p)
        pa.close()
        c.drawPath(pa, fill(rgb(col, a)))
        c.drawPath(pa, stroke(with_alpha(0xFF1A0A10, 0.55 * a), 3))


def s_cubo(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.clear(0xFF0B0E1C)
    hc.aurora(c, t, 0xFF0A2438, 0xFF2A1038, seed=1202)
    glow(c, W / 2, 1230, 760, 0xFFFF3050, 0.22)
    tl = P["tl"]
    boom, vis = 0.0, (lambda q: 1.0)
    if sid == "s1":
        pass
    elif sid == "s2":
        boom = 0.0
    elif sid == "s3":
        boom = ease_out(clamp(lt / 0.8))
        d3 = d / 3
        cl = 3 if lt < d3 else (2 if lt < 2 * d3 else 1)
        vis = lambda q: 1.0 if painted(q) == cl else 0.1
    elif sid == "s4":
        boom = 1.0
        vis = lambda q: 1.0 if painted(q) == 0 else max(0.0, 0.1 - lt)
    elif sid == "cta":
        boom = 0.45
        vis = lambda q: 1.0 if painted(q) == 0 else 0.0
    cube_world(c, t, P, boom, vis, cy=880 if sid == "cta" else 1180, sz=(92 if sid == "cta" else 118 * (1 - 0.22 * boom)))
    if sid == "s2" and lt > 0.8:
        hc.timer(c, W / 2, 1720, 76, clamp(1 - (lt - 0.8) / max(0.1, d - 1.0)), str(int(max(1, math.ceil(d - lt)))), GOLD)
    if sid == "s3":
        d3 = d / 3
        i = 0 if lt < d3 else (1 if lt < 2 * d3 else 2)
        hc.big(c, ["8 ESQUINAS", "24 ARISTAS", "24 CARAS"][i], W / 2, 1745, 92, WHITE, 1.0, 0.0)
    if sid == "s4":
        hc.big(c, "8", W / 2, 1720, 170, GOLD, min(1, lt * 3), 0.0)


V1202 = dict(slug="1202_cubo_pintado", accent=RED, drone=0.02, scene=s_cubo, mood="epico", send="RETA A UN AMIGO: ¿QUÉ NÚMERO DICE?",
             rehook=("s3", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="Pinto este cubo por fuera, y lo parto. ¿Cuántos cubitos quedan sin nada de pintura?",
         cap="¿Cuántos cubitos quedan *SIN PINTURA*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Cuatro por cuatro por cuatro. Sesenta y cuatro cubitos.", cap="4 × 4 × 4 = *64*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Di un número. Tienes tres segundos.", cap="Di un *número*… | *3 segundos*", hold=2.3),
    dict(id="s3", who="nar", cut=True, say="Las esquinas tienen tres caras pintadas: ocho. Las aristas, dos caras: veinticuatro. Y en cada cara, una: otros veinticuatro.",
         cap="*3* caras pintadas | *2* caras pintadas | *1* cara pintada", hold=0.1),
    dict(id="s4", who="nar", cut=True, say="Sesenta y cuatro, menos cincuenta y seis. Quedan ocho. Los del corazón, que nunca vieron la pintura.",
         cap="64 − 56 = *8* | Los del *corazón*", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="¿Qué número dijiste? Comenta. Y mándaselo a un amigo, a ver si lo saca sin ver el final.",
         cap="¿Qué dijiste? | *COMENTA* tu número"),
])

VIDEOS = [V1201, V1202]


def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
    return scene


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = "auto" if len(sys.argv) > 2 else None
    for i in idxs:
        K.run(VIDEOS[i], make_scene(VIDEOS[i]), OUT, preview=pv, extra_audio=VIDEOS[i].get("extra"))
