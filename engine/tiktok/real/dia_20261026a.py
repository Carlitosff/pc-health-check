"""Lote 26/10 madrugada (91–93): cuerpo + mitos + números (patrón ganador en IG), voz v3 Piper."""
import math, sys, random
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow

OUT = "/home/claude/tiktok/outnight3"
CTA = "¡Comenta y sígueme para más!"


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


# ------------------------------------------------------------------ corazón
def heart_path(s):
    p = skia.Path()
    p.moveTo(0, 0.35 * s)
    p.cubicTo(-0.55 * s, -0.05 * s, -0.5 * s, -0.55 * s, -0.12 * s, -0.48 * s)
    p.cubicTo(0.02 * s, -0.45 * s, 0.05 * s, -0.35 * s, 0.06 * s, -0.3 * s)
    p.cubicTo(0.12 * s, -0.5 * s, 0.55 * s, -0.55 * s, 0.52 * s, -0.12 * s)
    p.cubicTo(0.5 * s, 0.1 * s, 0.25 * s, 0.25 * s, 0, 0.35 * s)
    p.close()
    return p


def beat(t, bpm=72):
    ph = (t * bpm / 60) % 1
    return math.exp(-((ph - 0.05) / 0.05) ** 2) + 0.55 * math.exp(-((ph - 0.25) / 0.05) ** 2)


def heart(c, x, y, s, t, bpm=72):
    b = beat(t, bpm)
    sc = s * (1 + 0.07 * b)
    glow(c, x, y, sc * 0.9, 0xFFFF2D55, 0.35 + 0.4 * b)
    c.save(); c.translate(x, y); c.rotate(-12)
    p = heart_path(sc)
    g = skia.GradientShader.MakeRadial((-0.15 * sc, -0.25 * sc), sc * 0.8, [0xFFFF7A8A, 0xFFD0102E, 0xFF5A0010], [0, 0.55, 1])
    c.drawPath(p, skia.Paint(Shader=g, AntiAlias=True))
    # aorta y vasos
    for (dx, w, col) in ((-0.05, 0.11, 0xFFE0354F), (0.12, 0.08, 0xFF4A6AE0), (-0.2, 0.06, 0xFF4A6AE0)):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(dx * sc, -0.72 * sc, w * sc, 0.32 * sc), w * sc / 2, w * sc / 2), fill(col))
    # venas superficiales
    for k in range(5):
        pa = skia.Path(); x0 = -0.3 * sc + k * 0.14 * sc
        pa.moveTo(x0, -0.3 * sc); pa.quadTo(x0 + 0.08 * sc, 0, x0 - 0.02 * sc, 0.2 * sc)
        c.drawPath(pa, stroke(with_alpha(0xFF8A0018, 0.6), max(2, sc * 0.012)))
    c.drawOval(skia.Rect.MakeXYWH(-0.35 * sc, -0.42 * sc, 0.25 * sc, 0.12 * sc), fill(with_alpha(WHITE, 0.25)))
    c.restore()


def ecg(c, t, y0, col, bpm=72):
    path = skia.Path(); first = True
    for i in range(0, W + 6, 6):
        tt = t - (W - i) / W * 2.5
        ph = (tt * bpm / 60) % 1
        v = 0
        if 0.0 < ph < 0.04: v = -ph / 0.04 * 0.2
        elif 0.04 <= ph < 0.08: v = 1.0
        elif 0.08 <= ph < 0.12: v = -0.4
        elif 0.3 < ph < 0.42: v = 0.18 * math.sin((ph - 0.3) / 0.12 * math.pi)
        yy = y0 - v * 110
        if first: path.moveTo(i, yy); first = False
        else: path.lineTo(i, yy)
    c.drawPath(path, stroke(with_alpha(col, 0.35), 14)); c.drawPath(path, stroke(col, 5))


def s_corazon(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF3A0010, 0xFF1A0A2A)
    heart(c, W / 2, 980, 520 if sid != "cta" else 380, t)
    ecg(c, t, 1420, 0xFF3CFF8A)
    if sid == "s1":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(100000 * p), "LATIDOS AL DÍA", V["accent"], y=1640)
    if sid == "s2":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(7000 * p) + " L", "DE SANGRE AL DÍA", V["accent"], y=1640)
    if sid == "s3":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(2500 * p) + " M", "LATIDOS EN UNA VIDA", V["accent"], y=1640)
    if sid == "s4":
        hc.stamp(c, "SIN DESCANSO", W / 2, 1640, lt, 0.2, 110)


V91 = dict(slug="91_corazon", accent=0xFFFF5A78, drone=0.02, scene=s_corazon, segs=[
    dict(id="h", who="nar", say="Mientras ves este vídeo, tu corazón va a latir unas treinta veces. Y no se lo has pedido.",
         cap="Mientras ves esto, | tu corazón latirá | *30 veces*"),
    dict(id="s1", who="nar", cut=True, say="Al día son unos cien mil latidos.", cap="Al día: | *100.000 latidos*"),
    dict(id="s2", who="nar", cut=True, say="Y bombea unos siete mil litros de sangre. Una cisterna de camión… cada día.",
         cap="Bombea unos *7.000 litros*. | Un camión cisterna… | *cada día*"),
    dict(id="s3", who="nar", cut=True, say="En una vida larga, más de dos mil quinientos millones de latidos.",
         cap="En una vida: | más de *2.500 millones* | de latidos"),
    dict(id="s4", who="nar", say="Sin pararse ni una sola vez a descansar.", cap="Sin parar | *ni una vez*"),
    dict(id="cta", who="nar", cut=True, say="Ponte la mano en el pecho… y dale las gracias. " + CTA,
         cap="Ponte la mano en el pecho… | *COMENTA* | y *SÍGUEME*"),
])


# ------------------------------------------------------------------ pez dorado
def fish(c, x, y, s, t, flip=False):
    c.save(); c.translate(x, y)
    if flip: c.scale(-1, 1)
    c.scale(s, s)
    wag = math.sin(t * 7) * 14
    tail = skia.Path(); tail.moveTo(-150, 0); tail.quadTo(-250, -90 + wag, -290, -110 + wag); tail.quadTo(-240, 0, -290, 110 + wag)
    tail.quadTo(-250, 90 + wag, -150, 0); tail.close()
    c.drawPath(tail, skia.Paint(Shader=skia.GradientShader.MakeLinear([(-150, 0), (-290, 0)], [0xFFFF9A2E, with_alpha(0xFFFFD27A, 0.7)]), AntiAlias=True))
    fin = skia.Path(); fin.moveTo(-40, -85); fin.quadTo(20, -170 + wag * 0.5, 80, -80); fin.close()
    c.drawPath(fin, fill(with_alpha(0xFFFFB04A, 0.85)))
    body = skia.Rect.MakeXYWH(-170, -95, 330, 190)
    g = skia.GradientShader.MakeRadial((40, -40), 220, [0xFFFFD27A, 0xFFFF8A1E, 0xFFC84A08], [0, 0.5, 1])
    c.drawOval(body, skia.Paint(Shader=g, AntiAlias=True))
    for k in range(5):  # escamas
        for j in range(3):
            c.drawArc(skia.Rect.MakeXYWH(-90 + k * 42, -55 + j * 40, 40, 40), 100, 160, False, stroke(with_alpha(0xFFFFE0A0, 0.35), 3))
    c.drawCircle(95, -20, 26, fill(WHITE)); c.drawCircle(102, -20, 14, fill(0xFF101010)); c.drawCircle(106, -25, 5, fill(WHITE))
    c.drawArc(skia.Rect.MakeXYWH(125, 10, 30, 22), 200, 120, False, stroke(0xFF8A2A00, 4))
    c.restore()


def bubbles(c, t, seed=3):
    r = random.Random(seed)
    for i in range(18):
        x = r.uniform(80, W - 80); sp = r.uniform(60, 140); ph = r.uniform(0, 30)
        y = H - ((t * sp + ph * 60) % (H + 200))
        rr = r.uniform(6, 18)
        c.drawCircle(x + math.sin(t + i) * 10, y, rr, stroke(with_alpha(WHITE, 0.45), 2))


def s_pez(c, t, P, V):
    sid, lt = seg(P, t)
    g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF0E6BA8, 0xFF04203A])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    for k in range(6):  # rayos de luz
        x = 150 + k * 170 + math.sin(t * 0.5 + k) * 30
        p = skia.Path(); p.moveTo(x, 0); p.lineTo(x + 60, 0); p.lineTo(x + 220, H); p.lineTo(x + 120, H); p.close()
        c.drawPath(p, fill(with_alpha(WHITE, 0.04)))
    bubbles(c, t)
    fx = W / 2 + math.sin(t * 0.6) * 220
    flip = math.cos(t * 0.6) < 0
    fish(c, fx, 980 + math.sin(t * 1.3) * 30, 1.25, t, flip)
    if sid == "h":
        hc.big(c, "3 SEGUNDOS", W / 2, 1600, 130, V["accent"], lt, 0.2)
    if sid in ("s1",):
        hc.stamp(c, "MITO", W / 2, 1600, lt, 0.2, 160)
    if sid == "s2":
        K.counter(c, t, lt - 0.2, lambda p: str(int(round(3 * p))), "MESES RECORDANDO", V["accent"], y=1640)
    if sid == "s3":
        # palanca y comida
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(820, 1350, 40, 220), 12, 12), fill(0xFFB8B8C0))
        c.drawCircle(840, 1350, 34, fill(0xFFFF4D6D))
        for k in range(8):
            c.drawCircle(700 + (k * 37) % 160, 1280 + ((lt * 120 + k * 40) % 200), 8, fill(0xFFC8862E))


V92 = dict(slug="92_pez_memoria", accent=0xFFFFB04A, drone=0.02, scene=s_pez, segs=[
    dict(id="h", who="nar", say="Te han dicho toda la vida que los peces dorados tienen tres segundos de memoria.",
         cap="Los peces dorados tienen | *3 segundos* | de memoria…"),
    dict(id="s1", who="nar", cut=True, say="Es mentira.", cap="Es *MENTIRA*"),
    dict(id="s2", who="nar", cut=True, say="En experimentos, han recordado cosas durante meses.", cap="Han recordado cosas | durante *MESES*"),
    dict(id="s3", who="nar", say="Se les ha enseñado a empujar una palanca para conseguir comida… e incluso a ir a comer a una hora concreta del día.",
         cap="Aprenden a empujar | una *palanca* por comida… | y hasta la *hora* de comer"),
    dict(id="s4", who="nar", cut=True, say="Así que ese pez que tienes en casa… probablemente se acuerda de ti.",
         cap="Ese pez de tu casa… | probablemente | *se acuerda de ti*"),
    dict(id="cta", who="nar", cut=True, say="¿Qué otro mito quieres que desmonte? Comenta y sígueme.",
         cap="¿Qué otro *mito* | desmonto? | *COMENTA*"),
])


# ------------------------------------------------------------------ bacterias
def bacterium(c, x, y, L, w, ang, col, t, k):
    c.save(); c.translate(x, y); c.rotate(ang + math.sin(t * 2 + k) * 6)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-L / 2, -w / 2, L, w), w / 2, w / 2)
    g = skia.GradientShader.MakeLinear([(0, -w / 2), (0, w / 2)], [with_alpha(WHITE, 0.9), col, with_alpha(0xFF000000, 0.6)], [0, 0.4, 1])
    c.drawRRect(r, skia.Paint(Shader=g, AntiAlias=True))
    c.drawRRect(r, stroke(with_alpha(WHITE, 0.5), 2))
    for j in range(4):  # flagelos
        p = skia.Path(); p.moveTo(-L / 2, (j - 1.5) * w * 0.2)
        for s in range(1, 8):
            p.lineTo(-L / 2 - s * 12, (j - 1.5) * w * 0.2 + math.sin(t * 8 + s + j + k) * 8)
        c.drawPath(p, stroke(with_alpha(col, 0.6), 2))
    c.restore()


def s_bact(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A2A1A, 0xFF10203A)
    r = random.Random(5)
    n = 26
    for k in range(n):
        x = (r.uniform(0, W) + t * r.uniform(-30, 30)) % W
        y = 680 + (r.uniform(0, 860) + t * r.uniform(-20, 20)) % 860
        col = [0xFF3CD48A, 0xFF8AE04A, 0xFF4AC8E0][k % 3]
        bacterium(c, x, y, r.uniform(90, 150), r.uniform(34, 48), r.uniform(0, 180), col, t, k)
    if sid in ("s2", "s3", "s4", "cta"):
        for k in range(4):
            hc.cell(c, 220 + k * 220, 1250 + math.sin(t + k) * 20, 85, t, seed=k)
    if sid == "s1":
        hc.big(c, "×10", W / 2, 1620, 170, V["accent"], lt, 0.1)
        hc.stamp(c, "MITO", W / 2, 1450, lt, 1.0, 120)
    if sid == "s2":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(38 * p) + " BILLONES", "BACTERIAS", V["accent"], y=1600, size=100)
    if sid == "s3":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(30 * p) + " BILLONES", "CÉLULAS HUMANAS", 0xFFFF8FC7, y=1600, size=100)
    if sid == "s4":
        hc.big(c, "≈ 1 : 1", W / 2, 1620, 170, V["accent"], lt, 0.1)


V93 = dict(slug="93_bacterias", accent=0xFF6CFFA8, drone=0.02, scene=s_bact, segs=[
    dict(id="h", who="nar", say="¿Eres más bacteria que humano? Seguro que has oído que sí.",
         cap="¿Eres más *BACTERIA* | que *humano*?"),
    dict(id="s1", who="nar", cut=True, say="El dato famoso dice que tienes diez bacterias por cada célula tuya. Es un mito.",
         cap="Dicen que tienes | *10 bacterias* por cada célula… | Es un *MITO*"),
    dict(id="s2", who="nar", cut=True, say="En dos mil dieciséis lo volvieron a calcular: unos treinta y ocho billones de bacterias.",
         cap="En *2016* lo recalcularon: | unos *38 billones* | de bacterias"),
    dict(id="s3", who="nar", say="Y unos treinta billones de células humanas.", cap="Y unos *30 billones* | de células humanas"),
    dict(id="s4", who="nar", cut=True, say="Más o menos, una a una. Eres mitad tú… y mitad ellas.",
         cap="Más o menos *1 a 1*. | Mitad tú… | y mitad *ellas*"),
    dict(id="cta", who="nar", cut=True, say="¿Lo sabías? " + CTA, cap="¿Lo sabías? | *COMENTA* | y *SÍGUEME*"),
])

VIDEOS = [V91, V92, V93]


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
