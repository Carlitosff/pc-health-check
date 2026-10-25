"""Lote 'números que rompen la cabeza' (81–84) — basado en los reels top de Instagram (escala/números)."""
import math, sys, random
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow
import dia_20261025n as D

OUT = "/home/claude/tiktok/outnight2"
CTA = "¡Comenta y sígueme para más!"
DJ = skia.Typeface.MakeFromFile("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
DJB = skia.Typeface.MakeFromFile("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
STARS = K.Stars(seed=81)


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


def glyph(c, ch, x, y, size, col, tf=DJ):
    f = skia.Font(tf, size)
    w = f.measureText(ch)
    c.drawString(ch, x - w / 2, y + size * 0.35, f, fill(col))


def bg(c, t, a1, a2):
    hc.aurora(c, t, a1, a2)


# ------------------------------------------------------------------ 81 baraja
SUITS = [("♠", 0xFF15151A), ("♥", 0xFFE0263C), ("♦", 0xFFE0263C), ("♣", 0xFF15151A)]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def card(c, x, y, ang, s, idx, face=True):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-90, -130, 180, 260), 16, 16)
    c.drawRRect(r.makeOffset(6, 8) if hasattr(r, "makeOffset") else r, fill(with_alpha(0xFF000000, 0.35)))
    if face:
        c.drawRRect(r, fill(0xFFFAFAF7)); c.drawRRect(r, stroke(0xFFCCCCCC, 2))
        su, col = SUITS[idx // 13 % 4]; rk = RANKS[idx % 13]
        f = skia.Font(DJB, 40); c.drawString(rk, -76, -86, f, fill(col))
        glyph(c, su, -62, -58, 34, col)
        glyph(c, su, 0, 10, 120, col)
    else:
        c.drawRRect(r, fill(0xFF1E3A8A))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-76, -116, 152, 232), 10, 10), stroke(0xFFE8C46A, 4))
        for k in range(-4, 5):
            c.drawLine(-76, k * 26, 76, k * 26 + 60, stroke(with_alpha(0xFFE8C46A, 0.35), 2))
    c.restore()


def s_baraja(c, t, P, V):
    sid, lt = seg(P, t)
    bg(c, t, 0xFF0B3D2E, 0xFF14532D)
    rnd = random.Random(int(t * 2) if sid in ("h", "s1") else 7)
    cx, cy = W / 2, 980
    if sid in ("h", "s1"):
        # barajando: cartas volando en abanico que cambia
        n = 13
        for i in range(n):
            ph = (t * 0.9 + i / n) % 1
            ang = lerp(-60, 60, i / (n - 1)) + math.sin(t * 3 + i) * 6
            rr = 240 + math.sin(t * 2 + i) * 30
            x = cx + math.sin(math.radians(ang)) * rr
            y = cy + 120 - math.cos(math.radians(ang)) * rr * 0.6
            card(c, x, y, ang * 0.8, 0.95, (i * 7 + int(t * 3)) % 52)
    else:
        # mazo central + número gigante
        for i in range(6):
            card(c, cx + i * 3, 900 - i * 3, -4 + i, 1.1, 0, face=False)
        card(c, cx + 60, 880, 8, 1.1, int(t * 4) % 52)
    if sid == "s1":
        hc.big(c, "52 CARTAS", W / 2, 1600, 130, V["accent"], lt, 0.2)
    if sid == "s2":
        hc.big(c, "8 × 10⁶⁷", W / 2, 1560, 150, V["accent"], lt, 0.1)
        K.tag(c, W / 2, 1700, "8 Y 67 CEROS", lt - 0.5, accent=V["accent"], size=34)
    if sid in ("s3",):
        D.earth(c, 840, 1270, 120, t * 0.1)
        K.tag(c, 700, 1430, "ÁTOMOS DE LA TIERRA ≈ 10⁵⁰", lt - 0.3, accent=0xFF5AA8FF, size=30)
        hc.big(c, "MÁS", W / 2, 1600, 150, V["accent"], lt, 0.2)
    if sid == "s4":
        hc.stamp(c, "ÚNICO", W / 2, 1560, lt, 0.3, 150)


V81 = dict(slug="81_baraja", accent=0xFFFFD23F, drone=0.02, scene=s_baraja, segs=[
    dict(id="h", who="nar", say="Cada vez que barajas bien unas cartas, creas un orden que casi seguro nunca ha existido.",
         cap="Cada vez que barajas… | creas un orden que | *NUNCA* ha existido"),
    dict(id="s1", who="nar", cut=True, say="Una baraja francesa tiene cincuenta y dos cartas.", cap="Una baraja: | *52 cartas*"),
    dict(id="s2", who="nar", cut=True, say="Y se pueden ordenar de unas ocho por diez elevado a sesenta y siete formas distintas. Un ocho seguido de sesenta y siete ceros.",
         cap="Se pueden ordenar de | *8 × 10⁶⁷* formas. | Un 8 y *67 ceros*"),
    dict(id="s3", who="nar", cut=True, say="Son muchas más combinaciones que átomos tiene el planeta Tierra.",
         cap="*Más* combinaciones | que *átomos* | tiene la Tierra"),
    dict(id="s4", who="nar", cut=True, say="Así que si barajas bien, ese orden probablemente es único en la historia del universo.",
         cap="Ese orden es *único* | en la historia | del *universo*"),
    dict(id="cta", who="nar", cut=True, say="Ve a por una baraja y crea historia. " + CTA, cap="Ve a por una baraja… | *COMENTA* | y *SÍGUEME*"),
])


# ------------------------------------------------------------------ 82 contar hasta mil millones
def s_contar(c, t, P, V):
    sid, lt = seg(P, t); tl = P["tl"]
    c.clear(0xFF04050C)
    STARS.draw(c, t, camx=t * 30, zoom=1.0, alpha=0.7)
    # Tierra girando rápido = días pasando
    sp = 0.1 if sid in ("h", "s1") else 0.1 + (t - tl["s1"][1]) * 0.25
    D.earth(c, W / 2, 1020, 300, t * sp)
    if sid == "h":
        n = int(lerp(1, 999999999, ease_in_out(prog(lt, 0.3, 3.0)) ** 3))
        hc.big(c, "{:,}".format(n).replace(",", "."), W / 2, 1520, 110, V["accent"], lt, 0.0)
    if sid == "s1":
        hc.big(c, "1 POR SEGUNDO", W / 2, 1520, 110, V["accent"], lt, 0.1)
    if sid == "s2":
        K.counter(c, t, lt - 0.2, lambda p: "%.1f días" % (11.6 * p), "UN MILLÓN", V["accent"], y=1560)
    if sid == "s3":
        K.counter(c, t, lt - 0.2, lambda p: "%.1f años" % (31.7 * p), "MIL MILLONES", V["accent"], y=1560)
    if sid == "s4":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(31700 * p) + " años", "UN BILLÓN", V["accent"], y=1560)
    if sid == "s5":
        hc.stamp(c, "SIN DORMIR", W / 2, 1540, lt, 0.2, 120)


V82 = dict(slug="82_contar_mil_millones", accent=0xFF6FE3FF, drone=0.02, scene=s_contar, segs=[
    dict(id="h", who="nar", say="Si empezaras a contar hasta mil millones ahora mismo… ¿cuándo acabarías?",
         cap="Si contaras hasta | *MIL MILLONES*… | ¿cuándo acabarías?"),
    dict(id="s1", who="nar", cut=True, say="Un número por segundo, sin parar.", cap="Un número | por *segundo*"),
    dict(id="s2", who="nar", cut=True, say="Hasta un millón tardarías once días y medio.", cap="Hasta un millón: | *11 días y medio*"),
    dict(id="s3", who="nar", cut=True, say="Pero hasta mil millones… treinta y un años y ocho meses.", cap="Hasta mil millones: | *casi 32 AÑOS*"),
    dict(id="s4", who="nar", cut=True, say="Y hasta un billón, un millón de millones: treinta y un mil setecientos años. Más que toda la historia escrita.",
         cap="Hasta un *billón*: | *31.700 años*. | Más que toda la historia"),
    dict(id="s5", who="nar", say="Y eso sin dormir ni un segundo.", cap="Y sin *dormir* | ni un segundo"),
    dict(id="cta", who="nar", cut=True, say="¿Hasta cuánto has contado tú alguna vez? " + CTA,
         cap="¿Hasta cuánto | has contado tú? | *COMENTA*"),
])


# ------------------------------------------------------------------ 83 ajedrez
PIECES = "♜♞♝♛♚♝♞♜"


def board(c, t, lt, spin):
    c.save(); c.translate(W / 2, 1050)
    c.concat(skia.Matrix.MakeAll(1, 0, 0, 0, 0.55, 0, 0, 0.0004, 1))
    c.rotate(spin)
    s = 92
    for i in range(8):
        for j in range(8):
            col = 0xFFEAD7B0 if (i + j) % 2 == 0 else 0xFF8A5A34
            c.drawRect(skia.Rect.MakeXYWH(-4 * s + i * s, -4 * s + j * s, s, s), fill(col))
    c.drawRect(skia.Rect.MakeXYWH(-4 * s, -4 * s, 8 * s, 8 * s), stroke(0xFF3A2414, 10))
    c.restore()


def s_ajedrez(c, t, P, V):
    sid, lt = seg(P, t)
    if sid in ("s3", "s4"):
        c.clear(0xFF02030A)
        STARS.draw(c, t, camx=t * 60, zoom=1.0 + (t % 10) * 0.05, alpha=1.0)
        glow(c, W / 2, 900, 380, 0xFF8A6AFF, 0.6)
    else:
        bg(c, t, 0xFF2A1A0A, 0xFF4A2A10)
        board(c, t, lt, math.sin(t * 0.3) * 8)
        f_y = 860
        for i, ch in enumerate(PIECES):
            x = W / 2 - 3.5 * 110 + i * 110
            bob = math.sin(t * 2 + i) * 10
            glyph(c, ch, x, f_y + bob, 120, 0xFF15151A, DJ)
            glyph(c, "♟", x, f_y + 150 + bob * 0.5, 100, 0xFF15151A, DJ)
    if sid == "s1":
        K.counter(c, t, lt - 0.2, lambda p: str(int(round(400 * p))), "POSICIONES TRAS 1 JUGADA CADA UNO", V["accent"], y=1600)
    if sid == "s2":
        hc.big(c, "10¹²⁰", W / 2, 1560, 180, V["accent"], lt, 0.1)
        K.tag(c, W / 2, 1720, "PARTIDAS POSIBLES (SHANNON, 1950)", lt - 0.5, accent=V["accent"], size=30)
    if sid == "s3":
        hc.big(c, "10⁸⁰", W / 2, 1500, 180, 0xFFBFAEFF, lt, 0.1)
        K.tag(c, W / 2, 1660, "ÁTOMOS EN EL UNIVERSO OBSERVABLE", lt - 0.5, accent=0xFFBFAEFF, size=30)
    if sid == "s4":
        hc.big(c, "10¹²⁰ > 10⁸⁰", W / 2, 1520, 140, V["accent"], lt, 0.1)


V83 = dict(slug="83_ajedrez", accent=0xFFFFB86B, drone=0.02, scene=s_ajedrez, segs=[
    dict(id="h", who="nar", say="Hay más partidas de ajedrez posibles que átomos en todo el universo.",
         cap="Hay más partidas de *AJEDREZ* | que *átomos* | en el universo"),
    dict(id="s1", who="nar", cut=True, say="Tras solo un movimiento de cada jugador, ya hay cuatrocientas posiciones posibles.",
         cap="Tras *un movimiento* | de cada uno: | *400 posiciones*"),
    dict(id="s2", who="nar", cut=True, say="En mil novecientos cincuenta, el matemático Claude Shannon calculó unas diez elevado a ciento veinte partidas distintas.",
         cap="En *1950*, Claude *Shannon* | calculó unas | *10¹²⁰ partidas*"),
    dict(id="s3", who="nar", cut=True, say="Los átomos de todo el universo observable se estiman en diez elevado a ochenta.",
         cap="Átomos del universo: | unos *10⁸⁰*"),
    dict(id="s4", who="nar", cut=True, say="Cuarenta ceros más. Por eso, cada partida que juegas es probablemente nueva.",
         cap="*40 ceros más*. | Tu partida, | probablemente *nueva*"),
    dict(id="cta", who="nar", cut=True, say="¿Juegas al ajedrez? " + CTA, cap="¿Juegas al ajedrez? | *COMENTA* | y *SÍGUEME*"),
])


# ------------------------------------------------------------------ 84 la luz 7,5 vueltas
def s_luz(c, t, P, V):
    sid, lt = seg(P, t); tl = P["tl"]
    c.clear(0xFF02030A)
    STARS.draw(c, t, camx=t * 15, zoom=1.0, alpha=0.9)
    ex, ey, R = W / 2, 1000, 330
    D.earth(c, ex, ey, R, t * 0.05)
    run = sid in ("s1", "s2")
    if run or sid == "h":
        speed = 0.6 if sid == "h" else 2.2
        a0 = t * speed * 2 * math.pi
        for k in range(26):
            a = a0 - k * 0.06
            x = ex + math.cos(a) * (R + 40)
            y = ey + math.sin(a) * (R + 40) * 0.35
            front = math.sin(a) > 0
            if not front and (x - ex) ** 2 < (R * 0.95) ** 2:
                continue
            glow(c, x, y, 34 - k, 0xFFFFF2A8, (1 - k / 26))
        c.drawCircle(ex + math.cos(a0) * (R + 40), ey + math.sin(a0) * (R + 40) * 0.35, 9, fill(WHITE))
    if sid == "s1":
        K.counter(c, t, lt - 0.2, lambda p: "%.1f" % (7.5 * p), "VUELTAS EN 1 SEGUNDO", V["accent"], y=1600)
    if sid == "s2":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(299792 * p) + " km/s", "VELOCIDAD DE LA LUZ", V["accent"], y=1600, size=110)
    if sid == "s3":
        D.moon(c, 880, 470, 70)
        hc.big(c, "1,3 s", W / 2, 1600, 150, V["accent"], lt, 0.1)
    if sid == "s4":
        D.sun(c, 880, 560, 90, t)
        hc.big(c, "8 MIN 20 S", W / 2, 1600, 130, V["accent"], lt, 0.1)


V84 = dict(slug="84_luz_vueltas", accent=0xFFFFF27A, drone=0.02, scene=s_luz, segs=[
    dict(id="h", who="nar", say="En lo que dura un chasquido de dedos, la luz le da siete vueltas y media a la Tierra.",
         cap="En un *chasquido*, | la luz da | *7,5 VUELTAS* a la Tierra"),
    dict(id="s1", who="nar", cut=True, say="Siete vueltas y media en un solo segundo.", cap="*7,5 vueltas* | en *1 segundo*"),
    dict(id="s2", who="nar", cut=True, say="Porque viaja a casi trescientos mil kilómetros por segundo.", cap="Casi | *300.000 km* | por segundo"),
    dict(id="s3", who="nar", cut=True, say="A la Luna llega en poco más de un segundo.", cap="A la *Luna*: | poco más de *1 segundo*"),
    dict(id="s4", who="nar", cut=True, say="Y aun así, la luz del Sol tarda más de ocho minutos en llegarte. Así de enorme es el espacio.",
         cap="Y la del *Sol* tarda | *8 minutos*. | Así de enorme es el espacio"),
    dict(id="cta", who="nar", cut=True, say="¿Lo sabías? " + CTA, cap="¿Lo sabías? | *COMENTA* | y *SÍGUEME*"),
])

VIDEOS = [V81, V82, V83, V84]


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
