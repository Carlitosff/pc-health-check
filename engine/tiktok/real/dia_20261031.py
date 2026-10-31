"""Lote diario 31/10/2026 (601–610) — HALLOWEEN. Motor v9 (CUENTA ATRÁS VISIBLE hasta la revelación:
V['reveal']=(seg, 'LA RESPUESTA') -> pill con reloj 'LA RESPUESTA EN 9s' que baja en tiempo real, late en rojo y hace
tic-tac los 3 últimos segundos y estalla '¡AHORA!'. Objetivo: tiempo medio 11-18 s -> que la gente llegue al dato).
Mezcla según métricas 29/10 a 48 h (techo ~1.300, sin crecimiento de 24 a 48 h): ilusiones en serie (T4 nueva:
serpientes de Kitaoka, espiral de Fraser, ilusión de White) + reto de conteo (rectángulos) en la noche; Titán a las 12:00
(lo prometido tras Ganímedes); mito de clase (Einstein), mito de animales (pájaro tocado), '3 cosas' (frío);
Houdini: murió en Halloween hace exactamente 100 años (31/10/1926) -> serie implícita (el código 'Rosabelle', mañana)."""
import math, sys, random
import numpy as np
import skia
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
import v33_planetas as P33
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow, pill
from core import draw_text, font, text_w

OUT = "/home/claude/tiktok/outdaily"
ILU = 0xFFFFE04D
GREEN = 0xFF2FD46B
RED = 0xFFFF3B4A


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


def blur(r):
    return skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r)


# ====================================================================== 601 Titán (lo prometido)
def titan_texture():
    path = S.TEX + "titan_proc.png"
    try:
        Image.open(path)
        return S.load("titan_proc.png")
    except Exception:
        pass
    w, h = 2048, 1024
    rnd = np.random.default_rng(601)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = np.zeros((h, w), np.float32)
    for k in range(6):
        f = 2 ** k
        ph = rnd.uniform(0, 6.28, 3)
        n += np.sin(xx / w * 6.28 * f + ph[0] + 1.6 * np.sin(yy / h * 6.28 * f * 0.7 + ph[1])) * \
            np.cos(yy / h * 3.14 * f * 1.3 + ph[2]) / (k + 1) ** 0.9
    n = (n - n.min()) / (n.max() - n.min())
    lat = np.abs(yy / h - 0.5) * 2
    dunes = (lat < 0.35) & (n < 0.5)  # campos de dunas oscuros en el ecuador
    v = np.where(dunes, 0.55 + 0.1 * n, 0.8 + 0.15 * n)
    img = np.stack([v * 0.95, v * 0.62, v * 0.25], -1)
    # lagos de metano cerca del polo norte (oscuros, lisos)
    lakes = (yy / h < 0.16) & (n > 0.62)
    img[lakes] = [0.18, 0.13, 0.08]
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    im.save(path)
    return S.load("titan_proc.png")


TITAN = titan_texture()
SAT = S.load("saturnmap.jpg")
DAY = S.load("earth_atmos_2048.jpg")
CLOUDS = S.load("earth_clouds_1024.png", "A")
ST = K.Stars(seed=601)
L0 = (-0.55, 0.3, 0.78)


def titan(c, x, y, R, t, haze=1.0):
    S.draw_planet(c, x, y, R, S.render(2 * R, TITAN, spin=t * 0.12, light=L0, gain=1.05, limb=0.55, ambient=0.12))
    # neblina naranja espesa (la atmósfera tapa casi toda la superficie)
    c.drawCircle(x, y, R, skia.Paint(AntiAlias=True, Color=with_alpha(0xFFE8A040, 0.45 * haze)))
    S.atmosphere(c, x, y, R, color=0xFFFFB050, strength=1.4 * haze)
    S.atmosphere(c, x, y, R * 1.04, color=0xFF7AA8FF, strength=0.35 * haze)


def saturn(c, x, y, R, t):
    P33.saturn_ring(c, x, y, R, front=False)
    S.draw_planet(c, x, y, R, S.render(2 * R, SAT, spin=t * 0.1, tilt=math.radians(-14), light=L0, ambient=0.05, gain=1.15))
    P33.saturn_ring(c, x, y, R, front=True)


def titan_land(c, t, rain=0.0, lake=True):
    """Superficie de Titán: cielo naranja, dunas, lago de metano con oleaje lento y lluvia de gotas grandes y lentas."""
    sky = skia.GradientShader.MakeLinear([(0, 0), (0, 1400)], [0xFF3A1E08, 0xFFB86A22, 0xFFE8A050])
    c.drawRect(skia.Rect.MakeWH(W, 1400), skia.Paint(Shader=sky))
    glow(c, W * 0.7, 520, 260, 0xFFFFE0A0, 0.18)  # el Sol, apenas una mancha difusa
    for k, (yb, col) in enumerate(((1180, 0xFF6A3A14), (1290, 0xFF4E2A0E))):
        p = skia.Path(); p.moveTo(0, H)
        for x in range(0, W + 40, 40):
            p.lineTo(x, yb + 60 * math.sin(x * 0.006 + k * 2 + t * 0.05) + 25 * math.sin(x * 0.017 + k))
        p.lineTo(W, H); p.close()
        c.drawPath(p, fill(col))
    if lake:
        top = 1420
        c.drawRect(skia.Rect.MakeLTRB(0, top, W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear(
            [(0, top), (0, H)], [0xFF2A1A0C, 0xFF0C0804])))
        for k in range(14):
            y = top + 20 + k * k * 3.2
            ph = t * 0.5 + k
            c.drawLine(0, y + math.sin(ph) * 3, W, y + math.sin(ph * 1.3) * 3, stroke(with_alpha(0xFFE8A050, 0.10 + 0.012 * k), 2 + k * 0.3))
        c.drawRect(skia.Rect.MakeLTRB(W * 0.55, top, W * 0.85, H), fill(with_alpha(0xFFFFD090, 0.05)))
    if rain > 0:
        R = random.Random(3)
        for i in range(160):
            x0 = R.uniform(0, W)
            sp = R.uniform(140, 230)  # cae despacio: gravedad baja y aire denso
            y = (R.uniform(0, 1500) + t * sp) % 1500
            L = R.uniform(18, 34)
            c.drawLine(x0, y, x0 - 4, y + L, stroke(with_alpha(0xFFFFE8C0, 0.45 * rain), R.uniform(4, 7)))
            if y > 1380 and lake:
                c.drawOval(skia.Rect.MakeXYWH(x0 - 18, 1430 + (i % 7) * 30, 36, 8), stroke(with_alpha(0xFFFFE0B0, 0.25 * rain), 2))


def huygens(c, x, y, s, t):
    c.save(); c.translate(x, y + math.sin(t * 2) * 6); c.rotate(math.sin(t * 1.3) * 4)
    can = skia.Path(); can.moveTo(-260 * s, -380 * s); can.quadTo(0, -620 * s, 260 * s, -380 * s); can.close()
    c.drawPath(can, fill(0xFFE8E2D6))
    for k in range(-3, 4):
        c.drawLine(k * 74 * s, -395 * s - (9 - k * k) * 5 * s, 0, -40 * s, stroke(with_alpha(0xFF8A7A6A, 0.9), 2.5))
    for k in range(-2, 3):
        c.drawLine(k * 100 * s, -420 * s, k * 100 * s, -380 * s - 10, stroke(0xFFC0B8AA, 4))
    c.drawOval(skia.Rect.MakeXYWH(-80 * s, -40 * s, 160 * s, 70 * s), fill(0xFFD8B860))
    c.drawOval(skia.Rect.MakeXYWH(-80 * s, -40 * s, 160 * s, 70 * s), stroke(0xFF8A6A20, 4))
    c.drawRect(skia.Rect.MakeXYWH(-50 * s, 10 * s, 100 * s, 22 * s), fill(0xFF9A9A9A))
    c.restore()


def dragonfly(c, x, y, s, t):
    c.save(); c.translate(x, y + math.sin(t * 2.2) * 14); c.rotate(math.sin(t * 1.1) * 3)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-150 * s, -40 * s, 300 * s, 80 * s), 30 * s, 30 * s), fill(0xFFDADDE2))
    c.drawRect(skia.Rect.MakeXYWH(-120 * s, -20 * s, 240 * s, 12 * s), fill(0xFFE0B020))
    for dx in (-230, -130, 130, 230):
        for dy in (-70, -110):
            c.drawLine(dx * 0.55 * s, -30 * s, dx * s, dy * s, stroke(0xFF9AA0AA, 7 * s))
            spin = (t * 31 + dx) % 6.28
            w = 110 * s * abs(math.cos(spin))
            c.drawOval(skia.Rect.MakeXYWH(dx * s - max(w, 8), dy * s - 7 * s, 2 * max(w, 8), 14 * s),
                       fill(with_alpha(0xFF2A2A2A, 0.55)))
    for dx in (-90, 90):
        c.drawLine(dx * s, 40 * s, dx * 1.4 * s, 100 * s, stroke(0xFF707680, 8 * s))
    c.restore()


def bars(c, items, lt, y0=1700, maxh=520):
    n = len(items)
    for i, (lab, val, ref, col) in enumerate(items):
        x = W / 2 + (i - (n - 1) / 2) * 300
        k = ease_out(clamp((lt - 0.2 - 0.25 * i) / 0.9))
        hgt = maxh * val / ref * k
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 90, y0 - hgt, 180, hgt), 16, 16), fill(col))
        draw_text(c, lab, x, y0 + 60, 40, WHITE)


def s_titan(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020308)
    if sid in ("h", "s1"):
        ST.draw(c, t, camx=t * 10, alpha=0.9)
        R0 = lerp(260, 470, ease_out(clamp(t / 3.0)))
        if sid == "h":
            saturn(c, W * 0.86, 560, 230, t)
            titan(c, W / 2 - 40, 1210, R0, t)
            hc.stamp(c, "LLUEVE METANO", W / 2, 1780, lt, 1.3, 88, col=0xFFE07A10)
        else:
            k = ease_in_out(clamp((lt - 0.4) / 1.8))
            titan(c, W / 2, 1180, 470, t, haze=1 - 0.8 * k)
            K.tag(c, W / 2, 1760, "−179 °C", lt - 0.5, accent=V["accent"], size=48)
    elif sid == "s2":
        titan_land(c, t, rain=ease_out(clamp(lt / 1.2)))
        K.tag(c, W / 2, 1640, "LAGOS DE METANO Y ETANO", lt - 0.4, accent=V["accent"], size=36)
    elif sid == "s3":
        titan_land(c, t, rain=0.3)
        y = lerp(600, 1250, ease_in_out(clamp(lt / 3.2)))
        huygens(c, W / 2, y, 0.9, t)
        hc.big(c, "14 / 1 / 2005", W / 2, 1700, 110, V["accent"], lt, 0.4)
        K.tag(c, W / 2, 1830, "SONDA HUYGENS (ESA)", lt - 0.8, accent=WHITE, size=34)
    elif sid == "s4":
        c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF1A0E06, 0xFF3A2410])))
        bars(c, [("GRAVEDAD", 14, 100, 0xFF7AB8FF), ("PRESIÓN", 150, 150, V["accent"])], lt, y0=1450, maxh=560)
        draw_text(c, "14%", W / 2 - 150, 1450 - 560 * 0.14 * ease_out(clamp((lt - 0.2) / 0.9)) - 30, 64, WHITE)
        draw_text(c, "×1,5", W / 2 + 150, 1450 - 560 * ease_out(clamp((lt - 0.45) / 0.9)) - 30, 64, WHITE)
        K.tag(c, W / 2, 1640, "RESPECTO A LA TIERRA", lt - 1.0, accent=WHITE, size=34)
    elif sid == "s5":
        titan_land(c, t, rain=0.0)
        dragonfly(c, lerp(-200, W / 2, ease_out(clamp(lt / 2.0))), 900, 1.1, t)
        hc.big(c, "DRAGONFLY", W / 2, 1640, 110, V["accent"], lt, 0.6)
        K.tag(c, W / 2, 1780, "NASA · LANZAMIENTO PREVISTO 2028", lt - 1.0, accent=WHITE, size=32)
    else:
        ST.draw(c, t, camx=t * 10, alpha=0.9)
        titan(c, W / 2, 1180, 420, t)


V601 = dict(slug="601_titan_lluvia_metano", accent=0xFFFFA43A, drone=0.035, scene=s_titan, tease="LO PROMETIDO",
            send="ENVÍASELO A QUIEN LE GUSTE EL ESPACIO", rehook=("s4", "Y AQUÍ PODRÍAS VOLAR"),
            reveal=("s4", "LO MÁS LOCO"), segs=[
    dict(id="h", who="nar", say="En esta luna llueve. Pero no agua: llueve metano.",
         cap="En esta luna *llueve*… | pero no agua: | llueve *METANO*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Es Titán, la luna más grande de Saturno. A ciento setenta y nueve bajo cero, y con una atmósfera tan espesa que tapa el suelo.",
         cap="Es *Titán*, de Saturno: | *−179 °C* y una atmósfera | tan espesa que tapa el suelo"),
    dict(id="s2", who="nar", cut=True, say="Ahí abajo hay ríos, lagos y mares. De metano líquido. Como la Tierra, pero al revés.",
         cap="Hay *ríos*, *lagos* y *mares*… | de metano líquido. | Como la *Tierra*, pero al revés"),
    dict(id="s3", who="nar", cut=True, say="En dos mil cinco, la sonda Huygens bajó en paracaídas y aterrizó allí. Es lo más lejos que hemos aterrizado nunca.",
         cap="En *2005* la sonda *Huygens* | aterrizó allí: lo más | *LEJOS* que hemos llegado"),
    dict(id="s4", who="nar", cut=True, say="Y lo más loco: la gravedad es muy baja y el aire es tan denso, que con unas alas en los brazos, una persona podría volar.",
         cap="Gravedad muy baja, aire *denso*… | con alas en los brazos | podrías *VOLAR*"),
    dict(id="s5", who="nar", cut=True, say="Por eso la NASA mandará un dron volador, Dragonfly. Su lanzamiento está previsto en dos mil veintiocho.",
         cap="La NASA mandará un *dron*: | *Dragonfly*, lanzamiento | previsto en *2028*"),
    dict(id="cta", who="nar", cut=True, say="¿Irías a Titán, aunque no pudieras volver? Comenta sí o no. Y sígueme: el próximo es Saturno.",
         cap="¿Irías a *Titán*? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 602 Mito de clase: Einstein no suspendió matemáticas
def paper(c, t):
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, H / 2), 1300, [0xFF3A2A1C, 0xFF140E08])))


def chalkboard(c, t, lt, eqs, k=1.0):
    r = skia.Rect.MakeXYWH(60, 640, W - 120, 1000)
    c.drawRRect(skia.RRect.MakeRectXY(r.makeOffset(0, 14), 20, 20), fill(0x88000000))
    c.drawRRect(skia.RRect.MakeRectXY(r, 20, 20), fill(0xFF6A4A2A))
    c.drawRect(skia.Rect.MakeXYWH(90, 670, W - 180, 940), skia.Paint(Shader=skia.GradientShader.MakeRadial(
        (W / 2, 1100), 800, [0xFF2E4A3A, 0xFF1A2E24])))
    for i, e in enumerate(eqs):
        p = clamp((lt - 0.3 - i * 0.7) / 0.6) * k
        if p <= 0:
            continue
        f = font(76, K.TF_BOLD)
        n = max(1, int(len(e) * p))
        c.drawString(e[:n], 150, 820 + i * 190, f, fill(with_alpha(0xFFF4F1E6, 0.92)))
    for i in range(30):
        R = random.Random(i)
        c.drawCircle(R.uniform(100, W - 100), R.uniform(680, 1600), R.uniform(1, 3), fill(with_alpha(WHITE, 0.08)))


def certificate(c, t, lt, hl=-1):
    c.save(); c.translate(W / 2, 1200); c.rotate(-2 + math.sin(t * 0.6) * 0.8)
    r = skia.Rect.MakeXYWH(-420, -560, 840, 1120)
    c.drawRect(r.makeOffset(16, 22), fill(0x88000000))
    c.drawRect(r, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, -560), (0, 560)], [0xFFF2E6C8, 0xFFE0CFA4])))
    c.drawRect(r.makeInset(24, 24), stroke(0xFF8A6A3A, 4))
    draw_text(c, "MATURA · AARAU 1896", 0, -440, 44, 0xFF3A2A1A, shadow=False)
    draw_text(c, "Albert Einstein", 0, -360, 52, 0xFF1A1A3A, tf=K.TF_BOLD, shadow=False)
    rows = [("Álgebra", "6"), ("Geometría", "6"), ("Geometría descriptiva", "6"), ("Física", "5-6"), ("Francés", "3")]
    for i, (sub, g) in enumerate(rows):
        y = -220 + i * 120
        a = clamp((lt - 0.3 - i * 0.35) / 0.3)
        if a <= 0:
            continue
        f = font(46, K.TF_BOLD)
        c.drawString(sub, -350, y, f, fill(with_alpha(0xFF2A2A2A, a)))
        col = 0xFF1A7A3A if g.startswith(("6", "5")) else 0xFFB02A2A
        c.drawString(g, 270, y, font(56), fill(with_alpha(col, a)))
        c.drawLine(-350, y + 22, 350, y + 22, stroke(with_alpha(0xFF8A6A3A, 0.4 * a), 2))
        if i == hl or (hl == 9 and i < 3):
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-370, y - 62, 740, 92), 20, 20),
                        stroke(with_alpha(0xFFFF3B4A, 0.6 + 0.4 * math.sin(t * 8)), 7))
    draw_text(c, "escala: 6 = la MÁXIMA", 0, 420, 40, 0xFF6A4A2A, shadow=False)
    c.restore()


def newspaper(c, t, lt, k=1.0):
    c.save(); c.translate(W / 2, 1180); c.rotate(lerp(30, -4, ease_out(clamp(lt / 0.6)))); s = ease_back(clamp(lt / 0.6), 1.8)
    c.scale(s, s)
    r = skia.Rect.MakeXYWH(-430, -500, 860, 1000)
    c.drawRect(r.makeOffset(16, 20), fill(0x88000000))
    c.drawRect(r, fill(0xFFE9E3D2))
    draw_text(c, "RIPLEY'S", 0, -380, 96, 0xFF1A1A1A, shadow=False)
    draw_text(c, "BELIEVE IT OR NOT!", 0, -300, 46, 0xFFB02A2A, shadow=False)
    c.drawLine(-380, -260, 380, -260, stroke(0xFF1A1A1A, 5))
    draw_text(c, "«El mayor matemático vivo", 0, -150, 44, 0xFF1A1A1A, tf=K.TF_BOLD, shadow=False)
    draw_text(c, "SUSPENDIÓ matemáticas»", 0, -90, 50, 0xFF1A1A1A, shadow=False)
    for i in range(9):
        c.drawRect(skia.Rect.MakeXYWH(-380, 0 + i * 48, 760 - (i % 3) * 120, 18), fill(0xFFB8B2A2))
    draw_text(c, "1935", 300, 440, 60, 0xFFB02A2A, shadow=False)
    c.restore()


def s_einstein(c, t, P, V):
    sid, lt = seg(P, t)
    paper(c, t)
    if sid == "h":
        chalkboard(c, t, lt + 1.5, ["∫ x² dx = x³/3", "E = mc²", "d/dx (sen x) = cos x"])
        hc.stamp(c, "FALSO", W / 2, 1760, lt, 1.0, 130, col=RED)
    elif sid == "s1":
        newspaper(c, t, lt)
    elif sid == "s2":
        newspaper(c, t, 2.0)
        if lt > 0.6:
            hc.stamp(c, "MENTIRA", W / 2, 1300, lt, 0.6, 120, col=RED)
    elif sid == "s3":
        chalkboard(c, t, lt, ["∫ f(x) dx", "dy/dx", "lím  x→0"])
        hc.big(c, "ANTES DE LOS 15", W / 2, 1760, 100, V["accent"], lt, 0.5)
    elif sid == "s4":
        certificate(c, t, lt, hl=9 if lt > 2.0 else -1)
    elif sid == "s5":
        certificate(c, t, 3.0, hl=-1)
        c.drawPaint(fill(0x88000000))
        k = ease_out(clamp(lt / 0.6))
        draw_text(c, "6 = TU 10", W / 2, 1150, 150 * k + 1, V["accent"])
        K.tag(c, W / 2, 1360, "EN SUIZA 6 ERA LA MEJOR NOTA", lt - 0.6, accent=WHITE, size=38)
    else:
        chalkboard(c, t, 5, ["∫ x² dx = x³/3", "E = mc²"])


V602 = dict(slug="602_einstein_no_suspendio", accent=0xFF5AD0FF, drone=0.025, scene=s_einstein, tease="TE LO ENSEÑARON MAL",
            rehook=("s4", "MIRA SUS NOTAS REALES"), reveal=("s4", "SUS NOTAS"), segs=[
    dict(id="h", who="nar", say="Einstein nunca suspendió matemáticas. Es un bulo de hace casi cien años.",
         cap="Einstein *NUNCA* suspendió | matemáticas. Es un *bulo*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="En mil novecientos treinta y cinco, la columna Ripley's publicó que el mayor matemático vivo había suspendido matemáticas.",
         cap="En *1935*, la columna *Ripley's* | publicó que había | *suspendido* mates"),
    dict(id="s2", who="nar", cut=True, say="Se lo enseñaron al propio Einstein. Y lo negó: dijo que nunca había suspendido.",
         cap="Se lo enseñaron a Einstein… | y lo *NEGÓ*", hold=0.2),
    dict(id="s3", who="nar", cut=True, say="Contó que, antes de los quince años, ya dominaba el cálculo diferencial e integral.",
         cap="Antes de los *15* ya | dominaba el cálculo | *diferencial e integral*"),
    dict(id="s4", who="nar", cut=True, say="Y sus notas lo confirman: en su examen final de mil ochocientos noventa y seis sacó un seis en álgebra y en geometría.",
         cap="Notas de *1896*: | un *6* en álgebra | y en *geometría*"),
    dict(id="s5", who="nar", cut=True, say="Y en esa escuela suiza, el seis era la nota máxima. El bulo leyó la escala al revés.",
         cap="En Suiza, el *6* era | la nota *MÁXIMA*. | Se leyó *al revés*"),
    dict(id="cta", who="nar", cut=True, say="¿A ti te contaron este mito? Comenta sí o no. Y sígueme para más mitos que te tragaste en clase.",
         cap="¿Te contaron este mito? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 603 Mito de animales: pájaro tocado
def garden(c, t):
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF8FC8F0, 0xFFCFE8F4, 0xFF6AA05A])))
    for k in range(3):
        y = 1450 + k * 90
        p = skia.Path(); p.moveTo(0, H)
        for x in range(0, W + 30, 30):
            p.lineTo(x, y + 30 * math.sin(x * 0.01 + k) + 8 * math.sin(x * 0.07 + t))
        p.lineTo(W, H); p.close()
        c.drawPath(p, fill([0xFF5A9A4A, 0xFF4A8A3A, 0xFF3A7A2E][k]))
    # rama
    c.drawLine(-50, 760, W + 50, 700, stroke(0xFF5A3A1E, 46))
    for i in range(12):
        R = random.Random(i)
        x = R.uniform(0, W)
        y = 730 - x * 0.055
        c.drawOval(skia.Rect.MakeXYWH(x - 40, y - 70 + math.sin(t * 2 + i) * 4, 80, 50), fill(0xFF4E9A3A))


def bird(c, x, y, s, t, flap=0.0, chick=False, beak_open=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    body_c = [0xFFB8865A, 0xFF7A5232] if not chick else [0xFFD8C08A, 0xFF9A8250]
    c.drawOval(skia.Rect.MakeXYWH(-120, -80, 240, 170), skia.Paint(Shader=skia.GradientShader.MakeRadial((-30, -40), 220, body_c), AntiAlias=True))
    c.drawOval(skia.Rect.MakeXYWH(-60, -20, 140, 100), fill(0xFFF0D8B0 if not chick else 0xFFF4E4C0))  # pecho
    c.drawCircle(85, -95, 70, skia.Paint(Shader=skia.GradientShader.MakeRadial((70, -120), 90, body_c), AntiAlias=True))
    if chick:
        for k in range(6):
            a = -2.2 + k * 0.35
            c.drawLine(85 + math.cos(a) * 60, -95 + math.sin(a) * 60, 85 + math.cos(a) * 82, -95 + math.sin(a) * 82, stroke(0xFFE8D8A8, 5))
    c.drawCircle(108, -110, 13, fill(0xFF101010)); c.drawCircle(112, -114, 4, fill(WHITE))
    bo = 14 * beak_open
    up = skia.Path(); up.moveTo(140, -100 - bo); up.lineTo(205, -88 - bo * 0.3); up.lineTo(140, -78); up.close()
    lo = skia.Path(); lo.moveTo(140, -78); lo.lineTo(195, -76 + bo); lo.lineTo(140, -64 + bo * 0.5); lo.close()
    bc = 0xFFF2C21A if chick else 0xFFE89A2A
    c.drawPath(up, fill(bc)); c.drawPath(lo, fill(bc))
    wa = -40 * flap
    c.save(); c.translate(-20, -30); c.rotate(wa)
    wing = skia.Path(); wing.moveTo(0, 0); wing.cubicTo(-60, -20, -170, 10, -190, 70); wing.cubicTo(-120, 60, -40, 70, 20, 40); wing.close()
    c.drawPath(wing, fill(0xFF6A4428 if not chick else 0xFFB8A070))
    c.restore()
    if not chick:
        tail = skia.Path(); tail.moveTo(-110, 0); tail.lineTo(-210, 40); tail.lineTo(-200, 70); tail.lineTo(-100, 40); tail.close()
        c.drawPath(tail, fill(0xFF6A4428))
    c.restore()


def nest(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-260, -60, 520, 170), fill(0xFF6A4A26))
    R = random.Random(9)
    for i in range(60):
        a = R.uniform(0, 3.14)
        x1, y1 = -250 + R.uniform(0, 500), R.uniform(-40, 90)
        c.drawLine(x1, y1, x1 + math.cos(a) * 90, y1 + math.sin(a) * 20, stroke(R.choice([0xFF8A6A3A, 0xFF5A3A1A, 0xFFA8884A]), 6))
    c.restore()


def s_pajaro(c, t, P, V):
    sid, lt = seg(P, t)
    garden(c, t)
    if sid == "h":
        nest(c, W / 2, 1300, 1.2)
        bird(c, W / 2, 1180, 1.3, t, chick=True, beak_open=0.5 + 0.5 * math.sin(t * 9))
        hc.stamp(c, "MITO", W / 2, 1720, lt, 1.0, 140, col=RED)
    elif sid == "s1":
        bird(c, W / 2, 1450, 1.2, t, chick=True, beak_open=0.3 * (1 + math.sin(t * 7)))
        # mano que se acerca (dedos reales)
        y = lerp(2300, 1720, ease_out(clamp(lt / 1.6)))
        hc.finger(c, W / 2 - 70, y, -4, 300, 82)
        hc.finger(c, W / 2 + 30, y + 20, 3, 320, 84)
        K.tag(c, W / 2, 900, "«SU MADRE LO RECHAZARÁ»", lt - 0.4, accent=V["accent"], size=40)
    elif sid == "s2":
        # olfato pobre: nariz tachada, ojos y oídos sí
        bird(c, W / 2, 1150, 1.6, t, flap=0.3 * math.sin(t * 3))
        k = ease_back(clamp((lt - 0.4) / 0.4), 2)
        for i, (lab, ok) in enumerate((("VISTA", True), ("OÍDO", True), ("OLFATO", False))):
            x = W / 2 + (i - 1) * 320
            a = clamp((lt - 0.4 - 0.35 * i) / 0.3)
            if a <= 0:
                continue
            c.drawCircle(x, 1640, 110 * k, fill(with_alpha(GREEN if ok else RED, 0.9 * a)))
            draw_text(c, "✓" if ok else "✗", x, 1675, 110, WHITE)
            draw_text(c, lab, x, 1810, 40, WHITE)
    elif sid == "s3":
        nest(c, W / 2, 1450, 1.2)
        bird(c, W / 2 - 60, 1330, 1.0, t, chick=True, beak_open=0.5 + 0.5 * math.sin(t * 10))
        bird(c, W / 2 + 120, 1350, 0.9, t + 1, chick=True, beak_open=0.5 + 0.5 * math.sin(t * 11))
        px = lerp(W + 300, W / 2 + 40, ease_out(clamp(lt / 1.4)))
        bird(c, px, lerp(700, 1150, ease_out(clamp(lt / 1.4))), 1.1, t, flap=math.sin(t * 18) if lt < 1.4 else 0.1, beak_open=0.4)
        K.tag(c, W / 2, 1700, "VUELVE IGUAL", lt - 1.3, accent=V["accent"], size=48)
    elif sid == "s4":
        nest(c, W / 2 + 200, 1000, 0.8)
        bird(c, W / 2 - 180, 1500 + abs(math.sin(t * 3)) * -40, 1.0, t, chick=True, flap=0.5 * abs(math.sin(t * 3)))
        K.tag(c, W / 2, 1780, "SI TIENE PLUMAS: DÉJALO", lt - 0.4, accent=V["accent"], size=40)
        K.tag(c, W / 2 + 200, 1150, "SIN PLUMAS: AL NIDO", lt - 1.4, accent=WHITE, size=32)
    else:
        nest(c, W / 2, 1300, 1.2)
        bird(c, W / 2, 1180, 1.3, t, chick=True, beak_open=0.5 + 0.5 * math.sin(t * 9))


V603 = dict(slug="603_mito_pajaro_tocado", accent=0xFFFF8A2A, drone=0.02, scene=s_pajaro, tease="CASI TODOS LO CREEN",
            send="ENVÍASELO A QUIEN SE LO CREÍA", rehook=("s3", "MIRA LO QUE HACE LA MADRE"), reveal=("s3", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="Si tocas a un pajarito caído, su madre no lo va a abandonar. Es un mito.",
         cap="Si tocas a un pajarito, | su madre *NO* lo abandona. | Es un *MITO*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Seguro que te dijeron que, si lo tocas, la madre olerá tu olor y lo rechazará.",
         cap="Te dijeron que la madre | olería tu *olor* | y lo *rechazaría*"),
    dict(id="s2", who="nar", cut=True, say="Pero la mayoría de los pájaros apenas usan el olfato para reconocer a sus crías. Las reconocen por la vista y por el sonido.",
         cap="La mayoría de pájaros | casi no usan el *olfato*: | reconocen por *vista* y *sonido*"),
    dict(id="s3", who="nar", cut=True, say="Según el Laboratorio de Ornitología de Cornell, los padres no abandonan a una cría por que la toque una persona.",
         cap="Ornitología de *Cornell*: | los padres *NO* la abandonan | por tocarla"),
    dict(id="s4", who="nar", cut=True, say="Eso sí: si ya tiene plumas y salta por el suelo, déjalo. Está aprendiendo a volar, y sus padres están cerca.",
         cap="Si ya tiene *plumas* y salta, | *DÉJALO*: está aprendiendo | y sus padres están cerca"),
    dict(id="cta", who="nar", cut=True, say="¿Tú te lo creías? Comenta sí o no. Y sígueme para otro mito de animales.",
         cap="¿Te lo creías? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 604 Saturno se queda sin anillos
def ring_rain(c, x, y, R, t, k=1.0):
    Rr = random.Random(7)
    for i in range(140):
        side = 1 if i % 2 else -1
        ph = (t * 0.35 + Rr.random()) % 1.0
        r0 = R * Rr.uniform(1.3, 2.1)
        lat = Rr.uniform(0.55, 0.8)
        sx, sy = x + side * r0, y + Rr.uniform(-8, 8)
        ex, ey = x + side * R * math.cos(lat), y - R * math.sin(lat) * (1 if i % 4 < 2 else -1)
        cx, cy = x + side * r0 * 0.8, (sy + ey) / 2 - (ey - sy) * 0.2
        u = ph
        px = (1 - u) ** 2 * sx + 2 * (1 - u) * u * cx + u * u * ex
        py = (1 - u) ** 2 * sy + 2 * (1 - u) * u * cy + u * u * ey
        c.drawCircle(px, py, 4.5, skia.Paint(AntiAlias=True, Color=with_alpha(0xFFBFE6FF, 0.75 * k * (1 - u * 0.5)), MaskFilter=blur(2)))


def pool(c, x, y, frac, t):
    c.save(); c.translate(x, y)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-330, -120, 660, 240), 18, 18), fill(0xFFE8EEF4))
    inner = skia.Rect.MakeXYWH(-300, -95, 600, 190)
    c.drawRect(inner, fill(0xFF5A6A7A))
    hgt = 190 * clamp(frac)
    c.drawRect(skia.Rect.MakeXYWH(-300, 95 - hgt, 600, hgt), fill(0xFF3AA8E8))
    for k in range(1, 8):
        c.drawLine(-300 + k * 75, -95, -300 + k * 75, 95, stroke(with_alpha(WHITE, 0.6), 3))
    c.restore()


def s_saturno(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF02030A)
    ST.draw(c, t, camx=t * 8, alpha=0.9)
    if sid == "h":
        R = lerp(320, 260, ease_out(clamp(t / 2.5)))
        a = clamp(1 - (lt - 1.2) / 1.6) if lt > 1.2 else 1.0
        P33.saturn_ring(c, W / 2, 1150, R, front=False, alpha=a)
        S.draw_planet(c, W / 2, 1150, R, S.render(2 * R, SAT, spin=t * 0.1, light=L0, ambient=0.05, gain=1.15))
        P33.saturn_ring(c, W / 2, 1150, R, front=True, alpha=a)
        hc.stamp(c, "SIN ANILLOS", W / 2, 1750, lt, 1.6, 110, col=RED)
    elif sid in ("s1", "s2"):
        R = 260
        saturn(c, W / 2, 1150, R, t)
        ring_rain(c, W / 2, 1150, R, t, k=ease_out(clamp(lt / 0.8)))
        if sid == "s1":
            K.tag(c, W / 2, 1720, "«LLUVIA DE ANILLO» · NASA 2018", lt - 0.5, accent=V["accent"], size=36)
        else:
            pool(c, W / 2, 1700, (lt % 2.2) / 2.2, t)
            hc.timer(c, W / 2 + 400, 1530, 60, (lt % 2.2) / 2.2, "30'", V["accent"])
            K.tag(c, W / 2, 1880, "UNA PISCINA OLÍMPICA CADA 30 MIN", lt - 0.6, accent=WHITE, size=32)
    elif sid == "s3":
        R = 260
        a = 1 - 0.85 * ease_in_out(clamp(lt / 3.0))
        P33.saturn_ring(c, W / 2, 1150, R, front=False, alpha=a)
        S.draw_planet(c, W / 2, 1150, R, S.render(2 * R, SAT, spin=t * 0.1, light=L0, ambient=0.05, gain=1.15))
        P33.saturn_ring(c, W / 2, 1150, R, front=True, alpha=a)
        K.counter(c, t, lt - 0.3, lambda p: f"{int(round(300 * p))} MILLONES", "DE AÑOS (COMO MUCHO)", V["accent"], y=1720, size=100)
    elif sid == "s4":
        # línea temporal: dinosaurios vs edad de los anillos
        y = 1150
        c.drawLine(100, y, W - 100, y, stroke(WHITE, 8))
        def px(my):
            return lerp(W - 100, 100, my / 250)
        k = ease_out(clamp(lt / 1.0))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(px(230), y - 120, px(66), y - 30), 14, 14), fill(with_alpha(0xFF6ACB5A, k)))
        draw_text(c, "DINOSAURIOS", (px(230) + px(66)) / 2, y - 160, 44, 0xFF9AEB8A)
        k2 = ease_out(clamp((lt - 1.2) / 1.0))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(px(100) , y + 30, lerp(px(100), px(0), k2), y + 120), 14, 14), fill(V["accent"]))
        if k2 > 0:
            draw_text(c, "ANILLOS: ¿<100 M AÑOS?", W / 2 + 150, y + 210, 44, V["accent"])
        draw_text(c, "HACE 250 M", 210, y + 300, 34, WHITE); draw_text(c, "HOY", W - 150, y + 300, 34, WHITE)
        R = 170
        S.draw_planet(c, W / 2, 620, R, S.render(2 * R, SAT, spin=t * 0.1, light=L0, ambient=0.05, gain=1.15))
    else:
        saturn(c, W / 2, 1150, 260, t)


V604 = dict(slug="604_saturno_sin_anillos", accent=0xFFF2C77A, drone=0.03, scene=s_saturno, tease="NO DURARÁ PARA SIEMPRE",
            send="ENVÍASELO A QUIEN LE GUSTE EL ESPACIO", rehook=("s4", "Y LO MÁS RARO VIENE AHORA"), segs=[
    dict(id="h", who="nar", say="Saturno se está quedando sin anillos. Y la NASA ya ha calculado cuándo.",
         cap="Saturno se está | quedando *SIN ANILLOS*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Los anillos son trozos de hielo. Y Saturno se los está tragando: caen sobre el planeta como una lluvia.",
         cap="Son trozos de *hielo*… | y Saturno se los *traga*: | caen como *lluvia*"),
    dict(id="s2", who="nar", cut=True, say="Un estudio de la NASA de dos mil dieciocho calculó que cae tanta agua, que llenaría una piscina olímpica cada media hora.",
         cap="*NASA, 2018*: cae agua | para llenar una *piscina* | *olímpica* cada media hora"),
    dict(id="s3", who="nar", cut=True, say="A ese ritmo, los anillos desaparecerían en unos trescientos millones de años, como mucho.",
         cap="A ese ritmo, *desaparecen* | en unos *300 millones* | de años"),
    dict(id="s4", who="nar", cut=True, say="Y lo más raro: según la sonda Cassini, los anillos podrían ser más jóvenes que los dinosaurios. Puede que los primeros dinosaurios vivieran con un Saturno sin anillos.",
         cap="Cassini: los anillos podrían | ser más *jóvenes* que los | *DINOSAURIOS*"),
    dict(id="cta", who="nar", cut=True, say="¿Sabías que Saturno no siempre tuvo anillos? Comenta sí o no. Y sígueme para más secretos del espacio.",
         cap="¿Lo sabías? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 605 3 cosas que hace tu cuerpo cuando tienes frío
def snow(c, t, k=1.0):
    R = random.Random(5)
    for i in range(140):
        x = (R.uniform(0, W) + math.sin(t * 0.8 + i) * 30) % W
        y = (R.uniform(0, H) + t * R.uniform(60, 140)) % H
        c.drawCircle(x, y, R.uniform(3, 8), skia.Paint(AntiAlias=True, Color=with_alpha(WHITE, 0.6 * k), MaskFilter=blur(1.5)))


def thermo(c, x, y, temp, t):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 40, y - 520, 80, 560), 40, 40), fill(0xFFE8EEF4))
    c.drawCircle(x, y + 40, 80, fill(0xFFE8EEF4))
    hgt = 480 * clamp((temp + 10) / 50)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 22, y - hgt, 44, hgt + 40), 22, 22), fill(0xFF3A8AFF if temp < 10 else 0xFFFF4A3A))
    c.drawCircle(x, y + 40, 60, fill(0xFF3A8AFF if temp < 10 else 0xFFFF4A3A))
    for k in range(9):
        c.drawLine(x + 46, y - 40 - k * 55, x + 76, y - 40 - k * 55, stroke(0xFF8A9AAA, 4))


def muscle(c, cx, cy, t, shake):
    for i in range(9):
        x = cx - 320 + i * 80 + math.sin(t * 70 + i * 1.7) * 9 * shake
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 30, cy - 330, 60, 660), 30, 30)
        c.drawRRect(r, skia.Paint(Shader=skia.GradientShader.MakeLinear([(x - 30, 0), (x + 30, 0)], [0xFF8A1A2A, 0xFFE05A6A, 0xFF8A1A2A]), AntiAlias=True))
        for k in range(14):
            c.drawLine(x - 24, cy - 300 + k * 46, x + 24, cy - 300 + k * 46, stroke(with_alpha(0xFFFFB0B8, 0.35), 3))
    if shake > 0:
        for k in range(6):
            yy = (cy - 380 - (t * 160 + k * 70) % 420)
            p = skia.Path(); p.moveTo(cx - 300 + k * 120, yy)
            for j in range(8):
                p.lineTo(cx - 300 + k * 120 + math.sin(j + t * 6) * 14, yy - j * 18)
            c.drawPath(p, stroke(with_alpha(0xFFFF9A3A, 0.6 * shake), 6))


def vessel(c, cx, cy, wdt, t, label=None):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 420, cy - wdt / 2 - 18, 840, wdt + 36), 40, 40), fill(0xFFE8A0A0))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 420, cy - wdt / 2, 840, wdt), 30, 30), fill(0xFF7A0A1A))
    R = random.Random(2)
    for i in range(int(wdt / 6)):
        x = cx - 400 + ((R.uniform(0, 800) + t * 300 * (60 / max(20, wdt))) % 800)
        y = cy + R.uniform(-wdt / 2 + 14, wdt / 2 - 14)
        c.drawOval(skia.Rect.MakeXYWH(x - 16, y - 10, 32, 20), fill(0xFFD02A3A))


def s_frio(c, t, P, V):
    sid, lt = seg(P, t)
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF0A1A3A, 0xFF1A3A6A, 0xFF4A7AAA])))
    snow(c, t)
    if sid == "h":
        thermo(c, W / 2, 1450, lerp(30, -5, ease_in_out(clamp(t / 2.5))), t)
        hc.stamp(c, "3 COSAS", W / 2, 1760, lt, 1.0, 120, col=0xFF3A8AFF)
    elif sid == "s1":
        muscle(c, W / 2, 1200, t, ease_out(clamp((lt - 0.5) / 0.4)))
        hc.big(c, "1", 150, 780, 150, V["accent"], lt, 0.0)
        K.tag(c, W / 2, 1700, "TIRITAR = CALEFACCIÓN", lt - 0.8, accent=V["accent"], size=44)
    elif sid == "s2":
        k = ease_in_out(clamp((lt - 0.6) / 1.6))
        vessel(c, W / 2, 1050, lerp(200, 70, k), t)
        hc.big(c, "2", 150, 780, 150, V["accent"], lt, 0.0)
        c.save(); c.translate(0, 120)
        hc.finger(c, W / 2 - 120, 1560, -8, 260, 80)
        hc.finger(c, W / 2, 1540, 0, 290, 84)
        hc.finger(c, W / 2 + 120, 1560, 8, 260, 80)
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - 200, 1180, 400, 240), skia.Paint(Color=with_alpha(0xFF3A8AFF, 0.35 * k), BlendMode=skia.BlendMode.kSrcATop))
        c.restore()
        K.tag(c, W / 2, 1830, "MANOS Y PIES FRÍOS = ÓRGANOS A SALVO", lt - 1.0, accent=WHITE, size=32)
    elif sid == "s3":
        hc.big(c, "3", 150, 780, 150, V["accent"], lt, 0.0)
        # gota que se llena
        k = clamp(lt / 3.0)
        c.save(); c.translate(W / 2, 1200)
        drop = skia.Path(); drop.moveTo(0, -330); drop.cubicTo(120, -150, 230, 0, 230, 90); drop.cubicTo(230, 240, 120, 320, 0, 320)
        drop.cubicTo(-120, 320, -230, 240, -230, 90); drop.cubicTo(-230, 0, -120, -150, 0, -330); drop.close()
        c.drawPath(drop, stroke(WHITE, 10))
        c.save(); c.clipPath(drop, doAntiAlias=True)
        lvl = lerp(320, -330, k)
        wave = skia.Path(); wave.moveTo(-260, 400)
        for x in range(-260, 270, 20):
            wave.lineTo(x, lvl + math.sin(x * 0.03 + t * 5) * 10)
        wave.lineTo(260, 400); wave.close()
        c.drawPath(wave, fill(0xFFF2D23A))
        c.restore(); c.restore()
        K.tag(c, W / 2, 1700, "DIURESIS POR FRÍO", lt - 0.6, accent=V["accent"], size=44)
    else:
        thermo(c, W / 2, 1450, -5, t)


V605 = dict(slug="605_3_cosas_frio", accent=0xFF7AD8FF, drone=0.025, scene=s_frio, tease="LA 3 TE HA PASADO SEGURO",
            send="ENVÍASELO A QUIEN SIEMPRE TIENE FRÍO", rehook=("s3", "Y LA 3 ES LA MÁS RARA"), reveal=("s3", "LA MÁS RARA"), segs=[
    dict(id="h", who="nar", say="Tres cosas que hace tu cuerpo cuando tienes frío. La tercera te ha pasado seguro.",
         cap="*3 cosas* que hace tu cuerpo | cuando tienes *FRÍO*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Uno: tiritas. Tus músculos se contraen sin parar, muy rápido, solo para fabricar calor.",
         cap="*UNO*: tiritas. Tus músculos | se contraen sin parar | para fabricar *calor*"),
    dict(id="s2", who="nar", cut=True, say="Dos: se te enfrían las manos y los pies. Tu cuerpo estrecha esos vasos sanguíneos, para guardar el calor en los órganos.",
         cap="*DOS*: manos y pies fríos. | Tu cuerpo cierra esos vasos | para salvar los *órganos*"),
    dict(id="s3", who="nar", cut=True, say="Y tres: te entran ganas de ir al baño. Al cerrar esos vasos, la sangre se concentra dentro, y los riñones fabrican más orina. Se llama diuresis por frío.",
         cap="*TRES*: ganas de ir al *BAÑO*. | La sangre va hacia dentro | y los riñones hacen más orina"),
    dict(id="cta", who="nar", cut=True, say="¿Eres de los que siempre tiene frío? Comenta sí o no. Y sígueme para la próxima lista.",
         cap="¿Siempre tienes frío? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== Ilusiones T4: fondo común
SERIE = "ILUSIONES IMPOSIBLES T4 · PARTE {}/3"


def ilu_bg(c, t, seed):
    hc.aurora(c, t, 0xFF1A2A6A, 0xFF4A1A5A, seed=seed)


# ====================================================================== 606 T4 P1: serpientes rotatorias (Kitaoka 2003)
SNAKE_COLS = [0xFF000000, 0xFF1F4FC8, 0xFFFFFFFF, 0xFFF2D21A]  # negro, azul, blanco, amarillo (deriva periférica)


def snake_disc(c, x, y, R, rings=5, n=24, rev=False):
    c.drawCircle(x, y, R + 6, fill(0xFF2A2A2A))
    for r in range(rings, 0, -1):
        rr = R * r / rings
        rin = R * (r - 1) / rings
        m = max(8, int(n * r / rings))
        for i in range(m):
            a0 = 360 * i / m
            step = 360 / m / 4
            for j, col in enumerate(SNAKE_COLS if (r % 2 == 0) != rev else SNAKE_COLS[::-1]):
                p = skia.Path()
                p.addArc(skia.Rect.MakeXYWH(x - rr, y - rr, 2 * rr, 2 * rr), a0 + j * step, step + 0.6)
                p.arcTo(skia.Rect.MakeXYWH(x - rin, y - rin, 2 * rin, 2 * rin), a0 + (j + 1) * step + 0.6, -step - 0.6, False)
                p.close()
                c.drawPath(p, skia.Paint(AntiAlias=True, Color=col))


def snakes(c, t, cy=1230, sc=1.0):
    R = 215 * sc
    for i, (dx, dy) in enumerate(((-230, -230), (230, -230), (-230, 230), (230, 230))):
        snake_disc(c, W / 2 + dx * sc, cy + dy * sc, R, rev=(i % 3 == 0))


def s_serpientes(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 606)
    panel = skia.Rect.MakeXYWH(40, 700, W - 80, 1060)
    c.drawRRect(skia.RRect.MakeRectXY(panel, 40, 40), fill(0xFF6A6A6A))
    if sid == "s3":
        # demostración: tapa casi todo y deja un disco: al mirarlo fijo, se para
        snakes(c, t)
        c.drawRRect(skia.RRect.MakeRectXY(panel, 40, 40), fill(with_alpha(0xFF101010, 0.82 * ease_out(clamp(lt / 0.6)))))
        snake_disc(c, W / 2 - 230, 1000, 215)
        c.drawCircle(W / 2 - 230, 1000, 16, fill(RED))
        K.tag(c, W / 2, 1600, "MIRA EL PUNTO ROJO: SE PARA", lt - 0.5, accent=V["accent"], size=36)
    else:
        snakes(c, t)
    if sid == "h":
        hc.timer(c, W / 2, 1840, 56, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s1" and lt > 0.8:
        hc.stamp(c, "IMAGEN QUIETA", W / 2, 1840, lt, 0.8, 80, col=RED)
    if sid == "s2":
        hc.big(c, "2003", W / 2, 1850, 120, V["accent"], lt, 0.3)
    if sid == "s4":
        K.tag(c, W / 2, 1850, "NEGRO → AZUL → BLANCO → AMARILLO", lt - 0.4, accent=V["accent"], size=32)


V606 = dict(slug="606_ilusion_serpientes_t4p1", accent=ILU, drone=0.02, scene=s_serpientes, badge=SERIE.format(1),
            send="ENVÍASELO A ALGUIEN Y QUE TE DIGA SI GIRA", rehook=("s3", "AHORA HAZ ESTA PRUEBA"), loop=True, segs=[
    dict(id="h", who="nar", say="¿Ves estos círculos girar? La imagen está totalmente quieta.",
         cap="¿Los ves *GIRAR*? | Está *QUIETA*", hold=1.4),
    dict(id="s1", who="nar", cut=True, say="No hay animación. Ni un píxel se mueve. El movimiento lo está fabricando tu cerebro.",
         cap="Ni un píxel se mueve. | El giro lo fabrica | tu *CEREBRO*", hold=0.4),
    dict(id="s2", who="nar", cut=True, say="Se llama serpientes rotatorias. La creó el psicólogo japonés Akiyoshi Kitaoka en dos mil tres.",
         cap="*Serpientes rotatorias*: | Akiyoshi Kitaoka, | Japón, *2003*"),
    dict(id="s3", who="nar", cut=True, say="Haz la prueba: mira fijo el punto rojo. El círculo que miras se para. Los de alrededor siguen girando.",
         cap="Mira fijo el *punto rojo*: | ese círculo *SE PARA*", hold=0.6),
    dict(id="s4", who="nar", say="El truco es el orden: negro, azul, blanco y amarillo. Tu vista periférica lo lee como movimiento.",
         cap="El orden *negro, azul*, | *blanco, amarillo*: | tu vista lo lee como *movimiento*"),
    dict(id="cta", who="nar", cut=True, say="Temporada cuatro, parte uno de tres. ¿Te giraban? Comenta sí o no. Y sígueme: la dos es todavía peor.",
         cap="T4, parte *1 de 3*. | ¿Te giraban? *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 607 Reto: ¿cuántos rectángulos?
def s_rect(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A3A5A, 0xFF3A1A5A, seed=607)
    n, cell = 3, 260
    x0, y0 = W / 2 - n * cell / 2 + math.sin(t * 0.6) * 4, 1230 - n * cell / 2
    groups = {"s3": [(1, 1)], "s4": [(1, 2), (2, 1)], "s5": [(1, 3), (3, 1)], "s6": [(2, 2)], "s7": [(2, 3), (3, 2)], "s8": [(3, 3)]}
    base = {"s3": 0, "s4": 9, "s5": 21, "s6": 27, "s7": 31, "s8": 35}
    if sid in groups:
        rects = []
        for (w_, h_) in groups[sid]:
            for j in range(n - h_ + 1):
                for i in range(n - w_ + 1):
                    rects.append((i, j, w_, h_))
        cnt = len(rects)
        dur = max(1.2, (P["tl"][sid][1] - P["tl"][sid][0]) - 0.6)
        shown = min(cnt, int(lt / (dur / cnt)) + 1)
        i, j, w_, h_ = rects[shown - 1]
        r = skia.Rect.MakeXYWH(x0 + i * cell + 10, y0 + j * cell + 10, w_ * cell - 20, h_ * cell - 20)
        c.drawRect(r, fill(with_alpha(V["accent"], 0.35)))
        c.drawRect(r, stroke(V["accent"], 12))
        hc.big(c, str(base[sid] + shown), W / 2, 1770, 160, V["accent"], 1.0, 0.0)
    for i in range(n + 1):
        c.drawLine(x0 + i * cell, y0, x0 + i * cell, y0 + n * cell, stroke(WHITE, 10))
        c.drawLine(x0, y0 + i * cell, x0 + n * cell, y0 + i * cell, stroke(WHITE, 10))
    if sid == "h":
        hc.timer(c, W / 2, 1810, 70, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s1":
        K.tag(c, W / 2, 1780, "COMENTA TU NÚMERO", lt - 0.2, accent=V["accent"], size=44)
    if sid == "cta":
        hc.stamp(c, "36", W / 2, 1760, lt, 0.1, 150, col=GREEN)


V607 = dict(slug="607_cuantos_rectangulos", accent=0xFFFF5AC8, drone=0.02, scene=s_rect, tease="PEOR QUE EL DE LOS CUADRADOS",
            send="RETA A UN AMIGO: ENVÍASELO", rehook=("s4", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s3", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="¿Cuántos rectángulos ves? Es peor que el de los cuadrados.",
         cap="¿Cuántos *RECTÁNGULOS* | ves?", hold=1.5),
    dict(id="s1", who="nar", cut=True, say="Ojo, que un cuadrado también es un rectángulo. Escribe tu número antes de seguir.",
         cap="Un cuadrado también | cuenta. Escribe tu | número en *COMENTARIOS*", hold=0.6),
    dict(id="s2", who="q", cut=True, say="¿Ya? Vamos a contarlos.", cap="¿Ya? | Vamos a *contarlos*"),
    dict(id="s3", who="nar", cut=True, say="Los pequeños: nueve.", cap="Los pequeños: | *NUEVE*", hold=1.0),
    dict(id="s4", who="nar", cut=True, say="De dos piezas, tumbados y de pie: doce más.", cap="De *dos piezas*: | *DOCE* más", hold=1.2),
    dict(id="s5", who="nar", cut=True, say="De tres en fila: seis.", cap="De *tres en fila*: | *SEIS*", hold=0.9),
    dict(id="s6", who="nar", cut=True, say="Cuadrados de dos por dos: cuatro.", cap="De *2×2*: | *CUATRO*", hold=0.8),
    dict(id="s7", who="nar", cut=True, say="De dos por tres: otros cuatro.", cap="De *2×3*: | otros *CUATRO*", hold=0.8),
    dict(id="s8", who="nar", cut=True, say="Y el grande. Uno.", cap="Y el *GRANDE*", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Treinta y seis. ¿Cuántos dijiste tú? Comenta. Y sígueme para el próximo reto.",
         cap="Total: *36*. ¿Y tú? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 608 T4 P2: espiral de Fraser (1908)
def fraser(c, t, cx, cy, hl=-1, hk=0.0, checker=True):
    if checker:
        c.save(); c.translate(cx, cy)
        for r in range(1, 12):
            for i in range(32):
                p = skia.Path()
                rr, rin = r * 46, (r - 1) * 46
                a0 = i * 360 / 32
                p.addArc(skia.Rect.MakeXYWH(-rr, -rr, 2 * rr, 2 * rr), a0, 360 / 32)
                p.arcTo(skia.Rect.MakeXYWH(-rin, -rin, 2 * rin, 2 * rin), a0 + 360 / 32, -360 / 32, False)
                p.close()
                c.drawPath(p, fill(0xFF2E8A3A if (i + r) % 2 else 0xFF5ABA4A))
        c.restore()
    for k, R in enumerate((120, 210, 300, 390, 470)):
        m = int(R / 9)
        for i in range(m):
            a = 2 * math.pi * i / m
            x, y = cx + R * math.cos(a), cy + R * math.sin(a)
            c.save(); c.translate(x, y); c.rotate(math.degrees(a) + 90 + 28)
            col = 0xFF111111 if i % 2 else 0xFFFFFFFF
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-17, -7, 34, 14), 7, 7), fill(col))
            c.restore()
        if k == hl and hk > 0:
            p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, 2 * R), -90, 360 * hk)
            c.drawPath(p, stroke(with_alpha(RED, 0.95), 14))


def s_fraser(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 608)
    cx, cy = W / 2, 1230
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(40, cy - 540, W - 80, 1080), 40, 40), fill(0xFF1A1A1A))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(40, cy - 540, W - 80, 1080), 40, 40))
    if sid == "s2":
        fraser(c, t, cx, cy, hl=3, hk=ease_in_out(clamp((lt - 0.3) / 2.2)))
    elif sid == "s3":
        fraser(c, t, cx, cy, checker=lt < 1.0 or int(lt * 2) % 2 == 0)
    else:
        fraser(c, t, cx, cy)
    c.restore()
    if sid == "h":
        hc.timer(c, W / 2, 1840, 56, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2" and lt > 2.6:
        hc.stamp(c, "CÍRCULOS", W / 2, 1840, lt, 2.6, 90, col=RED)
    if sid == "s3" and lt > 0.3:
        hc.big(c, "1908", W / 2, 1850, 120, V["accent"], lt, 0.3)


V608 = dict(slug="608_ilusion_fraser_t4p2", accent=ILU, drone=0.02, scene=s_fraser, badge=SERIE.format(2),
            send="ENVÍASELO A QUIEN VEA LA ESPIRAL", rehook=("s2", "SIGUE LA LÍNEA ROJA"), reveal=("s2", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Ves una espiral? Mira bien. No hay ninguna.",
         cap="¿Ves una *ESPIRAL*? | No hay *NINGUNA*", hold=1.4),
    dict(id="s1", who="nar", cut=True, say="Parece que las líneas van girando hacia el centro. Pero intenta seguir una con el dedo.",
         cap="Parece que giran hacia | el centro… Sigue una | con el *dedo*", hold=0.4),
    dict(id="s2", who="nar", cut=True, say="Mira: si la sigo, vuelvo al mismo punto. Son círculos perfectos, uno dentro de otro.",
         cap="Vuelvo al mismo punto: | son *CÍRCULOS* perfectos", hold=0.9),
    dict(id="s3", who="nar", cut=True, say="Es la espiral de Fraser. La publicó el psicólogo británico James Fraser en mil novecientos ocho.",
         cap="*Espiral de Fraser*: | James Fraser, | en *1908*"),
    dict(id="s4", who="nar", say="Cada círculo está hecho de trocitos inclinados. Tu cerebro suma esas inclinaciones, y convierte los círculos en una espiral.",
         cap="Trocitos *inclinados*: | tu cerebro los suma | y crea una *ESPIRAL*"),
    dict(id="cta", who="nar", cut=True, say="Temporada cuatro, parte dos de tres. ¿La viste? Comenta sí o no. Y sígueme: la tres es la más difícil.",
         cap="T4, parte *2 de 3*. | ¿La viste? *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 609 Houdini murió en Halloween (100 años) — serie implícita
def stage(c, t, spot=1.0):
    c.drawPaint(fill(0xFF0A0506))
    for side in (-1, 1):
        for k in range(8):
            x = W / 2 + side * (W / 2 - 40 - k * 32)
            c.drawRect(skia.Rect.MakeXYWH(x - 30, 0, 60, H), skia.Paint(Shader=skia.GradientShader.MakeLinear(
                [(x - 30, 0), (x + 30, 0)], [0xFF4A0A10, 0xFF9A1A24, 0xFF4A0A10])))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 220), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, 220)], [0xFF6A0A14, 0xFF3A0508])))
    c.drawRect(skia.Rect.MakeXYWH(0, 1640, W, 400), fill(0xFF2A1A10))
    for k in range(6):
        c.drawLine(0, 1660 + k * 50, W, 1660 + k * 50, stroke(with_alpha(0xFF000000, 0.4), 3))
    sh = skia.GradientShader.MakeRadial((W / 2, 1200), 620, [with_alpha(0xFFFFF0C0, 0.35 * spot), 0x00000000])
    c.drawCircle(W / 2, 1200, 620, skia.Paint(Shader=sh))


def water_cell(c, x, y, t, fill_k=1.0):
    c.save(); c.translate(x, y)
    r = skia.Rect.MakeXYWH(-230, -420, 460, 840)
    hgt = 800 * fill_k
    c.drawRect(skia.Rect.MakeXYWH(-215, 405 - hgt, 430, hgt), fill(with_alpha(0xFF2A7AB8, 0.55)))
    R = random.Random(1)
    for i in range(40):
        bx = R.uniform(-190, 190)
        by = 400 - ((R.uniform(0, 800) + t * R.uniform(80, 200)) % max(1, hgt))
        c.drawCircle(bx + math.sin(t * 3 + i) * 6, by, R.uniform(4, 11), stroke(with_alpha(WHITE, 0.6), 2))
    c.drawRect(r, stroke(0xFFB8A060, 16))
    for yy in (-420, 420):
        c.drawRect(skia.Rect.MakeXYWH(-250, yy - 22, 500, 44), fill(0xFF8A7038))
    c.drawRect(skia.Rect.MakeXYWH(-215, -405, 80, 810), fill(with_alpha(WHITE, 0.08)))
    c.restore()


def chains(c, x, y, t, k=1.0):
    for j in range(16):
        a = j * 0.5 + math.sin(t * 2) * 0.1
        cx, cy = x + math.cos(a) * 220, y + j * 38 - 300
        c.save(); c.translate(cx, cy); c.rotate(90 * (j % 2) + 20)
        c.drawOval(skia.Rect.MakeXYWH(-30, -18, 60, 36), stroke(with_alpha(0xFFB8BCC4, k), 11))
        c.restore()
    # candado
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 70, y + 330, 140, 120), 16, 16), fill(0xFFC8A040))
    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - 50, y + 260, 100, 140), 180, 180)
    c.drawPath(p, stroke(0xFFB8BCC4, 16))
    c.drawCircle(x, y + 385, 14, fill(0xFF3A2A10))


def headline(c, t, lt, top, sub, date):
    c.save(); c.translate(W / 2, 1150); c.rotate(lerp(-25, -3, ease_out(clamp(lt / 0.5))))
    s = ease_back(clamp(lt / 0.5), 1.8); c.scale(s, s)
    r = skia.Rect.MakeXYWH(-440, -520, 880, 1040)
    c.drawRect(r.makeOffset(16, 20), fill(0x88000000))
    c.drawRect(r, fill(0xFFEAE4D2))
    draw_text(c, date, 0, -440, 40, 0xFF3A3A3A, shadow=False)
    c.drawLine(-400, -410, 400, -410, stroke(0xFF1A1A1A, 4))
    draw_text(c, top, 0, -280, 110, 0xFF111111, shadow=False)
    draw_text(c, sub, 0, -170, 50, 0xFFB02A2A, shadow=False)
    for i in range(10):
        c.drawRect(skia.Rect.MakeXYWH(-400, -80 + i * 50, 800 - (i % 4) * 110, 20), fill(0xFFB8B2A2))
    c.restore()


def candles(c, t, n=5, y=1450):
    c.drawOval(skia.Rect.MakeXYWH(90, y - 60, W - 180, 300), fill(0xFF2A1608))
    for i in range(n):
        x = W / 2 + (i - (n - 1) / 2) * 170
        c.drawRect(skia.Rect.MakeXYWH(x - 26, y - 180, 52, 180), fill(0xFFEDE4CC))
        fl = 1 + 0.15 * math.sin(t * 13 + i * 2) + 0.1 * math.sin(t * 29 + i)
        glow(c, x, y - 230, 160, 0xFFFFB040, 0.35 * fl)
        p = skia.Path(); p.moveTo(x, y - 290 * fl + 30 * (fl - 1)); p.quadTo(x + 22, y - 220, x, y - 190); p.quadTo(x - 22, y - 220, x, y - 290 * fl + 30 * (fl - 1))
        c.drawPath(p, fill(0xFFFFD27A))


def s_houdini(c, t, P, V):
    sid, lt = seg(P, t)
    if sid == "h":
        stage(c, t)
        chains(c, W / 2, 1150, t)
        hc.big(c, "31 OCT 1926", W / 2, 1780, 120, V["accent"], lt, 0.6)
    elif sid == "s1":
        stage(c, t)
        water_cell(c, W / 2, 1180, t, fill_k=ease_out(clamp(lt / 2.0)))
        K.tag(c, W / 2, 1800, "LA CELDA DE TORTURA CHINA", lt - 0.5, accent=V["accent"], size=36)
    elif sid == "s2":
        stage(c, t, spot=0.6)
        k = ease_out(clamp(lt / 0.3))
        c.save(); c.translate(W / 2, 1150); c.scale(1 + 0.4 * (1 - k), 1 + 0.4 * (1 - k))
        draw_text(c, "22 OCT 1926", 0, -40, 120, WHITE)
        draw_text(c, "MONTREAL", 0, 90, 70, V["accent"])
        c.restore()
        if lt > 1.2:
            hc.stamp(c, "POR SORPRESA", W / 2, 1600, lt, 1.2, 100, col=RED)
    elif sid == "s3":
        c.drawPaint(fill(0xFF120A08))
        headline(c, t, lt, "HOUDINI", "MUERE EN HALLOWEEN", "DETROIT · 1 DE NOVIEMBRE DE 1926")
        K.tag(c, W / 2, 1820, "APENDICITIS → PERITONITIS", lt - 0.8, accent=V["accent"], size=36)
    elif sid == "s4":
        c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, 1200), 1200, [0xFF2A160A, 0xFF060302])))
        candles(c, t)
        k = ease_out(clamp((lt - 0.4) / 1.0))
        c.save(); c.translate(W / 2, 900); c.rotate(-4)
        c.drawRect(skia.Rect.MakeXYWH(-330 * k, -110, 660 * k, 220), fill(0xFFF0E6CC))
        if k > 0.9:
            draw_text(c, "CÓDIGO SECRETO", 0, -20, 48, 0xFF5A2A1A, shadow=False)
            draw_text(c, "• • • • • • • •", 0, 60, 60, 0xFF1A1A1A, shadow=False)
        c.restore()
    else:
        c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, 1200), 1200, [0xFF2A160A, 0xFF060302])))
        candles(c, t)


V609 = dict(slug="609_houdini_halloween_100", accent=0xFFFFB03A, drone=0.04, scene=s_houdini, tease="HISTORIA REAL",
            send="ENVÍASELO A QUIEN LE GUSTE LA MAGIA", rehook=("s3", "Y MURIÓ JUSTO ESE DÍA"), loop=False, segs=[
    dict(id="h", who="nar", say="Hoy hace exactamente cien años, el mago más famoso del mundo murió en la noche de Halloween.",
         cap="Hoy hace *100 años*, el mago | más famoso del mundo | murió en *HALLOWEEN*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Harry Houdini escapaba de esposas, de cadenas, y de una celda llena de agua, colgado boca abajo.",
         cap="*Harry Houdini* escapaba | de cadenas… y de una | celda llena de *AGUA*"),
    dict(id="s2", who="nar", cut=True, say="El veintidós de octubre de mil novecientos veintiséis, en Montreal, un estudiante le dio varios puñetazos en el abdomen, por sorpresa.",
         cap="*22 de octubre de 1926*: | un estudiante le golpea | el abdomen *por sorpresa*"),
    dict(id="s3", who="nar", cut=True, say="Siguió actuando con dolor. Tenía el apéndice reventado. Murió en Detroit el treinta y uno de octubre. Justo en Halloween.",
         cap="Tenía el *apéndice* reventado. | Murió el *31 de octubre*: | justo en *Halloween*"),
    dict(id="s4", who="nar", cut=True, say="Pero antes, Houdini y su mujer pactaron un código secreto. Si había vida después de la muerte, él se lo diría desde el más allá.",
         cap="Antes pactó con su mujer | un *código secreto*… | para hablarle desde el *más allá*"),
    dict(id="cta", who="nar", cut=True, say="Lo que pasó en las sesiones de espiritismo, cada Halloween, te lo cuento mañana. Sígueme para no perdértelo, y comenta: ¿crees en fantasmas?",
         cap="Lo que pasó *cada Halloween*, | te lo cuento *MAÑANA*. | *SÍGUEME* y comenta"),
])


# ====================================================================== 610 T4 P3: ilusión de White (1979)
def white_ill(c, t, cx, cy, merge=0.0, strip=1.0):
    W0, H0 = 820, 900
    x0, y0 = cx - W0 / 2, cy - H0 / 2
    nb = 18
    bh = H0 / nb
    for i in range(nb):
        col = 0xFF111111 if i % 2 == 0 else 0xFFFFFFFF
        if strip < 1:
            col = lerpcol(col, 0xFF7A7AAA, 1 - strip)
        c.drawRect(skia.Rect.MakeXYWH(x0, y0 + i * bh, W0, bh), fill(col))
    gray = 0xFF8A8A8A
    # izquierda: grises sobre barras NEGRAS (filas pares); derecha: sobre barras BLANCAS (impares)
    for i in range(4, 14):
        if i % 2 == 0:
            xl = lerp(x0 + 90, cx - 150, merge)
            c.drawRect(skia.Rect.MakeXYWH(xl, y0 + i * bh, 200, bh), fill(gray))
        else:
            xr = lerp(x0 + W0 - 290, cx - 50, merge)
            c.drawRect(skia.Rect.MakeXYWH(xr, y0 + i * bh, 200, bh), fill(gray))


def lerpcol(a, b, k):
    ch = [int(lerp((a >> s) & 255, (b >> s) & 255, k)) for s in (16, 8, 0)]
    return 0xFF000000 | (ch[0] << 16) | (ch[1] << 8) | ch[2]


def s_white(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 610)
    cx, cy = W / 2, 1220
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(60, cy - 500, W - 120, 1000), 40, 40), fill(0xFF7A7AAA))
    if sid == "s2":
        white_ill(c, t, cx, cy, strip=1 - ease_in_out(clamp((lt - 0.3) / 1.4)))
    elif sid == "s3":
        white_ill(c, t, cx, cy, merge=ease_in_out(clamp((lt - 0.2) / 1.6)))
    else:
        white_ill(c, t, cx, cy)
    if sid in ("h", "s1"):
        K.tag(c, W / 2 - 230, cy + 560, "A", lt - 0.2, accent=V["accent"], size=60)
        K.tag(c, W / 2 + 230, cy + 560, "B", lt - 0.2, accent=V["accent"], size=60)
    if sid == "h":
        hc.timer(c, W / 2, 1860, 52, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2" and lt > 1.8:
        hc.stamp(c, "MISMO GRIS", W / 2, 1830, lt, 1.8, 90, col=RED)
    if sid == "s4":
        hc.big(c, "1979", W / 2, 1830, 120, V["accent"], lt, 0.3)


V610 = dict(slug="610_ilusion_white_t4p3", accent=ILU, drone=0.02, scene=s_white, badge=SERIE.format(3),
            send="ENVÍASELO A QUIEN DIGA QUE VE BIEN", rehook=("s2", "QUITO LAS RAYAS"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Qué gris es más claro, el de la A o el de la B?",
         cap="¿Qué gris es *más claro*: | el de la *A* o el de la *B*?", hold=1.4),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo dice la A. Elige tú, y luego mira.",
         cap="Casi todos dicen la *A*. | Elige… y *MIRA*", hold=0.5),
    dict(id="s2", who="nar", cut=True, say="Si quito las rayas negras y blancas, son exactamente el mismo gris.",
         cap="Sin rayas… son | *EXACTAMENTE* | el mismo gris", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Y si los junto, ya no hay ninguna diferencia.", cap="Si los junto… | *NINGUNA* diferencia", hold=0.6),
    dict(id="s4", who="nar", say="Es la ilusión de White, de mil novecientos setenta y nueve. Tu cerebro no mide el color: lo compara con lo que tiene alrededor.",
         cap="*Ilusión de White*, 1979: | tu cerebro no mide el color, | lo *COMPARA*"),
    dict(id="cta", who="nar", cut=True, say="¿Cuál de las tres te engañó más? Comenta uno, dos o tres. Y sígueme: mañana, más retos para tu cerebro.",
         cap="¿Cuál te engañó más? | Comenta *1, 2 o 3* | y *SÍGUEME*"),
])

VIDEOS = [V601, V602, V603, V604, V605, V606, V607, V608, V609, V610]


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
