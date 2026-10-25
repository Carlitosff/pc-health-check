"""35 · El monte Olimpo de Marte."""
import math, random, sys
import numpy as np
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import spheres as S
import core as K
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, pill

V = dict(slug="35_olimpo", accent=0xFFFF8A4C, drone=0.022, segs=[
    dict(id="h", who="nar", say="Esta montaña es más del doble de alta que el Everest.",
         cap="Esta montaña es | *más del doble* | de alta que el *Everest*"),
    dict(id="s1", who="nar", cut=True, say="Es el monte Olimpo, en Marte: un volcán de más de veintiún kilómetros de altura.",
         cap="Monte *Olimpo*, Marte: | más de *21 km*"),
    dict(id="s2", who="nar", say="El Everest mide ocho mil ochocientos cuarenta y nueve metros. A su lado, parece una colina.",
         cap="Everest: *8.849 m*… | a su lado, | una *colina*"),
    dict(id="s3", who="nar", cut=True, say="Y su base mide unos seiscientos kilómetros. Más que de Madrid a Barcelona.",
         cap="Base: *≈ 600 km*… | más que | *Madrid–Barcelona*"),
    dict(id="q", who="q", say="Si estuvieras en la cima… ¿te darías cuenta de que estás en una montaña?",
         cap="Desde la cima… | ¿notarías que estás | en una *montaña*?", quiz=dict(a="SÍ", b="NO", ans="b")),
    dict(id="r", who="nar", cut=True,
         say="No. Sus laderas son tan suaves y tan largas que se pierden tras el horizonte.",
         cap="*NO*: sus laderas | son tan suaves… | que se pierden tras el *horizonte*"),
    dict(id="s4", who="nar",
         say="Creció tanto porque en Marte no hay placas que se muevan: la lava salió en el mismo sitio durante millones de años.",
         cap="Sin placas que se muevan… | la lava salió en el | *mismo sitio*"),
    dict(id="cta", who="nar", cut=True, say="¿Subirías? ¡Comenta y sígueme para más!",
         cap="¿Subirías? | *COMENTA* | y *SÍGUEME*"),
])

ACC = V["accent"]
MARS = S.load("marsmap1k.jpg")
STARS = K.Stars(seed=35)
OLY = (18.65, 226.2 - 180.0)  # la textura tiene 0° en el borde izquierdo
LIGHT = (-0.6, 0.3, 0.74)
_marsimg = skia.Image.open(S.TEX + "marsmap1k.jpg")


def mars(c, x, y, R, spin, lat0=0.25):
    img = S.render(2 * R, MARS, spin=spin, light=LIGHT, ambient=0.05, gain=1.15, limb=0.2, lat0=lat0)
    S.draw_planet(c, x, y, R, img)
    S.atmosphere(c, x, y, R, color=0xFFFF9A6A, strength=0.55)


def mars_fill(x0, y0, scale=1.6):
    m = skia.Matrix.Scale(scale, scale)
    m.postTranslate(x0, y0)
    return _marsimg.makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, skia.SamplingOptions(skia.FilterMode.kLinear), m)


def shield(cx, base_y, half_w, h):
    """Perfil de volcán en escudo con caldera."""
    p = skia.Path()
    p.moveTo(cx - half_w, base_y)
    n = 40
    for i in range(n + 1):
        f = i / n * 2 - 1
        prof = (1 - abs(f) ** 1.6)
        y = base_y - h * prof
        if abs(f) < 0.07:
            y += h * 0.04
        p.lineTo(cx + f * half_w, y)
    p.lineTo(cx + half_w, base_y)
    p.close()
    return p


def jagged(cx, base_y, half_w, h, seed=3):
    rnd = random.Random(seed)
    p = skia.Path()
    p.moveTo(cx - half_w, base_y)
    n = 18
    for i in range(1, n):
        f = i / n
        prof = 1 - abs(f - 0.5) / 0.5
        p.lineTo(cx - half_w + 2 * half_w * f, base_y - h * prof ** 1.2 + rnd.uniform(-1, 1) * h * 0.05 * (1 - prof))
    p.lineTo(cx + half_w, base_y)
    p.close()
    return p


def sky(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, 0), (0, H)], [0xFF1A0E10, 0xFF6A3A2A, 0xFFC8835A], [0, 0.6, 1])))
    STARS.draw(c, t, alpha=0.25, band=False)


def ground(c, y0, t):
    c.drawRect(skia.Rect.MakeLTRB(0, y0, W, H), skia.Paint(Shader=mars_fill(-t * 20 - 400, y0 - 600, 3.0)))
    c.drawRect(skia.Rect.MakeLTRB(0, y0, W, H), fill(0x44000000))


def scene(c, t, P):
    tl = P["tl"]
    sg = K.seg_at(P, t)
    sid = sg["id"]
    lt = t - sg["a"]
    c.clear(0xFF02030A)
    if sid in ("h", "s4", "cta"):
        STARS.draw(c, t, camx=t * 10)
        if sid == "h":
            p = ease_in_out(prog(t, 0, 3.0))
            R = lerp(380, 560, p)
            spin = math.radians(OLY[1]) - lerp(1.2, 0.0, p)
            cy = 1080
        else:
            R, spin, cy = (520, math.radians(OLY[1]) + 0.05 * lt, 1080) if sid == "s4" else (380, t * 0.15, 900)
        mars(c, W / 2, cy, R, spin, lat0=0.3)
        x, y, z = S.project(OLY[0], OLY[1], spin=spin, lat0=0.3)
        if z > 0.1 and sid != "cta":
            px, py = W / 2 + x * R, cy + y * R
            if sid == "s4":
                K.glow(c, px, py, 160, 0xFFFF5A1E, 0.55 + 0.25 * math.sin(t * 4))
                K.glow(c, px, py, 60, 0xFFFFD27A, 0.6)
            ring = (t * 1.1) % 1
            c.drawCircle(px, py, 18 + ring * 60, stroke(with_alpha(ACC, 1 - ring), 5))
            c.drawCircle(px, py, 12, stroke(WHITE, 4))
            K.tag(c, px + 170, py - 200, "MONTE OLIMPO", (t - 1.0) if sid == "h" else lt, accent=ACC, line_to=(px, py))
        return
    if sid in ("s1", "s2"):
        sky(c, t)
        base = 1500
        k = 40  # px por km
        a1 = tl["s1"][0]
        l1 = t - a1
        h = 21.3 * k * ease_out(prog(l1, 0.1, 1.6))
        ground(c, base, t)
        pth = shield(560, base + 4, 470, h)
        c.drawPath(pth, skia.Paint(Shader=mars_fill(-600, 350, 3.0), AntiAlias=True))
        c.drawPath(pth, skia.Paint(Shader=skia.GradientShader.MakeLinear([(90, 0), (1030, 0)],
                                                                         [0x22FFFFFF, 0x00000000, 0x66000000]), AntiAlias=True))
        c.drawPath(pth, stroke(with_alpha(0xFFFFC9A0, 0.6), 3))
        if sid == "s1":
            K.counter(c, t, l1 - 0.1, lambda p: K.fmt(21.3 * p, 1) + " km", "MONTE OLIMPO", ACC, y=1640, size=110, dur=1.5)
        if sid == "s2":
            eh = 8.849 * k * ease_out(prog(lt, 0.2, 1.0))
            ev = jagged(930, base + 4, 110, eh)
            c.drawPath(ev, skia.Paint(Shader=skia.GradientShader.MakeLinear([(930, base - eh), (930, base)],
                                                                            [0xFFE8EEF8, 0xFF7A808C, 0xFF3A3E46]), AntiAlias=True))
            c.drawPath(ev, stroke(with_alpha(WHITE, 0.6), 2))
            K.tag(c, 930, base - eh - 60, "EVEREST · 8.849 m", lt - 0.8, accent=WHITE, size=30)
            K.tag(c, 560, base - 21.3 * k - 60, "OLIMPO · 21,3 km", lt - 0.5, accent=ACC, size=30)
            pill(c, W / 2, base + 120, "ALTURAS A ESCALA", 28, bg=0xCC000000, fg=WHITE)
        return
    # s3, q, r: perfil real (casi plano) + horizonte
    sky(c, t)
    if sid in ("s3", "q", "q_count"):
        a3 = tl["s3"][0]
        l3 = t - a3
        base = 1250
        ground(c, base, t)
        k = 1000 / 600.0  # px por km
        hreal = 21.3 * k * 1.0
        pth = shield(W / 2, base + 2, 500, hreal * ease_out(prog(l3, 0, 0.8)))
        c.drawPath(pth, skia.Paint(Shader=mars_fill(-600, 500, 3.0), AntiAlias=True))
        c.drawPath(pth, stroke(0xFFFFC9A0, 3))
        p = ease_out(prog(l3, 0.4, 1.3))
        y0 = base + 70
        c.drawLine(40, y0, lerp(40, 1040, p), y0, stroke(ACC, 6))
        c.drawLine(40, y0 - 20, 40, y0 + 20, stroke(ACC, 6))
        if p >= 1:
            c.drawLine(1040, y0 - 20, 1040, y0 + 20, stroke(ACC, 6))
            pill(c, W / 2, y0 + 55, "≈ 600 km", 40, bg=ACC, fg=INK, scale=ease_back(prog(l3, 1.3, 1.6)))
        p2 = ease_out(prog(l3, 1.8, 2.8))
        y1 = y0 + 160
        mb = 505 * k
        c.drawLine(40, y1, 40 + mb * p2, y1, stroke(WHITE, 5))
        c.drawCircle(40, y1, 10, fill(WHITE))
        if p2 >= 1:
            c.drawCircle(40 + mb, y1, 10, fill(WHITE))
            pill(c, 40 + mb / 2, y1 + 50, "MADRID → BARCELONA ≈ 505 km", 30, bg=WHITE, fg=INK, scale=ease_back(prog(l3, 2.8, 3.1)))
        pill(c, W / 2, base - 120, "PERFIL REAL, SIN EXAGERAR", 28, bg=0xCC000000, fg=WHITE, scale=ease_back(prog(l3, 0.8, 1.1)))
        return
    # r: el horizonte esconde la base
    ar = tl["r"][0]
    l = t - ar
    Rm = 2600.0
    cx, cy = W / 2, 1150 + Rm
    c.save()
    zoom = lerp(1.0, 1.15, prog(l, 0, 4))
    c.translate(W / 2, 1150)
    c.scale(zoom, zoom)
    c.translate(-W / 2, -1150)
    arc = skia.Path()
    arc.addCircle(cx, cy, Rm)
    c.drawPath(arc, skia.Paint(Shader=mars_fill(0, 0, 2.0), AntiAlias=True))
    c.drawPath(arc, fill(0x33000000))
    bump = shield(cx, cy - Rm + 3, 420, 90)
    c.drawPath(bump, skia.Paint(Shader=mars_fill(0, 0, 1.3), AntiAlias=True))
    c.drawPath(bump, stroke(0xFFFFC9A0, 3))
    top_y = cy - Rm - 85
    # astronauta
    c.drawCircle(cx, top_y - 30, 12, fill(WHITE))
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - 10, top_y - 18, 20, 22), 6, 6, fill(WHITE))
    # línea de visión hasta el horizonte (tangente a la ladera)
    p = ease_out(prog(l, 1.8, 2.8))
    for sgn in (-1, 1):
        hx, hy = cx + sgn * 330, cy - Rm + 8
        c.drawLine(cx, top_y - 30, lerp(cx, hx + sgn * 260, p), lerp(top_y - 30, hy + 30, p),
                   stroke(with_alpha(ACC, 0.9), 4))
    if p >= 1:
        K.tag(c, cx, top_y - 130, "TODO PARECE LLANO", l - 2.8, accent=ACC, size=34)
        pill(c, cx + 300, cy - Rm + 120, "LA BASE QUEDA FUERA DE LA VISTA", 26, bg=WHITE, fg=INK,
             scale=ease_back(prog(l, 3.0, 3.3)))
    c.restore()


if __name__ == "__main__":
    K.run(V, scene, "/home/claude/tiktok/out35", preview="auto" if len(sys.argv) > 1 else None)
