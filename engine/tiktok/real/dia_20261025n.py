"""Lote nocturno 25/10/2026 · 5 vídeos de espacio con texturas reales (71–75)."""
import math, sys
import numpy as np
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import spheres as S
import core as K
import hc
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, pill, glow
import v33_planetas as P33

OUT = "/home/claude/tiktok/outnight"
CTA = "¡Comenta y sígueme para más!"
DAY = S.load("earth_atmos_2048.jpg")
NIGHT = S.load("earth_lights_2048.png")
SPEC = S.load("earth_specular_2048.jpg", "L")
CLOUDS = S.load("earth_clouds_1024.png", "A")
MOON = S.load("moon_1024.jpg")
SUN = S.load("sunmap.jpg")
SAT = S.load("saturnmap.jpg")
MARS = S.load("marsmap1k.jpg")
STARS = K.Stars(seed=71)
LIGHT = (-0.55, 0.35, 0.75)


def earth(c, x, y, R, spin, lat0=0.4, light=LIGHT):
    if R < 2:
        c.drawCircle(x, y, max(R, 1.5), fill(0xFF5AA8FF)); return
    img = S.render(2 * R, DAY, spin=spin, light=light, night=NIGHT, spec=SPEC, clouds=CLOUDS, lat0=lat0, gain=1.12)
    S.draw_planet(c, x, y, R, img); S.atmosphere(c, x, y, R)


def moon(c, x, y, R, spin=0.3, light=LIGHT):
    img = S.render(2 * R, MOON, spin=spin, light=light, ambient=0.04, gain=1.1)
    S.draw_planet(c, x, y, R, img)


def sun(c, x, y, R, t):
    glow(c, x, y, R * 2.4, 0xFFFFA030, 0.9)
    img = S.render(2 * R, SUN, spin=t * 0.05, emissive=True, gain=1.25, tint=(1.0, 0.82, 0.45), contrast=1.4, limb=0.5)
    S.draw_planet(c, x, y, R, img)


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


# ------------------------------------------------------------------ 71 Voyager
def probe(c, x, y, s, t):
    """Sonda tipo Voyager: antena parabólica, cuerpo y mástiles."""
    c.save(); c.translate(x, y); c.rotate(-18 + math.sin(t * 0.6) * 3); c.scale(s, s)
    c.drawLine(-10, 0, -230, 40, stroke(0xFFB8B8C0, 5))
    c.drawLine(10, 10, 170, 120, stroke(0xFFB8B8C0, 4))
    c.drawRect(skia.Rect.MakeXYWH(-38, 10, 76, 46), fill(0xFF8A7A5A))
    c.drawRect(skia.Rect.MakeXYWH(-38, 10, 76, 46), stroke(0xFFE0C890, 3))
    g = skia.GradientShader.MakeRadial((-20, -40), 140, [0xFFFFFFFF, 0xFFC8CCD8, 0xFF6A7080])
    c.drawOval(skia.Rect.MakeXYWH(-110, -70, 220, 80), skia.Paint(Shader=g, AntiAlias=True))
    c.drawOval(skia.Rect.MakeXYWH(-110, -70, 220, 80), stroke(0xFF404450, 3))
    c.drawLine(0, -30, 0, -95, stroke(0xFFD0D0D8, 4)); c.drawCircle(0, -98, 7, fill(WHITE))
    c.drawCircle(150, 104, 14, fill(0xFF5A5A62))
    c.restore()


def s_voyager(c, t, P, V):
    sid, lt = seg(P, t); tl = P["tl"]
    c.clear(0xFF010208)
    STARS.draw(c, t, camx=t * 40, zoom=1.0 + t * 0.004, alpha=1.0)
    # la Tierra se aleja hasta ser un punto
    pe = ease_in_out(prog(t, 0.5, 9.0))
    eR = lerp(420, 3, pe)
    ex, ey = lerp(W / 2, 170, pe), lerp(1300, 1500, pe)
    earth(c, ex, ey, eR, t * 0.05)
    if eR < 12:
        K.tag(c, ex + 40, ey - 70, "TIERRA", t - 9.0, accent=0xFF5AA8FF, size=28)
    px, py = 760 + math.sin(t * 0.4) * 20, 760 + math.cos(t * 0.3) * 14
    s0 = ease_back(prog(t, 0.2, 1.0), 1.4)
    probe(c, px, py, 1.15 * s0, t)
    if sid == "h":
        K.tag(c, px, py + 210, "VOYAGER 1", lt - 0.8, accent=V["accent"], size=36)
    if sid == "s1":
        K.counter(c, t, lt - 0.3, lambda p: str(int(round(lerp(1970, 1977, p)))), "AÑO DE LANZAMIENTO", V["accent"], y=1560)
    if sid in ("s2", "s3"):
        K.counter(c, t, lt - 0.3, lambda p: K.fmt(25900 * p) + " M km", "DE LA TIERRA", V["accent"], y=1560)
    if sid in ("s3", "s4"):
        # pulso de luz viajando de la sonda a la Tierra
        ph = (lt * 0.35) % 1
        lx, ly = lerp(px, ex, ph), lerp(py, ey, ph)
        glow(c, lx, ly, 60, 0xFFFFE08A, 0.9); c.drawCircle(lx, ly, 10, fill(WHITE))
        c.drawLine(px, py, ex, ey, stroke(with_alpha(0xFFFFE08A, 0.18), 3))
    if sid == "s4":
        hc.big(c, "24 HORAS", W / 2, 1600, 150, V["accent"], lt, 0.2)
    if sid == "s5":
        hc.big(c, "18 NOV 2026", W / 2, 1600, 130, V["accent"], lt, 0.2)
    if sid == "cta":
        # disco de oro (teaser)
        r = 170 * ease_back(prog(lt, 0, 0.6), 1.5)
        if r > 1:
            g = skia.GradientShader.MakeSweep(W / 2, 1450, [0xFFFFD27A, 0xFFB8862E, 0xFFFFE9A8, 0xFFB8862E, 0xFFFFD27A])
            c.drawCircle(W / 2, 1450, r, skia.Paint(Shader=g, AntiAlias=True))
            for k in range(6):
                c.drawCircle(W / 2, 1450, r * (0.3 + 0.12 * k), stroke(with_alpha(0xFF6A4A10, 0.35), 2))
            c.drawCircle(W / 2, 1450, r * 0.12, fill(0xFF3A2A08))
            c.save(); c.translate(W / 2, 1450); c.rotate(lt * 40)
            c.drawLine(0, 0, r * 0.95, 0, stroke(with_alpha(WHITE, 0.5), 3)); c.restore()


V71 = dict(slug="71_voyager", accent=0xFFFFD27A, drone=0.02, scene=s_voyager, segs=[
    dict(id="h", who="nar", say="Ahora mismo hay una máquina humana a casi un día luz de la Tierra.",
         cap="Hay una máquina humana | a casi *UN DÍA LUZ* | de la Tierra"),
    dict(id="s1", who="nar", cut=True, say="Se llama Voyager uno. La lanzaron en mil novecientos setenta y siete… y nunca ha dejado de alejarse.",
         cap="*Voyager 1*. | Lanzada en *1977*… | y no ha parado"),
    dict(id="s2", who="nar", say="El dieciocho de noviembre de este año estará a casi veintiséis mil millones de kilómetros.",
         cap="Estará a casi | *26.000 millones* | de kilómetros"),
    dict(id="s3", who="nar", say="Tan lejos, que su señal, viajando a la velocidad de la luz…",
         cap="Tan lejos, que su señal | a la *velocidad de la luz*…"),
    dict(id="s4", who="nar", say="tardará un día entero en llegar. Veinticuatro horas.", cap="tardará *UN DÍA* | en llegar"),
    dict(id="s5", who="nar", cut=True, say="Será lo primero que la humanidad haya enviado a un día luz de casa.",
         cap="Lo primero de la humanidad | a *un día luz* | de casa"),
    dict(id="cta", who="nar", cut=True,
         say="Y lleva dentro un disco de oro con un mensaje para extraterrestres. Lo que dice… te lo cuento mañana. Sígueme.",
         cap="Lleva un *disco de oro* | para *extraterrestres*… | mañana te lo cuento. *SÍGUEME*"),
])


# ------------------------------------------------------------------ 72 Sol 8 minutos
def s_sol(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020208)
    STARS.draw(c, t, camx=t * 8, zoom=1.0, alpha=0.8)
    gone = sid in ("s2", "s3", "s4") and True
    fade = 1.0
    if sid == "s1":
        fade = 1.0 - ease_in_out(prog(lt, 1.0, 1.6))
    elif gone:
        fade = 0.0
    if sid == "cta":
        fade = 1.0
    sx, sy, sr = 300, 640, 230
    if fade > 0.01:
        c.saveLayerAlpha(None, int(255 * fade)); sun(c, sx, sy, sr, t); c.restore()
    elif sid in ("s2", "s3", "s4"):
        c.drawCircle(sx, sy, sr, stroke(with_alpha(WHITE, 0.25), 3))
        K.tag(c, sx, sy + sr + 50, "YA NO ESTÁ", lt, accent=0xFFFF5A5A, size=32)
    # Tierra en órbita, iluminada por el Sol
    ang = t * 0.06
    ex, ey = 800 + math.cos(ang) * 30, 1180 + math.sin(ang) * 30
    li = (-(ex - sx), -(ey - sy) * -1, 400)
    n = math.sqrt(li[0] ** 2 + li[1] ** 2 + li[2] ** 2)
    earth(c, ex, ey, 190, t * 0.08, light=(li[0] / n, li[1] / n, li[2] / n))
    # luz viajando (aún llega)
    if sid in ("h", "s2", "s3"):
        for k in range(5):
            ph = ((t * 0.18) + k / 5) % 1
            if sid == "s3" and k / 5 + t * 0.18 % 1 > 1:
                continue
            lx, ly = lerp(sx + 200, ex - 170, ph), lerp(sy + 120, ey - 110, ph)
            glow(c, lx, ly, 40, 0xFFFFD08A, 0.6)
    if sid in ("s2", "s3"):
        frac = clamp((t - P["tl"]["s2"][0]) / 9.0)
        rem = 500 * (1 - frac)
        hc.timer(c, W / 2, 1640, 120, 1 - frac, "%d:%02d" % (rem // 60, rem % 60), V["accent"])
    if sid == "s4":
        hc.big(c, "8 MIN 20 S", W / 2, 1620, 140, V["accent"], lt, 0.1)


V72 = dict(slug="72_sol_8min", accent=0xFFFFB13C, drone=0.02, scene=s_sol, segs=[
    dict(id="h", who="nar", say="Si el Sol desapareciera ahora mismo… no te enterarías hasta dentro de ocho minutos.",
         cap="Si el *SOL* desapareciera… | no te enterarías hasta | dentro de *8 minutos*"),
    dict(id="s1", who="nar", cut=True, say="Imagina que se apaga. Ya.", cap="Imagina que | se *apaga*. | *YA*."),
    dict(id="s2", who="nar", say="La luz que te está llegando salió de él hace unos ocho minutos y veinte segundos. Sigue viajando.",
         cap="La luz que ves salió | hace *8 min y 20 s*. | *Sigue viajando*"),
    dict(id="s3", who="nar", say="Y la Tierra seguiría girando a su alrededor igual, porque la gravedad también viaja a la velocidad de la luz.",
         cap="Y la Tierra *seguiría girando*: | la *gravedad* también viaja | a la velocidad de la luz"),
    dict(id="s4", who="nar", cut=True, say="Ocho minutos y veinte segundos de normalidad… antes de la oscuridad total.",
         cap="*8 minutos* de normalidad… | antes de la | *oscuridad*"),
    dict(id="cta", who="nar", cut=True, say="¿Qué harías en esos ocho minutos? " + CTA,
         cap="¿Qué harías en | esos *8 minutos*? | *COMENTA*"),
])


# ------------------------------------------------------------------ 73 Saturno flota
def ocean(c, y0, t, alpha=1.0):
    g = skia.GradientShader.MakeLinear([(0, y0), (0, H)], [with_alpha(0xFF2A8FD8, 0.85 * alpha), with_alpha(0xFF04204A, alpha)])
    path = skia.Path(); path.moveTo(0, H)
    for i in range(0, W + 20, 20):
        path.lineTo(i, y0 + math.sin(i * 0.012 + t * 2.2) * 14 + math.sin(i * 0.031 - t * 1.4) * 7)
    path.lineTo(W, H); path.close()
    c.drawPath(path, skia.Paint(Shader=g, AntiAlias=True))
    sp = skia.Path(); sp.moveTo(0, y0)
    for i in range(0, W + 20, 20):
        sp.lineTo(i, y0 + math.sin(i * 0.012 + t * 2.2) * 14 + math.sin(i * 0.031 - t * 1.4) * 7)
    c.drawPath(sp, stroke(with_alpha(0xFFCFF0FF, 0.7 * alpha), 4))


def saturn(c, x, y, R, t):
    P33.saturn_ring(c, x, y, R, front=False)
    img = S.render(2 * R, SAT, spin=t * 0.1, tilt=math.radians(-14), light=LIGHT, ambient=0.05, gain=1.15)
    S.draw_planet(c, x, y, R, img)
    P33.saturn_ring(c, x, y, R, front=True)


def s_saturno(c, t, P, V):
    sid, lt = seg(P, t); tl = P["tl"]
    c.clear(0xFF03040C)
    STARS.draw(c, t, camx=t * 10, zoom=1.0, alpha=0.8)
    R = 230
    wy = 1250
    y = 820
    show_ocean = sid not in ("h", "s1")
    if sid in ("q", "q_count"):
        y = 820 + math.sin(t * 2) * 10
    if sid == "r" or sid in ("s3", "s4", "cta"):
        a = tl["r"][0]
        p = ease_out(prog(t, a, a + 1.6))
        y = lerp(820, wy - R * 0.25, p) + (math.sin((t - a) * 2.4) * 18 * (1 - p) if p < 1 else math.sin(t * 1.6) * 8)
    saturn(c, W / 2, y, R, t)
    if show_ocean:
        ocean(c, wy, t, ease_out(prog(t, tl["s2"][0], tl["s2"][0] + 0.8)))
    if sid == "h":
        K.tag(c, W / 2, y + R + 90, "SATURNO", lt - 0.5, accent=V["accent"], size=36)
    if sid == "s1":
        K.counter(c, t, lt - 0.3, lambda p: "×" + str(int(round(1 + 94 * p))), "LA MASA DE LA TIERRA", V["accent"], y=1600)
    if sid == "s3":
        K.counter(c, t, lt - 0.2, lambda p: "%.2f g/cm³" % (0.69 * p), "SU DENSIDAD", V["accent"], y=1650)
    if sid == "s4":
        hc.big(c, "AGUA = 1", W / 2, 1650, 120, WHITE, lt, 0.1)


V73 = dict(slug="73_saturno_flota", accent=0xFFF2C77A, drone=0.02, scene=s_saturno, segs=[
    dict(id="h", who="nar", say="Este planeta flotaría en el agua. Y no es pequeño.",
         cap="Este planeta | *FLOTARÍA* | en el agua"),
    dict(id="s1", who="nar", cut=True, say="Saturno pesa noventa y cinco veces más que la Tierra.",
         cap="Saturno pesa | *95 veces* | más que la Tierra"),
    dict(id="s2", who="nar", say="Imagina una bañera lo bastante grande para meterlo dentro.", cap="Imagina una *bañera* | gigante…"),
    dict(id="q", who="q", say="¿Qué pasaría? ¿Se hunde o flota?", cap="¿Se *HUNDE* | o *FLOTA*?",
         quiz=dict(a="SE HUNDE", b="FLOTA", ans="b")),
    dict(id="r", who="nar", cut=True, say="Flota. Saturno es casi todo hidrógeno y helio, los gases más ligeros que existen.",
         cap="*FLOTA*. | Casi todo es *hidrógeno* | y *helio*"),
    dict(id="s3", who="nar", say="Su densidad media es de cero coma sesenta y nueve gramos por centímetro cúbico.",
         cap="Su densidad: | *0,69 g/cm³*"),
    dict(id="s4", who="nar", say="El agua tiene uno. Así que es menos denso que el agua. El único planeta así del sistema solar.",
         cap="El agua: *1*. | El *único planeta* | menos denso que el agua"),
    dict(id="cta", who="nar", cut=True, say="¿Lo sabías? " + CTA, cap="¿Lo sabías? | *COMENTA* | y *SÍGUEME*"),
])


# ------------------------------------------------------------------ 74 La Luna se aleja
def s_luna(c, t, P, V):
    sid, lt = seg(P, t); tl = P["tl"]
    c.clear(0xFF020308)
    STARS.draw(c, t, camx=t * 10, zoom=1.0, alpha=0.9)
    ex, ey, eR = 330, 1180, 250
    earth(c, ex, ey, eR, t * 0.07)
    drift = ease_in_out(prog(t, 0.5, 30.0)) * 90
    mx, my = 800 + drift, 640 - drift * 0.5
    moon(c, mx, my, 110, spin=0.2 + t * 0.01)
    if sid in ("s2", "s3"):
        # láser desde la Tierra a la Luna y de vuelta
        ph = (lt * 0.8) % 2
        p = ph if ph < 1 else 2 - ph
        sx, sy = ex + eR * 0.55, ey - eR * 0.6
        lx, ly = lerp(sx, mx - 80, p), lerp(sy, my + 70, p)
        c.drawLine(sx, sy, lx, ly, stroke(with_alpha(0xFF3CFF6A, 0.85), 6))
        glow(c, lx, ly, 40, 0xFF3CFF6A, 0.9)
        K.tag(c, mx, my + 180, "REFLECTOR APOLO 11", lt - 0.6, accent=0xFF3CFF6A, size=28)
    if sid == "s1":
        K.counter(c, t, lt - 0.3, lambda p: "%.1f cm" % (3.8 * p), "CADA AÑO", V["accent"], y=1600)
    if sid == "s4":
        # uña creciendo como comparación
        hc.big(c, "≈ TUS UÑAS", W / 2, 1600, 110, V["accent"], lt, 0.1)
    if sid == "s5":
        K.counter(c, t, lt - 0.3, lambda p: "%.0f m" % (38 * p), "EN 1.000 AÑOS", V["accent"], y=1600)


V74 = dict(slug="74_luna_se_aleja", accent=0xFFBFD7FF, drone=0.02, scene=s_luna, segs=[
    dict(id="h", who="nar", say="La Luna se está escapando de la Tierra. Y lo podemos medir.",
         cap="La *LUNA* se está | *escapando* | de la Tierra"),
    dict(id="s1", who="nar", cut=True, say="Cada año se aleja unos tres coma ocho centímetros.", cap="Cada año se aleja | *3,8 cm*"),
    dict(id="s2", who="nar", say="¿Cómo lo sabemos? En mil novecientos sesenta y nueve, el Apolo once dejó allí unos espejos.",
         cap="En *1969*, el *Apolo 11* | dejó allí | unos *espejos*"),
    dict(id="s3", who="nar", say="Desde la Tierra se les dispara un láser… y se mide cuánto tarda en volver.",
         cap="Se les dispara un *láser*… | y se mide cuánto | tarda en *volver*"),
    dict(id="s4", who="nar", cut=True, say="Tres coma ocho centímetros al año es, más o menos, lo que crecen tus uñas.",
         cap="*3,8 cm* al año… | lo que crecen | tus *uñas*"),
    dict(id="s5", who="nar", say="Parece poco… pero en mil años son treinta y ocho metros. Y no va a parar.",
         cap="En *1.000 años*: | *38 metros*. | Y no para"),
    dict(id="cta", who="nar", cut=True, say="¿Y qué le pasará a la Tierra cuando esté más lejos? Eso, en la parte dos. Sígueme.",
         cap="¿Y qué le pasará | a la *Tierra*? | *Parte 2*… *SÍGUEME*"),
])


# ------------------------------------------------------------------ 75 Atardecer azul en Marte
def sky(c, top, mid, bot, hz):
    g = skia.GradientShader.MakeLinear([(0, 0), (0, hz)], [top, mid, bot], [0, 0.6, 1])
    c.drawRect(skia.Rect.MakeWH(W, hz), skia.Paint(Shader=g))


def dunes(c, hz, col1, col2, t):
    for k, (col, amp, off) in enumerate([(col1, 40, 0.0), (col2, 60, 1.7)]):
        p = skia.Path(); p.moveTo(0, H)
        for i in range(0, W + 30, 30):
            p.lineTo(i, hz + k * 120 + math.sin(i * 0.006 + off) * amp + math.sin(i * 0.017 + off * 2) * amp * 0.3)
        p.lineTo(W, H); p.close()
        c.drawPath(p, fill(col))


def s_marte(c, t, P, V):
    sid, lt = seg(P, t); tl = P["tl"]
    hz = 1250
    if sid in ("h", "s1"):
        c.clear(0xFF02030A)
        STARS.draw(c, t, camx=t * 10, zoom=1.0, alpha=0.9)
        R = lerp(380, 460, ease_in_out(prog(t, 0, 8)))
        img = S.render(2 * R, MARS, spin=t * 0.06, light=LIGHT, ambient=0.05, gain=1.15)
        S.draw_planet(c, W / 2, 900, R, img)
        S.atmosphere(c, W / 2, 900, R, color=0xFFFF9A6A, strength=0.5)
        if sid == "s1":
            K.tag(c, W / 2, 900 + R + 70, "CURIOSITY · 2015", lt - 0.5, accent=V["accent"], size=32)
        return
    earthy = sid in ("s3",)
    sunset = ease_in_out(prog(lt, 0, 3.0)) if sid == "s2" else 1.0
    if earthy:
        sky(c, 0xFF1A3A7A, 0xFFFF8A3C, 0xFFFF5A2A, hz)
        sx, sy = W / 2, hz - 120
        glow(c, sx, sy, 300, 0xFFFF6A2A, 0.9)
        c.drawCircle(sx, sy, 60, fill(0xFFFFD08A))
        dunes(c, hz, 0xFF2A1A12, 0xFF1A100A, t)
        K.tag(c, W / 2, 600, "TIERRA", lt - 0.2, accent=0xFFFF8A3C, size=40)
        return
    # cielo marciano: de día ocre, al atardecer halo azul alrededor del Sol
    top = 0xFF3A2416 if sunset > 0.5 else 0xFFB07850
    sky(c, top, 0xFF8A5A3A, 0xFF6A4A3A, hz)
    sx, sy = W / 2, lerp(500, hz - 90, sunset)
    blue = sunset
    glow(c, sx, sy, 420, 0xFF4A8CFF, 0.9 * blue)
    glow(c, sx, sy, 180, 0xFFA8D0FF, 0.9 * blue)
    c.drawCircle(sx, sy, 34, fill(0xFFF2F6FF))
    dunes(c, hz, 0xFF7A3E22, 0xFF4E2614, t)
    # rover sencillo en silueta
    rx, ry = 260, hz + 60
    c.drawRect(skia.Rect.MakeXYWH(rx - 70, ry - 60, 140, 40), fill(0xFF1A0E08))
    c.drawLine(rx + 40, ry - 60, rx + 40, ry - 140, stroke(0xFF1A0E08, 8))
    c.drawRect(skia.Rect.MakeXYWH(rx + 20, ry - 165, 50, 28), fill(0xFF1A0E08))
    for k in (-50, 0, 50):
        c.drawCircle(rx + k, ry, 20, fill(0xFF1A0E08))
    if sid == "cta":
        K.tag(c, W / 2, 600, "MARTE", lt - 0.2, accent=0xFF4A8CFF, size=40)


V75 = dict(slug="75_marte_azul", accent=0xFF6FA8FF, drone=0.02, scene=s_marte, segs=[
    dict(id="h", who="nar", say="En Marte, los atardeceres son azules.", cap="En *MARTE*, | los atardeceres | son *AZULES*"),
    dict(id="s1", who="nar", cut=True, say="Lo fotografió el rover Curiosity en dos mil quince, desde el cráter Gale.",
         cap="Lo fotografió | el rover *Curiosity* | en *2015*"),
    dict(id="s2", who="nar", cut=True,
         say="Durante el día el cielo marciano es color caramelo. Pero cuando el Sol se pone… aparece un halo azul.",
         cap="De día: color *caramelo*. | Al ponerse el Sol… | un halo *AZUL*"),
    dict(id="s3", who="nar", cut=True, say="En la Tierra pasa justo lo contrario: el cielo es azul y el atardecer, naranja.",
         cap="En la Tierra, | *al revés*: | cielo azul, atardecer *naranja*"),
    dict(id="s4", who="nar", cut=True,
         say="La culpa es del polvo marciano: sus granos dejan pasar mejor la luz azul en la dirección del Sol.",
         cap="La culpa: el *polvo*. | Deja pasar la luz *azul* | hacia el Sol"),
    dict(id="cta", who="nar", cut=True, say="¿Te imaginas verlo en persona? " + CTA,
         cap="¿Te imaginas | *verlo*? | *COMENTA* y *SÍGUEME*"),
])

VIDEOS = [V71, V72, V73, V74, V75]


def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
    return scene


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = "auto" if len(sys.argv) > 2 else None
    for i in idxs:
        V = VIDEOS[i]
        K.run(V, make_scene(V), OUT, preview=pv)
