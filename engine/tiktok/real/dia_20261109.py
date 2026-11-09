"""Producción 09/11/2026 (1701 y 1702, motor 2D; 1703 mito_agua.py y 1704 serie_roche.py en 3D, 1709 ciudad3d).
  1701 PRUEBA EN DIRECTO: la rejilla que se cura (Healing Grid), Ryota Kanai (Universidad de Utrecht), finalista del Best Illusion of the Year 2005
       (illusionoftheyear.com, 23/08/2005): 'As you stare at the center of the grid for say 20 seconds, the regularity of the grid pattern at the center
       spreads into the irregular parts in the periphery'. La imagen NO cambia nunca (steady): lo que se ordena lo pone tu cerebro.
  1702 RETO: ¿qué cable enciende la bombilla? Cables del mismo color que se cruzan; la respuesta sale del propio trazado (assert), no se escribe a mano."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80; YEL = 0xFFFFE600


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 1701 rejilla que se cura (Kanai 2005)
GX, GY = W / 2, 1180           # punto de fijación (quieto todo el vídeo)
SP = 74


def _grid_picture():
    """Se dibuja UNA vez: centro regular, desorden creciente hacia fuera (posición y giro). Nada cambia después."""
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(0xFF0B0E1A)
    rs = np.random.RandomState(2005)
    p = stroke(0xFFF2F4FA, 9); p.setStrokeCap(skia.Paint.kButt_Cap)
    for i in range(-8, 9):
        for j in range(-7, 8):
            x0, y0 = GX + i * SP, GY + j * SP
            if not (40 < x0 < W - 40 and 760 < y0 < 1660):
                continue
            r = math.hypot(x0 - GX, y0 - GY)
            k = clamp((r - 150) / 330)          # 0 en el centro, 1 en los bordes
            dx, dy = rs.uniform(-1, 1, 2) * 20 * k
            ang = rs.uniform(-1, 1) * 38 * k
            L = 22 + rs.uniform(-1, 1) * 7 * k
            c.save(); c.translate(x0 + dx, y0 + dy); c.rotate(ang)
            c.drawLine(-L, 0, L, 0, p); c.drawLine(0, -L, 0, L, p)
            c.restore()
    return s.makeImageSnapshot()


_GRID = None


def s_heal(c, t, P, V):
    global _GRID
    if _GRID is None:
        _GRID = _grid_picture()
    sid, lt, d = seg(P, t)
    c.drawImage(_GRID, 0, 0)
    c.drawCircle(GX, GY, 15, fill(RED)); c.drawCircle(GX, GY, 15, stroke(WHITE, 4))
    if sid == "s1" and lt > .5:  # se señala el desorden FUERA de la rejilla (flechas en el borde inferior)
        K.tag(c, W / 2, 1745, "BORDES: TORCIDOS · CENTRO: RECTO", lt - .5, accent=GOLD, size=40)
    if sid in ("s2", "s3"):
        n = max(0, int(math.ceil(P["tl"]["s4"][0] - t)))
        hc.big(c, f"AGUANTA {n}", W / 2, 1790, 84, WHITE, 1.0, 0.0, outline=10)
    if sid == "s4" and lt > .6:
        K.tag(c, W / 2, 1745, "RYOTA KANAI · BEST ILLUSION OF THE YEAR 2005", lt - .6, accent=GOLD, size=32)


V1701 = dict(slug="1701_rejilla_que_se_cura", accent=GOLD, drone=0.012, scene=s_heal, mood="misterio", steady=True, music=0.03,
             send="ENVÍASELO, A VER SI A ÉL SE LE ORDENA", rehook=("s3", "NO MUEVAS LOS OJOS"), reveal=("s4", "QUÉ HA PASADO"), segs=[
    dict(id="h", who="nar", say="Mira el punto rojo del centro, sin mover los ojos. ¿Ves que los bordes están desordenados?", cap="Mira el punto *ROJO*: los bordes están *DESORDENADOS*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Las cruces de fuera están torcidas, y solo las del centro están rectas.", cap="Fuera, *torcidas*. | Solo el centro | está *recto*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Ahora mira solo el punto, y aguanta sin mover los ojos.", cap="Mira *solo el punto*… | y *aguanta*", hold=2.4),
    dict(id="s3", who="nar", cut=True, say="Poco a poco, el orden del centro se come los bordes, y parece una rejilla perfecta.", cap="El orden del centro | se *come los bordes*…", hold=1.2),
    dict(id="s4", who="nar", cut=True, say="Y la imagen no ha cambiado nada. Es la rejilla que se cura, de Ryota Kanai, de dos mil cinco.", cap="La imagen *NO ha cambiado*. | Lo ordena | *tu cerebro*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Si mueves los ojos, el desorden vuelve. Comenta si se te ordenó, y envíaselo a alguien, a ver si le pasa.", cap="¿Se te ordenó? | *SÍ o NO*: comenta"),
])


# ============================ 1702 ¿qué cable enciende la bombilla?
TOPX = [190, 420, 660, 890]          # enchufes A B C D
BOTX = [190, 420, 660, 890]          # extremos de abajo
TY, BY = 880, 1600
BULB = 1                             # la bombilla está justo debajo del B (la trampa)
PERM = {0: 3, 1: 0, 2: 2, 3: 1}      # cable i (A..D) -> extremo de abajo
LET = "ABCD"


def _cable_pts(i):
    """Spline por puntos de paso deterministas; se muestrea en 400 puntos (lo mismo sirve para dibujar y para el trazado de la respuesta)."""
    rs = np.random.RandomState(31 + i * 7)
    x0, x1 = TOPX[i], BOTX[PERM[i]]
    ys = np.linspace(TY, BY, 6)
    xs = [x0] + [float(np.clip(lerp(x0, x1, k / 5) + rs.uniform(-340, 340), 110, W - 110)) for k in range(1, 5)] + [x1]
    ctrl = list(zip(xs, ys))
    pts = []
    ext = [ctrl[0]] + ctrl + [ctrl[-1]]
    for k in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[k - 1], ext[k], ext[k + 1], ext[k + 2]
        for u in np.linspace(0, 1, 80, endpoint=False):
            u2, u3 = u * u, u * u * u
            pts.append(tuple(.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * u + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * u2 + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * u3) for a in (0, 1)))
    pts.append(ctrl[-1])
    return pts


CABLES = [_cable_pts(i) for i in range(4)]
ANSWER = [i for i in range(4) if PERM[i] == BULB][0]
assert LET[ANSWER] == "D" and PERM[1] != BULB  # el cable que sale encima de la bombilla NO llega a ella


def _crossings():
    n = 0
    for a in range(4):
        for b in range(a + 1, 4):
            A, B = np.array(CABLES[a]), np.array(CABLES[b])
            d = A[:, 0] - np.interp(A[:, 1], B[:, 1], B[:, 0])
            n += int(np.sum(np.diff(np.sign(d)) != 0))
    return n


NCROSS = _crossings()
assert NCROSS >= 5, NCROSS     # que de verdad sea un lío


def _path(pts, upto=None):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:upto]:
        p.lineTo(*q)
    return p


def _picture():
    s = skia.Surface(W, H); c = s.getCanvas()
    g = skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 600), skia.Point(0, 1800)], [0xFF2B2F3D, 0xFF161922]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    rs = np.random.RandomState(9)
    for _ in range(900):  # textura de pared
        c.drawCircle(rs.uniform(0, W), rs.uniform(0, H), rs.uniform(1, 3), fill(with_alpha(WHITE, rs.uniform(.01, .04))))
    # regleta arriba
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(90, 760, W - 90, 890), 24, 24), fill(0xFFE9E6DD))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(90, 760, W - 90, 890), 24, 24), stroke(0xFF9C978A, 5))
    for i, x in enumerate(TOPX):
        c.drawCircle(x, 810, 38, fill(0xFFCFCBBF)); c.drawCircle(x - 12, 810, 7, fill(0xFF333333)); c.drawCircle(x + 12, 810, 7, fill(0xFF333333))
    # cables (mismo color): sombra, borde oscuro, cuerpo, brillo; los cruces se leen por el orden de dibujo
    for i in (2, 0, 3, 1):
        pth = _path(CABLES[i])
        sh = stroke(with_alpha(0xFF000000, .45), 30); sh.setStrokeCap(skia.Paint.kRound_Cap); sh.setStrokeJoin(skia.Paint.kRound_Join)
        c.save(); c.translate(8, 12); c.drawPath(pth, sh); c.restore()
        for col, wdt in ((0xFF1A1A1A, 26), (0xFFE36A1E, 18), (with_alpha(0xFFFFB27A, .7), 5)):
            p = stroke(col, wdt); p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
            if wdt == 5:
                c.save(); c.translate(-4, -4); c.drawPath(pth, p); c.restore()
            else:
                c.drawPath(pth, p)
    for i, x in enumerate(TOPX):  # clavijas
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 30, 830, 60, 70), 10, 10), fill(0xFF242424))
        draw_text(c, LET[i], x, 748, 70, WHITE, shadow=True)
    for k, x in enumerate(BOTX):
        if k == BULB:
            continue
        # cable cortado: cobre pelado
        for dx in (-8, 0, 8):
            c.drawLine(x + dx * .5, BY, x + dx, BY + 34, stroke(0xFFD08A3A, 5))
        c.drawCircle(x, BY + 40, 10, fill(with_alpha(0xFFFFE08A, .25)))
    return s.makeImageSnapshot()


_PIC = None


def bulb(c, x, y, on, t):
    if on > 0:
        c.drawCircle(x, y + 90, 300, skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(x, y + 90), 300, [with_alpha(0xFFFFE27A, .55 * on), with_alpha(0xFFFFE27A, 0)], [0, 1])))
    c.drawRect(skia.Rect.MakeXYWH(x - 30, y, 60, 46), fill(0xFF8C8C96))
    for k in range(4):
        c.drawLine(x - 30, y + 8 + k * 11, x + 30, y + 14 + k * 11, stroke(0xFF5E5E66, 3))
    col = 0xFFFFF1B0 if on > .5 else 0xFF7C8090
    c.drawCircle(x, y + 110, 68, fill(with_alpha(col, .92)))
    c.drawCircle(x, y + 110, 68, stroke(with_alpha(WHITE, .6), 4))
    c.drawLine(x - 18, y + 110, x + 18, y + 110, stroke(0xFFFF9A2A if on > .5 else 0xFF4A4D58, 5))


def s_cable(c, t, P, V):
    global _PIC
    if _PIC is None:
        _PIC = _picture()
    sid, lt, d = seg(P, t)
    c.drawImage(_PIC, 0, 0)
    # polvo que flota delante de la pared (movimiento sin tocar los cables)
    rs = np.random.RandomState(4)
    for _ in range(40):
        x = (rs.uniform(0, W) + t * rs.uniform(6, 20)) % W; y = (rs.uniform(600, 1800) - t * rs.uniform(4, 14)) % 1300 + 560
        c.drawCircle(x, y, rs.uniform(1.5, 3.5), fill(with_alpha(WHITE, .12)))
    on = 0.0
    t3 = P["tl"]["s3"][0]
    if t >= t3:
        lt3 = t - t3; d3 = P["tl"]["s3"][1] - t3
        # 1º se recorre el B (la trampa) en rojo, luego el D en amarillo
        for i, (a, b, col) in ((1, (0.2, 0.42 * d3, RED)), (ANSWER, (0.5 * d3, 0.9 * d3, YEL))):
            k = clamp((lt3 - a) / (b - a))
            if k <= 0:
                continue
            n = max(2, int(len(CABLES[i]) * ease_out(k)))
            gp = stroke(with_alpha(col, .35), 44); gp.setStrokeCap(skia.Paint.kRound_Cap); gp.setStrokeJoin(skia.Paint.kRound_Join)
            pp = stroke(col, 16); pp.setStrokeCap(skia.Paint.kRound_Cap); pp.setStrokeJoin(skia.Paint.kRound_Join)
            pth = _path(CABLES[i], n)
            c.drawPath(pth, gp); c.drawPath(pth, pp)
            hx, hy = CABLES[i][n - 1]
            c.drawCircle(hx, hy, 22 + 4 * math.sin(t * 20), fill(WHITE))
            if i == 1 and k >= 1:
                hc.big(c, "✗", BOTX[PERM[1]], BY + 120, 110, RED, 1.0, 0.0, outline=10)
        on = clamp((lt3 - 0.9 * d3) / .25)
    if sid == "cta":
        on = 1.0
    bulb(c, BOTX[BULB], BY - 10, on, t)
    if on <= 0:
        draw_text(c, "?", BOTX[BULB], BY + 125, 70, WHITE, shadow=False)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1800, 120, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > .6:
        K.tag(c, W / 2, 1800, "EL B SALE JUSTO ENCIMA…", lt - .6, accent=GOLD, size=40)
    if sid in ("s4", "cta") and t < P["total"] - .5:
        K.tag(c, W / 2, 1800, f"ES EL {LET[ANSWER]}", (t - P['tl']['s4'][0]), accent=GREEN, size=56)


V1702 = dict(slug="1702_que_cable_enciende", accent=GOLD, drone=0.02, scene=s_cable, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", rehook=("s2", "AQUÍ ESTÁ LA TRAMPA"), reveal=("s3", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Solo uno de estos cables enciende la bombilla. ¿Sabes cuál de los cuatro es?", cap="¿Qué cable enciende la *BOMBILLA*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos, y no vale usar el dedo, solo los ojos.", cap="*5 segundos*. | Sin dedo, | *solo los ojos*", hold=4.2),
    dict(id="s2", who="nar", cut=True, say="Ojo con la trampa, porque el cable que sale justo encima de la bombilla no llega hasta ella.", cap="El que sale *justo encima*… | *no llega*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Vamos a seguirlos. El B se escapa hasta el corte de la izquierda, y el que llega de verdad es el D.", cap="El *B* se escapa… | y llega *el D*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Era el que salía más lejos de la bombilla, al otro lado de la regleta.", cap="Es *el D*: | el que sale | *más lejos*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta qué letra dijiste antes de la respuesta, y envíaselo a quien crea que lo saca en cinco segundos.", cap="¿Qué letra dijiste? | *COMENTA*"),
])
VIDEOS = {"1701": V1701, "1702": V1702}


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
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        K.run(VIDEOS[k], make_scene(VIDEOS[k]), OUT, preview=pv)
