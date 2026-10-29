"""Lote diario 29/10/2026 (401–410). Motor v7 (LLAMADA A ENVIAR: pill blanca con avión de papel animado en el CTA,
V['send']; en IG 2026 los envíos por DM son la señal que más alcance da fuera de seguidores).
Mezcla según métricas del 28/10: ilusiones en serie P1/P2 = 1.282/1.360 (la serie funciona) -> TEMPORADA 2
(Sander, Poggendorff, Delboeuf) en la noche; test con el cuerpo 'haz esto' (dedo flotante 1.329 y 8 envíos) ->
brazo flotante (Kohnstamm); '3 cosas' (cerebro 1.008) -> 3 cosas mientras duermes; Ío a las 12:00 (lo prometido;
Europa 1.286); mitos de animal/colegio (prometidos): perros y colores, Colón y la Tierra plana; escala/espacio
'tú': túnel a través de la Tierra; experimental: '¿cuántos triángulos ves?' (Q/O 1.348 -> retos de búsqueda)."""
import math, sys, random
import numpy as np
import skia
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow, pill
from core import draw_text, font, text_w

OUT = "/home/claude/tiktok/outdaily"
ILU = 0xFFFFE04D
GREEN = 0xFF2FD46B


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


def lerpc(a, b, k):
    ch = [int(lerp((a >> s) & 255, (b >> s) & 255, k)) for s in (16, 8, 0)]
    return 0xFF000000 | (ch[0] << 16) | (ch[1] << 8) | ch[2]


# ====================================================================== 401 Ío (lo prometido)
def io_texture():
    path = S.TEX + "io_proc.png"
    try:
        Image.open(path)
        return S.load("io_proc.png")
    except Exception:
        pass
    w, h = 2048, 1024
    rnd = np.random.default_rng(401)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    base = np.zeros((h, w), np.float32)
    for k in range(7):
        f = 2 ** k
        ph = rnd.uniform(0, 6.28, 3)
        base += np.sin(xx / w * 6.28 * f + ph[0] + 1.5 * np.sin(yy / h * 6.28 * f + ph[1])) * \
            np.cos(yy / h * 3.14 * f * 1.3 + ph[2]) / (k + 1) ** 0.9
    base = (base - base.min()) / (base.max() - base.min())
    # azufre: amarillo -> naranja -> blanco (escarcha de SO2)
    r = 0.93 + 0.05 * base
    g = 0.78 + 0.16 * base
    b = 0.30 + 0.35 * base ** 2
    img = np.stack([r, g, b], -1)
    pole = np.abs(yy / h - 0.5)[..., None] * 2
    img = img * (1 - 0.35 * pole ** 3) + np.array([0.55, 0.42, 0.30]) * 0.35 * pole ** 3
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    R = random.Random(401)
    for _ in range(7):  # anillos rojizos difusos de depósitos (tipo Pele)
        x, y, rr = R.uniform(0, w), R.uniform(250, h - 250), R.uniform(50, 120)
        d.ellipse([x - rr, y - rr * 0.8, x + rr, y + rr * 0.8], outline=(205, 120, 70), width=int(R.uniform(10, 22)))
    for _ in range(90):  # calderas oscuras (paterae)
        x, y, rr = R.uniform(0, w), R.uniform(80, h - 80), R.uniform(3, 12)
        d.ellipse([x - rr, y - rr * 0.7, x + rr, y + rr * 0.7], fill=(int(R.uniform(30, 70)), int(R.uniform(20, 40)), 15))
    for _ in range(18):  # manchas de lava reciente (casi negras con borde naranja)
        x, y, rr = R.uniform(0, w), R.uniform(150, h - 150), R.uniform(5, 14)
        d.ellipse([x - rr - 5, y - rr * 0.7 - 4, x + rr + 5, y + rr * 0.7 + 4], fill=(230, 120, 40))
        d.ellipse([x - rr, y - rr * 0.7, x + rr, y + rr * 0.7], fill=(25, 15, 10))
    im = im.filter(ImageFilter.GaussianBlur(2.6))
    im.save(path)
    return S.load("io_proc.png")


IO = io_texture()
JUP = S.load("jupitermap.jpg")
MOON = S.load("moon_1024.jpg")
DAY = S.load("earth_atmos_2048.jpg")
CLOUDS = S.load("earth_clouds_1024.png", "A")
ST = K.Stars(seed=401)


def plume(c, x, y, ang, height, t, k=1.0, seed=0, col=0xFFFFD27A):
    """Penacho volcánico en paraguas: partículas balísticas que suben y caen (sin aire en Ío)."""
    r = random.Random(seed)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    p = skia.Paint(AntiAlias=True)
    for i in range(140):
        ph = (t * 0.45 + r.random()) % 1.0
        spread = r.uniform(-1, 1)
        hx = spread * height * 0.75 * ph * 2
        hy = -height * (4 * ph * (1 - ph))  # parábola
        X = x + hx * ca - hy * sa
        Y = y + hx * sa + hy * ca
        a = k * (1 - ph) ** 0.5 * r.uniform(0.3, 0.9)
        p.setColor(with_alpha(col if i % 3 else 0xFFFFF4E0, a))
        c.drawCircle(X, Y, r.uniform(2, 5), p)
    glow(c, x, y, height * 0.35, 0xFFFF8A3A, 0.5 * k)


def s_io(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020308)
    ST.draw(c, t, camx=t * 12, alpha=0.9)
    L = (-0.55, 0.3, 0.78)
    if sid == "h":
        jr = 640
        S.draw_planet(c, W * 0.12, 1420, jr, S.render(2 * jr, JUP, spin=t * 0.3, light=L, gain=1.1, limb=0.35))
        ir = lerp(140, 330, ease_out(clamp(lt / 3.0)))
        cx, cy = W * 0.64, 1120
        S.draw_planet(c, cx, cy, ir, S.render(2 * ir, IO, spin=t * 0.2, light=L, gain=1.15, limb=0.25))
        plume(c, cx + ir * 0.62, cy - ir * 0.78, 38, ir * 0.55, t, seed=1)
        plume(c, cx - ir * 0.9, cy - ir * 0.35, -68, ir * 0.4, t + 0.3, seed=2)
    elif sid == "s1":
        ir = 340
        S.draw_planet(c, W / 2 - 170, 1230, ir, S.render(2 * ir, IO, spin=t * 0.2, light=L, gain=1.15, limb=0.25))
        mr = ir * 3474 / 3643
        S.draw_planet(c, W / 2 + 300, 1330, mr * 0.55, S.render(int(2 * mr * 0.55), MOON, spin=0.3, light=L, gain=1.2))
        K.tag(c, W / 2 - 170, 1660, "ÍO · 3.640 km", lt - 0.3, accent=V["accent"], size=34)
        K.tag(c, W / 2 + 300, 1560, "NUESTRA LUNA", lt - 0.6, accent=WHITE, size=30)
    elif sid in ("s2", "s3"):
        ir = 520 if sid == "s2" else 420
        cx, cy = W / 2, 1450 if sid == "s3" else 1250
        S.draw_planet(c, cx, cy, ir, S.render(2 * ir, IO, spin=t * 0.15, light=L, gain=1.15, limb=0.25))
        rr = random.Random(5)
        for k in range(12 if sid == "s2" else 3):  # puntos de lava incandescente
            a = rr.uniform(-2.6, -0.5)
            d = rr.uniform(0.2, 0.85) * ir
            glow(c, cx + math.cos(a) * d, cy + math.sin(a) * d, 40, 0xFFFF6A2A, 0.6 + 0.3 * math.sin(t * 6 + k))
        if sid == "s2":
            K.counter(c, t, lt - 0.2, lambda p: f"~{int(round(400 * p))}", "VOLCANES ACTIVOS", V["accent"], y=680)
        else:
            plume(c, cx, cy - ir + 10, 0, 520, t, seed=7)
            plume(c, cx + ir * 0.6, cy - ir * 0.8 + 10, 37, 300, t + 0.5, seed=8)
            K.counter(c, t, lt - 0.2, lambda p: f"+{int(round(300 * p))} km", "DE ALTURA", 0xFFFF8A3A, y=700)
    elif sid == "s4":
        # foto antigua de la Voyager: imagen granulada con marco
        c.drawRect(skia.Rect.MakeXYWH(90, 760, W - 180, 900), fill(0xFF0A0A0A))
        ir = 300
        S.draw_planet(c, W / 2, 1210, ir, S.render(2 * ir, IO, spin=0.4, light=L, gain=0.9, limb=0.3))
        c.drawRect(skia.Rect.MakeXYWH(90, 760, W - 180, 900), fill(with_alpha(0xFF0A0A0A, 0.25)))
        k = ease_out(clamp((lt - 0.8) / 0.8))
        plume(c, W / 2 - ir * 0.95, 1210 - 30, -88, 170, t, k=k, seed=9, col=0xFFDDE6FF)
        if lt > 1.2:
            c.drawCircle(W / 2 - ir - 80, 1180, 120, stroke(with_alpha(0xFFFF3B4A, clamp((lt - 1.2) * 3)), 8))
        c.drawRect(skia.Rect.MakeXYWH(90, 760, W - 180, 900), stroke(with_alpha(WHITE, 0.6), 4))
        K.tag(c, W / 2, 1760, "VOYAGER 1 · MARZO 1979", lt - 0.3, accent=V["accent"], size=36)
    elif sid == "s5":
        jr = 380
        S.draw_planet(c, W / 2, 1250, jr, S.render(2 * jr, JUP, spin=t * 0.3, light=L, gain=1.1, limb=0.35))
        for k, (rad, per, nm, tex, sz) in enumerate(((470, 1.0, "ÍO", IO, 34), (560, 2.0, "EUROPA", MOON, 30),
                                                     (650, 4.0, "GANÍMEDES", MOON, 42))):
            c.drawCircle(W / 2, 1250, rad, stroke(with_alpha(WHITE, 0.18), 3))
            a = -t * 1.6 / per + k
            x, y = W / 2 + math.cos(a) * rad, 1250 + math.sin(a) * rad * 0.9
            S.draw_planet(c, x, y, sz, S.render(2 * sz, tex, spin=t, light=L, gain=1.2))
        K.tag(c, W / 2, 1880, "1 : 2 : 4", lt - 0.3, accent=V["accent"], size=48)
    else:
        ir = 330 if sid != "cta" else 260
        S.draw_planet(c, W / 2, 1200, ir, S.render(2 * ir, IO, spin=t * 0.2, light=L, gain=1.15, limb=0.25))
        bulge = 1 + 0.03 * math.sin(t * 3)
        c.drawOval(skia.Rect.MakeXYWH(W / 2 - ir * bulge - 6, 1200 - ir - 6, 2 * ir * bulge + 12, 2 * ir + 12),
                   stroke(with_alpha(0xFFFF8A3A, 0.6), 6))
        if sid == "s6":
            K.counter(c, t, lt - 0.2, lambda p: f"{int(round(100 * p))} m", "SUBE Y BAJA EL SUELO", 0xFFFF8A3A, y=1700)
        plume(c, W / 2 + ir * 0.7, 1200 - ir * 0.72, 44, 160, t, seed=11)
        if sid == "cta":
            gr = 140
            gx = lerp(W + 200, W - 210, ease_out(clamp(lt / 1.2)))
            S.draw_planet(c, gx, 1660, gr, S.render(2 * gr, MOON, spin=1.0, light=L, gain=1.15))
            c.drawCircle(gx, 1660, gr, fill(with_alpha(0xFF9A8A70, 0.35)))


V401 = dict(slug="401_io_volcanes", accent=0xFFFFC23A, drone=0.035, scene=s_io, badge="LO PROMETIDO · JÚPITER PARTE 3",
            send="ENVÍASELO A UN FRIKI DEL ESPACIO", segs=[
    dict(id="h", who="nar", say="Esta luna tiene unos cuatrocientos volcanes activos. Es el lugar más volcánico del Sistema Solar.",
         cap="Esta luna tiene | *400 VOLCANES* | activos", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Se llama Ío, y es otra luna de Júpiter. Casi igual de grande que nuestra Luna.",
         cap="Se llama *Ío*. | Casi como | *nuestra Luna*"),
    dict(id="s2", who="nar", cut=True, say="Pero en vez de cráteres, está llena de volcanes en erupción. Unos cuatrocientos.",
         cap="En vez de cráteres… | *VOLCANES* | en erupción"),
    dict(id="s3", who="nar", cut=True, say="Y como casi no tiene aire, sus penachos suben a más de trescientos kilómetros de altura.",
         cap="Sin aire, sus penachos | suben a más de | *300 KM*"),
    dict(id="s4", who="nar", cut=True, say="Lo descubrió en marzo de mil novecientos setenta y nueve Linda Morabito, una ingeniera de la NASA, en una foto de la Voyager uno.",
         cap="*Marzo de 1979*: | Linda Morabito lo vio | en una foto de la *Voyager*"),
    dict(id="s5", who="nar", cut=True, say="¿Por qué está tan caliente? Por un baile: por cada vuelta de Ganímedes, Europa da dos, e Ío da cuatro.",
         cap="¿Por qué? Un *baile*: | Ganímedes 1 vuelta, | Europa 2, *Ío 4*"),
    dict(id="s6", who="nar", cut=True, say="Júpiter y sus lunas la estiran sin parar, y su suelo sube y baja hasta unos cien metros. Eso la funde por dentro.",
         cap="La estiran sin parar: | su suelo sube y baja | hasta *100 METROS*"),
    dict(id="cta", who="nar", cut=True, say="Y mañana, la luna más grande del Sistema Solar. Es más grande que Mercurio. Sígueme, y comenta qué luna quieres ver.",
         cap="Mañana: una luna más grande | que *MERCURIO*. | *SÍGUEME* y *COMENTA*"),
])


# ====================================================================== 402 Mito: los perros ven en blanco y negro
def dogify(col, k):
    """Aproximación a la visión dicromática del perro: rojo/verde -> amarillo-marrón; azul se conserva."""
    a = (col >> 24) & 255
    r, g, b = (col >> 16) & 255, (col >> 8) & 255, col & 255
    y = 0.5 * r + 0.5 * g
    nr, ng, nb = y * 0.86, y * 0.84, b
    rr, gg, bb = [int(lerp(v0, v1, k)) for v0, v1 in ((r, nr), (g, ng), (b, nb))]
    rr, gg, bb = [max(0, min(255, v)) for v in (rr, gg, bb)]
    return (a << 24) | (rr << 16) | (gg << 8) | bb


def gray(col, k):
    r, g, b = (col >> 16) & 255, (col >> 8) & 255, col & 255
    y = 0.3 * r + 0.59 * g + 0.11 * b
    rr, gg, bb = [int(lerp(v, y, k)) for v in (r, g, b)]
    return 0xFF000000 | (rr << 16) | (gg << 8) | bb


def park(c, t, cf, ball_x=None):
    """Parque con césped, cielo, flores, pelota roja y frisbee azul. cf(color) transforma los colores."""
    sky = skia.GradientShader.MakeLinear([(0, 560), (0, 1250)], [cf(0xFF5AA8FF), cf(0xFFBFE6FF)])
    c.drawRect(skia.Rect.MakeLTRB(0, 560, W, 1250), skia.Paint(Shader=sky))
    c.drawCircle(860, 720, 70, fill(cf(0xFFFFF2A0)))
    for k in range(3):  # colinas
        p = skia.Path(); p.moveTo(0, 1250)
        for x in range(0, W + 41, 40):
            p.lineTo(x, 1150 - k * 40 - 60 * math.sin(x / (220 + 60 * k) + k))
        p.lineTo(W, 1250); p.close()
        c.drawPath(p, fill(cf([0xFF3A8A3A, 0xFF4A9A40, 0xFF5AAA48][k])))
    g = skia.GradientShader.MakeLinear([(0, 1230), (0, H)], [cf(0xFF4AB040), cf(0xFF2A7A28)])
    c.drawRect(skia.Rect.MakeLTRB(0, 1230, W, H), skia.Paint(Shader=g))
    r = random.Random(4)
    for _ in range(260):  # briznas
        x, y = r.uniform(0, W), r.uniform(1250, H)
        sw = math.sin(t * 2 + x / 80) * 6
        c.drawLine(x, y, x + sw, y - r.uniform(14, 34), stroke(cf(0xFF2E8A2A if r.random() < 0.5 else 0xFF6AC85A), 3))
    for _ in range(18):  # flores
        x, y = r.uniform(40, W - 40), r.uniform(1300, 1900)
        col = r.choice((0xFFFF3B4A, 0xFFFFE04D, 0xFFFF7AD9, 0xFF6F8AFF))
        for a in range(5):
            c.drawCircle(x + math.cos(a * 1.256) * 12, y + math.sin(a * 1.256) * 12, 10, fill(cf(col)))
        c.drawCircle(x, y, 7, fill(cf(0xFFFFF4C0)))
    bx = ball_x if ball_x is not None else 340 + math.sin(t * 1.2) * 30
    by = 1560 - abs(math.sin(t * 3)) * 90
    c.drawOval(skia.Rect.MakeXYWH(bx - 70, 1625, 140, 26), fill(0x44000000))
    c.drawCircle(bx, by, 72, skia.Paint(Shader=skia.GradientShader.MakeRadial((bx - 22, by - 24), 90,
                                                                              [cf(0xFFFF8A8A), cf(0xFFE0202A), cf(0xFF8A0A10)]), AntiAlias=True))
    fx, fy = 760, 1500 + math.sin(t * 2) * 10
    c.drawOval(skia.Rect.MakeXYWH(fx - 110, fy - 30, 220, 60), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(fx, fy - 30), (fx, fy + 30)], [cf(0xFF6FB0FF), cf(0xFF1A4ABF)]), AntiAlias=True))


def s_perros(c, t, P, V):
    sid, lt = seg(P, t)
    if sid == "h":
        park(c, t, lambda col: gray(col, 1.0))
        hc.stamp(c, "MITO", W / 2, 1760, lt, 1.0, 140)
    elif sid == "s1":
        park(c, t, lambda col: gray(col, 1 - ease_in_out(clamp(lt / 1.2))))
    elif sid in ("s2", "s3"):
        # pantalla partida: humano (izq) / perro (der), la línea barre
        split = W / 2 + math.sin(t * 0.8) * 120
        c.save(); c.clipRect(skia.Rect.MakeLTRB(0, 0, split, H)); park(c, t, lambda col: col); c.restore()
        c.save(); c.clipRect(skia.Rect.MakeLTRB(split, 0, W, H)); park(c, t, lambda col: dogify(col, 1.0)); c.restore()
        c.drawLine(split, 560, split, H, stroke(WHITE, 8))
        K.tag(c, split - 200, 640, "TÚ", 1.0, accent=WHITE, size=36)
        K.tag(c, split + 200, 640, "TU PERRO", 1.0, accent=V["accent"], size=36)
        if sid == "s2":
            for k, col in enumerate((0xFF3A6AFF, 0xFFFFD23A)):
                c.drawCircle(W / 2 - 70 + k * 140, 1840, 52, fill(col))
            K.tag(c, W / 2, 1740, "2 CONOS (TÚ TIENES 3)", lt - 0.3, accent=V["accent"], size=32)
    elif sid == "s4":
        park(c, t, lambda col: dogify(col, 1.0), ball_x=W / 2)
        hc.big(c, "1989", W / 2, 820, 170, V["accent"], lt, 0.2)
        K.tag(c, W / 2, 980, "UNIVERSIDAD DE CALIFORNIA", lt - 0.5, accent=WHITE, size=32)
    elif sid == "s5":
        park(c, t, lambda col: dogify(col, 1.0), ball_x=W / 2 + math.sin(t * 0.7) * 260)
        hc.stamp(c, "¿DÓNDE ESTÁ?", W / 2, 1800, lt, 0.6, 90, col=0xFFFF3B4A)
    else:
        park(c, t, lambda col: dogify(col, 0.0 if sid == "cta" else 1.0))
        if sid == "s6":
            for k, col in enumerate((0xFF3A6AFF, 0xFFFFD23A)):
                x = W / 2 - 150 + k * 300
                c.drawCircle(x, 1450, 95, skia.Paint(Shader=skia.GradientShader.MakeRadial((x - 30, 1420), 120, [WHITE, col]), AntiAlias=True))
            hc.big(c, "AZUL O AMARILLA", W / 2, 1720, 100, V["accent"], lt, 0.3)


V402 = dict(slug="402_perros_colores_mito", accent=0xFFFFD23A, drone=0.025, scene=s_perros, tease="TE LO DIJERON MAL",
            send="ENVÍASELO A ALGUIEN CON PERRO", segs=[
    dict(id="h", who="nar", say="Tu perro no ve en blanco y negro. Es un mito.",
         cap="Tu perro *NO* ve | en *blanco y negro*", hold=0.6),
    dict(id="s1", who="nar", cut=True, say="Durante décadas se repitió que los perros no veían colores. Pero sí los ven. Solo que menos que tú.",
         cap="Sí ven *colores*… | solo que | *menos que tú*"),
    dict(id="s2", who="nar", cut=True, say="Tú tienes tres tipos de conos en los ojos. Ellos, dos. Ven muy bien los azules y los amarillos.",
         cap="Tú tienes *3* tipos de conos. | Ellos, *2*: | *azul* y *amarillo*"),
    dict(id="s3", who="nar", cut=True, say="Pero el rojo y el verde los confunden. Para ellos se parecen a un marrón amarillento.",
         cap="El *rojo* y el *verde* | los confunden: | parecen *marrón*"),
    dict(id="s4", who="nar", cut=True, say="Lo demostró en mil novecientos ochenta y nueve un equipo de la Universidad de California, con pruebas de color a perros.",
         cap="Lo demostró en *1989* | un equipo de la | Universidad de *California*"),
    dict(id="s5", who="nar", cut=True, say="Por eso, una pelota roja sobre el césped verde casi se le pierde.",
         cap="Una *pelota roja* | en el césped… | casi *no la ve*"),
    dict(id="s6", who="nar", cut=True, say="Si quieres que la encuentre a la primera, cómprasela azul o amarilla.",
         cap="Si quieres que la vea: | *AZUL* o *AMARILLA*"),
    dict(id="cta", who="nar", cut=True, say="¿De qué color es la pelota de tu perro? Comenta. Y sígueme, que mañana desmonto otro mito de animales.",
         cap="¿De qué color es | la pelota de tu perro? | *COMENTA*"),
])


# ====================================================================== 403 Túnel a través de la Tierra
def earth_section(c, cx, cy, R, t, tunnel=1.0, ball=None):
    layers = ((1.0, 0xFF6A4A2A, 0xFF8A5A30), (0.97, 0xFFE0602A, 0xFFB8401A), (0.55, 0xFFFFA03A, 0xFFE0702A),
              (0.19, 0xFFFFF0A0, 0xFFFFC23A))
    for (f, c1, c2) in layers:
        r = R * f
        c.drawCircle(cx, cy, r, skia.Paint(Shader=skia.GradientShader.MakeRadial((cx, cy), r, [c2, c1]), AntiAlias=True))
    glow(c, cx, cy, R * 0.4, 0xFFFFE08A, 0.35 + 0.1 * math.sin(t * 3))
    if tunnel > 0:
        h = (R * 2) * tunnel
        c.drawRect(skia.Rect.MakeXYWH(cx - 22, cy - R, 44, h), fill(with_alpha(0xFF05060C, 0.92)))
        c.drawRect(skia.Rect.MakeXYWH(cx - 22, cy - R, 44, h), stroke(with_alpha(WHITE, 0.5), 3))
    if ball is not None:
        by = cy - R * math.cos(ball * math.pi)
        glow(c, cx, by, 70, 0xFF6FD6FF, 0.9)
        c.drawCircle(cx, by, 20, fill(WHITE))


def s_tunel(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020308)
    ST.draw(c, t, camx=t * 10, alpha=0.8)
    L = (-0.6, 0.3, 0.75)
    cx, cy, R = W / 2, 1200, 430
    if sid == "h":
        S.draw_planet(c, cx, cy, R, S.render(2 * R, DAY, spin=t * 0.12, light=L, clouds=CLOUDS, gain=1.1))
        S.atmosphere(c, cx, cy, R)
        k = ease_out(clamp(lt / 1.5))
        c.drawLine(cx, cy - R - 60, cx, cy - R - 60 + (2 * R + 120) * k, stroke(with_alpha(0xFF6FD6FF, 0.9), 10))
        glow(c, cx, cy - R - 60 + (2 * R + 120) * k, 80, 0xFF6FD6FF, 0.8)
    elif sid in ("s1", "s2", "s3"):
        earth_section(c, cx, cy, R, t, tunnel=1.0, ball=(0.5 - 0.5 * math.cos(t * 1.1)))
        if sid == "s1":
            K.tag(c, cx, cy + R + 90, "12.742 km DE TÚNEL", lt - 0.3, accent=V["accent"], size=36)
        if sid == "s2":
            K.counter(c, t, lt - 0.1, lambda p: f"{int(round(42 * p))} min", "CÁLCULO CLÁSICO", WHITE, y=cy + R + 120)
        if sid == "s3":
            K.tag(c, cx + 250, cy, "NÚCLEO MUY DENSO", lt - 0.3, accent=0xFFFFC23A, size=30, line_to=(cx + 40, cy))
    elif sid == "s4":
        earth_section(c, cx, cy, R, t, tunnel=1.0, ball=clamp(lt / 3.0))
        K.counter(c, t, lt - 0.1, lambda p: f"{int(round(38 * p))} min", "ALEXANDER KLOTZ · 2015", V["accent"], y=cy + R + 120)
    elif sid == "s5":
        earth_section(c, cx, cy, R, t, tunnel=1.0, ball=0.5 - 0.5 * math.cos(t * 2.2))
        hc.stamp(c, "IDA Y VUELTA", W / 2, cy + R + 140, lt, 0.4, 90, col=0xFFFF3B4A)
    else:
        S.draw_planet(c, cx, cy, R, S.render(2 * R, DAY, spin=t * 0.12, light=L, clouds=CLOUDS, gain=1.1))
        S.atmosphere(c, cx, cy, R)


V403 = dict(slug="403_tunel_tierra", accent=0xFF6FD6FF, drone=0.035, scene=s_tunel, tease="MIRA HASTA EL FINAL",
            send="ENVÍASELO A QUIEN SALTARÍA", segs=[
    dict(id="h", who="nar", say="Si cavas un túnel que atraviese la Tierra y saltas dentro, llegarías al otro lado en solo treinta y ocho minutos.",
         cap="Si saltas por un túnel | que atraviesa la Tierra… | llegas en *38 MINUTOS*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Imagina un túnel recto, sin aire, de doce mil setecientos kilómetros. Saltas, y la gravedad te acelera hacia el centro.",
         cap="Un túnel recto, *sin aire*, | de *12.742 km*. | Saltas… y *aceleras*"),
    dict(id="s2", who="nar", cut=True, say="Durante décadas, los libros de física decían cuarenta y dos minutos. Pero suponían una Tierra igual de densa por todas partes.",
         cap="Los libros decían | *42 minutos*… | con una Tierra *uniforme*"),
    dict(id="s3", who="nar", cut=True, say="Y no lo es. El núcleo es mucho más denso que la corteza, así que te tira con más fuerza durante más tiempo.",
         cap="Pero el *núcleo* es | mucho más *denso*… | y tira *más fuerte*"),
    dict(id="s4", who="nar", cut=True, say="En dos mil quince, el físico Alexander Klotz lo recalculó con la densidad real de la Tierra: treinta y ocho minutos.",
         cap="*2015*: el físico | *Alexander Klotz* lo recalculó: | *38 minutos*"),
    dict(id="s5", who="nar", cut=True, say="Y si no te agarras al llegar, vuelves a caer. Irías y vendrías, de un lado al otro, como un péndulo.",
         cap="Si no te agarras… | *vuelves a caer*. | Como un *péndulo*"),
    dict(id="cta", who="nar", cut=True, say="¿Saltarías? Comenta sí o no. Y sígueme para más cosas que te rompen la cabeza.",
         cap="¿Saltarías? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 404 Mito: en tiempos de Colón creían en la Tierra plana
def parchment(c, t):
    c.clear(0xFF2A1E12)
    g = skia.GradientShader.MakeRadial((W / 2, H / 2), H * 0.7, [0xFFE8D6A8, 0xFFC8A870, 0xFF6A4A2A])
    c.drawRect(skia.Rect.MakeXYWH(40, 520, W - 80, H - 600), skia.Paint(Shader=g))
    r = random.Random(12)
    for _ in range(90):
        x, y = r.uniform(60, W - 60), r.uniform(540, H - 100)
        c.drawCircle(x, y, r.uniform(8, 40), fill(with_alpha(0xFF8A6A3A, 0.06)))


def ship(c, x, y, s, t):
    c.save(); c.translate(x, y + math.sin(t * 2) * 8); c.scale(s, s); c.rotate(math.sin(t * 1.5) * 3)
    hull = skia.Path(); hull.moveTo(-160, 0); hull.lineTo(160, 0); hull.lineTo(120, 60); hull.lineTo(-120, 60); hull.close()
    c.drawPath(hull, fill(0xFF4A2A14))
    for k, (mx, h) in enumerate(((-60, 220), (40, 260))):
        c.drawLine(mx, 0, mx, -h, stroke(0xFF3A2010, 10))
        sail = skia.Path(); sail.moveTo(mx - 70, -h + 30); sail.quadTo(mx, -h + 10 + 20 * math.sin(t * 3 + k), mx + 70, -h + 30)
        sail.lineTo(mx + 70, -h + 160); sail.quadTo(mx, -h + 140, mx - 70, -h + 160); sail.close()
        c.drawPath(sail, fill(0xFFF4ECD8))
        c.drawLine(mx - 20, -h + 70, mx + 20, -h + 110, stroke(0xFFB8202A, 10))
        c.drawLine(mx + 20, -h + 70, mx - 20, -h + 110, stroke(0xFFB8202A, 10))
    c.restore()


def s_colon(c, t, P, V):
    sid, lt = seg(P, t)
    L = (-0.6, 0.3, 0.75)
    if sid in ("h", "s1"):
        c.clear(0xFF020308)
        ST.draw(c, t, camx=t * 10, alpha=0.8)
        R = 420
        S.draw_planet(c, W / 2, 1200, R, S.render(2 * R, DAY, spin=t * 0.15, light=L, clouds=CLOUDS, gain=1.1))
        S.atmosphere(c, W / 2, 1200, R)
        if sid == "h":
            hc.stamp(c, "FALSO", W / 2, 1760, lt, 1.0, 140)
        else:
            hc.big(c, "+2.000 AÑOS", W / 2, 1760, 120, V["accent"], lt, 0.3)
    elif sid == "s2":
        # Eratóstenes: rayos de sol paralelos sobre un arco de Tierra con dos palos; uno sin sombra, otro con sombra
        c.clear(0xFF0A1630)
        sky = skia.GradientShader.MakeLinear([(0, 500), (0, 1500)], [0xFF1A3A7A, 0xFF8AB8E8])
        c.drawRect(skia.Rect.MakeLTRB(0, 500, W, 1500), skia.Paint(Shader=sky))
        for k in range(9):
            x = 60 + k * 120
            c.drawLine(x, 520, x, 1500, stroke(with_alpha(0xFFFFE89A, 0.35 + 0.1 * math.sin(t * 3 + k)), 6))
        ocx, ocy, R = W / 2, 2900, 1550
        c.drawCircle(ocx, ocy, R, skia.Paint(Shader=skia.GradientShader.MakeRadial((ocx, ocy - R), 900,
                                                                                   [0xFFE8C88A, 0xFFB88A4A]), AntiAlias=True))
        for k, ang in enumerate((-90, -82)):
            a = math.radians(ang)
            bx, by = ocx + math.cos(a) * R, ocy + math.sin(a) * R
            tx, ty = ocx + math.cos(a) * (R + 160), ocy + math.sin(a) * (R + 160)
            c.drawLine(bx, by, tx, ty, stroke(0xFF3A2010, 14))
            if k == 1:
                sh = ease_out(clamp(lt / 1.2))
                c.drawLine(bx, by, bx - 60 * sh, by - 3 * sh, stroke(with_alpha(0xFF2A1A0A, 0.8), 12))
            K.tag(c, tx, ty - 60, ("SIENA", "ALEJANDRÍA")[k], 1.0, accent=WHITE, size=28)
        hc.big(c, "~240 a.C.", W / 2, 1720, 120, V["accent"], lt, 0.2)
    elif sid in ("s3", "s4"):
        parchment(c, t)
        # mapa: Europa a la derecha, Asia a la izquierda, océano enorme; el barco cruza
        c.drawRect(skia.Rect.MakeXYWH(80, 760, W - 160, 700), fill(with_alpha(0xFF4A7A9A, 0.35)))
        c.drawRect(skia.Rect.MakeXYWH(80, 760, W - 160, 700), stroke(0xFF6A4A2A, 5))
        k = ease_in_out(clamp(lt / 4.0))
        ship(c, lerp(W - 200, 260, k), 1240, 0.8, t)
        if sid == "s3":
            K.tag(c, W / 2, 1600, "COLÓN: «LA TIERRA ES MÁS PEQUEÑA»", lt - 0.3, accent=0xFFFF7A3A, size=30)
            K.tag(c, W / 2, 1700, "LOS SABIOS: «NO, ES MÁS GRANDE»", lt - 1.0, accent=GREEN, size=30)
        else:
            hc.stamp(c, "AMÉRICA EN MEDIO", W / 2, 1650, lt, 0.8, 90, col=0xFF1A6A3A)
    elif sid == "s5":
        parchment(c, t)
        c.save(); c.translate(W / 2, 1200); c.rotate(-3 + math.sin(t) * 1.5)
        c.drawRect(skia.Rect.MakeXYWH(-320, -420, 640, 840), fill(0xFF5A1A1A))
        c.drawRect(skia.Rect.MakeXYWH(-290, -390, 580, 780), stroke(0xFFE0C070, 6))
        draw_text(c, "COLÓN", 0, -120, 80, 0xFFE0C070, shadow=False)
        draw_text(c, "W. IRVING", 0, 0, 56, 0xFFE0C070, shadow=False)
        c.restore()
        hc.big(c, "1828", W / 2, 1770, 160, V["accent"], lt, 0.2)
    else:
        c.clear(0xFF020308)
        ST.draw(c, t, camx=t * 10, alpha=0.8)
        R = 380
        S.draw_planet(c, W / 2, 1250, R, S.render(2 * R, DAY, spin=t * 0.15, light=L, clouds=CLOUDS, gain=1.1))
        S.atmosphere(c, W / 2, 1250, R)


V404 = dict(slug="404_colon_tierra_plana_mito", accent=0xFFFFC870, drone=0.025, scene=s_colon, tease="TE LO ENSEÑARON MAL", segs=[
    dict(id="h", who="nar", say="Te enseñaron que en la época de Colón creían que la Tierra era plana. Es falso.",
         cap="¿En la época de Colón | creían que la Tierra | era *PLANA*? *FALSO*", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Los sabios ya sabían que era redonda desde hacía casi dos mil años.",
         cap="Ya sabían que era | *redonda* desde hacía | casi *2.000 años*"),
    dict(id="s2", who="nar", cut=True, say="Hacia el doscientos cuarenta antes de Cristo, el griego Eratóstenes midió su tamaño solo con la sombra de unos palos. Y casi acertó.",
         cap="Hacia el *240 a.C.*, | *Eratóstenes* la midió | con *sombras*"),
    dict(id="s3", who="nar", cut=True, say="La discusión con Colón no era la forma, sino el tamaño. Él creía que la Tierra era mucho más pequeña. Y los expertos tenían razón.",
         cap="La pelea era el *TAMAÑO*: | Colón la creía pequeña… | y *se equivocaba*"),
    dict(id="s4", who="nar", cut=True, say="Si no se hubiera topado con América por el camino, se habría quedado sin comida mucho antes de llegar a Asia.",
         cap="Si no se topa con | *AMÉRICA*… | se queda *sin comida*"),
    dict(id="s5", who="nar", cut=True, say="El mito se hizo famoso en mil ochocientos veintiocho, con una biografía de Colón muy novelada del escritor Washington Irving.",
         cap="El mito se hizo famoso | en *1828*, con una biografía | *novelada* de Colón"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo enseñaron así en el colegio? Comenta. Y sígueme para más mitos que te tragaste en clase.",
         cap="¿Te lo enseñaron así? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 405 Lista: 3 cosas que hace tu cuerpo mientras duermes
def night_bg(c, t):
    g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF040818, 0xFF0A1A3A, 0xFF1A1A4A])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    ST.draw(c, t, camx=t * 6, alpha=0.6, band=False)
    glow(c, 880, 700, 260, 0xFFBFD4FF, 0.3)
    c.drawCircle(880, 700, 90, fill(0xFFF4F0E0))
    c.drawCircle(920, 670, 80, fill(0xFF081430))  # luna creciente


def s_dormir(c, t, P, V):
    sid, lt = seg(P, t)
    night_bg(c, t)
    if sid in ("h", "s1", "s2"):
        hc.brain(c, W / 2, 1180, 1.2, t)
        if sid in ("s1", "s2"):
            # líquido que barre: partículas azules entre los pliegues
            r = random.Random(1)
            for k in range(120):
                ph = (t * 0.35 + r.random()) % 1.0
                x = W / 2 - 380 + ph * 760
                y = 1180 + math.sin(ph * 9 + k) * 220 * r.random()
                c.drawCircle(x, y, r.uniform(3, 7), fill(with_alpha(0xFF6FD6FF, 0.75 * math.sin(ph * math.pi))))
            if sid == "s2":
                K.counter(c, t, lt - 0.1, lambda p: f"+{int(round(60 * p))} %", "ESPACIO ENTRE NEURONAS", V["accent"], y=1620)
            else:
                K.tag(c, W / 2, 1620, "SE «LAVA» POR DENTRO", lt - 0.3, accent=V["accent"], size=38)
    elif sid in ("s3", "s4"):
        sacc = math.sin(t * 22) * 60 * (1 if int(t * 3) % 2 else -1)  # movimientos rápidos de ojos (REM)
        c.save(); c.translate(sacc * 0.0, 0)
        hc.eye(c, W / 2, 1130, 230, t * 6)
        c.restore()
        # cadenas de 'desconexión' en músculos: candados
        if sid == "s4":
            for k in range(3):
                x = W / 2 - 300 + k * 300
                y = 1580
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 55, y - 30, 110, 90), 16, 16), fill(0xFFFFB84D))
                arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(x - 38, y - 85, 76, 100), 180, 180)
                c.drawPath(arc, stroke(0xFFE0E0E8, 14))
            hc.big(c, "PARALIZADO", W / 2, 1800, 110, 0xFFFF3B4A, lt, 0.2)
        else:
            K.tag(c, W / 2, 1600, "FASE REM: SUEÑAS", lt - 0.3, accent=V["accent"], size=40)
    elif sid in ("s5", "s6"):
        # caída: estrellas que suben rápido (sensación de caer) y 'sacudida'
        fall = sid == "s5"
        r = random.Random(9)
        for k in range(80):
            x = r.uniform(0, W)
            y = (r.uniform(0, H) - t * (900 if fall else 80)) % H
            c.drawLine(x, y, x, y + (60 if fall else 4), stroke(with_alpha(WHITE, 0.5), 3))
        jolt = math.exp(-((lt - 1.5) % 3.0) * 6) if sid == "s6" else 0
        c.save(); c.translate(0, -jolt * 60)
        hc.brain(c, W / 2, 1180, 1.1, t)
        c.restore()
        if sid == "s6":
            hc.stamp(c, "¡BOTE!", W / 2, 1650, lt, 1.5, 120, col=0xFFFF3B4A)
        else:
            K.tag(c, W / 2, 1650, "SENSACIÓN DE CAER", lt - 0.3, accent=V["accent"], size=40)
    else:
        hc.brain(c, W / 2, 1180, 1.1, t)
    items = {"s1": 1, "s2": 1, "s3": 2, "s4": 2, "s5": 3, "s6": 3}
    if sid in items:
        n = items[sid]
        for k in range(3):
            on = k + 1 <= n
            col = V["accent"] if k + 1 == n else (with_alpha(WHITE, 0.5) if on else with_alpha(WHITE, 0.18))
            c.drawCircle(W / 2 - 120 + k * 120, 1880, 34, fill(col))
            draw_text(c, str(k + 1), W / 2 - 120 + k * 120, 1894, 40, INK, shadow=False)


V405 = dict(slug="405_tres_cosas_dormir", accent=0xFF9AB8FF, drone=0.03, scene=s_dormir, tease="LA 2 DA UN POCO DE MIEDO", segs=[
    dict(id="h", who="nar", say="Tres cosas que hace tu cuerpo mientras duermes. La segunda da un poco de miedo.",
         cap="*3 cosas* que hace | tu cuerpo *mientras duermes*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Uno. Tu cerebro se lava. Un líquido lo recorre por dentro y arrastra los desechos del día.",
         cap="*UNO*: tu cerebro | *se lava* por dentro"),
    dict(id="s2", who="nar", say="En dos mil trece, en la Universidad de Rochester, vieron en ratones que al dormir el espacio entre neuronas crece un sesenta por ciento para dejarlo pasar.",
         cap="*2013*, en ratones: al dormir, | el espacio entre neuronas | crece un *60 %*"),
    dict(id="s3", who="nar", cut=True, say="Dos. Cuando sueñas, tus ojos se mueven rápido bajo los párpados…",
         cap="*DOS*: cuando sueñas, | tus ojos se mueven | *muy rápido*…"),
    dict(id="s4", who="nar", say="… pero el resto de tu cuerpo queda paralizado. Tu cerebro desconecta los músculos para que no hagas lo que estás soñando.",
         cap="… y tu cuerpo queda | *PARALIZADO*, para que no | hagas lo que sueñas"),
    dict(id="s5", who="nar", cut=True, say="Tres. Justo al quedarte dormido, a veces sientes que caes…",
         cap="*TRES*: al dormirte, | a veces sientes | que *CAES*…"),
    dict(id="s6", who="nar", say="… y das un bote en la cama. Se llama sacudida hípnica. Es normal, y le pasa a casi todo el mundo.",
         cap="… y das un *BOTE*. | *Sacudida hípnica*. | Le pasa a casi todos"),
    dict(id="cta", who="nar", cut=True, say="¿Te ha pasado la tercera? Comenta sí o no. Y sígueme para la próxima lista.",
         cap="¿Te ha pasado la 3? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 406 Test: brazo flotante (Kohnstamm)
def arm(c, sx, sy, ang, t, L1=430, L2=400, wid=120):
    """Brazo semirrealista visto de frente: hombro en (sx, sy), ang en grados desde la vertical hacia fuera."""
    c.save(); c.translate(sx, sy); c.rotate(-ang)
    sh = skia.GradientShader.MakeLinear([(-wid / 2, 0), (wid / 2, 0)], [hc.SKIN[2], hc.SKIN[0], hc.SKIN[1], hc.SKIN[2]], [0, 0.35, 0.7, 1])
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-wid / 2, 0, wid, L1 + L2), wid / 2, wid / 2)
    c.drawRRect(r.makeOffset(10, 14), fill(0x44000000))
    c.drawRRect(r, skia.Paint(Shader=sh, AntiAlias=True))
    # mano (dorso)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-wid * 0.62, L1 + L2 - 40, wid * 1.24, 170), 50, 50),
                skia.Paint(Shader=sh, AntiAlias=True))
    for k in range(4):
        c.drawLine(-wid * 0.45 + k * wid * 0.3, L1 + L2 + 60, -wid * 0.45 + k * wid * 0.3, L1 + L2 + 120,
                   stroke(with_alpha(hc.SKIN[2], 0.6), 4))
    c.restore()


def s_brazo(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF2A2A30)
    wall = skia.GradientShader.MakeLinear([(0, 0), (W, 0)], [0xFF4A4A54, 0xFF6A6A74, 0xFF4A4A54])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=wall))
    # marco de puerta de madera a la derecha
    fx = 830
    c.drawRect(skia.Rect.MakeXYWH(fx, 0, 90, H), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(fx, 0), (fx + 90, 0)], [0xFF6A4424, 0xFFA06A3A, 0xFF5A3A1A])))
    for k in range(12):
        c.drawLine(fx + 10 + k * 7, 0, fx + 12 + k * 7, H, stroke(with_alpha(0xFF3A2410, 0.25), 2))
    sx, sy = 560, 620
    if sid in ("h", "s1"):
        ang = 8 + math.sin(t * 1.2) * 2 if sid == "s1" else lerp(8, 70, 0.5 + 0.5 * math.sin(t * 1.5))
    elif sid == "s2":
        ang = 20 + math.sin(t * 30) * 0.6  # empujando: tiembla
    elif sid in ("s3", "s4"):
        ang = lerp(6, 70, ease_out(clamp(lt / 3.0))) if sid == "s3" else 66 + math.sin(t * 1.3) * 4
    else:
        ang = 10 + math.sin(t) * 3
    # torso con camiseta a la izquierda y manga sobre el hombro (que se lea como un brazo real)
    tor = skia.GradientShader.MakeLinear([(sx - 500, 0), (sx + 40, 0)], [0xFF1A3A6A, 0xFF2A5A9A, 0xFF1A3A6A])
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx - 560, sy - 140, 590, 1600), 120, 120), skia.Paint(Shader=tor, AntiAlias=True))
    arm(c, sx, sy, ang, t)
    c.save(); c.translate(sx, sy); c.rotate(-ang)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -60, 160, 260), 70, 70), skia.Paint(Shader=tor, AntiAlias=True))
    c.restore()
    if sid == "s2":
        for k in range(4):  # ondas de fuerza contra el marco
            rr = ((t * 260 + k * 60) % 240)
            c.drawCircle(fx, 1040, rr, stroke(with_alpha(0xFFFF8A3A, 0.6 * (1 - rr / 240)), 6))
        frac = clamp(lt / 3.6)
        hc.timer(c, 300, 1500, 110, frac, str(max(1, 30 - int(frac * 30))), V["accent"])
        K.tag(c, 300, 1680, "30 SEGUNDOS", lt - 0.3, accent=V["accent"], size=34)
    if sid == "h":
        K.tag(c, 330, 1700, "HAZLO AHORA", lt - 0.3, accent=V["accent"], size=44)
    if sid == "s3":
        for k in range(3):  # trazos de 'flotar'
            y = 1500 - k * 60 - (t * 120 % 60)
            c.drawLine(250, y, 330, y - 30, stroke(with_alpha(WHITE, 0.5), 5))
        hc.stamp(c, "¡SUBE SOLO!", 330, 1750, lt, 1.2, 90, col=0xFFFF3B4A)
    if sid == "s4":
        hc.big(c, "1915", 330, 1650, 160, V["accent"], lt, 0.2)
        K.tag(c, 330, 1800, "OSKAR KOHNSTAMM", lt - 0.5, accent=WHITE, size=34)
    if sid == "s5":
        hc.brain(c, 300, 1550, 0.6, t)
        glow(c, 300, 1550, 200, 0xFFFF8A3A, 0.3 + 0.2 * math.sin(t * 6))


V406 = dict(slug="406_brazo_flotante", accent=0xFFFF8A3A, drone=0.02, scene=s_brazo, tease="HAZLO MIENTRAS LO VES",
            send="ENVÍASELO A ALGUIEN Y QUE LO PRUEBE", segs=[
    dict(id="h", who="nar", say="Haz esto y tu brazo va a subir solo, como si flotara.",
         cap="Haz esto y tu brazo | va a *SUBIR SOLO*", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Ponte de pie junto al marco de una puerta, con el brazo estirado hacia abajo.",
         cap="De pie junto al | *marco de una puerta*, | brazo estirado"),
    dict(id="s2", who="nar", cut=True, say="Empuja el marco hacia fuera con el dorso de la mano, con fuerza, durante treinta segundos. Pausa el vídeo si quieres.",
         cap="*EMPUJA* el marco | con el dorso de la mano | *30 segundos*", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Ahora sepárate y relaja el brazo del todo. ¿Lo notas? Sube solo.",
         cap="Ahora sepárate y *relaja*… | ¿lo notas? | *SUBE SOLO*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Se llama fenómeno de Kohnstamm. Lo describió el médico alemán Oskar Kohnstamm en mil novecientos quince.",
         cap="*Fenómeno de Kohnstamm*: | lo describió | en *1915*"),
    dict(id="s5", who="nar", cut=True, say="Tu cerebro sigue mandando la orden de empujar un rato después de que paras. Y como ya no hay pared, el brazo sube.",
         cap="Tu cerebro *sigue* | mandando la orden… | y sin pared, *SUBE*"),
    dict(id="cta", who="nar", cut=True, say="¿Te ha subido? Comenta sí o no. Y sígueme para más trucos que engañan a tu cerebro.",
         cap="¿Te ha subido? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== Ilusiones T2: fondo común
SERIE = "ILUSIONES IMPOSIBLES T2 · PARTE {}/3"


def ilu_bg(c, t, seed):
    hc.aurora(c, t, 0xFF1A2A6A, 0xFF4A1A5A, seed=seed)


# ====================================================================== 407 T2 P1: paralelogramo de Sander
def s_sander(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 407)
    Lb, s, h, m = 760, -200, 520, 580
    ox, oy = W / 2 - (Lb + s) / 2 - 40, 1500
    A = (ox, oy); B = (ox + Lb, oy); C = (ox + Lb + s, oy - h); D = (ox + s, oy - h)
    M0 = (ox + m, oy); M1 = (ox + m + s, oy - h)
    fade = 1.0
    if sid == "s3":
        fade = 1 - ease_in_out(clamp(lt / 1.0))
    elif sid in ("s4",):
        fade = 0.0
    elif sid in ("s5", "cta"):
        fade = 1.0
    sw = math.sin(t * 0.7) * 6
    c.save(); c.translate(sw, 0)
    if fade > 0:
        pth = skia.Path(); pth.moveTo(*A); pth.lineTo(*B); pth.lineTo(*C); pth.lineTo(*D); pth.close()
        c.drawPath(pth, fill(with_alpha(WHITE, 0.08 * fade)))
        c.drawPath(pth, stroke(with_alpha(WHITE, 0.95 * fade), 9))
        c.drawLine(*M0, *M1, stroke(with_alpha(WHITE, 0.95 * fade), 9))
    left_end = M1
    d1 = (A, left_end)
    d2 = (M1, B)
    if sid == "s2":  # giro de la diagonal izquierda sobre la derecha
        k = ease_in_out(clamp(lt / 1.4))
        # la diagonal izquierda (A->M1) se refleja respecto a la vertical por M1 => coincide con (M1->B)
        ax = lerp(A[0], B[0], k); ay = A[1]
        d1 = ((ax, ay), M1)
    c.drawLine(*d1[0], *d1[1], stroke(0xFF3AC8FF, 16))
    c.drawLine(*d2[0], *d2[1], stroke(0xFFFF5A7A, 16))
    c.restore()
    if sid == "h":
        K.tag(c, ox + 120, oy + 90, "AZUL", lt - 0.2, accent=0xFF3AC8FF, size=34)
        K.tag(c, ox + Lb - 40, oy + 90, "ROSA", lt - 0.35, accent=0xFFFF5A7A, size=34)
        hc.timer(c, W / 2, 1800, 64, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2" and lt > 1.4:
        hc.stamp(c, "IGUALES", W / 2, 1750, lt, 1.4, 130, col=GREEN)
    if sid == "s4":
        hc.big(c, "1926", W / 2, 1780, 160, V["accent"], lt, 0.2)


V407 = dict(slug="407_ilusion_sander_t2p1", accent=ILU, drone=0.02, scene=s_sander, badge=SERIE.format(1), segs=[
    dict(id="h", who="nar", say="¿Qué línea es más larga, la azul o la rosa? Tienes tres segundos.",
         cap="¿Qué línea es | más *LARGA*: | la azul o la rosa?", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="La azul parece bastante más larga, ¿verdad?", cap="La *azul* parece | bastante más larga…"),
    dict(id="s2", who="nar", cut=True, say="Mira lo que pasa si la giro encima de la rosa. Miden exactamente lo mismo.",
         cap="La giro encima… | miden *EXACTAMENTE* | lo mismo", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Y si quito el dibujo de alrededor, ya se ve.", cap="Quito el dibujo… | y *ya se ve*"),
    dict(id="s4", who="nar", cut=True, say="Es el paralelogramo de Sander. Lo publicó el psicólogo alemán Friedrich Sander en mil novecientos veintiséis.",
         cap="*Paralelogramo de Sander*: | Friedrich Sander, | en *1926*"),
    dict(id="s5", who="nar", say="Tu cerebro mide la línea junto con la figura que la rodea. La azul está en la grande, y la estira.",
         cap="Tu cerebro mide la línea | *con la figura*: la azul está | en la grande… y la *ESTIRA*"),
    dict(id="cta", who="nar", cut=True, say="Temporada dos, parte uno de tres. La dos es más difícil. Sígueme para verla, y comenta si caíste.",
         cap="T2, parte *1 de 3*. | La 2 es *más difícil*. | *SÍGUEME*"),
])


# ====================================================================== 408 Experimental: ¿cuántos triángulos ves?
def tri_pts():
    apex = (W / 2, 760)
    base_y, mid_y = 1560, 1160
    xs = [W / 2 - 430, W / 2 - 120, W / 2 + 160, W / 2 + 430]  # 2 lados + 2 cevianas en la base
    base = [(x, base_y) for x in xs]
    mid = [(lerp(apex[0], x, (mid_y - apex[1]) / (base_y - apex[1])), mid_y) for x in xs]
    return apex, base, mid


def s_triangulos(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A3A5A, 0xFF3A1A5A, seed=408)
    apex, base, mid = tri_pts()
    c.save(); c.translate(math.sin(t * 0.6) * 5, 0)
    for b in base:
        c.drawLine(*apex, *b, stroke(WHITE, 10))
    c.drawLine(*base[0], *base[-1], stroke(WHITE, 10))
    c.drawLine(*mid[0], *mid[-1], stroke(WHITE, 10))
    # recuento: s3 los 6 de la base, s4 los 6 de la línea del medio
    tris = []
    for row in (base, mid):
        for i in range(4):
            for j in range(i + 1, 4):
                tris.append((apex, row[i], row[j]))
    shown = 0
    if sid == "s3":
        shown = min(6, int(lt / 0.55) + 1)
        idx = list(range(shown))
    elif sid == "s4":
        shown = 6 + min(6, int(lt / 0.55) + 1)
        idx = list(range(6, shown))
    else:
        idx = []
    if idx:
        cur = tris[idx[-1]]
        pth = skia.Path(); pth.moveTo(*cur[0]); pth.lineTo(*cur[1]); pth.lineTo(*cur[2]); pth.close()
        c.drawPath(pth, fill(with_alpha(V["accent"], 0.45)))
        c.drawPath(pth, stroke(V["accent"], 12))
    c.restore()
    if sid == "h":
        hc.timer(c, W / 2, 1800, 70, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s1":
        K.tag(c, W / 2, 1760, "COMENTA TU NÚMERO", lt - 0.2, accent=V["accent"], size=44)
    if sid in ("s3", "s4"):
        hc.big(c, str(shown), W / 2, 1800, 190, V["accent"], 1.0, 0.0)
    if sid == "s5":
        hc.stamp(c, "12", W / 2, 1780, lt, 0.2, 170, col=GREEN)


V408 = dict(slug="408_cuantos_triangulos", accent=0xFF3AC8FF, drone=0.02, scene=s_triangulos, tease="CASI NADIE ACIERTA",
            send="RETA A UN AMIGO: ENVÍASELO", segs=[
    dict(id="h", who="nar", say="¿Cuántos triángulos ves? Casi nadie acierta a la primera.",
         cap="¿Cuántos *TRIÁNGULOS* | ves?", hold=1.5),
    dict(id="s1", who="nar", cut=True, say="Cuéntalos bien. Y antes de seguir, escribe tu número en los comentarios.",
         cap="Cuéntalos… y escribe | tu número en los | *COMENTARIOS*", hold=0.8),
    dict(id="s2", who="q", cut=True, say="¿Ya? Vamos a contarlos juntos.", cap="¿Ya? | Vamos a *contarlos*"),
    dict(id="s3", who="nar", cut=True, say="Primero, los que tocan la base de abajo. Uno, dos, tres, cuatro, cinco y seis.",
         cap="Los que tocan la *base*: | uno, dos, tres… | *SEIS*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Y ahora el truco: los mismos, pero cortados por la línea del medio. Otros seis.",
         cap="El truco: los mismos, | cortados por la línea | del medio. *OTROS SEIS*", hold=0.6),
    dict(id="s5", who="nar", cut=True, say="En total, doce. La mayoría dice seis u ocho, porque solo ve los de abajo.",
         cap="Total: *12*. | Casi todos dicen | *6 u 8*"),
    dict(id="cta", who="nar", cut=True, say="¿Cuántos dijiste tú? Comenta. Y sígueme, que mañana traigo uno más difícil.",
         cap="¿Cuántos dijiste tú? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 409 T2 P2: Poggendorff
def s_poggendorff(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 409)
    x0, x1 = 370, 700   # barra vertical ancha (más ilusión)
    ang = math.radians(36)
    yL0 = 1600          # la diagonal entra por la izquierda en x=60
    yL = yL0 - (x0 - 60) * math.tan(ang)
    yTrue = yL - (x1 - x0) * math.tan(ang)
    yWrong = yTrue + 85  # el tramo correcto parece 'demasiado alto' -> el distractor va debajo
    cover = 1.0
    if sid == "s2":
        cover = 1 - ease_in_out(clamp(lt / 1.0))
    elif sid in ("s3", "s4"):
        cover = 0.0
    elif sid in ("s5", "cta"):
        cover = 1.0 if sid == "cta" else 0.0
    sw = math.sin(t * 0.7) * 5
    c.save(); c.translate(sw, 0)
    c.drawLine(60, yL0, x0, yL, stroke(0xFFFF5A7A, 14))
    endx = 1020
    col_a = 0xFFFFE04D
    col_b = 0xFF3AC8FF
    c.drawLine(x1, yWrong, endx, yWrong - (endx - x1) * math.tan(ang), stroke(col_a, 14))
    c.drawLine(x1, yTrue, endx, yTrue - (endx - x1) * math.tan(ang), stroke(col_b, 14))
    if cover < 1:  # tramo oculto: la diagonal real continúa hasta B
        c.drawLine(x0, yL, x1, yTrue, stroke(with_alpha(0xFFFF5A7A, 1 - cover), 14))
    if cover > 0:
        c.drawRect(skia.Rect.MakeLTRB(x0, 560, x1, 1950), fill(with_alpha(0xFF6A6A7A, cover)))
        c.drawRect(skia.Rect.MakeLTRB(x0, 560, x1, 1950), stroke(with_alpha(WHITE, 0.5 * cover), 4))
    c.restore()
    if sid in ("h", "s1"):
        K.tag(c, endx - 40, yWrong - (endx - x1) * math.tan(ang) + 60, "A", lt - 0.2, accent=col_a, size=40)
        K.tag(c, endx - 40, yTrue - (endx - x1) * math.tan(ang) - 60, "B", lt - 0.35, accent=col_b, size=40)
    if sid == "h":
        hc.timer(c, 820, 1780, 64, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2" and lt > 1.0:
        hc.stamp(c, "ES LA B", 760, 1780, lt, 1.0, 120, col=GREEN)
    if sid == "s4":
        hc.big(c, "1860", 780, 1780, 160, V["accent"], lt, 0.2)


V409 = dict(slug="409_ilusion_poggendorff_t2p2", accent=ILU, drone=0.02, scene=s_poggendorff, badge=SERIE.format(2), segs=[
    dict(id="h", who="nar", say="¿Qué línea continúa la rosa, la A o la B? Mira bien antes de responder.",
         cap="¿Qué línea *continúa* | la rosa: | la *A* o la *B*?", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo dice la A. Parece la única que encaja.", cap="Casi todos dicen | la *A*…"),
    dict(id="s2", who="nar", cut=True, say="Pero quito la barra gris… y la que continúa es la B.",
         cap="Quito la barra… | y es la *B*", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Si sigues la línea con el dedo, lo compruebas: es una sola recta.", cap="Síguela con el dedo: | es *una sola recta*"),
    dict(id="s4", who="nar", cut=True, say="Es la ilusión de Poggendorff. Lleva el nombre del físico alemán Johann Poggendorff, que la publicó en mil ochocientos sesenta.",
         cap="*Ilusión de Poggendorff*: | Johann Poggendorff, | en *1860*"),
    dict(id="s5", who="nar", say="Cuando una línea se esconde detrás de algo, tu cerebro calcula mal por dónde va a salir.",
         cap="Cuando una línea | se *esconde*… | tu cerebro *calcula mal*"),
    dict(id="cta", who="nar", cut=True, say="Parte dos de tres. La tres es la que más gente falla. Sígueme para verla, y comenta si elegiste la A.",
         cap="Parte *2 de 3*. | La 3 es la que *MÁS FALLAN*. | *SÍGUEME*"),
])


# ====================================================================== 410 T2 P3: Delboeuf
def disc(c, x, y, r, col):
    c.drawCircle(x, y, r, skia.Paint(Shader=skia.GradientShader.MakeRadial((x - r * 0.3, y - r * 0.3), r * 1.3,
                                                                         [lerpc(col, 0xFFFFFFFF, 0.35), col]), AntiAlias=True))


def s_delboeuf(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 410)
    r = 120
    p1, p2 = (W / 2, 950), (W / 2, 1530)
    ring = 1.0
    if sid == "s3":
        ring = 1 - ease_in_out(clamp(lt / 1.0))
    elif sid == "s4":
        ring = 0.0
    c1x, c2x = p1[0], p2[0]
    y1, y2 = p1[1], p2[1]
    if sid == "s2":
        k = ease_in_out(clamp(lt / 1.4))
        c2x = lerp(p2[0], W / 2 + 330, k); y2 = lerp(p2[1], p1[1], k)
        c1x = lerp(p1[0], W / 2 - 330, k)
    if sid == "s2" or sid == "s3" or sid == "s4":
        if sid != "s2":
            c1x, c2x, y2 = W / 2 - 250, W / 2 + 250, p1[1]
    pulse = 1 + 0.01 * math.sin(t * 3)
    if ring > 0:
        c.drawCircle(c1x, y1, r * 1.28, stroke(with_alpha(WHITE, ring), 12))
        c.drawCircle(c2x, y2, r * 2.25, stroke(with_alpha(WHITE, ring), 12))
    disc(c, c1x, y1, r * pulse, 0xFFFF8A3A)
    disc(c, c2x, y2, r * pulse, 0xFFFF8A3A)
    if sid == "h":
        K.tag(c, W / 2 + 330, y1, "ARRIBA", lt - 0.2, accent=WHITE, size=32)
        K.tag(c, W / 2 + 360, y2 + 300, "ABAJO", lt - 0.35, accent=WHITE, size=32)
        hc.timer(c, W / 2 - 360, 1850, 64, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2" and lt > 1.4:
        c.drawLine(W / 2 - 520, y1 - r, W / 2 + 520, y1 - r, stroke(with_alpha(GREEN, 0.9), 5))
        c.drawLine(W / 2 - 520, y1 + r, W / 2 + 520, y1 + r, stroke(with_alpha(GREEN, 0.9), 5))
        hc.stamp(c, "IGUALES", W / 2, 1700, lt, 1.4, 130, col=GREEN)
    if sid == "s4":
        hc.big(c, "1865", W / 2, 1500, 160, V["accent"], lt, 0.2)


V410 = dict(slug="410_ilusion_delboeuf_t2p3", accent=ILU, drone=0.02, scene=s_delboeuf, badge=SERIE.format(3), segs=[
    dict(id="h", who="nar", say="¿Qué círculo naranja es más grande, el de arriba o el de abajo? Esta la falla casi todo el mundo.",
         cap="¿Qué círculo naranja | es más *GRANDE*: | arriba o abajo?", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="El de arriba parece más grande. El de abajo parece perdido dentro de su anillo.",
         cap="El de *arriba* parece | más grande…"),
    dict(id="s2", who="nar", cut=True, say="Los pongo a la misma altura… y son exactamente iguales.",
         cap="A la misma altura… | son *EXACTAMENTE* | iguales", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Y si quito los anillos, la ilusión desaparece.", cap="Quito los anillos… | y *desaparece*"),
    dict(id="s4", who="nar", cut=True, say="Es la ilusión de Delboeuf. La describió el filósofo belga Joseph Delboeuf en mil ochocientos sesenta y cinco.",
         cap="*Ilusión de Delboeuf*: | Joseph Delboeuf, | en *1865*"),
    dict(id="s5", who="nar", say="Un anillo pegado hace que el círculo parezca más grande. Uno lejano, que parezca más pequeño. Tu cerebro nunca mide solo.",
         cap="Anillo pegado: *más grande*. | Anillo lejano: *más pequeño*. | Tu cerebro *nunca mide solo*"),
    dict(id="cta", who="nar", cut=True, say="¿Cuál de las tres te engañó más? Comenta uno, dos o tres. Y sígueme: mañana, más retos para tu cerebro.",
         cap="¿Cuál te engañó más? | Comenta *1, 2 o 3* | y *SÍGUEME*"),
])

VIDEOS = [V401, V402, V403, V404, V405, V406, V407, V408, V409, V410]


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
