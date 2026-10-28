"""Lote diario 28/10/2026 (301–310). Motor v6 (BUCLE INVISIBLE: los últimos 0,45 s se funden con el frame 0 y el audio
cae en fundido -> el reel se reinicia sin corte y suma revisionados).
Mezcla según métricas del 27/10: las ilusiones con pregunta '¿cuál es más…?' son 3/3 ganadoras (1.268–1.436) ->
SERIE EXPLÍCITA 'ILUSIONES IMPOSIBLES' partes 1–3 en la noche; mitos de animales/colegio (prometidos); 2 tests
'haz esto ahora' con el propio cuerpo; formato lista '3 cosas' (25/10: 1.633); Europa a las 12:00 (prometido; el
mediodía de espacio rinde 1.190–1.716). Serie implícita nueva: Europa -> 'mañana, Ío'."""
import math, sys, random
import numpy as np
import skia
from PIL import Image
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow, pill
from core import draw_text, font, text_w

OUT = "/home/claude/tiktok/outdaily"
TEASE = "MIRA HASTA EL FINAL"
ILU = 0xFFFFE04D


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


# ====================================================================== 301 Europa (lo prometido)
def europa_texture():
    """Textura procedural de Europa: hielo beige-blanco con 'lineae' rojizas (grietas) y manchas de caos."""
    path = S.TEX + "europa_proc.png"
    try:
        Image.open(path)
        return S.load("europa_proc.png")
    except Exception:
        pass
    w, h = 2048, 1024
    rnd = np.random.default_rng(301)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    base = np.zeros((h, w), np.float32)
    for k in range(6):
        f = 2 ** k
        ph = rnd.uniform(0, 6.28, 4)
        base += np.sin(xx / w * 6.28 * f + ph[0] + np.sin(yy / h * 6.28 * f + ph[1])) * \
            np.cos(yy / h * 3.14 * f + ph[2]) / (k + 1)
    base = (base - base.min()) / (base.max() - base.min())
    img = np.stack([0.86 + 0.08 * base, 0.82 + 0.08 * base, 0.74 + 0.06 * base], -1)
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    r = random.Random(301)
    for _ in range(140):  # lineae: curvas largas
        x, y = r.uniform(0, w), r.uniform(80, h - 80)
        a = r.uniform(0, 6.28)
        col = (int(r.uniform(120, 170)), int(r.uniform(70, 100)), int(r.uniform(50, 70)))
        wd = r.choice((1, 2, 2, 3, 4))
        pts = []
        for s in range(r.randint(20, 70)):
            a += r.uniform(-0.08, 0.08)
            x += math.cos(a) * 14; y += math.sin(a) * 7
            pts.append((x % w, y))
        for p0, p1 in zip(pts, pts[1:]):
            if abs(p0[0] - p1[0]) < 40:
                d.line([p0, p1], fill=col, width=wd)
    for _ in range(25):  # zonas de caos
        x, y, rr = r.uniform(0, w), r.uniform(150, h - 150), r.uniform(15, 50)
        d.ellipse([x - rr, y - rr * 0.7, x + rr, y + rr * 0.7], fill=(150, 105, 80))
    im.save(path)
    return S.load("europa_proc.png")


EUR = europa_texture()
JUP = S.load("jupitermap.jpg")
DAY = S.load("earth_atmos_2048.jpg")
CLOUDS = S.load("earth_clouds_1024.png", "A")
MOON = S.load("moon_1024.jpg")
ST1 = K.Stars(seed=301)


def ice_section(c, t, lt, k_ocean):
    """Corte de Europa: corteza de hielo arriba, océano abajo con burbujas y luz que se filtra."""
    top, ice_b, bot = 800, 1080, 1880
    g = skia.GradientShader.MakeLinear([(0, top), (0, ice_b)], [0xFFF4F8FF, 0xFFB8D4EE, 0xFF7AA6CC])
    c.drawRect(skia.Rect.MakeLTRB(0, top, W, ice_b), skia.Paint(Shader=g))
    r = random.Random(7)
    for _ in range(26):  # grietas del hielo
        x = r.uniform(0, W); y = r.uniform(top + 20, ice_b - 20)
        c.drawLine(x, y, x + r.uniform(-120, 120), y + r.uniform(-40, 40), stroke(with_alpha(0xFF8AA0B8, 0.6), 3))
    oc = skia.GradientShader.MakeLinear([(0, ice_b), (0, bot)], [0xFF1A5A8A, 0xFF0A2A4A, 0xFF020A18])
    c.drawRect(skia.Rect.MakeLTRB(0, ice_b, W, bot), skia.Paint(Shader=oc))
    for k in range(5):  # rayos de luz bajo el hielo
        x = 150 + k * 200 + math.sin(t * 0.6 + k) * 40
        p = skia.Path(); p.moveTo(x - 30, ice_b); p.lineTo(x + 30, ice_b); p.lineTo(x + 140, bot); p.lineTo(x - 60, bot); p.close()
        c.drawPath(p, fill(with_alpha(0xFF6FD6FF, 0.06 * k_ocean)))
    for k in range(60):  # burbujas que suben
        x = (k * 97 % W) + math.sin(t * 2 + k) * 12
        y = bot - ((t * (40 + k % 7 * 12) + k * 53) % (bot - ice_b))
        c.drawCircle(x, y, 3 + k % 4, stroke(with_alpha(WHITE, 0.35 * k_ocean), 2))
    c.drawLine(0, ice_b, W, ice_b, stroke(with_alpha(WHITE, 0.6), 4))


def s_europa(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020308)
    ST1.draw(c, t, camx=t * 14, alpha=0.9)
    L = (-0.6, 0.25, 0.76)
    if sid == "h":
        # Júpiter de fondo y Europa entrando en primer plano
        jr = 620
        S.draw_planet(c, W * 0.15, 1350, jr, S.render(2 * jr, JUP, spin=t * 0.3, light=L, gain=1.1, limb=0.35))
        er = lerp(120, 330, ease_out(clamp(lt / 3.0)))
        glow(c, W * 0.66, 1150, er * 1.6, 0xFFBFE6FF, 0.25)
        S.draw_planet(c, W * 0.66, 1150, er, S.render(2 * er, EUR, spin=t * 0.25, light=L, gain=1.15, limb=0.2))
    elif sid == "s1":
        er = 360
        S.draw_planet(c, W / 2 - 180, 1250, er, S.render(2 * er, EUR, spin=t * 0.25, light=L, gain=1.15, limb=0.2))
        mr = er * 3474 / 3122
        S.draw_planet(c, W / 2 + 270, 1250 + (er - mr) * 0.0, mr * 0.55,
                      S.render(2 * mr * 0.55, MOON, spin=0.3, light=L, gain=1.2))
        K.tag(c, W / 2 - 180, 1680, "EUROPA · 3.100 km", lt - 0.3, accent=0xFFBFE6FF, size=34)
        K.tag(c, W / 2 + 270, 1580, "NUESTRA LUNA", lt - 0.6, accent=WHITE, size=30)
    elif sid in ("s2", "s3"):
        ice_section(c, t, lt, 1.0 if sid == "s3" else ease_out(clamp(lt / 1.0)))
        if sid == "s2":
            K.counter(c, t, lt - 0.2, lambda p: f"{int(round(15 + 10 * p))} km", "DE HIELO ENCIMA", V["accent"], y=960)
        else:
            K.counter(c, t, lt - 0.2, lambda p: f"×{K.fmt(2 * p, 0)}", "EL AGUA DE TODOS NUESTROS OCÉANOS", 0xFF6FD6FF, y=1450)
    elif sid == "s4":
        er = 300
        S.draw_planet(c, W / 2, 1150, er, S.render(2 * er, EUR, spin=t * 0.25, light=L, gain=1.15, limb=0.2))
        # Júpiter tira de Europa: flechas de marea y calor
        for k in range(6):
            a = k * math.pi / 3 + t * 0.6
            x1, y1 = W / 2 + math.cos(a) * (er + 40), 1150 + math.sin(a) * (er + 40)
            x2, y2 = W / 2 + math.cos(a) * (er + 120 + 15 * math.sin(t * 5)), 1150 + math.sin(a) * (er + 120 + 15 * math.sin(t * 5))
            c.drawLine(x1, y1, x2, y2, stroke(with_alpha(0xFFFF9A4A, 0.85), 10))
        glow(c, W / 2, 1150, er * 0.7, 0xFFFF7A3A, 0.25 + 0.1 * math.sin(t * 4))
        K.tag(c, W / 2, 1600, "JÚPITER LA ESTIRA Y LA CALIENTA", lt - 0.3, accent=0xFFFF9A4A, size=34)
    else:
        er = 280 if sid != "s5" else lerp(150, 300, ease_out(clamp(lt / 3)))
        S.draw_planet(c, W / 2, 1180, er, S.render(2 * er, EUR, spin=t * 0.25, light=L, gain=1.15, limb=0.2))
        # sonda acercándose
        px = lerp(-80, W / 2 + er + 90, ease_out(clamp(lt / 2.5))) if sid == "s5" else W / 2 + er + 90 + math.sin(t) * 10
        py = 760 + math.sin(t * 1.5) * 10
        c.drawRect(skia.Rect.MakeXYWH(px - 160, py - 18, 320, 36), fill(0xFF3A5A9A))
        for k in range(8):
            c.drawLine(px - 160 + k * 40, py - 18, px - 160 + k * 40, py + 18, stroke(0xFF1A2A4A, 3))
        c.drawRect(skia.Rect.MakeXYWH(px - 30, py - 40, 60, 80), fill(0xFFD8D8E0))
        c.drawCircle(px, py - 60, 34, stroke(0xFFE8E8F0, 8))
        if sid == "s5":
            K.tag(c, W / 2, 1600, "EUROPA CLIPPER · 14 OCT 2024", lt - 0.3, accent=V["accent"], size=34)
        if sid == "s6":
            hc.big(c, "2030", W / 2, 1640, 170, V["accent"], lt, 0.2)
        if sid == "cta":
            for k in range(14):  # Ío asomando: puntos volcánicos
                pass
            ir = 110
            ix = lerp(W + 150, W - 200, ease_out(clamp(lt / 1.2)))
            S.draw_planet(c, ix, 1650, ir, S.render(2 * ir, MOON, spin=1.0, light=L, gain=1.25))
            c.drawCircle(ix, 1650, ir, fill(with_alpha(0xFFFFC23A, 0.45)))


V301 = dict(slug="301_europa_oceano", accent=0xFFBFE6FF, drone=0.035, scene=s_europa, badge="LO PROMETIDO · JÚPITER PARTE 2", segs=[
    dict(id="h", who="nar", say="Esta luna de Júpiter podría tener más agua que toda la Tierra. Y está escondida.",
         cap="Esta luna podría tener | *MÁS AGUA* | que toda la Tierra", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Se llama Europa. Es un poco más pequeña que nuestra Luna, unos tres mil cien kilómetros.",
         cap="Se llama *Europa*. | Algo más *pequeña* | que nuestra Luna"),
    dict(id="s2", who="nar", cut=True, say="Por fuera es una bola de hielo. Pero debajo de quince a veinticinco kilómetros de hielo…",
         cap="Por fuera, *hielo*. | Pero debajo de | *15 a 25 km* de hielo…"),
    dict(id="s3", who="nar", cut=True, say="… hay un océano de agua salada. Según la NASA, podría tener el doble de agua que todos los océanos de la Tierra.",
         cap="… un *OCÉANO* salado. | Podría tener el *DOBLE* | que los de la Tierra"),
    dict(id="s4", who="nar", cut=True, say="¿Y por qué no se congela? Porque la gravedad de Júpiter la estira y la encoge sin parar, y eso la calienta por dentro.",
         cap="¿Por qué no se congela? | *Júpiter* la estira y encoge… | y la *CALIENTA*"),
    dict(id="s5", who="nar", cut=True, say="El catorce de octubre de dos mil veinticuatro, la NASA lanzó una nave solo para estudiarla: Europa Clipper.",
         cap="*14 oct 2024*: la NASA | lanzó *Europa Clipper* | solo para estudiarla"),
    dict(id="s6", who="nar", cut=True, say="Llegará en dos mil treinta. Y buscará si ese océano podría tener lo necesario para la vida.",
         cap="Llega en *2030*. | Buscará si ese océano | podría tener *VIDA*"),
    dict(id="cta", who="nar", cut=True, say="Y Júpiter tiene otra luna todavía más loca, llena de volcanes. Mañana te la enseño. Sígueme, y comenta si crees que hay vida.",
         cap="Mañana: la luna de los | *VOLCANES*. | ¿Hay vida? *COMENTA*"),
])


# ====================================================================== 302 Mito: murciélagos ciegos
def bat(c, x, y, s, t, ph=0.0, col=0xFF0A0A12):
    f = math.sin(t * 9 + ph)
    c.save(); c.translate(x, y); c.scale(s, s)
    for side in (-1, 1):
        p = skia.Path()
        tip_y = -40 * f
        p.moveTo(0, 0)
        p.cubicTo(side * 40, -30 + tip_y * 0.5, side * 90, -40 + tip_y, side * 140, -20 + tip_y)
        p.lineTo(side * 120, 10 + tip_y * 0.6)
        p.quadTo(side * 100, 0, side * 90, 18 + tip_y * 0.4)
        p.quadTo(side * 70, 8, side * 55, 25 + tip_y * 0.2)
        p.quadTo(side * 35, 15, 0, 22)
        p.close()
        c.drawPath(p, fill(col))
    c.drawOval(skia.Rect.MakeXYWH(-16, -22, 32, 50), fill(col))
    for side in (-1, 1):
        q = skia.Path(); q.moveTo(side * 6, -18); q.lineTo(side * 14, -36); q.lineTo(side * 14, -16); q.close()
        c.drawPath(q, fill(col))
    c.restore()


def s_bats(c, t, P, V):
    sid, lt = seg(P, t)
    g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF0A1030, 0xFF2A2050, 0xFF6A3A50])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    glow(c, 780, 900, 380, 0xFFFFF2D0, 0.35)
    c.drawCircle(780, 900, 170, fill(0xFFFFF4DC))
    c.drawCircle(730, 870, 30, fill(0xFFEDE0C0)); c.drawCircle(830, 950, 22, fill(0xFFEDE0C0))
    # árboles
    p = skia.Path(); p.moveTo(0, H)
    for x in range(0, W + 41, 40):
        p.lineTo(x, 1640 - abs(math.sin(x / 90)) * 160 - (x * 37 % 50))
    p.lineTo(W, H); p.close(); c.drawPath(p, fill(0xFF05060A))
    r = random.Random(3)
    n = 9 if sid in ("h", "s1", "cta") else 4
    for k in range(n):
        x = (r.uniform(0, W) + t * r.uniform(60, 140)) % (W + 300) - 150
        y = r.uniform(800, 1450) + math.sin(t * 1.5 + k) * 40
        bat(c, x, y, r.uniform(0.5, 1.0), t, k)
    if sid == "s2":  # ondas de ecolocación
        bx, by = W / 2, 1200
        bat(c, bx, by, 1.6, t)
        for k in range(5):
            rr = ((t * 300 + k * 120) % 600)
            c.drawCircle(bx, by, rr, stroke(with_alpha(0xFF6FD6FF, 0.6 * (1 - rr / 600)), 6))
    if sid in ("s3", "s4"):
        bx, by = W / 2, 1200
        bat(c, bx, by, 2.4, t, col=0xFF2A1E1A)
        for side in (-1, 1):  # ojos grandes del zorro volador
            glow(c, bx + side * 18 * 2.4, by - 6 * 2.4, 40, 0xFFFFD27A, 0.8)
            c.drawCircle(bx + side * 18 * 2.4 * 0.5, by - 4 * 2.4, 10, fill(0xFFFFE6A0))
        if sid == "s4":
            K.tag(c, W / 2, 1560, "ZORROS VOLADORES", lt - 0.3, accent=V["accent"], size=38)
    if sid == "h":
        hc.stamp(c, "MITO", W / 2, 1700, lt, 1.0, 140)
    if sid == "s1":
        hc.big(c, "+1.400 ESPECIES", W / 2, 1700, 110, V["accent"], lt, 0.2)
    if sid == "s5":
        hc.big(c, "0 CIEGAS", W / 2, 1700, 150, 0xFF2FD46B, lt, 0.2)


V302 = dict(slug="302_murcielagos_ciegos", accent=0xFFFFC870, drone=0.03, scene=s_bats, tease="TE LO DIJERON MAL", segs=[
    dict(id="h", who="nar", say="«Ciego como un murciélago». Lo has oído mil veces… y es mentira.",
         cap="*«Ciego como* | *un murciélago»*… | es *MENTIRA*", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Hay más de mil cuatrocientas especies de murciélago. Y ninguna es ciega.",
         cap="Hay más de *1.400 especies*… | y *NINGUNA* es ciega"),
    dict(id="s2", who="nar", cut=True, say="Muchas usan ecolocación: lanzan sonidos y escuchan el eco para cazar en la oscuridad. Pero además, ven.",
         cap="Muchas usan el *eco* | para cazar a oscuras… | pero *ADEMÁS VEN*"),
    dict(id="s3", who="nar", cut=True, say="Y algunas ni siquiera usan el eco: se guían sobre todo con la vista.",
         cap="Y algunas ni usan el eco: | se guían con | la *VISTA*"),
    dict(id="s4", who="nar", cut=True, say="Los zorros voladores, por ejemplo, tienen ojos grandes y ven muy bien con poca luz. Mejor que tú de noche.",
         cap="Los *zorros voladores* | ven de noche | *mejor que tú*"),
    dict(id="s5", who="nar", say="Así que lo correcto sería decir: ves como un murciélago. Y sería un piropo.",
         cap="Lo correcto sería: | *«ves como un murciélago»*… | y sería un *piropo*"),
    dict(id="cta", who="nar", cut=True, say="¿Lo sabías? Comenta. Y sígueme, que mañana desmonto otro mito de animales.",
         cap="¿Lo *sabías*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 303 Ilusión de Aristóteles (test)
def crossed(c, cx, cy, s, t, cross=1.0, touch=0.0, wob=0.0):
    """Índice y corazón: cruzados (cross=1) o rectos (0). touch: objeto entre las yemas."""
    c.save(); c.translate(cx, cy + math.sin(t * 2) * 6); c.scale(s, s); c.rotate(math.sin(t * 1.2) * 3 + wob)
    palm = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-150, 0, 300, 360), 120, 120)
    c.drawRRect(palm.makeOffset(10, 16), fill(0x55000000))
    c.drawRRect(palm, skia.Paint(Shader=skia.GradientShader.MakeRadial((0, 160), 280, [hc.SKIN[0], hc.SKIN[1], hc.SKIN[2]]), AntiAlias=True))
    hc.finger(c, -95, 40, -4, 170, 66, bend=1.0)   # anular doblado
    hc.finger(c, -150, 90, -8, 130, 60, bend=1.0)  # meñique doblado
    a_mid = lerp(2, -14, cross)
    a_idx = lerp(8, 26, cross)
    hc.finger(c, 45, 10, a_mid, 330, 76)    # corazón
    hc.finger(c, 115, 20, -a_idx * 0.2 + lerp(6, -18, cross), 300, 74)  # índice cruzando por delante
    c.restore()
    if touch > 0:
        glow(c, cx - 40 * s, cy - 300 * s, 70 * s, 0xFFFF3B4A, 0.9 * touch)
        glow(c, cx + 40 * s, cy - 300 * s, 70 * s, 0xFFFF3B4A, 0.9 * touch)


def s_aristoteles(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF3A1A5A, 0xFF0A3A5A, seed=33)
    if sid in ("h", "s1"):
        crossed(c, W / 2, 1150, 1.3, t, cross=ease_in_out(clamp(lt / 1.2)) if sid == "s1" else 0.0)
        if sid == "h":
            K.tag(c, W / 2, 1700, "HAZLO AHORA", lt - 0.3, accent=V["accent"], size=44)
    elif sid in ("s2", "s3"):
        crossed(c, W / 2, 1250, 1.3, t, cross=1.0, touch=1.0, wob=math.sin(t * 6) * 4)
        # canica entre las yemas
        c.drawCircle(W / 2, 1250 - 330 * 1.3 + 20, 46, skia.Paint(Shader=skia.GradientShader.MakeRadial(
            (W / 2 - 15, 1250 - 330 * 1.3), 60, [0xFFBFE6FF, 0xFF2A6AB0]), AntiAlias=True))
        if sid == "s3":
            hc.stamp(c, "¿DOS?", W / 2, 1720, lt, 0.4, 140, col=0xFFFF3B4A)
    elif sid == "s4":
        hc.big(c, "+2.300 AÑOS", W / 2, 1150, 130, V["accent"], lt, 0.2)
        K.tag(c, W / 2, 1320, "ARISTÓTELES YA LO DESCRIBIÓ", lt - 0.5, accent=WHITE, size=38)
    else:
        hc.brain(c, W / 2, 1150, 1.2, t)
        if sid == "s5":
            K.tag(c, W / 2, 1600, "ESOS LADOS NUNCA SE TOCAN", lt - 0.3, accent=V["accent"], size=38)
            K.tag(c, W / 2, 1710, "= 2 OBJETOS", lt - 0.8, accent=0xFFFF3B4A, size=38)


V303 = dict(slug="303_ilusion_aristoteles", accent=0xFFFF7AD9, drone=0.02, scene=s_aristoteles, tease="HAZLO MIENTRAS LO VES", segs=[
    dict(id="h", who="nar", say="Haz esto ahora mismo y vas a notar dos narices. Cruza los dedos índice y corazón.",
         cap="Haz esto y notarás | *DOS NARICES*. | Cruza estos dedos", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Así, con fuerza, el corazón por encima del índice.", cap="Así, *bien cruzados*", hold=0.6),
    dict(id="s2", who="nar", cut=True, say="Ahora cierra los ojos y toca la punta de tu nariz con las dos yemas a la vez. Muévelos un poco.",
         cap="Cierra los ojos y toca | la *punta de tu nariz* | con las dos yemas", hold=1.4),
    dict(id="s3", who="nar", cut=True, say="¿Lo notas? Parece que tocas dos narices distintas.", cap="¿Lo notas? | *DOS NARICES*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Se llama ilusión de Aristóteles, porque ya la describió él hace más de dos mil trescientos años.",
         cap="*Ilusión de Aristóteles*: | la describió hace | más de *2.300 años*"),
    dict(id="s5", who="nar", say="Normalmente, el lado de fuera de esos dos dedos nunca toca la misma cosa. Así que tu cerebro deduce que son dos objetos.",
         cap="Esos dos lados *nunca* | tocan lo mismo… | y tu cerebro cuenta *DOS*"),
    dict(id="cta", who="nar", cut=True, say="¿Te ha funcionado? Comenta sí o no. Y sígueme, que tengo otro truco con los dedos todavía más raro.",
         cap="¿Te funcionó? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 304 Dedo salchicha (test)
def s_salchicha(c, t, P, V):
    sid, lt = seg(P, t)
    # pared del fondo desenfocada (ladrillos suaves)
    c.clear(0xFF3A2A24)
    for i in range(30):
        for j in range(10):
            x = j * 120 + (60 if i % 2 else 0) - 60
            y = i * 66
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 4, y + 4, 112, 58), 6, 6),
                        fill(with_alpha(0xFF8A5A44 if (i * 7 + j) % 3 else 0xFF7A4A3A, 0.8)))
    c.drawRect(skia.Rect.MakeWH(W, H), fill(0x88000000))
    gap = 60 if sid in ("h", "s1") else lerp(60, 20, ease_in_out(clamp(lt / 1.0))) if sid == "s2" else 20
    y = 1250 + math.sin(t * 1.5) * 8
    blur = sid in ("s2", "s3", "s4")
    if blur:
        # cuando enfocas el fondo, los dedos se desdoblan: dos imágenes semitransparentes por ojo
        for dx, a in ((-38, 0.55), (38, 0.55)):
            c.save(); c.translate(dx, 0)
            for side in (-1, 1):
                hc.finger(c, W / 2 + side * (gap / 2 + 420), y, side * -90, 420, 110)
            c.restore()
        # la 'salchicha' flotante: solape de las dos yemas
        k = ease_out(clamp(lt / 0.8)) if sid == "s2" else 1.0
        sw = 160 + 30 * math.sin(t * 2)
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - sw / 2, y - 55, sw, 110), 55, 55)
        c.drawRRect(r, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, y - 55), (0, y + 55)],
                                                                         [hc.SKIN[0], hc.SKIN[1], hc.SKIN[2]]),
                                  AntiAlias=True, Alpha=int(255 * k)))
        glow(c, W / 2, y, 200, 0xFFFFE04D, 0.25 * k)
    else:
        for side in (-1, 1):
            hc.finger(c, W / 2 + side * (gap / 2 + 420), y, side * -90, 420, 110)
    if sid == "h":
        K.tag(c, W / 2, 1600, "A LA ALTURA DE LOS OJOS", lt - 0.4, accent=V["accent"], size=38)
    if sid == "s1":
        K.tag(c, W / 2, 1600, "SEPARADOS 1 CM", lt - 0.2, accent=V["accent"], size=40)
    if sid == "s3":
        hc.stamp(c, "UN DEDO FLOTANTE", W / 2, 1650, lt, 0.2, 90, col=0xFFFF3B4A)
    if sid == "s5":
        hc.eye(c, W / 2 - 220, 1650, 110, t)
        hc.eye(c, W / 2 + 220, 1650, 110, t)


V304 = dict(slug="304_dedo_flotante", accent=0xFFFFE04D, drone=0.02, scene=s_salchicha, tease="HAZLO MIENTRAS LO VES", segs=[
    dict(id="h", who="nar", say="Pon los dos dedos índice así, delante de tus ojos, apuntándose. Hazlo ya.",
         cap="Pon los dos *índices* | así, delante | de tus *OJOS*", hold=0.6),
    dict(id="s1", who="nar", cut=True, say="Sepáralos más o menos un centímetro.", cap="Sepáralos | *un centímetro*", hold=0.5),
    dict(id="s2", who="nar", cut=True, say="Ahora no mires los dedos: mira la pared del fondo, a través de ellos.",
         cap="No mires los dedos: | mira la *PARED* | del fondo", hold=1.2),
    dict(id="s3", who="nar", cut=True, say="¿Lo ves? Aparece un trocito de dedo flotando en el aire, como una salchicha.",
         cap="Aparece un *dedo flotante*… | como una *SALCHICHA*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Y si separas un poco más los dedos, la salchicha se encoge.", cap="Sepáralos más… | y *se encoge*", hold=0.5),
    dict(id="s5", who="nar", cut=True, say="Pasa porque cada ojo ve los dedos desde un ángulo distinto. Al mirar lejos, tu cerebro junta las dos imágenes y se inventa un trozo que no existe.",
         cap="Cada *ojo* los ve distinto. | Tu cerebro junta las dos… | y se *INVENTA* un trozo"),
    dict(id="cta", who="nar", cut=True, say="¿Te ha salido la salchicha? Comenta. Y sígueme para más trucos que engañan a tu cerebro.",
         cap="¿Te salió la *salchicha*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 305 Lista: 3 cosas que hace tu cerebro
def s_cerebro3(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF1A3A6A, 0xFF5A1A4A, seed=305)
    pulse = 0.5 + 0.5 * math.sin(t * 5)
    if sid in ("h", "s1", "s2"):
        hc.brain(c, W / 2, 1150, 1.25, t)
        glow(c, W / 2, 1150, 420, 0xFFFFB84D, 0.25 + 0.2 * pulse)
        if sid == "s1":
            hc.big(c, "2 % DEL PESO", W / 2, 1560, 100, WHITE, lt, 0.1)
        if sid == "s2":
            K.counter(c, t, lt - 0.1, lambda p: f"{int(round(20 * p))} %", "DE TU ENERGÍA", V["accent"], y=1600)
    elif sid in ("s3", "s4"):
        hc.brain(c, W / 2, 1150, 1.25, t)
        # sonda quirúrgica + 'sin dolor'
        x = W / 2 + 120 + math.sin(t * 2) * 10
        c.drawLine(x + 300, 700, x, 1050, stroke(0xFFD8DCE4, 18))
        c.drawCircle(x, 1050, 14, fill(0xFF6FD6FF))
        glow(c, x, 1050, 90, 0xFF6FD6FF, 0.5 * pulse)
        if sid == "s4":
            hc.stamp(c, "0 RECEPTORES DE DOLOR", W / 2, 1620, lt, 0.2, 70, col=0xFF2FD46B)
    elif sid in ("s5", "s6"):
        bl = sid == "s5" and (t * 1.6) % 1.0 < 0.12
        hc.eye(c, W / 2 - 50, 1150, 230, t)
        if sid == "s6" or bl:
            # párpado bajando (parpadeo)
            k = 1.0 if bl else (0.5 + 0.5 * math.sin(t * 9)) ** 6
            c.drawRect(skia.Rect.MakeXYWH(0, 1150 - 260, W, 520 * k), fill(0xFFB8735A))
        if sid == "s5":
            K.counter(c, t, lt - 0.1, lambda p: str(int(round(15 * p))), "PARPADEOS POR MINUTO", V["accent"], y=1600)
        else:
            hc.big(c, "Y NO LO VES", W / 2, 1620, 120, V["accent"], lt, 0.2)
    else:
        hc.brain(c, W / 2, 1150, 1.25, t)
    # numeración de la lista siempre visible abajo
    items = {"s1": 1, "s2": 1, "s3": 2, "s4": 2, "s5": 3, "s6": 3}
    if sid in items:
        n = items[sid]
        for k in range(3):
            on = k + 1 <= n
            col = V["accent"] if k + 1 == n else (with_alpha(WHITE, 0.5) if on else with_alpha(WHITE, 0.18))
            c.drawCircle(W / 2 - 120 + k * 120, 1820, 34, fill(col))
            draw_text(c, str(k + 1), W / 2 - 120 + k * 120, 1834, 40, INK, shadow=False)


V305 = dict(slug="305_tres_cosas_cerebro", accent=0xFFFFB84D, drone=0.025, scene=s_cerebro3, tease="LA 3 ES LA MÁS RARA", segs=[
    dict(id="h", who="nar", say="Tres cosas que hace tu cerebro sin que te des cuenta. La tercera está pasando ahora mismo.",
         cap="*3 cosas* de | tu cerebro… | la 3ª pasa *AHORA*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Uno. Pesa solo un dos por ciento de tu cuerpo…", cap="*UNO*: pesa solo un *2 %* | de tu cuerpo…"),
    dict(id="s2", who="nar", say="… pero se gasta alrededor del veinte por ciento de tu energía. Aunque estés sin hacer nada.",
         cap="… pero gasta el *20 %* | de tu energía. | Aunque no hagas *NADA*"),
    dict(id="s3", who="nar", cut=True, say="Dos. Tu cerebro no puede sentir dolor. No tiene receptores de dolor.",
         cap="*DOS*: tu cerebro | *no siente dolor*"),
    dict(id="s4", who="nar", say="Por eso hay operaciones de cerebro con el paciente despierto, hablando con el cirujano.",
         cap="Por eso hay operaciones | con el paciente *DESPIERTO*, | hablando"),
    dict(id="s5", who="nar", cut=True, say="Tres. Parpadeas unas quince veces por minuto, y cada parpadeo te deja a oscuras una décima de segundo.",
         cap="*TRES*: parpadeas unas | *15 veces* por minuto, | y te quedas *a oscuras*"),
    dict(id="s6", who="nar", say="Pero nunca ves esa oscuridad. Tu cerebro la borra. Lo acabas de hacer varias veces viendo este vídeo.",
         cap="Pero tu cerebro | *BORRA* esa oscuridad. | Lo hizo mientras veías esto"),
    dict(id="cta", who="nar", cut=True, say="¿Cuál te ha sorprendido más, la uno, la dos o la tres? Comenta. Y sígueme para la próxima lista.",
         cap="¿Cuál te sorprendió: | *1, 2 o 3*? *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 306 Mito: camaleón
def scales(c, t, phase_col, k_nano=0.0):
    """Piel de escamas hexagonales que cambian de color en ola."""
    R = 46
    for i in range(-1, 26):
        for j in range(-1, 14):
            x = j * R * 1.75 + (R * 0.87 if i % 2 else 0)
            y = i * R * 1.5 + 650
            if y > 1950:
                continue
            wv = 0.5 + 0.5 * math.sin(t * 2 - (x + y) / 260)
            col = phase_col(wv, x, y)
            p = skia.Path()
            for a in range(6):
                ang = math.pi / 6 + a * math.pi / 3
                pt = (x + math.cos(ang) * R * 0.92, y + math.sin(ang) * R * 0.92)
                (p.moveTo if a == 0 else p.lineTo)(*pt)
            p.close()
            c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeRadial((x - 10, y - 12), R * 1.1,
                                                                           [with_alpha(WHITE, 0.6), col, with_alpha(INK, 1)],
                                                                           [0, 0.45, 1]), AntiAlias=True))


def lerpc(a, b, k):
    ch = [int(lerp((a >> s) & 255, (b >> s) & 255, k)) for s in (16, 8, 0)]
    return 0xFF000000 | (ch[0] << 16) | (ch[1] << 8) | ch[2]


def s_camaleon(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF071008)
    if sid in ("h", "s1"):
        scales(c, t, lambda w, x, y: lerpc(0xFF2E9A3A, 0xFF8ACD3A, w))
        if sid == "h":
            hc.stamp(c, "MITO", W / 2, 1650, lt, 1.0, 140)
    elif sid == "s2":
        scales(c, t, lambda w, x, y: lerpc(0xFF2E9A3A, 0xFFFF7A2A, ease_in_out(clamp(lt / 1.5)) * w))
        K.tag(c, W / 2, 1650, "ESTOY ENFADADO · NO TE ACERQUES", lt - 0.5, accent=0xFFFF7A2A, size=32)
    elif sid == "s3":
        scales(c, t, lambda w, x, y: lerpc(0xFF3A3A3A, 0xFF1A1A1A, w))
        K.tag(c, W / 2, 1650, "TENGO FRÍO: ME OSCUREZCO", lt - 0.3, accent=0xFF6FD6FF, size=34)
    elif sid in ("s4", "s5"):
        c.clear(0xFF04060C)
        # nanocristales: red que se expande y cambia de color reflejado
        k = 0.5 + 0.5 * math.sin(t * 1.4)
        sp = lerp(70, 110, k)
        col = lerpc(0xFF3A8AFF, 0xFFFFB03A, k)
        for i in range(-12, 13):
            for j in range(-8, 9):
                x = W / 2 + j * sp + (sp / 2 if i % 2 else 0)
                y = 1180 + i * sp * 0.87
                if 700 < y < 1700:
                    c.drawCircle(x, y, 16, skia.Paint(Shader=skia.GradientShader.MakeRadial((x - 5, y - 5), 18, [WHITE, col]), AntiAlias=True))
        glow(c, W / 2, 1180, 400, col, 0.25)
        if sid == "s4":
            K.tag(c, W / 2, 1780, "NANOCRISTALES · GINEBRA 2015", lt - 0.3, accent=V["accent"], size=34)
        else:
            K.tag(c, W / 2, 1780, "SEPARADOS = AMARILLO · JUNTOS = AZUL", lt - 0.3, accent=col, size=30)
    else:
        scales(c, t, lambda w, x, y: lerpc(0xFF2E9A3A, 0xFF3AC8FF, w))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 700), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, 500), (0, 700)], [0xFF071008, 0x00071008])))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 520), fill(0xFF071008))


V306 = dict(slug="306_camaleon_mito", accent=0xFF8ACD3A, drone=0.025, scene=s_camaleon, tease="TE LO DIJERON MAL", segs=[
    dict(id="h", who="nar", say="Los camaleones no cambian de color para esconderse. Te lo contaron al revés.",
         cap="El camaleón *NO* | cambia de color | para *esconderse*", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Su color normal ya les camufla bastante bien entre las hojas. El cambio sirve para otra cosa.",
         cap="Su color normal *ya* | les camufla. El cambio | sirve para *OTRA COSA*"),
    dict(id="s2", who="nar", cut=True, say="Sobre todo, para hablar. Un macho que se pone de colores fuertes le está diciendo a otro: no te acerques.",
         cap="Sobre todo, para *HABLAR*: | colores fuertes = | *«no te acerques»*"),
    dict(id="s3", who="nar", cut=True, say="Y también para controlar su temperatura: más oscuro, absorbe más calor.",
         cap="Y para la *temperatura*: | más oscuro = | absorbe *más calor*"),
    dict(id="s4", who="nar", cut=True, say="En dos mil quince, un equipo de la Universidad de Ginebra descubrió cómo lo hacen: con nanocristales dentro de la piel.",
         cap="*2015*, Universidad de *Ginebra*: | lo hacen con | *NANOCRISTALES*"),
    dict(id="s5", who="nar", say="Al separar o juntar esos cristales, cambia la luz que reflejan. No es pintura: es física.",
         cap="Los separan o los juntan… | y cambia la *luz* que reflejan. | Es *FÍSICA*"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo creías? Comenta. Y sígueme, que mañana desmonto otro mito de animales.",
         cap="¿Te lo *creías*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 307 Ilusiones imposibles P1: Ponzo
def rails(c, t, k_hide=0.0):
    vx, vy = W / 2, 620
    g = skia.GradientShader.MakeLinear([(0, 600), (0, H)], [0xFF1A2230, 0xFF4A3A2A])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    a = 1 - k_hide
    if a <= 0:
        return
    for side in (-1, 1):
        c.drawLine(vx + side * 10, vy, W / 2 + side * 560, H + 50, stroke(with_alpha(0xFFB8B8C0, a), 18))
    for k in range(18):  # traviesas en perspectiva
        z = ((k + (t * 0.8) % 1) / 18) ** 2
        y = lerp(vy, H + 50, z)
        hw = lerp(20, 700, z)
        c.drawLine(W / 2 - hw, y, W / 2 + hw, y, stroke(with_alpha(0xFF5A3A24, a), lerp(3, 40, z)))


def bar(c, y, L, col):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - L / 2, y - 22, L, 44), 10, 10), fill(col))


def s_ponzo(c, t, P, V):
    sid, lt = seg(P, t)
    hide = ease_in_out(clamp(lt / 1.0)) if sid == "s3" else (1.0 if sid in ("s4",) else 0.0)
    if sid == "s4":
        hide = 1 - ease_in_out(clamp((lt - 1.5) / 1.0))
    rails(c, t, hide)
    L = 300
    y1, y2 = 900, 1520
    if sid == "s2":
        k = ease_in_out(clamp(lt / 1.2))
        bar(c, lerp(y2, y1 + 70, k), L, with_alpha(0xFF3AC8FF, 0.85))
        bar(c, y1, L, ILU)
    else:
        bar(c, y1, L, ILU)
        bar(c, y2, L, 0xFF3AC8FF)
    if sid == "h":
        K.tag(c, W / 2, y1 - 90, "ARRIBA", lt - 0.2, accent=ILU, size=34)
        K.tag(c, W / 2, y2 + 90, "ABAJO", lt - 0.35, accent=0xFF3AC8FF, size=34)
        hc.timer(c, W / 2, 1780, 64, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2":
        hc.stamp(c, "IGUALES", W / 2, 1720, lt, 1.2, 130, col=0xFF2FD46B)
    if sid == "s4":
        hc.big(c, "1911", W / 2, 1750, 160, V["accent"], lt, 0.2)


SERIE = "ILUSIONES IMPOSIBLES · PARTE {}/3"
V307 = dict(slug="307_ilusion_ponzo_p1", accent=ILU, drone=0.02, scene=s_ponzo, badge=SERIE.format(1), segs=[
    dict(id="h", who="nar", say="¿Qué barra es más larga, la de arriba o la de abajo? Tienes tres segundos.",
         cap="¿Qué barra es | más *LARGA*: | arriba o abajo?", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo dice la de arriba. Parece mucho más larga.", cap="Casi todos dicen | la de *ARRIBA*…"),
    dict(id="s2", who="nar", cut=True, say="Pues mira lo que pasa si subo la de abajo. Son exactamente iguales.",
         cap="Subo la de abajo… | son *EXACTAMENTE* | iguales", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="Y si quito las vías del tren, ya no te engaña.", cap="Quito las *vías*… | y ya no engaña"),
    dict(id="s4", who="nar", cut=True, say="Es la ilusión de Ponzo. La describió el psicólogo italiano Mario Ponzo en mil novecientos once.",
         cap="*Ilusión de Ponzo*: | Mario Ponzo, | en *1911*"),
    dict(id="s5", who="nar", say="Tu cerebro ve las vías juntarse a lo lejos, cree que la barra de arriba está más lejos… y la agranda para compensar.",
         cap="Tu cerebro cree que la de arriba | está más *LEJOS*… | y la *AGRANDA*"),
    dict(id="cta", who="nar", cut=True, say="Esta es la parte uno de tres. La dos es más difícil. Sígueme para verla, y comenta si caíste.",
         cap="Parte *1 de 3*. | La 2 es *más difícil*. | *SÍGUEME*"),
])


# ====================================================================== 308 Mito: mapa de la lengua
def tongue(c, x, y, s, t, zones=1.0, flood=0.0):
    c.save(); c.translate(x, y + math.sin(t * 1.5) * 8); c.scale(s, s)
    p = skia.Path()
    p.moveTo(-260, -330)
    p.cubicTo(-300, -50, -260, 250, 0, 380)
    p.cubicTo(260, 250, 300, -50, 260, -330)
    p.close()
    c.drawPath(p.makeTransform(skia.Matrix.Translate(8, 14)) if hasattr(p, "makeTransform") else p, fill(0x55000000))
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeRadial((0, 0), 420, [0xFFF5A0A8, 0xFFE06A7A, 0xFFB8485A]), AntiAlias=True))
    c.drawLine(0, -300, 0, 250, stroke(with_alpha(0xFF9A3A4A, 0.5), 8))
    r = random.Random(8)
    for _ in range(260):  # papilas
        px, py = r.uniform(-240, 240), r.uniform(-310, 340)
        if abs(px) < 250 - max(0, py) * 0.6:
            c.drawCircle(px, py, r.uniform(3, 7), fill(with_alpha(0xFFFFC8D0, 0.5)))
    zs = [(0, 300, 120, 0xFFFF7AD9, "DULCE"), (-200, 60, 110, 0xFF6FD6FF, "SALADO"), (200, 60, 110, 0xFF6FD6FF, "SALADO"),
          (-210, -170, 100, 0xFFFFE04D, "ÁCIDO"), (210, -170, 100, 0xFFFFE04D, "ÁCIDO"), (0, -260, 130, 0xFF8ACD3A, "AMARGO")]
    if zones > 0:
        for (zx, zy, zr, col, lab) in zs:
            c.drawCircle(zx, zy, zr, fill(with_alpha(col, 0.55 * zones)))
    if flood > 0:
        for k, col in enumerate((0xFFFF7AD9, 0xFF6FD6FF, 0xFFFFE04D, 0xFF8ACD3A, 0xFFFFA04D)):
            a = t * 1.5 + k * 1.25
            c.drawCircle(math.cos(a) * 60, math.sin(a) * 90, 330 * flood, skia.Paint(
                Shader=skia.GradientShader.MakeRadial((math.cos(a) * 60, math.sin(a) * 90), 330 * flood + 1,
                                                      [with_alpha(col, 0.16), with_alpha(col, 0)]), BlendMode=skia.BlendMode.kPlus))
    c.restore()
    if zones > 0.5:
        for (zx, zy, zr, col, lab) in zs[::2] + zs[5:]:
            K.tag(c, x + zx * s, y + zy * s, lab, 1.0, accent=col, size=26)


def s_lengua(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF5A1A3A, 0xFF1A2A5A, seed=308)
    zones = 1.0 if sid in ("h", "s1") else 0.0
    flood = 0.0
    if sid == "s2":
        zones = 1.0
    if sid == "s3":
        zones = 1 - ease_in_out(clamp(lt / 1.2)); flood = ease_in_out(clamp(lt / 1.2))
    if sid in ("s4", "s5", "cta"):
        flood = 1.0
    if sid in ("h", "s1", "s3", "s4", "s5", "cta"):
        tongue(c, W / 2, 1200, 1.15, t, zones, flood)
    if sid == "h":
        hc.stamp(c, "FALSO", W / 2, 1760, lt, 1.0, 130)
    if sid == "s2":
        # libro de texto antiguo: hoja envejecida con el mapa
        c.save(); c.translate(W / 2, 1200); c.rotate(-4 + math.sin(t) * 1.5)
        c.drawRect(skia.Rect.MakeXYWH(-400, -520, 800, 1040), fill(0xFFE8DCC0))
        c.drawRect(skia.Rect.MakeXYWH(-400, -520, 800, 1040), stroke(0xFFA08A60, 6))
        c.restore()
        tongue(c, W / 2, 1220, 0.85, t, 1.0, 0)
        hc.big(c, "1901 → 1942", W / 2, 1830, 110, V["accent"], lt, 0.3)
    if sid == "s4":
        hc.big(c, "TODA LA LENGUA", W / 2, 1760, 110, V["accent"], lt, 0.2)
    if sid == "s5":
        K.tag(c, W / 2, 1720, "UMAMI · 1908 · KIKUNAE IKEDA", lt - 0.3, accent=0xFFFFA04D, size=34)


V308 = dict(slug="308_mapa_lengua_mito", accent=0xFFFF7AD9, drone=0.025, scene=s_lengua, tease="TE LO ENSEÑARON MAL", segs=[
    dict(id="h", who="nar", say="Este mapa de la lengua salía en tu libro del colegio. Y es falso.",
         cap="Este *mapa de la lengua* | salía en tu libro… | y es *FALSO*", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Dulce en la punta, amargo al fondo, salado y ácido a los lados. Te lo aprendiste para el examen, ¿verdad?",
         cap="Dulce en la punta, | *amargo* al fondo… | ¿te lo aprendiste?"),
    dict(id="s2", who="nar", cut=True, say="Viene de un estudio alemán de mil novecientos uno, que solo encontró pequeñas diferencias. En mil novecientos cuarenta y dos, en Harvard, se exageró hasta convertirlo en este mapa.",
         cap="Estudio alemán de *1901*: | diferencias pequeñas. | En *1942* lo exageraron"),
    dict(id="s3", who="nar", cut=True, say="La verdad es que toda la lengua detecta todos los sabores.", cap="La verdad: *TODA* la lengua | detecta *todos* los sabores"),
    dict(id="s4", who="nar", cut=True, say="Pruébalo: ponte un poco de azúcar en un lado de la lengua. Lo notarás dulce igual.",
         cap="Pruébalo: *azúcar* | en un lado… | y sabe *DULCE* igual"),
    dict(id="s5", who="nar", cut=True, say="Y además, ese mapa se olvida de un quinto sabor, el umami. Lo descubrió el japonés Kikunae Ikeda en mil novecientos ocho.",
         cap="Y falta un *quinto* sabor: | el *UMAMI*, | descubierto en *1908*"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo enseñaron en el colegio? Comenta. Y sígueme para más mitos que te tragaste en clase.",
         cap="¿Te lo enseñaron? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 309 Ilusiones imposibles P2: muro de la cafetería
def cafe_wall(c, t, mortar=1.0, shift=1.0, guides=0.0):
    rows, tile = 13, 110
    y0 = 700
    c.drawRect(skia.Rect.MakeXYWH(0, y0 - 6, W, rows * tile + 12), fill(lerpc(0xFFFFFFFF, 0xFF7A7A7A, mortar)))
    for i in range(rows):
        off = (math.sin(i * math.pi / 2) * tile / 2) * shift  # desplazamiento alterno de media baldosa
        for j in range(-2, 12):
            if j % 2 == 0:
                x = j * tile + off
                c.drawRect(skia.Rect.MakeXYWH(x, y0 + i * tile + 3, tile, tile - 6), fill(0xFF0A0A0A))
    if mortar > 0:
        for i in range(rows + 1):
            c.drawRect(skia.Rect.MakeXYWH(0, y0 + i * tile - 3, W, 6), fill(with_alpha(0xFF7A7A7A, mortar)))
    if guides > 0:
        for i in range(rows + 1):
            pp = stroke(with_alpha(0xFFFF3B4A, guides), 6)
            pp.setPathEffect(skia.DashPathEffect.Make([30, 18], -t * 80))
            c.drawLine(0, y0 + i * tile, W * guides, y0 + i * tile, pp)


def s_cafe(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF101014)
    mortar, shift, guides = 1.0, 1.0, 0.0
    if sid == "s2":
        guides = ease_out(clamp(lt / 1.0))
    if sid == "s3":
        guides = 1.0
        shift = 1 - ease_in_out(clamp((lt - 0.4) / 1.2))
    if sid == "s4":
        mortar = 0.0 if (lt % 2.0) < 1.0 else 1.0
    c.save(); c.translate(math.sin(t * 0.5) * 12, 0)
    cafe_wall(c, t, mortar, shift, guides)
    c.restore()
    if sid == "h":
        hc.timer(c, W / 2, 2160 - 330, 64, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2":
        hc.stamp(c, "PARALELAS", W / 2, 1300, lt, 1.0, 120, col=0xFF2FD46B)
    if sid == "s5":
        hc.big(c, "BRISTOL · 1973", W / 2, 1300, 110, V["accent"], lt, 0.2)


V309 = dict(slug="309_ilusion_cafeteria_p2", accent=ILU, drone=0.02, scene=s_cafe, badge=SERIE.format(2), segs=[
    dict(id="h", who="nar", say="¿Estas líneas están torcidas o rectas? Mira bien antes de responder.",
         cap="¿Estas líneas están | *TORCIDAS* | o rectas?", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="Parecen inclinadas, como si el muro se abriera en cuñas.", cap="Parecen *inclinadas*… | como cuñas"),
    dict(id="s2", who="nar", cut=True, say="Pero si pongo una regla encima, todas son perfectamente paralelas.",
         cap="Pongo una *regla*… | son perfectamente | *PARALELAS*", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="Y si alineo las baldosas, la ilusión desaparece.", cap="Alineo las baldosas… | y *desaparece*"),
    dict(id="s4", who="nar", cut=True, say="El truco está en las líneas grises de en medio. Sin ellas, se nota mucho menos.",
         cap="El truco son las | líneas *GRISES* | de en medio"),
    dict(id="s5", who="nar", cut=True, say="Se llama ilusión del muro de la cafetería. El psicólogo Richard Gregory la describió en mil novecientos setenta y tres, tras verla en la pared de un café de Bristol.",
         cap="*Muro de la cafetería*: | Richard Gregory la vio | en un café de *Bristol*, *1973*"),
    dict(id="cta", who="nar", cut=True, say="Parte dos de tres. La tres es la que más gente falla. Sígueme para verla, y comenta si te ha engañado.",
         cap="Parte *2 de 3*. | La 3 es la que *MÁS FALLAN*. | *SÍGUEME*"),
])


# ====================================================================== 310 Ilusiones imposibles P3: Jastrow
def arc_shape(c, cx, cy, col, scale=1.0):
    R1, R2, a0, sweep = 700 * scale, 460 * scale, 230, 80
    p = skia.Path()
    ocx, ocy = cx, cy + 600 * scale
    p.addArc(skia.Rect.MakeXYWH(ocx - R1, ocy - R1, 2 * R1, 2 * R1), a0, sweep)
    a1 = math.radians(a0 + sweep)
    p.lineTo(ocx + math.cos(a1) * R2, ocy + math.sin(a1) * R2)
    p.arcTo(skia.Rect.MakeXYWH(ocx - R2, ocy - R2, 2 * R2, 2 * R2), a0 + sweep, -sweep, False)
    p.close()
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeLinear([(cx - 300, 0), (cx + 300, 0)],
                                                                   [col, with_alpha(WHITE, 1), col], [0, 0.5, 1]), AntiAlias=True))
    c.drawPath(p, skia.Paint(Color=col, AntiAlias=True, Alpha=200))


def s_jastrow(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF1A2A6A, 0xFF5A1A3A, seed=310)
    A, B = 0xFFFF5A7A, 0xFF3AC8FF
    yA, yB = 1250, 1570
    xA, xB = W / 2 + 70, W / 2 + 70
    if sid == "s2":  # intercambio
        k = ease_in_out(clamp(lt / 1.4))
        yA, yB = lerp(1250, 1570, k), lerp(1570, 1250, k)
    if sid in ("s3", "s4", "s5", "cta"):
        yA, yB = 1570, 1250
    if sid == "s3":  # superposición
        k = ease_in_out(clamp(lt / 1.2))
        yB = lerp(1250, 1570, k)
    sw = math.sin(t * 0.8) * 8
    if sid != "s3":
        arc_shape(c, xA + sw, yA - 380, A)
        arc_shape(c, xB + sw, yB - 380, B)
    else:
        arc_shape(c, xA + sw, yA - 380, A)
        c.saveLayerAlpha(None, 170)
        arc_shape(c, xB + sw, yB - 380, B)
        c.restore()
        if lt > 1.3:
            hc.stamp(c, "IDÉNTICAS", W / 2, 1800, lt, 1.3, 120, col=0xFF2FD46B)
    if sid == "h":
        K.tag(c, W / 2 + 70, yA - 230, "ROSA", lt - 0.2, accent=A, size=34)
        K.tag(c, W / 2 + 70, yB - 230, "AZUL", lt - 0.35, accent=B, size=34)
        hc.timer(c, W / 2, 1830, 64, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s4":
        hc.big(c, "1889", W / 2, 1830, 160, V["accent"], lt, 0.2)


V310 = dict(slug="310_ilusion_jastrow_p3", accent=ILU, drone=0.02, scene=s_jastrow, badge=SERIE.format(3), segs=[
    dict(id="h", who="nar", say="¿Qué figura es más grande, la rosa o la azul? Esta la falla casi todo el mundo.",
         cap="¿Qué figura es | más *GRANDE*: | la rosa o la azul?", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="La azul parece claramente más grande, ¿no?", cap="La *azul* parece | claramente más grande…"),
    dict(id="s2", who="nar", cut=True, say="Ahora las cambio de sitio. Mira: ahora la grande parece la rosa.",
         cap="Las cambio de sitio… | y ahora la grande | parece la *ROSA*", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Y si las pongo una encima de la otra… son idénticas.", cap="Una encima de otra… | son *IDÉNTICAS*", hold=0.8),
    dict(id="s4", who="nar", cut=True, say="Es la ilusión de Jastrow. La descubrió el psicólogo Joseph Jastrow en mil ochocientos ochenta y nueve.",
         cap="*Ilusión de Jastrow*: | Joseph Jastrow, | en *1889*"),
    dict(id="s5", who="nar", say="Tu cerebro compara el borde corto de una con el borde largo de la otra… y decide mal cuál es mayor.",
         cap="Compara el borde *corto* | de una con el *largo* | de la otra… y *FALLA*"),
    dict(id="cta", who="nar", cut=True, say="¿Cuál de las tres te engañó más? Comenta uno, dos o tres. Y sígueme: mañana empieza una serie nueva.",
         cap="¿Cuál te engañó más? | Comenta *1, 2 o 3* | y *SÍGUEME*"),
])

VIDEOS = [V301, V302, V303, V304, V305, V306, V307, V308, V309, V310]


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
