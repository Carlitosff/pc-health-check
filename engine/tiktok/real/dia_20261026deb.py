"""Lote 'debate' 26/10/2026 (111–115): temas que dividen y hacen comentar. Datos verificados. Voz v3."""
import math, sys, random
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow

OUT = "/home/claude/tiktok/outdeb"
CTA_D = "Comenta, que esto se pone interesante. Y sígueme para más."


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


def plate(c, x, y, r):
    c.drawCircle(x + 10, y + 16, r * 1.18, fill(with_alpha(0xFF000000, 0.35)))
    g = skia.GradientShader.MakeRadial((x - r * 0.3, y - r * 0.3), r * 1.4, [0xFFFFFFFF, 0xFFDCDCE0])
    c.drawCircle(x, y, r * 1.18, skia.Paint(Shader=g, AntiAlias=True))
    c.drawCircle(x, y, r * 1.02, stroke(0xFFC8C8CC, 3))


def vs_bar(c, t, lt, a_lbl, b_lbl, ca, cb, y=1560):
    """Barra de votación animada A vs B (sin resultado: invita a comentar)."""
    p = 0.5 + 0.18 * math.sin(lt * 2.2)
    w = 900; x0 = W / 2 - w / 2
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y, w * p, 90), 45, 45), fill(ca))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 + w * p, y, w * (1 - p), 90), 45, 45), fill(cb))
    f = skia.Font(K.TF_BLACK, 44)
    c.drawString(a_lbl, x0 + 30, y + 62, f, fill(WHITE))
    c.drawString(b_lbl, x0 + w - 30 - f.measureText(b_lbl), y + 62, f, fill(WHITE))
    hc.big(c, "VS", W / 2, y - 40, 70, WHITE, lt, 0.0)


# ---------------------------------------------------------------- 111 tortilla
def tortilla(c, x, y, r, t, onion, cut=0.0):
    plate(c, x, y, r)
    c.save()
    if cut > 0:
        c.clipPath(skia.Path().addCircle(x, y, r), skia.ClipOp.kIntersect)
    g = skia.GradientShader.MakeRadial((x - r * 0.25, y - r * 0.3), r * 1.2, [0xFFFFD873, 0xFFE8A93A, 0xFFB86A1E], [0, 0.6, 1])
    c.drawCircle(x, y, r, skia.Paint(Shader=g, AntiAlias=True))
    rr = random.Random(4)
    for k in range(40):
        a = rr.uniform(0, 6.28); d = rr.uniform(0, r * 0.9)
        c.drawCircle(x + math.cos(a) * d, y + math.sin(a) * d, rr.uniform(6, 16), fill(with_alpha(0xFF8A4A10, 0.25)))
    c.restore()
    if cut > 0:  # porción sacada: se ve el interior
        a0 = -30
        c.save(); c.translate(x, y)
        wedge = skia.Path(); wedge.moveTo(0, 0); wedge.arcTo(skia.Rect.MakeXYWH(-r, -r, 2 * r, 2 * r), a0, 50, False); wedge.close()
        c.translate(math.cos(math.radians(a0 + 25)) * 60 * cut, math.sin(math.radians(a0 + 25)) * 60 * cut)
        c.drawPath(wedge, fill(0xFFFFE9A0))
        rr2 = random.Random(9)
        c.clipPath(wedge)
        for k in range(26):
            px, py = rr2.uniform(0, r), rr2.uniform(-r * 0.6, r * 0.3)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(px, py, 46, 22), 8, 8), fill(0xFFF6E7B0))
            if onion and k % 2 == 0:
                c.drawArc(skia.Rect.MakeXYWH(px + 10, py - 20, 40, 30), 200, 140, False, stroke(0xFFF2F0D8, 6))
        c.restore()


def s_tortilla(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF3A2006, 0xFF1A1A3A)
    onion = sid in ("s2",)
    tortilla(c, W / 2, 1020, 330, t, onion=True, cut=ease_out(prog(t, 1.0, 2.0)))
    if sid in ("q", "q_count"):
        pass
    if sid == "s1":
        hc.big(c, "1817", W / 2, 1560, 160, V["accent"], lt, 0.1)
    if sid in ("h", "s3", "cta"):
        vs_bar(c, t, lt, "CON", "SIN", 0xFFE8A93A, 0xFF6A5AF0)


V111 = dict(slug="111_tortilla", accent=0xFFFFC23C, drone=0.02, scene=s_tortilla, segs=[
    dict(id="h", who="nar", say="Este vídeo va a acabar en pelea en los comentarios. Tortilla de patatas: ¿con cebolla o sin cebolla?",
         cap="Esto acaba en *pelea*: | tortilla de patatas, | ¿*CON* o *SIN* cebolla?"),
    dict(id="s1", who="nar", cut=True, say="La primera referencia escrita que se conoce es de mil ochocientos diecisiete, en un documento de Navarra.",
         cap="La primera referencia escrita: | *1817*, | en *Navarra*"),
    dict(id="s2", who="nar", cut=True, say="Y hablaba de tortilla con patatas… sin decir nada de la cebolla.",
         cap="Hablaba de patatas… | y de la cebolla, | *ni una palabra*"),
    dict(id="q", who="q", say="Entonces, ¿cuál es la de verdad?", cap="¿Cuál es | la *de verdad*?",
         quiz=dict(a="CON CEBOLLA", b="SIN CEBOLLA", ans="a")),
    dict(id="s3", who="nar", cut=True, say="Yo ya he elegido. Pero me interesa más lo que pienses tú.", cap="Yo ya he elegido… | pero dime *tú*"),
    dict(id="cta", who="nar", cut=True, say="Escribe con o sin. " + CTA_D, cap="Escribe *CON* o *SIN* 👇 | y *SÍGUEME*"),
])


# ---------------------------------------------------------------- 112 pizza con piña
def pizza(c, x, y, r, t, pine=1.0):
    plate(c, x, y, r)
    g = skia.GradientShader.MakeRadial((x, y), r, [0xFFE8B060, 0xFFC8802E], [0.85, 1])
    c.drawCircle(x, y, r, skia.Paint(Shader=g, AntiAlias=True))
    c.drawCircle(x, y, r * 0.86, fill(0xFFC8321E))
    rr = random.Random(8)
    for k in range(30):
        a = rr.uniform(0, 6.28); d = rr.uniform(0, r * 0.75)
        c.drawCircle(x + math.cos(a) * d, y + math.sin(a) * d, rr.uniform(30, 55), fill(with_alpha(0xFFFFE8A0, 0.85)))
    for k in range(10):
        a = rr.uniform(0, 6.28); d = rr.uniform(r * 0.2, r * 0.75)
        c.drawCircle(x + math.cos(a) * d, y + math.sin(a) * d, 26, fill(0xFFE8506A))
    rr2 = random.Random(3)
    for k in range(int(14 * pine)):
        a = rr2.uniform(0, 6.28); d = rr2.uniform(0, r * 0.72)
        px, py = x + math.cos(a) * d, y + math.sin(a) * d - (1 - clamp(pine * 3 - k * 0.15)) * 300
        c.save(); c.translate(px, py); c.rotate(rr2.uniform(0, 180))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-30, -18, 60, 36), 8, 8), fill(0xFFFFD84A))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-30, -18, 60, 36), 8, 8), stroke(0xFFE0A818, 3))
        c.restore()


def s_pizza(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF3A0A0A, 0xFF0A2A1A)
    pizza(c, W / 2, 1000, 330, t, pine=ease_out(prog(t, 0.3, 2.0)))
    if sid == "s1":
        hc.big(c, "CANADÁ · 1962", W / 2, 1560, 120, V["accent"], lt, 0.1)
    if sid == "s2":
        hc.big(c, "SAM PANOPOULOS", W / 2, 1560, 100, V["accent"], lt, 0.1)
    if sid in ("h", "cta"):
        vs_bar(c, t, lt, "SÍ", "JAMÁS", 0xFFFFC23C, 0xFFE0263C)


V112 = dict(slug="112_pizza_pina", accent=0xFFFFD84A, drone=0.02, scene=s_pizza, segs=[
    dict(id="h", who="nar", say="Pizza con piña. Hay gente que la defiende… y gente que la considera un crimen.",
         cap="Pizza con *PIÑA*: | ¿manjar | o *crimen*?"),
    dict(id="s1", who="nar", cut=True, say="Lo más curioso: no es italiana ni hawaiana. Nació en Canadá, en mil novecientos sesenta y dos.",
         cap="Ni italiana ni hawaiana: | nació en *Canadá*, | en *1962*"),
    dict(id="s2", who="nar", cut=True, say="La inventó Sam Panopoulos, un griego que tenía un restaurante en Ontario. La llamó hawaiana por la marca de la lata de piña.",
         cap="La inventó *Sam Panopoulos*, | un *griego* en Ontario. | Hawaiana… por la *lata*"),
    dict(id="q", who="q", say="¿Y tú qué eres?", cap="¿Y tú | qué eres?", quiz=dict(a="EQUIPO PIÑA", b="NI MUERTO", ans="a")),
    dict(id="cta", who="nar", cut=True, say="Comenta sí o jamás. " + CTA_D, cap="Comenta *SÍ* o *JAMÁS* 👇 | y *SÍGUEME*"),
])


# ---------------------------------------------------------------- 113 tomate fruta
def tomato(c, x, y, r, t):
    glow(c, x, y, r * 1.4, 0xFFFF3A2A, 0.3)
    g = skia.GradientShader.MakeRadial((x - r * 0.35, y - r * 0.35), r * 1.5, [0xFFFF8A6A, 0xFFE0261A, 0xFF7A0A06], [0, 0.5, 1])
    c.drawOval(skia.Rect.MakeXYWH(x - r * 1.08, y - r * 0.95, r * 2.16, r * 1.9), skia.Paint(Shader=g, AntiAlias=True))
    c.drawOval(skia.Rect.MakeXYWH(x - r * 0.65, y - r * 0.7, r * 0.45, r * 0.25), fill(with_alpha(WHITE, 0.4)))
    for k in range(5):
        a = math.radians(k * 72 + math.sin(t) * 5)
        p = skia.Path(); p.moveTo(x, y - r * 0.9)
        p.quadTo(x + math.cos(a) * r * 0.25, y - r * 0.95 + math.sin(a) * r * 0.1, x + math.cos(a) * r * 0.45, y - r * 0.85 + math.sin(a) * r * 0.18)
        c.drawPath(p, stroke(0xFF2E8A2E, 18))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 8, y - r * 1.15, 16, r * 0.3), 8, 8), fill(0xFF2E7A2E))


def gavel(c, x, y, lt):
    ang = -30 + 30 * abs(math.sin(lt * 4)) if lt < 1.0 else 0
    c.save(); c.translate(x, y); c.rotate(ang)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-14, -10, 28, 220), 12, 12), fill(0xFF6A3A18))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -60, 160, 70), 18, 18), fill(0xFF8A4A1E))
    c.restore()


def s_tomate(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF2A0606, 0xFF06200E)
    tomato(c, W / 2, 1000, 260, t)
    if sid == "s1":
        hc.stamp(c, "FRUTA", W / 2, 1520, lt, 0.2, 140, col=0xFF2FD46B)
    if sid in ("s2", "s3"):
        gavel(c, 830, 1380, lt)
        hc.big(c, "1893", W / 2, 1600, 150, V["accent"], lt, 0.1)
    if sid == "s3":
        hc.stamp(c, "VERDURA", W / 2, 1420, lt, 0.4, 120)


V113 = dict(slug="113_tomate", accent=0xFFFF6A5A, drone=0.02, scene=s_tomate, segs=[
    dict(id="h", who="nar", say="¿El tomate es una fruta o una verdura? Ojo, que la respuesta tiene trampa.",
         cap="¿El tomate es | *FRUTA* o *VERDURA*? | Ojo, que hay *trampa*"),
    dict(id="q", who="q", say="¿Tú qué dices?", cap="¿Tú qué dices?", quiz=dict(a="FRUTA", b="VERDURA", ans="a")),
    dict(id="s1", who="nar", cut=True, say="Para la botánica, es una fruta: nace de la flor y lleva las semillas dentro.",
         cap="Para la botánica: *FRUTA*. | Nace de la flor | y lleva *semillas*"),
    dict(id="s2", who="nar", cut=True, say="Pero en mil ochocientos noventa y tres, el Tribunal Supremo de Estados Unidos decidió lo contrario.",
         cap="Pero en *1893*, | el *Tribunal Supremo* de EE. UU. | decidió otra cosa"),
    dict(id="s3", who="nar", say="Por un tema de impuestos, lo declaró verdura. Así que… depende de a quién preguntes.",
         cap="Por *impuestos*, | lo declaró *VERDURA*. | Depende de a quién preguntes"),
    dict(id="cta", who="nar", cut=True, say="¿Fruta o verdura? " + CTA_D, cap="¿*Fruta* o *verdura*? 👇 | y *SÍGUEME*"),
])


# ---------------------------------------------------------------- 114 vikingos sin cuernos
def helmet(c, x, y, s, t, horns=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if horns > 0.01:
        for side in (-1, 1):
            p = skia.Path(); p.moveTo(side * 150, -40)
            p.cubicTo(side * 260, -80, side * 300, -220, side * 230, -330)
            p.cubicTo(side * 230, -230, side * 190, -120, side * 140, -95); p.close()
            c.drawPath(p, fill(with_alpha(0xFFF2E6CC, horns)))
            c.drawPath(p, stroke(with_alpha(0xFF8A7A5A, horns), 4))
    dome = skia.Path(); dome.addArc(skia.Rect.MakeXYWH(-170, -200, 340, 380), 180, 180)
    dome.lineTo(170, 20); dome.lineTo(-170, 20); dome.close()
    g = skia.GradientShader.MakeLinear([(-170, -200), (170, 20)], [0xFFD8DCE4, 0xFF7A808C, 0xFF3A3F4A], [0, 0.5, 1])
    c.drawPath(dome, skia.Paint(Shader=g, AntiAlias=True))
    c.drawRect(skia.Rect.MakeXYWH(-175, -10, 350, 40), fill(0xFF8A6A3A))
    c.drawRect(skia.Rect.MakeXYWH(-14, -200, 28, 210), fill(0xFF8A6A3A))
    c.drawRect(skia.Rect.MakeXYWH(-18, 20, 36, 120), fill(0xFF6A7080))
    for k in range(-3, 4):
        c.drawCircle(k * 46, 10, 7, fill(0xFFE8D8A8))
    c.restore()


def s_vikingos(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A1A2A, 0xFF2A1A0A)
    a = P["tl"]["s1"][0]
    horns = 1.0 - ease_in_out(prog(t, a + 0.6, a + 1.4))
    helmet(c, W / 2, 1100, 1.5, t, horns)
    if sid == "s1":
        hc.stamp(c, "FALSO", W / 2, 1560, lt, 0.2, 150)
    if sid == "s2":
        hc.big(c, "1876", W / 2, 1600, 160, V["accent"], lt, 0.1)
    if sid == "s3":
        hc.big(c, "UNA ÓPERA", W / 2, 1600, 130, V["accent"], lt, 0.1)


V114 = dict(slug="114_vikingos", accent=0xFFFFC27A, drone=0.02, scene=s_vikingos, segs=[
    dict(id="h", who="nar", say="Todo lo que crees saber de los vikingos tiene un error. Y lo has visto mil veces.",
         cap="Lo que sabes de los *VIKINGOS* | tiene un *error*… | y lo has visto mil veces"),
    dict(id="s1", who="nar", cut=True, say="Los cascos con cuernos. No hay ninguna prueba de que los llevaran en batalla.",
         cap="Los cascos con *cuernos*. | Ninguna prueba | de que los llevaran"),
    dict(id="s2", who="nar", cut=True, say="El único casco vikingo casi completo que se ha encontrado, el de Gjermundbu, no tiene cuernos. La imagen se popularizó en mil ochocientos setenta y seis.",
         cap="El único casco casi completo: | *sin cuernos*. | La imagen se popularizó en *1876*"),
    dict(id="s3", who="nar", cut=True, say="Fue por una ópera de Wagner: el diseñador de vestuario se los inventó. Y se quedaron para siempre.",
         cap="Por una *ópera de Wagner*: | el vestuario se los *inventó*… | y se quedaron"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo creías? Di la verdad. " + CTA_D, cap="¿Te lo creías? | Di la *verdad* 👇 | y *SÍGUEME*"),
])


# ---------------------------------------------------------------- 115 agujeros de una pajita
def straw(c, x, y, t, sq=0.0):
    c.save(); c.translate(x, y); c.rotate(-25 + math.sin(t * 0.8) * 6)
    L, R = 560, 70
    g = skia.GradientShader.MakeLinear([(0, -R), (0, R)], [0xFFFFFFFF, 0xFFFF6A8A, 0xFFB01A40], [0, 0.45, 1])
    c.drawRect(skia.Rect.MakeXYWH(-L / 2, -R, L, 2 * R), skia.Paint(Shader=g, AntiAlias=True))
    for k in range(-5, 6):
        c.drawLine(k * 50 - 30, -R, k * 50 + 30, R, stroke(with_alpha(WHITE, 0.6), 14))
    for sx in (-L / 2, L / 2):
        c.drawOval(skia.Rect.MakeXYWH(sx - 26, -R, 52, 2 * R), fill(0xFFFF8AA8))
        c.drawOval(skia.Rect.MakeXYWH(sx - 18, -R + 12, 36, 2 * R - 24), fill(0xFF2A0610))
    c.restore()


def s_pajita(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF2A0A2A, 0xFF0A1A3A)
    if sid in ("s2", "s3"):
        # donut: la pajita "aplastada" es un anillo
        r = 230
        g = skia.GradientShader.MakeRadial((W / 2 - 60, 940), 420, [0xFFFFB8C8, 0xFFFF6A8A, 0xFFB01A40])
        p = skia.Path(); p.addCircle(W / 2, 1000, r); p.addCircle(W / 2, 1000, r * 0.42); p.setFillType(skia.PathFillType.kEvenOdd)
        c.drawPath(p, skia.Paint(Shader=g, AntiAlias=True))
        hc.big(c, "= DONUT", W / 2, 1420, 120, V["accent"], lt, 0.2)
    else:
        straw(c, W / 2, 1000, t)
    if sid == "s1":
        hc.big(c, "1 AGUJERO", W / 2, 1560, 140, V["accent"], lt, 0.1)
    if sid == "s3":
        hc.big(c, "TOPOLOGÍA", W / 2, 1620, 110, WHITE, lt, 0.2)


V115 = dict(slug="115_pajita", accent=0xFFFF8AC8, drone=0.02, scene=s_pajita, segs=[
    dict(id="h", who="nar", say="Esta pregunta ha dividido a internet: ¿cuántos agujeros tiene una pajita? ¿Uno o dos?",
         cap="¿Cuántos *agujeros* | tiene una *pajita*? | ¿*1* o *2*?"),
    dict(id="q", who="q", say="Piénsalo bien antes de contestar.", cap="Piénsalo *bien*…", quiz=dict(a="UNO", b="DOS", ans="a")),
    dict(id="s1", who="nar", cut=True, say="Para las matemáticas, la respuesta es uno.", cap="Para las matemáticas: | *UNO*"),
    dict(id="s2", who="nar", cut=True, say="Si pudieras aplastarla y estirarla sin romperla, acabaría siendo un donut. Un solo agujero que la atraviesa.",
         cap="Aplástala sin romperla… | y es un *DONUT*: | *un solo agujero*"),
    dict(id="s3", who="nar", say="Esa rama de las matemáticas se llama topología. Y para ella, una taza y un donut son lo mismo.",
         cap="Se llama *topología*. | Para ella, una *taza* | y un *donut* son lo mismo"),
    dict(id="cta", who="nar", cut=True, say="¿Uno o dos? Defiende tu respuesta. " + CTA_D, cap="¿*1* o *2*? | Defiéndelo 👇 | y *SÍGUEME*"),
])

VIDEOS = [V111, V112, V113, V114, V115]


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
