"""Producción 02/11/2026 (901–904) — motor v12 paisaje.py (paisajes fractales) + voz v6 kokoroN:em_alex (core.VOICES).
  901 ILUSIÓN EN DIRECTO: foto en negativo -> gris que tu cerebro pinta (John Sadowski, 'Big Spanish Castle', 2006;
      Lines and Colors 12/09/2006, moillusions 13/06/2006: mirar 20-30 s). Paisaje generado por código.
  902 RETO: ¿cuántos cubos FALTAN para el 4x4x4? alturas fijas: faltan 1+5+10+13 = 29 (assert).
  903 MITO CON 'TÚ': 1 año de perro no son 7 (Wang, Ideker et al., UC San Diego, Cell Systems 02/07/2020, 104 labradores,
      edad humana = 16 ln(edad perro) + 31; 8 semanas = bebé de 9 meses; 1 año ~30; 12 años ~70).
  904 SERIE (lo prometido tras Tritón): Miranda, Verona Rupes (NASA APOD 29/11/2020: ~20 km, 10x Gran Cañón, ~12 min de
      caída, ~200 km/h, sobrevivible con airbags; Voyager 2 1986; g=0,079 m/s2 -> t=711 s, v=202 km/h, assert)."""
import math, sys, random, os
import numpy as np
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
import paisaje as Pz
import dia_20261031 as D
import dia_20261101 as D1
from core import glow, W, H, WHITE, INK, clamp, lerp, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, draw_text

OUT = "/home/claude/tiktok/outdaily"
GREEN = 0xFF2FD46B
RED = 0xFFFF3B4A
GOLD = 0xFFFFC23A
seg = D.seg
blur = D.blur
cube = D1.cube
CUBE_BLUE = D1.CUBE_COLS[0]


def rrect(x, y, w, h, r):
    return skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)


# ====================================================================== 901 Postimagen de foto
_col = Pz.sunset(940, 940)
IMG_POS = Pz.to_image(_col)
IMG_NEG = Pz.to_image(Pz.chroma_invert(_col))
IMG_GRAY = Pz.to_image(Pz.gray(_col))
PX, PY, PS = 70, 640, 940  # panel de la foto; el punto no se mueve en todo el vídeo
FX, FY = PX + PS / 2, PY + PS / 2


def photo(c, img, a=1.0):
    p = skia.Paint(AntiAlias=True, Alphaf=a)
    c.save()
    c.clipRRect(rrect(PX, PY, PS, PS, 26), True)
    c.drawImageRect(img, skia.Rect.MakeXYWH(PX, PY, PS, PS), skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore()


def fix_dot(c):
    c.drawCircle(FX, FY, 15, fill(0xFF000000))
    c.drawCircle(FX, FY, 7, fill(0xFFFFFFFF))


def s_foto(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF0A0A0E)
    t0, t1 = P["tl"]["s1"][0], P["tl"]["s3"][0]  # empieza a mirar / cambio a gris
    if sid in ("h", "s1", "s2"):
        photo(c, IMG_NEG)
        fix_dot(c)
        if sid != "h":  # anillo de cuenta atrás abajo, fuera de la foto: lo único que se mueve (no resetea la retina)
            hc.timer(c, W / 2, 1700, 78, clamp((t - t0) / (t1 - t0)), str(max(0, math.ceil(t1 - t))), GOLD)
    elif sid == "s3":
        photo(c, IMG_GRAY)  # corte seco, sin fundido: el efecto está en el contraste
        fix_dot(c)
    elif sid == "s4":
        photo(c, IMG_GRAY)
        K.tag(c, W / 2, 1680, "LA FOTO ES GRIS DE VERDAD", lt - 0.2, accent=GOLD, size=44)
    else:
        z = 1 + 0.03 * math.sin(lt * 1.5)
        c.save(); c.translate(FX, FY); c.scale(z, z); c.translate(-FX, -FY)
        photo(c, IMG_POS)
        c.restore()
        K.tag(c, W / 2, 1610, "ESTO ES LO QUE TÚ HAS PINTADO", lt - 0.1, accent=GOLD, size=40)


V901 = dict(slug="901_foto_que_tu_cerebro_pinta", accent=GOLD, drone=0.0, music=0.03, scene=s_foto, mood="misterio",
            steady=True, clean=True, tease="NO MUEVAS LOS OJOS", send="ENVÍASELO A UN AMIGO",
            rehook=("s2", "NO MUEVAS LOS OJOS"), reveal=("s3", "LA MAGIA"), segs=[
    dict(id="h", who="nar", say="Esta foto se va a volver gris, y tú la vas a ver en color.",
         cap="Tu cerebro va a *PINTAR* esta foto", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Mira el punto del centro, y no muevas los ojos, hasta que acabe la cuenta.",
         cap="Mira el *PUNTO* | y no muevas los ojos", hold=5.0),
    dict(id="s2", who="nar", cut=True, say="Sigue mirando. Ni un milímetro. Ya casi está.",
         cap="Sigue mirando… | *ya casi*", hold=4.5),
    dict(id="s3", who="nar", cut=True, say="¡Ahora! ¿Lo ves? Un cielo azul, y un sol naranja.",
         cap="*¡AHORA!* | ¿Ves los colores?", hold=1.6),
    dict(id="s4", who="nar", cut=True, say="Pero esa foto es gris. Tus ojos se cansan de un color, y tu cerebro pinta el contrario.",
         cap="Tus ojos se *cansan*… | y tu cerebro pinta | el *color contrario*"),
    dict(id="cta", who="nar", cut=True, say="¿La viste en color? Comenta sí o no. Y envíasela a un amigo.",
         cap="¿La viste en color? | Comenta *SÍ* o *NO*"),
])


# ====================================================================== 902 ¿Cuántos cubos faltan?
HM = [[4, 4, 3, 2], [4, 3, 2, 1], [3, 2, 2, 1], [2, 1, 1, 0]]
NB = 4
for i in range(NB):
    for j in range(NB):
        if i < NB - 1:
            assert HM[i][j] >= HM[i + 1][j]  # alturas que bajan hacia la cámara: ninguna columna queda escondida
        if j < NB - 1:
            assert HM[i][j] >= HM[i][j + 1]
BUILT = [(i, j, k) for i in range(NB) for j in range(NB) for k in range(HM[i][j])]
MISS = {k: [(i, j, k) for i in range(NB) for j in range(NB) if HM[i][j] <= k] for k in range(NB)}
assert len(BUILT) == 35 and [len(MISS[k]) for k in range(NB)] == [1, 5, 10, 13] and 64 - len(BUILT) == 29
GOLDC = (0xFFFFD86A, 0xFFE8A824, 0xFFA87410)
LAY = {"s2": 0, "s3": 1, "s4": 2, "s5": 3}
BASE = {"s2": 0, "s3": 1, "s4": 6, "s5": 16}


def ghost_box(c, cx, cy, s, a):
    """Marco del bloque completo 4x4x4: enseña qué hay que rellenar."""
    iso = D1.iso
    q = lambda i, j, k: iso(i, j, k, cx, cy, s)
    col = stroke(with_alpha(WHITE, a), 4)
    for (p, r) in (((0, 0, 4), (4, 0, 4)), ((4, 0, 4), (4, 4, 4)), ((4, 4, 4), (0, 4, 4)), ((0, 4, 4), (0, 0, 4)),
                   ((4, 0, 4), (4, 0, 0)), ((0, 4, 4), (0, 4, 0)), ((4, 4, 4), (4, 4, 0)),
                   ((4, 0, 0), (4, 4, 0)), ((0, 4, 0), (4, 4, 0))):
        c.drawLine(*q(*p), *q(*r), col)


def s_faltan(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A2A4A, 0xFF3A1A4A, seed=902)
    s = 112
    cx, cy = W / 2 + math.sin(t * 0.9) * 10, 1120 + math.sin(t * 1.3) * 10
    solved = []  # huecos ya rellenados, cada uno con su tiempo de llegada
    for sg_id, k in LAY.items():
        a, b = P["tl"][sg_id]
        cubes = MISS[k]
        dur = max(0.8, (b - a) - 0.5)
        for n, q in enumerate(cubes):
            solved.append((q, a + n * dur / len(cubes)))
    items = [(q, None) for q in BUILT] + solved
    items.sort(key=lambda it: (it[0][2], it[0][0] + it[0][1]))
    glowing = 0
    for q, ta in items:
        if ta is None:
            cube(c, *q, cx, cy, s, CUBE_BLUE)
        elif t >= ta:
            drop = (1 - ease_out(clamp((t - ta) / 0.28))) * 500
            cube(c, *q, cx, cy, s, GOLDC, lift=drop)
            glowing += 1
    if sid in ("h", "s1"):
        ghost_box(c, cx, cy, s, 0.55 + 0.25 * math.sin(t * 4))
    if sid == "h":
        hc.timer(c, W / 2, 1810, 64, clamp(lt / max(0.1, P["tl"]["h"][1])), str(max(0, 5 - int(t))), GOLD)
    elif sid == "s1":
        K.tag(c, W / 2, 1810, "COMENTA TU NÚMERO ANTES DE SEGUIR", lt - 0.2, accent=GOLD, size=40)
    elif sid in LAY:
        hc.big(c, str(glowing), W / 2, 1830, 130, GOLD, 1.0, 0.0)
    else:
        hc.stamp(c, "29", W / 2, 1790, lt, 0.1, 140, col=GREEN)


V902 = dict(slug="902_cuantos_cubos_faltan_29", accent=GOLD, drone=0.02, scene=s_faltan, mood="misterio",
            tease="TIENES 5 SEGUNDOS", send="RETA A UN AMIGO: ENVÍASELO", rehook=("s4", "AHORA VIENE LO DIFÍCIL"),
            reveal=("cta", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="¿Cuántos cubos faltan, para completar el bloque? Cinco segundos.",
         cap="¿Cuántos cubos *FALTAN*?", hold=2.6),
    dict(id="s1", who="nar", cut=True, say="El bloque es de cuatro por cuatro por cuatro. Escribe tu número, antes de seguir.",
         cap="Bloque de *4 × 4 × 4*. | Escribe tu *número*", hold=0.8),
    dict(id="s2", who="q", cut=True, say="Vamos a rellenarlo. Abajo, solo falta uno.", cap="Abajo: falta *UNO*", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="En el segundo piso, cinco.", cap="Segundo piso: *CINCO*", hold=0.8),
    dict(id="s4", who="nar", cut=True, say="En el tercero, diez.", cap="Tercero: *DIEZ*", hold=1.0),
    dict(id="s5", who="nar", cut=True, say="Y arriba, trece.", cap="Arriba: *TRECE*", hold=1.0),
    dict(id="cta", who="nar", cut=True, say="Faltaban veintinueve. ¿Cuántos dijiste tú? Comenta, y reta a un amigo.",
         cap="Faltaban *29*. ¿Y tú? | *COMENTA* | y reta a un amigo"),
])


# ====================================================================== 903 Mito: 1 año de perro no son 7
def human(a):
    return 16 * math.log(a) + 31


assert round(human(1)) == 31 and round(human(12)) == 71 and round(human(4)) == 53
AX0, AX1, AY0, AY1 = 150, 960, 1520, 720  # ejes del gráfico: 0-16 años de perro, 0-110 humanos


def gx(a): return lerp(AX0, AX1, a / 16)
def gy(h): return lerp(AY0, AY1, h / 110)


def chart(c, t, upto, seven=1.0, curve=1.0, accent=GOLD):
    c.drawRRect(rrect(70, 660, 940, 960, 30), fill(with_alpha(0xFF0C1020, 0.82)))
    c.drawLine(AX0, AY0, AX1, AY0, stroke(WHITE, 5))
    c.drawLine(AX0, AY0, AX0, AY1, stroke(WHITE, 5))
    for a in (4, 8, 12, 16):
        draw_text(c, str(a), gx(a), AY0 + 50, 36, WHITE, shadow=False)
    for h in (25, 50, 75, 100):
        c.drawLine(AX0, gy(h), AX1, gy(h), stroke(with_alpha(WHITE, 0.14), 3))
        draw_text(c, str(h), AX0 - 48, gy(h) + 13, 34, WHITE, shadow=False)
    draw_text(c, "AÑOS DE TU PERRO", (AX0 + AX1) / 2, AY0 + 92, 30, with_alpha(WHITE, 0.8), shadow=False)
    if seven > 0:  # la regla de siempre, en rojo discontinuo
        p = skia.Path()
        p.moveTo(gx(0), gy(0))
        end = min(16 * seven, 110 / 7)
        p.lineTo(gx(end), gy(7 * end))
        pp = stroke(RED, 7)
        pp.setPathEffect(skia.DashPathEffect.Make([22, 16], 0))
        c.drawPath(p, pp)
        if seven >= 1:
            draw_text(c, "× 7", gx(13.2), gy(100), 56, RED)
    if upto > 0.05:
        p = skia.Path()
        n = 90
        a0 = 0.15
        for i in range(n + 1):
            a = lerp(a0, max(a0, upto), i / n)
            x, y = gx(a), gy(max(0, human(a)))
            p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
        c.drawPath(p, stroke(accent, 12))
        x, y = gx(upto), gy(max(0, human(upto)))
        glow(c, x, y, 70, accent, 0.5)
        c.drawCircle(x, y, 16, fill(WHITE))


TABLE = [(1, 31), (2, 42), (3, 49), (4, 53), (6, 60), (8, 64), (10, 68), (12, 71), (14, 73)]
for a_, h_ in TABLE:
    assert round(human(a_)) == h_


# v12: silueta de labrador a contraluz sobre un atardecer fractal (el perro de espaldas parecía una patata)
BG_DOG = Pz.to_image(Pz.sunset(1080, 1920, seed=903))


def smooth_path(pts, close=True):
    """Catmull-Rom cerrada: una curva suave que pasa por todos los puntos."""
    p = skia.Path()
    n = len(pts)
    p.moveTo(*pts[0])
    for i in range(n if close else n - 1):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        p.cubicTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                  p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    if close:
        p.close()
    return p


DOG_PTS = [(-205, 0), (-250, -70), (-235, -170), (-170, -290), (-85, -390), (-10, -470), (30, -555), (85, -610), (150, -605),
           (205, -570), (275, -545), (305, -515), (285, -480), (205, -465), (140, -450), (115, -395), (120, -300),
           (112, -170), (108, -50), (160, -22), (160, 0), (45, 0), (40, -60), (30, -150), (-30, -130), (-55, -70), (40, -28), (55, 0)]
EAR_PTS = [(55, -575), (110, -560), (118, -490), (92, -420), (55, -425), (35, -500)]


def labrador(c, x, y, s, t, wag=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    # sombra en el suelo
    c.drawOval(skia.Rect.MakeXYWH(-330, -14, 620, 44), skia.Paint(AntiAlias=True, Color=0x88000000, MaskFilter=blur(14)))
    # cola: se mueve de verdad
    a = math.sin(t * 9) * 0.55 * wag
    tail = [(-215, -35), (-300 - 40 * a, -70 - 90 * a), (-395 - 40 * a, -130 - 160 * a)]
    pt = skia.Path(); pt.moveTo(*tail[0]); pt.quadTo(*tail[1], *tail[2])
    c.drawPath(pt, stroke(0xFF08070C, 44))
    body = smooth_path(DOG_PTS)
    c.drawPath(body, fill(0xFF08070C))
    # luz de contorno cálida del atardecer (solo por delante): separa la silueta del fondo
    c.save(); c.clipPath(body, True)
    rim = stroke(0xFFFFB05A, 11)
    rim.setMaskFilter(blur(5))
    c.translate(-7, 7)
    c.drawPath(body, rim)
    c.restore()
    c.save(); c.translate(115, -570); c.rotate(math.sin(t * 2.2) * 3); c.translate(-115, 570)
    c.drawPath(smooth_path(EAR_PTS), fill(0xFF17121A))
    c.restore()
    c.drawCircle(178, -560, 8, fill(0xFFFFE2B8))  # brillo del ojo
    c.drawCircle(292, -520, 13, fill(0xFF000000))
    c.restore()


def s_perro(c, t, P, V):
    sid, lt = seg(P, t)
    z = 1.06 + 0.012 * t  # lento zoom de fondo: nunca está quieto
    c.save(); c.translate(W / 2, H * 0.62); c.scale(z, z); c.translate(-W / 2, -H * 0.62)
    c.drawImage(BG_DOG, 0, 0)
    c.restore()
    c.drawPaint(fill(0x33000010))
    if sid == "h":
        labrador(c, W / 2 + 10, 1690, 1.32, t)
        a = ease_out(clamp(lt / 0.2))
        z = 1 + 0.03 * math.sin(t * 5)
        c.save(); c.translate(W / 2, 720); c.scale(z, z)
        draw_text(c, "1 AÑO = 7", 0, 40, 112, with_alpha(WHITE, a), outline=14)
        c.restore()
        k = clamp((lt - 0.9) / 0.25)
        if k > 0:
            c.drawLine(W / 2 - 320, 750, lerp(W / 2 - 320, W / 2 + 320, k), lerp(750, 700, k), stroke(RED, 22))
        if lt > 1.3:
            hc.stamp(c, "MENTIRA", W / 2, 1810, lt, 1.3, 90, col=RED)
    elif sid == "s1":
        labrador(c, W / 2 + 10, 1680, 1.15, t, wag=0.7)
        hc.big(c, "2020", W / 2 - 250, 800, 120, V["accent"], lt, 0.2)
        hc.big(c, "104", W / 2 + 250, 800, 120, V["accent"], lt, 0.5)
        K.tag(c, W / 2 + 250, 900, "LABRADORES", lt - 0.6, accent=WHITE, size=34)
        K.tag(c, W / 2, 1810, "UNIVERSIDAD DE CALIFORNIA · SAN DIEGO", lt - 0.8, accent=V["accent"], size=34)
    elif sid == "s2":
        a = lerp(0.15, 8 / 52, ease_out(clamp(lt / 1.0)))
        chart(c, t, a, seven=clamp(lt / 0.8), curve=1)
        hc.big(c, "8 SEMANAS", W / 2, 1720, 76, WHITE, lt, 0.3)
        K.tag(c, W / 2, 1810, "= BEBÉ DE 9 MESES", lt - 0.6, accent=V["accent"], size=46)
    elif sid == "s3":
        a = lerp(8 / 52, 1, ease_in_out(clamp(lt / 1.6)))
        chart(c, t, a)
        hc.big(c, f"{round(max(1, human(a)))}", W / 2, 1810, 150, V["accent"], 1.0, 0.0)
    elif sid == "s4":
        a = lerp(1, 12, ease_in_out(clamp(lt / 2.6)))
        chart(c, t, a)
        hc.big(c, f"{round(human(a))}", W / 2, 1810, 150, V["accent"], 1.0, 0.0)
    elif sid in ("s5", "cta"):
        c.drawRRect(rrect(120, 650, 840, 1000, 30), fill(with_alpha(0xFF0C1020, 0.88)))
        draw_text(c, "TU PERRO", 340, 730, 42, V["accent"])
        draw_text(c, "EN HUMANO", 740, 730, 42, V["accent"])
        tt = t - P["tl"]["s5"][0]
        for i, (a_, h_) in enumerate(TABLE):
            k = ease_out(clamp((tt - i * 0.12) / 0.3))
            y = 820 + i * 88
            draw_text(c, f"{a_} {'año' if a_ == 1 else 'años'}", 340 - (1 - k) * 60, y, 52, with_alpha(WHITE, k))
            draw_text(c, str(h_), 740 + (1 - k) * 60, y, 60, with_alpha(V["accent"], k))
        draw_text(c, "Estudio en labradores · Cell Systems 2020", W / 2, 1625, 28, with_alpha(WHITE, 0.75), shadow=False)
    # patitas que cruzan abajo: movimiento constante
    for i in range(6):
        x = (t * 90 + i * 210) % (W + 200) - 100
        y = 1890 - (i % 2) * 18
        c.drawCircle(x, y, 13, fill(with_alpha(WHITE, 0.10)))


V903 = dict(slug="903_mito_anos_de_perro", accent=GOLD, drone=0.02, scene=s_perro, mood="luz",
            send="ENVÍASELO A ALGUIEN CON PERRO",
            rehook=("s3", "Y AQUÍ VIENE LO RARO"), reveal=("s5", "LA EDAD DE TU PERRO"), segs=[
    dict(id="h", who="nar", say="Te enseñaron mal. Un año de tu perro, no son siete años.",
         cap="Te lo *enseñaron mal*", hold=0.8),
    dict(id="s1", who="nar", cut=True, say="En dos mil veinte, en la Universidad de California, miraron el ADN de ciento cuatro labradores.",
         cap="Miraron el *ADN* | de *104 labradores*"),
    dict(id="s2", who="nar", cut=True, say="Con ocho semanas, tu perro es como un bebé de nueve meses.",
         cap="*8 semanas*: | como un bebé", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="Pero con un año, ya es como alguien de treinta.",
         cap="¡Con *1 año*, | ya tiene unos *30*!", hold=0.8),
    dict(id="s4", who="nar", cut=True, say="Luego frena. Con doce años, tiene unos setenta.",
         cap="Luego *frena*: | con 12, unos *70*", hold=0.6),
    dict(id="s5", who="nar", cut=True, say="Busca aquí al tuyo.", cap="Busca al *TUYO* | y guárdalo", hold=3.4),
    dict(id="cta", who="nar", cut=True, say="¿Cuántos años tiene? Comenta, y envíaselo a alguien con perro.",
         cap="¿Cuántos tiene el tuyo? | *COMENTA*"),
])


# ====================================================================== 904 Miranda: el acantilado de 12 minutos
G_MIR, HEIGHT = 0.079, 20000.0
FALL_T = math.sqrt(2 * HEIGHT / G_MIR)
FALL_V = G_MIR * FALL_T * 3.6
assert 690 < FALL_T < 730 and 195 < FALL_V < 210  # coincide con APOD: ~12 min, ~200 km/h
ST = K.Stars(seed=904)
_mir = S.TEX + "miranda_proc.png"
if not os.path.exists(_mir):
    Pz.miranda_texture(_mir)
MIR = S.load("miranda_proc.png")
URA = S.load("uranusmap.jpg")
WALL = Pz.cliff_wall(760, 2400)
IMG_WALL = Pz.to_image(WALL)
_rng = np.random.default_rng(4)
_edge = Pz.ridge(2400, 44, base=9, octaves=7)  # borde irregular de la pared, en píxeles
L0 = (-0.55, 0.35, 0.76)


def uranus(c, x, y, R, t):
    S.draw_planet(c, x, y, R, S.render(int(2 * R), URA, spin=t * 0.04, tilt=1.3, light=L0, gain=1.2, limb=0.55, ambient=0.05))
    S.atmosphere(c, x, y, R, color=0xFF8AE4F0, strength=0.8)


def miranda(c, x, y, R, t):
    S.draw_planet(c, x, y, R, S.render(int(2 * R), MIR, spin=t * 0.09, tilt=0.15, light=L0, gain=1.2, limb=0.5, ambient=0.06))


def wall(c, scroll, xw=640, zoom=1.0):
    """Pared en el lado izquierdo con el borde recortado, que sube al caer (scroll en píxeles)."""
    path = skia.Path()
    path.moveTo(-10, -10)
    off = int(scroll) % 2400
    pts = 48
    for i in range(pts + 1):
        y = i * H / pts
        e = _edge[(off + int(y)) % 2400]
        path.lineTo(xw + (e - 0.5) * 150, y)
    path.lineTo(-10, H + 10)
    path.close()
    c.save()
    c.clipPath(path, True)
    y0 = -(scroll % 2400)
    for yy in (y0, y0 + 2400):
        c.drawImageRect(IMG_WALL, skia.Rect.MakeXYWH(0, yy, 900, 2400), skia.SamplingOptions(skia.FilterMode.kLinear))
    # luz rasante desde el borde
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (xw, 0)], [0x99000000, 0x00000000])))
    c.restore()


def rock(c, x, y, r, t):
    glow(c, x, y, r * 3, 0xFFBFD8FF, 0.22)
    c.save(); c.translate(x, y); c.rotate(math.degrees(t * 2.2))
    p = skia.Path()
    R = random.Random(9)
    n = 10
    for i in range(n):
        a = i / n * 6.283
        rr = r * R.uniform(0.72, 1.08)
        p.moveTo(math.cos(a) * rr, math.sin(a) * rr) if i == 0 else p.lineTo(math.cos(a) * rr, math.sin(a) * rr)
    p.close()
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-r, -r), (r, r)], [0xFFD4DAE4, 0xFF4A5060])))
    c.restore()


def streaks(c, t, k):
    R = random.Random(int(t * 24))
    for i in range(int(16 * k)):
        x = R.uniform(640, W)
        y = R.uniform(0, H)
        L = R.uniform(60, 180) * k
        c.drawLine(x, y, x, y - L, stroke(with_alpha(WHITE, 0.16), 3))


def hud(c, lt_frac, accent):
    """Instrumentos de caída acelerados: tiempo, altura y velocidad reales de la física de Miranda."""
    tf = lt_frac * FALL_T
    h = max(0, HEIGHT - 0.5 * G_MIR * tf * tf)
    v = G_MIR * tf * 3.6
    mm, ss = int(tf // 60), int(tf % 60)
    c.drawRRect(rrect(590, 1370, 450, 340, 28), fill(with_alpha(0xFF0A0E1C, 0.85)))
    draw_text(c, f"{mm:02d}:{ss:02d}", 815, 1475, 100, accent, shadow=False)
    draw_text(c, f"{h / 1000:.1f} km", 815, 1570, 56, WHITE, shadow=False)
    draw_text(c, f"{v:.0f} km/h", 815, 1650, 56, WHITE, shadow=False)


def s_miranda(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF02030A)
    ST.draw(c, t, camx=t * 6, alpha=0.9)
    if sid == "h":
        uranus(c, 850, 620, 210, t)
        # la cámara se asoma: la pared empieza a subir
        wall(c, 90 * t + 30 * t * t)
        rock(c, 770, 900 + 170 * t * t * 0.35, 44, t)
        hc.stamp(c, "20 KM", 815, 1650, lt, 0.8, 120, col=RED)
    elif sid == "s1":
        R = lerp(300, 370, ease_out(clamp(lt / 2)))
        uranus(c, 860, 780, 150, t)
        miranda(c, W / 2 - 40, 1200, R, t)
        K.tag(c, W / 2, 1720, "MIRANDA · LUNA DE URANO", lt - 0.2, accent=V["accent"], size=44)
    elif sid == "s2":
        # comparación de escala real: 20 km, Everest 8,8 km, Gran Cañón ~2 km (APOD: 10 veces el Gran Cañón)
        bars = [("GRAN CAÑÓN", 2.0, 0xFF8AB4FF), ("EVEREST", 8.8, WHITE), ("VERONA RUPES", 20.0, V["accent"])]
        base = 1640
        for i, (n, km, col) in enumerate(bars):
            k = ease_out(clamp((lt - 0.2 - i * 0.45) / 0.7))
            hh = km / 20.0 * 900 * k
            x = 210 + i * 330
            r = skia.Rect.MakeXYWH(x - 95, base - hh, 190, hh)
            c.drawRRect(skia.RRect.MakeRectXY(r, 14, 14), fill(with_alpha(col, 0.92)))
            if k > 0.2:
                draw_text(c, f"{km:g} km".replace(".", ","), x, base - hh - 22, 50, col)
                draw_text(c, n, x, base + 54, 30, WHITE, shadow=False)
    elif sid == "s3":
        k = clamp(lt / max(0.1, P["tl"]["s3"][1] - P["tl"]["s3"][0]))
        uranus(c, 860, 500, 120 * (1 - k * 0.25), t)
        wall(c, 70 * t + 480 * lt)
        streaks(c, t, 0.4 + k)
        rock(c, 800, 980 + math.sin(t * 7) * 6, 46, t)
        hud(c, k * 0.55, V["accent"])
    elif sid == "s4":
        k = clamp(lt / max(0.1, P["tl"]["s4"][1] - P["tl"]["s4"][0]))
        wall(c, 70 * t + 900 * (lt + 4))
        streaks(c, t, 1.2)
        # el suelo sube
        gy_ = lerp(H + 120, 1420, ease_in_out(clamp((k - 0.45) / 0.3)))
        c.drawRect(skia.Rect.MakeXYWH(0, gy_, W, H - gy_ + 20), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, gy_), (0, H)], [0xFFA8B4C6, 0xFF4E5868])))
        rocky = lerp(1000, gy_ - 150, ease_in_out(clamp((k - 0.45) / 0.3)))
        if k < 0.72:
            rock(c, 800, rocky, 46, t)
        else:  # airbag que rebota
            kk = (k - 0.72) / 0.28
            ry = gy_ - 160 - abs(math.sin(kk * 6.28)) * 260 * (1 - kk * 0.6)
            sq = 1 + 0.08 * math.sin(kk * 25)
            c.save(); c.translate(800, ry); c.scale(sq, 2 - sq)
            c.drawCircle(0, 0, 130, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((-40, -50), 170, [0xFFFFE28A, 0xFFE89A20])))
            c.drawCircle(0, 0, 130, stroke(0xFF8A5A10, 6))
            c.restore()
            K.tag(c, 720, 1240, "AIRBAGS", (kk * 2), accent=V["accent"], size=44)
        hud(c, 0.55 + 0.45 * min(1, k / 0.6), V["accent"])
    elif sid == "s5":
        # Voyager 2 sobrevuela: una sola nave, una sola visita
        uranus(c, W / 2 + 180, 760, 220, t)
        miranda(c, W / 2 - 200, 1230, 190, t)
        x = lerp(-80, W + 60, clamp(lt / 3.2))
        y = lerp(1420, 480, clamp(lt / 3.2))
        c.save(); c.translate(x, y); c.rotate(-28)
        c.drawRect(skia.Rect.MakeXYWH(-30, -20, 60, 40), fill(0xFFC8CCD4))
        c.drawLine(0, -20, 0, -46, stroke(0xFF9098A4, 8))
        c.drawOval(skia.Rect.MakeXYWH(-62, -80, 124, 44), fill(0xFFF2F4F8))
        c.drawOval(skia.Rect.MakeXYWH(-62, -80, 124, 44), stroke(0xFF8C94A0, 4))
        c.drawLine(30, 0, 170, 8, stroke(0xFFAAB0BC, 5))
        c.drawLine(-30, 6, -120, 60, stroke(0xFFAAB0BC, 5))
        c.restore()
        hc.big(c, "1986", W / 2, 1650, 140, V["accent"], lt, 0.3)
        K.tag(c, W / 2, 1770, "VOYAGER 2 · LA ÚNICA VISITA", lt - 0.6, accent=WHITE, size=38)
    else:
        uranus(c, 840, 720, 190, t)
        wall(c, 60 * t)
        rock(c, 790, 1120 + math.sin(t * 2.2) * 26, 46, t)


V904 = dict(slug="904_miranda_acantilado_12_minutos", accent=0xFF8AE4F0, drone=0.03, scene=s_miranda, mood="epico",
            tease="LO PROMETIDO", send="ENVÍASELO A QUIEN SALTARÍA", rehook=("s3", "ESPERA, QUE SIGUES CAYENDO"),
            reveal=("s3", "EL TIEMPO"), segs=[
    dict(id="h", who="nar", say="Saltas desde este acantilado. ¿Cuánto tardas en llegar abajo?",
         cap="¿*CUÁNTO TARDAS* en caer desde aquí?", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Está en Miranda, una luna de Urano.",
         cap="Está en *Miranda*, | una luna de Urano", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Se llama Verona Rupes, y mide unos veinte kilómetros. Diez veces el Gran Cañón.",
         cap="*Verona Rupes*: | unos *20 km*. | ¡10 Grandes Cañones!", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Como allí casi no hay gravedad, tardarías unos doce minutos en caer. Doce.",
         cap="Casi sin gravedad: | ¡*12 MINUTOS* cayendo!", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Llegarías a unos doscientos por hora. La NASA dice que, con airbags, quizá sobrevivirías.",
         cap="Llegas a *200 km/h*. | Con *airbags*, | quizá sobrevives", hold=0.5),
    dict(id="s5", who="nar", cut=True, say="Solo una nave lo ha visto de cerca: la Voyager 2, en mil novecientos ochenta y seis.",
         cap="Solo la ha visto | la *Voyager 2*, en *1986*"),
    dict(id="cta", who="nar", cut=True, say="¿Saltarías? Comenta sí o no. Y sígueme: la próxima luna casi se parte en dos.",
         cap="¿Saltarías? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])

VIDEOS = [V901, V902, V903, V904]


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
