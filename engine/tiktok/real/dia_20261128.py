"""Producción 28/11/2026 (3601 y 3602, motor 2D; 3603 mito_pez.py y 3604 serie_dia48.py en 3D; sin ciudad: IGEV01 327 < 332).
  3601 PRUEBA EN DIRECTO: ¿QUÉ CASILLA ES MÁS OSCURA? (tablero y sombra de Adelson). Edward H. Adelson (MIT), 1995. persci.mit.edu/gallery/checkershadow:
       'The squares marked A and B are the same shade of gray', '©1995, Edward H. Adelson'; Wikipedia 'Checker shadow illusion': 'published by Edward H.
       Adelson, professor of vision science at MIT, in 1995'. Dibujo propio (tablero, cilindro y sombra). Assert en píxeles: la casilla de arriba (oscura,
       al sol) y la de la sombra (clara, en sombra) miden el MISMO gris (120·120·120) y uniforme; y el cuentagotas del vídeo mide el frame real.
  3602 RETO DE LAS CAMPANADAS: un reloj da 6 campanadas en 5 s → 5 huecos de 1 s → 12 campanadas = 11 huecos = 11 s (no 10). Assert con fracciones.
       Las 6 campanadas SUENAN a 1 s exacto (motor v39: V['sfx'] con 'bell' sintetizada) y el dibujo se sincroniza con core.sfx_times."""
import math, sys
from fractions import Fraction as Fr
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


# ============================ 3601 tablero y sombra de Adelson
N = 5
TL_, TR_, BR_, BL_ = np.array([250., 800.]), np.array([830., 800.]), np.array([1030., 1400.]), np.array([50., 1400.])
LIGHT, DARK, SHADE_A = 200, 120, 102          # sombra = negro con alfa 102/255 → 200·(153/255) = 120 exacto
A_SQ, B_SQ = (1, 1), (2, 3)                     # (col u, fila v): A oscura al sol, B clara en la sombra
assert (A_SQ[0] + A_SQ[1]) % 2 == 0 and (B_SQ[0] + B_SQ[1]) % 2 == 1
assert round(LIGHT * (255 - SHADE_A) / 255) == DARK
SH_C, SH_R = np.array([2.55, 3.45]), np.array([1.35, 1.15])   # elipse de sombra en coordenadas de tablero
CYL = np.array([3.55, 2.55])                                     # base del cilindro


def bmap(u, v):
    """Tablero (u, v) en [0, N]² → pantalla (bilineal sobre el trapecio)."""
    a, b = u / N, v / N
    top = TL_ + (TR_ - TL_) * a; bot = BL_ + (BR_ - BL_) * a
    return top + (bot - top) * b


def _poly(pts):
    pa = skia.Path(); pa.moveTo(*pts[0])
    for p in pts[1:]:
        pa.lineTo(*p)
    pa.close(); return pa


def sq_path(i, j, inset=0.0):
    return _poly([bmap(i + inset, j + inset), bmap(i + 1 - inset, j + inset), bmap(i + 1 - inset, j + 1 - inset), bmap(i + inset, j + 1 - inset)])


def sq_center(sq):
    return bmap(sq[0] + .5, sq[1] + .5)


def shadow_path():
    pts = [bmap(*(SH_C + SH_R * np.array([math.cos(a), math.sin(a)]))) for a in np.linspace(0, 2 * math.pi, 72, endpoint=False)]
    return _poly(pts)


def gray(v):
    return skia.Color(v, v, v)


def board(c, alpha_rest=1.0):
    """Tablero + sombra + cilindro. alpha_rest < 1 apaga todo menos las casillas A y B (que quedan EXACTAS)."""
    lay = c.saveLayer(paint=skia.Paint(Alphaf=alpha_rest)) if alpha_rest < 1 else None
    for i in range(N):
        for j in range(N):
            c.drawPath(sq_path(i, j), fill(gray(DARK if (i + j) % 2 == 0 else LIGHT)))
    sh = skia.Paint(Color=skia.Color(0, 0, 0, SHADE_A), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
    c.drawPath(shadow_path(), sh)
    # canto del tablero
    edge = _poly([BL_, BR_, BR_ + (0, 40), BL_ + (0, 40)]); c.drawPath(edge, fill(0xFF5A5A5A))
    # cilindro verde
    b = bmap(*CYL); w, h = 150, 330
    body = skia.Rect.MakeXYWH(b[0] - w / 2, b[1] - h, w, h)
    c.drawRect(body, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(b[0] - w / 2, 0), skia.Point(b[0] + w / 2, 0)], [0xFF1E6A2E, 0xFF5FD07A, 0xFF2E8A44, 0xFF14451E], [0, .35, .7, 1])))
    c.drawOval(skia.Rect.MakeXYWH(b[0] - w / 2, b[1] - 22, w, 44), fill(0xFF14451E))
    c.drawOval(skia.Rect.MakeXYWH(b[0] - w / 2, b[1] - h - 22, w, 44), fill(0xFF7BE394))
    if lay is not None:
        c.restore()
        if alpha_rest < 1:     # A y B, encima y exactas (las tapa la capa semitransparente si no se repintan)
            c.drawPath(sq_path(*A_SQ), fill(gray(DARK)))
            c.drawPath(sq_path(*B_SQ), fill(gray(DARK)))


def _assert_adelson():
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(0xFF1B1E26); board(c)
    a = s.makeImageSnapshot().toarray()[..., :3].astype(int)
    for sq in (A_SQ, B_SQ):
        m = skia.Surface(W, H); mc = m.getCanvas(); mc.clear(0xFF000000); mc.drawPath(sq_path(*sq, inset=.2), fill(WHITE))
        mask = m.makeImageSnapshot().toarray()[..., 0] > 127
        vals = a[mask]
        assert mask.sum() > 4000 and abs(vals.mean() - DARK) < 0.6 and vals.std() < 0.6, (sq, vals.mean(), vals.std())
    # y las casillas vecinas sí son distintas (la ilusión tiene contraste): clara al sol 200, oscura en la sombra 72
    assert abs(a[tuple(np.round(sq_center((2, 1))[::-1]).astype(int))].mean() - LIGHT) < 1


_assert_adelson()


def s_adelson(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(0xFF1B1E26))
    rest = 1.0
    if sid == "s3":
        rest = 1 - .85 * ease_io((lt - .2) / 1.0)
    elif sid == "s4":
        rest = .15 + .85 * ease_io((lt - .3) / 1.4)
    board(c, rest)
    A, B = sq_center(A_SQ), sq_center(B_SQ)
    if sid in ("h", "s1", "cta"):     # marcas fuera de las casillas
        for p, txt, col, dx in ((A, "ARRIBA", GOLD, -0), (B, "SOMBRA", CYAN, 0)):
            c.drawPath(sq_path(*(A_SQ if txt == "ARRIBA" else B_SQ), inset=-.02), stroke(col, 7))
        K.pill(c, A[0] - 40, 735, "ARRIBA ↓", 40, bg=GOLD, fg=INK)
        K.pill(c, B[0] - 230, 1500, "↑ EN LA SOMBRA", 40, bg=CYAN, fg=INK)
    if sid == "s2":                   # tira gris del MISMO color que A, que baja hasta B
        k = ease_io((lt - 1.0) / 2.2)
        if k > 0:
            e = A + (B - A) * k
            c.drawLine(*A, *e, stroke(gray(DARK), 64))
    if sid == "s3":
        c.drawLine(*A, *B, stroke(with_alpha(gray(DARK), 1 - ease_io((lt - .2) / 1.0)), 64))
        if lt > 1.3:
            al = ease_io((lt - 1.3) / .4)
            K.eyedropper(c, *A, a=al, label_dy=-150, accent=GOLD)
            K.eyedropper(c, *B, a=al, label_dy=160, accent=CYAN)
    if sid == "s4" and lt > 2.6:
        K.tag(c, W / 2, 1840, "EDWARD ADELSON · MIT · 1995", lt - 2.6, accent=WHITE, size=32)


V3601 = dict(slug="3601_tablero_adelson", accent=GOLD, drone=0.012, scene=s_adelson, mood="misterio", music=0.035, clean=True, steady=True,
             send="ENVÍASELO Y QUE ELIJA UNA", vote=("s3", ("ARRIBA", "IGUALES"), 1, 1740), dare=("s1", "PREGÚNTALE CUÁL ES MÁS OSCURA", 1840),
             rehook=("s2", "MIRA ESTA TIRA GRIS"), reveal=("s3", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Qué casilla es más oscura, la de arriba o la de la sombra?",
         cap="¿Cuál es *MÁS OSCURA*?", hold=0.6),
    dict(id="s1", who="nar", cut=True, say="La de arriba parece casi negra, y la de la sombra casi blanca. Míralas bien un momento.",
         cap="¿La de *ARRIBA*?", hold=0.8),
    dict(id="s2", who="nar", cut=True, say="Ahora pongo una tira gris del mismo color que la de arriba, y la bajo hasta la casilla de la sombra.",
         cap="Una tira *DEL MISMO GRIS*…", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="Son exactamente el mismo gris. El cuentagotas marca lo mismo en las dos.",
         cap="*EL MISMO* gris", hold=0.8),
    dict(id="s4", who="nar", cut=True, say="Tu cerebro descuenta la sombra, y aclara esa casilla sin preguntarte. La dibujó Edward Adelson, del MIT, en mil novecientos noventa y cinco.",
         cap="Edward Adelson, *1995*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta cuál te parecía más oscura, y envíaselo a alguien para ver si se lo cree.",
         cap="¿Cuál elegiste? | *COMENTA*"),
])


# ============================ 3602 campanadas
STRIKES, SECS, ASK = 6, Fr(5), 12
GAP = SECS / (STRIKES - 1)
ANS = GAP * (ASK - 1)
assert GAP == 1 and ANS == 11 and ANS != SECS * ASK / STRIKES   # 10 es la respuesta rápida (proporción), falsa


def night(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)], [0xFF0C1430, 0xFF1C2A55, 0xFF0A0F22], [0, .6, 1])))
    for i in range(70):
        x = (i * 157.3) % W; y = (i * 97.7) % 1500
        c.drawCircle(x, y, 1.6 + (i % 3) * .8, fill(with_alpha(WHITE, .35 + .35 * math.sin(t * 2 + i))))
    # campanario: arco de piedra
    stone = 0xFF8A7F72
    c.drawRect(skia.Rect.MakeXYWH(150, 700, 780, 70), fill(stone))
    c.drawRect(skia.Rect.MakeXYWH(150, 700, 90, 760), fill(stone)); c.drawRect(skia.Rect.MakeXYWH(840, 700, 90, 760), fill(stone))
    for y in range(720, 1460, 60):
        c.drawLine(150, y, 240, y, stroke(0xFF6E655A, 3)); c.drawLine(840, y, 930, y, stroke(0xFF6E655A, 3))
    c.drawRect(skia.Rect.MakeXYWH(120, 1440, 840, 50), fill(0xFF6E655A))


def bell(c, cx, top, ang, ring):
    """Campana de bronce colgada en (cx, top), girada ang grados; ring 0..1 = brillo + ondas del golpe."""
    c.save(); c.translate(cx, top); c.rotate(ang)
    c.drawRect(skia.Rect.MakeXYWH(-90, -20, 180, 30), fill(0xFF3A2A1A))
    pa = skia.Path(); pa.moveTo(-70, 20); pa.cubicTo(-80, 120, -120, 250, -200, 330); pa.lineTo(200, 330); pa.cubicTo(120, 250, 80, 120, 70, 20); pa.close()
    c.drawPath(pa, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([skia.Point(-200, 0), skia.Point(200, 0)], [0xFF7A4A12, 0xFFFFD27A, 0xFFC0861E, 0xFF5A360C], [0, .35, .65, 1])))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-210, 320, 420, 34), 17, 17), fill(0xFFB07A1E))
    c.drawLine(0, 30, math.sin(math.radians(-ang * 1.6)) * 60, 330, stroke(0xFF3A2A1A, 14))
    c.drawCircle(math.sin(math.radians(-ang * 1.6)) * 60, 345, 26, fill(0xFF3A2A1A))
    c.restore()
    if ring > 0:
        for k in range(3):
            r = 260 + (1 - ring) * 260 + k * 70
            c.drawCircle(cx, top + 220, r, stroke(with_alpha(GOLD, ring * (.55 - k * .15)), 8))


def strike_times(P, V):
    return [tt for tt, kind, _ in K.sfx_times(V, P) if kind == "bell"]


def timeline(c, n_dots, t_dots, y=1540, x0=140, x1=940, gaps=None, hi_gap=None, lab=None):
    """Fila de campanadas (puntos dorados) con los HUECOS marcados entre ellas."""
    n = max(2, n_dots)
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    for i in range(n - 1):
        if gaps is not None and i < gaps:
            col = GREEN if hi_gap else WHITE
            c.drawLine(xs[i] + 22, y, xs[i + 1] - 22, y, stroke(with_alpha(col, .9), 8))
            if n <= 6 or i % 2 == 0 or True:
                draw_text(c, "1 s", (xs[i] + xs[i + 1]) / 2, y - 26, 30 if n > 6 else 38, with_alpha(col, .95), outline=4)
    for i in range(n):
        a = t_dots[i] if i < len(t_dots) else 0
        if a > 0:
            c.drawCircle(xs[i], y, 22 * K.ease_back(clamp(a)), fill(GOLD))
    if lab:
        K.pill(c, W / 2, y + 95, lab, 44, bg=0xEE000000, fg=GOLD)


def s_bells(c, t, P, V):
    sid, lt, d = seg(P, t)
    night(c, t)
    st = strike_times(P, V)
    # balanceo: cada campanada es un golpe que hace oscilar la campana y lanza ondas
    past = [s for s in st if s <= t]
    ring = 0.0; ang = 0.0
    if past:
        dt = t - past[-1]; ring = max(0, 1 - dt / .9); ang = 14 * math.sin(dt * 7) * math.exp(-dt * 2.2)
    ang += 2.5 * math.sin(t * 1.3)
    bell(c, W / 2, 790, ang, ring)
    if sid == "h":
        K.pill(c, W / 2 - 200, 1580, "6 = 5 s", 60, bg=GOLD, fg=INK)
        K.pill(c, W / 2 + 200, 1580, "12 = ¿?", 60, bg=RED, fg=WHITE, scale=1 + .08 * math.sin(t * 6))
    elif sid == "s1":
        shown = [clamp((t - s) / .25) for s in st]
        timeline(c, 6, shown, gaps=sum(1 for x in shown[1:] if x > .5))
        if past:
            el = min(5.0, t - st[0])
            hc.big(c, f"{el:0.1f} s", W / 2, 1450, 96, WHITE, 1.0, 0.0, outline=10)
    elif sid == "s2":
        timeline(c, 6, [1] * 6, gaps=5)
        if lt > d * .45:
            K.pill(c, W / 2, 1720, "¿EL DOBLE? 10 s", 52, bg=0xEE000000, fg=RED)
    elif sid == "s3":
        k = ease_io((lt - 2.2) / 2.0)
        n = 6 + int(round(6 * k))
        timeline(c, n, [1] * n, gaps=n - 1, lab=f"{n} CAMPANADAS = {n - 1} HUECOS")
    elif sid == "s4":
        timeline(c, 12, [1] * 12, gaps=11, hi_gap=True, lab="11 HUECOS × 1 s = 11 s")
    else:
        timeline(c, 12, [1] * 12, gaps=11, hi_gap=True)


V3602 = dict(slug="3602_reto_campanadas", accent=GOLD, drone=0.02, scene=s_bells, mood="misterio", music=0.03,
             send="ENVÍASELO A QUIEN DIGA 10", dare=("s2", "RETA A UN AMIGO YA", 1840),
             vote=("s4", ("10 s", "11 s"), 1, 1770),
             sfx=[("s1", f"e{0.3 + k}", "bell", .26) for k in range(STRIKES)],
             rehook=("s3", "ESPERA… CUENTA LOS HUECOS"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Un reloj da seis campanadas en cinco segundos. ¿Cuántos segundos tarda en dar las doce?",
         cap="¿Cuánto tarda en dar *12*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Escucha las seis campanadas y cuenta los segundos.",
         cap="*6 campanadas*, 5 segundos", hold=5.6),
    dict(id="s2", who="nar", cut=True, say="Lo que sale rápido es decir diez segundos, porque son el doble de campanadas.",
         cap="¿Diez *SEGUNDOS*?", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Pero el tiempo no está en los golpes, está en los huecos. Entre seis campanadas hay cinco huecos de un segundo, y entre doce hay once.",
         cap="Cuenta *LOS HUECOS*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Esta cuenta dice que el reloj tarda once segundos en dar las doce, no diez.",
         cap="Tarda *11 segundos*", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Comenta qué habías dicho, y envíaselo a alguien para ver si cae en la trampa del diez.",
         cap="¿Qué dijiste tú? | *COMENTA*"),
])

VIDEOS = {"3601": V3601, "3602": V3602}


def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
    return scene


if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == "check":
        sys.path.insert(0, '/home/claude/tts2'); import check_voice
        for k, V in VIDEOS.items():
            print(k, check_voice.check(V['segs']))
        raise SystemExit
    if arg == "dur":
        for k, V in VIDEOS.items():
            P = K.plan(V); print(k, round(P["total"], 1), {kk: round(v[0], 1) for kk, v in P["tl"].items()}, [round(x[0], 2) for x in K.sfx_times(V, P)])
        raise SystemExit
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        V = VIDEOS[k]
        K.run(V, make_scene(V), OUT, preview=pv)
