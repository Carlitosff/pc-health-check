"""Producción 03/11/2026 (1001–1004) — motor v13: nube de puntos sin pistas de profundidad, radiografía procedural, qa.py.
  1001 ILUSIÓN EN DIRECTO: bola de puntos con giro ambiguo (efecto cinético de profundidad; Wallach & O'Connell, J Exp
       Psychol 45(4):205-217, 1953. Proyección ORTOGONAL y puntos iguales: no hay ninguna pista de profundidad).
  1002 RETO: caminos de A a B en rejilla 4x4 solo derecha/abajo = C(8,4) = 70 (assert por enumeración y por suma).
  1003 MITO CON 'TÚ': crujirse los dedos. Donald Unger, Arthritis & Rheumatism 1998: mano izquierda ≥2 veces/día, 50 años,
       ≥36.500 crujidos; sin artritis en ninguna (Scientific American; Arthritis UK 30/11/2025). Ig Nobel Medicina 2009
       (The Conversation). Estudio 1990 de 300 pacientes sin más artritis (SciAm). Burbuja de gas 'most likely'.
  1004 SERIE (lo prometido tras Miranda): Mimas, 396 km; Herschel 130 km, 1/3 de la luna, 10 km de hondo, pico central 6 km,
       'probably came close to disintegrating the moon' (Hamilton, How It Works 30/10/2020)."""
import math, sys, random, os, itertools
import numpy as np
import skia
from PIL import Image, ImageFilter
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
import paisaje as Pz
import dia_20261031 as D
from core import glow, W, H, WHITE, INK, clamp, lerp, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, draw_text

OUT = "/home/claude/tiktok/outdaily"
GREEN = 0xFF2FD46B
RED = 0xFFFF3B4A
GOLD = 0xFFFFC23A
CYAN = 0xFF7DE8FF
SR = 44100
seg = D.seg
blur = D.blur


def rrect(x, y, w, h, r):
    return skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)


def chevrons(c, x, y, sign, t, col, a=1.0):
    for i in range(3):
        k = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 6 - i * 1.1))
        xx = x + sign * i * 34
        p = skia.Path()
        p.moveTo(xx - sign * 16, y - 34); p.lineTo(xx + sign * 16, y); p.lineTo(xx - sign * 16, y + 34)
        c.drawPath(p, stroke(with_alpha(col, a * k), 13))


# ====================================================================== 1001 ¿Hacia dónde gira?
_r = np.random.default_rng(1953)
_n = 1500
_i = np.arange(_n) + 0.5
LAT = np.arcsin(1 - 2 * _i / _n) + _r.normal(0, 0.006, _n)
LON = (np.pi * (1 + 5 ** 0.5) * _i) % (2 * np.pi)
BCX, BCY, BR = W / 2, 1160, 415
OMEGA = 1.35


def ball_xyz(t, tilt):
    th = LON + OMEGA * t
    x = np.cos(LAT) * np.sin(th)
    y0 = np.sin(LAT)
    z0 = np.cos(LAT) * np.cos(th)  # z>0 = hacia el espectador. Con th creciente, la cara de delante va a la DERECHA
    y = y0 * math.cos(tilt) - z0 * math.sin(tilt)
    z = y0 * math.sin(tilt) + z0 * math.cos(tilt)
    return x, y, z


def draw_ball(c, t, tilt=0.2, depth=0.0, a=1.0, col=CYAN):
    """depth=0: proyección ortogonal con puntos idénticos: el sentido de giro es matemáticamente ambiguo.
    depth=+1: los de z>0 se agrandan (se ve girar a la derecha); depth=-1: la misma imagen plana, al revés (izquierda)."""
    x, y, z = ball_xyz(t, tilt)
    px = BCX + BR * x
    py = BCY - BR * y
    if abs(depth) < 1e-3:
        pts = [skia.Point(float(u), float(v)) for u, v in zip(px, py)]
        pa = skia.Paint(AntiAlias=True, Color=with_alpha(col, a), StrokeWidth=11, StrokeCap=skia.Paint.kRound_Cap)
        c.drawPoints(skia.Canvas.kPoints_PointMode, pts, pa)
        return
    zz = z * (1 if depth > 0 else -1)
    dd = abs(depth)
    order = np.argsort(zz)
    for i in order:
        f = (zz[i] + 1) / 2
        r = 5.5 * (1 - dd) + dd * lerp(1.6, 11.0, f)
        aa = a * ((1 - dd) + dd * lerp(0.22, 1.0, f))
        c.drawCircle(float(px[i]), float(py[i]), float(r), fill(with_alpha(col, aa)))


def side_label(c, txt, x, y, col, a=1.0):
    draw_text(c, txt, x, y, 40, with_alpha(col, a))


def s_gira(c, t, P, V):
    sid, lt = seg(P, t)
    a, b = P["tl"][sid]
    k = clamp(lt / max(0.1, b - a))
    c.clear(0xFF05070F)
    hc.aurora(c, t, 0xFF08203A, 0xFF1E1038, seed=1001)
    glow(c, BCX, BCY, 640, 0xFF1A5A9A, 0.28)
    if sid in ("h", "s1"):
        draw_ball(c, t)
        ya = 1680
        side_label(c, "IZQUIERDA", 250, ya + 16, WHITE)
        side_label(c, "DERECHA", 830, ya + 16, WHITE)
        chevrons(c, 90, ya, -1, t, GOLD)
        chevrons(c, 990, ya, 1, t, GOLD)
        if sid == "s1" and lt > 1.2:
            bl = clamp((lt - 1.2) / 0.3)
            hc.big(c, "¿HA CAMBIADO?", W / 2, 1610, 66, GOLD, 1.0, 0.0) if bl >= 1 else None
    elif sid == "s2":
        draw_ball(c, t, tilt=0.2 * (1 - ease_in_out(k)))
    elif sid == "s3":
        draw_ball(c, t, tilt=0.0)
        # raíles: cada punto va y viene en línea recta
        al = ease_out(clamp(lt / 1.0)) * 0.4
        yy = np.unique(np.round((BCY - BR * np.sin(LAT[::30])) / 14) * 14)
        for y in yy[::2]:
            hw = BR * math.sqrt(max(0, 1 - ((y - BCY) / BR) ** 2))
            c.drawLine(BCX - hw, float(y), BCX + hw, float(y), stroke(with_alpha(WHITE, al), 2))
        K.tag(c, W / 2, 1680, "WALLACH Y O'CONNELL, 1953", lt - 0.5, accent=GOLD, size=44)
    elif sid == "s4":
        half = 0.5
        if k < half:
            dp = ease_out(clamp(k / 0.14))
            draw_ball(c, t, tilt=0.0, depth=dp)
            draw_text(c, "A LA DERECHA", W / 2 - 40, 1690, 66, GOLD)
            chevrons(c, 860, 1668, 1, t, GOLD)
        else:
            dp = ease_out(clamp((k - half) / 0.14))
            draw_ball(c, t, tilt=0.0, depth=-dp)
            draw_text(c, "A LA IZQUIERDA", W / 2 + 40, 1690, 66, GOLD)
            chevrons(c, 170, 1668, -1, t, GOLD)
    else:
        draw_ball(c, t, a=0.5)


V1001 = dict(slug="1001_hacia_donde_gira", accent=GOLD, drone=0.02, scene=s_gira, mood="misterio",
             tease="DECIDE ANTES DE 3 SEGUNDOS", send="ENVÍASELA: ¿VE LO MISMO QUE TÚ?",
             rehook=("s4", "MIRA, LOS MISMOS PUNTOS"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Hacia dónde gira esta bola? ¿A la izquierda, o a la derecha?",
         cap="¿Hacia dónde *GIRA* esta bola?", hold=0.7),
    dict(id="s1", who="nar", cut=True, say="Decide ya. Y ahora parpadea fuerte. A algunos les cambia de sentido.",
         cap="*Parpadea* fuerte… | a algunos les *cambia*", hold=2.2),
    dict(id="s2", who="nar", cut=True, say="¿La respuesta? Ninguna. La bola, no existe.",
         cap="La respuesta: *NINGUNA*. | La bola *no existe*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Son puntos planos, que van y vienen en línea recta. La profundidad te la inventas tú.",
         cap="Puntos *planos* | en línea recta. | La profundidad | te la *inventas tú*"),
    dict(id="s4", who="nar", cut=True, say="Mira. Si agrando los de delante, gira a la derecha. Si agrando los otros, a la izquierda.",
         cap="Mismo movimiento… | *otro sentido*", hold=0.8),
    dict(id="cta", who="nar", cut=True, say="¿Qué viste primero? Comenta izquierda o derecha. Y envíasela a un amigo, a ver si ve lo mismo.",
         cap="Comenta | *IZQUIERDA* o *DERECHA*"),
])


# ====================================================================== 1002 Caminos de A a B
N = 4
PATHS = sorted(set(itertools.permutations("RRRRDDDD")))
assert len(PATHS) == 70 == math.comb(8, 4)
WAYS = [[1] * (N + 1) for _ in range(N + 1)]
for i in range(1, N + 1):
    for j in range(1, N + 1):
        WAYS[i][j] = WAYS[i - 1][j] + WAYS[i][j - 1]
assert WAYS[N][N] == 70 and WAYS[3][4] == 35 and WAYS[4][3] == 35 and WAYS[2][2] == 6 and WAYS[3][3] == 20
random.Random(70).shuffle(PATHS)
CELL, GX0, GY0 = 190, 160, 760


def node(i, j):  # i = fila (abajo), j = columna (derecha)
    return GX0 + j * CELL, GY0 + i * CELL


def path_pts(p):
    i, j = 0, 0
    pts = [node(0, 0)]
    for m in p:
        if m == "R":
            j += 1
        else:
            i += 1
        pts.append(node(i, j))
    return pts


def draw_path(c, p, k, col, w=14, a=1.0, head=True):
    pts = path_pts(p)
    L = k * 8
    sk = skia.Path(); sk.moveTo(*pts[0])
    hx, hy = pts[0]
    for n in range(8):
        f = clamp(L - n)
        if f <= 0:
            break
        x = lerp(pts[n][0], pts[n + 1][0], f)
        y = lerp(pts[n][1], pts[n + 1][1], f)
        sk.lineTo(x, y)
        hx, hy = x, y
    st = stroke(with_alpha(col, a), w)
    st.setStrokeJoin(skia.Paint.kRound_Join)
    c.drawPath(sk, st)
    if head:
        glow(c, hx, hy, 60, col, 0.8)
        c.drawCircle(hx, hy, 15, fill(WHITE))


def city(c, t):
    c.clear(0xFF070B18)
    hc.aurora(c, t, 0xFF08304A, 0xFF2A1040, seed=1002)
    rng = random.Random(4)
    for i in range(N):
        for j in range(N):
            x, y = node(i, j)
            c.drawRRect(rrect(x + 22, y + 22, CELL - 44, CELL - 44, 16), fill(0xFF141C34))
            c.drawRRect(rrect(x + 22, y + 22, CELL - 44, CELL - 44, 16), stroke(0xFF2A3660, 3))
            for a_ in range(3):  # ventanitas que parpadean
                for b_ in range(3):
                    on = 0.5 + 0.5 * math.sin(t * rng.uniform(0.6, 1.8) + rng.uniform(0, 6.3))
                    c.drawRect(skia.Rect.MakeXYWH(x + 44 + a_ * 36, y + 44 + b_ * 36, 20, 20), fill(with_alpha(0xFFFFD27A, 0.05 + 0.2 * on)))
    for i in range(N + 1):
        c.drawLine(*node(i, 0), *node(i, N), stroke(0xFF43527E, 8))
        c.drawLine(*node(0, i), *node(N, i), stroke(0xFF43527E, 8))
    for i in range(N + 1):
        for j in range(N + 1):
            c.drawCircle(*node(i, j), 8, fill(0xFF8496C8))


def end_nodes(c, t):
    ax, ay = node(0, 0)
    bx, by = node(N, N)
    glow(c, ax, ay, 90, GREEN, 0.6)
    c.drawCircle(ax, ay, 44, fill(GREEN)); draw_text(c, "A", ax, ay + 20, 56, INK, shadow=False)
    pu = 1 + 0.08 * math.sin(t * 5)
    glow(c, bx, by, 110 * pu, GOLD, 0.7)
    c.drawCircle(bx, by, 44 * pu, fill(GOLD)); draw_text(c, "B", bx, by + 20, 56, INK, shadow=False)


def num_chip(c, i, j, val, s, col=WHITE):
    if s <= 0:
        return
    x, y = node(i, j)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 44, fill(0xFF0A1022))
    c.drawCircle(0, 0, 44, stroke(col, 5))
    draw_text(c, str(val), 0, 17, 50 if val < 10 else 46, col, shadow=False)
    c.restore()


def s_caminos(c, t, P, V):
    sid, lt = seg(P, t)
    a, b = P["tl"][sid]
    k = clamp(lt / max(0.1, b - a))
    city(c, t)
    if sid == "h":
        n = int(t / 1.25)
        draw_path(c, PATHS[n % 70], clamp((t % 1.25) / 1.1), CYAN)
        K.tag(c, W / 2, 1650, "SOLO DERECHA Y ABAJO", t - 0.3, accent=GOLD, size=46)
    elif sid == "s1":
        n = int(t / 1.25)
        draw_path(c, PATHS[n % 70], clamp((t % 1.25) / 1.1), CYAN)
        hc.timer(c, W / 2, 1690, 72, k, str(max(0, math.ceil((b - t)))), GOLD)
    elif sid == "s2":
        # arranca lento y se acelera: se ve que a mano no se acaba nunca
        q = (k ** 1.8) * 24
        shown = int(q)
        for m in range(max(0, shown - 7), shown):
            draw_path(c, PATHS[m], 1.0, CYAN, w=8, a=0.28, head=False)
        draw_path(c, PATHS[shown % 70], q - shown, CYAN)
        hc.big(c, str(shown + 1), W / 2, 1720, 130, CYAN, 1.0, 0.0)
    elif sid in ("s3", "s4", "cta"):
        ta, tb = P["tl"]["s3"]
        ca, cb = P["tl"]["s4"]
        for dg in range(0, 8):
            if sid == "s3":
                d0 = lerp(0.4, tb - ta - 0.3, dg / 8)
                s = ease_back(clamp((lt - d0) / 0.3)) if dg < 7 else 0
            elif dg < 7:
                s = 1.0
            else:
                s = ease_back(clamp((t - (cb - 2.6)) / 0.3))
            for i in range(0, dg + 1):
                j = dg - i
                if i > N or j > N:
                    continue
                col = GOLD if dg == 7 else WHITE
                num_chip(c, i, j, WAYS[i][j], s if sid != "cta" else 1.0, col)
        if sid == "s3":  # enseña la regla en un cruce: 3 + 3 = 6
            d4 = lerp(0.4, tb - ta - 0.3, 0.5) + 0.2
            if lt > d4:
                pu = 1 + 0.1 * math.sin(t * 7)
                x, y = node(2, 2)
                c.drawCircle(x, y, 58 * pu, stroke(GOLD, 8))
                K.tag(c, W / 2, 1680, "3 + 3 = 6", lt - d4, accent=GOLD, size=62)
        if sid == "s4" and t > cb - 2.6:
            hc.big(c, "35 + 35", W / 2, 1720, 120, GOLD, t - (cb - 2.6), 0.0)
        if sid == "cta":
            for p in PATHS:
                draw_path(c, p, clamp(lt / 1.0), GOLD, w=5, a=0.2, head=False)
            s = ease_back(clamp(lt / 0.35), 2.2)
            c.save(); c.translate(W / 2, 1000); c.scale(s, s)
            glow(c, 0, 0, 200, GOLD, 0.8)
            c.drawCircle(0, 0, 92, fill(GOLD))
            draw_text(c, "70", 0, 40, 112, INK, shadow=False)
            c.restore()
    end_nodes(c, t) if sid != "cta" else None


V1002 = dict(slug="1002_cuantos_caminos_70", accent=GOLD, drone=0.02, scene=s_caminos, mood="misterio",
             tease="TIENES 5 SEGUNDOS", send="RETA A UN AMIGO: ENVÍASELO",
             rehook=("s3", "HAY UN TRUCO"), reveal=("cta", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="¿Cuántos caminos hay de A a B? Solo puedes ir a la derecha, o hacia abajo.",
         cap="¿Cuántos *CAMINOS* hay de A a B?", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Escribe tu número antes de seguir.",
         cap="Escribe tu *NÚMERO*", hold=2.6),
    dict(id="s2", who="q", cut=True, say="Vamos a contarlos. Uno, dos, tres… A mano no acabas nunca.",
         cap="Uno, dos, tres… | a mano *no acabas*", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="Hay un truco. A cada cruce llegas desde arriba, o desde la izquierda. Así que solo sumas esos dos.",
         cap="Cada cruce: | *SUMA* | los dos de antes", hold=0.5),
    dict(id="s4", who="nar", cut=True, say="Uno, tres, seis, diez, veinte. Y en la última esquina: treinta y cinco, más treinta y cinco.",
         cap="Última esquina: | *35 + 35*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Setenta caminos. ¿Cuántos dijiste tú? Comenta, y reta a un amigo.",
         cap="*70 caminos*. ¿Y tú? | *COMENTA* | y reta a un amigo"),
])


# ====================================================================== 1003 Crujirse los dedos: radiografía
assert 2 * 365 * 50 == 36500
FING = [  # (x, y de la base del metacarpo, ángulo, largo metacarpo, 3 falanges) mano con pulgar a la izquierda
    (-105, 150, -8, 165, (108, 66, 50)),   # meñique
    (-40, 140, -3, 190, (132, 86, 56)),    # anular
    (30, 135, 1, 205, (142, 96, 58)),      # corazón
    (95, 140, 6, 195, (128, 82, 54)),      # índice
]
THUMB = (125, 165, 30, 95, (80, 60))


def bone(c, x0, y0, x1, y1, w, col):
    c.drawLine(x0, y0, x1, y1, stroke(col, w))
    r = w * 0.74
    c.drawCircle(x0, y0, r, fill(col))
    c.drawCircle(x1, y1, r, fill(col))


def finger_chain(spec):
    x, y, ang, meta, ph = spec
    pts = [(x, y)]
    a = math.radians(ang)
    for ln in (meta,) + tuple(ph):
        x += math.sin(a) * ln
        y -= math.cos(a) * ln
        pts.append((x, y))
        a *= 1.12
    return pts


def xray_hand(c, cx, cy, s, flip, t, active=0.0, crack=None, tissue=1.0, tint=0xFFD8ECFF, boost=0.0):
    """Mano en radiografía: tejido translúcido, huesos con gradiente y nudillos. flip=True pone el pulgar a la derecha."""
    c.save(); c.translate(cx, cy); c.scale(-s if flip else s, s)
    # tejido blando
    tp = skia.Paint(AntiAlias=True, Color=with_alpha(0xFF3C86C8, 0.26 * tissue), StrokeCap=skia.Paint.kRound_Cap,
                    Style=skia.Paint.kStroke_Style, MaskFilter=blur(5))
    for sp in FING + [THUMB]:
        ch = finger_chain(sp) if len(sp[4]) == 3 else finger_chain(sp)
        tp.setStrokeWidth(62)
        c.drawLine(*ch[1], *ch[-1], tp)
    palm = skia.Path(); palm.addRRect(rrect(-150, -80, 300, 300, 80))
    c.drawPath(palm, skia.Paint(AntiAlias=True, Color=with_alpha(0xFF3C86C8, 0.26 * tissue), MaskFilter=blur(5)))
    c.drawRRect(rrect(-100, 190, 200, 140, 40), skia.Paint(AntiAlias=True, Color=with_alpha(0xFF3C86C8, 0.22 * tissue), MaskFilter=blur(5)))
    # carpo
    for (x, y, r) in [(-70, 200, 30), (-15, 212, 32), (42, 205, 32), (92, 212, 26), (-45, 255, 30), (15, 262, 33), (68, 256, 28)]:
        c.drawCircle(x, y, r, fill(with_alpha(tint, 0.82)))
    # radio y cúbito
    bone(c, -45, 300, -55, 470, 42, with_alpha(tint, 0.8))
    bone(c, 45, 300, 50, 470, 52, with_alpha(tint, 0.8))
    # huesos
    for n, sp in enumerate(FING + [THUMB]):
        ch = finger_chain(sp)
        for i in range(len(ch) - 1):
            w = lerp(36, 23, i / 3)
            gap = 11
            x0, y0 = ch[i]; x1, y1 = ch[i + 1]
            d = math.hypot(x1 - x0, y1 - y0)
            ux, uy = (x1 - x0) / d, (y1 - y0) / d
            bone(c, x0 + ux * gap, y0 + uy * gap, x1 - ux * gap, y1 - uy * gap, w, with_alpha(tint, 0.95))
        if active > 0 and n < 4:
            kx, ky = ch[1]
            f = 0.5 + 0.5 * math.sin(t * 6 + n)
            glow(c, kx, ky, 60, 0xFFFF6A4A, active * (0.35 + 0.4 * f))
            if crack is not None:
                ph = (crack + n * 0.11) % 1
                if ph < 0.5:
                    c.drawCircle(kx, ky, 18 + ph * 120, stroke(with_alpha(0xFFFFB05A, active * (1 - ph * 2)), 5))
    if boost > 0:
        for sp in FING:
            ch = finger_chain(sp)
            glow(c, *ch[1], 64, GREEN, boost * 0.5)
    c.restore()


def lightbox(c, t, y_scan=True):
    c.clear(0xFF03090F)
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, 1050), 980, [0xFF123050, 0xFF03090F])))
    for x in range(0, W, 90):
        c.drawLine(x, 0, x, H, stroke(with_alpha(0xFF6AA8E0, 0.05), 2))
    for y in range(0, H, 90):
        c.drawLine(0, y, W, y, stroke(with_alpha(0xFF6AA8E0, 0.05), 2))


def scanline(c, t, y0=640, y1=1560, a=0.7, sp=0.75):
    y = lerp(y0, y1, 0.5 - 0.5 * math.cos(t * sp * 2))
    c.drawRect(skia.Rect.MakeXYWH(0, y - 40, W, 80), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, y - 40), (0, y + 40)], [0x005AE0FF, with_alpha(0xFF5AE0FF, 0.22 * a), 0x005AE0FF])))
    c.drawLine(0, y, W, y, stroke(with_alpha(0xFF9AF0FF, a), 3))


HY = 1000


def s_crujir(c, t, P, V):
    sid, lt = seg(P, t)
    a, b = P["tl"][sid]
    k = clamp(lt / max(0.1, b - a))
    lightbox(c, t)
    if sid in ("h", "s1", "s2", "s3", "cta"):
        ta = {"h": 0.0}.get(sid, 1.0)
        if sid == "h":
            act = 0.5 + 0.5 * math.sin(t * 3)
        elif sid == "s3":
            act = 0.0
        else:
            act = 1.0
        s_ = 0.92 + 0.012 * math.sin(t * 1.2)
        bb = ease_out(clamp((lt - (b - a) * 0.72) / 0.5)) if sid == "s3" else 0.0
        bb2 = ease_out(clamp((lt - (b - a) * 0.42) / 0.5)) if sid == "s3" else 0.0
        crk = t * 1.1 if sid in ("h", "s1", "s2") else None
        xray_hand(c, 278, HY, s_, False, t, active=act, crack=crk, boost=bb2)
        xray_hand(c, 802, HY, s_, True, t, boost=bb)
        scanline(c, t, a=0.7 if sid != "cta" else 0.25)
        if sid in ("s1", "s2", "s3"):
            draw_text(c, "IZQUIERDA", 278, 1490, 44, 0xFFFFB05A)
            draw_text(c, "DERECHA", 802, 1490, 44, 0xFF9AD8FF)
        if sid == "s1":
            hc.big(c, "×2 AL DÍA", 278, 1590, 56, 0xFFFFB05A, lt, 1.0)
            hc.big(c, "NUNCA", 802, 1590, 56, 0xFF9AD8FF, lt, 2.6)
        elif sid == "s2":
            q = ease_in_out(clamp(lt / max(0.1, (b - a) - 0.5)))
            n = int(36500 * q)
            hc.big(c, f"{n:,}".replace(",", "."), W / 2, 1600, 130, 0xFFFFB05A, 1.0, 0.0)
            draw_text(c, f"AÑO {int(50 * q)}", W / 2, 1740, 50, WHITE)
        elif sid == "s3":
            if bb2 > 0:
                hc.stamp(c, "0", 278, 1630, lt - (b - a) * 0.42, 0.0, 120, col=GREEN)
            if bb > 0:
                hc.stamp(c, "0", 802, 1630, lt - (b - a) * 0.72, 0.0, 120, col=GREEN)
            K.tag(c, W / 2, 1745, "CASOS DE ARTRITIS", lt - 0.5, accent=WHITE, size=38)
    elif sid == "s4":
        # primer plano del nudillo: dos huesos, líquido y burbuja que aparece y estalla
        dz = 1 + 0.03 * math.sin(t)
        c.save(); c.translate(W / 2, 1120); c.scale(dz, dz)
        sp = ease_out(clamp(lt / 1.0)) * 34  # los huesos se separan
        tint = 0xFFD8ECFF
        for sgn in (-1, 1):
            yy = sgn * (160 + sp)
            bone(c, 0, yy, 0, sgn * 560, 150, with_alpha(tint, 0.95))
            c.drawOval(skia.Rect.MakeXYWH(-155, yy - 90, 310, 180), fill(with_alpha(tint, 0.95)))
        cap_ = skia.Paint(AntiAlias=True, Color=with_alpha(0xFF3C86C8, 0.34))
        c.drawRRect(rrect(-210, -180 - sp, 420, 360 + 2 * sp, 100), cap_)
        ph = (lt - 0.7) / max(0.5, (b - a) - 1.0)
        if 0 < ph < 0.78:
            r = 12 + 86 * ease_out(ph / 0.78)
            c.drawCircle(0, 0, r, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((-r / 3, -r / 3), r * 1.3, [0xCCFFFFFF, 0x225AE0FF])))
            c.drawCircle(0, 0, r, stroke(with_alpha(WHITE, 0.9), 5))
        elif ph >= 0.78:
            e = clamp((ph - 0.78) / 0.2)
            for i in range(16):
                an = i / 16 * 6.283
                c.drawLine(math.cos(an) * (60 + 200 * e), math.sin(an) * (60 + 200 * e), math.cos(an) * (120 + 240 * e), math.sin(an) * (120 + 240 * e),
                           stroke(with_alpha(GOLD, 1 - e), 10))
            hc.stamp(c, "¡CRAC!", 0, 20, (ph - 0.78) * 3, 0.0, 130, col=GOLD)
        c.restore()
        K.tag(c, W / 2, 1720, "IG NOBEL DE MEDICINA · 2009", lt - 0.2, accent=GOLD, size=42)


def crack_sfx(m, P):
    """Crujidos sintéticos: ráfagas de ruido muy cortas y filtradas. Aceleran durante el contador."""
    rng = np.random.default_rng(36500)
    def crack(tc, gain=0.5):
        n = int(0.035 * SR)
        s = rng.normal(0, 1, n) * np.exp(-np.linspace(0, 9, n))
        s = np.diff(np.r_[0, s])
        i = int(tc * SR)
        if i + n < len(m.buf):
            m.buf[i:i + n] += s * gain
    a, b = P["tl"]["h"]
    for x in (0.25, 0.42, 0.61):
        crack(x, 0.3)
    a, b = P["tl"]["s2"]
    tc = a + 0.2
    gap = 0.34
    while tc < b - 0.5:
        crack(tc, 0.16)
        tc += gap
        gap = max(0.05, gap * 0.9)
    a, b = P["tl"]["s4"]
    crack(a + 0.7 + 0.78 * max(0.5, (b - a) - 1.0), 0.42)


V1003 = dict(slug="1003_crujir_dedos_unger", accent=0xFFFFB05A, drone=0.02, scene=s_crujir, mood="misterio",
             tease="50 AÑOS DE EXPERIMENTO", send="ENVÍASELO AL QUE SE LOS CRUJE", extra=crack_sfx,
             rehook=("s3", "MIRA EL RESULTADO"), reveal=("s3", "EL RESULTADO"), segs=[
    dict(id="h", who="nar", say="¿Crujirte los dedos te da artritis? Un médico lo probó en sí mismo.",
         cap="¿Crujirte los dedos te da *ARTRITIS*?", hold=0.0),
    dict(id="s1", who="nar", cut=True, say="Donald Unger se crujía la mano izquierda, al menos dos veces al día. La derecha, nunca.",
         cap="*Donald Unger*: | solo la *izquierda*, | la derecha *nunca*"),
    dict(id="s2", who="nar", cut=True, say="Así, cincuenta años. Al menos treinta y seis mil quinientos crujidos.",
         cap="*50 años*. | Al menos *36.500 crujidos*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Mil novecientos noventa y ocho. Artritis en la izquierda: ninguna. En la derecha: ninguna.",
         cap="*1998*: | en la izquierda, *NINGUNA*. | En la derecha, *NINGUNA*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Es un solo hombre. Pero en un estudio de trescientas personas, tampoco hubo más artritis. El crac es, probablemente, una burbuja de gas.",
         cap="*300 personas*: | tampoco más artritis. | El crac: *una burbuja*"),
    dict(id="cta", who="nar", cut=True, say="¿Te los crujes? Comenta sí o no. Y envíaselo a quien te riñe.",
         cap="¿Te los crujes? | Comenta *SÍ* o *NO*"),
])


# ====================================================================== 1004 Mimas
_mim = S.TEX + "mimas_proc.png"


def mimas_texture(path, w=2048, h=1024, seed=1789):
    n = Pz.fbm(h, w, seed, base=(4, 8), octaves=6)
    hgt = n * 0.05
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rnd = np.random.default_rng(seed)

    def crater(cx, cy, r, depth):
        kx = 1 / max(0.25, math.cos((cy / h - 0.5) * math.pi))
        rx = r * kx
        x0, x1 = int(max(cx - 2.2 * rx, 0)), int(min(cx + 2.2 * rx, w))
        y0, y1 = int(max(cy - 2.2 * r, 0)), int(min(cy + 2.2 * r, h))
        if x1 <= x0 or y1 <= y0:
            return
        dx = (xx[y0:y1, x0:x1] - cx) / kx
        d = np.hypot(dx, yy[y0:y1, x0:x1] - cy) / r
        hgt[y0:y1, x0:x1] += depth * (np.where(d < 1, d * d - 1, 0) + 0.32 * np.exp(-((d - 1) / 0.13) ** 2))

    for _ in range(620):  # superficie muy castigada, como en las fotos de Cassini
        crater(rnd.uniform(0, w), rnd.uniform(40, h - 40), rnd.uniform(3, 22) ** 1.0, rnd.uniform(0.04, 0.09))
    for _ in range(60):
        crater(rnd.uniform(0, w), rnd.uniform(60, h - 60), rnd.uniform(20, 42), rnd.uniform(0.09, 0.14))
    # Herschel: radio angular = 65/198 rad = 18,8° -> 107 px en un mapa de 2048
    hx, hy, hr = w * 0.5, h * 0.5, 107
    crater(hx, hy, hr, 0.55)
    d = np.hypot(xx - hx, yy - hy) / hr
    hgt += 0.34 * np.exp(-(d / 0.20) ** 2)  # pico central
    gy_, gx_ = np.gradient(hgt)
    shade = 0.55 + 7.5 * (-gx_ * 0.7 - gy_ * 0.7)
    v = np.clip(shade, 0.02, 1.25) * (0.86 + 0.14 * n)
    img = np.stack([v * 0.98, v * 0.99, v * 1.02], -1)
    Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).save(path)


if not os.path.exists(_mim):
    mimas_texture(_mim)
MIM = S.load("mimas_proc.png")
L0 = (-0.55, 0.42, 0.72)
SPIN0 = 0.0  # con este valor Herschel queda de cara (comprobado en la preview)
_st = random.Random(396)
STARS = [(_st.uniform(0, W), _st.uniform(0, H), _st.uniform(0.8, 2.6), _st.uniform(0, 6.3)) for _ in range(260)]


def space(c, t):
    c.clear(0xFF03040A)
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((820, 500), 1300, [0xFF10203A, 0xFF03040A])))
    for x, y, r, p in STARS:
        xx = (x - t * 6 * r) % W
        c.drawCircle(xx, y, r, fill(with_alpha(WHITE, 0.45 + 0.4 * math.sin(t * 1.5 + p))))


def mimas(c, x, y, R, t, sway=0.05, light=L0):
    S.draw_planet(c, x, y, R, S.render(int(2 * R), MIM, spin=SPIN0 + sway * math.sin(t * 0.5), tilt=0.1, light=light, gain=1.25, limb=0.5, ambient=0.05))


MR = 420
MX, MY = W / 2, 1130


def s_mimas(c, t, P, V):
    sid, lt = seg(P, t)
    a, b = P["tl"][sid]
    k = clamp(lt / max(0.1, b - a))
    space(c, t)
    if sid == "h":
        R = lerp(MR * 0.94, MR, ease_out(clamp(t / 3)))
        mimas(c, MX, MY, R, t)
        crater_ring(c, MX, MY, R, 0.5 + 0.5 * math.sin(t * 4), 0.75)
    elif sid == "s1":
        R = MR
        mimas(c, MX, MY, R, t)
        ww = ease_out(clamp(lt / 0.9))
        y = MY + R + 60
        c.drawLine(MX - R * ww, y, MX + R * ww, y, stroke(WHITE, 8))
        for sg in (-1, 1):
            c.drawLine(MX + sg * R * ww, y - 22, MX + sg * R * ww, y + 22, stroke(WHITE, 8))
        hc.big(c, "396 KM", MX, y + 104, 90, WHITE, lt, 0.5)
    elif sid == "s2":
        R = MR + 30 * ease_out(k)
        mimas(c, MX, MY, R, t)
        hr = R * math.sin(65 / 198)
        ww = ease_out(clamp((lt - 0.7) / 0.8))
        crater_ring(c, MX, MY, R, 1.0, 1.0)
        c.drawLine(MX - hr * ww, MY, MX + hr * ww, MY, stroke(GOLD, 8))
        hc.big(c, "130 KM", MX, MY + R + 110, 100, GOLD, lt, 0.8)
    elif sid == "s3":
        # corte transversal: el cuenco y la montaña en el centro (a escala vertical real: 10 km hondo, 6 km el pico)
        x0, x1 = 60, W - 60
        ys = 900
        kmv = 44  # px por km en vertical
        c.drawRect(skia.Rect.MakeXYWH(0, ys, W, H - ys), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, ys), (0, H)], [0xFF6E7684, 0xFF1E2230])))
        g = ease_out(clamp(lt / 0.9))
        pts = []
        M = 120
        p = skia.Path(); p.moveTo(0, ys)
        for i in range(M + 1):
            u = i / M
            x = lerp(x0, x1, u)
            d = abs(u - 0.5) * 2
            dep = 10 * (1 - d ** 2.4) * (1 if d < 1 else 0)
            peak = 6 * math.exp(-(d / 0.17) ** 2)
            yy = ys + (dep - peak) * kmv * g - 0.0
            p.lineTo(x, yy)
            pts.append((x, yy))
        p.lineTo(W, ys); p.lineTo(W, 0); p.lineTo(0, 0); p.close()
        c.save(); c.clipPath(p, True); space(c, t); c.restore()
        c.drawPath(skia.Path().moveTo(*pts[0]), fill(WHITE))
        for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
            c.drawLine(u0, v0, u1, v1, stroke(0xFFE6ECF6, 6))
        yfl = ys + 10 * kmv
        xl = 210
        al = ease_out(clamp((lt - 0.5) / 0.5))
        c.drawLine(xl, ys, xl, lerp(ys, yfl, al), stroke(GOLD, 7))
        if al > 0.8:
            draw_text(c, "10 KM", xl + 110, (ys + yfl) / 2 + 18, 52, GOLD)
        xm = W / 2
        ap = ease_out(clamp((lt - 2.1) / 0.5))
        ypk = yfl - 6 * kmv
        if ap > 0:
            c.drawLine(xm + 150, yfl, xm + 150, lerp(yfl, ypk, ap), stroke(CYAN, 7))
            if ap > 0.8:
                draw_text(c, "6 KM", xm + 262, (yfl + ypk) / 2 + 18, 52, CYAN)
    elif sid == "s4":
        ka = clamp(lt / 1.1)  # asteroide
        if lt < 1.1:
            mimas(c, MX, MY, MR, t)
            ax, ay = lerp(W + 80, MX, ka ** 2), lerp(420, MY, ka ** 2)
            for i in range(8):
                f = i / 8
                glow(c, lerp(ax, W + 200, f * 0.3), lerp(ay, 300, f * 0.3), 50 * (1 - f), 0xFFFFB05A, 0.5 * (1 - f))
            c.drawCircle(ax, ay, 26, fill(0xFF4A4238))
        else:
            e = clamp((lt - 1.1) / max(0.5, (b - a) - 1.4))
            sep = ease_in_out(clamp((e - 0.42) / 0.5)) * 300
            img = S.render(int(2 * MR), MIM, spin=SPIN0, tilt=0.1, light=L0, gain=1.25, limb=0.5, ambient=0.05)
            rng = random.Random(7)
            jag = [(MX + rng.uniform(-30, 30), MY - MR - 20 + i * (2 * MR + 40) / 16) for i in range(17)]
            for sgn in (-1, 1):
                pth = skia.Path(); pth.moveTo(*jag[0])
                for q in jag[1:]:
                    pth.lineTo(*q)
                pth.lineTo(MX + sgn * (MR + 80), MY + MR + 20); pth.lineTo(MX + sgn * (MR + 80), MY - MR - 20); pth.close()
                c.save()
                c.translate(sgn * sep, sgn * sep * 0.14)
                c.clipPath(pth, True)
                S.draw_planet(c, MX, MY, MR, img)
                c.restore()
            # grietas y onda
            for i in range(12):
                an = i / 12 * 6.283 + 0.3
                gl = ease_out(clamp(e / 0.4)) * MR * 0.8
                if sep < 1:
                    c.drawLine(MX + math.cos(an) * 100, MY + math.sin(an) * 100, MX + math.cos(an) * (100 + gl), MY + math.sin(an) * (100 + gl), stroke(0xFFFFD27A, 5))
            sw = clamp((lt - 1.1) / 0.8)
            c.drawCircle(MX, MY, 80 + sw * 900, stroke(with_alpha(WHITE, 0.8 * (1 - sw)), 14))
            if lt - 1.1 < 0.14:
                c.drawPaint(fill(with_alpha(WHITE, 0.9 * (1 - (lt - 1.1) / 0.14))))
            dr = random.Random(9)
            for i in range(180):
                an = dr.uniform(0, 6.283); v = dr.uniform(0.3, 1.2); sz = dr.uniform(2, 11)
                rr = 40 + v * 900 * clamp(e * 1.1)
                c.drawCircle(MX + math.cos(an) * rr, MY + math.sin(an) * rr, sz, fill(with_alpha(0xFFB9C2D0, clamp(1.2 - e))))
            K.tag(c, W / 2, 1740, "ASÍ HABRÍA ACABADO", lt - 1.8, accent=RED, size=48)
    else:
        mimas(c, MX, MY, MR, t)


def crater_ring(c, x, y, R, pu, a):
    hr = R * math.sin(65 / 198)
    c.drawCircle(x, y, hr + 8 + 8 * pu, stroke(with_alpha(GOLD, a), 7))


V1004 = dict(slug="1004_mimas_casi_se_parte", accent=GOLD, drone=0.03, scene=s_mimas, mood="epico",
             tease="LO PROMETIDO", send="ENVÍASELO A QUIEN LE GUSTE EL ESPACIO",
             rehook=("s3", "MIRA EL CENTRO"), reveal=("s4", "LO QUE CASI PASA"), segs=[
    dict(id="h", who="nar", say="Este golpe casi parte esta luna en dos. Mira ese cráter.",
         cap="Este golpe casi la *PARTE EN DOS*", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Es Mimas, una luna de Saturno. Mide unos cuatrocientos kilómetros.",
         cap="*Mimas*, luna de Saturno: | unos *400 km*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="El cráter se llama Herschel, y mide ciento treinta. Un tercio de toda la luna.",
         cap="*Herschel*: *130 km*. | ¡Un tercio de la luna!", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Tiene diez kilómetros de hondo. Y en el centro, una montaña de seis.",
         cap="*10 km* de hondo. | Y en medio, | una montaña de *6*", hold=1.0),
    dict(id="s4", who="nar", cut=True, say="Los astrónomos creen que ese golpe estuvo cerca de desintegrarla. Un poco más fuerte, y hoy quizá no existiría.",
         cap="Estuvo cerca | de *DESINTEGRARLA*", hold=1.0),
    dict(id="cta", who="nar", cut=True, say="¿A qué te recuerda esta luna? Comenta. Y sígueme: la próxima tiene una cara blanca, y otra negra.",
         cap="¿A qué te *recuerda*? | *COMENTA* | y *SÍGUEME*"),
])

VIDEOS = [V1001, V1002, V1003, V1004]


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
