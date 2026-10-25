"""2 historias en 3 partes: Violet Jessop (la mujer insumergible) y Apolo 13.

uso: python3 historias.py <índices|all> [prev]
"""
import math, random, sys
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, pill, glow

OUT = "/home/claude/tiktok/out60"
VIDEOS = []


def part_badge(c, txt, accent):
    pill(c, W / 2, 292, txt, 30, bg=accent, fg=INK)


def year_card(c, year, lt, accent, y=1500):
    hc.big(c, year, W / 2, y, 150, accent, lt, 0.2)


def cliff(c, t, lt, accent, txt="CONTINUARÁ…"):
    hc.big(c, txt, W / 2, 1520, 90, accent, lt, 0.4)


# ================================================================== barcos
def sea(c, t, horizon=1250, night=True, cam=0.0):
    top = 0xFF050A1C if night else 0xFF6A8AB0
    mid = 0xFF101A3A if night else 0xFFB8C8D8
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, horizon), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, 0), (0, horizon)], [top, mid])))
    if night:
        rnd = random.Random(3)
        p = skia.Paint(AntiAlias=True)
        for _ in range(160):
            x, y = rnd.uniform(0, W), rnd.uniform(0, horizon - 80)
            p.setColor(with_alpha(WHITE, rnd.uniform(0.2, 0.9) * (0.7 + 0.3 * math.sin(t * 2 + x))))
            c.drawCircle(x, y, rnd.uniform(1, 2.6), p)
    c.drawRect(skia.Rect.MakeLTRB(0, horizon, W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, horizon), (0, H)], [0xFF0A1A30 if night else 0xFF2A4A6A, 0xFF02060E if night else 0xFF0E2236])))
    for k in range(14):
        y = horizon + 12 + k * k * 4
        off = (t * (20 + k * 4) + cam * (1 + k * 0.2)) % 120
        pth = skia.Path()
        pth.moveTo(-120 + off, y)
        for x in range(-120, W + 120, 60):
            pth.lineTo(x + off, y + math.sin(x / 50 + t * 2 + k) * (2 + k * 0.4))
        c.drawPath(pth, stroke(with_alpha(0xFF7FA8D8, 0.12 + 0.01 * k), 2 + k * 0.15))


def liner(c, x, y, s, t, lights=True, tilt=0.0, sink=0.0, name=None):
    """Transatlántico de 4 chimeneas (clase Olympic), vista lateral. (x, y) = línea de flotación al centro."""
    c.save()
    c.translate(x, y + sink * 300 * s)
    c.rotate(tilt)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(-2000, -2000, 2000, 0 + 2 * s - sink * 300 * s * 0))
    L = 900 * s
    hull = skia.Path()
    hull.moveTo(-L / 2, -60 * s)
    hull.lineTo(L / 2 + 20 * s, -70 * s)
    hull.lineTo(L / 2 - 10 * s, 30 * s)
    hull.lineTo(-L / 2 + 30 * s, 30 * s)
    hull.close()
    c.drawPath(hull, fill(0xFF14161C))
    c.drawRect(skia.Rect.MakeLTRB(-L / 2 + 30 * s, 8 * s, L / 2 - 10 * s, 30 * s), fill(0xFF8A2A22))
    # superestructura
    c.drawRect(skia.Rect.MakeLTRB(-L * 0.38, -110 * s, L * 0.36, -60 * s), fill(0xFFE8E4DA))
    c.drawRect(skia.Rect.MakeLTRB(-L * 0.3, -135 * s, L * 0.28, -110 * s), fill(0xFFDCD8CC))
    # chimeneas
    for k in range(4):
        fx = -L * 0.24 + k * L * 0.15
        fun = skia.Path()
        fun.moveTo(fx - 22 * s, -135 * s); fun.lineTo(fx + 22 * s, -135 * s)
        fun.lineTo(fx + 30 * s, -250 * s); fun.lineTo(fx - 14 * s, -250 * s); fun.close()
        c.drawPath(fun, fill(0xFFD8A44A))
        c.drawRect(skia.Rect.MakeLTRB(fx - 15 * s, -250 * s, fx + 30 * s, -228 * s), fill(0xFF14161C))
        if k < 3 and lights:
            for j in range(3):
                ph = (t * 0.6 + j * 0.33 + k * 0.2) % 1
                c.drawCircle(fx + 10 * s + ph * 40 * s, -260 * s - ph * 90 * s, (10 + ph * 26) * s,
                             fill(with_alpha(0xFF8A8A92, 0.35 * (1 - ph))))
    # mástiles
    c.drawLine(-L * 0.42, -60 * s, -L * 0.42, -300 * s, stroke(0xFF2A2C34, 4 * s))
    c.drawLine(L * 0.4, -60 * s, L * 0.4, -290 * s, stroke(0xFF2A2C34, 4 * s))
    c.drawLine(-L * 0.42, -300 * s, L * 0.4, -290 * s, stroke(with_alpha(0xFF2A2C34, 0.6), 1.5 * s))
    # ojos de buey
    if lights:
        for row, yy in enumerate((-40 * s, -88 * s, -122 * s)):
            for k in range(28 - row * 6):
                px = -L * 0.42 + row * 40 * s + k * L * 0.03
                fl = 0.75 + 0.25 * math.sin(t * 3 + k * 1.7 + row)
                c.drawCircle(px, yy, 3.5 * s, fill(with_alpha(0xFFFFE6A0, fl)))
    c.restore()
    c.restore()
    if name:
        pill(c, x, y + 90 * s, name, 34, bg=WHITE, fg=INK)


def warship(c, x, y, s):
    p = skia.Path()
    p.moveTo(-300 * s, -30 * s); p.lineTo(260 * s, -30 * s); p.lineTo(320 * s, 10 * s)
    p.lineTo(300 * s, 30 * s); p.lineTo(-290 * s, 30 * s); p.close()
    c.save(); c.translate(x, y)
    c.drawPath(p, fill(0xFF4A5058))
    c.drawRect(skia.Rect.MakeLTRB(-150 * s, -80 * s, 120 * s, -30 * s), fill(0xFF5A6068))
    for k in range(2):
        c.drawRect(skia.Rect.MakeXYWH(-80 * s + k * 90 * s, -150 * s, 34 * s, 70 * s), fill(0xFF3A4048))
    c.drawLine(-20 * s, -80 * s, -20 * s, -220 * s, stroke(0xFF3A4048, 5 * s))
    c.restore()


def iceberg(c, x, y, s, t):
    p = skia.Path()
    pts = [(-260, 0), (-200, -160), (-120, -230), (-40, -330), (40, -260), (130, -300), (210, -150), (270, 0)]
    p.moveTo(x + pts[0][0] * s, y + pts[0][1] * s)
    for (a, b) in pts[1:]:
        p.lineTo(x + a * s, y + b * s)
    p.close()
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeLinear([(x - 260 * s, y - 330 * s), (x + 270 * s, y)],
                                                                   [0xFFF2FAFF, 0xFFA8C8E0, 0xFF5A7A9A]), AntiAlias=True))
    sub = skia.Path()
    sub.moveTo(x - 260 * s, y); sub.lineTo(x + 270 * s, y); sub.lineTo(x + 380 * s, y + 260 * s)
    sub.lineTo(x - 330 * s, y + 240 * s); sub.close()
    c.drawPath(sub, fill(with_alpha(0xFF6A9AC8, 0.25)))


def lifeboat(c, x, y, s, t, people=6):
    bob = math.sin(t * 1.8) * 6 * s
    p = skia.Path()
    p.moveTo(-120 * s, -20 * s); p.lineTo(120 * s, -20 * s); p.lineTo(90 * s, 25 * s); p.lineTo(-90 * s, 25 * s); p.close()
    c.save(); c.translate(x, y + bob)
    c.drawPath(p, fill(0xFFE8E4DA))
    c.drawLine(-115 * s, -20 * s, 115 * s, -20 * s, stroke(0xFF8A6A3A, 5 * s))
    for k in range(people):
        px = -90 * s + k * 36 * s
        c.drawCircle(px, -42 * s, 11 * s, fill(0xFF2A2C34))
        c.drawRoundRect(skia.Rect.MakeXYWH(px - 11 * s, -34 * s, 22 * s, 16 * s), 6 * s, 6 * s, fill(0xFF2A2C34))
    c.restore()


def propeller(c, x, y, r, t):
    c.save(); c.translate(x, y); c.rotate(t * 300)
    for k in range(3):
        c.rotate(120)
        c.drawOval(skia.Rect.MakeXYWH(-r * 0.22, -r, r * 0.44, r), fill(0xFF8A6A3A))
    c.restore()
    c.drawCircle(x, y, r * 0.2, fill(0xFF6A4A2A))


def sepia(c, a=0.25):
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=with_alpha(0xFF6A4A20, a), BlendMode=skia.BlendMode.kOverlay))


def ships_tally(c, t, lt, done, accent):
    names = ["OLYMPIC · 1911", "TITANIC · 1912", "BRITANNIC · 1916"]
    for i, n in enumerate(names):
        s = ease_back(prog(lt, 0.3 + i * 0.35, 0.6 + i * 0.35), 2.0)
        if s <= 0:
            continue
        y = 1000 + i * 150
        c.save(); c.translate(W / 2, y); c.scale(s, s)
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-330, -55, 660, 110), 30, 30)
        c.drawRRect(r, fill(with_alpha(0xFF101426, 0.85)))
        c.drawRRect(r, stroke(accent if i < done else with_alpha(WHITE, 0.3), 5))
        c.drawString(n, -290, 18, hc.font(48), fill(WHITE))
        if i < done:
            c.drawCircle(270, 0, 34, fill(0xFF2FD46B))
            pth = skia.Path(); pth.moveTo(255, 0); pth.lineTo(266, 12); pth.lineTo(286, -12)
            c.drawPath(pth, stroke(WHITE, 8))
        else:
            hc.draw_text(c, "?", 270, 22, 60, accent, shadow=False)
        c.restore()


hc.font = K.font
hc.draw_text = K.draw_text

# ------------------------------------------------------------------ Violet · parte 1 (Olympic)
def s_v1(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    acc = V["accent"]
    if sid == "h":
        hc.aurora(c, t, acc, 0xFF3C6AFF, 31)
        ships_tally(c, t, t + 0.4, 3, acc)
    elif sid in ("s1",):
        sea(c, t, night=False)
        liner(c, W / 2 + 40 - lt * 15, 1280, 1.0, t, lights=False)
        hc.big(c, "VIOLET JESSOP", W / 2, 820, 96, WHITE, lt, 0.3)
        K.tag(c, W / 2, 940, "CAMARERA DE BARCOS DE LUJO", lt - 0.8, accent=acc, size=34)
    elif sid == "s2":
        sea(c, t, night=False)
        liner(c, W / 2 + 120 - lt * 25, 1280, 1.05, t, lights=False, name="RMS OLYMPIC")
        year_card(c, "1911", lt, acc, y=820)
    elif sid in ("s3", "s4"):
        sea(c, t, night=False)
        hit = ease_in_out(prog(t - P["tl"]["s3"][0], 0.3, 2.2))
        liner(c, W / 2 + 140, 1280, 0.95, t, lights=False)
        warship(c, lerp(-300, 330, hit), 1300, 0.8)
        if hit >= 1:
            glow(c, 330 + 240, 1270, 220, 0xFFFFB050, 0.7 * math.exp(-(t - P["tl"]["s3"][0] - 2.2) * 2) + 0.1)
            if sid == "s3":
                hc.stamp(c, "¡CHOQUE!", W / 2, 820, t - P["tl"]["s3"][0], 2.2, 110)
        if sid == "s4":
            K.tag(c, W / 2, 820, "0 MUERTOS · VUELVE A PUERTO", lt - 0.4, accent=acc, size=40)
            ships_tally(c, t, 10, 1, acc) if False else None
    elif sid == "s5":
        sea(c, t, night=True)
        a = ease_in_out(prog(lt, 0.2, 2.0))
        liner(c, lerp(W + 500, W / 2, a), 1280, 1.0, t, lights=True, name="TITANIC" if a > 0.9 else None)
        sepia(c, 0.15)
    else:
        sea(c, t, night=True)
        liner(c, W / 2, 1280, 1.0, t, lights=True)
        cliff(c, t, lt, acc, "PARTE 2 →")
    part_badge(c, "HISTORIA · PARTE 1/3", acc)


VIDEOS.append(dict(slug="61_violet_parte1", accent=0xFFFFC857, drone=0.03, scene=s_v1, segs=[
    dict(id="h", who="nar", say="Esta mujer sobrevivió a tres desastres… en los tres barcos más famosos de su época. Parte uno.",
         cap="Sobrevivió a *3 desastres*… | en los 3 barcos | más famosos de su época"),
    dict(id="s1", who="nar", cut=True, say="Se llamaba Violet Jessop, y trabajaba como camarera en barcos de lujo.",
         cap="Se llamaba *Violet Jessop*… | camarera en barcos de *lujo*"),
    dict(id="s2", who="nar", cut=True, say="En mil novecientos once estaba a bordo del Olympic, uno de los barcos más grandes del mundo.",
         cap="1911: a bordo del *OLYMPIC*… | de los más grandes | del mundo"),
    dict(id="s3", who="nar", cut=True,
         say="Nada más zarpar, un buque de guerra británico chocó contra él y le abrió un boquete en el casco.",
         cap="Al zarpar… | un buque de guerra | le abrió un *boquete*"),
    dict(id="s4", who="nar", say="No murió nadie. El Olympic volvió a puerto por sus propios medios.",
         cap="No murió *nadie*… | y volvió a puerto"),
    dict(id="s5", who="nar", cut=True,
         say="Pero meses después, Violet subió a bordo de su barco gemelo. Se llamaba… Titanic.",
         cap="Meses después, subió | a su barco *gemelo*… | el *TITANIC*"),
    dict(id="cta", who="nar", cut=True, say="Sígueme para la parte dos.", cap="*SÍGUEME* | para la *PARTE 2*"),
]))


# ------------------------------------------------------------------ Violet · parte 2 (Titanic)
def s_v2(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    acc = V["accent"]
    tl = P["tl"]
    sea(c, t, night=True)
    if sid == "h":
        liner(c, W / 2 - t * 20, 1280, 1.0, t, lights=True, name="TITANIC")
        year_card(c, "1912", t + 0.3, acc, y=820)
    elif sid == "s1":
        a = ease_in_out(prog(lt, 0.2, 2.0))
        iceberg(c, lerp(W + 300, 900, a), 1260, 0.9, t)
        liner(c, 380, 1280, 0.85, t, lights=True)
        if a >= 1:
            hc.stamp(c, "ICEBERG", W / 2, 820, lt, 2.0, 110)
    elif sid in ("s2", "s3"):
        tilt = 4 * ease_in_out(prog(t - tl["s2"][0], 0, 3))
        liner(c, W / 2 + 100, 1200, 0.85, t, lights=True, tilt=tilt)
        lifeboat(c, 360, 1380, 1.2, t)
        K.tag(c, 360, 1520, "BOTE Nº 16", lt - 0.5 if sid == "s2" else 1, accent=acc, size=40)
        if sid == "s3":
            glow(c, 360, 1330, 120, 0xFFFFE6A0, 0.5 + 0.2 * math.sin(t * 3))
            K.tag(c, W / 2, 820, "LE DIERON UN BEBÉ", lt - 0.8, accent=WHITE, size=42)
    elif sid == "s4":
        sink = ease_in_out(prog(lt, 0, 3))
        liner(c, W / 2 + 100, 1200, 0.85, t, lights=sink < 0.5, tilt=4 + 12 * sink, sink=sink)
        lifeboat(c, 300, 1400, 1.1, t)
        K.counter(c, t, lt - 0.3, lambda p: "+" + K.fmt(1500 * p), "MUERTOS ESA NOCHE", acc, y=820, size=120)
    elif sid == "s5":
        lifeboat(c, W / 2, 1380, 1.2, t)
        hc.big(c, "¿Y DEJÓ EL MAR?", W / 2, 820, 96, acc, lt, 0.4)
        hc.big(c, "NO.", W / 2, 1000, 160, WHITE, lt, 2.4)
    else:
        lifeboat(c, W / 2, 1380, 1.2, t)
        cliff(c, t, lt, acc, "PARTE 3 →")
    sepia(c, 0.12)
    part_badge(c, "HISTORIA · PARTE 2/3", acc)


VIDEOS.append(dict(slug="62_violet_parte2", accent=0xFFFFC857, drone=0.03, scene=s_v2, segs=[
    dict(id="h", who="nar", say="Abril de mil novecientos doce. Violet trabaja de camarera en el Titanic. Parte dos.",
         cap="Abril de *1912*… | Violet trabaja | en el *TITANIC*"),
    dict(id="s1", who="nar", cut=True, say="La noche del catorce, el barco choca contra un iceberg.",
         cap="La noche del 14… | choca contra un *ICEBERG*"),
    dict(id="s2", who="nar", cut=True, say="Violet sube a cubierta y la colocan en el bote salvavidas número dieciséis.",
         cap="La suben al bote | salvavidas *nº 16*"),
    dict(id="s3", who="nar", say="Mientras bajaban el bote, un oficial le puso un bebé en los brazos para que lo cuidara.",
         cap="Un oficial le pone | un *BEBÉ* en los brazos… | para que lo cuide"),
    dict(id="s4", who="nar", cut=True, say="Más de mil quinientas personas murieron esa noche. Ella sobrevivió.",
         cap="Más de *1.500* murieron… | ella *sobrevivió*"),
    dict(id="s5", who="nar", cut=True,
         say="Cualquiera habría dejado el mar para siempre. Violet no. Cuatro años después, subió al tercer gemelo.",
         cap="¿Dejó el mar? | *NO*… | subió al *tercer gemelo*"),
    dict(id="cta", who="nar", cut=True, say="Sígueme para la parte tres.", cap="*SÍGUEME* | para la *PARTE 3*"),
]))


# ------------------------------------------------------------------ Violet · parte 3 (Britannic)
def s_v3(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    acc = V["accent"]
    tl = P["tl"]
    if sid == "h":
        sea(c, t, night=False)
        liner(c, W / 2 - t * 15, 1280, 1.0, t, lights=False, name="HMHS BRITANNIC")
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - t * 15 - 60, 1180, 120, 40), fill(0xFF2FA84A))
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - t * 15 - 18, 1160, 36, 80), fill(0xFFD83A2E))
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - t * 15 - 50, 1182, 100, 36), fill(0xFFD83A2E))
        year_card(c, "1916", t + 0.3, acc, y=820)
    elif sid == "s1":
        sea(c, t, night=False)
        sink = ease_in_out(prog(lt, 1.2, 4.0))
        liner(c, W / 2, 1280, 1.0, t, lights=False, tilt=-6 * sink, sink=sink * 0.6)
        if lt > 0.8:
            glow(c, W / 2 + 300, 1290, 320, 0xFFFFB050, 0.9 * math.exp(-(lt - 0.8) * 1.5))
        K.counter(c, t, lt - 1.0, lambda p: K.fmt(55 * p) + " min", "EN HUNDIRSE", acc, y=820, size=120)
    elif sid in ("s2", "s3"):
        # vista submarina: bote arrastrado hacia las hélices
        c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF2A5A7A, 0xFF06182A])))
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, 700), fill(0xFF8AA8C0))
        hull = skia.Path(); hull.moveTo(W, 560); hull.lineTo(560, 640); hull.lineTo(480, 1200); hull.lineTo(W, 1200); hull.close()
        c.drawPath(hull, fill(0xFF1A1C22))
        propeller(c, 620, 1050, 220, t)
        pull = ease_in(prog(t - tl["s2"][0], 0, 4))
        lifeboat(c, lerp(200, 420, pull), 690, 1.0, t)
        if sid == "s3":
            sp = ease_out(prog(lt, 0.2, 0.8))
            c.drawCircle(lerp(260, 230, sp), lerp(690, 900, sp), 18, fill(WHITE))
            for k in range(8):
                ph = (t * 1.5 + k / 8) % 1
                c.drawCircle(230 + math.sin(k) * 30, 900 - ph * 220, 6 * (1 - ph) + 2, stroke(with_alpha(WHITE, 1 - ph), 2))
            K.tag(c, 330, 1250, "SALTA AL AGUA", lt - 0.5, accent=acc, size=40)
    elif sid in ("s4", "s5"):
        hc.aurora(c, t, acc, 0xFF3C6AFF, 33)
        ships_tally(c, t, lt if sid == "s4" else 5, 3, acc)
        if sid == "s4":
            K.tag(c, W / 2, 1520, "MURIÓ EN 1971 · 83 AÑOS", lt - 2.0, accent=WHITE, size=38)
        else:
            hc.big(c, "MISS INSUMERGIBLE", W / 2, 1520, 84, acc, lt, 0.3)
    else:
        hc.aurora(c, t, acc, 0xFF3C6AFF, 33)
        ships_tally(c, t, 5, 3, acc)
    if sid not in ("s4", "s5", "cta"):
        sepia(c, 0.12)
    part_badge(c, "HISTORIA · PARTE 3/3", acc)


def ease_in(x):
    return x * x * x


VIDEOS.append(dict(slug="63_violet_parte3", accent=0xFFFFC857, drone=0.03, scene=s_v3, segs=[
    dict(id="h", who="nar", say="Mil novecientos dieciséis. Primera Guerra Mundial. Violet es enfermera en el Britannic. Parte tres.",
         cap="*1916*, Primera Guerra Mundial… | enfermera en el | *BRITANNIC*"),
    dict(id="s1", who="nar", cut=True, say="El barco choca con una mina alemana… y se hunde en solo cincuenta y cinco minutos.",
         cap="Choca con una *mina*… | y se hunde en | *55 minutos*"),
    dict(id="s2", who="nar", cut=True, say="Su bote salvavidas empieza a ser arrastrado hacia las hélices, que seguían girando.",
         cap="Su bote es arrastrado | hacia las *HÉLICES*… | que seguían girando"),
    dict(id="s3", who="nar", say="Violet salta al agua. Se golpea la cabeza… pero la rescatan.",
         cap="Violet *salta*… | se golpea la cabeza… | pero la *rescatan*"),
    dict(id="s4", who="nar", cut=True,
         say="Sobrevivió a los tres. Siguió trabajando en barcos y murió en mil novecientos setenta y uno, con ochenta y tres años.",
         cap="Sobrevivió a *los tres*… | y vivió hasta | los *83 años*"),
    dict(id="s5", who="nar", say="Hoy la conocen como… Miss Insumergible.", cap="Hoy la llaman… | *MISS INSUMERGIBLE*"),
    dict(id="cta", who="nar", cut=True, say="¿Conocías su historia? Comenta, y sígueme para más historias así.",
         cap="¿La conocías? | *COMENTA* | y *SÍGUEME*"),
]))


# ================================================================== Apolo 13
STARS = K.Stars(seed=13)
_T = {}


def tex(name, mode="RGB"):
    if name not in _T:
        _T[name] = S.load(name, mode)
    return _T[name]


def earth(c, x, y, R, spin, lat0=0.3, light=(-0.6, 0.3, 0.75)):
    img = S.render(2 * R, tex("earth_atmos_2048.jpg"), spin=spin, light=light, clouds=tex("earth_clouds_1024.png", "A"),
                   spec=tex("earth_specular_2048.jpg", "L"), night=tex("earth_lights_2048.png"), lat0=lat0, gain=1.12)
    S.draw_planet(c, x, y, R, img)
    S.atmosphere(c, x, y, R)


def moon(c, x, y, R, spin=0.0, light=(-0.6, 0.3, 0.75)):
    S.draw_planet(c, x, y, R, S.render(2 * R, tex("moon_1024.jpg"), spin=spin, light=light, ambient=0.04, gain=1.15))


def craft(c, x, y, s, t, ang=0.0, damage=0.0, frost=0.0):
    """Nave Apolo (módulo de mando + servicio + módulo lunar), apuntando a la derecha."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    # módulo lunar (dorado) detrás
    c.drawRect(skia.Rect.MakeXYWH(-330, -60, 110, 120), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(-330, -60), (-220, 60)], [0xFFF2C84A, 0xFFB8862A, 0xFFE8B83A]), AntiAlias=True))
    for k in range(4):
        c.drawLine(-330 + k * 30, -60, -320 + k * 30, 60, stroke(0x55FFFFFF, 2))
    # módulo de servicio
    c.drawRect(skia.Rect.MakeXYWH(-220, -55, 230, 110), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, -55), (0, 55)], [0xFFF2F4F8, 0xFFB8BEC8, 0xFF6A707A]), AntiAlias=True))
    for k in range(5):
        c.drawLine(-200 + k * 45, -55, -200 + k * 45, 55, stroke(0x33000000, 2))
    # módulo de mando (cono)
    cm = skia.Path(); cm.moveTo(10, -55); cm.lineTo(120, -12); cm.lineTo(120, 12); cm.lineTo(10, 55); cm.close()
    c.drawPath(cm, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, -55), (0, 55)], [0xFFFFFFFF, 0xFFA8AEB8]),
                              AntiAlias=True))
    c.drawCircle(60, -18, 7, fill(0xFF1A2E44))
    if damage > 0:
        c.drawRect(skia.Rect.MakeXYWH(-120, -55, 60, 40), fill(0xFF2A2A2A))
        rnd = random.Random(int(t * 20))
        for k in range(int(30 * damage)):
            a = rnd.uniform(-2.4, -0.7)
            d = rnd.uniform(40, 260) * damage
            c.drawCircle(-90 + math.cos(a) * d, -40 + math.sin(a) * d, rnd.uniform(3, 12),
                         fill(with_alpha(WHITE, rnd.uniform(0.2, 0.7))))
    c.restore()
    if frost > 0:
        glow(c, x, y, 380 * s, 0xFFBFE8FF, 0.25 * frost)


def a_badge(c, n, accent):
    part_badge(c, f"APOLO 13 · PARTE {n}/3", accent)


def s_a1(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; tl = P["tl"]
    acc = V["accent"]
    c.clear(0xFF020308)
    STARS.draw(c, t, camx=t * 12)
    if sid == "h":
        earth(c, 260, 1500, 420, t * 0.1)
        craft(c, 640, 950, 1.0, t, ang=-8, damage=ease_out(prog(t, 1.0, 1.6)))
        if t > 1.0:
            glow(c, 560, 920, 500, 0xFFFFC46B, 0.9 * math.exp(-(t - 1.0) * 2.5))
    elif sid == "s1":
        earth(c, W / 2, 1450, 520, t * 0.1)
        y = lerp(1300, 700, ease_in_out(prog(lt, 0, 3)))
        craft(c, W / 2, y, 0.8, t, ang=-90)
        glow(c, W / 2, y + 230, 120, 0xFFFFB050, 0.8)
        year_card(c, "1970", lt, acc, y=1650)
    elif sid in ("s2", "s3", "s4"):
        moon(c, 860, 760, 90)
        earth(c, 160, 1650, 260, t * 0.1)
        ex = t - tl["s2"][0]
        boom = ease_out(prog(ex, 1.0, 1.4))
        craft(c, W / 2, 1100, 1.15, t, ang=-4 + 3 * math.sin(t * 0.7), damage=boom)
        if ex > 1.0:
            glow(c, W / 2 - 100, 1060, 600, 0xFFFFC46B, 0.95 * math.exp(-(ex - 1.0) * 1.8))
        if sid == "s2":
            K.counter(c, t, lt - 0.2, lambda p: K.fmt(56 * p) + " h", "DE MISIÓN", acc, y=1550, size=110)
        if sid == "s3":
            r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(90, 700, 900, 170), 30, 30)
            c.drawRRect(r, fill(with_alpha(0xFF101426, 0.9)))
            c.drawRRect(r, stroke(acc, 5))
            hc.draw_text(c, "“HOUSTON, WE'VE HAD", W / 2, 775, 50, WHITE, shadow=False)
            hc.draw_text(c, "A PROBLEM HERE”", W / 2, 840, 50, WHITE, shadow=False)
            for k in range(40):
                h = abs(math.sin(t * 9 + k * 0.7)) * 50
                c.drawLine(140 + k * 20, 950 - h, 140 + k * 20, 950 + h, stroke(acc, 6))
        if sid == "s4":
            for i, lbl in enumerate(["OXÍGENO", "ELECTRICIDAD", "AGUA"]):
                hc.stamp(c, lbl, W / 2, 1450 + i * 0, lt, 0.3 + i * 0.6, 70) if i == 2 else None
            K.tag(c, W / 2, 1550, "SIN OXÍGENO · SIN LUZ · SIN AGUA", lt - 0.3, accent=0xFFFF3B4A, size=36)
    elif sid == "s5":
        moon(c, 860, 760, 90)
        earth(c, 160, 1650, 260, t * 0.1)
        craft(c, W / 2, 1100, 1.15, t, ang=-4, damage=1.0)
        hc.big(c, "¿VOLVERÍAN VIVOS?", W / 2, 1550, 90, acc, lt, 0.4)
    else:
        earth(c, W / 2, 1100, 330, t * 0.1)
        cliff(c, t, lt, acc, "PARTE 2 →")
    a_badge(c, 1, acc)


VIDEOS.append(dict(slug="64_apolo13_parte1", accent=0xFF4DE1FF, drone=0.035, scene=s_a1, segs=[
    dict(id="h", who="nar", say="A más de trescientos mil kilómetros de la Tierra… su nave explotó. Esta es la historia del Apolo trece. Parte uno.",
         cap="A más de *300.000 km* | de la Tierra… | su nave *EXPLOTÓ*"),
    dict(id="s1", who="nar", cut=True, say="Abril de mil novecientos setenta. Tres astronautas despegan rumbo a la Luna.",
         cap="Abril de *1970*… | 3 astronautas | rumbo a la *Luna*"),
    dict(id="s2", who="nar", cut=True, say="Casi cincuenta y seis horas después… un tanque de oxígeno explota.",
         cap="56 horas después… | un tanque de oxígeno | *EXPLOTA*"),
    dict(id="s3", who="nar", say="Desde la nave llega el mensaje: Houston, hemos tenido un problema.",
         cap="«*Houston*… | hemos tenido | un *problema*»"),
    dict(id="s4", who="nar", say="Pierden oxígeno, electricidad y agua. El alunizaje queda cancelado.",
         cap="Sin *oxígeno*, sin *luz*, | sin *agua*… | alunizaje *cancelado*"),
    dict(id="s5", who="nar", cut=True, say="Y la pregunta ya era otra: ¿podrían volver vivos?",
         cap="La pregunta ya era otra: | ¿volverían *VIVOS*?"),
    dict(id="cta", who="nar", cut=True, say="Sígueme para la parte dos.", cap="*SÍGUEME* | para la *PARTE 2*"),
]))


def s_a2(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; tl = P["tl"]
    acc = V["accent"]
    c.clear(0xFF020308)
    STARS.draw(c, t, camx=t * 8)
    if sid in ("h", "s1"):
        moon(c, 880, 700, 120)
        craft(c, W / 2, 1100, 1.2, t, ang=-3, damage=1.0)
        if sid == "h":
            K.tag(c, 280, 1300, "MÓDULO LUNAR = BOTE SALVAVIDAS", t - 1.2, accent=acc, size=32, line_to=(300, 1100))
        if sid == "s1":
            K.counter(c, t, lt - 0.2, lambda p: "2 → 3  ·  45 → " + K.fmt(90 * p) + " h", "PERSONAS · HORAS", acc, y=1550, size=90)
    elif sid == "s2":
        craft(c, W / 2, 1050, 1.2, t, ang=-3, damage=1.0, frost=ease_out(prog(lt, 0, 2)))
        c.drawRect(skia.Rect.MakeWH(W, H), fill(with_alpha(0xFF0A1A2A, 0.35 * prog(lt, 0, 2))))
        K.counter(c, t, lt - 0.3, lambda p: "≈ " + K.fmt(20 - 17 * p) + " °C", "EN LA CABINA", 0xFFBFE8FF, y=1550, size=120)
    elif sid == "s3":
        hc.aurora(c, t, 0xFFFF3B4A, 0xFF4A1A2A, 41)
        K.counter(c, t, lt, lambda p: "CO₂ ↑", "DIÓXIDO DE CARBONO SUBIENDO", 0xFFFF3B4A, y=1100, size=170, dur=0.3)
        k = (t * 1.3) % 1
        c.drawRect(skia.Rect.MakeWH(W, H), fill(with_alpha(0xFFFF0000, 0.08 * (1 - k))))
    elif sid == "s4":
        hc.aurora(c, t, acc, 0xFF3C6AFF, 42)
        s = ease_back(prog(lt, 0.2, 0.6))
        c.save(); c.translate(320, 1080); c.scale(s, s)
        c.drawRoundRect(skia.Rect.MakeXYWH(-140, -140, 280, 280), 20, 20, fill(0xFFB8BEC8))
        c.drawRoundRect(skia.Rect.MakeXYWH(-140, -140, 280, 280), 20, 20, stroke(WHITE, 6))
        c.restore()
        s2 = ease_back(prog(lt, 1.0, 1.4))
        c.save(); c.translate(780, 1080); c.scale(s2, s2)
        c.drawCircle(0, 0, 140, fill(0xFF101426))
        c.drawCircle(0, 0, 140, stroke(WHITE, 10))
        c.restore()
        pill(c, 320, 1290, "FILTRO", 36, bg=WHITE, fg=INK, scale=s)
        pill(c, 780, 1290, "HUECO", 36, bg=WHITE, fg=INK, scale=s2)
        hc.big(c, "≠", W / 2 + 10, 1080, 160, 0xFFFF3B4A, lt, 1.5)
    elif sid == "s5":
        hc.aurora(c, t, acc, 0xFF3C6AFF, 43)
        rnd = random.Random(8)
        for k in range(12):
            x0, y0 = 120 + (k % 4) * 280, 700 + (k // 4) * 260
            c.drawRoundRect(skia.Rect.MakeXYWH(x0, y0, 200, 120), 12, 12, fill(0xFF2A2E38))
            for j in range(5):
                on = (int(t * 4) + k + j) % 3 == 0
                c.drawCircle(x0 + 30 + j * 35, y0 + 40, 9, fill(acc if on else 0xFF4A505A))
            c.drawRect(skia.Rect.MakeXYWH(x0 + 20, y0 + 70, 160 * abs(math.sin(t + k)), 14), fill(0xFF2FD46B))
        K.tag(c, W / 2, 1550, "HOUSTON · CONTRARRELOJ", lt - 0.4, accent=acc, size=40)
    else:
        craft(c, W / 2, 1050, 1.0, t, ang=-3, damage=1.0)
        cliff(c, t, lt, acc, "PARTE 3 →")
    a_badge(c, 2, acc)


VIDEOS.append(dict(slug="65_apolo13_parte2", accent=0xFF4DE1FF, drone=0.035, scene=s_a2, segs=[
    dict(id="h", who="nar", say="Su nave se moría. Solo les quedaba un bote salvavidas: el módulo lunar. Parte dos.",
         cap="Su nave se *moría*… | solo les quedaba | el *módulo lunar*"),
    dict(id="s1", who="nar", cut=True,
         say="Estaba pensado para dos personas durante cuarenta y cinco horas. Tuvo que mantener a tres durante unas noventa.",
         cap="Para *2 personas*, 45 horas… | tuvo que aguantar | a *3* durante *90*"),
    dict(id="s2", who="nar", cut=True, say="Apagaron casi todo para ahorrar energía. La cabina se quedó a pocos grados sobre cero.",
         cap="Apagaron casi todo… | la cabina, a pocos grados | sobre *cero*"),
    dict(id="s3", who="nar", cut=True, say="Y entonces, el dióxido de carbono empezó a subir.",
         cap="Y entonces… | el *dióxido de carbono* | empezó a subir"),
    dict(id="s4", who="nar", cut=True, say="Los filtros de repuesto eran cuadrados… y el hueco donde iban, redondo.",
         cap="Los filtros eran *CUADRADOS*… | y el hueco, *REDONDO*"),
    dict(id="s5", who="nar", cut=True,
         say="En la Tierra, los ingenieros tenían horas para inventar una solución… solo con lo que había a bordo.",
         cap="Los ingenieros tenían *horas*… | solo con lo que había | *a bordo*"),
    dict(id="cta", who="nar", cut=True, say="Sígueme para la parte tres.", cap="*SÍGUEME* | para la *PARTE 3*"),
]))


def s_a3(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; tl = P["tl"]
    acc = V["accent"]
    c.clear(0xFF020308)
    if sid in ("h", "s1"):
        hc.aurora(c, t, acc, 0xFF3C6AFF, 51)
        x, y = W / 2, 1080
        c.drawRoundRect(skia.Rect.MakeXYWH(x - 200, y - 150, 300, 300), 20, 20, fill(0xFFB8BEC8))
        bag = skia.Path(); bag.moveTo(x + 100, y - 120); bag.cubicTo(x + 260, y - 160, x + 300, y + 160, x + 100, y + 120)
        bag.close()
        c.drawPath(bag, fill(with_alpha(0xFFE8F4FF, 0.55)))
        for k in range(5):
            yy = y - 110 + k * 55
            c.drawRect(skia.Rect.MakeXYWH(x + 60, yy, 150, 26), fill(0xFF8A8E96))
        c.drawRoundRect(skia.Rect.MakeXYWH(x - 240, y + 120, 160, 70), 10, 10, fill(0xFFD8B87A))
        if sid == "h":
            for i, lbl in enumerate(("PLÁSTICO", "CARTÓN", "CINTA")):
                pill(c, 240 + i * 300, 1450, lbl, 36, bg=WHITE, fg=INK, scale=ease_back(prog(t, 0.3 + i * 0.4, 0.6 + i * 0.4)))
        else:
            hc.stamp(c, "FUNCIONÓ", W / 2, 1480, lt, 1.4, 100, col=0xFF2FD46B)
    elif sid == "s2":
        STARS.draw(c, t, camx=t * 10)
        p = ease_in_out(prog(lt, 0, 4))
        moon(c, W / 2 + 120, 1050, 300, spin=t * 0.05)
        a = lerp(-0.6, 3.6, p)
        craft(c, W / 2 + 120 + math.cos(a) * 420, 1050 + math.sin(a) * 420, 0.35, t, ang=math.degrees(a) + 90, damage=1)
        K.counter(c, t, lt - 0.5, lambda q: K.fmt(400171 * q) + " km", "RÉCORD: LO MÁS LEJOS QUE HA IDO UN HUMANO", acc,
                  y=1600, size=100)
    elif sid in ("s3", "s4"):
        STARS.draw(c, t, alpha=0.5)
        earth(c, W / 2, 2300, 1300, 0.6, lat0=0.1)
        x, y = W / 2, 980
        heat = 1.0 if sid == "s3" else 1 - prog(lt, 0, 3)
        glow(c, x, y + 80, 380, 0xFFFF7A1E, 0.8 * heat)
        trail = skia.Path(); trail.moveTo(x - 70, y + 40); trail.lineTo(x + 70, y + 40); trail.lineTo(x, y - 600); trail.close()
        c.drawPath(trail, skia.Paint(Shader=skia.GradientShader.MakeLinear([(x, y), (x, y - 600)],
                                                                           [with_alpha(0xFFFFB050, 0.8 * heat), 0x00FFB050]),
                                     BlendMode=skia.BlendMode.kPlus))
        cm = skia.Path(); cm.moveTo(x - 90, y + 50); cm.lineTo(x + 90, y + 50); cm.lineTo(x + 25, y - 60); cm.lineTo(x - 25, y - 60)
        cm.close()
        c.drawPath(cm, fill(0xFF5A5048))
        if sid == "s3":
            for k in range(60):
                xx = random.random() * W
                c.drawLine(xx, 650, xx, 650 + random.random() * 30, stroke(with_alpha(WHITE, 0.15), 2))
            hc.big(c, "SIN RADIO", W / 2, 1450, 120, 0xFFFF3B4A, lt, 0.5)
        else:
            secs = int(240 * clamp(lt / max(0.5, sg["b"] - sg["a"] - 0.6)))
            K.counter(c, t, lt, lambda q: f"{secs // 60}:{secs % 60:02d}", "SIN CONTACTO", WHITE, y=1450, size=110, dur=0.01)
    elif sid == "s5":
        sea(c, t, horizon=1150, night=False)
        y = lerp(500, 1080, ease_out(prog(lt, 0, 2.5)))
        for dx, col in ((-150, 0xFFFF6A3A), (0, WHITE), (150, 0xFFFF6A3A)):
            c.drawArc(skia.Rect.MakeXYWH(W / 2 + dx - 120, y - 420, 240, 200), 180, 180, True, fill(col))
            c.drawLine(W / 2 + dx - 115, y - 320, W / 2, y - 60, stroke(with_alpha(WHITE, 0.6), 2))
            c.drawLine(W / 2 + dx + 115, y - 320, W / 2, y - 60, stroke(with_alpha(WHITE, 0.6), 2))
        cm = skia.Path(); cm.moveTo(W / 2 - 80, y + 40); cm.lineTo(W / 2 + 80, y + 40); cm.lineTo(W / 2 + 20, y - 60)
        cm.lineTo(W / 2 - 20, y - 60); cm.close()
        c.drawPath(cm, fill(0xFF8A8078))
        year_card(c, "17 · ABRIL · 1970", lt - 1.5, acc, y=1500)
    else:
        STARS.draw(c, t)
        earth(c, W / 2, 1050, 330, t * 0.1)
    a_badge(c, 3, acc)


VIDEOS.append(dict(slug="66_apolo13_parte3", accent=0xFF4DE1FF, drone=0.035, scene=s_a3, segs=[
    dict(id="h", who="nar", say="Con plástico, cartón y cinta adhesiva… salvaron tres vidas. Parte tres.",
         cap="Con *plástico*, *cartón* | y *cinta adhesiva*… | salvaron 3 vidas"),
    dict(id="s1", who="nar", cut=True, say="Fabricaron un adaptador con lo que había a bordo. Y funcionó.",
         cap="Fabricaron un *adaptador*… | y *FUNCIONÓ*"),
    dict(id="s2", who="nar", cut=True,
         say="Rodearon la Luna, y llegaron más lejos de la Tierra que ningún ser humano: unos cuatrocientos mil kilómetros.",
         cap="Rodearon la Luna… | más lejos que *ningún humano*: | *400.000 km*"),
    dict(id="s3", who="nar", cut=True, say="Al entrar en la atmósfera, la radio se cortó. Silencio total.",
         cap="Al entrar en la atmósfera… | la radio se *CORTÓ*"),
    dict(id="s4", who="nar", say="Fueron unos minutos eternos… hasta que aparecieron los paracaídas.",
         cap="Minutos *eternos*… | hasta que aparecieron | los *paracaídas*"),
    dict(id="s5", who="nar", cut=True, say="Diecisiete de abril de mil novecientos setenta. Los tres volvieron vivos.",
         cap="17 de abril de 1970… | los tres volvieron | *VIVOS*"),
    dict(id="cta", who="nar", cut=True, say="¿Conocías esta historia? Comenta, y sígueme para más historias así.",
         cap="¿La conocías? | *COMENTA* | y *SÍGUEME*"),
]))


def make_scene(V):
    return lambda c, t, P: V["scene"](c, t, P, V)


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = "auto" if len(sys.argv) > 2 else None
    for i in idxs:
        V = VIDEOS[i]
        K.run(V, make_scene(V), OUT, preview=pv)
