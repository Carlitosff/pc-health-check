"""Producción 22/11/2026 (3001 y 3002, motor 2D; 3003 mito_cafe.py y 3004 serie_jupiterg.py en 3D; sin ciudad: IGEV01 331 < 332).
  3001 PRUEBA EN DIRECTO: ANILLO DE KOFFKA. Anillo de un gris uniforme (128) sobre un fondo mitad negro / mitad blanco: sin línea se ve casi
       uniforme; con una línea fina en el borde de los fondos, la mitad sobre negro se ve más clara; al separar las mitades, más todavía.
       Wikipedia (Koffka ring): Kurt Koffka, 'Principles of Gestalt Psychology', 1935; 'a circular ring colored a uniform shade of gray';
       sin línea 'the contrast illusion almost completely disappears'; 'If ... the two ring halves are shifted so that they are completely
       separated, the illusion becomes particularly noticeable'. Assert: las dos mitades son R=G=B=128 en la imagen dibujada.
  3002 RETO: el bate y la pelota (1,10 €; el bate cuesta 1 € más; la pelota 5 céntimos). Shane Frederick, test de reflexión cognitiva (2005);
       Upworthy (18/06/2026) cita a Kahneman, 'Thinking, Fast and Slow' (2011): 'about 50% of students tested at elite schools such as MIT,
       Princeton University, and Harvard University got the question wrong'. Assert con fracciones: pelota 0,05; 0,10 daría 1,20."""
import math, sys
from fractions import Fraction as Fr
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80
GRAY = 0xFF808080


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


# ============================ 3001 anillo de Koffka
RCX, RCY, RO, RI = W / 2, 1120, 330, 205


def koffka(c, sep=0.0, line=0.0, bgk=1.0, ring=GRAY, wob=0.0):
    """Fondo: izquierda negro, derecha blanco (bgk 1) o gris medio uniforme (bgk 0). Anillo gris uniforme partido por x = RCX.
    sep separa las mitades (px). line 0..1 dibuja la línea fina negra en el borde."""
    lb = int(lerp(0x60, 0x00, bgk)); rb = int(lerp(0x60, 0xFF, bgk))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W / 2, H), fill(skia.Color(lb, lb, lb)))
    c.drawRect(skia.Rect.MakeXYWH(W / 2, 0, W / 2, H), fill(skia.Color(rb, rb, rb)))
    for side in (-1, 1):
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(0 if side < 0 else W / 2, 0, W / 2, H))
        c.translate(side * sep, wob)
        p = skia.Path(); p.addCircle(RCX, RCY, RO); p.addCircle(RCX, RCY, RI, skia.PathDirection.kCCW)
        c.drawPath(p, skia.Paint(Color=ring, AntiAlias=True))
        c.restore()
    if line > 0:
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - 4, RCY - RO - 60, 8, (2 * RO + 120) * line), fill(0xFFE0343A if bgk > .5 else INK))


def _assert_koffka():
    surf = skia.Surface(W, H); cc = surf.getCanvas()
    koffka(cc, sep=60, line=1)
    a = surf.makeImageSnapshot().toarray()[..., :3].astype(int)
    mid = (RO + RI) // 2
    L, R_ = a[RCY, int(RCX - 60 - mid)], a[RCY, int(RCX + 60 + mid)]
    assert (L == 128).all() and (R_ == 128).all(), (L, R_)
    assert (a[100, 100] == 0).all() and (a[100, W - 100] == 255).all()


_assert_koffka()


def s_koffka(c, t, P, V):
    sid, lt, d = seg(P, t)
    sep, line, bgk = 0.0, 0.0, 1.0
    if sid == "s1":
        line = ease_io((lt - d * .55) / .5)
    elif sid == "s2":
        line = 1; sep = 70 * ease_io((lt - d * .45) / .9)
    elif sid == "s3":
        line = 1; sep = 70 * (1 - ease_io((lt - d * .5) / .8))
    elif sid in ("s4", "cta"):
        line = 1 if sid == "s4" else 0; sep = 0
        if sid == "cta":
            bgk = 1.0
    wob = 6 * math.sin(t * 1.3) - (300 * ease_io(lt / .8) if sid == "cta" else 0)
    koffka(c, sep, line, bgk, wob=wob)
    if sid == "h":
        K.pill(c, W / 2, 1640, "¿UN SOLO GRIS? ¿SÍ o NO?", 54, bg=0xEE000000, fg=GOLD)
    if sid == "s2" and lt > 1.0 and lt < d * .45:
        K.tag(c, W / 2, 1640, "¿CUÁL ES MÁS CLARA?", lt - 1.0, accent=GOLD, size=48)
    if sid == "s3":                                   # cuentagotas en las dos mitades
        a = ease_out(clamp((lt - .4) / .4)); mid = (RO + RI) / 2
        for side in (-1, 1):
            px, py = RCX + side * (sep + mid), RCY + wob
            c.drawCircle(px, py, 30 * a, stroke(with_alpha(GOLD, a), 7)); c.drawCircle(px, py, 6 * a, fill(with_alpha(RED, a)))
        if lt > .8:
            K.pill(c, W / 2, 1600, "LAS DOS: R 128 · G 128 · B 128", 40, bg=0xEE000000, fg=WHITE, alpha=a)
    if sid == "s4" and lt > 1.2:
        K.tag(c, W / 2, 1700, "ANILLO DE KOFFKA · KURT KOFFKA, 1935", lt - 1.2, accent=GOLD, size=36)


V3001 = dict(slug="3001_anillo_de_koffka", accent=GOLD, drone=0.015, scene=s_koffka, mood="misterio", music=0.04,
             send="ENVÍASELO Y QUE TE DIGA QUÉ VE", dare=("s2", "PREGÚNTASELO A ALGUIEN", 1840),
             rehook=("s2", "¿Y AHORA?"), reveal=("s3", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Este anillo es todo del mismo gris? Fíjate bien y contesta: sí o no.",
         cap="¿Es *UN SOLO GRIS*?", hold=0.8),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo dice que sí. Ahora voy a poner una línea fina justo en el medio.",
         cap="Ahora, *una línea* | en el medio", hold=0.8),
    dict(id="s2", who="nar", cut=True, say="¿Y ahora? La mitad de la izquierda parece más clara que la otra, y si las separo, todavía más.",
         cap="¿Ves *DOS GRISES*?", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Pero no he tocado el color: si mido las dos mitades, son exactamente el mismo gris.",
         cap="*EL MISMO GRIS*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Es el anillo de Koffka: con la línea, tu cerebro compara cada mitad con el fondo que tiene detrás.",
         cap="Tu cerebro lo *compara* | con el fondo", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Comenta qué mitad viste más clara, y envíaselo a alguien para ver si le pasa lo mismo.",
         cap="¿Cuál viste más clara? | *COMENTA*"),
])


# ============================ 3002 el bate y la pelota
_ball = Fr(110 - 100, 2) / 100
assert _ball == Fr(5, 100) and _ball + (_ball + 1) == Fr(110, 100)
assert Fr(10, 100) + (Fr(10, 100) + 1) == Fr(120, 100)


def bat(c, x, y, ang, s=1.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    p = skia.Path(); p.moveTo(-330, -14); p.lineTo(-60, -30); p.cubicTo(120, -52, 300, -56, 340, -40)
    p.cubicTo(362, -30, 362, 30, 340, 40); p.cubicTo(300, 56, 120, 52, -60, 30); p.lineTo(-330, 14); p.close()
    g = skia.GradientShader.MakeLinear([skia.Point(0, -56), skia.Point(0, 56)], [0xFFE8B878, 0xFFC08440, 0xFF8A5626], [0, .45, 1])
    c.drawPath(p, skia.Paint(Shader=g, AntiAlias=True))
    for i in range(6):                                  # cinta del mango
        c.drawRect(skia.Rect.MakeXYWH(-325 + i * 26, -15, 14, 30), fill(0xFF2A2A30))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-352, -24, 26, 48), 10, 10), fill(0xFF7A4A20))
    c.drawPath(p, stroke(0x55000000, 3))
    c.restore()


def ball(c, x, y, r, rot):
    g = skia.GradientShader.MakeRadial(skia.Point(x - r * .35, y - r * .35), r * 1.4, [0xFFFFFFFF, 0xFFE9E4DA, 0xFFB8B0A2], [0, .6, 1])
    c.drawCircle(x, y, r, skia.Paint(Shader=g, AntiAlias=True))
    c.save(); c.translate(x, y); c.rotate(rot)
    for sgn in (-1, 1):
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(sgn * r * .55 - r * .8, -r * .8, r * 1.6, r * 1.6), 125 if sgn < 0 else -55, 110)
        c.drawPath(p, stroke(0xFFD0302A, 4))
        for k in range(7):
            a = math.radians((125 if sgn < 0 else -55) + 8 + k * 15)
            cx, cy = sgn * r * .55 + r * .8 * math.cos(a), r * .8 * math.sin(a)
            c.drawLine(cx - 6, cy - 6, cx + 6, cy + 6, stroke(0xFFD0302A, 3))
    c.restore()


def price_tag(c, x, y, txt, col, sw, s=1.0, alpha=1.0):
    c.save(); c.translate(x, y); c.rotate(sw); c.scale(s, s)
    c.drawLine(0, -90, 0, -30, stroke(with_alpha(0xFF333333, alpha), 4))
    w = max(220, 46 * len(txt) * .62 + 60)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -30, w, 96), 18, 18), fill(with_alpha(col, alpha)))
    c.drawCircle(0, -14, 8, fill(with_alpha(0xFF333333, alpha)))
    draw_text(c, txt, 0, 36, 52, with_alpha(INK, alpha), outline=0)
    c.restore()


def s_bate(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)], [0xFF1E3A5F, 0xFF0E1C30])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    for i in range(14):                                   # focos del estadio
        x = (i * 151) % W; c.drawCircle(x, 300 + 30 * math.sin(t * .7 + i), 60, fill(0x10FFFFFF))
    c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, H - 1500), fill(0xFF2E6B34))
    for i in range(12):
        c.drawRect(skia.Rect.MakeXYWH(i * 100 - (t * 30) % 100, 1500, 50, H - 1500), fill(0x14FFFFFF))
    sw = .05 * math.sin(t * 1.8)
    bat(c, W / 2 - 60, 1060 + 8 * math.sin(t * 1.1), -.32 + .03 * math.sin(t), 1.2)
    bx, by = W / 2 + 330, 1330 + 14 * abs(math.sin(t * 2.2))
    ball(c, bx, by, 72, t * .8)
    good = sid in ("s4", "cta")
    if sid not in ("s3", "cta"):
        price_tag(c, W / 2 - 160, 900, "1,05 €" if good else "BATE", GREEN if good else 0xFFF2E6C8, sw)
        price_tag(c, bx, 1180, "0,05 €" if good else "¿?", GREEN if good else GOLD, -sw, 1.0)
    if sid in ("h", "s1"):
        K.pill(c, W / 2, 1640, "JUNTOS: 1,10 €", 56, bg=0xEE000000, fg=WHITE)
        if lt > (1.8 if sid == "h" else 0):
            K.pill(c, W / 2, 1745, "EL BATE CUESTA 1 € MÁS", 46, bg=0xEE000000, fg=GOLD)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 800, 140, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2":
        a = ease_out(clamp((lt - .3) / .4))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - 300, 1600, 600, 150), 30, 30), fill(with_alpha(0xFF000000, .85 * a)))
        draw_text(c, "¿10 céntimos?", W / 2, 1700, int(70 * (.7 + .3 * a)), with_alpha(RED, a), outline=6)
        if lt > 2.0:
            K.tag(c, W / 2, 1830, "FREDERICK, 2005 · KAHNEMAN, 2011", lt - 2.0, accent=WHITE, size=30)
    if sid == "s3":                                       # ticket que comprueba la respuesta intuitiva
        a = ease_out(clamp((lt - .2) / .4)); x0, y0 = W / 2 - 330, 760
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y0, 660, 560), 20, 20), fill(with_alpha(0xFFFBF7EE, a)))
        rows = [("PELOTA", "0,10 €", INK, .6), ("BATE (+1 €)", "1,10 €", INK, 1.8), ("TOTAL", "1,20 €", RED, 3.2)]
        for i, (l, v, col, at) in enumerate(rows):
            if lt > at:
                b = ease_out(clamp((lt - at) / .3)); yy = y0 + 120 + i * 150
                if i == 2:
                    c.drawLine(x0 + 40, yy - 70, x0 + 620, yy - 70, stroke(with_alpha(INK, b), 4))
                draw_text(c, l, x0 + 190, yy, 50, with_alpha(INK, b), outline=0)
                draw_text(c, v, x0 + 500, yy, 60, with_alpha(col, b), outline=0)
        if lt > 4.0:
            K.pill(c, W / 2, 1440, "NO SALE 1,10 €", 56, bg=RED, fg=WHITE)
    if sid == "s4" and lt > 1.0:
        K.tag(c, W / 2, 1680, "0,05 + 1,05 = 1,10 €", lt - 1.0, accent=GREEN, size=52)


V3002 = dict(slug="3002_el_bate_y_la_pelota", accent=GOLD, drone=0.02, scene=s_bate, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1840),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Un bate y una pelota cuestan un euro con diez, y el bate cuesta un euro más que la pelota. ¿Cuánto cuesta la pelota?",
         cap="¿Cuánto cuesta *LA PELOTA*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos, y lo primero que piensas casi seguro que está mal.",
         cap="*5 segundos*", hold=2.4),
    dict(id="s2", who="nar", cut=True, say="Alrededor de la mitad de los estudiantes de Harvard, del MIT y de Princeton contestaron diez céntimos.",
         cap="*La mitad* | contestó *10 céntimos*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero si la pelota costara diez céntimos, el bate costaría uno diez, y juntos sumarían uno veinte.",
         cap="Así suman *1,20 €*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="La pelota cuesta cinco céntimos, y el bate cuesta un euro con cinco.",
         cap="La pelota: *5 CÉNTIMOS*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta qué dijiste tú, y envíaselo a un amigo para ver si cae en la trampa.",
         cap="¿Qué dijiste tú? | *COMENTA*"),
])

VIDEOS = {"3001": V3001, "3002": V3002}


def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
    return scene


if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == "check":
        sys.path.insert(0, '/home/claude/tts2'); import check_voice
        for k, V in VIDEOS.items():
            print(k, check_voice.check(V['segs']))
        raise SystemExit
    if arg == "dur":
        for k, V in VIDEOS.items():
            print(k, round(K.plan(V)["total"], 1))
        raise SystemExit
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        V = VIDEOS[k]
        K.run(V, make_scene(V), OUT, preview=pv)
