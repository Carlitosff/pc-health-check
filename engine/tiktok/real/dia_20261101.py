"""Producción 01/11/2026 (802–805) — PLAYBOOK v3 'menos y mejor': 4 vídeos + montaña (801, montana.py 90 113).
Motor v11: V['steady'] (ilusiones en directo sin zoom/sacudidas/destellos) + montaña con nieve real al pasar 100 m.
Mezcla fija:
  802 PRUEBA EN DIRECTO: perseguidor lila (Jeremy Hinton, antes de 2005; 12 discos, fijar la cruz -> disco verde)
  803 RETO: ¿cuántos cubos? escalera en esquina 4 pisos = 16+9+4+1 = 30 (calculado con assert)
  804 MITO CON 'TÚ': tu perro y la cola (Quaranta, Siniscalchi, Vallortigara, Univ. Trieste, Current Biology 2007,
      30 perros: dueño -> más a la derecha; perro grande desconocido -> más a la izquierda)  [TRIAL REEL]
  805 SERIE (lo prometido tras Encélado): Tritón (≈2.700 km, órbita retrógrada, Voyager 2 agosto 1989, géiseres de
      nitrógeno 8 km, ≈ −235 °C, en ≈3.600 M años cruzará el límite de Roche y se romperá) -> próxima: Miranda.
Voz: kokoroP:em_santa (core.VOICES por defecto, elegida por Carlos) con pausas."""
import math, sys, random
import numpy as np
import skia
from PIL import Image, ImageFilter
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
import dia_20261031 as D
from core import glow, W, H, WHITE, INK, clamp, lerp, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, draw_text

OUT = "/home/claude/tiktok/outdaily"
GREEN = 0xFF2FD46B
RED = 0xFFFF3B4A
seg = D.seg
blur = D.blur


# ====================================================================== 802 Perseguidor lila (en directo)
GREY = 0xFFBDBDBD
LILAC = 0xFFE58FE5
LC = (W / 2, 1260)
LR = 330


def lilac_disc_img():
    s = skia.Surface(260, 260)
    with s as c:
        c.clear(0x00000000)
        c.drawCircle(130, 130, 62, skia.Paint(AntiAlias=True, Color=LILAC, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26)))
    return s.makeImageSnapshot()


DISC = lilac_disc_img()


def lilac(c, t):
    c.clear(GREY)
    gone = int(t / 0.125) % 12  # 8 pasos por segundo, un disco ausente cada vez (como el original)
    for k in range(12):
        if k == gone:
            continue
        a = -math.pi / 2 + 2 * math.pi * k / 12
        x, y = LC[0] + LR * math.cos(a), LC[1] + LR * math.sin(a)
        c.drawImage(DISC, x - 130, y - 130)
    cx, cy = LC
    c.drawRect(skia.Rect.MakeXYWH(cx - 22, cy - 3.5, 44, 7), fill(0xFF000000))
    c.drawRect(skia.Rect.MakeXYWH(cx - 3.5, cy - 22, 7, 44), fill(0xFF000000))


def s_lilac(c, t, P, V):
    sid, lt = seg(P, t)
    lilac(c, t)
    # flecha que señala la cruz solo en el gancho (fuera del anillo para no tapar nada)
    if sid == "h":
        a = clamp(t / 0.3) * (0.6 + 0.4 * math.sin(t * 8))
        y = LC[1] + LR + 230 + math.sin(t * 6) * 12
        p = skia.Path(); p.moveTo(LC[0], y - 70); p.lineTo(LC[0] - 40, y); p.lineTo(LC[0] + 40, y); p.close()
        c.drawPath(p, fill(with_alpha(RED, a)))
        draw_text(c, "MIRA LA CRUZ", LC[0], y + 70, 54, with_alpha(INK, a))


V802 = dict(slug="802_perseguidor_lila_en_directo", accent=0xFFB04AD0, drone=0.0, music=0.035, scene=s_lilac, mood="misterio",
            steady=True, clean=True, tease="NO APARTES LA VISTA", send="ENVÍASELO A UN AMIGO, A VER SI LO VE",
            rehook=("s2", "NO MUEVAS LOS OJOS"), reveal=("s3", "LA EXPLICACIÓN"), segs=[
    dict(id="h", who="nar", say="Mira la cruz del centro, y no apartes la vista. ¿De qué color es el círculo que gira?",
         cap="Mira la *CRUZ*… | ¿de qué *COLOR* | es el que gira?", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Son rosas. Pero tú sigue mirando la cruz. Sin parpadear.",
         cap="Son *ROSAS*… | tú sigue mirando | la *cruz*", hold=0.7),
    dict(id="s2", who="nar", cut=True, say="No muevas los ojos. ¿Ya lo ves? ¿Y dónde se han ido los rosas?",
         cap="¿Ya lo ves? | ¿Y dónde se han | ido los *rosas*?", hold=1.4),
    dict(id="s3", who="nar", cut=True, say="Ahí no hay nada verde. Es la huella que deja el rosa en tu ojo.",
         cap="No hay *NADA VERDE*: | es la *huella* del rosa | en tu ojo", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Y los rosas se borran porque tu cerebro ignora lo borroso y quieto. Es el perseguidor lila.",
         cap="Tu cerebro *borra* | lo borroso y quieto. | *Perseguidor lila*", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="¿Viste el círculo verde? Comenta sí o no. Y envíaselo a un amigo, a ver si lo ve.",
         cap="¿Viste el *VERDE*? | Comenta *SÍ* o *NO*"),
])


# ====================================================================== 803 Reto: ¿cuántos cubos? (30)
NCUBE = 4
CUBES = [(i, j, k) for k in range(NCUBE) for i in range(NCUBE - k) for j in range(NCUBE - k)]
assert len(CUBES) == 30 and [sum(1 for q in CUBES if q[2] == k) for k in range(4)] == [16, 9, 4, 1]
CUBE_COLS = [(0xFF4AA8FF, 0xFF2C7AD0, 0xFF1C559A), (0xFFFFB84A, 0xFFE08A1C, 0xFFAA6410),
             (0xFF7AE07A, 0xFF3AB04A, 0xFF267A32), (0xFFFF6A8A, 0xFFE03A5C, 0xFFA82640)]


def iso(i, j, k, cx, cy, s):
    return cx + (i - j) * s * 0.866, cy + (i + j) * s * 0.5 - k * s


def cube(c, i, j, k, cx, cy, s, cols, hl=0.0, lift=0.0):
    def P(a, b, d):
        x, y = iso(a, b, d, cx, cy, s)
        return x, y - lift
    top = [P(i, j, k + 1), P(i + 1, j, k + 1), P(i + 1, j + 1, k + 1), P(i, j + 1, k + 1)]
    right = [P(i + 1, j, k + 1), P(i + 1, j + 1, k + 1), P(i + 1, j + 1, k), P(i + 1, j, k)]
    left = [P(i, j + 1, k + 1), P(i + 1, j + 1, k + 1), P(i + 1, j + 1, k), P(i, j + 1, k)]
    for poly, col in ((top, cols[0]), (right, cols[1]), (left, cols[2])):
        p = skia.Path(); p.moveTo(*poly[0])
        for q in poly[1:]:
            p.lineTo(*q)
        p.close()
        c.drawPath(p, fill(col))
        if hl > 0:
            c.drawPath(p, fill(with_alpha(WHITE, 0.35 * hl)))
        c.drawPath(p, stroke(0xFF101420, 4))


def stack(c, t, cx, cy, s, explode=0.0, hl_layer=-1, hl=0.0, mono=True):
    order = sorted(CUBES, key=lambda q: (q[2], q[0] + q[1]))
    for (i, j, k) in order:
        cols = CUBE_COLS[0] if mono else CUBE_COLS[k]
        lift = explode * k * s * 0.9
        cube(c, i, j, k, cx, cy, s, cols, hl=hl if k == hl_layer else 0.0, lift=lift)


def s_cubos(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A2A4A, 0xFF2A0A4A, seed=803)
    s = 104
    cy = 1110 + math.sin(t * 1.3) * 10
    cx = W / 2
    lay = {"s3": 3, "s4": 2, "s5": 1, "s6": 0}
    base = {"s3": 0, "s4": 1, "s5": 5, "s6": 14}
    ex = 0.0
    if sid in lay or sid == "cta":
        ex = ease_in_out(clamp((t - P["tl"]["s3"][0]) / 0.9))
    if sid == "cta":
        ex = 1.0 - ease_in_out(clamp(lt / 0.8))
    mono = sid in ("h", "s1", "s2")
    cy2 = cy + 190 * ex  # al separar los pisos, la base baja un poco para que quepa todo
    stack(c, t, cx, cy2, s, explode=ex, hl_layer=lay.get(sid, -1), hl=0.6 + 0.4 * math.sin(t * 8), mono=mono)
    if sid in lay:
        k = lay[sid]
        n = (NCUBE - k) ** 2
        dur = max(0.9, (P["tl"][sid][1] - P["tl"][sid][0]) - 0.4)
        shown = min(n, int(lt / (dur / n)) + 1)
        hc.big(c, str(base[sid] + shown), W / 2, 1830, 130, V["accent"], 1.0, 0.0)
    if sid == "h":
        hc.timer(c, W / 2, 1830, 64, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s1":
        K.tag(c, W / 2, 1850, "COMENTA TU NÚMERO", lt - 0.2, accent=V["accent"], size=44)
    if sid == "cta":
        hc.stamp(c, "30", W / 2, 1800, lt, 0.1, 130, col=GREEN)


V803 = dict(slug="803_cuantos_cubos_30", accent=0xFFFFC23A, drone=0.02, scene=s_cubos, mood="misterio",
            tease="CASI NADIE ACIERTA", send="RETA A UN AMIGO: ENVÍASELO", rehook=("s5", "AQUÍ FALLA CASI TODO EL MUNDO"),
            reveal=("cta", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="¿Cuántos cubos hay aquí? Tienes tres segundos.",
         cap="¿Cuántos *CUBOS* | hay aquí?", hold=1.6),
    dict(id="s1", who="nar", cut=True, say="Cuenta también los que no se ven. Escribe tu número antes de seguir.",
         cap="También los que | *NO SE VEN*. | Escribe tu número", hold=0.8),
    dict(id="s2", who="q", cut=True, say="¿Ya? Vamos a separarlos.", cap="¿Ya? | Vamos a *separarlos*"),
    dict(id="s3", who="nar", cut=True, say="Arriba del todo, uno.", cap="Arriba: *UNO*", hold=0.8),
    dict(id="s4", who="nar", cut=True, say="El segundo piso, cuatro.", cap="Segundo piso: *CUATRO*", hold=0.8),
    dict(id="s5", who="nar", cut=True, say="El tercero, nueve. Aunque desde arriba solo veías cinco.",
         cap="Tercero: *NUEVE*. | Desde arriba | solo veías *cinco*", hold=0.8),
    dict(id="s6", who="nar", cut=True, say="Y la base, dieciséis.", cap="Y la base: *16*", hold=1.0),
    dict(id="cta", who="nar", cut=True, say="Treinta cubos. ¿Cuántos dijiste tú? Comenta, y reta a un amigo.",
         cap="Total: *30*. ¿Y tú? | *COMENTA* | y reta a un amigo"),
])


# ====================================================================== 804 Mito: tu perro y la cola
FUR = (0xFFC98A4A, 0xFF8A5426)


def dog_back(c, x, y, s, t, wag_side=1.0, wag=1.0):
    """Perro visto desde atrás (sentado), con pelaje degradado; la cola barre más hacia wag_side (+1 su derecha =
    derecha de la pantalla, porque lo vemos por detrás)."""
    sh = skia.Paint(AntiAlias=True, Color=0x55000000, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
    c.drawOval(skia.Rect.MakeXYWH(x - 300 * s, y + 330 * s, 600 * s, 90 * s), sh)
    body = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((x - 60 * s, y - 40 * s), 420 * s, [FUR[0], FUR[1]]))
    # patas traseras
    for sx in (-1, 1):
        c.drawOval(skia.Rect.MakeXYWH(x + sx * 150 * s - 120 * s, y + 120 * s, 240 * s, 250 * s), body)
        c.drawOval(skia.Rect.MakeXYWH(x + sx * 190 * s - 70 * s, y + 320 * s, 140 * s, 60 * s), fill(FUR[1]))
    # cuerpo
    c.drawOval(skia.Rect.MakeXYWH(x - 230 * s, y - 230 * s, 460 * s, 560 * s), body)
    # cabeza y orejas
    hy = y - 360 * s
    c.drawOval(skia.Rect.MakeXYWH(x - 95 * s, hy + 60 * s, 190 * s, 200 * s), fill(FUR[1]))  # cuello en sombra
    head = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((x - 50 * s, hy - 50 * s), 260 * s, [0xFFD89A5A, FUR[1]]))
    c.drawOval(skia.Rect.MakeXYWH(x - 140 * s, hy - 120 * s, 280 * s, 250 * s), head)
    for sx in (-1, 1):  # orejas caídas que se balancean
        sw = math.sin(t * 2.2 + sx) * 0.08
        c.save(); c.translate(x + sx * 120 * s, hy - 70 * s); c.rotate(math.degrees(sx * (0.25 + sw)))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-45 * s, 0, 90 * s, 210 * s), 45 * s, 45 * s), fill(0xFF5A3214))
        c.restore()
    c.drawArc(skia.Rect.MakeXYWH(x - 140 * s, hy - 120 * s, 280 * s, 250 * s), 190, 120, False, stroke(with_alpha(0xFFFFE0B0, 0.5), 6 * s))
    c.drawArc(skia.Rect.MakeXYWH(x - 230 * s, y - 230 * s, 460 * s, 560 * s), 190, 90, False, stroke(with_alpha(0xFFFFE0B0, 0.35), 8 * s))
    # textura de pelo: trazos finos
    R = random.Random(4)
    for i in range(160):
        a = R.uniform(0, 6.28); r = R.uniform(0, 1) ** 0.5
        px, py = x + math.cos(a) * r * 200 * s, y + 40 * s + math.sin(a) * r * 260 * s
        c.drawLine(px, py, px + 6 * s, py + 16 * s, stroke(with_alpha(0xFF5A3214, 0.35), 2.5 * s))
    # cola: barrido asimétrico
    base = (x, y + 250 * s)
    sweep = math.sin(t * 11) * 0.5 + 0.5
    amp = 0.95 * wag
    ang = -math.pi / 2 + wag_side * (0.25 + amp * sweep) - (1 - abs(wag_side)) * 0
    if wag_side == 0:
        ang = -math.pi / 2 + amp * math.sin(t * 11)
    L = 280 * s
    tip = (base[0] + math.cos(ang) * L, base[1] + math.sin(ang) * L)
    mid = (base[0] + math.cos(ang - 0.35 * wag_side) * L * 0.55, base[1] + math.sin(ang - 0.35 * wag_side) * L * 0.55)
    p = skia.Path(); p.moveTo(*base); p.quadTo(*mid, *tip)
    c.drawPath(p, stroke(FUR[1], 52 * s))
    c.drawPath(p, stroke(FUR[0], 34 * s))
    c.drawCircle(*tip, 24 * s, fill(0xFFF0D6B0))
    # rastro del movimiento
    for k in range(1, 4):
        sw2 = math.sin(t * 11 - k * 0.35) * 0.5 + 0.5
        a2 = -math.pi / 2 + wag_side * (0.25 + amp * sw2) if wag_side else -math.pi / 2 + amp * math.sin(t * 11 - k * 0.35)
        c.drawCircle(base[0] + math.cos(a2) * L, base[1] + math.sin(a2) * L, 20 * s, fill(with_alpha(0xFFF0D6B0, 0.25 / k)))


def meter(c, x, y, side, lt, accent):
    """Medidor IZQUIERDA / DERECHA con aguja."""
    k = ease_out(clamp(lt / 0.6))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 380, y - 40, 760, 80), 40, 40), fill(with_alpha(0xFF101420, 0.85 * k)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 380, y - 40, 380, 80), 40, 40), fill(with_alpha(RED, 0.35 * k)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - 40, 380, 80), 40, 40), fill(with_alpha(GREEN, 0.35 * k)))
    draw_text(c, "IZQUIERDA", x - 200, y + 14, 36, with_alpha(WHITE, k))
    draw_text(c, "DERECHA", x + 200, y + 14, 36, with_alpha(WHITE, k))
    nx = x + side * 300 * ease_out(clamp((lt - 0.3) / 0.8)) + math.sin(lt * 9) * 8
    c.drawCircle(nx, y, 34, fill(with_alpha(accent, k)))
    c.drawCircle(nx, y, 34, stroke(with_alpha(INK, k), 6))


def person(c, x, y, s, t, a=1.0):
    """'Llega su dueño': puerta que se abre con luz cálida y corazón que late (sin figura humana)."""
    k = ease_out(clamp(t % 100 / 0.6)) if False else 1.0
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 150, y - 260, 300, 470), 20, 20), fill(with_alpha(0xFF3A2A1A, a)))
    c.drawRect(skia.Rect.MakeXYWH(x - 125, y - 235, 250, 420), skia.Paint(AntiAlias=True,
               Shader=skia.GradientShader.MakeRadial((x, y), 330, [0xFFFFE6A8, 0xFFFFB84A])))
    glow(c, x, y, 380, 0xFFFFC870, 0.35 * a)
    hx, hy, hs = x, y - 30 + math.sin(t * 4) * 6, 60 * s * (1 + 0.12 * math.sin(t * 8))
    hp = skia.Path(); hp.moveTo(hx, hy + hs); hp.cubicTo(hx - 2.2 * hs, hy - 0.4 * hs, hx - 0.9 * hs, hy - 1.6 * hs, hx, hy - 0.5 * hs)
    hp.cubicTo(hx + 0.9 * hs, hy - 1.6 * hs, hx + 2.2 * hs, hy - 0.4 * hs, hx, hy + hs); hp.close()
    c.drawPath(hp, fill(with_alpha(RED, a)))


def big_dog(c, x, y, s, t, a=1.0):
    """Silueta de perro grande desconocido (de perfil) con ojos brillantes."""
    p = skia.Path()
    p.moveTo(x - 260 * s, y); p.lineTo(x - 250 * s, y - 180 * s); p.lineTo(x + 120 * s, y - 200 * s); p.lineTo(x + 180 * s, y - 330 * s)
    p.lineTo(x + 210 * s, y - 420 * s); p.lineTo(x + 250 * s, y - 330 * s); p.lineTo(x + 330 * s, y - 300 * s); p.lineTo(x + 260 * s, y - 230 * s)
    p.lineTo(x + 200 * s, y - 180 * s); p.lineTo(x + 190 * s, y); p.lineTo(x + 140 * s, y); p.lineTo(x + 120 * s, y - 110 * s)
    p.lineTo(x - 170 * s, y - 110 * s); p.lineTo(x - 190 * s, y); p.close()
    c.drawPath(p, fill(with_alpha(0xFF15151C, a)))
    g = 0.6 + 0.4 * math.sin(t * 6)
    c.drawCircle(x + 240 * s, y - 320 * s, 12 * s, skia.Paint(AntiAlias=True, Color=with_alpha(0xFFFFD040, a * g), MaskFilter=blur(4)))


def s_perro(c, t, P, V):
    sid, lt = seg(P, t)
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF2A3A5A, 0xFF4A6A4A])))
    # césped con movimiento
    c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, H - 1500), fill(0xFF2E5A2A))
    R = random.Random(9)
    for i in range(120):
        gx = R.uniform(0, W); gy = R.uniform(1500, H)
        sw = math.sin(t * 2 + gx * 0.01) * 8
        c.drawLine(gx, gy, gx + sw, gy - R.uniform(18, 40), stroke(0xFF4A8A3A, 4))
    dx, dy, ds = W / 2, 1360, 1.0
    if sid == "h":
        dog_back(c, dx, dy, ds, t, wag_side=0, wag=1.0)
        a = clamp((lt - 0.4) / 0.3)
        draw_text(c, "?", dx + 300, 900 + math.sin(t * 5) * 10, 220, with_alpha(0xFFFFC23A, a))
    elif sid == "s1":
        dog_back(c, dx, dy, ds * 0.85, t, wag_side=0, wag=0.6)
        hc.big(c, "2007", W / 2 - 250, 820, 120, V["accent"], lt, 0.2)
        hc.big(c, "30", W / 2 + 270, 820, 120, V["accent"], lt, 0.5)
        K.tag(c, W / 2 + 270, 930, "PERROS", lt - 0.6, accent=WHITE, size=34)
        K.tag(c, W / 2, 1850, "UNIVERSIDAD DE TRIESTE", lt - 0.8, accent=V["accent"], size=38)
    elif sid == "s2":
        person(c, W - 230, 900, 1.0, t)
        dog_back(c, dx, dy + 40, ds * 0.85, t, wag_side=1.0, wag=1.0)
        meter(c, W / 2, 1850, 1, lt, V["accent"])
    elif sid == "s3":
        a = ease_out(clamp(lt / 0.5))
        c.drawPaint(fill(with_alpha(0xFF0A0408, 0.55 * a)))
        glow(c, W / 2, 820, 520, 0xFFFF2A2A, 0.18 * a)
        for ex_ in (-110, 110):  # ojos en la oscuridad de un perro grande desconocido
            g = (0.7 + 0.3 * math.sin(t * 5)) * a
            c.drawOval(skia.Rect.MakeXYWH(W / 2 + ex_ - 46, 780, 92, 52), skia.Paint(AntiAlias=True, Color=with_alpha(0xFFFFD040, g), MaskFilter=blur(6)))
            c.drawOval(skia.Rect.MakeXYWH(W / 2 + ex_ - 10, 784, 20, 44), fill(with_alpha(0xFF100800, a)))
        K.tag(c, W / 2, 920, "PERRO GRANDE DESCONOCIDO", lt - 0.5, accent=RED, size=36)
        dog_back(c, dx, dy + 40, ds * 0.85, t, wag_side=-1.0, wag=0.55)
        meter(c, W / 2, 1850, -1, lt, V["accent"])
        hc.stamp(c, "ALERTA", W / 2, 1650, lt, 1.4, 80, col=RED)
    elif sid == "s4":
        dog_back(c, dx, dy, ds * 0.9, t, wag_side=1.0 if int(lt * 0.8) % 2 == 0 else -1.0, wag=0.8)
        K.tag(c, W / 2, 760, "CURRENT BIOLOGY · 2007", lt - 0.3, accent=V["accent"], size=40)
    else:
        dog_back(c, dx, dy, ds * 0.9, t, wag_side=1.0, wag=1.0)


V804 = dict(slug="804_mito_tu_perro_cola", accent=0xFFFFC23A, drone=0.02, scene=s_perro, mood="luz",
            tease="CASI NADIE LO SABE", send="ENVÍASELO A ALGUIEN CON PERRO",
            rehook=("s3", "Y AQUÍ VIENE LO RARO"), reveal=("s2", "HACIA DÓNDE"), segs=[
    dict(id="h", who="nar", say="Si tu perro mueve la cola, no siempre está contento. Fíjate hacia dónde la mueve.",
         cap="¿Tu perro mueve la cola | porque está *CONTENTO*? | *No siempre*", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="En dos mil siete, en la Universidad de Trieste, grabaron a treinta perros.",
         cap="*2007*, Universidad | de *Trieste*: | *30 perros*"),
    dict(id="s2", who="nar", cut=True, say="Cuando veían a su dueño, movían la cola más hacia su derecha.",
         cap="Ven a su *DUEÑO*: | más hacia su *DERECHA*", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="Pero ante un perro grande y desconocido, la movían más hacia la izquierda.",
         cap="Ante un *perro grande* | desconocido: | hacia la *IZQUIERDA*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Así que no mires solo cuánto la mueve. Mira hacia dónde.",
         cap="No mires *cuánto* | la mueve: mira | *HACIA DÓNDE*"),
    dict(id="cta", who="nar", cut=True, say="¿Hacia dónde la mueve el tuyo? Comenta derecha o izquierda. Y envíaselo a alguien con perro.",
         cap="¿Y el tuyo? Comenta | *DERECHA* o *IZQUIERDA*"),
])


# ====================================================================== 805 Tritón (lo prometido tras Encélado)
L0 = (-0.55, 0.3, 0.78)
ST = K.Stars(seed=805)


def triton_texture():
    path = S.TEX + "triton_proc.png"
    try:
        Image.open(path)
        return S.load("triton_proc.png")
    except Exception:
        pass
    w, h = 2048, 1024
    rnd = np.random.default_rng(805)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = np.zeros((h, w), np.float32)
    for k in range(6):
        f = 2 ** k
        ph = rnd.uniform(0, 6.28, 3)
        n += np.sin(xx / w * 6.28 * f + ph[0] + 1.7 * np.sin(yy / h * 6.28 * f + ph[1])) * np.cos(yy / h * 3.14 * f + ph[2]) / (k + 1)
    n = (n - n.min()) / (n.max() - n.min())
    # terreno 'piel de melón' (cantaloupe): celdas
    cell = np.sin(xx / 22.0 + 3 * n) * np.sin(yy / 22.0 + 3 * n)
    v = 0.72 + 0.16 * n + 0.06 * cell
    img = np.stack([v * 1.0, v * 0.88, v * 0.80], -1)
    # casquete polar sur rosado y brillante
    cap = np.clip((yy / h - 0.58) / 0.12, 0, 1)
    img = img * (1 - cap[..., None]) + np.array([0.96, 0.84, 0.82]) * cap[..., None]
    # rayas oscuras de los géiseres (arrastradas por el viento, todas hacia el noreste)
    for _ in range(70):
        x0, y0 = rnd.uniform(0, w), rnd.uniform(h * 0.66, h * 0.86)
        L = rnd.uniform(25, 70)
        for s in np.linspace(0, 1, 30):
            px, py = int((x0 + s * L) % w), int(y0 - s * L * 0.35)
            img[max(0, py - 3):py + 3, max(0, px - 3):px + 3] *= 0.72
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    im.save(path)
    return S.load("triton_proc.png")


TRI = triton_texture()
NEP = S.load("neptunemap.jpg")


def triton(c, x, y, R, t):
    S.draw_planet(c, x, y, R, S.render(int(2 * R), TRI, spin=-t * 0.08, tilt=0.35, light=L0, gain=1.1, limb=0.5, ambient=0.08))
    S.atmosphere(c, x, y, R, color=0xFFCFE0FF, strength=0.3)


def neptune(c, x, y, R, t):
    S.draw_planet(c, x, y, R, S.render(int(2 * R), NEP, spin=t * 0.12, light=L0, gain=1.15, limb=0.6, ambient=0.06))
    S.atmosphere(c, x, y, R, color=0xFF4A7AFF, strength=0.9)


def arrow_arc(c, cx, cy, rx, ry, a0, a1, col, w=10):
    p = skia.Path()
    n = 40
    for i in range(n + 1):
        a = lerp(a0, a1, i / n)
        x, y = cx + math.cos(a) * rx, cy + math.sin(a) * ry
        p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
    c.drawPath(p, stroke(col, w))
    ax, ay = cx + math.cos(a1) * rx, cy + math.sin(a1) * ry
    d = 1 if a1 > a0 else -1
    tx, ty = -math.sin(a1) * rx * d, math.cos(a1) * ry * d
    L = math.hypot(tx, ty) or 1
    tx, ty = tx / L, ty / L
    h = skia.Path(); h.moveTo(ax + tx * 30, ay + ty * 30); h.lineTo(ax - ty * 18, ay + tx * 18); h.lineTo(ax + ty * 18, ay - tx * 18); h.close()
    c.drawPath(h, fill(col))


def geysers(c, x, y, R, t, k=1.0):
    """Penachos de nitrógeno: columnas oscuras que suben recto y luego el viento las tumba (como vio la Voyager 2)."""
    rr = random.Random(805)
    for g in range(4):
        gx = x + (g - 1.5) * R * 0.28
        gy = y - R * 0.98 + abs(g - 1.5) * 18
        for i in range(70):
            ph = (t * 0.35 + i / 70) % 1.0
            hgt = ph * R * 0.75
            bend = max(0, hgt - R * 0.45) * 1.6
            px, py = gx + bend + rr.uniform(-6, 6), gy - min(hgt, R * 0.45)
            a = k * (1 - ph) * 0.55
            c.drawCircle(px, py, 6 + ph * 16, skia.Paint(AntiAlias=True, Color=with_alpha(0xFFB8B0BC, a), MaskFilter=blur(5)))


def s_triton(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF02030A)
    ST.draw(c, t, camx=t * 9, alpha=0.9)
    if sid == "h":
        neptune(c, W * 0.2, 560, 190, t)
        R = lerp(320, 390, ease_out(clamp(t / 3)))
        triton(c, W / 2 + 60, 1080, R, t)
        arrow_arc(c, W / 2 + 60, 1080, R + 70, (R + 70) * 0.35, 0.3, 2.6, 0xFFFF5A5A, 12)
        hc.stamp(c, "GIRA AL REVÉS", W / 2, 1820, lt, 0.9, 96, col=RED)
    elif sid == "s1":
        cx, cy = W / 2, 1150
        neptune(c, cx, cy, 230, t)
        arrow_arc(c, cx, cy, 290, 90, -2.6, -0.5, 0xFF7AD0FF, 9)  # giro de Neptuno
        a = -t * 0.9  # Tritón en sentido contrario
        orbit_rx, orbit_ry = 470, 170
        c.drawOval(skia.Rect.MakeXYWH(cx - orbit_rx, cy - orbit_ry, 2 * orbit_rx, 2 * orbit_ry), stroke(with_alpha(WHITE, 0.25), 3))
        tx, ty = cx + math.cos(a) * orbit_rx, cy + math.sin(a) * orbit_ry
        triton(c, tx, ty, 60, t)
        K.tag(c, W / 2, 1520, "≈ 2.700 km · LUNA DE NEPTUNO", lt - 0.4, accent=V["accent"], size=40)
        K.tag(c, W / 2, 1600, "LA ÚNICA LUNA GRANDE AL REVÉS", lt - 1.4, accent=WHITE, size=36)
    elif sid == "s2":
        # captura: Tritón llega desde fuera y se queda atrapado
        cx, cy = W / 2 - 120, 1150
        neptune(c, cx, cy, 200, t)
        k = ease_in_out(clamp(lt / 2.2))
        ang = lerp(-0.4, 2.2, k)
        rr = lerp(900, 420, k)
        tx, ty = cx + math.cos(ang) * rr, cy - math.sin(ang) * rr * 0.55
        for j in range(1, 12):  # estela
            k2 = clamp(k - j * 0.025)
            a2, r2 = lerp(-0.4, 2.2, k2), lerp(900, 420, k2)
            c.drawCircle(cx + math.cos(a2) * r2, cy - math.sin(a2) * r2 * 0.55, 18, fill(with_alpha(0xFFFFD8C8, 0.3 * (1 - j / 12))))
        triton(c, tx, ty, 70, t)
        hc.stamp(c, "CAPTURADA", W / 2, 1750, lt, 1.6, 100, col=0xFFFFB84A)
    elif sid == "s3":
        R = 470
        triton(c, W / 2, 1500, R, t)
        geysers(c, W / 2, 1500, R, t, k=ease_out(clamp(lt / 0.8)))
        hc.big(c, "8 km", W / 2 - 250, 760, 120, V["accent"], lt, 0.4)
        hc.big(c, "−235 °C", W / 2 + 200, 760, 110, 0xFF9AD8FF, lt, 1.2)
        K.tag(c, W / 2, 880, "VOYAGER 2 · AGOSTO 1989", lt - 0.3, accent=WHITE, size=36)
    elif sid == "s4":
        cx, cy = W / 2, 1150
        neptune(c, cx, cy, 230, t)
        k = ease_in(clamp(lt / 3.2)) if hasattr(K, "ease_in") else clamp(lt / 3.2) ** 2
        rr = lerp(470, 300, k)
        if k < 0.85:
            a = -t * 1.2
            triton(c, cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.36, 60, t)
        else:  # se rompe y forma un anillo
            q = clamp((k - 0.85) / 0.15)
            R2 = random.Random(3)
            for i in range(160):
                a = R2.uniform(0, 6.28) - t * 1.2
                r = rr + R2.uniform(-30, 30) * q
                c.drawCircle(cx + math.cos(a) * r, cy + math.sin(a) * r * 0.36, R2.uniform(2, 7), fill(with_alpha(0xFFE8D0C0, 0.9)))
        hc.big(c, "3.600", W / 2, 1640, 130, V["accent"], lt, 0.6)
        K.tag(c, W / 2, 1760, "MILLONES DE AÑOS", lt - 1.0, accent=WHITE, size=40)
    else:
        neptune(c, W * 0.22, 640, 170, t)
        triton(c, W / 2 + 40, 1120, 360, t)


V805 = dict(slug="805_triton_luna_al_reves", accent=0xFFFF9A7A, drone=0.03, scene=s_triton, tease="LO PROMETIDO", mood="epico",
            send="ENVÍASELO A QUIEN LE GUSTE EL ESPACIO", rehook=("s4", "Y AHORA LO PEOR"), reveal=("s4", "SU FINAL"), segs=[
    dict(id="h", who="nar", say="Esta luna gira al revés que su planeta. Y eso la va a destruir.",
         cap="Esta luna gira | *AL REVÉS*… | y eso la va a *destruir*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Es Tritón, la luna más grande de Neptuno. Y es la única luna grande que va en sentido contrario.",
         cap="Es *Tritón*, de Neptuno: | la única luna grande | que va *al revés*"),
    dict(id="s2", who="nar", cut=True, say="Por eso se cree que Neptuno la capturó.",
         cap="Se cree que Neptuno | la *CAPTURÓ*", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="En mil novecientos ochenta y nueve, la Voyager 2 vio géiseres de nitrógeno de ocho kilómetros, a doscientos treinta y cinco bajo cero.",
         cap="*Voyager 2*, 1989: | géiseres de *nitrógeno* | de *8 km*, a −235 °C"),
    dict(id="s4", who="nar", cut=True, say="Y como va al revés, se acerca a Neptuno. En unos tres mil seiscientos millones de años, se romperá en pedazos.",
         cap="Cada vez más *cerca*… | en ≈ *3.600 millones* de años | se *ROMPERÁ*", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="¿Te lo esperabas? Comenta sí o no. Y sígueme: la próxima luna tiene un acantilado gigante.",
         cap="¿Te lo esperabas? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])

VIDEOS = [V802, V803, V804, V805]


def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
    return scene


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = "auto" if len(sys.argv) > 2 else None
    for i in idxs:
        K.run(VIDEOS[i], make_scene(VIDEOS[i]), OUT, preview=pv)
