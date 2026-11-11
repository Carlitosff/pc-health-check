"""Producción 11/11/2026 (1901 y 1902, motor 2D; 1903 mito_ovejas.py y 1904 serie_inclina.py en 3D). Sin ciudad: IGEV01 bajó de 313 a 311.
  1901 PRUEBA EN DIRECTO: el vídeo mudo que 'suena' (vEAR, respuesta auditiva evocada por la vista). Chris Fassnidge y Elliot Freeman (City University
       of London), Cortex 2018, vía Smithsonian: 'more than 20 percent of the 4000 people surveyed find GIFs quite noisy'. Animación PROPIA (caja que
       salta a la comba entre dos farolas, con temblor de cámara en cada caída), no la del poste de HappyToast. Silencio total con V['hush'] (motor v22).
  1902 RETO: balanzas. Manzana = 3 naranjas; naranja + limón = 3 limones → naranja = 2 limones; manzana + limón = 7 limones (assert; error típico 6)."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
from dia_20261110 import fruit
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 1901 el vídeo mudo que suena
PER = 1.05  # s por salto


def jump_state(t):
    ph = (t % PER) / PER
    y = math.sin(math.pi * ph) ** 1.4          # altura de la caja 0..1
    land = (t % PER)                            # s desde la última caída
    rope = math.cos(2 * math.pi * ph)           # 1 = cuerda abajo (en el suelo) al caer
    return y, land, rope


def street(c, t, scale=1.0, cx=W / 2, gy=1500, shake=True):
    y, land, rope = jump_state(t)
    sh = 34 * math.exp(-land * 11) * scale if shake else 0  # temblor de toda la imagen en cada caída
    c.save(); c.translate(cx, gy + sh); c.scale(scale, scale)
    # suelo
    c.drawRect(skia.Rect.MakeXYWH(-900, 0, 1800, 700), fill(0xFF2A2F3E))
    for i in range(-8, 9):
        c.drawLine(i * 110 - 30, 0, i * 160, 600, stroke(with_alpha(0xFF3A4152, .8), 4))
    # farolas
    for sx in (-1, 1):
        x = sx * 380
        c.drawRect(skia.Rect.MakeXYWH(x - 14, -620, 28, 620), fill(0xFF5A6070))
        c.drawRect(skia.Rect.MakeXYWH(x - 60 * sx - 30, -650, 90, 36), fill(0xFF5A6070))
        K.glow(c, x - 60 * sx + 15, -600, 70, 0xFFFFD27A, .55)
        c.drawCircle(x - 60 * sx + 15, -606, 20, fill(0xFFFFE6A8))
    # cuerda (vista de frente: sube y baja como una elipse proyectada)
    ry = -330 + 330 * rope
    p = skia.Path(); p.moveTo(-370, -330); p.quadTo(0, ry * 2 + 330, 370, -330)
    front = rope > -.2
    if not front:
        c.drawPath(p, stroke(with_alpha(0xFFFF5A3A, .55), 9))
    # caja
    bh = 300
    by = -bh - 360 * y
    sq = 1 + .12 * math.exp(-land * 14)            # se aplasta al caer
    c.save(); c.translate(0, by + bh); c.scale(sq, 1 / sq)
    r = skia.Rect.MakeXYWH(-150, -bh, 300, bh)
    c.drawRect(r, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, -bh), skia.Point(0, 0)], [0xFFE0A15A, 0xFFB0722E]), AntiAlias=True))
    for k in range(1, 4):
        c.drawLine(-150, -bh * k / 4, 150, -bh * k / 4, stroke(with_alpha(0xFF7A4A1A, .6), 6))
    c.drawLine(-150, -bh, 150, 0, stroke(with_alpha(0xFF7A4A1A, .45), 8))
    c.drawRect(r, stroke(0xFF5A3410, 8))
    for ex in (-60, 60):  # ojos
        c.drawCircle(ex, -bh * .62, 26, fill(WHITE)); c.drawCircle(ex, -bh * .62 + 6 * y, 12, fill(INK))
    c.restore()
    # sombra
    c.drawOval(skia.Rect.MakeXYWH(-170 + 50 * y, -14, 340 - 100 * y, 28), fill(with_alpha(0xFF000000, .45 - .25 * y)))
    if front:
        c.drawPath(p, stroke(0xFFFF5A3A, 11))
    # polvo al caer
    if land < .45:
        rs = np.random.RandomState(int(t / PER))
        for _ in range(16):
            a = rs.rand() * math.pi; v = 120 + 260 * rs.rand()
            x = math.cos(a) * v * land * 2.2 * (1 if rs.rand() > .5 else -1); yy = -math.sin(a) * v * land * 1.2 + 300 * land * land
            c.drawCircle(x * 1.2, yy, 10 + 18 * land, fill(with_alpha(0xFFB8B0A0, .55 * (1 - land / .45))))
    c.restore()
    return land


def ear(c, x, y, s, on):
    col = GOLD if on else 0xFF5A6070
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(10, -60); p.cubicTo(70, -70, 80, 10, 30, 30); p.cubicTo(10, 40, 20, 70, -10, 70); p.cubicTo(-40, 70, -40, 40, -30, 20)
    c.drawPath(p, stroke(col, 14))
    q = skia.Path(); q.moveTo(0, -30); q.cubicTo(40, -40, 45, 0, 15, 10); c.drawPath(q, stroke(col, 10))
    if on:
        for k in range(3):
            c.drawArc(skia.Rect.MakeXYWH(-130 - k * 40, -50 - k * 40, 100 + k * 80, 100 + k * 80), 140, 80, False, stroke(with_alpha(GOLD, .8 - .2 * k), 8))
    c.restore()


def s_gif(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)], [0xFF0B1230, 0xFF1A2550, 0xFF2A2F3E]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    rs = np.random.RandomState(4)
    for _ in range(60):
        c.drawCircle(rs.rand() * W, rs.rand() * 900, 1.5 + 2 * rs.rand(), fill(with_alpha(WHITE, .25 + .5 * rs.rand() * (.6 + .4 * math.sin(t * 2 + rs.rand() * 6)))))
    if sid in ("h", "s1", "cta"):
        street(c, t, 1.0, gy=1560)
    elif sid == "s2":
        land = street(c, t, .8, gy=1400)
        if land < .3:
            K.glow(c, W / 2, 1390, 260, GOLD, .5 * (1 - land / .3))
        if lt > 1.2:
            K.tag(c, W / 2, 1640, "EL VÍDEO NO TENÍA SONIDO", lt - 1.2, accent=RED, size=44)
    elif sid == "s3":
        street(c, t, .55, gy=1060)
        for i in range(5):
            on = i == 2
            ear(c, 160 + i * 190, 1420, 1.0, on and lt > 1.2)
        if lt > 1.8:
            hc.big(c, "1 DE CADA 5", W / 2, 1640, 96, GOLD, lt - 1.8, 0.0, outline=10)
    elif sid == "s4":
        land = street(c, t, .7, gy=1300)
        # ondas que 'salen' de la imagen: el temblor que tu cerebro convierte en golpe
        for k in range(3):
            rr = (land * 900 + k * 140)
            if rr < 700:
                c.drawCircle(W / 2, 1290, rr, stroke(with_alpha(GOLD, .5 * (1 - rr / 700)), 8))
        if lt > 1.5:
            K.tag(c, W / 2, 1560, "TIEMBLA LA IMAGEN → TU CEREBRO PONE EL GOLPE", lt - 1.5, accent=GOLD, size=32)
        if lt > 3.0:
            K.tag(c, W / 2, 1660, "FASSNIDGE Y FREEMAN · CORTEX 2018", lt - 3.0, accent=WHITE, size=28)
    # aviso de silencio durante la prueba (s1)
    if sid == "s1" and P["segs"][1]["speech"][1] - P["segs"][1]["a"] < lt:
        a = clamp((lt - (P["segs"][1]["speech"][1] - P["segs"][1]["a"])) / .3)
        K.pill(c, W / 2, 760, "ESCUCHA…", 40, bg=with_alpha(0xFF000000, .6 * a), fg=with_alpha(WHITE, a))


V1901 = dict(slug="1901_video_mudo_que_suena", accent=GOLD, drone=0.02, scene=s_gif, mood="misterio", hush="s1",
             send="ENVÍASELO A VER SI ÉL LO OYE", rehook=("s3", "Y NO ERES EL ÚNICO"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Mira esta caja saltando a la comba. ¿Oyes algo cuando cae al suelo?", cap="¿*OYES* algo cuando cae?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Fíjate bien, porque a partir de ahora este vídeo no tiene ningún sonido.", cap="Ahora: | *CERO sonido*", hold=4.2),
    dict(id="s2", who="nar", cut=True, say="Si has oído un golpe sordo en cada salto, ese golpe lo ha creado tu cerebro.", cap="¿Oíste un *GOLPE*? | Lo creó | *tu cerebro*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="En una encuesta de la Universidad City de Londres, más de una de cada cinco personas oía estos vídeos mudos.",
         cap="Universidad City, Londres: | *1 de cada 5* | lo oye", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Al caer, tiembla toda la imagen, y tu cerebro espera un golpe, así que se lo inventa.", cap="Tiembla la imagen… | y tu cerebro | *pone el ruido*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta sí o no, y envíaselo a un amigo, a ver si también lo escucha.", cap="¿Lo oíste? | Comenta *SÍ* o *NO*"),
])


# ============================ 1902 balanzas (respuesta calculada)
from fractions import Fraction as Fr
L_ = Fr(1)
N_ = (3 * L_ - L_)        # balanza 2: naranja + limón = 3 limones
M_ = 3 * N_               # balanza 1: manzana = 3 naranjas
assert M_ == 3 * N_ and N_ + L_ == 3 * L_
ANSWER = int((M_ + L_) / L_)
WRONG = int(M_ / L_)
assert ANSWER == 7 and WRONG == 6


def balance(c, x, y, left, right, tilt=0.0, t=0.0, s=1.0, qmark=False, hl=None):
    """balanza: left/right listas de 'M','N','L'. tilt en grados (+ baja la derecha)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-16, -10, 32, 230), fill(0xFF8A90A0))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-110, 210, 220, 34), 12, 12), fill(0xFF6A7080))
    c.drawCircle(0, -10, 20, fill(GOLD))
    c.save(); c.rotate(tilt)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-400, -24, 800, 26), 10, 10), fill(0xFFC8CCD8))
    c.restore()
    a = math.radians(tilt)
    for side, items in ((-1, left), (1, right)):
        px, py = side * 380 * math.cos(a), side * 380 * math.sin(a)
        c.drawLine(px, py - 10, px - 120, py + 150, stroke(0xFFAAB0C0, 4)); c.drawLine(px, py - 10, px + 120, py + 150, stroke(0xFFAAB0C0, 4))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(px - 160, py + 150, 320, 26), 13, 13), fill(0xFFE4E7EE))
        n = len(items)
        for i, it in enumerate(items):
            cols = min(n, 3); row = i // 3; col = i % 3
            nn = min(3, n - row * 3)
            fx = px + (col - (nn - 1) / 2) * 100
            fy = py + 108 - row * 92
            if hl and it == hl:
                c.drawCircle(fx, fy, 62, fill(with_alpha(GOLD, .3 + .1 * math.sin(t * 8))))
            fruit(c, it, fx, fy, .78, t)
        if qmark and side == 1:
            draw_text(c, "?", px, py + 120, 150, GOLD, shadow=True)
    c.restore()


def s_bal(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1150), 1050 + 30 * math.sin(t), [0xFF3A2A5A, 0xFF22183A, 0xFF0E0A1C], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    wob = lambda k: 1.2 * math.sin(t * 1.3 + k)
    hl = "L" if sid == "s2" else None
    # balanza 1 y 2 (en equilibrio)
    balance(c, W / 2, 750, ["M"], ["N", "N", "N"], tilt=wob(0) * .5, t=t, s=.7)
    b2r = ["L", "L", "L"]; b2l = ["N", "L"]
    if sid == "s2" and lt > 1.6:  # quita un limón de cada lado
        k = clamp((lt - 1.6) / 1.0)
        b2l = ["N"] if k > .5 else b2l; b2r = ["L", "L"] if k > .5 else b2r
    balance(c, W / 2, 1050, b2l, b2r, tilt=wob(1) * .5, t=t, s=.7, hl=hl)
    # balanza de la pregunta
    if sid in ("s4", "cta"):
        right, q, tl = ["L"] * ANSWER, False, 0.0
    elif sid == "s3":
        n = min(6, int(lt / max(.3, (d - 1.0) / 6)) + 0)
        right, q, tl = ["L"] * n, n < 6, -8 * (1 - n / 7)
    else:
        right, q, tl = [], True, -10 + wob(2)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(60, 1290, W - 120, 470), 34, 34), stroke(with_alpha(GOLD, .5 + .3 * math.sin(t * 4)), 6))
    balance(c, W / 2, 1400, ["M", "L"], right, tilt=tl, t=t, s=.78, qmark=q, hl="L" if sid == "s3" and lt > d - 1.2 else None)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1840, 110, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > 2.8:
        K.tag(c, W / 2, 1840, "NARANJA = 2 LIMONES", lt - 2.8, accent=GOLD, size=48)
    if sid == "s3" and lt > .8:
        K.tag(c, W / 2, 1840, "3 NARANJAS × 2 = 6 LIMONES… + 1", lt - .8, accent=WHITE, size=42)
    if sid == "s4":
        hc.big(c, f"{WRONG}", W / 2 - 200, 1850, 110, RED, lt, 0.0, outline=10)
        c.drawLine(W / 2 - 260, 1880, W / 2 - 140, 1790, stroke(RED, 14))
        hc.big(c, f"{ANSWER}", W / 2 + 200, 1850, 130, GREEN, lt, .5, outline=12)


V1902 = dict(slug="1902_balanzas_limones", accent=GOLD, drone=0.02, scene=s_bal, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Mira las dos balanzas de arriba. ¿Cuántos limones hacen falta en la última?", cap="¿Cuántos *LIMONES* hacen falta?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Una manzana pesa como tres naranjas, y una naranja con un limón, como tres limones. Cinco segundos.",
         cap="*5 segundos*. | ¿Cuántos limones?", hold=3.8),
    dict(id="s2", who="nar", cut=True, say="La trampa está en la segunda balanza, porque si quitas un limón de cada lado, la naranja vale dos.",
         cap="Quita un limón | de *cada lado*: | naranja = *2 limones*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Así que la manzana vale seis limones, más el limón que ya estaba en el plato.",
         cap="Manzana = *6 limones*… | y *el limón del plato*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="La respuesta es siete limones, y no seis, como dice casi todo el mundo.", cap="Son *7*, | no *6*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta qué número te salió, y envíaselo a quien crea que lo saca a la primera.", cap="¿Qué te salió? | *COMENTA*"),
])

VIDEOS = {"1901": V1901, "1902": V1902}


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
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        K.run(VIDEOS[k], make_scene(VIDEOS[k]), OUT, preview=pv)
