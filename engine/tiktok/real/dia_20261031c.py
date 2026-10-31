"""Lote 31/10/2026 tarde-noche (701–710) — Motor v10: CAMA MUSICAL procedural (pad + bajo + arpegio que entra tras
el gancho, se intensifica en el re-gancho y deja un hueco de silencio antes de la revelación).
Contexto: el lote 601–611 se publicó de madrugada a petición de Carlos; este lote vuelve a las franjas 12:00–23:30.
Métricas 30/10 (24 h): techo ~1.300 sigue; 15:00 ya NO está muerta (Hermann 1.351, Napoleón 15:30 1.413);
flojos: Halloween nabos 153 y 3 cosas miedo 692. Conteo = más comentarios (7). Mezcla: Encélado (lo prometido
'otra luna'), mitos (pato/eco, María Antonieta), picante (cuerpo), ILUSIONES T5 (Cornsweet, Ehrenstein, Munker),
conteo de triángulos en el pentágono (35, calculado), MENTALISTA (formato experimental: 'adivino lo que piensas'),
Houdini P2 (la última sesión de espiritismo: hoy hace 90 años, 31/10/1936)."""
import math, sys, random, itertools
import numpy as np
import skia
from PIL import Image, ImageFilter
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
import dia_20261031 as D
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow, pill
from core import draw_text, font, text_w

OUT = "/home/claude/tiktok/outdaily"
ILU = 0xFFFFE04D
GREEN = 0xFF2FD46B
RED = 0xFFFF3B4A
seg = D.seg
blur = D.blur
ST = K.Stars(seed=701)
L0 = (-0.55, 0.3, 0.78)


# ====================================================================== 701 Encélado
def enc_texture():
    path = S.TEX + "enceladus_proc.png"
    try:
        Image.open(path)
        return S.load("enceladus_proc.png")
    except Exception:
        pass
    w, h = 2048, 1024
    rnd = np.random.default_rng(701)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = np.zeros((h, w), np.float32)
    for k in range(6):
        f = 2 ** k
        ph = rnd.uniform(0, 6.28, 3)
        n += np.sin(xx / w * 6.28 * f + ph[0] + 1.3 * np.sin(yy / h * 6.28 * f + ph[1])) * np.cos(yy / h * 3.14 * f + ph[2]) / (k + 1)
    n = (n - n.min()) / (n.max() - n.min())
    v = 0.86 + 0.12 * n
    img = np.stack([v * 0.97, v * 0.99, v * 1.0], -1)
    # cráteres suaves en el norte
    for _ in range(140):
        cx, cy, r = rnd.uniform(0, w), rnd.uniform(0, h * 0.6), rnd.uniform(6, 30)
        d = np.hypot(xx - cx, yy - cy)
        img[d < r] *= 0.9
    # 'rayas de tigre' azuladas cerca del polo sur (donde salen los géiseres)
    for k in range(4):
        yc = h * (0.80 + 0.035 * k)
        band = np.abs(yy - (yc + 18 * np.sin(xx / w * 6.28 * 3 + k))) < 5
        img[band] = [0.45, 0.68, 0.85]
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
    im.save(path)
    return S.load("enceladus_proc.png")


ENC = enc_texture()


def enceladus(c, x, y, R, t):
    S.draw_planet(c, x, y, R, S.render(2 * R, ENC, spin=t * 0.08, light=L0, gain=1.15, limb=0.5, ambient=0.1))
    S.atmosphere(c, x, y, R, color=0xFFBFE6FF, strength=0.5)


def plumes(c, x, y, R, t, k=1.0, n=260):
    """Chorros de hielo desde el polo sur: partículas balísticas que salen en abanico hacia abajo."""
    rr = random.Random(17)
    for i in range(n):
        src = rr.uniform(-0.45, 0.45)
        sx, sy = x + src * R, y + R * math.sqrt(max(0, 1 - src * src)) * 0.98
        ang = math.pi / 2 + src * 0.9 + rr.uniform(-0.18, 0.18)
        ph = (t * rr.uniform(0.25, 0.45) + rr.random()) % 1.0
        d = ph * R * rr.uniform(1.4, 2.6)
        px, py = sx + math.cos(ang) * d, sy + math.sin(ang) * d
        a = k * (1 - ph) * 0.7
        c.drawCircle(px, py, 3 + ph * 7, skia.Paint(AntiAlias=True, Color=with_alpha(0xFFE8F6FF, a), MaskFilter=blur(3)))


def ocean_cut(c, x, y, R, t, k):
    """Corte: corteza de hielo, océano global y núcleo rocoso."""
    c.drawCircle(x, y, R, fill(0xFFE8F0F8))
    c.drawCircle(x, y, R * 0.86, fill(0xFF1A5A9A))
    for j in range(10):
        rr = R * (0.6 + 0.024 * j)
        c.drawCircle(x, y, rr, stroke(with_alpha(0xFF3A8ADA, 0.25), 3 + math.sin(t * 2 + j)))
    c.drawCircle(x, y, R * 0.58, skia.Paint(Shader=skia.GradientShader.MakeRadial((x - 40, y - 40), R * 0.6, [0xFF8A6A4A, 0xFF4A3424]), AntiAlias=True))
    # tapa: la mitad derecha sigue entera hasta que se abre
    c.save(); c.clipRect(skia.Rect.MakeLTRB(x + R * 2 * k - R, y - R - 2, x + R + 2, y + R + 2))
    enceladus(c, x, y, R, t)
    c.restore()


def s_encelado(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF02030A)
    ST.draw(c, t, camx=t * 9, alpha=0.9)
    if sid == "h":
        D.saturn(c, W * 0.18, 520, 200, t)
        R = lerp(300, 380, ease_out(clamp(t / 3)))
        enceladus(c, W / 2 + 40, 1000, R, t)
        plumes(c, W / 2 + 40, 1000, R, t)
        hc.stamp(c, "ESCUPE AGUA", W / 2, 1800, lt, 1.0, 100, col=0xFF3AA8FF)
    elif sid == "s1":
        enceladus(c, W / 2, 1100, 420, t)
        K.tag(c, W / 2, 1720, "≈ 500 km · LUNA DE SATURNO", lt - 0.4, accent=V["accent"], size=40)
    elif sid == "s2":
        R = 330
        enceladus(c, W / 2, 860, R, t)
        plumes(c, W / 2, 860, R, t, k=ease_out(clamp(lt / 0.8)))
        hc.big(c, "2005", W / 2 - 230, 1750, 110, V["accent"], lt, 0.2)
        K.counter(c, t, lt - 1.6, lambda p: str(int(round(101 * p))), "GÉISERES (NASA 2014)", V["accent"], y=1720, size=120) if lt > 1.6 else None
    elif sid == "s3":
        ocean_cut(c, W / 2, 1150, 430, t, ease_in_out(clamp((lt - 0.3) / 1.2)))
        K.tag(c, W / 2, 1720, "OCÉANO BAJO EL HIELO", lt - 1.0, accent=V["accent"], size=44)
    elif sid == "s4":
        # anillo E alimentado por los chorros
        cx, cy = W / 2, 1150
        for j in range(60):
            c.drawOval(skia.Rect.MakeXYWH(cx - 520 - j * 2, cy - 120 - j * 0.6, 1040 + j * 4, 240 + j * 1.2),
                       stroke(with_alpha(0xFF9ACAFF, 0.03 * ease_out(clamp(lt / 1.5))), 3))
        D.saturn(c, cx, cy, 170, t)
        a = t * 0.6
        ex, ey = cx + math.cos(a) * 560, cy + math.sin(a) * 140
        enceladus(c, ex, ey, 40, t)
        plumes(c, ex, ey, 40, t, n=80)
        K.tag(c, W / 2, 1600, "ANILLO E", lt - 0.5, accent=V["accent"], size=56)
    else:
        enceladus(c, W / 2, 1100, 380, t)
        plumes(c, W / 2, 1100, 380, t)


V701 = dict(slug="701_encelado_geiseres", accent=0xFF7AD0FF, drone=0.03, scene=s_encelado, tease="LO PROMETIDO", mood="epico",
            send="ENVÍASELO A QUIEN LE GUSTE EL ESPACIO", rehook=("s3", "¿Y DE DÓNDE SALE?"), reveal=("s3", "DE DÓNDE SALE"), segs=[
    dict(id="h", who="nar", say="Esta luna de Saturno escupe agua al espacio. Y una sonda lo vio.",
         cap="Esta luna *escupe agua* | al *ESPACIO*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Es Encélado. Mide unos quinientos kilómetros, y está cubierta de hielo.",
         cap="Es *Encélado*: unos | *500 km* cubiertos | de *hielo*"),
    dict(id="s2", who="nar", cut=True, say="En dos mil cinco, la sonda Cassini vio chorros saliendo de su polo sur. En dos mil catorce, la NASA contó ciento uno.",
         cap="En *2005*, Cassini vio *chorros* | en su polo sur. | La NASA contó *101*"),
    dict(id="s3", who="nar", cut=True, say="¿Y de dónde sale? Bajo el hielo hay un océano entero, que rodea toda la luna.",
         cap="Bajo el hielo hay | un *OCÉANO* entero", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y ese hielo que escupe no se pierde: alimenta uno de los anillos de Saturno, el anillo E.",
         cap="Ese hielo alimenta | un anillo de Saturno: | el *anillo E*"),
    dict(id="cta", who="nar", cut=True, say="¿Crees que hay vida en ese océano? Comenta sí o no. Y sígueme: la próxima luna es todavía más rara.",
         cap="¿Hay *vida* ahí abajo? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 702 Mito: el cuac del pato no hace eco
def pond(c, t):
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF9AD0F0, 0xFFD8EEF8, 0xFF4A8AA8, 0xFF1E5A78], [0, 0.4, 0.55, 1])))
    for k in range(3):
        y = 980 + k * 30
        p = skia.Path(); p.moveTo(0, 1060)
        for x in range(0, W + 30, 30):
            p.lineTo(x, y - 40 * math.sin(x * 0.006 + k * 1.7) - 25)
        p.lineTo(W, 1060); p.close()
        c.drawPath(p, fill([0xFF6AA05A, 0xFF5A904A, 0xFF4A803A][k]))
    for k in range(16):
        y = 1080 + k * k * 3.6
        c.drawLine(0, y + math.sin(t + k) * 4, W, y + math.sin(t * 1.3 + k) * 4, stroke(with_alpha(WHITE, 0.10), 2 + k * 0.25))


def duck(c, x, y, s, t, quack=0.0):
    c.save(); c.translate(x, y + math.sin(t * 2) * 6); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-180, 40, 380, 50), fill(with_alpha(0xFF0A3A58, 0.35)))
    body = skia.Path(); body.moveTo(-190, -10); body.cubicTo(-200, -120, 80, -110, 160, -40); body.cubicTo(200, 30, 120, 70, 0, 70)
    body.cubicTo(-120, 70, -210, 40, -190, -10); body.close()
    c.drawPath(body, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, -110), (0, 70)], [0xFFB89A7A, 0xFF6A5040]), AntiAlias=True))
    wing = skia.Path(); wing.moveTo(-120, -40); wing.cubicTo(-40, -80, 60, -60, 100, -20); wing.cubicTo(20, 10, -80, 10, -120, -40); wing.close()
    c.drawPath(wing, fill(0xFF5A4232))
    c.drawRect(skia.Rect.MakeXYWH(-20, -40, 60, 14), fill(0xFF3A5AC8))  # espejuelo azul
    c.drawRect(skia.Rect.MakeXYWH(90, -150, 50, 120), fill(0xFFE8E2D2))  # collar
    head = skia.Paint(Shader=skia.GradientShader.MakeRadial((120, -200), 110, [0xFF2A9A5A, 0xFF0A4A2A]), AntiAlias=True)
    c.drawCircle(130, -190, 80, head)
    c.drawCircle(160, -210, 11, fill(0xFF101010)); c.drawCircle(163, -213, 3, fill(WHITE))
    o = 22 * quack
    up = skia.Path(); up.moveTo(195, -205 - o * 0.4); up.cubicTo(250, -205 - o, 290, -190 - o, 290, -178 - o * 0.6); up.lineTo(200, -175); up.close()
    lo = skia.Path(); lo.moveTo(200, -175); lo.lineTo(285, -172 + o * 0.6); lo.cubicTo(270, -158 + o, 230, -158 + o, 200, -160); lo.close()
    c.drawPath(up, fill(0xFFF2B21A)); c.drawPath(lo, fill(0xFFE09A12))
    c.restore()


def sound_rings(c, x, y, t, k=1.0, col=WHITE, n=4, speed=1.0):
    for i in range(n):
        ph = (t * speed + i / n) % 1.0
        r = 40 + ph * 420
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), -50, 100)
        c.drawPath(p, stroke(with_alpha(col, k * (1 - ph) * 0.9), 9))


def wave_plot(c, t, lt, x0, y0, w, h, echo=0.0, show_echo=True):
    """Forma de onda del cuac (ráfaga que se apaga) + eco retrasado y más débil."""
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 - 20, y0 - h / 2 - 30, w + 40, h + 60), 24, 24), fill(with_alpha(0xFF0B0E1A, 0.85)))
    c.drawLine(x0, y0, x0 + w, y0, stroke(with_alpha(WHITE, 0.3), 2))
    upto = clamp(lt / 1.6)
    for which, (off, amp, col) in enumerate(((0.05, 1.0, 0xFFF2B21A), (0.30, 0.42 * echo, 0xFF7AD0FF))):
        if which == 1 and not show_echo:
            continue
        p = skia.Path()
        first = True
        for i in range(400):
            u = i / 400
            if u > upto:
                break
            v = u - off
            a = amp * (math.exp(-v * 5.5) if v > 0 else 0) * (1 if v < 0.55 else 0)
            yy = y0 - math.sin(i * 1.7) * a * h * 0.45
            if first:
                p.moveTo(x0 + u * w, yy); first = False
            else:
                p.lineTo(x0 + u * w, yy)
        c.drawPath(p, stroke(col, 4))


def chamber(c, t, lt):
    """Cámara de reverberación: paredes duras inclinadas y el sonido rebotando."""
    c.drawPaint(fill(0xFF2A2E36))
    for i in range(7):
        for j in range(12):
            x, y = i * 170 - 40 + (j % 2) * 85, 300 + j * 140
            pth = skia.Path(); pth.moveTo(x, y); pth.lineTo(x + 160, y + 20); pth.lineTo(x + 150, y + 130); pth.lineTo(x - 10, y + 110); pth.close()
            sh = 0xFF8A909A if (i + j) % 3 else 0xFF6A707A
            c.drawPath(pth, fill(sh))
            c.drawPath(pth, stroke(0xFF3A3E46, 3))
    rr = random.Random(4)
    for k in range(18):
        ph = (lt * 0.6 + k / 18) % 1
        x = W / 2 + math.cos(k * 2.1) * 420 * ph
        y = 1150 + math.sin(k * 1.3) * 520 * ph
        c.drawCircle(x, y, 10 + 20 * ph, stroke(with_alpha(0xFF7AD0FF, 0.8 * (1 - ph)), 4))


def s_pato(c, t, P, V):
    sid, lt = seg(P, t)
    if sid == "h":
        pond(c, t)
        q = max(0, math.sin(t * 7)) if lt < 2.4 else 0
        duck(c, W / 2 - 60, 1160, 1.5, t, quack=q)
        sound_rings(c, W / 2 + 330, 880, t, k=0.9)
        hc.stamp(c, "MENTIRA", W / 2, 1780, lt, 1.3, 130, col=RED)
    elif sid == "s1":
        pond(c, t)
        duck(c, W / 2 - 60, 1160, 1.4, t)
        K.tag(c, W / 2, 620, "TREVOR COX · UNIV. DE SALFORD", lt - 0.3, accent=V["accent"], size=36)
        hc.big(c, "2003", W / 2, 1780, 120, V["accent"], lt, 0.6)
        K.tag(c, W / 2 + 200, 760, "«DAISY»", lt - 1.4, accent=WHITE, size=46)
    elif sid == "s2":
        chamber(c, t, lt)
        duck(c, W / 2 - 60, 1250, 1.0, t, quack=max(0, math.sin(t * 7)))
        K.tag(c, W / 2, 1780, "CÁMARA DE REVERBERACIÓN", lt - 0.4, accent=V["accent"], size=40)
    elif sid == "s3":
        chamber(c, t, lt + 3)
        c.drawPaint(fill(0x99000000))
        wave_plot(c, t, lt, 110, 1100, W - 220, 420, echo=ease_out(clamp((lt - 0.8) / 0.5)))
        if lt > 1.2:
            hc.stamp(c, "SÍ HACE ECO", W / 2, 1600, lt, 1.2, 110, col=GREEN)
    elif sid == "s4":
        pond(c, t)
        c.drawPaint(fill(0x66000000))
        wave_plot(c, t, lt + 2, 110, 1050, W - 220, 420, echo=1.0)
        k = ease_in_out(clamp((lt - 0.8) / 1.0))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(110 + (W - 220) * 0.27, 820, (W - 220) * 0.35 * k + 1, 460), 20, 20), stroke(RED, 8))
        K.tag(c, W / 2, 1420, "EL ECO SE ESCONDE EN LA COLA", lt - 1.4, accent=V["accent"], size=36)
    else:
        pond(c, t)
        duck(c, W / 2 - 60, 1160, 1.5, t, quack=max(0, math.sin(t * 7)))


V702 = dict(slug="702_mito_pato_eco", accent=0xFFF2B21A, drone=0.02, scene=s_pato, tease="CASI TODOS LO CREEN", mood="luz",
            send="ENVÍASELO A QUIEN SE LO CREÍA", rehook=("s3", "Y EL RESULTADO FUE…"), reveal=("s3", "EL RESULTADO"), segs=[
    dict(id="h", who="nar", say="Seguro que has oído que el cuac de un pato no hace eco. Es mentira.",
         cap="«El cuac de un pato | no hace *eco*». | Es *MENTIRA*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="En dos mil tres, el experto en acústica Trevor Cox, de la Universidad de Salford, lo probó con una pata llamada Daisy.",
         cap="En *2003*, el acústico | *Trevor Cox* lo probó | con una pata: *Daisy*"),
    dict(id="s2", who="nar", cut=True, say="La grabó en una cámara de reverberación: una sala hecha para que todo rebote.",
         cap="La grabó en una sala | hecha para que | todo *REBOTE*"),
    dict(id="s3", who="nar", cut=True, say="Y el cuac hizo eco. Como cualquier otro sonido.",
         cap="El cuac hizo *ECO*. | Como cualquier sonido", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="¿Por qué no lo oímos? Porque el cuac es bajito y se apaga poco a poco. El eco se mezcla con el final del propio cuac.",
         cap="El cuac es *bajito* y se apaga | poco a poco: el eco | se *ESCONDE* en su final"),
    dict(id="cta", who="nar", cut=True, say="¿Tú te lo creías? Comenta sí o no. Y sígueme para otro mito de animales.",
         cap="¿Te lo creías? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 703 Mito de clase: María Antonieta y los pasteles
def book(c, t, lt, quote=True):
    c.save(); c.translate(W / 2, 1150); c.rotate(-3 + math.sin(t * 0.5) * 0.8)
    for side in (-1, 1):
        r = skia.Rect.MakeXYWH(-440 if side < 0 else 0, -520, 440, 1040)
        c.drawRect(r.makeOffset(10, 18), fill(0x77000000))
        c.drawRect(r, skia.Paint(Shader=skia.GradientShader.MakeLinear([(side * 440, 0), (0, 0)], [0xFFF0E4C4, 0xFFC8B890])))
    c.drawLine(0, -520, 0, 520, stroke(0xFF8A7A5A, 4))
    draw_text(c, "LES CONFESSIONS", -220, -420, 40, 0xFF3A2A1A, shadow=False)
    draw_text(c, "Rousseau", -220, -360, 36, 0xFF6A4A2A, shadow=False)
    for i in range(14):
        c.drawRect(skia.Rect.MakeXYWH(-400, -290 + i * 52, 330 - (i % 4) * 40, 16), fill(0xFFB8A880))
        c.drawRect(skia.Rect.MakeXYWH(40, -460 + i * 52, 340 - (i % 3) * 50, 16), fill(0xFFB8A880))
    if quote:
        a = clamp((lt - 0.4) / 0.4)
        c.drawRect(skia.Rect.MakeXYWH(30, 300, 380, 170), fill(with_alpha(0xFFFFE04D, 0.55 * a)))
        draw_text(c, "«une grande", 220, 360, 38, with_alpha(0xFF1A1A1A, a), shadow=False)
        draw_text(c, "princesse»", 220, 420, 38, with_alpha(0xFF1A1A1A, a), shadow=False)
    c.restore()


def brioche(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-240, 60, 480, 70), fill(0x66000000))
    base = skia.Path(); base.moveTo(-220, 80)
    for i in range(13):
        a = math.pi + i * math.pi / 12
        base.lineTo(math.cos(a) * 230 + (12 if i % 2 else -12) * math.cos(a), -20 + math.sin(a) * 120 + (10 if i % 2 else 0))
    base.lineTo(220, 80); base.close()
    c.drawPath(base, skia.Paint(Shader=skia.GradientShader.MakeRadial((-60, -80), 320, [0xFFF2B05A, 0xFFB8641E, 0xFF7A3A10]), AntiAlias=True))
    c.drawCircle(0, -150, 90, skia.Paint(Shader=skia.GradientShader.MakeRadial((-30, -190), 130, [0xFFF6C06A, 0xFFB8641E]), AntiAlias=True))
    glow(c, -60, -180, 60, WHITE, 0.25)
    c.restore()


def timeline(c, t, lt, accent):
    y = 1150
    c.drawLine(80, y, W - 80, y, stroke(WHITE, 8))
    marks = [(1755, "NACE", 0.0), (1767, "ROUSSEAU", 0.5), (1793, "MUERE", 1.6), (1843, "1ª VEZ CON SU NOMBRE", 2.3)]
    for yr, lab, d in marks:
        x = lerp(120, W - 120, (yr - 1750) / 100)
        a = clamp((lt - d) / 0.3)
        if a <= 0:
            continue
        hot = yr in (1767, 1843)
        c.drawCircle(x, y, 18 + 8 * hot, fill(with_alpha(accent if hot else WHITE, a)))
        up = -1 if marks.index((yr, lab, d)) % 2 == 0 else 1
        draw_text(c, str(yr), x, y + up * 90 + 20, 52, with_alpha(accent if hot else WHITE, a))
        draw_text(c, lab, x, y + up * 160 + 14, 30, with_alpha(WHITE, a))


def s_antonieta(c, t, P, V):
    sid, lt = seg(P, t)
    D.paper(c, t)
    if sid == "h":
        brioche(c, W / 2, 1230, 1.5, t)
        hc.stamp(c, "NUNCA LO DIJO", W / 2, 1760, lt, 1.0, 100, col=RED)
    elif sid == "s1":
        book(c, t, lt)
        hc.big(c, "≈1767", W / 2, 1820, 110, V["accent"], lt, 0.8)
    elif sid == "s2":
        timeline(c, t, lt, V["accent"])
        if lt > 1.6:
            K.tag(c, W / 2, 1600, "TENÍA UNOS 11 AÑOS Y VIVÍA EN VIENA", lt - 1.6, accent=V["accent"], size=34)
    elif sid == "s3":
        brioche(c, W / 2, 1150, 1.6, t)
        K.tag(c, W / 2, 1620, "«QU'ILS MANGENT DE LA BRIOCHE»", lt - 0.4, accent=V["accent"], size=36)
    elif sid == "s4":
        timeline(c, t, 5, V["accent"])
        k = ease_out(clamp((lt - 0.3) / 0.5))
        c.drawCircle(lerp(120, W - 120, 0.93), 1150, 70 * k, stroke(RED, 9))
        K.tag(c, W / 2, 1600, "MEDIO SIGLO DESPUÉS DE MORIR", lt - 0.8, accent=V["accent"], size=36)
    else:
        brioche(c, W / 2, 1230, 1.5, t)


V703 = dict(slug="703_mito_maria_antonieta", accent=0xFFFF7AA8, drone=0.02, scene=s_antonieta, tease="TE LO ENSEÑARON MAL",
            send="ENVÍASELO A QUIEN LE GUSTE LA HISTORIA", rehook=("s2", "MIRA LAS FECHAS"), reveal=("s2", "LA PRUEBA"), segs=[
    dict(id="h", who="nar", say="María Antonieta nunca dijo «que coman pasteles». Y se puede demostrar.",
         cap="María Antonieta *NUNCA* dijo | «que coman *pasteles*»", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="La frase aparece en las Confesiones de Rousseau, escritas hacia mil setecientos sesenta y siete. Él se la atribuye a una gran princesa, sin nombre.",
         cap="Sale en las *Confesiones* | de Rousseau (*≈1767*): | «una gran *princesa*», sin nombre"),
    dict(id="s2", who="nar", cut=True, say="Pero en esa época, María Antonieta era una niña de unos once años, y vivía en Viena.",
         cap="En esa época era una *NIÑA* | de unos *11 años* | y vivía en *Viena*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Además, la frase original no habla de pasteles: dice «que coman brioche».",
         cap="Y la frase original | no dice pasteles: | dice *BRIOCHE*"),
    dict(id="s4", who="nar", cut=True, say="Y la primera vez que alguien se la atribuyó a ella fue en mil ochocientos cuarenta y tres. Medio siglo después de su muerte.",
         cap="Se le atribuyó en *1843*: | *medio siglo* después | de su muerte"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo enseñaron así en clase? Comenta sí o no. Y sígueme para más mitos que te tragaste en clase.",
         cap="¿Te lo enseñaron así? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 704 El picante no es un sabor
def chili(c, x, y, s, t, ang=-20):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(ang + math.sin(t * 1.5) * 3)
    p = skia.Path(); p.moveTo(-40, -260); p.cubicTo(80, -250, 120, -60, 70, 120); p.cubicTo(40, 240, -20, 300, -60, 330)
    p.cubicTo(-40, 220, -90, 60, -100, -60); p.cubicTo(-110, -180, -90, -250, -40, -260); p.close()
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeLinear([(-110, 0), (110, 0)], [0xFF8A0A0A, 0xFFE8241A, 0xFFB01010]), AntiAlias=True))
    c.drawPath(p, skia.Paint(AntiAlias=True, Color=with_alpha(WHITE, 0.25), Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    hl = skia.Path(); hl.moveTo(-60, -200); hl.cubicTo(-20, -210, 10, -120, -10, 40)
    c.drawPath(hl, stroke(with_alpha(WHITE, 0.45), 14))
    st = skia.Path(); st.moveTo(-50, -255); st.cubicTo(-60, -320, -10, -360, 40, -350)
    c.drawPath(st, stroke(0xFF2E7A2A, 26))
    c.drawOval(skia.Rect.MakeXYWH(-90, -290, 110, 50), fill(0xFF3A8A2E))
    c.restore()


def tongue(c, x, y, s, t, fire=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-300, -260); p.cubicTo(-320, 120, -180, 360, 0, 360); p.cubicTo(180, 360, 320, 120, 300, -260); p.close()
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeRadial((0, 0), 420, [0xFFFF8A9A, 0xFFE0506A, 0xFFA0283A]), AntiAlias=True))
    c.drawLine(0, -240, 0, 200, stroke(with_alpha(0xFF8A1A2A, 0.5), 10))
    rr = random.Random(3)
    for i in range(70):
        px, py = rr.uniform(-250, 250), rr.uniform(-230, 300)
        if abs(px) > 270 - (py + 260) * 0.05:
            continue
        on = fire > 0 and rr.random() < fire
        c.drawCircle(px, py, 9, fill(0xFFFFD21A if on else with_alpha(0xFFFFB0BA, 0.7)))
        if on:
            glow(c, px, py, 40, 0xFFFF8A1A, 0.6)
    c.restore()


def flames(c, t, k=1.0, y0=H):
    rr = random.Random(8)
    for i in range(120):
        x = rr.uniform(0, W)
        ph = (t * rr.uniform(0.6, 1.1) + rr.random()) % 1.0
        y = y0 - ph * rr.uniform(300, 700)
        r = (1 - ph) * rr.uniform(30, 70)
        col = 0xFFFFD21A if ph < 0.3 else (0xFFFF7A1A if ph < 0.6 else 0xFFE82A1A)
        c.drawCircle(x + math.sin(t * 5 + i) * 20, y, r, skia.Paint(AntiAlias=True, Color=with_alpha(col, 0.5 * k * (1 - ph)), MaskFilter=blur(10)))


def milk(c, x, y, s, t, lvl=0.8, liq=0xFFF8F6EE):
    c.save(); c.translate(x, y); c.scale(s, s)
    glass = skia.Path(); glass.moveTo(-170, -300); glass.lineTo(170, -300); glass.lineTo(140, 300); glass.lineTo(-140, 300); glass.close()
    c.drawPath(glass, fill(with_alpha(WHITE, 0.15)))
    c.save(); c.clipPath(glass, doAntiAlias=True)
    top = lerp(300, -280, lvl)
    c.drawRect(skia.Rect.MakeLTRB(-200, top + math.sin(t * 3) * 5, 200, 320), fill(liq))
    c.restore()
    c.drawPath(glass, stroke(with_alpha(WHITE, 0.8), 8))
    c.drawLine(-120, -250, -100, 240, stroke(with_alpha(WHITE, 0.5), 10))
    c.restore()


def s_picante(c, t, P, V):
    sid, lt = seg(P, t)
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, 1100), 1300, [0xFF3A0A08, 0xFF0A0202])))
    if sid == "h":
        flames(c, t, k=ease_out(clamp(t / 1.5)))
        chili(c, W / 2, 1150, 1.4, t)
        hc.stamp(c, "ES DOLOR", W / 2, 1780, lt, 1.0, 130, col=0xFFFF7A1A)
    elif sid == "s1":
        tongue(c, W / 2, 1150, 1.4, t, fire=ease_out(clamp((lt - 0.8) / 1.2)))
        chili(c, W / 2 + 330, 760, 0.6, t, ang=40)
        K.tag(c, W / 2, 1720, "RECEPTOR TRPV1 = SENSOR DE CALOR", lt - 0.6, accent=V["accent"], size=36)
    elif sid == "s2":
        flames(c, t, k=0.8)
        D.thermo(c, W / 2, 1400, lerp(20, 39, ease_out(clamp(lt / 1.5))), t)
        for i, lab in enumerate(("SUDOR", "CARA ROJA", "LÁGRIMAS")):
            K.tag(c, W / 2 + (i - 1) * 330, 1720, lab, lt - 0.5 - 0.4 * i, accent=V["accent"], size=36)
    elif sid == "s3":
        k = ease_in_out(clamp((lt - 1.6) / 0.8))
        c.save(); c.translate(-W * 0.25 * k, 0)
        milk(c, W / 2, 1150, 1.2, t, lvl=0.75, liq=with_alpha(0xFF5AB8F0, 0.7))  # vaso de agua
        c.restore()
        if lt < 2.0:
            draw_text(c, "AGUA", W / 2, 1720, 90, WHITE)
            if lt > 0.8:
                hc.stamp(c, "NO", W / 2, 1100, lt, 0.8, 200, col=RED)
        else:
            milk(c, W / 2, 1150, 1.3, t, lvl=0.8)
            K.tag(c, W / 2, 1640, "LA LECHE SÍ", lt - 2.0, accent=V["accent"], size=56)
    elif sid == "s4":
        hc.big(c, "NOBEL 2021", W / 2, 1100, 140, V["accent"], lt, 0.2)
        K.tag(c, W / 2, 1320, "DAVID JULIUS · MEDICINA", lt - 0.7, accent=WHITE, size=40)
        chili(c, W / 2, 1650, 0.6, t, ang=-70)
    else:
        flames(c, t, k=0.6)
        chili(c, W / 2, 1150, 1.3, t)


V704 = dict(slug="704_picante_es_dolor", accent=0xFFFF9A2A, drone=0.02, scene=s_picante, tease="TU CEREBRO CREE QUE ARDES",
            send="ENVÍASELO A QUIEN NO AGUANTA EL PICANTE", rehook=("s3", "Y EL AGUA NO SIRVE"), reveal=("s3", "EL TRUCO"), segs=[
    dict(id="h", who="nar", say="El picante no es un sabor. Es dolor. Y tu cerebro cree que te estás quemando.",
         cap="El picante *NO* es un sabor. | Es *DOLOR*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="La capsaicina de la guindilla activa un receptor de tu lengua, el TRPV1. Es el mismo que detecta el calor de verdad.",
         cap="La *capsaicina* activa | el receptor que detecta | el *CALOR* de verdad"),
    dict(id="s2", who="nar", cut=True, say="Por eso sudas, te pones rojo y te lloran los ojos: tu cuerpo intenta enfriar un fuego que no existe.",
         cap="Sudas, te pones *rojo*… | tu cuerpo enfría un | *fuego que no existe*"),
    dict(id="s3", who="nar", cut=True, say="Y por eso el agua casi no ayuda: la capsaicina no se disuelve en agua. La leche sí te la quita.",
         cap="El *agua* casi no ayuda: | no la disuelve. | La *LECHE* sí", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Quien descubrió ese receptor, David Julius, ganó el Nobel de Medicina en dos mil veintiuno.",
         cap="Descubrirlo le dio a | *David Julius* el *Nobel* | de Medicina en *2021*"),
    dict(id="cta", who="nar", cut=True, say="¿Tú aguantas el picante? Comenta sí o no. Y sígueme para más cosas que hace tu cuerpo.",
         cap="¿Aguantas el picante? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== Ilusiones T5: fondo común
SERIE = "ILUSIONES IMPOSIBLES T5 · PARTE {}/3"


def ilu_bg(c, t, seed):
    hc.aurora(c, t, 0xFF1A2A6A, 0xFF4A1A5A, seed=seed)


# ====================================================================== 705 T5 P1: Cornsweet
def cornsweet(c, cx, cy, cover=0.0, w=800, h=1000):
    x0, y0 = cx - w / 2, cy - h / 2
    g = 0.5
    edge = 170
    n = 120
    for i in range(n):
        u = i / n
        y = y0 + u * h
        d = (u - 0.5) * h  # distancia al borde central
        v = g
        if -edge < d < 0:
            v = g - 0.22 * (1 + d / edge) ** 2  # arriba: oscurece al acercarse al borde
        elif 0 <= d < edge:
            v = g + 0.22 * (1 - d / edge) ** 2  # abajo: aclara al acercarse al borde
        col = int(clamp(v) * 255)
        c.drawRect(skia.Rect.MakeXYWH(x0, y, w, h / n + 1), fill(0xFF000000 | (col << 16) | (col << 8) | col))
    if cover > 0:
        hh = 2 * edge + 40
        c.drawRect(skia.Rect.MakeXYWH(x0 - 30, cy - hh / 2, (w + 60) * cover, hh), fill(0xFF101010))


def s_cornsweet(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 705)
    cx, cy = W / 2, 1200
    cov = 0.0
    if sid == "s2":
        cov = ease_in_out(clamp((lt - 0.3) / 1.0))
    elif sid == "s3":
        cov = 1.0 - ease_in_out(clamp((lt - 0.4) / 0.8)) if int(lt * 1.2) % 2 == 0 else 1.0
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 430, cy - 530, 860, 1060), 30, 30), fill(0xFF101010))
    cornsweet(c, cx, cy, cover=cov)
    if sid in ("h", "s1"):
        K.tag(c, W / 2 - 330, cy - 300, "A", lt - 0.2, accent=V["accent"], size=60)
        K.tag(c, W / 2 - 330, cy + 300, "B", lt - 0.2, accent=V["accent"], size=60)
    if sid == "h":
        hc.timer(c, W / 2, 1860, 52, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2" and lt > 1.4:
        hc.stamp(c, "MISMO GRIS", W / 2, 1850, lt, 1.4, 90, col=RED)
    if sid == "s4":
        hc.big(c, "1970", W / 2, 1850, 120, V["accent"], lt, 0.3)


V705 = dict(slug="705_ilusion_cornsweet_t5p1", accent=ILU, drone=0.02, scene=s_cornsweet, badge=SERIE.format(1), mood="misterio",
            send="ENVÍASELO A QUIEN DIGA QUE VE BIEN", rehook=("s2", "TAPO SOLO LA RAYA"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Qué mitad es más oscura, la de arriba o la de abajo?",
         cap="¿Qué mitad es | más *OSCURA*: | la *A* o la *B*?", hold=1.4),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo dice la de arriba. Elige tú, y luego mira.",
         cap="Casi todos dicen la *A*. | Elige… y *MIRA*", hold=0.5),
    dict(id="s2", who="nar", cut=True, say="Si tapo solo la raya del medio, las dos mitades son exactamente el mismo gris.",
         cap="Si tapo la *raya* del medio… | son *EXACTAMENTE* | el mismo gris", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Quito la tapa, y vuelven a parecer distintas.", cap="Quito la tapa… | y vuelven a *engañarte*", hold=0.8),
    dict(id="s4", who="nar", say="Es la ilusión de Cornsweet, de mil novecientos setenta. Tu cerebro solo mira el borde, y se inventa el resto.",
         cap="*Ilusión de Cornsweet*: | tu cerebro mira el *borde* | y se *INVENTA* el resto"),
    dict(id="cta", who="nar", cut=True, say="Temporada cinco, parte uno de tres. ¿Te engañó? Comenta sí o no. Y sígueme: la dos es todavía peor.",
         cap="T5, parte *1 de 3*. | ¿Te engañó? *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 706 Reto: ¿cuántos triángulos en el pentágono? (35)
def penta_geom(cx, cy, R):
    Pt = [(cx + R * math.cos(-math.pi / 2 + 2 * math.pi * k / 5), cy + R * math.sin(-math.pi / 2 + 2 * math.pi * k / 5)) for k in range(5)]
    segs = list(itertools.combinations(range(5), 2))

    def inter(s1, s2):
        (a, b), (cc, d) = s1, s2
        p, q, r, s = Pt[a], Pt[b], Pt[cc], Pt[d]
        den = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
        if abs(den) < 1e-9:
            return None
        tt = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / den
        u = ((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / den
        if -1e-9 <= tt <= 1 + 1e-9 and -1e-9 <= u <= 1 + 1e-9:
            return (round(p[0] + tt * (q[0] - p[0]), 3), round(p[1] + tt * (q[1] - p[1]), 3))
    onseg = {i: set() for i in range(len(segs))}
    for i, j in itertools.combinations(range(len(segs)), 2):
        x = inter(segs[i], segs[j])
        if x:
            onseg[i].add(x); onseg[j].add(x)
    allp = sorted(set().union(*onseg.values()))

    def same(a, b):
        return any(a in v and b in v for v in onseg.values())

    def area(tr):
        return abs((tr[1][0] - tr[0][0]) * (tr[2][1] - tr[0][1]) - (tr[1][1] - tr[0][1]) * (tr[2][0] - tr[0][0])) / 2
    tris = [tr for tr in itertools.combinations(allp, 3) if area(tr) > 1 and same(tr[0], tr[1]) and same(tr[1], tr[2]) and same(tr[0], tr[2])]
    groups = {}
    for tr in tris:
        groups.setdefault(round(area(tr) / 500), []).append(tr)
    order = [groups[k] for k in sorted(groups)]
    return Pt, segs, order


PT, PSEG, PGROUPS = penta_geom(W / 2, 1230, 470)
assert sum(len(g) for g in PGROUPS) == 35 and [len(g) for g in PGROUPS] == [5, 5, 10, 10, 5]


def s_penta(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A3A5A, 0xFF3A1A5A, seed=706)
    gid = {"s3": 0, "s4": 1, "s5": 2, "s6": 3, "s7": 4}
    base = [0, 5, 10, 20, 30]
    if sid in gid:
        g = PGROUPS[gid[sid]]
        dur = max(1.2, (P["tl"][sid][1] - P["tl"][sid][0]) - 0.5)
        shown = min(len(g), int(lt / (dur / len(g))) + 1)
        tr = g[shown - 1]
        p = skia.Path(); p.moveTo(*tr[0]); p.lineTo(*tr[1]); p.lineTo(*tr[2]); p.close()
        c.drawPath(p, fill(with_alpha(V["accent"], 0.4)))
        c.drawPath(p, stroke(V["accent"], 10))
        hc.big(c, str(base[gid[sid]] + shown), W / 2, 1880, 150, V["accent"], 1.0, 0.0)
    for a, b in PSEG:
        c.drawLine(*PT[a], *PT[b], stroke(WHITE, 9))
    if sid == "h":
        hc.timer(c, W / 2, 1860, 64, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s1":
        K.tag(c, W / 2, 1850, "COMENTA TU NÚMERO", lt - 0.2, accent=V["accent"], size=44)
    if sid == "cta":
        hc.stamp(c, "35", W / 2, 1860, lt, 0.1, 150, col=GREEN)


V706 = dict(slug="706_cuantos_triangulos_pentagono", accent=0xFF5AE0C8, drone=0.02, scene=s_penta, tease="EL MÁS DIFÍCIL HASTA AHORA",
            send="RETA A UN AMIGO: ENVÍASELO", rehook=("s5", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s3", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="¿Cuántos triángulos hay en esta estrella? Es el más difícil hasta ahora.",
         cap="¿Cuántos *TRIÁNGULOS* | hay aquí?", hold=1.5),
    dict(id="s1", who="nar", cut=True, say="Cuenta bien, que hay muchos escondidos. Escribe tu número antes de seguir.",
         cap="Hay muchos *escondidos*. | Escribe tu número | en *COMENTARIOS*", hold=0.6),
    dict(id="s2", who="q", cut=True, say="¿Ya? Vamos a contarlos.", cap="¿Ya? | Vamos a *contarlos*"),
    dict(id="s3", who="nar", cut=True, say="Los más pequeños: cinco.", cap="Los más pequeños: | *CINCO*", hold=1.0),
    dict(id="s4", who="nar", cut=True, say="Las puntas de la estrella: cinco más.", cap="Las *puntas*: | cinco más", hold=1.0),
    dict(id="s5", who="nar", cut=True, say="Estos, que nadie ve: diez.", cap="Estos que nadie ve: | *DIEZ*", hold=1.6),
    dict(id="s6", who="nar", cut=True, say="Otros diez más grandes.", cap="Otros *DIEZ* | más grandes", hold=1.6),
    dict(id="s7", who="nar", cut=True, say="Y los cinco gigantes.", cap="Y los cinco *GIGANTES*", hold=1.0),
    dict(id="cta", who="nar", cut=True, say="Treinta y cinco. ¿Cuántos dijiste tú? Comenta. Y sígueme para el próximo reto.",
         cap="Total: *35*. ¿Y tú? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 707 T5 P2: Ehrenstein (1941)
def ehrenstein(c, cx, cy, gap=1.0, spacing=200, n=4, fillk=0.0):
    x0 = cx - spacing * n / 2
    y0 = cy - spacing * n / 2
    for i in range(n + 1):
        for j in range(n + 1):
            x, y = x0 + i * spacing, y0 + j * spacing
            r = 52 * gap
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                L = spacing / 2
                c.drawLine(x + dx * r, y + dy * r, x + dx * L, y + dy * L, stroke(0xFF111111, 12))
            if fillk > 0:
                c.drawCircle(x, y, r - 4, stroke(with_alpha(RED, fillk), 6))


def s_ehren(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 707)
    cx, cy = W / 2, 1200
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 470, cy - 470, 940, 940), 30, 30), fill(0xFFF2F2F2))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 470, cy - 470, 940, 940), 30, 30))
    if sid == "s2":
        ehrenstein(c, cx, cy, fillk=ease_out(clamp((lt - 0.3) / 0.6)))
    elif sid == "s3":
        k = ease_in_out(clamp((lt - 0.3) / 1.2))
        ehrenstein(c, cx, cy, gap=1 - k * 0.98)
    else:
        ehrenstein(c, cx, cy)
    c.restore()
    if sid == "h":
        hc.timer(c, W / 2, 1830, 52, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2" and lt > 1.2:
        hc.stamp(c, "NO HAY BORDE", W / 2, 1830, lt, 1.2, 90, col=RED)
    if sid == "s4":
        hc.big(c, "1941", W / 2, 1830, 120, V["accent"], lt, 0.3)


V707 = dict(slug="707_ilusion_ehrenstein_t5p2", accent=ILU, drone=0.02, scene=s_ehren, badge=SERIE.format(2),
            send="ENVÍASELO A QUIEN VEA LOS CÍRCULOS", rehook=("s2", "MIRA EL BORDE"), reveal=("s2", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Ves círculos blancos, más brillantes que el fondo? No hay ninguno.",
         cap="¿Ves *círculos* blancos | más brillantes? | No hay *NINGUNO*", hold=1.4),
    dict(id="s1", who="nar", cut=True, say="Parecen discos de luz, con su borde y todo. Pero fíjate bien en ese borde.",
         cap="Parecen discos de *luz*… | con su borde y todo", hold=0.4),
    dict(id="s2", who="nar", cut=True, say="No existe. El blanco del centro es exactamente el mismo blanco del fondo.",
         cap="El blanco del centro es | *EL MISMO* | que el del fondo", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Si alargo las líneas hasta el centro, los círculos desaparecen.",
         cap="Si alargo las líneas… | *DESAPARECEN*", hold=0.6),
    dict(id="s4", who="nar", say="Es la ilusión de Ehrenstein, de mil novecientos cuarenta y uno. Tu cerebro ve dónde se cortan las líneas, y rellena un círculo.",
         cap="*Ilusión de Ehrenstein*, 1941: | tu cerebro ve los cortes | y *RELLENA* un círculo"),
    dict(id="cta", who="nar", cut=True, say="Temporada cinco, parte dos de tres. ¿Los viste? Comenta sí o no. Y sígueme: la tres es la más difícil.",
         cap="T5, parte *2 de 3*. | ¿Los viste? *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 708 MENTALISTA: adivino lo que piensas (formato experimental)
def card(c, x, y, txt, lt, col, size=200, rot=0):
    s = ease_back(clamp(lt / 0.35), 2.0)
    if s <= 0:
        return
    c.save(); c.translate(x, y); c.rotate(rot + math.sin(lt * 2) * 1.5); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-200, -270, 400, 540), 34, 34)
    c.drawRRect(r.makeOffset(10, 16), fill(0x88000000))
    c.drawRRect(r, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, -270), (0, 270)], [0xFF1E2448, 0xFF0E1026])))
    c.drawRRect(r, stroke(col, 8))
    f = font(size)
    if text_w(txt, f) > 340:
        size = size * 340 / text_w(txt, f)
    draw_text(c, txt, 0, size * 0.36, size, col)
    c.restore()


def mind_bg(c, t):
    c.clear(0xFF05040E)
    ST.draw(c, t, camx=t * 6, alpha=0.7, band=False)
    for k in range(3):
        r = 300 + 120 * k + 30 * math.sin(t * 1.5 + k)
        c.drawCircle(W / 2, 1150, r, stroke(with_alpha(0xFFB07AFF, 0.12), 3))
    glow(c, W / 2, 1150, 520, 0xFF7A3AFF, 0.18)


EARTH = D.DAY


def elephant(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    gr = skia.GradientShader.MakeRadial((-60, -120), 420, [0xFFB4B4BC, 0xFF7A7A84, 0xFF4A4A54])
    pnt = skia.Paint(Shader=gr, AntiAlias=True)
    for lx in (-170, -60, 60, 160):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(lx - 45, 40, 90, 260), 30, 30), pnt)
    c.drawOval(skia.Rect.MakeXYWH(-260, -200, 470, 330), pnt)
    c.drawCircle(220, -150, 140, pnt)
    ear = skia.Path(); ear.moveTo(170, -250); ear.cubicTo(60, -300, 40, -40, 150, -20); ear.close()
    c.drawPath(ear, fill(0xFF6A6A74))
    tr = skia.Path(); tr.moveTo(320, -150); tr.cubicTo(380, -40, 360, 120, 330 + 20 * math.sin(t * 2), 220)
    c.drawPath(tr, stroke(0xFF7A7A84, 60))
    c.drawCircle(260, -190, 12, fill(0xFF101010))
    tk = skia.Path(); tk.moveTo(300, -60); tk.quadTo(360, 10, 420, -10)
    c.drawPath(tk, stroke(0xFFF4F0E4, 18))
    c.restore()


def s_mente(c, t, P, V):
    sid, lt = seg(P, t)
    mind_bg(c, t)
    if sid == "h":
        glow(c, W / 2, 1150, 300 + 40 * math.sin(t * 4), 0xFFB07AFF, 0.4)
        hc.big(c, "?", W / 2, 1260, 420, V["accent"], lt, 0.0)
        hc.stamp(c, "TE LEO LA MENTE", W / 2, 1780, lt, 0.9, 90, col=0xFFB07AFF)
    elif sid == "s1":
        card(c, W / 2 - 220, 1150, "1–10", lt, WHITE, 150, -6)
        card(c, W / 2 + 220, 1150, "× 9", lt - 1.6, V["accent"], 170, 6)
    elif sid == "s2":
        card(c, W / 2 - 220, 1150, "a+b", lt, WHITE, 150, -6)
        card(c, W / 2 + 220, 1150, "− 5", lt - 1.6, V["accent"], 170, 6)
    elif sid == "s3":
        for i, L in enumerate("ABCDE"):
            a = clamp((lt - 0.3 * i) / 0.3)
            draw_text(c, f"{i + 1}={L}", W / 2 + (i - 2) * 200, 1150, 80, with_alpha(WHITE, a))
    elif sid == "s4":
        card(c, W / 2 - 220, 1150, "PAÍS", lt, WHITE, 120, -6)
        card(c, W / 2 + 220, 1150, "ANIMAL", lt - 1.8, V["accent"], 110, 6)
    elif sid == "s5":
        card(c, W / 2, 1150, "COLOR", lt, V["accent"], 130, 0)
    elif sid == "s6":
        # revelación: la Tierra gira hasta Dinamarca y aparece un elefante gris
        k = ease_in_out(clamp(lt / 1.6))
        R = 330
        S.draw_planet(c, W / 2, 900, R, S.render(2 * R, EARTH, spin=lerp(2.5, -0.17, k), light=L0, gain=1.1))
        S.atmosphere(c, W / 2, 900, R)
        if k > 0.95:
            c.drawCircle(W / 2 + R * 0.08, 900 - R * 0.8, 26 + 6 * math.sin(t * 8), stroke(RED, 8))
        elephant(c, W / 2 - 60, 1530, 0.75 * ease_back(clamp((lt - 1.0) / 0.5), 1.8), t)
    elif sid == "s7":
        for i, (L, col) in enumerate((("× 9 → 9", WHITE), ("9 − 5 = 4 → D", V["accent"]), ("D → DINAMARCA", WHITE))):
            a = clamp((lt - 0.2 - 0.8 * i) / 0.3)
            draw_text(c, L, W / 2, 900 + i * 220, 96, with_alpha(col, a))
    else:
        elephant(c, W / 2 - 60, 1200, 0.9, t)


V708 = dict(slug="708_mentalista_elefante_gris", accent=0xFFFFC23A, drone=0.03, scene=s_mente, tease="HAZLO EN TU CABEZA", mood="misterio",
            send="ENVÍASELO A UN AMIGO A VER SI CAE", rehook=("s4", "CASI LO TENGO"), reveal=("s6", "TU RESPUESTA"), loop=False, segs=[
    dict(id="h", who="nar", say="Voy a adivinar lo que estás pensando. Haz lo que te digo, en tu cabeza.",
         cap="Voy a *adivinar* lo que | estás pensando", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Piensa un número del uno al diez. Multiplícalo por nueve.",
         cap="Piensa un número del *1 al 10*. | Multiplícalo *por 9*", hold=1.0),
    dict(id="s2", who="nar", cut=True, say="Si te da de dos cifras, súmalas entre sí. Al resultado, réstale cinco.",
         cap="Si tiene *dos cifras*, súmalas. | Luego *réstale 5*", hold=1.0),
    dict(id="s3", who="nar", cut=True, say="Convierte ese número en una letra: uno es la A, dos es la B, tres la C…",
         cap="Ese número es una *letra*: | 1 = A, 2 = B, 3 = C…", hold=0.7),
    dict(id="s4", who="nar", cut=True, say="Piensa un país de Europa que empiece por esa letra. Y un animal que empiece por la letra siguiente.",
         cap="Un *país de Europa* con esa letra… | y un *animal* con | la letra *siguiente*", hold=1.0),
    dict(id="s5", who="nar", cut=True, say="Ahora piensa de qué color es ese animal.", cap="¿De qué *color* es | ese animal?", hold=0.8),
    dict(id="s6", who="q", cut=True, say="¿Un elefante gris… en Dinamarca?", cap="¿Un *ELEFANTE GRIS*… | en *DINAMARCA*?", hold=1.2),
    dict(id="s7", who="nar", cut=True, say="El truco: por nueve, siempre suma nueve. Menos cinco, cuatro: la D. Y en Europa, Dinamarca.",
         cap="Por 9 siempre suma *9*. | Menos 5 = *4* = *D*. | Y en Europa: *Dinamarca*"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo adiviné? Comenta sí o no. Y envíaselo a un amigo, a ver si cae.",
         cap="¿Te lo adiviné? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 709 Houdini P2: la última sesión (31/10/1936) — hoy hace 90 años
def ring(c, x, y, R, t, txt="ROSABELLE"):
    c.save(); c.translate(x, y); c.rotate(math.sin(t * 0.8) * 8)
    c.drawOval(skia.Rect.MakeXYWH(-R, -R * 0.55, 2 * R, 1.1 * R), stroke(0xFFE8C060, 60))
    c.drawOval(skia.Rect.MakeXYWH(-R, -R * 0.55, 2 * R, 1.1 * R), stroke(with_alpha(0xFFFFF0B0, 0.6), 10))
    glow(c, -R * 0.6, -R * 0.4, 80, WHITE, 0.4)
    draw_text(c, txt, 0, R * 0.2, 64, 0xFF5A3A10, shadow=False)
    c.restore()


def rooftop(c, t):
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF05061A, 0xFF1A1438, 0xFF3A2440])))
    ST.draw(c, t, alpha=0.6, band=False)
    c.drawCircle(W * 0.78, 420, 90, fill(0xFFF2EED8)); glow(c, W * 0.78, 420, 260, 0xFFF2EED8, 0.25)
    for k, (x, hgt) in enumerate(((60, 420), (220, 600), (420, 380), (700, 520), (900, 640))):
        c.drawRect(skia.Rect.MakeXYWH(x, 1500 - hgt, 170, hgt), fill(0xFF0E0C18))
        for i in range(int(hgt / 60)):
            for j in range(3):
                if (i * 3 + j + k) % 4:
                    c.drawRect(skia.Rect.MakeXYWH(x + 20 + j * 50, 1530 - hgt + i * 60, 24, 30), fill(with_alpha(0xFFFFD27A, 0.5)))
    c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, 420), fill(0xFF1A1418))
    draw_text(c, "KNICKERBOCKER", W / 2, 1600, 70, with_alpha(0xFFFF5A7A, 0.85 + 0.15 * math.sin(t * 9)))


def s_houdini2(c, t, P, V):
    sid, lt = seg(P, t)
    if sid == "h":
        c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, 1200), 1200, [0xFF2A160A, 0xFF060302])))
        D.candles(c, t)
        hc.big(c, "10 HALLOWEENS", W / 2, 900, 120, V["accent"], lt, 0.5)
    elif sid == "s1":
        D.stage(c, t)
        D.chains(c, W / 2, 1150, t)
        K.tag(c, W / 2, 1800, "HOUDINI + BESS: UN CÓDIGO", lt - 0.4, accent=V["accent"], size=40)
    elif sid == "s2":
        c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, 1100), 1200, [0xFF2A1A0A, 0xFF060302])))
        ring(c, W / 2, 950, 300, t)
        word = "BELIEVE"
        for i, L in enumerate(word):
            a = clamp((lt - 1.4 - 0.18 * i) / 0.2)
            draw_text(c, L, W / 2 + (i - 3) * 120, 1550, 120, with_alpha(V["accent"], a))
        K.tag(c, W / 2, 1720, "«CREE»", lt - 2.8, accent=WHITE, size=44)
    elif sid == "s3":
        rooftop(c, t)
        D.candles(c, t, n=3, y=1480)
        hc.big(c, "31 OCT 1936", W / 2, 700, 120, V["accent"], lt, 0.3)
        K.tag(c, W / 2, 860, "HOY HACE 90 AÑOS", lt - 1.0, accent=RED, size=44)
    elif sid == "s4":
        rooftop(c, t)
        D.candles(c, t, n=3, y=1480)
        c.drawPaint(fill(0x99000000))
        k = ease_out(clamp(lt / 0.6))
        c.save(); c.translate(W / 2, 1050); c.rotate(-2); c.scale(k, k)
        r = skia.Rect.MakeXYWH(-450, -260, 900, 520)
        c.drawRect(r, fill(0xFFF0E6CC))
        draw_text(c, "«Diez años ya es", 0, -90, 66, 0xFF2A1A0A, shadow=False)
        draw_text(c, "bastante esperar", 0, 0, 66, 0xFF2A1A0A, shadow=False)
        draw_text(c, "a cualquier hombre»", 0, 90, 66, 0xFF2A1A0A, shadow=False)
        draw_text(c, "— Bess Houdini", 120, 200, 44, 0xFF8A2A1A, shadow=False)
        c.restore()
    else:
        c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, 1200), 1200, [0xFF2A160A, 0xFF060302])))
        D.candles(c, t)


V709 = dict(slug="709_houdini_ultima_sesion_p2", accent=0xFFFFB03A, drone=0.04, scene=s_houdini2, badge="HOUDINI · PARTE 2", mood="misterio",
            send="ENVÍASELO A QUIEN LE GUSTE EL MISTERIO", rehook=("s3", "LA ÚLTIMA SESIÓN"), reveal=("s4", "LO QUE PASÓ"), loop=False, segs=[
    dict(id="h", who="nar", say="Durante diez años, cada Halloween, su viuda intentó hablar con Houdini en el más allá.",
         cap="Durante *10 años*, cada | *Halloween*, su viuda intentó | hablar con *Houdini*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Houdini y su mujer, Bess, habían pactado un código secreto. Si había algo después de la muerte, él se lo diría.",
         cap="Él y su mujer, *Bess*, | pactaron un | *código secreto*"),
    dict(id="s2", who="nar", cut=True, say="Empezaba por Rosabelle, la canción que ella cantaba cuando se conocieron, grabada en su anillo. Y escondía una palabra: believe. Cree.",
         cap="Empezaba por «*Rosabelle*», | su canción. Y escondía | una palabra: *BELIEVE*"),
    dict(id="s3", who="nar", cut=True, say="Bess hizo una sesión de espiritismo cada Halloween. La última, hoy hace noventa años: en la azotea del hotel Knickerbocker, en Hollywood.",
         cap="La *última* sesión: | hoy hace *90 años*, en una | azotea de *Hollywood*"),
    dict(id="s4", who="nar", cut=True, say="Houdini no dio ninguna señal. Y Bess dijo: diez años ya es bastante esperar a cualquier hombre.",
         cap="No hubo *ninguna* señal. | «Diez años ya es bastante | esperar a *cualquier hombre*»"),
    dict(id="cta", who="nar", cut=True, say="Pero la tradición sigue: cada Halloween, alguien intenta llamarle. ¿Tú lo intentarías? Comenta sí o no. Y sígueme.",
         cap="Cada Halloween alguien | aún lo *intenta*. ¿Y tú? | Comenta y *SÍGUEME*"),
])


# ====================================================================== 710 T5 P3: Munker (bolas del mismo color)
BEIGE = 0xFFC8B48A


def sphere(c, x, y, r, col=BEIGE):
    sh = skia.GradientShader.MakeRadial((x - r * 0.35, y - r * 0.4), r * 1.4, [0xFFF2E6CA, col, 0xFF5A4A30], [0, 0.45, 1])
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, AntiAlias=True))


def munker(c, t, cx, cy, strip=1.0):
    panel_w, panel_h = 440, 900
    for side, scol in ((-1, 0xFFE8201A), (1, 0xFF1AA8E8)):
        px = cx + side * 240 - panel_w / 2
        c.drawRect(skia.Rect.MakeXYWH(px, cy - panel_h / 2, panel_w, panel_h), fill(0xFF0A0A0A))
        for i in range(3):
            sphere(c, px + panel_w / 2 + math.sin(t * 0.8 + i + side) * 6, cy - 280 + i * 280, 110)
        if strip > 0:
            for k in range(0, int(panel_h / 36)):
                y = cy - panel_h / 2 + k * 36
                c.drawRect(skia.Rect.MakeXYWH(px, y, panel_w, 13), fill(with_alpha(scol, strip)))


def s_munker(c, t, P, V):
    sid, lt = seg(P, t)
    ilu_bg(c, t, 710)
    cx, cy = W / 2, 1200
    if sid == "s2":
        munker(c, t, cx, cy, strip=1 - ease_in_out(clamp((lt - 0.3) / 1.2)))
    elif sid == "s3":
        munker(c, t, cx, cy, strip=ease_in_out(clamp((lt - 0.2) / 1.0)))
    else:
        munker(c, t, cx, cy)
    if sid in ("h", "s1"):
        K.tag(c, W / 2 - 240, cy + 520, "A", lt - 0.2, accent=V["accent"], size=60)
        K.tag(c, W / 2 + 240, cy + 520, "B", lt - 0.2, accent=V["accent"], size=60)
    if sid == "h":
        hc.timer(c, W / 2, 1870, 50, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2" and lt > 1.6:
        hc.stamp(c, "MISMO COLOR", W / 2, 1830, lt, 1.6, 90, col=RED)
    if sid == "s4":
        hc.big(c, "1970", W / 2, 1830, 120, V["accent"], lt, 0.3)


V710 = dict(slug="710_ilusion_munker_t5p3", accent=ILU, drone=0.02, scene=s_munker, badge=SERIE.format(3), mood="misterio",
            send="ENVÍASELO A QUIEN DIGA QUE VE BIEN", rehook=("s2", "QUITO LAS RAYAS"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿De qué color son las bolas de la A? ¿Y las de la B?",
         cap="¿De qué *color* son | las bolas de la *A* | y las de la *B*?", hold=1.4),
    dict(id="s1", who="nar", cut=True, say="Unas parecen naranjas, y las otras azuladas. Elige, y luego mira.",
         cap="Unas parecen *naranjas*… | y otras *azuladas*. Elige", hold=0.5),
    dict(id="s2", who="nar", cut=True, say="Si quito las rayas de colores, todas las bolas son exactamente del mismo color.",
         cap="Sin rayas, todas son | *EXACTAMENTE* | del mismo color", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Vuelvo a ponerlas, y otra vez parecen distintas.", cap="Vuelvo a ponerlas… | y otra vez *te engaña*", hold=0.6),
    dict(id="s4", who="nar", say="Es la ilusión de Munker, de mil novecientos setenta. Tu cerebro mezcla el color de las rayas con el de las bolas.",
         cap="*Ilusión de Munker*, 1970: | tu cerebro *mezcla* | el color de las rayas"),
    dict(id="cta", who="nar", cut=True, say="¿Cuál de las tres te engañó más? Comenta uno, dos o tres. Y sígueme: mañana, más retos para tu cerebro.",
         cap="¿Cuál te engañó más? | Comenta *1, 2 o 3* | y *SÍGUEME*"),
])

VIDEOS = [V701, V702, V703, V704, V705, V706, V707, V708, V709, V710]


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
