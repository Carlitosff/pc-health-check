"""Lote diario 30/10/2026 (501–510). Motor v8 (RE-GANCHO a mitad de vídeo: V['rehook']=(seg, texto) -> pill de aviso
amarilla con franjas + punch-in + riser/pop; objetivo: subir el tiempo medio, que se queda en 13-16 s).
Mezcla según métricas del 29/10: ilusiones en serie 3/3 ≈1.300 (T3: Hering, Zöllner, Kanizsa) en la noche; reto de
conteo (triángulos 1.579, 5 comentarios = el mejor del día) -> cuadrados; '3 cosas' (dormir 1.425) -> 3 cosas cuando
pasas miedo (víspera de Halloween); mito del colegio (Colón 1.264) -> Napoleón; Halloween: nabos antes que calabazas;
Ganímedes a las 12:00 (lo prometido; Ío 1.278); mito de animales (prometido) -> lemmings y Disney.
TEST 15:00: esa franja lleva 4/4 días muerta (126-245 vistas) con formatos flojos -> hoy va una ilusión fuerte
(rejilla de Hermann) para separar 'franja' de 'contenido'."""
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
RED = 0xFFFF3B4A


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


def lerpc(a, b, k):
    ch = [int(lerp((a >> s) & 255, (b >> s) & 255, k)) for s in (16, 8, 0)]
    return 0xFF000000 | (ch[0] << 16) | (ch[1] << 8) | ch[2]


# ====================================================================== 501 Ganímedes (lo prometido)
def gany_texture():
    path = S.TEX + "ganymede_proc.png"
    try:
        Image.open(path)
        return S.load("ganymede_proc.png")
    except Exception:
        pass
    w, h = 2048, 1024
    rnd = np.random.default_rng(501)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = np.zeros((h, w), np.float32)
    for k in range(6):
        f = 2 ** k
        ph = rnd.uniform(0, 6.28, 3)
        n += np.sin(xx / w * 6.28 * f + ph[0] + 1.3 * np.sin(yy / h * 6.28 * f * 0.8 + ph[1])) * \
            np.cos(yy / h * 3.14 * f * 1.1 + ph[2]) / (k + 1) ** 0.8
    n = (n - n.min()) / (n.max() - n.min())
    dark = n < 0.42  # regiones antiguas oscuras (tipo Galileo Regio)
    # terreno claro con surcos paralelos (grooved terrain)
    grooves = 0.5 + 0.5 * np.sin((xx * 0.9 + yy * 0.45) / 7.0 + 4 * n)
    light = 0.60 + 0.12 * grooves + 0.1 * n
    darkv = 0.30 + 0.12 * n
    v = np.where(dark, darkv, light)
    r = v * 1.02
    g = v * 0.97
    b = v * 0.90
    img = np.stack([r, g, b], -1)
    pole = np.abs(yy / h - 0.5)[..., None] * 2
    img = img * (1 - 0.25 * pole ** 4) + 0.25 * pole ** 4 * np.array([0.92, 0.94, 0.98])  # escarcha polar
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    R = random.Random(501)
    for _ in range(140):  # cráteres brillantes con rayos
        x, y, rr = R.uniform(0, w), R.uniform(60, h - 60), R.uniform(3, 14)
        d.ellipse([x - rr, y - rr * 0.8, x + rr, y + rr * 0.8], fill=(235, 232, 225))
        if R.random() < 0.15:
            for k in range(10):
                a = R.uniform(0, 6.28)
                L = rr * R.uniform(3, 7)
                d.line([x, y, x + math.cos(a) * L, y + math.sin(a) * L * 0.8], fill=(215, 212, 205), width=2)
    im = im.filter(ImageFilter.GaussianBlur(1.6))
    im.save(path)
    return S.load("ganymede_proc.png")


GANY = gany_texture()
MERC = S.load("mercurymap.jpg")
JUP = S.load("jupitermap.jpg")
MOON = S.load("moon_1024.jpg")
DAY = S.load("earth_atmos_2048.jpg")
CLOUDS = S.load("earth_clouds_1024.png", "A")
ST = K.Stars(seed=501)
L0 = (-0.55, 0.3, 0.78)


def aurora_ring(c, x, y, R, t, k=1.0):
    for j in range(3):
        rr = R * (0.55 + 0.05 * j)
        a = (0.35 + 0.2 * math.sin(t * 4 + j)) * k
        c.drawOval(skia.Rect.MakeXYWH(x - rr, y - R * 0.88 - rr * 0.18, 2 * rr, rr * 0.36),
                   skia.Paint(AntiAlias=True, Color=with_alpha(0xFF5AFFB0, a), Style=skia.Paint.kStroke_Style,
                              StrokeWidth=10, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)))
        c.drawOval(skia.Rect.MakeXYWH(x - rr, y + R * 0.88 - rr * 0.18, 2 * rr, rr * 0.36),
                   skia.Paint(AntiAlias=True, Color=with_alpha(0xFF5AFFB0, a * 0.8), Style=skia.Paint.kStroke_Style,
                              StrokeWidth=10, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)))


def field_lines(c, x, y, R, t, k=1.0):
    for j in range(1, 6):
        s = R * (1.1 + 0.35 * j)
        for side in (-1, 1):
            p = skia.Path()
            p.moveTo(x, y - R * 0.9)
            p.cubicTo(x + side * s * 1.2, y - s * 0.9, x + side * s * 1.2, y + s * 0.9, x, y + R * 0.9)
            ph = (t * 0.6 + j * 0.2) % 1
            c.drawPath(p, stroke(with_alpha(0xFF7AB8FF, (0.18 + 0.25 * ph) * k), 4))


def s_gany(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020308)
    ST.draw(c, t, camx=t * 12, alpha=0.9)
    if sid == "h":
        jr = 600
        S.draw_planet(c, W * 0.1, 1450, jr, S.render(2 * jr, JUP, spin=t * 0.3, light=L0, gain=1.1, limb=0.35))
        gr = lerp(150, 360, ease_out(clamp(lt / 3.0)))
        S.draw_planet(c, W * 0.62, 1130, gr, S.render(2 * gr, GANY, spin=t * 0.15, light=L0, gain=1.15, limb=0.3))
        hc.stamp(c, "MÁS QUE UN PLANETA", W / 2, 1720, lt, 1.2, 80, col=0xFF2A6AFF)
    elif sid == "s1":
        gr, mr = 360, 360 * 4879 / 5268
        x1, x2 = W / 2 - 230, W / 2 + 250
        k = ease_out(clamp(lt / 1.0))
        S.draw_planet(c, lerp(-400, x1, k), 1220, gr, S.render(2 * gr, GANY, spin=t * 0.15, light=L0, gain=1.15, limb=0.3))
        S.draw_planet(c, lerp(W + 400, x2, k), 1220 + (gr - mr), mr, S.render(int(2 * mr), MERC, spin=t * 0.1, light=L0, gain=1.2))
        K.tag(c, x1, 1660, "GANÍMEDES · 5.268 km", lt - 0.6, accent=V["accent"], size=32)
        K.tag(c, x2, 1660, "MERCURIO · 4.879 km", lt - 0.9, accent=WHITE, size=32)
    elif sid == "s2":
        gr, mr = 330, 330 * 4879 / 5268
        x1, x2 = W / 2 - 230, W / 2 + 250
        # balanza: Mercurio baja, Ganímedes sube
        k = ease_in_out(clamp((lt - 0.3) / 1.2))
        tilt = -14 * k
        c.save(); c.translate(W / 2, 1650); c.rotate(tilt)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-500, -10, 1000, 20), 10, 10), fill(0xFFB8BCC8))
        c.restore()
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - 12, 1650, 24, 260), fill(0xFF8A8E9A))
        dy1 = -500 * math.sin(math.radians(-tilt)) * 0.48
        S.draw_planet(c, x1, 1300 + dy1, gr * 0.8, S.render(int(2 * gr * 0.8), GANY, spin=t * 0.15, light=L0, gain=1.15, limb=0.3))
        S.draw_planet(c, x2, 1340 - dy1, mr * 0.8, S.render(int(2 * mr * 0.8), MERC, spin=t * 0.1, light=L0, gain=1.2))
        K.counter(c, t, lt - 1.4, lambda p: f"{int(round(45 * p))}%", "DEL PESO DE MERCURIO", V["accent"], y=760, size=120)
    elif sid == "s3":
        gr = 480
        cx, cy = W / 2, 1300
        S.draw_planet(c, cx, cy, gr, S.render(2 * gr, GANY, spin=t * 0.12, light=L0, gain=1.1, limb=0.3))
        # corte: cuña con capas (hielo / océano / roca)
        k = ease_out(clamp(lt / 1.2))
        c.save()
        wedge = skia.Path(); wedge.moveTo(cx, cy); wedge.arcTo(skia.Rect.MakeXYWH(cx - gr, cy - gr, 2 * gr, 2 * gr), -10, 80 * k, False); wedge.close()
        c.clipPath(wedge, doAntiAlias=True)
        for rr, col in ((gr, 0xFFE8EEF4), (gr * 0.86, 0xFF1A5AB8), (gr * 0.7, 0xFFDDE6EE), (gr * 0.5, 0xFF8A6A4A), (gr * 0.25, 0xFFB86A3A)):
            c.drawCircle(cx, cy, rr, fill(col))
        for j in range(30):  # olas en el océano
            a = math.radians(-10 + j * 2.6)
            rr = gr * 0.78 + 6 * math.sin(t * 4 + j)
            c.drawCircle(cx + math.cos(a) * rr, cy + math.sin(a) * rr, 5, fill(with_alpha(0xFF7AC8FF, 0.6)))
        c.restore()
        K.tag(c, cx + 300, cy + 560, "OCÉANO SALADO", lt - 1.0, accent=0xFF3A9AFF, size=36)
        K.tag(c, W / 2, 760, "HUBBLE · 2015", lt - 0.4, accent=V["accent"], size=36)
    elif sid == "s4":
        gr = 340
        cx, cy = W / 2, 1250
        k = ease_out(clamp(lt / 0.8))
        field_lines(c, cx, cy, gr, t, k)
        S.draw_planet(c, cx, cy, gr, S.render(2 * gr, GANY, spin=t * 0.15, light=L0, gain=1.15, limb=0.3))
        aurora_ring(c, cx, cy, gr, t, k)
        K.tag(c, W / 2, 1830, "SONDA GALILEO · 1996", lt - 0.5, accent=V["accent"], size=36)
    elif sid == "s5":
        # telescopio de Galileo (enero de 1610) -> la nave JUICE
        jr = 160
        S.draw_planet(c, W / 2, 1150, jr, S.render(2 * jr, JUP, spin=t * 0.3, light=L0, gain=1.1, limb=0.35))
        for k2, (d, sz) in enumerate(((-330, 18), (260, 22), (420, 26), (-470, 16))):
            x = W / 2 + d + math.sin(t * 0.8 + k2) * 15
            c.drawCircle(x, 1150, sz, fill(0xFFF4ECD8))
            glow(c, x, 1150, sz * 3, 0xFFFFF4D8, 0.3)
        K.tag(c, W / 2 + 420, 1060, "GANÍMEDES", lt - 0.3, accent=V["accent"], size=28)
        hc.big(c, "ENERO 1610", W / 2, 1450, 110, WHITE, lt, 0.4)
        # nave con paneles solares
        nx = lerp(-200, W / 2, ease_out(clamp((lt - 1.5) / 2.0)))
        if lt > 1.5:
            c.save(); c.translate(nx, 1700); c.rotate(-8)
            c.drawRect(skia.Rect.MakeXYWH(-50, -40, 100, 80), fill(0xFFD8B04A))
            for side in (-1, 1):
                for j in range(5):
                    c.drawRect(skia.Rect.MakeXYWH(side * 60 + (0 if side > 0 else -300) + j * 60, -30, 56, 60), fill(0xFF1A2A6A))
                    c.drawRect(skia.Rect.MakeXYWH(side * 60 + (0 if side > 0 else -300) + j * 60, -30, 56, 60), stroke(0xFF5A7AC8, 3))
            c.restore()
            K.tag(c, W / 2, 1830, "JUICE · LLEGA EN 2031", lt - 1.8, accent=0xFF3A9AFF, size=34)
    else:
        gr = 300
        S.draw_planet(c, W / 2, 1230, gr, S.render(2 * gr, GANY, spin=t * 0.15, light=L0, gain=1.15, limb=0.3))
        field_lines(c, W / 2, 1230, gr, t, 0.6)


V501 = dict(slug="501_ganimedes", accent=0xFF8AD4FF, drone=0.035, scene=s_gany, badge="LO PROMETIDO · JÚPITER PARTE 4",
            send="ENVÍASELO A UN FRIKI DEL ESPACIO", rehook=("s3", "ESPERA… AHORA LO MÁS LOCO"), segs=[
    dict(id="h", who="nar", say="Esta luna es más grande que un planeta. Y está en nuestro Sistema Solar.",
         cap="Esta luna es | más grande que | un *PLANETA*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Es Ganímedes, de Júpiter. Mide casi cinco mil trescientos kilómetros. Mercurio, menos de cinco mil.",
         cap="*Ganímedes*: 5.268 km. | *Mercurio*: | 4.879 km"),
    dict(id="s2", who="nar", cut=True, say="Pero pesa menos de la mitad que Mercurio. Porque está hecha, casi a partes iguales, de roca y de hielo.",
         cap="Pero pesa | *MENOS DE LA MITAD*: | mitad roca, mitad *hielo*"),
    dict(id="s3", who="nar", cut=True, say="Y bajo ese hielo, el telescopio Hubble encontró pruebas de un océano salado. Podría tener más agua que toda la superficie de la Tierra.",
         cap="Bajo el hielo: | un *OCÉANO SALADO* | con más agua que la Tierra"),
    dict(id="s4", who="nar", cut=True, say="Y es la única luna con campo magnético propio. Hasta tiene auroras. Lo descubrió la sonda Galileo en mil novecientos noventa y seis.",
         cap="La única luna con | *campo magnético* propio. | Tiene *AURORAS*"),
    dict(id="s5", who="nar", cut=True, say="Galileo la vio en mil seiscientos diez. Y la sonda europea JUICE llega en dos mil treinta y uno.",
         cap="Galileo la vio en *1610*. | La sonda *JUICE* | llega en *2031*"),
    dict(id="cta", who="nar", cut=True, say="¿Sabías que una luna podía ser más grande que un planeta? Comenta. Y sígueme: la próxima es la luna donde llueve metano.",
         cap="¿Lo sabías? *COMENTA*. | Próxima: donde *llueve metano*. | *SÍGUEME*"),
])


# ====================================================================== 502 Mito: los lemmings y Disney
def tundra(c, t, sepia=0.0):
    g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF6A8AB0, 0xFFC8D8E8, 0xFFE8EEF4])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    r = random.Random(7)
    for k in range(5):  # montañas lejanas
        x = k * 300 - 100
        p = skia.Path(); p.moveTo(x - 300, 1100); p.lineTo(x, 760 + r.uniform(-60, 60)); p.lineTo(x + 300, 1100); p.close()
        c.drawPath(p, fill(0xFF8A9AB8))
        p2 = skia.Path(); p2.moveTo(x - 60, 880); p2.lineTo(x, 770); p2.lineTo(x + 60, 880); p2.close()
        c.drawPath(p2, fill(0xFFF4F8FC))
    c.drawRect(skia.Rect.MakeLTRB(0, 1080, W, H), fill(0xFFEEF2F6))
    p = skia.Paint(AntiAlias=True)
    for k in range(80):  # nieve cayendo
        x = (r.uniform(0, W) + math.sin(t + k) * 20) % W
        y = (r.uniform(0, H) + t * r.uniform(40, 90)) % H
        p.setColor(with_alpha(WHITE, 0.7))
        c.drawCircle(x, y, r.uniform(2, 5), p)


def lemming(c, x, y, s, t, seed=0, flip=False):
    r = random.Random(seed)
    c.save(); c.translate(x, y + abs(math.sin(t * 9 + seed)) * -8 * s); c.scale(-s if flip else s, s)
    c.drawOval(skia.Rect.MakeXYWH(-70, 30, 140, 22), fill(0x33000000))
    body = skia.GradientShader.MakeRadial((-10, -20), 90, [0xFFE8B070, 0xFFB0743A, 0xFF6A4020])
    c.drawOval(skia.Rect.MakeXYWH(-75, -45, 150, 90), skia.Paint(Shader=body, AntiAlias=True))
    c.drawOval(skia.Rect.MakeXYWH(-60, -48, 110, 30), fill(with_alpha(0xFF2A1A10, 0.75)))  # franja oscura del lomo
    c.drawCircle(58, -6, 34, skia.Paint(Shader=body, AntiAlias=True))
    c.drawCircle(70, -16, 6, fill(0xFF111111))
    c.drawCircle(72, -18, 2, fill(WHITE))
    c.drawCircle(92, -2, 5, fill(0xFF3A2010))
    c.drawCircle(46, -36, 10, fill(0xFF8A5A30))
    for k in range(40):  # pelaje
        a = r.uniform(0, 6.28)
        rr = r.uniform(0.6, 1.0)
        px, py = math.cos(a) * 70 * rr, math.sin(a) * 40 * rr
        c.drawLine(px, py, px + math.cos(a) * 9, py + math.sin(a) * 9, stroke(with_alpha(0xFF5A3A1A, 0.5), 2))
    for k in (-40, 30):
        c.drawOval(skia.Rect.MakeXYWH(k - 10, 32, 24, 14), fill(0xFF5A3A1A))
    c.restore()


def film(c, t, k=1.0):
    """Viejo metraje: sepia, rayas y bordes de película."""
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=with_alpha(0xFF704214, 0.35 * k), BlendMode=skia.BlendMode.kColor))
    r = random.Random(int(t * 12))
    for _ in range(4):
        x = r.uniform(0, W)
        c.drawLine(x, 0, x + r.uniform(-20, 20), H, stroke(with_alpha(0xFFFFF4E0, 0.15 * k), 2))
    for side in (0, W - 70):
        c.drawRect(skia.Rect.MakeXYWH(side, 0, 70, H), fill(with_alpha(0xFF0A0A0A, 0.9 * k)))
        for j in range(24):
            yy = (j * 90 + t * 300) % (H + 90) - 90
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(side + 18, yy, 34, 50), 8, 8), fill(with_alpha(0xFFE8E0D0, 0.8 * k)))


def cliff_scene(c, t, push=0.0, n=5):
    tundra(c, t)
    # acantilado a la izquierda, agua a la derecha
    c.drawRect(skia.Rect.MakeLTRB(0, 1350, W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, 1350), (0, H)], [0xFF2A5A7A, 0xFF0A2A3A])))
    for k in range(10):
        yy = 1400 + k * 50
        c.drawLine(560, yy + math.sin(t * 2 + k) * 6, W, yy + math.sin(t * 2.3 + k) * 6, stroke(with_alpha(WHITE, 0.15), 3))
    rock = skia.Path(); rock.moveTo(0, 1180); rock.lineTo(560, 1180); rock.lineTo(600, 1300); rock.lineTo(540, 1500)
    rock.lineTo(580, H); rock.lineTo(0, H); rock.close()
    c.drawPath(rock, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 1180), (600, 1600)], [0xFF6A6058, 0xFF3A322C]), AntiAlias=True))
    c.drawRect(skia.Rect.MakeLTRB(0, 1160, 565, 1185), fill(0xFFF4F8FC))
    sp = 170
    for i in range(n):
        x = -60 + i * sp + ((t * 140 * (1 + push)) % sp)
        if x > 540:
            fall = (x - 540) / sp
            c.save(); c.translate(540 + fall * 120, 1140 + fall ** 2 * 380); c.rotate(fall * 50)
            lemming(c, 0, 0, 1.0, t, seed=i); c.restore()
        else:
            lemming(c, x, 1140, 1.0, t, seed=i)


def s_lemming(c, t, P, V):
    sid, lt = seg(P, t)
    if sid in ("h", "s1"):
        cliff_scene(c, t, push=0.4 if sid == "h" else 0.0)
        if sid == "h":
            hc.stamp(c, "MONTAJE", W / 2, 1750, lt, 1.4, 120)
        else:
            hc.stamp(c, "FALSO", W / 2, 1750, lt, 1.6, 140)
    elif sid == "s2":
        cliff_scene(c, t)
        film(c, t, ease_out(clamp(lt / 0.4)))
        hc.big(c, "1958", W / 2, 1750, 170, V["accent"], lt, 0.3)
        K.tag(c, W / 2, 1880, "DOCUMENTAL DE DISNEY", lt - 0.6, accent=WHITE, size=34)
    elif sid == "s3":
        tundra(c, t)
        # plataforma giratoria con lemmings encima
        cx, cy = W / 2, 1330
        c.drawOval(skia.Rect.MakeXYWH(cx - 360, cy - 60, 720, 200), fill(0xFF4A3A2A))
        c.drawOval(skia.Rect.MakeXYWH(cx - 360, cy - 90, 720, 200), fill(0xFF8A6A4A))
        for i in range(5):
            a = t * 1.6 + i * 1.256
            lemming(c, cx + math.cos(a) * 250, cy + 10 + math.sin(a) * 60, 0.8, t, seed=i, flip=math.sin(a) < 0)
        film(c, t, 0.8)
        K.tag(c, W / 2, 1600, "ALBERTA, CANADÁ", lt - 0.3, accent=V["accent"], size=38)
        K.tag(c, W / 2, 1700, "PLATAFORMA GIRATORIA", lt - 1.0, accent=WHITE, size=34)
    elif sid == "s4":
        c.clear(0xFF0A0810)
        glow(c, W / 2, 1150, 600, 0xFFFFC23A, 0.35)
        # trofeo dorado genérico
        c.save(); c.translate(W / 2, 1150); s = ease_back(prog(lt, 0.1, 0.5)); c.scale(s, s)
        gold = skia.GradientShader.MakeLinear([(-120, 0), (120, 0)], [0xFF8A6010, 0xFFFFE08A, 0xFFB8861A])
        cup = skia.Path(); cup.moveTo(-170, -260); cup.lineTo(170, -260); cup.quadTo(160, 20, 30, 60); cup.lineTo(30, 160)
        cup.lineTo(110, 200); cup.lineTo(110, 250); cup.lineTo(-110, 250); cup.lineTo(-110, 200); cup.lineTo(-30, 160)
        cup.lineTo(-30, 60); cup.quadTo(-160, 20, -170, -260); cup.close()
        c.drawPath(cup, skia.Paint(Shader=gold, AntiAlias=True))
        c.restore()
        hc.stamp(c, "PREMIO A MEJOR DOCUMENTAL", W / 2, 1600, lt, 0.8, 52, col=0xFFB8861A)
    elif sid == "s5":
        c.clear(0xFFE8E0D0)
        # periódico
        c.save(); c.translate(W / 2, 1200); c.rotate(-4 + math.sin(t) * 1.2)
        c.drawRect(skia.Rect.MakeXYWH(-420, -480, 840, 960), fill(0xFFF8F4EA))
        draw_text(c, "LA VERDAD DE", 0, -360, 64, INK, shadow=False)
        draw_text(c, "LOS LEMMINGS", 0, -280, 72, INK, shadow=False)
        for j in range(14):
            c.drawRect(skia.Rect.MakeXYWH(-380 + (j % 2) * 390, -200 + (j // 2) * 80, 370, 16), fill(0xFFB8B0A0))
        c.restore()
        hc.big(c, "1982", W / 2, 1780, 150, V["accent"], lt, 0.3)
    elif sid == "s6":
        tundra(c, t)
        for i in range(6):
            lemming(c, (i * 260 + t * 90) % (W + 300) - 150, 1250 + (i % 3) * 170, 1.0, t, seed=i + 20)
        K.tag(c, W / 2, 1700, "MIGRAN, NO SE SUICIDAN", lt - 0.4, accent=GREEN, size=40)
    else:
        tundra(c, t)
        lemming(c, W / 2, 1300, 1.3, t, seed=3)


V502 = dict(slug="502_lemmings_disney_mito", accent=0xFFFFC870, drone=0.025, scene=s_lemming, tease="TE LO CONTARON MAL",
            send="ENVÍASELO A QUIEN SE LO CREÍA", rehook=("s3", "ATENTO A ESTO"), segs=[
    dict(id="h", who="nar", say="Para un documental de Disney empujaron lemmings por un acantilado. Y así nació un mito.",
         cap="Para un documental de *DISNEY* | empujaron lemmings | por un *ACANTILADO*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Seguro que has oído que los lemmings se suicidan en masa saltando al mar. Es falso.",
         cap="¿Los lemmings se | *suicidan en masa*? | *FALSO*"),
    dict(id="s2", who="nar", cut=True, say="La idea se hizo famosa en mil novecientos cincuenta y ocho, con un documental de Disney sobre el Ártico.",
         cap="Se hizo famosa en *1958* | con un documental | de *DISNEY*"),
    dict(id="s3", who="nar", cut=True, say="Lo rodaron en Alberta, en Canadá, donde no viven esos lemmings. Los llevaron de fuera, y los hicieron correr en una plataforma giratoria.",
         cap="Lo rodaron donde | *no viven* lemmings… | y los hicieron *girar*"),
    dict(id="s4", who="nar", cut=True, say="Después los empujaron al río para la escena final. Y el documental ganó el Óscar.",
         cap="Los *EMPUJARON* al río… | y el documental | *ganó el Óscar*"),
    dict(id="s5", who="nar", cut=True, say="Lo destapó en mil novecientos ochenta y dos el periodista canadiense Brian Vallee.",
         cap="Lo destapó en *1982* | el periodista | *Brian Vallee*"),
    dict(id="s6", who="nar", cut=True, say="La verdad: cuando hay demasiados, migran, y algunos se ahogan cruzando ríos. Pero no saltan a propósito.",
         cap="La verdad: *MIGRAN*. | Algunos se ahogan… | pero *no saltan*"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo creías? Comenta sí o no. Y sígueme para otro mito de animales.",
         cap="¿Te lo creías? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 503 Rejilla de Hermann (TEST franja 15:00)
def grid(c, t, n=6, sq=130, gap=30, col_sq=0xFF0A0A0A, col_bg=WHITE, dots=False, cy=1200, sway=True):
    tot = n * sq + (n - 1) * gap
    x0 = W / 2 - tot / 2 + (math.sin(t * 0.6) * 4 if sway else 0)
    y0 = cy - tot / 2
    c.drawRect(skia.Rect.MakeXYWH(x0 - gap, y0 - gap, tot + 2 * gap, tot + 2 * gap), fill(col_bg))
    for i in range(n):
        for j in range(n):
            c.drawRect(skia.Rect.MakeXYWH(x0 + i * (sq + gap), y0 + j * (sq + gap), sq, sq), fill(col_sq))
    if dots:
        for i in range(1, n):
            for j in range(1, n):
                c.drawCircle(x0 + i * (sq + gap) - gap / 2, y0 + j * (sq + gap) - gap / 2, gap * 0.62, fill(WHITE))
    return x0, y0, tot


def s_hermann(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF1A2A6A, 0xFF4A1A5A, seed=503)
    if sid in ("s4", "s5", "cta"):
        k = ease_in_out(clamp(lt / 0.8)) if sid == "s4" else 1.0
        grid(c, t, col_sq=0xFF0A0A0A, col_bg=lerpc(WHITE, 0xFF8A8A8A, k), dots=k > 0.5)
        if sid == "s4" and lt > 0.9:
            hc.timer(c, W / 2, 1830, 64, clamp((lt - 0.9) / 3.0), str(max(0, 3 - int(lt - 0.9))), V["accent"])
        if sid == "s5":
            hc.big(c, "1994", W / 2, 1800, 140, V["accent"], lt, 0.2)
        return
    x0, y0, tot = grid(c, t)
    if sid == "s2":
        # señala una intersección: allí el punto gris 'desaparece'
        cx, cy = x0 + 3 * 160 - 15, y0 + 3 * 160 - 15
        c.drawCircle(cx, cy, 60, stroke(with_alpha(RED, clamp(lt * 3)), 8))
    if sid == "s3":
        hc.big(c, "1870", W / 2, 1800, 160, V["accent"], lt, 0.2)
        K.tag(c, W / 2, 1920 - 40, "LUDIMAR HERMANN", lt - 0.5, accent=WHITE, size=32)
    if sid == "h":
        hc.timer(c, W / 2, 1830, 60, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])


V503 = dict(slug="503_rejilla_hermann", accent=ILU, drone=0.02, scene=s_hermann, tease="NO EXISTEN",
            send="ENVÍASELO A ALGUIEN Y QUE LOS CUENTE", rehook=("s4", "AHORA, LA VERSIÓN DIFÍCIL"), segs=[
    dict(id="h", who="nar", say="¿Ves puntos grises entre los cuadrados? No existen.",
         cap="¿Ves *puntos grises* | entre los cuadrados? | *NO EXISTEN*", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="Aparecen en los cruces de las líneas blancas. Pero en la imagen no hay ni uno.",
         cap="Salen en los *cruces*… | pero en la imagen | *no hay ni uno*"),
    dict(id="s2", who="nar", cut=True, say="Mira fijamente un cruce. El punto de ese cruce desaparece, y los demás siguen ahí.",
         cap="Mira fijo un cruce: | ese punto *DESAPARECE*… | y los demás siguen"),
    dict(id="s3", who="nar", cut=True, say="Es la rejilla de Hermann. La describió el fisiólogo Ludimar Hermann en mil ochocientos setenta.",
         cap="*Rejilla de Hermann*: | Ludimar Hermann, | en *1870*"),
    dict(id="s4", who="nar", cut=True, say="Ahora pongo puntos blancos en los cruces. Intenta contar los puntos negros. No puedes: parpadean.",
         cap="Ahora con puntos blancos: | cuenta los *NEGROS*… | *NO PUEDES*", hold=1.2),
    dict(id="s5", who="nar", cut=True, say="Esta versión es la rejilla centelleante, de mil novecientos noventa y cuatro. Tus ojos procesan el contraste por zonas, y en los cruces se equivocan.",
         cap="*Rejilla centelleante*, 1994. | Tu ojo procesa el contraste | *por zonas*… y falla"),
    dict(id="cta", who="nar", cut=True, say="¿Cuántos puntos negros has contado? Comenta tu número. Y sígueme para más ilusiones.",
         cap="¿Cuántos puntos negros | has contado? *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 504 Mito: Napoleón era bajito
def parchment(c, t):
    g = skia.GradientShader.MakeRadial((W / 2, H / 2), H * 0.7, [0xFFF0E0B8, 0xFFC8A870])
    c.drawPaint(skia.Paint(Shader=g))
    r = random.Random(4)
    for _ in range(90):
        x, y = r.uniform(60, W - 60), r.uniform(540, H - 100)
        c.drawCircle(x, y, r.uniform(8, 40), fill(with_alpha(0xFF8A6A3A, 0.06)))


def bicorne(c, x, y, s, t):
    c.save(); c.translate(x, y + math.sin(t * 1.5) * 6); c.scale(s, s); c.rotate(math.sin(t) * 2)
    p = skia.Path(); p.moveTo(-260, 40); p.quadTo(0, -230, 260, 40); p.quadTo(0, 0, -260, 40); p.close()
    c.drawPath(p.makeOffset(0, 14) if hasattr(p, "makeOffset") else p, fill(0x55000000))
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, -200), (0, 40)], [0xFF2A2A2A, 0xFF0A0A0A]), AntiAlias=True))
    c.drawPath(p, stroke(0xFFC8A040, 6))
    for rr, col in ((46, 0xFF1A3AA0), (32, WHITE), (18, 0xFFC8202A)):  # escarapela
        c.drawCircle(120, -40, rr, fill(col))
    c.restore()


def ruler(c, x, y0, px_per_cm, t):
    c.drawRect(skia.Rect.MakeXYWH(x - 40, y0 - 180 * px_per_cm, 80, 180 * px_per_cm), fill(0xFFF4E4B0))
    for cm in range(0, 181, 5):
        yy = y0 - cm * px_per_cm
        L = 40 if cm % 10 == 0 else 20
        c.drawLine(x - 40, yy, x - 40 + L, yy, stroke(0xFF3A2A10, 3))
        if cm % 20 == 0 and cm >= 140:
            c.drawString(f"{cm}", x + 50, yy + 10, font(28), fill(0xFF3A2A10))


def bar(c, x, y0, ppc, cm, lab, col, lt, delay):
    k = ease_out(clamp((lt - delay) / 1.0))
    h = cm * ppc * k
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 70, y0 - h, 140, h), 14, 14), fill(col))
    if k > 0.9:
        draw_text(c, lab, x, y0 - h - 30, 46, WHITE, outline=10)


def s_napoleon(c, t, P, V):
    sid, lt = seg(P, t)
    parchment(c, t)
    y0, ppc = 1880, 6.0  # 180 cm = 1080 px
    vis = 150  # se muestra de 150 a 180 cm ampliado: base visual en 140 cm
    if sid == "h":
        bicorne(c, W / 2, 1150, 1.4, t)
        hc.stamp(c, "MITO", W / 2, 1650, lt, 1.0, 150)
    elif sid in ("s1", "s3"):
        # barras ampliadas (eje desde 140 cm)
        base = 140
        sc = 22.0
        def b(x, cm, lab, col, d):
            k = ease_out(clamp((lt - d) / 1.0))
            h = (cm - base) * sc * k
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 110, 1800 - h, 220, h), 18, 18), fill(col))
            if k > 0.9:
                draw_text(c, lab, x, 1800 - h - 30, 56, WHITE, outline=12)
        c.drawLine(80, 1800, W - 80, 1800, stroke(0xFF3A2A10, 6))
        if sid == "s1":
            b(W / 2 - 220, 164.5, "1,64", 0xFF8A7A6A, 0.2)
            b(W / 2 + 220, 168.5, "1,68", 0xFF1A3AA0, 0.6)
            K.tag(c, W / 2 - 220, 1860, "FRANCÉS MEDIO", lt - 0.4, accent=WHITE, size=30)
            K.tag(c, W / 2 + 220, 1860, "NAPOLEÓN", lt - 0.8, accent=V["accent"], size=30)
            bicorne(c, W / 2 + 220, 1800 - 28.5 * sc * ease_out(clamp((lt - 0.6) / 1.0)) - 160, 0.45, t)
        else:
            b(W / 2 - 220, 157, "1,57", RED, 0.2)
            b(W / 2 + 220, 168.5, "1,69", GREEN, 0.7)
            K.tag(c, W / 2 - 220, 1860, "PULGADAS INGLESAS", lt - 0.4, accent=WHITE, size=28)
            K.tag(c, W / 2 + 220, 1860, "PULGADAS FRANCESAS", lt - 0.8, accent=V["accent"], size=28)
    elif sid == "s2":
        # informe de autopsia
        c.save(); c.translate(W / 2, 1230); c.rotate(-3 + math.sin(t) * 1)
        c.drawRect(skia.Rect.MakeXYWH(-400, -430, 800, 860), fill(0xFFFBF6E8))
        c.drawRect(skia.Rect.MakeXYWH(-400, -430, 800, 860), stroke(0xFF8A6A3A, 4))
        draw_text(c, "AUTOPSIA · 1821", 0, -330, 52, INK, shadow=False)
        for j in range(6):
            c.drawRect(skia.Rect.MakeXYWH(-330, -230 + j * 60, 660, 12), fill(0xFFC8BCA8))
        k = ease_out(clamp((lt - 0.6) / 0.4))
        draw_text(c, "5 pieds 2 pouces", 0, 220, 76 * (0.6 + 0.4 * k), 0xFF8A1A1A, shadow=False)
        c.restore()
    elif sid == "s4":
        # caricatura: grabado con marco y un sombrero diminuto
        c.drawRect(skia.Rect.MakeXYWH(110, 700, W - 220, 1000), fill(0xFFF8F0DC))
        for j in range(60):
            c.drawLine(110, 700 + j * 17, W - 110, 700 + j * 17 + 40, stroke(with_alpha(0xFF6A5A3A, 0.12), 2))
        c.drawRect(skia.Rect.MakeXYWH(110, 700, W - 220, 1000), stroke(0xFF3A2A10, 10))
        bicorne(c, W / 2, 1300, 0.35 + 0.05 * math.sin(t * 6), t * 3)
        hc.stamp(c, "«LITTLE BONEY»", W / 2, 1520, lt, 0.5, 90, col=0xFF8A1A1A)
        K.tag(c, W / 2, 1800, "JAMES GILLRAY · CARICATURISTA", lt - 0.9, accent=V["accent"], size=30)
    elif sid == "s5":
        for i in range(7):  # guardia imperial: altos chacós en fila
            x = 120 + i * 140
            hh = 520 + (i % 2) * 30
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 55, 1750 - hh, 110, hh), 20, 20), fill(0xFF1A2A6A))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 50, 1750 - hh - 170, 100, 180), 30, 30), fill(0xFF1A1410))
            c.drawRect(skia.Rect.MakeXYWH(x - 8, 1750 - hh - 210, 16, 50), fill(RED))
        K.tag(c, W / 2, 1850, "GUARDIA IMPERIAL", lt - 0.3, accent=V["accent"], size=36)
        hc.big(c, "«EL PEQUEÑO CABO»", W / 2, 900, 80, WHITE, lt, 0.8)
    else:
        bicorne(c, W / 2, 1200, 1.2, t)


V504 = dict(slug="504_napoleon_bajito_mito", accent=0xFFFFC870, drone=0.025, scene=s_napoleon, tease="TE LO ENSEÑARON MAL",
            rehook=("s3", "AQUÍ ESTÁ EL TRUCO"), segs=[
    dict(id="h", who="nar", say="Napoleón no era bajito. Te lo hicieron creer los ingleses.",
         cap="Napoleón *NO* era | bajito. Te lo hicieron | creer los *ingleses*", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Medía alrededor de un metro sesenta y ocho. Algo más que el francés medio de su época.",
         cap="Medía unos *1,68 m*: | más que el francés | *medio* de su época"),
    dict(id="s2", who="nar", cut=True, say="El lío vino de su autopsia, en mil ochocientos veintiuno: cinco pies y dos pulgadas. Pero eran pulgadas francesas.",
         cap="Su autopsia: *5 pies y 2*… | pero eran pulgadas | *FRANCESAS*"),
    dict(id="s3", who="nar", cut=True, say="En medidas inglesas eso sería un metro cincuenta y siete. En francesas, casi un metro sesenta y nueve.",
         cap="En inglesas: *1,57*. | En francesas: | casi *1,69*"),
    dict(id="s4", who="nar", cut=True, say="Y los caricaturistas británicos, como James Gillray, lo dibujaban diminuto y rabioso. Lo llamaban Little Boney.",
         cap="Los caricaturistas | lo dibujaban *DIMINUTO*: | «Little Boney»"),
    dict(id="s5", who="nar", cut=True, say="Encima iba rodeado de su guardia, de soldados muy altos, y sus tropas le llamaban el pequeño cabo. Con cariño.",
         cap="Rodeado de su *guardia* | de gigantes… y le llamaban | «el *pequeño cabo*»"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo enseñaron así? Comenta. Y sígueme para más mitos que te tragaste en clase.",
         cap="¿Te lo enseñaron así? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 505 Lista: 3 cosas que hace tu cuerpo cuando pasas miedo
def heart(c, x, y, s, t, bpm=70):
    beat = (t * bpm / 60) % 1
    sc = s * (1 + 0.12 * math.exp(-beat * 9))
    c.save(); c.translate(x, y); c.scale(sc, sc)
    p = skia.Path(); p.moveTo(0, 160); p.cubicTo(-260, 0, -170, -210, 0, -90); p.cubicTo(170, -210, 260, 0, 0, 160); p.close()
    glow(c, 0, 0, 320, 0xFFFF3B4A, 0.3)
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeRadial((-60, -80), 260, [0xFFFF6A7A, 0xFFC8102A, 0xFF6A0A18]), AntiAlias=True))
    for k in range(3):
        c.drawPath(p, stroke(with_alpha(0xFF8A0A1A, 0.2), 3))
    c.restore()


def eye_pupil(c, x, y, R, pup, t):
    c.save(); c.translate(x, y)
    eye = skia.Path(); eye.moveTo(-R * 1.6, 0); eye.quadTo(0, -R * 1.25, R * 1.6, 0); eye.quadTo(0, R * 1.25, -R * 1.6, 0); eye.close()
    c.drawPath(eye, fill(0xFFF8F0EC))
    c.save(); c.clipPath(eye, doAntiAlias=True)
    c.drawPath(eye, stroke(with_alpha(0xFFE08A8A, 0.4), 30))
    ir = R * 0.62
    c.drawCircle(0, 0, ir, skia.Paint(Shader=skia.GradientShader.MakeRadial((0, 0), ir, [0xFF4A8A6A, 0xFF2A5A4A, 0xFF1A2A2A], [0.3, 0.8, 1]), AntiAlias=True))
    r = random.Random(2)
    for k in range(60):
        a = r.uniform(0, 6.28)
        c.drawLine(math.cos(a) * ir * 0.35, math.sin(a) * ir * 0.35, math.cos(a) * ir * 0.95, math.sin(a) * ir * 0.95,
                   stroke(with_alpha(0xFF8AC8A0, 0.25), 2))
    c.drawCircle(0, 0, ir * pup, fill(0xFF050505))
    c.drawCircle(-ir * 0.3, -ir * 0.3, ir * 0.12, fill(with_alpha(WHITE, 0.85)))
    c.restore()
    c.restore()


def skin_hairs(c, t, k):
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, 1100), 1100, [0xFFF4C8A8, 0xFFD8987A, 0xFFA8684A])))
    r = random.Random(9)
    for i in range(140):
        x, y = r.uniform(40, W - 40), r.uniform(560, 1900)
        bump = 10 + 16 * k
        c.drawCircle(x, y + 4, bump, fill(with_alpha(0xFF8A4A3A, 0.25 * k)))
        c.drawCircle(x, y, bump, skia.Paint(Shader=skia.GradientShader.MakeRadial((x - 4, y - 4), bump, [0xFFFFD8C0, 0xFFE0A080]), AntiAlias=True))
        ang = lerp(-75, -15, k) + r.uniform(-10, 10)
        L = r.uniform(50, 80)
        a = math.radians(ang)
        c.drawLine(x, y, x + math.cos(a) * L, y + math.sin(a) * L * (1 if k < 0.5 else 1) - L * 0.6 * k, stroke(0xFF3A2010, 3))


def s_miedo(c, t, P, V):
    sid, lt = seg(P, t)
    dark = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF06040A, 0xFF1A0A14, 0xFF0A0408])
    c.drawPaint(skia.Paint(Shader=dark))
    if sid == "h":
        # pasillo oscuro con una linterna
        for j in range(10):
            s = 1 - j * 0.09
            c.drawRect(skia.Rect.MakeXYWH(W / 2 - 520 * s, 1150 - 760 * s, 1040 * s, 1520 * s), stroke(with_alpha(0xFF6A4A5A, 0.5 - j * 0.04), 4))
        fx = W / 2 + math.sin(t * 1.3) * 220
        glow(c, fx, 1150, 420, 0xFFFFE8B0, 0.35)
        c.drawCircle(W / 2 + 40, 1120, 14, fill(with_alpha(0xFFFF3B4A, 0.4 + 0.4 * math.sin(t * 5))))
        c.drawCircle(W / 2 - 40, 1120, 14, fill(with_alpha(0xFFFF3B4A, 0.4 + 0.4 * math.sin(t * 5))))
    elif sid == "s1":
        bpm = lerp(70, 130, ease_out(clamp(lt / 2.0)))
        heart(c, W / 2, 1180, 1.25, t, bpm)
        K.counter(c, t, lt - 0.2, lambda p: f"{int(round(70 + 60 * p))} lpm", "LATIDOS POR MINUTO", V["accent"], y=1720, size=110)
    elif sid == "s2":
        pup = lerp(0.32, 0.78, ease_in_out(clamp((lt - 0.4) / 1.4)))
        eye_pupil(c, W / 2, 1200, 300, pup, t)
        K.tag(c, W / 2, 1700, "PUPILA DILATADA = MÁS LUZ", lt - 1.2, accent=V["accent"], size=36)
    elif sid in ("s3", "s4"):
        k = ease_out(clamp((lt - 0.5) / 1.2)) if sid == "s3" else 1.0
        skin_hairs(c, t, k)
        if sid == "s3":
            K.tag(c, W / 2, 1800, "PIEL DE GALLINA", lt - 0.8, accent=V["accent"], size=44)
        else:
            c.drawRect(skia.Rect.MakeWH(W, H), fill(with_alpha(0xFF000000, 0.55)))
            # silueta de gato erizado
            c.save(); c.translate(W / 2, 1350); s = ease_back(prog(lt, 0.2, 0.6)); c.scale(s, s)
            body = skia.Path(); body.moveTo(-260, 120); body.cubicTo(-240, -200, 220, -200, 240, 120); body.close()
            c.drawPath(body, fill(0xFF0A0A0A))
            for j in range(40):
                a = math.radians(200 + j * 3.5)
                px, py = math.cos(a) * 250, 120 + math.sin(a) * 300
                c.drawLine(px, py, px * 1.12, py * 1.12 - 20, stroke(0xFF0A0A0A, 8))
            c.drawCircle(300, 40, 90, fill(0xFF0A0A0A))
            for side in (-1, 1):
                ear = skia.Path(); ear.moveTo(300 + side * 70, -10); ear.lineTo(300 + side * 55, -110); ear.lineTo(300 + side * 10, -60); ear.close()
                c.drawPath(ear, fill(0xFF0A0A0A))
            c.drawCircle(275, 30, 12, fill(0xFFFFE04D)); c.drawCircle(330, 30, 12, fill(0xFFFFE04D))
            tail = skia.Path(); tail.moveTo(-240, 100); tail.cubicTo(-380, 0, -330, -260, -280, -300)
            c.drawPath(tail, stroke(0xFF0A0A0A, 40))
            c.restore()
            K.tag(c, W / 2, 1800, "COMO UN GATO ASUSTADO", lt - 0.5, accent=V["accent"], size=40)
    else:
        heart(c, W / 2, 1230, 0.9, t, 90)


V505 = dict(slug="505_3cosas_miedo", accent=0xFFFF7A3A, drone=0.035, scene=s_miedo, tease="LA 3 ES MUY RARA",
            send="ENVÍASELO A ALGUIEN MIEDICA", rehook=("s3", "LA 3 ES LA MÁS RARA"), segs=[
    dict(id="h", who="nar", say="Tres cosas que hace tu cuerpo cuando pasas miedo. La tercera viene de cuando éramos peludos.",
         cap="*3 cosas* que hace | tu cuerpo cuando | pasas *MIEDO*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Uno. En un instante sueltas adrenalina: el corazón se dispara y respiras más rápido, para correr o pelear.",
         cap="*UNO*: adrenalina. | El corazón se *DISPARA* | para correr o pelear"),
    dict(id="s2", who="nar", cut=True, say="Dos. Se te dilatan las pupilas, para que entre más luz y veas mejor el peligro.",
         cap="*DOS*: se te *dilatan* | las pupilas, para ver | mejor el *peligro*"),
    dict(id="s3", who="nar", cut=True, say="Tres. Se te pone la piel de gallina. Unos músculos diminutos levantan cada pelo.",
         cap="*TRES*: piel de *gallina*. | Músculos diminutos | levantan cada pelo"),
    dict(id="s4", who="nar", say="Es un resto de cuando teníamos pelo por todo el cuerpo. Al erizarlo, parecíamos más grandes. Como un gato asustado.",
         cap="Restos de cuando éramos | *PELUDOS*: al erizarlo, | parecíamos *más grandes*"),
    dict(id="cta", who="nar", cut=True, say="¿Qué es lo que más miedo te da? Comenta. Y sígueme, que mañana es Halloween.",
         cap="¿Qué te da más miedo? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== Ilusiones T3: fondo común
SERIE = "ILUSIONES IMPOSIBLES T3 · PARTE {}/3"


def ilu_bg(c, t, seed):
    hc.aurora(c, t, 0xFF1A2A6A, 0xFF4A1A5A, seed=seed)


# ====================================================================== 506 T3 P1: Hering
def s_hering(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 506)
    cx, cy = W / 2, 1230
    rays = 1.0
    if sid == "s2":
        rays = 1 - ease_in_out(clamp((lt - 0.2) / 1.0))
    elif sid in ("s3",):
        rays = 0.0
    if rays > 0:
        c.save(); c.translate(cx, cy); c.rotate(t * 2)
        for k in range(36):
            a = math.radians(k * 5)
            c.drawLine(-math.cos(a) * 1100, -math.sin(a) * 1100, math.cos(a) * 1100, math.sin(a) * 1100,
                       stroke(with_alpha(WHITE, 0.75 * rays), 4))
        c.restore()
    for side in (-1, 1):
        c.drawLine(cx + side * 190, cy - 640, cx + side * 190, cy + 640, stroke(0xFFFF3B4A, 14))
    if sid == "s2" and lt > 1.2:
        for side in (-1, 1):
            c.drawLine(cx + side * 190, cy - 640, cx + side * 190, cy + 640, stroke(with_alpha(GREEN, 0.9), 6))
        hc.stamp(c, "RECTAS", W / 2, 1740, lt, 1.2, 110, col=GREEN)
    if sid == "h":
        hc.timer(c, W / 2, 1830, 56, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s3":
        hc.big(c, "1861", W / 2, 1760, 140, V["accent"], lt, 0.2)


V506 = dict(slug="506_ilusion_hering_t3p1", accent=ILU, drone=0.02, scene=s_hering, badge=SERIE.format(1),
            rehook=("s2", "MIRA LO QUE PASA"), segs=[
    dict(id="h", who="nar", say="¿Las líneas rojas son curvas o rectas? Responde en tres segundos.",
         cap="¿Las líneas *rojas* | son *CURVAS* | o rectas?", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="Parecen dos arcos, abombados hacia fuera, ¿verdad?", cap="Parecen *abombadas* | hacia fuera…"),
    dict(id="s2", who="nar", cut=True, say="Quito los rayos del fondo… y son perfectamente rectas y paralelas.",
         cap="Quito los rayos… | son *RECTAS* | y paralelas", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Es la ilusión de Hering. La publicó el fisiólogo alemán Ewald Hering en mil ochocientos sesenta y uno.",
         cap="*Ilusión de Hering*: | Ewald Hering, | en *1861*"),
    dict(id="s4", who="nar", say="Una teoría dice que tu cerebro se adelanta, como si avanzaras hacia el centro, y dobla las líneas antes de tiempo.",
         cap="Tu cerebro *se adelanta*, | como si avanzaras… | y *DOBLA* las líneas"),
    dict(id="cta", who="nar", cut=True, say="Temporada tres, parte uno de tres. La dos es más difícil. Sígueme para verla, y comenta si caíste.",
         cap="T3, parte *1 de 3*. | La 2 es *más difícil*. | *SÍGUEME*"),
])


# ====================================================================== 507 Reto: ¿cuántos cuadrados ves?
def s_cuadrados(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A3A5A, 0xFF3A1A5A, seed=507)
    n, cell = 4, 200
    x0, y0 = W / 2 - n * cell / 2 + math.sin(t * 0.6) * 4, 1230 - n * cell / 2
    for i in range(n + 1):
        c.drawLine(x0 + i * cell, y0, x0 + i * cell, y0 + n * cell, stroke(WHITE, 9))
        c.drawLine(x0, y0 + i * cell, x0 + n * cell, y0 + i * cell, stroke(WHITE, 9))
    groups = {"s3": (1, 16), "s4": (2, 9), "s5": (3, 4), "s6": (4, 1)}
    base = {"s3": 0, "s4": 16, "s5": 25, "s6": 29}
    if sid in groups:
        sz, cnt = groups[sid]
        m = n - sz + 1
        shown = min(cnt, int(lt / (2.6 / cnt)) + 1) if cnt > 1 else 1
        q = shown - 1
        i, j = q % m, q // m
        r = skia.Rect.MakeXYWH(x0 + i * cell + 8, y0 + j * cell + 8, sz * cell - 16, sz * cell - 16)
        c.drawRect(r, fill(with_alpha(V["accent"], 0.35)))
        c.drawRect(r, stroke(V["accent"], 12))
        hc.big(c, str(base[sid] + shown), W / 2, 1770, 160, V["accent"], 1.0, 0.0)
    if sid == "h":
        hc.timer(c, W / 2, 1810, 70, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s1":
        K.tag(c, W / 2, 1780, "COMENTA TU NÚMERO", lt - 0.2, accent=V["accent"], size=44)
    if sid == "cta":
        hc.stamp(c, "30", W / 2, 1760, lt, 0.1, 150, col=GREEN)


V507 = dict(slug="507_cuantos_cuadrados", accent=0xFF3AC8FF, drone=0.02, scene=s_cuadrados, tease="MÁS DIFÍCIL QUE AYER",
            send="RETA A UN AMIGO: ENVÍASELO", rehook=("s4", "AQUÍ FALLA CASI TODO EL MUNDO"), segs=[
    dict(id="h", who="nar", say="¿Cuántos cuadrados ves? Más difícil que el de los triángulos.",
         cap="¿Cuántos *CUADRADOS* | ves?", hold=1.5),
    dict(id="s1", who="nar", cut=True, say="Cuéntalos bien. Y antes de seguir, escribe tu número en los comentarios.",
         cap="Cuéntalos… y escribe | tu número en los | *COMENTARIOS*", hold=0.8),
    dict(id="s2", who="q", cut=True, say="¿Ya? Vamos a contarlos juntos.", cap="¿Ya? | Vamos a *contarlos*"),
    dict(id="s3", who="nar", cut=True, say="Los pequeños son fáciles: dieciséis.", cap="Los pequeños: | *DIECISÉIS*", hold=1.2),
    dict(id="s4", who="nar", cut=True, say="Pero hay cuadrados de dos por dos. Nueve más.", cap="Pero hay de *2×2*: | *NUEVE* más", hold=1.0),
    dict(id="s5", who="nar", cut=True, say="De tres por tres, otros cuatro.", cap="De *3×3*: | otros *CUATRO*", hold=1.0),
    dict(id="s6", who="nar", cut=True, say="Y el grande, que lo rodea todo. Uno más.", cap="Y el *GRANDE*: | uno más", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="En total, treinta. ¿Cuántos dijiste tú? Comenta. Y sígueme, que el próximo es todavía peor.",
         cap="Total: *30*. ¿Cuántos | dijiste tú? *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 508 T3 P2: Zöllner
def s_zollner(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 508)
    hatch = 1.0
    if sid == "s2":
        hatch = 1 - ease_in_out(clamp((lt - 0.2) / 1.0))
    elif sid == "s3":
        hatch = 0.0
    cx, cy = W / 2, 1230
    c.save(); c.translate(cx + math.sin(t * 0.6) * 4, cy)
    for k in range(6):
        off = (k - 2.5) * 125
        c.save(); c.translate(-off * 0.707, off * 0.707); c.rotate(45)
        c.drawLine(-420, 0, 420, 0, stroke(WHITE, 10))
        if hatch > 0:
            for j in range(-7, 8):
                x = j * 56
                if k % 2 == 0:
                    c.drawLine(x - 22, -40, x + 22, 40, stroke(with_alpha(WHITE, hatch), 8))
                else:
                    c.drawLine(x - 22, 40, x + 22, -40, stroke(with_alpha(WHITE, hatch), 8))
        c.restore()
    c.restore()
    if sid == "s2" and lt > 1.2:
        hc.stamp(c, "PARALELAS", W / 2, 1790, lt, 1.2, 100, col=GREEN)
    if sid == "h":
        hc.timer(c, W / 2, 1830, 56, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s3":
        hc.big(c, "1860", W / 2, 1790, 140, V["accent"], lt, 0.2)


V508 = dict(slug="508_ilusion_zollner_t3p2", accent=ILU, drone=0.02, scene=s_zollner, badge=SERIE.format(2),
            rehook=("s2", "MIRA LO QUE PASA"), segs=[
    dict(id="h", who="nar", say="¿Estas líneas largas son paralelas o están torcidas? Mira bien.",
         cap="¿Estas líneas son | *PARALELAS* | o torcidas?", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="Parece que se abren y se cierran, como una cremallera, ¿verdad?", cap="Parece que se *abren* | y se *cierran*…"),
    dict(id="s2", who="nar", cut=True, say="Quito las rayitas… y todas son perfectamente paralelas.",
         cap="Quito las rayitas… | todas son | *PARALELAS*", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Es la ilusión de Zöllner. El astrofísico alemán Johann Zöllner la vio en el dibujo de una tela, en mil ochocientos sesenta.",
         cap="*Ilusión de Zöllner*: | la vio en una *TELA*, | en *1860*"),
    dict(id="s4", who="nar", say="Tu cerebro exagera los ángulos pequeños entre las rayitas y la línea, y eso inclina cada línea entera.",
         cap="Tu cerebro *exagera* | los ángulos pequeños… | y *INCLINA* la línea"),
    dict(id="cta", who="nar", cut=True, say="Parte dos de tres. La tres es la que más gente ve y no existe. Sígueme para verla, y comenta si caíste.",
         cap="Parte *2 de 3*. | La 3 *NO EXISTE*. | *SÍGUEME*"),
])


# ====================================================================== 509 Halloween: las primeras calabazas eran nabos
def night_fog(c, t):
    g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF0A0614, 0xFF1A0E24, 0xFF2A1A20])
    c.drawPaint(skia.Paint(Shader=g))
    glow(c, 860, 640, 300, 0xFFFFE8C0, 0.25)
    c.drawCircle(860, 640, 110, fill(0xFFF8F0DC))
    r = random.Random(12)
    for k in range(6):
        y = 1500 + k * 70
        x = (r.uniform(0, W) + t * (20 + 10 * k)) % (W + 600) - 300
        sh = skia.GradientShader.MakeRadial((x, y), 500, [with_alpha(0xFFB8B0C8, 0.10), with_alpha(0xFFB8B0C8, 0)])
        c.drawCircle(x, y, 500, skia.Paint(Shader=sh))


def carved_face(c, s, t, glow_col=0xFFFFB03A):
    f = 0.85 + 0.15 * math.sin(t * 13) * math.sin(t * 7)
    col = with_alpha(glow_col, f)
    for sx in (-1, 1):
        p = skia.Path(); p.moveTo(sx * 40 * s, -20 * s); p.lineTo(sx * 100 * s, -20 * s); p.lineTo(sx * 70 * s, -75 * s); p.close()
        c.drawPath(p, fill(col))
    m = skia.Path(); m.moveTo(-110 * s, 40 * s)
    for k in range(7):
        m.lineTo((-110 + k * 36.6) * s, (40 + (25 if k % 2 else 0)) * s)
    m.lineTo(110 * s, 40 * s); m.quadTo(0, 150 * s, -110 * s, 40 * s); m.close()
    c.drawPath(m, fill(col))


def turnip(c, x, y, s, t):
    c.save(); c.translate(x, y); c.rotate(math.sin(t * 1.3) * 2)
    glow(c, 0, 0, 380 * s, 0xFFFF9A2A, 0.35)
    body = skia.Path(); body.moveTo(0, -170 * s); body.cubicTo(200 * s, -170 * s, 230 * s, 120 * s, 0, 190 * s)
    body.cubicTo(-230 * s, 120 * s, -200 * s, -170 * s, 0, -170 * s); body.close()
    c.drawPath(body, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, -170 * s), (0, 190 * s)],
                                                                      [0xFF9A4A9A, 0xFFE8D8E0, 0xFFF4ECE4], [0, 0.35, 1]), AntiAlias=True))
    c.drawLine(0, 190 * s, 10 * s, 290 * s, stroke(0xFFD8C8B8, 6 * s))
    for k in range(3):
        c.drawLine((k - 1) * 20 * s, -165 * s, (k - 1) * 50 * s, -260 * s, stroke(0xFF4A7A3A, 12 * s))
    carved_face(c, s * 0.9, t)
    c.restore()


def pumpkin(c, x, y, s, t):
    c.save(); c.translate(x, y)
    glow(c, 0, 0, 420 * s, 0xFFFF9A2A, 0.4)
    for k, dx in enumerate((-150, -75, 75, 150, 0)):
        c.drawOval(skia.Rect.MakeXYWH((dx - 130) * s, -170 * s, 260 * s, 340 * s),
                   skia.Paint(Shader=skia.GradientShader.MakeRadial((dx * s, -40 * s), 260 * s, [0xFFFFA040, 0xFFE06A10, 0xFF8A3A08]), AntiAlias=True))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-18 * s, -230 * s, 36 * s, 80 * s), 10, 10), fill(0xFF4A5A2A))
    carved_face(c, s * 1.1, t)
    c.restore()


def s_nabos(c, t, P, V):
    sid, lt = seg(P, t)
    night_fog(c, t)
    if sid == "h":
        k = ease_in_out(clamp((lt - 0.4) / 1.2))
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k))); pumpkin(c, W / 2, 1250, 1.3, t); c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k)); turnip(c, W / 2, 1250, 1.3, t); c.restore()
        hc.stamp(c, "NABOS", W / 2, 1760, lt, 1.4, 140, col=0xFF9A4A9A)
    elif sid == "s1":
        turnip(c, W / 2 - 230, 1250, 0.9, t)
        # patata y remolacha talladas
        c.save(); c.translate(W / 2 + 250, 1150)
        glow(c, 0, 0, 220, 0xFFFF9A2A, 0.3)
        c.drawOval(skia.Rect.MakeXYWH(-140, -100, 280, 200), skia.Paint(Shader=skia.GradientShader.MakeRadial((0, -30), 200, [0xFFD8B080, 0xFF8A6030]), AntiAlias=True))
        carved_face(c, 0.6, t + 1)
        c.restore()
        c.save(); c.translate(W / 2 + 230, 1500)
        glow(c, 0, 0, 200, 0xFFFF9A2A, 0.3)
        c.drawCircle(0, 0, 110, skia.Paint(Shader=skia.GradientShader.MakeRadial((-30, -30), 150, [0xFFC83A6A, 0xFF5A0A2A]), AntiAlias=True))
        carved_face(c, 0.55, t + 2)
        c.restore()
        K.tag(c, W / 2, 1800, "IRLANDA Y ESCOCIA · SAMHAIN", lt - 0.4, accent=V["accent"], size=34)
    elif sid == "s2":
        turnip(c, W / 2, 1250, 1.2, t)
        # brasa dentro
        glow(c, W / 2, 1290, 120, 0xFFFF4A1A, 0.7 + 0.3 * math.sin(t * 9))
        K.tag(c, W / 2, 1780, "JACK EL TACAÑO", lt - 0.5, accent=V["accent"], size=44)
    elif sid == "s3":
        # barco de emigrantes y calabaza que aparece
        c.drawRect(skia.Rect.MakeLTRB(0, 1450, W, H), fill(0xFF0A1A2A))
        for k in range(8):
            c.drawLine(0, 1480 + k * 50 + math.sin(t * 2 + k) * 6, W, 1480 + k * 50 + math.sin(t * 2.2 + k) * 6, stroke(with_alpha(WHITE, 0.12), 3))
        sx = lerp(-300, W / 2 - 150, ease_out(clamp(lt / 2.5)))
        c.save(); c.translate(sx, 1420 + math.sin(t * 2) * 8)
        hull = skia.Path(); hull.moveTo(-260, 0); hull.lineTo(260, 0); hull.lineTo(200, 90); hull.lineTo(-200, 90); hull.close()
        c.drawPath(hull, fill(0xFF2A1A10))
        c.drawRect(skia.Rect.MakeXYWH(-120, -90, 240, 90), fill(0xFF3A2A1A))
        c.drawRect(skia.Rect.MakeXYWH(-30, -230, 40, 140), fill(0xFF1A1A1A))
        c.restore()
        if lt > 2.0:
            pumpkin(c, W / 2 + 230, 1080, 0.65 * ease_back(prog(lt, 2.0, 2.4)), t)
        K.tag(c, W / 2, 800, "SIGLO XIX · EE. UU.", lt - 0.3, accent=V["accent"], size=38)
    elif sid == "s4":
        turnip(c, W / 2 - 240, 1250, 0.75, t)
        pumpkin(c, W / 2 + 240, 1250, 0.85, t)
        hc.big(c, "JACK-O'-LANTERN", W / 2, 1720, 96, V["accent"], lt, 0.3)
        K.tag(c, W / 2, 1850, "= LA LINTERNA DE JACK", lt - 0.8, accent=WHITE, size=38)
    else:
        pumpkin(c, W / 2, 1250, 1.0, t)


V509 = dict(slug="509_halloween_nabos", accent=0xFFFF9A2A, drone=0.035, scene=s_nabos, tease="ESTO NO TE LO CONTARON",
            send="ENVÍASELO A QUIEN CELEBRE HALLOWEEN", rehook=("s2", "Y LA LEYENDA ES PEOR"), segs=[
    dict(id="h", who="nar", say="Las primeras calabazas de Halloween no eran calabazas. Eran nabos.",
         cap="Las primeras calabazas | de Halloween… | eran *NABOS*", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="En Irlanda y Escocia, por la antigua fiesta de Samhain, tallaban caras en nabos, patatas y remolachas, y les metían una brasa.",
         cap="En *Irlanda* y *Escocia* | tallaban caras en nabos, | patatas y *remolachas*"),
    dict(id="s2", who="nar", cut=True, say="Según la leyenda, Jack el Tacaño engañó al diablo, y acabó vagando en la oscuridad con un carbón encendido dentro de un nabo.",
         cap="*Jack el Tacaño* engañó | al diablo… y vagó con | un *carbón* en un nabo"),
    dict(id="s3", who="nar", cut=True, say="En el siglo diecinueve, millones de irlandeses emigraron a Estados Unidos. Y allí descubrieron la calabaza: más grande y mucho más fácil de tallar.",
         cap="Los irlandeses emigraron | a *EE. UU.*… y allí | descubrieron la *CALABAZA*"),
    dict(id="s4", who="nar", cut=True, say="Por eso en inglés se llama jack o lantern. La linterna de Jack.",
         cap="Por eso se llama | *jack-o'-lantern*: | la linterna de *Jack*"),
    dict(id="cta", who="nar", cut=True, say="¿Tú tallas calabaza en Halloween? Comenta sí o no. Y sígueme para más historias de Halloween.",
         cap="¿Tú tallas calabaza? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 510 T3 P3: triángulo de Kanizsa
def s_kanizsa(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 510)
    cx, cy, R = W / 2, 1250, 400
    panel = skia.Rect.MakeXYWH(70, cy - 560, W - 140, 1080)
    c.drawRRect(skia.RRect.MakeRectXY(panel, 40, 40), fill(0xFFF4F4F4))
    rot = 0.0
    if sid == "s2":
        rot = 180 * ease_in_out(clamp((lt - 0.3) / 1.2))
    elif sid == "s3":
        rot = 180 * (1 - ease_in_out(clamp((lt - 0.3) / 1.0)))
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in (-90, 30, 150)]
    for (x, y) in pts:
        ang = math.degrees(math.atan2(cy - y, cx - x))
        c.save(); c.translate(x, y); c.rotate(ang + rot)
        p = skia.Path(); p.moveTo(0, 0); p.arcTo(skia.Rect.MakeXYWH(-120, -120, 240, 240), 30, 300, False); p.close()
        c.drawPath(p, fill(0xFF111111))
        c.restore()
    # triángulo invertido de contorno (V sueltas)
    ipts = [(cx + R * 0.95 * math.cos(math.radians(a)), cy + R * 0.95 * math.sin(math.radians(a))) for a in (90, 210, 330)]
    for i, (x, y) in enumerate(ipts):
        for j in (1, 2):
            ox, oy = ipts[(i + j) % 3]
            c.drawLine(x, y, lerp(x, ox, 0.25), lerp(y, oy, 0.25), stroke(0xFF111111, 10))
    if sid == "s4":
        # el contorno que tu cerebro 'dibuja'
        k = 0.5 + 0.5 * math.sin(t * 4)
        p = skia.Path(); p.moveTo(*pts[0]); p.lineTo(*pts[1]); p.lineTo(*pts[2]); p.close()
        c.drawPath(p, stroke(with_alpha(0xFFFF3B4A, 0.7 * k), 6))
    if sid == "h":
        hc.timer(c, W / 2, 1840, 56, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2" and lt > 1.4:
        hc.stamp(c, "NO EXISTE", W / 2, 1700, lt, 1.4, 100, col=RED)
    if sid == "s3" and lt > 0.3:
        hc.big(c, "1955", W / 2, 1700, 130, V["accent"], lt, 0.3)


V510 = dict(slug="510_ilusion_kanizsa_t3p3", accent=ILU, drone=0.02, scene=s_kanizsa, badge=SERIE.format(3),
            send="ENVÍASELO A QUIEN VEA EL TRIÁNGULO", rehook=("s2", "AHORA GIRO LAS PIEZAS"), segs=[
    dict(id="h", who="nar", say="¿Ves un triángulo blanco en el centro? No existe.",
         cap="¿Ves un *triángulo* | *BLANCO*? | *NO EXISTE*", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="Hasta parece más blanco que el fondo, y con bordes nítidos. Pero no hay ni una línea.",
         cap="Parece *más blanco* | que el fondo… | y no hay *ni una línea*"),
    dict(id="s2", who="nar", cut=True, say="Mira: si giro las tres piezas negras, el triángulo desaparece.",
         cap="Giro las piezas… | y *DESAPARECE*", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Es el triángulo de Kanizsa. Lo publicó el psicólogo italiano Gaetano Kanizsa en mil novecientos cincuenta y cinco.",
         cap="*Triángulo de Kanizsa*: | Gaetano Kanizsa, | en *1955*"),
    dict(id="s4", who="nar", say="Tu cerebro odia los huecos. Ve tres esquinas alineadas, y se inventa los bordes que faltan.",
         cap="Tu cerebro *odia los huecos*: | ve tres esquinas… | y se *INVENTA* los bordes"),
    dict(id="cta", who="nar", cut=True, say="¿Cuál de las tres te engañó más? Comenta uno, dos o tres. Y sígueme: mañana empieza una serie nueva.",
         cap="¿Cuál te engañó más? | Comenta *1, 2 o 3* | y *SÍGUEME*"),
])

VIDEOS = [V501, V502, V503, V504, V505, V506, V507, V508, V509, V510]


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
