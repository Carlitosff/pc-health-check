"""31 · Ahora mismo vas a más de 100.000 km/h."""
import math, random, sys
import numpy as np
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import spheres as S
import core as K
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, smooth, with_alpha, fill, stroke, pill

V = dict(slug="31_velocidad", accent=0xFF6FE3FF, drone=0.02, segs=[
    dict(id="h", who="nar", say="Ahora mismo vas a más de cien mil kilómetros por hora… y ni te enteras.",
         cap="Ahora mismo vas a | *+100.000 km/h*… | y ni te *enteras*"),
    dict(id="s1", who="nar", cut=True,
         say="Primero, la Tierra gira. En España, el suelo bajo tus pies va a unos mil trescientos kilómetros por hora.",
         cap="La Tierra *gira*: | en España vas a | *1.300 km/h*"),
    dict(id="s2", who="nar", cut=True,
         say="Pero eso no es nada. La Tierra da vueltas alrededor del Sol a unos ciento siete mil kilómetros por hora.",
         cap="Pero eso no es nada… | alrededor del *Sol*: | *107.000 km/h*"),
    dict(id="q", who="q", say="¿Y el Sol? ¿Está quieto… o se mueve?", cap="¿Y el *Sol*? | ¿Quieto… o se *mueve*?",
         quiz=dict(a="QUIETO", b="SE MUEVE", ans="b")),
    dict(id="r", who="nar", cut=True,
         say="¡Se mueve! Arrastra a todo el sistema solar alrededor de la galaxia a unos ochocientos mil kilómetros por hora.",
         cap="¡Se *MUEVE*! | alrededor de la galaxia: | *800.000 km/h*"),
    dict(id="s3", who="nar", say="Y aun así, tarda unos doscientos treinta millones de años en dar una sola vuelta.",
         cap="Y aun así… | una vuelta: | *230 millones* de años"),
    dict(id="s4", who="nar", say="La última vez que pasamos por aquí… los dinosaurios acababan de aparecer.",
         cap="La última vez que pasamos por aquí… | los *dinosaurios* | acababan de aparecer"),
    dict(id="cta", who="nar", cut=True, say="¿Lo sabías? ¡Comenta y sígueme para más!",
         cap="¿Lo sabías? | *COMENTA* | y *SÍGUEME*"),
])

DAY = S.load("earth_atmos_2048.jpg")
NIGHT = S.load("earth_lights_2048.png")
SPEC = S.load("earth_specular_2048.jpg", "L")
CLOUDS = S.load("earth_clouds_1024.png", "A")
SUN = S.load("sunmap.jpg")
STARS = K.Stars(seed=31)
SPAIN = (40.4, -3.7)

# galaxia: partículas en brazos espirales
_rnd = np.random.default_rng(7)
N = 9000
arm = _rnd.integers(0, 4, N)
rr = _rnd.power(0.6, N) * 1.0
th = arm * (np.pi / 2) + np.log(rr + 0.05) * 2.6 + _rnd.normal(0, 0.28, N) * (1.1 - rr)
GX = rr * np.cos(th) + _rnd.normal(0, 0.03, N)
GY = rr * np.sin(th) + _rnd.normal(0, 0.03, N)
bulge = _rnd.normal(0, 0.12, (2500, 2))
GX = np.concatenate([GX, bulge[:, 0]])
GY = np.concatenate([GY, bulge[:, 1]])
GR = np.sqrt(GX ** 2 + GY ** 2)
GB = np.clip(1.2 - GR, 0.25, 1.0) * _rnd.uniform(0.4, 1.0, len(GX))
SUN_R, SUN_A0 = 0.55, 2.2


def earth(c, x, y, R, spin, lat0=0.35, tilt=0.41, light=(-0.65, 0.3, 0.7)):
    img = S.render(2 * R, DAY, spin=spin, tilt=tilt, light=light, night=NIGHT, spec=SPEC, clouds=CLOUDS,
                   cloud_spin=spin * 0.1, lat0=lat0, gain=1.12)
    S.draw_planet(c, x, y, R, img)
    S.atmosphere(c, x, y, R, strength=1.0)


def sun(c, x, y, R, t, a=1.0):
    K.glow(c, x, y, R * 6, 0xFFFF7A1E, 0.30 * a)
    K.glow(c, x, y, R * 2.4, 0xFFFFA040, 0.45 * a)
    img = S.render(2 * R, SUN, spin=t * 0.15, emissive=True, gain=1.25, limb=0.65, tint=(1.0, 0.72, 0.32), contrast=2.2)
    S.draw_planet(c, x, y, R, img)
    K.glow(c, x, y, R * 1.25, 0xFFFFB050, 0.18 * a)


def galaxy(c, t, cx, cy, scale, rot, alpha=1.0, tiltk=0.5):
    cr, sr = math.cos(rot), math.sin(rot)
    X = (GX * cr - GY * sr) * scale + cx
    Y = (GX * sr + GY * cr) * scale * tiltk + cy
    K.glow(c, cx, cy, scale * 0.55, 0xFFFFE3B0, 0.55 * alpha)
    K.glow(c, cx, cy, scale * 1.15, 0xFF7A6AD0, 0.18 * alpha)
    p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kPlus, StrokeCap=skia.Paint.kRound_Cap)
    for lo, hi, col, w in ((0.0, 0.45, 0xFF8FA8FF, 2.4), (0.45, 0.75, 0xFFC9D6FF, 3.0), (0.75, 1.01, 0xFFFFF0D8, 3.6)):
        m = (GB >= lo) & (GB < hi)
        pts = [skia.Point(float(a), float(b)) for a, b in zip(X[m], Y[m])]
        p.setColor(with_alpha(col, 0.75 * alpha))
        p.setStrokeWidth(w * max(0.6, scale / 700))
        c.drawPoints(skia.Canvas.kPoints_PointMode, pts, p)
    # el Sol dentro de la galaxia
    a = SUN_A0 + rot
    sx = SUN_R * math.cos(a) * scale + cx
    sy = SUN_R * math.sin(a) * scale * tiltk + cy
    return sx, sy


def scene(c, t, P):
    tl = P["tl"]
    c.clear(0xFF02030A)
    sg = K.seg_at(P, t)
    sid = sg["id"]
    lt = t - sg["a"]
    acc = V["accent"]
    if sid in ("h", "s1", "cta"):
        if sid == "h":
            STARS.draw(c, t, camx=t * 40, camy=0, zoom=1 + t * 0.05, streak=0.5 * (1 - prog(t, 2.5, 3.5)))
            R = lerp(560, 470, ease_out(prog(t, 0, 2.5)))
            earth(c, W / 2, 1060, R, spin=-0.9 + t * 0.35, lat0=0.3)
            K.counter(c, t, t + 0.3, lambda p: K.fmt(107000 * p) + " km/h", "TU VELOCIDAD AHORA MISMO", acc,
                      y=1460, dur=2.2)
        elif sid == "s1":
            STARS.draw(c, t, camx=t * 20, zoom=1.0)
            p = ease_in_out(prog(lt, 0, 1.0))
            R = lerp(470, 640, p)
            lat0 = lerp(0.3, 0.62, p)
            spin = lerp(-0.9 + sg["a"] * 0.35, math.radians(SPAIN[1]) - 0.35, p) + lt * 0.05
            cy = lerp(1060, 1150, p)
            earth(c, W / 2, cy, R, spin=spin, lat0=lat0)
            x, y, z = S.project(SPAIN[0], SPAIN[1], spin=spin, tilt=0.41, lat0=lat0)
            if z > 0.05:
                px, py = W / 2 + x * R, cy + y * R
                ring = (t * 1.2) % 1
                c.drawCircle(px, py, 14 + ring * 50, stroke(with_alpha(acc, 1 - ring), 5))
                c.drawCircle(px, py, 11, fill(acc))
                c.drawCircle(px, py, 11, stroke(WHITE, 4))
                K.tag(c, px + 170, py - 170, "ESTÁS AQUÍ", lt - 0.8, accent=WHITE, line_to=(px, py))
            K.counter(c, t, lt - 1.0, lambda p: K.fmt(1300 * p) + " km/h", "SOLO POR LA ROTACIÓN", acc, y=1480)
        else:  # cta
            STARS.draw(c, t, camx=t * 15)
            earth(c, W / 2, 840, 330, spin=-0.5 + t * 0.2, lat0=0.35)
        return
    if sid in ("s2", "q", "q_count"):
        a2 = tl["s2"][0]
        l2 = t - a2
        STARS.draw(c, t, camx=t * 10, zoom=1 - 0.1 * ease_out(prog(l2, 0, 1.5)))
        sx, sy = W / 2, 930
        A, B = 400, 120
        th = 0.8 + l2 * 0.45
        ex, ey = sx + A * math.cos(th), sy + B * math.sin(th)
        p = ease_in_out(prog(l2, 0, 1.0))
        # órbita
        orbit = skia.Path()
        orbit.addOval(skia.Rect.MakeLTRB(sx - A, sy - B, sx + A, sy + B))
        op = stroke(with_alpha(acc, 0.35 * p), 3)
        op.setPathEffect(skia.DashPathEffect.Make([14, 12], -t * 30))
        c.drawPath(orbit, op)
        # estela
        for k in range(30):
            tk = th - k * 0.03
            c.drawCircle(sx + A * math.cos(tk), sy + B * math.sin(tk), 8 * (1 - k / 30),
                         fill(with_alpha(acc, 0.5 * (1 - k / 30) * p)))
        ER = lerp(640, 46, p)
        exx, eyy = lerp(W / 2, ex, p), lerp(1150, ey, p)
        behind = math.sin(th) < 0
        sun_a = prog(l2, 0.3, 1.2)
        if behind:
            earth(c, exx, eyy, ER, spin=t * 0.4, lat0=0.3, light=(sx - exx, -(sy - eyy), 200))
        if sun_a > 0:
            sun(c, sx, sy, 150 * ease_out(sun_a), t, sun_a)
        if not behind:
            earth(c, exx, eyy, ER, spin=t * 0.4, lat0=0.3, light=((sx - exx) / 400, -(sy - eyy) / 400, 0.3))
        if p >= 1:
            K.tag(c, ex, ey - 90, "TIERRA", l2 - 1.0, accent=WHITE, size=30)
        if sid == "s2":
            K.counter(c, t, l2 - 1.0, lambda p: K.fmt(107000 * p) + " km/h", "ALREDEDOR DEL SOL", acc, y=1480)
        return
    # galaxia: r, s3, s4
    ar = tl["r"][0]
    lr = t - ar
    STARS.draw(c, t, camx=t * 5, alpha=0.7, band=False)
    zoomp = ease_in_out(prog(lr, 0, 1.6))
    scale = lerp(4200, 540, zoomp)
    rot = -0.4 - (t - ar) * 0.06
    cx = W / 2
    cy = 960
    # centrar en el Sol al principio y alejarse
    ox = lerp(-SUN_R * math.cos(SUN_A0 + rot) * 4200, 0, zoomp)
    oy = lerp(-SUN_R * math.sin(SUN_A0 + rot) * 4200 * 0.5, 0, zoomp)
    sxg, syg = galaxy(c, t, cx + ox, cy + oy, scale, rot, alpha=0.4 + 0.6 * zoomp)
    ring = (t * 1.1) % 1
    c.drawCircle(sxg, syg, 10 + ring * 40, stroke(with_alpha(0xFFFFD27A, 1 - ring), 4))
    K.glow(c, sxg, syg, 50, 0xFFFFD27A, 0.9)
    c.drawCircle(sxg, syg, 7, fill(WHITE))
    K.tag(c, sxg - 150, syg + 150, "EL SOL", lr - 1.8, accent=0xFFFFD27A, line_to=(sxg, syg))
    if sid == "r":
        K.counter(c, t, lr - 1.7, lambda p: K.fmt(800000 * p) + " km/h", "ALREDEDOR DE LA GALAXIA", acc, y=1480)
    else:
        a3 = tl["s3"][0]
        l3 = t - a3
        # trayectoria completa del Sol
        pth = skia.Path()
        pth.addOval(skia.Rect.MakeLTRB(cx - SUN_R * scale, cy - SUN_R * scale * 0.5, cx + SUN_R * scale,
                                       cy + SUN_R * scale * 0.5))
        meas = skia.PathMeasure(pth, False)
        seg = skia.Path()
        meas.getSegment(0, meas.getLength() * ease_out(prog(l3, 0.2, 2.4)), seg, True)
        pp = stroke(with_alpha(0xFFFFD27A, 0.85), 5)
        pp.setPathEffect(skia.DashPathEffect.Make([16, 10], -t * 40))
        c.drawPath(seg, pp)
        if sid == "s3":
            K.counter(c, t, l3 - 0.2, lambda p: K.fmt(230 * p) + " M años", "UNA SOLA VUELTA", acc, y=1480)
        else:
            l4 = t - tl["s4"][0]
            K.tag(c, W / 2, 1480, "HACE ≈ 230 MILLONES DE AÑOS", l4 - 0.3, accent=0xFFFFD27A, size=44)


if __name__ == "__main__":
    K.run(V, scene, "/home/claude/tiktok/out35", preview="auto" if len(sys.argv) > 1 else None)
