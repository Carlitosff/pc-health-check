"""32 · Toda el agua de la Tierra cabe en esta bola."""
import math, sys
import numpy as np
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import spheres as S
import core as K
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, pill

V = dict(slug="32_agua", accent=0xFF5AC8FF, drone=0.018, segs=[
    dict(id="h", who="nar", say="Toda el agua de la Tierra cabe en esta bola.",
         cap="*TODA* el agua de la Tierra… | cabe en *esta bola*"),
    dict(id="s1", who="nar", cut=True,
         say="Océanos, hielo, ríos, nubes… todo junto formaría una esfera de unos mil trescientos ochenta y cinco kilómetros.",
         cap="Océanos, hielo, nubes… | una bola de | *1.385 km*"),
    dict(id="s2", who="nar", say="Es más pequeña que la Luna.", cap="Más pequeña | que la *LUNA*"),
    dict(id="q", who="q", say="¿Y el agua de todos los ríos y lagos? ¿Una bola de quinientos kilómetros… o de cincuenta?",
         cap="¿Y la de *ríos* y *lagos*? | ¿*500 km* o *50 km*?", quiz=dict(a="≈ 500 KM", b="≈ 50 KM", ans="b")),
    dict(id="r", who="nar", cut=True,
         say="De unos cincuenta y seis kilómetros. Esa bolita es toda el agua de los ríos y lagos del planeta.",
         cap="Solo *56 km*… | toda el agua de | *ríos* y *lagos*"),
    dict(id="s3", who="nar", say="Si sumas el agua dulce subterránea, llega a unos doscientos setenta y tres.",
         cap="Con la *subterránea*: | *273 km*"),
    dict(id="s4", who="nar", say="Así que la próxima vez que dejes el grifo abierto… piensa en esta bolita.",
         cap="La próxima vez… | piensa en | *esta bolita*"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo esperabas? ¡Comenta y sígueme para más!",
         cap="¿Te lo esperabas? | *COMENTA* | y *SÍGUEME*"),
])

DAY = S.load("earth_atmos_2048.jpg")
NIGHT = S.load("earth_lights_2048.png")
SPEC = S.load("earth_specular_2048.jpg", "L")
CLOUDS = S.load("earth_clouds_1024.png", "A")
MOON = S.load("moon_1024.jpg")
STARS = K.Stars(seed=32)
RE = 6371.0
SPOT = (42.0, -98.0)  # sobre Norteamérica, como la imagen del USGS
LIGHT = (-0.55, 0.35, 0.75)


def earth(c, x, y, R, spin, lat0=0.5):
    img = S.render(2 * R, DAY, spin=spin, tilt=0.0, light=LIGHT, night=NIGHT, spec=SPEC, clouds=CLOUDS,
                   cloud_spin=0.0, lat0=lat0, gain=1.12)
    S.draw_planet(c, x, y, R, img)
    S.atmosphere(c, x, y, R)


def water_ball(c, x, y, r, t, alpha=1.0):
    if r < 0.5:
        return
    # sombra
    sh = skia.GradientShader.MakeRadial((x + r * 0.2, y + r * 1.1), r * 1.1, [with_alpha(0xFF000000, 0.35 * alpha), 0x00000000])
    c.drawOval(skia.Rect.MakeXYWH(x - r * 0.9, y + r * 0.8, r * 2.2, r * 0.6), skia.Paint(Shader=sh))
    g = skia.GradientShader.MakeRadial((x - r * 0.35, y - r * 0.4), r * 1.5,
                                       [with_alpha(0xFF7FD8FF, alpha), with_alpha(0xFF1F78D0, alpha),
                                        with_alpha(0xFF0A2E70, alpha)], [0, 0.45, 1])
    c.drawCircle(x, y, r, skia.Paint(Shader=g, AntiAlias=True))
    # ondas internas
    c.save()
    c.clipPath(skia.Path().addCircle(x, y, r))
    for k in range(3):
        yy = y + r * (0.2 + 0.25 * k) + math.sin(t * 2 + k) * r * 0.05
        c.drawOval(skia.Rect.MakeXYWH(x - r * 1.2, yy - r * 0.1, r * 2.4, r * 0.25),
                   stroke(with_alpha(0xFFBFEFFF, 0.12 * alpha), max(1, r * 0.04)))
    c.restore()
    c.drawCircle(x, y, r, stroke(with_alpha(0xFFBFEFFF, 0.5 * alpha), max(1, r * 0.03)))
    c.drawOval(skia.Rect.MakeXYWH(x - r * 0.55, y - r * 0.7, r * 0.5, r * 0.3), fill(with_alpha(WHITE, 0.55 * alpha)))


def moon(c, x, y, R):
    img = S.render(2 * R, MOON, spin=0.3, light=LIGHT, ambient=0.04, gain=1.1)
    S.draw_planet(c, x, y, R, img)


def magnifier(c, t, lt, mx, my, Rm, src, items, zoom_lbl):
    """Lupa: círculo con fondo de océano/tierra y bolas ampliadas. items: [(r_px, dx, label)]."""
    s = ease_back(prog(lt, 0, 0.45), 1.8)
    if s <= 0:
        return
    R = Rm * s
    c.drawLine(src[0], src[1], mx, my, stroke(with_alpha(WHITE, 0.7), 3))
    c.drawCircle(src[0], src[1], 10, stroke(WHITE, 3))
    c.save()
    c.clipPath(skia.Path().addCircle(mx, my, R))
    g = skia.GradientShader.MakeLinear([(mx, my - R), (mx, my + R)], [0xFF2E5A2A, 0xFF5E7A3A, 0xFF8A7A50])
    c.drawCircle(mx, my, R, skia.Paint(Shader=g))
    for (r, dx, label) in items:
        water_ball(c, mx + dx * s, my + 20 * s, r * s, t)
    c.restore()
    c.drawCircle(mx, my, R, stroke(WHITE, 8))
    c.drawCircle(mx, my, R + 8, stroke(with_alpha(0xFF000000, 0.4), 6))
    pill(c, mx + R * 0.72, my - R * 0.82, zoom_lbl, 30, bg=WHITE, fg=INK, scale=s)
    for (r, dx, label) in items:
        if label:
            K.tag(c, mx + dx * s, my + 20 * s + r * s + 40, label, lt - 0.4, accent=V["accent"], size=30)


def scene(c, t, P):
    tl = P["tl"]
    c.clear(0xFF02030A)
    sg = K.seg_at(P, t)
    sid = sg["id"]
    lt = t - sg["a"]
    STARS.draw(c, t, camx=t * 12, zoom=1.0, alpha=0.9)
    spin = math.radians(SPOT[1]) + 0.25 + t * 0.012
    lat0 = 0.55
    # cámara: gancho cerca, luego se aleja
    ph = ease_in_out(prog(t, 0.2, 3.2))
    R = lerp(820, 360, ph)
    ex, ey = W / 2, lerp(1250, 1080, ph)
    if sid in ("s2",):
        p2 = ease_in_out(prog(lt, 0, 0.9))
        ex = lerp(W / 2, 420, p2)
    elif sid in ("q", "q_count", "r", "s3", "s4"):
        ex = 420
    if sid == "cta":
        ex, ey, R = W / 2, 900, 330
    earth(c, ex, ey, R, spin, lat0)
    x, y, z = S.project(SPOT[0], SPOT[1], spin=spin, tilt=0.0, lat0=lat0)
    bx, by = ex + x * R, ey + y * R - R * 0.18
    rw = R * 1385 / 2 / RE
    if sid != "cta":
        water_ball(c, bx, by, rw * ease_back(prog(t, 0.0, 0.5), 1.6) if t < 0.5 else rw, t)
    if sid in ("h", "s1"):
        K.tag(c, bx + 190, by - 170, "TODA EL AGUA", t - 1.0, accent=V["accent"], line_to=(bx + rw * 0.6, by - rw * 0.6))
    if sid == "s1":
        K.counter(c, t, lt - 0.6, lambda p: K.fmt(1385 * p) + " km", "DE DIÁMETRO", V["accent"], y=1560)
    if sid == "s2":
        mR = R * 1737 / RE
        ms = ease_back(prog(lt, 0.3, 0.9), 1.6)
        mx, my = 860, 760
        moon(c, mx, my, mR * ms)
        K.tag(c, mx, my + mR + 60, "LUNA · 3.474 km", lt - 0.8, accent=WHITE, size=32)
        K.tag(c, bx, by + rw + 50, "AGUA · 1.385 km", lt - 0.9, accent=V["accent"], size=32)
    if sid in ("r", "s3", "s4"):
        ar = tl["r"][0]
        z1 = 8.0  # aumento de la lupa
        fresh = R * 273 / 2 / RE * z1
        lakes = R * 56 / 2 / RE * z1
        if sid == "r":
            items = [(lakes, 0, "56 km")]
            lbl = "×8"
        elif sid == "s3":
            items = [(fresh, -70, "273 km"), (lakes, 130, "56 km")]
            lbl = "×8"
        else:
            items = [(lakes * 3, 0, "56 km")]
            lbl = "×24"
        magnifier(c, t, t - ar - 1.6 if sid == "r" else 1.0, 760, 1180 if sid != "s4" else 1180, 230,
                  (bx + rw * 1.4, by + rw * 0.5), items, lbl)
    if sid == "cta":
        water_ball(c, W / 2 + 120, 900 - 260, 330 * 1385 / 2 / RE, t)


if __name__ == "__main__":
    K.run(V, scene, "/home/claude/tiktok/out35", preview="auto" if len(sys.argv) > 1 else None)
