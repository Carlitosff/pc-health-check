"""33 · Todos los planetas caben entre la Tierra y la Luna (en el apogeo)."""
import math, sys
import numpy as np
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import spheres as S
import core as K
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, pill

V = dict(slug="33_planetas", accent=0xFFFFC857, drone=0.02, segs=[
    dict(id="h", who="nar", say="Todos los planetas del sistema solar caben entre la Tierra y la Luna.",
         cap="*TODOS* los planetas… | caben entre la *Tierra* | y la *Luna*"),
    dict(id="s1", who="nar", cut=True,
         say="Cuando la Luna está en su punto más lejano, el hueco entre las dos mide unos trescientos noventa y siete mil kilómetros.",
         cap="Con la Luna en su punto | más *lejano*… | hueco: *≈ 397.000 km*"),
    dict(id="q", who="q", say="¿Caben todos los planetas? ¿Sí… o no?", cap="¿Caben *TODOS*? | ¿Sí… o *no*?",
         quiz=dict(a="SÍ, CABEN", b="NO CABEN", ans="a")),
    dict(id="r", who="nar", cut=True,
         say="¡Caben! Mercurio, Venus, Marte, Júpiter, Saturno, Urano y Neptuno suman unos trescientos ochenta mil kilómetros.",
         cap="¡*CABEN*! | todos juntos: | *≈ 380.000 km*"),
    dict(id="s2", who="nar", say="Y todavía sobran unos diecisiete mil.", cap="Y aún sobran | *≈ 17.000 km*"),
    dict(id="s3", who="nar", say="Júpiter y Saturno, ellos solos, ocupan dos tercios del hueco.",
         cap="*Júpiter* y *Saturno*: | dos tercios | del hueco"),
    dict(id="s4", who="nar", say="Ojo: con la Luna a su distancia media, se quedarían cortos por muy poco.",
         cap="Ojo: a distancia *media*… | se quedan *cortos* | por muy poco"),
    dict(id="s5", who="nar", say="Y la Tierra, a esta escala… es apenas este puntito.",
         cap="Y la Tierra, a esta escala… | es este *puntito*"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo esperabas? ¡Comenta y sígueme para más!",
         cap="¿Te lo esperabas? | *COMENTA* | y *SÍGUEME*"),
])

STARS = K.Stars(seed=33)
EARTH = (S.load("earth_atmos_2048.jpg"), S.load("earth_clouds_1024.png", "A"), S.load("earth_specular_2048.jpg", "L"))
MOON = S.load("moon_1024.jpg")
PL = [  # nombre, textura, diámetro km
    ("MERCURIO", "mercurymap.jpg", 4879), ("VENUS", "venusmap.jpg", 12104), ("MARTE", "marsmap1k.jpg", 6779),
    ("JÚPITER", "jupitermap.jpg", 139820), ("SATURNO", "saturnmap.jpg", 116460), ("URANO", "uranusmap.jpg", 50724),
    ("NEPTUNO", "neptunemap.jpg", 49244)]
TEXS = {n: S.load(f) for n, f, _ in PL}
RING = np.asarray(__import__("PIL.Image", fromlist=["Image"]).open(S.TEX + "saturnringcolor.jpg").convert("RGB"))
GAP = 397588.0
Y_EARTH = 1730.0  # superficie de la Tierra
Y_MOON = 640.0    # superficie de la Luna
SC = (Y_EARTH - Y_MOON) / GAP
LIGHT = (-0.7, 0.3, 0.65)


def planet_img(name, R, t):
    return S.render(2 * R, TEXS[name], spin=t * 0.3, light=LIGHT, ambient=0.08, gain=1.1, limb=0.25)


def saturn_ring(c, x, y, Rs, front, alpha=1.0):
    rin, rout = Rs * 1.24, Rs * 2.27
    k = 0.28
    n = 40
    c.save()
    if front:
        c.clipRect(skia.Rect.MakeLTRB(x - rout - 5, y, x + rout + 5, y + rout))
    else:
        c.clipRect(skia.Rect.MakeLTRB(x - rout - 5, y - rout, x + rout + 5, y))
    for i in range(n):
        f = i / (n - 1)
        r = lerp(rin, rout, f)
        px = RING[RING.shape[0] // 2, int(f * (RING.shape[1] - 1))]
        col = (int(255 * alpha * 0.85) << 24) | (int(px[0]) << 16) | (int(px[1]) << 8) | int(px[2])
        c.drawOval(skia.Rect.MakeXYWH(x - r, y - r * k, 2 * r, 2 * r * k),
                   stroke(col, (rout - rin) / n * 1.3))
    c.restore()


def layout(t, P):
    """Posición vertical (centro) de cada planeta apilado."""
    y = Y_EARTH
    out = []
    for name, _, d in PL:
        r = d / 2 * SC
        out.append((name, y - r, r))
        y -= d * SC
    return out, y  # y = tope de la pila


def scene(c, t, P):
    tl = P["tl"]
    c.clear(0xFF02030A)
    sg = K.seg_at(P, t)
    sid = sg["id"]
    lt = t - sg["a"]
    acc = V["accent"]
    STARS.draw(c, t, camy=-t * 8, alpha=0.9)
    # cámara: gancho empieza cerca de la Tierra y se aleja
    zp = ease_in_out(prog(t, 0, 2.6))
    zoom = lerp(2.4, 1.0, zp)
    fy = lerp(Y_EARTH - 120, H / 2 + 120, zp)
    c.save()
    c.translate(W / 2, H / 2 + 120)
    c.scale(zoom, zoom)
    c.translate(-W / 2, -fy)
    cx = W / 2
    # Tierra y Luna (tamaño real a escala)
    er = 6371 * SC
    ed, ecl, esp = EARTH
    K.glow(c, cx, Y_EARTH + er, 90, 0xFF5AA8FF, 0.5)
    img = S.render(64, ed, spin=t * 0.4, light=LIGHT, clouds=ecl, spec=esp, gain=1.2)
    S.draw_planet(c, cx, Y_EARTH + er, er, img)
    mr = 1737 * SC
    K.glow(c, cx, Y_MOON - mr, 60, 0xFFD8D8E0, 0.45)
    S.draw_planet(c, cx, Y_MOON - mr, mr, S.render(32, MOON, light=LIGHT, gain=1.2))
    # qué planetas se ven
    stack, top = layout(t, P)
    show = 1.0
    drop_start = None
    if sid in ("s1", "q", "q_count"):
        show = 1 - ease_in_out(prog(t - tl["s1"][0], 0, 0.6))
    if sid in ("r", "s2", "s3", "s4", "s5", "cta"):
        drop_start = tl["r"][0] + 1.6
    for i, (name, y, r) in enumerate(stack):
        a = show
        yy = y
        if drop_start is not None:
            pi = prog(t, drop_start + i * 0.32, drop_start + i * 0.32 + 0.45)
            a = 1.0 if pi > 0 else 0.0
            yy = lerp(-400, y, ease_out(pi))
        if a <= 0.01:
            continue
        dim = 1.0
        if sid == "s3" and name not in ("JÚPITER", "SATURNO"):
            dim = 1 - 0.65 * prog(lt, 0, 0.5)
        if name == "SATURNO":
            saturn_ring(c, cx, yy, r, front=False, alpha=a * dim)
        im = planet_img(name, max(r, 4), t)
        p = skia.Paint(Alphaf=a * dim, AntiAlias=True)
        c.drawImageRect(im, skia.Rect.MakeXYWH(cx - r, yy - r, 2 * r, 2 * r), skia.SamplingOptions(skia.FilterMode.kLinear), p)
        if name == "SATURNO":
            saturn_ring(c, cx, yy, r, front=True, alpha=a * dim)
        if zp >= 1 and a > 0.5:
            side = 1 if i % 2 == 0 else -1
            lx = cx + side * (max(r, 30) + 150)
            yy_l = yy + {"MERCURIO": 30, "VENUS": 0, "MARTE": -34}.get(name, 0)
            if name == "SATURNO":
                lx = cx + side * (r * 2.27 + 110)
            pill(c, lx, yy_l, name, 26, bg=WHITE, fg=INK, scale=ease_back(prog(t - (drop_start or 0) - i * 0.32, 0.3, 0.6)) if drop_start else 1.0)
            c.drawLine(lx - side * 70, yy_l, cx + side * r, yy, stroke(with_alpha(WHITE, 0.45), 2))
    # etiquetas Tierra/Luna
    if zp >= 1:
        pill(c, cx, Y_EARTH + er + 62, "TIERRA", 28, bg=0xFF5AA8FF, fg=INK)
        pill(c, cx - 150, Y_MOON - mr, "LUNA", 28, bg=0xFFD8D8E0, fg=INK)
    # medidas
    if sid in ("s1", "q", "q_count"):
        p = ease_out(prog(t - tl["s1"][0], 0.5, 1.6))
        x0 = cx + 300
        c.drawLine(x0, Y_EARTH, x0, lerp(Y_EARTH, Y_MOON, p), stroke(acc, 6))
        c.drawLine(x0 - 25, Y_EARTH, x0 + 25, Y_EARTH, stroke(acc, 6))
        if p >= 1:
            c.drawLine(x0 - 25, Y_MOON, x0 + 25, Y_MOON, stroke(acc, 6))
            c.save(); c.translate(x0 + 10, (Y_EARTH + Y_MOON) / 2); c.rotate(-90)
            pill(c, 0, 0, "≈ 397.000 km", 40, bg=acc, fg=INK, scale=ease_back(prog(t - tl["s1"][0], 1.6, 2.0)))
            c.restore()
    if sid == "s2":
        p = ease_out(prog(lt, 0.2, 0.8))
        c.drawRect(skia.Rect.MakeLTRB(cx - 260, Y_MOON, cx + 260, top), fill(with_alpha(acc, 0.25 * p)))
        c.drawRect(skia.Rect.MakeLTRB(cx - 260, Y_MOON, cx + 260, top), stroke(with_alpha(acc, p), 4))
        pill(c, cx + 360, (Y_MOON + top) / 2, "≈ 17.000 km LIBRES", 34, bg=acc, fg=INK, scale=ease_back(prog(lt, 0.5, 0.9)))
    if sid == "s3":
        ys = [y for (n, y, r) in stack if n in ("JÚPITER", "SATURNO")]
        rs = [r for (n, y, r) in stack if n in ("JÚPITER", "SATURNO")]
        y_lo, y_hi = ys[0] + rs[0], ys[1] - rs[1]
        x0 = cx - 330
        p = ease_out(prog(lt, 0.3, 1.0))
        c.drawLine(x0, y_lo, x0, lerp(y_lo, y_hi, p), stroke(acc, 6))
        if p >= 1:
            c.drawLine(x0 - 20, y_lo, x0 + 20, y_lo, stroke(acc, 6)); c.drawLine(x0 - 20, y_hi, x0 + 20, y_hi, stroke(acc, 6))
    if sid == "s5":
        ring = (t * 1.2) % 1
        c.drawCircle(cx, Y_EARTH + er, er + 6 + ring * 60, stroke(with_alpha(0xFF5AA8FF, 1 - ring), 5))
        c.drawCircle(cx, Y_EARTH + er, er + 10, stroke(0xFF5AA8FF, 4))
    c.restore()
    if sid == "s4":
        K.tag(c, W / 2, 1560, "DISTANCIA MEDIA: NO CABEN POR ≈ 4.000 km", lt - 0.3, accent=acc, size=34)
    if sid == "r":
        K.counter(c, t, lt - 1.7, lambda p: K.fmt(380000 * p) + " km", "LOS 7 PLANETAS EN FILA", acc, y=1560, size=110)
    if sid == "s3":
        K.counter(c, t, lt - 0.3, lambda p: K.fmt(67 * p) + " %", "JÚPITER + SATURNO", acc, y=1560, size=110)


if __name__ == "__main__":
    K.run(V, scene, "/home/claude/tiktok/out35", preview="auto" if len(sys.argv) > 1 else None)
