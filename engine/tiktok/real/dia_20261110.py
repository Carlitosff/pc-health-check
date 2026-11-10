"""Producción 10/11/2026 (1801 y 1802, motor 2D; 1803 mito_rayo.py y 1804 serie_giro.py en 3D, 1809 ciudad3d).
  1801 PRUEBA CON TU CUERPO: el agujero en la mano. American Academy of Ophthalmology, 'Experiment: Hole In Your Hand' (14/09/2017): tubo en la mano
       izquierda delante del ojo izquierdo, los dos ojos abiertos mirando algo lejano, la mano derecha abierta delante del ojo derecho, con el borde pegado
       al tubo. 'The tube allows you to look into the distance with your left eye and to see your hand with your right eye': el cerebro junta las dos.
  1802 RETO: frutas que suman (manzana, naranja, limón). La respuesta se calcula con la precedencia de Python (assert 42; el error típico, 48)."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, paisaje
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80
SK = (0xFFF0C09A, 0xFFC98A62, 0xFFA8693F)


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 1801 agujero en la mano
_SKY = None


def sky():
    global _SKY
    if _SKY is None:
        _SKY = paisaje.to_image(paisaje.sunset(960, 960))
    return _SKY


def shade(x0, x1):
    return skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x1, 0)], [SK[2], SK[0], SK[0], SK[1]], [0, .3, .65, 1]), AntiAlias=True)


def finger(c, bx, by, L, w, ang):
    c.save(); c.translate(bx, by); c.rotate(ang)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -L, w, L + 50), w / 2, w / 2)
    c.drawRRect(rr, shade(-w / 2, w / 2)); c.drawRRect(rr, stroke(with_alpha(0xFF2A1408, .3), 3))
    for f in (.33, .6):
        c.drawLine(-w * .3, -L * f, w * .3, -L * f, stroke(with_alpha(SK[2], .5), 3))
    c.restore()


def palm(c, x, y, s, hole=0.0, t=0.0, sway=0.0):
    """mano derecha abierta vista por la palma (desde tus ojos). hole 0..1: radio del agujero con el cielo dentro."""
    c.save(); c.translate(x, y); c.rotate(sway); c.scale(s, s)
    arm = skia.Path(); arm.moveTo(-120, 260); arm.lineTo(120, 260); arm.lineTo(170, 900); arm.lineTo(-170, 900); arm.close()
    c.drawPath(arm, shade(-170, 170))
    for L, dx, a in ((300, -105, -9), (350, -36, -3), (340, 36, 3), (280, 102, 10)):
        finger(c, dx, -150, L, 72, a)
    finger(c, 165, 60, 230, 84, 48)  # pulgar
    pr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-150, -200, 300, 470), 120, 120)
    c.drawRRect(pr, shade(-150, 150))
    for (a, b, cx_, cy_) in ((-120, 40, -20, 10), (-90, 90, 10, 90)):
        p = skia.Path(); p.moveTo(a, cy_ - 40); p.quadTo(cx_, cy_ + 30, b, cy_ - 60)
        c.drawPath(p, stroke(with_alpha(SK[2], .55), 5))
    if hole > 0:
        r = 128 * hole
        cl = skia.Path(); cl.addCircle(0, 20, r)
        c.save(); c.clipPath(cl, doAntiAlias=True)
        c.drawImageRect(sky(), skia.Rect.MakeXYWH(-260 + 30 * math.sin(t * .4), -230, 520, 520))
        c.restore()
        c.drawCircle(0, 20, r, stroke(with_alpha(0xFF3A1A08, .55), 10))
        c.drawCircle(0, 20, r + 9, stroke(with_alpha(SK[1], .7), 8))
    c.restore()


def tube(c, x, y, L, w, ang, roll=1.0):
    """folio enrollado: roll 0 = hoja plana, 1 = tubo."""
    c.save(); c.translate(x, y); c.rotate(ang)
    ww = lerp(w * 3.1, w, ease_out(roll))
    c.drawRect(skia.Rect.MakeXYWH(-ww / 2, -L, ww, L), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(-ww / 2, 0), skia.Point(ww / 2, 0)], [0xFFB8BCC8, 0xFFFFFFFF, 0xFFE4E7EE, 0xFF9EA3B2], [0, .35, .6, 1]), AntiAlias=True))
    for k in range(1, 9):
        c.drawLine(-ww / 2, -L * k / 9, ww / 2, -L * k / 9, stroke(with_alpha(0xFF8FA6D8, .35 * (1 - roll)), 2))
    if roll > .6:
        e = skia.Rect.MakeXYWH(-ww / 2, -L - ww * .14, ww, ww * .28)
        c.drawOval(e, fill(0xFF2A2E3A)); c.drawOval(e, stroke(WHITE, 5))
    c.restore()


def head_top(c, x, y, t, tube_k, hand_k):
    """esquema cenital: cabeza vista desde arriba, ojos, tubo en el ojo izquierdo y mano derecha delante del derecho."""
    c.drawOval(skia.Rect.MakeXYWH(x - 190, y - 150, 380, 330), fill(0xFF3A2A22))
    c.drawOval(skia.Rect.MakeXYWH(x - 170, y - 160, 340, 300), fill(0xFFE3B08A))
    c.drawOval(skia.Rect.MakeXYWH(x - 26, y - 200, 52, 70), fill(0xFFD49C76))  # nariz
    for sx in (-1, 1):
        c.drawCircle(x + sx * 82, y - 118, 30, fill(WHITE)); c.drawCircle(x + sx * 82, y - 128, 14, fill(0xFF2B4E7A))
    draw_text(c, "IZQ", x - 82, y + 20, 40, INK, shadow=False); draw_text(c, "DCHA", x + 82, y + 20, 40, INK, shadow=False)
    if tube_k > 0:
        L = 620 * ease_out(tube_k)
        c.drawRect(skia.Rect.MakeXYWH(x - 82 - 48, y - 150 - L, 96, L), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(x - 130, 0), skia.Point(x - 34, 0)], [0xFFB8BCC8, 0xFFFFFFFF, 0xFF9EA3B2]), AntiAlias=True))
        # lo que ve el ojo izquierdo: lejos
        for i in range(3):
            yy = y - 160 - L - 40 - ((t * 140 + i * 90) % 270)
            c.drawCircle(x - 82, yy, 10, fill(with_alpha(CYAN, .8)))
    if hand_k > 0:
        hy = y - 150 - 300 * hand_k
        hx = x + 82 + 260 * (1 - ease_out(hand_k))
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(hx - 150, hy - 34, 280, 68), 34, 34)
        c.drawRRect(r, fill(0xFFF0C09A)); c.drawRRect(r, stroke(0xFFA8693F, 4))
        if hand_k > .95:
            c.drawLine(x + 82, y - 150, x + 82, hy + 26, stroke(with_alpha(GOLD, .9), 8))


def room(c, t):
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1100), 980 + 40 * math.sin(t * .8), [0xFF2E3C6A, 0xFF1A2040, 0xFF0D0F1E], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    rs = np.random.RandomState(5)
    for _ in range(40):
        x = (rs.rand() * W + t * (6 + 20 * rs.rand())) % W; y = (rs.rand() * H - t * (10 + 30 * rs.rand())) % H
        c.drawCircle(x, y, 2 + 5 * rs.rand(), fill(with_alpha(0xFFFFE0C0, .05 + .12 * rs.rand())))


def s_hole(c, t, P, V):
    sid, lt, d = seg(P, t)
    room(c, t)
    if sid == "h":
        palm(c, W / 2, 1180, 1.25 + .05 * math.sin(t * 1.2), hole=1.0, t=t, sway=1.5 * math.sin(t * .9))
    elif sid == "s1":
        k = clamp((lt - .4) / 2.2)
        tube(c, W / 2, 1520, 760, 210, 6 * math.sin(t * .7), roll=k)
        if k >= 1:
            K.tag(c, W / 2, 1720, "UN FOLIO ENROLLADO", lt - 2.6, accent=GOLD, size=44)
    elif sid in ("s2", "s3"):
        head_top(c, W / 2, 1600, t, 1.0 if sid == "s3" else clamp(lt / 1.2), clamp((lt - .3) / 1.6) if sid == "s3" else 0)
        lab = "TUBO EN EL OJO IZQUIERDO · LOS DOS ABIERTOS" if sid == "s2" else "MANO DERECHA PEGADA AL TUBO"
        K.tag(c, W / 2, 1860, lab, lt - .5, accent=GOLD, size=34)
    elif sid == "s4":
        # lo que ve cada ojo, por separado, y luego juntos
        m = K.smooth((lt - 1.2) / 1.8)
        ox = 250 * (1 - m)
        c.save(); c.translate(-ox, 0)
        cl = skia.Path(); cl.addCircle(W / 2, 1150, 160)
        c.save(); c.clipPath(cl, doAntiAlias=True); c.drawImageRect(sky(), skia.Rect.MakeXYWH(W / 2 - 300, 850, 600, 600)); c.restore()
        c.drawCircle(W / 2, 1150, 160, stroke(WHITE, 8))
        c.restore()
        c.saveLayerAlpha(None, int(255 * (1 - .9 * m)))
        palm(c, W / 2 + ox, 1130, 1.0, hole=0, t=t)
        c.restore()
        if m > 0:
            c.saveLayerAlpha(None, int(255 * m))
            palm(c, W / 2, 1130, 1.0 + .1 * m, hole=1.0, t=t)
            c.restore()
        if m < .3:
            draw_text(c, "OJO IZQ.", W / 2 - 250, 1400, 46, CYAN, shadow=True); draw_text(c, "OJO DCHO.", W / 2 + 250, 1720, 46, GOLD, shadow=True)
        if lt > 3.2:
            K.tag(c, W / 2, 1810, "TU CEREBRO JUNTA LAS DOS", lt - 3.2, accent=GREEN, size=44)
    else:
        palm(c, W / 2, 1180, 1.15, hole=1.0, t=t, sway=1.2 * math.sin(t * .9))


V1801 = dict(slug="1801_agujero_en_la_mano", accent=GOLD, drone=0.02, scene=s_hole, mood="misterio",
             send="ENVÍASELO A ALGUIEN CON UN FOLIO", rehook=("s3", "AHORA VIENE LO RARO"), reveal=("s4", "EL AGUJERO"), segs=[
    dict(id="h", who="nar", say="¿Quieres ver un agujero en tu propia mano? Solo necesitas un folio.", cap="¿Ves un *AGUJERO* en tu mano?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Enrolla el folio hasta que quede como un tubo, del grosor de un rollo de papel.", cap="Enrolla *un folio* | como un *tubo*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Ponlo delante de tu ojo izquierdo y mira algo lejano, con los dos ojos bien abiertos.", cap="Tubo en el *ojo izquierdo*, | los *dos abiertos*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Ahora pon la mano derecha abierta delante del otro ojo, con el borde pegado al tubo.", cap="Mano derecha | *pegada al tubo*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Y aparece un agujero en tu mano, porque cada ojo ve una cosa distinta y tu cerebro las junta en una sola.", cap="Cada ojo ve *una cosa*… | y tu cerebro | las *JUNTA*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta sí si te ha salido el agujero, y envíaselo a alguien para que lo pruebe ahora mismo.", cap="¿Te salió? | Comenta *SÍ* o *NO*"),
])


# ============================ 1802 frutas que suman (respuesta calculada)
M, N_, L_ = 10, 4, 2
ROWS = [("MMM", "+", 30), ("MNN", "+", 18), ("NL", "-", 2)]
for fr, op, res in ROWS:
    val = {"M": M, "N": N_, "L": L_}
    s_ = val[fr[0]]
    for f in fr[1:]:
        s_ = s_ + val[f] if op == "+" else s_ - val[f]
    assert s_ == res, (fr, s_, res)
ANSWER = L_ + M * N_
WRONG = (L_ + M) * N_
assert ANSWER == 42 and WRONG == 48


def fruit(c, kind, x, y, s, t=0.0):
    c.save(); c.translate(x, y + 4 * math.sin(t * 2 + x * .01)); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-56, 48, 112, 22), fill(with_alpha(0xFF000000, .3)))
    if kind == "M":
        p = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(-18, -18), 80, [0xFFFF7A7A, 0xFFE0242C, 0xFF8E0E16]), AntiAlias=True)
        c.drawCircle(-20, 4, 50, p); c.drawCircle(20, 4, 50, p)
        c.drawLine(0, -40, 6, -72, stroke(0xFF5A3A1A, 9))
        lf = skia.Path(); lf.moveTo(6, -62); lf.quadTo(40, -96, 56, -62); lf.quadTo(30, -50, 6, -62); c.drawPath(lf, fill(0xFF3FBF4A))
    elif kind == "N":
        p = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(-16, -16), 80, [0xFFFFC266, 0xFFFF8A00, 0xFFB65A00]), AntiAlias=True)
        c.drawCircle(0, 0, 58, p)
        rs = np.random.RandomState(3)
        for _ in range(16):
            a, r = rs.rand() * 6.28, rs.rand() * 46
            c.drawCircle(math.cos(a) * r, math.sin(a) * r, 2.5, fill(with_alpha(0xFF8A4200, .5)))
        c.drawCircle(0, -54, 7, fill(0xFF3F7A2A))
    else:
        p = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(-14, -12), 80, [0xFFFFF7A0, 0xFFFFE01A, 0xFFC9A600]), AntiAlias=True)
        c.drawOval(skia.Rect.MakeXYWH(-66, -42, 132, 84), p)
        c.drawCircle(-66, 0, 10, p); c.drawCircle(66, 0, 10, p)
    c.restore()


def eq_row(c, items, y, t, appear, res=None, res_col=WHITE, hl=None):
    """items: lista de 'M','N','L' u operadores. appear 0..1"""
    n = len(items) + 2
    gap = 960 / n
    x0 = 60 + gap / 2
    for i, it in enumerate(items):
        k = clamp(appear * n - i)
        if k <= 0:
            continue
        x = x0 + i * gap
        sc = .85 * (1 + .25 * math.exp(-k * 4) * math.sin(k * 12)) * min(1, k * 2)
        if it in "MNL":
            if hl == it:
                c.drawCircle(x, y, 78, fill(with_alpha(GOLD, .28 + .1 * math.sin(t * 8))))
            fruit(c, it, x, y, sc, t)
        else:
            draw_text(c, it, x, y + 30, 92 * min(1, k * 2), WHITE, shadow=True)
    k = clamp(appear * n - len(items))
    if k > 0 and res is not None:
        draw_text(c, "=", x0 + len(items) * gap, y + 30, 92, WHITE, shadow=True)
        draw_text(c, str(res), x0 + (len(items) + 1) * gap - 10, y + 32, 96, res_col, shadow=True)


def s_frutas(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1100), 1000 + 30 * math.sin(t), [0xFF1F4A3A, 0xFF12291F, 0xFF081410], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    # pizarra
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(40, 690, W - 80, 960), 40, 40), fill(with_alpha(0xFF000000, .28)))
    tl = P["tl"]; T = t
    ys = [790, 990, 1190]
    for i, (fr, op, res) in enumerate(ROWS):
        items = []
        for j, f in enumerate(fr):
            if j:
                items.append(op)
            items.append(f)
        app = 1.0
        hl = None
        if sid == "s3":
            hl = "N" if i == 1 and lt < 2.4 else ("L" if i == 2 and lt >= 2.4 else None)
        eq_row(c, items, ys[i], T, app, res=res, hl=hl)
    # fila de la pregunta: limón + manzana × naranja
    app = 1.0
    if sid in ("s4", "cta"):
        res, col = ANSWER, GREEN
    else:
        res, col = "?", GOLD
    y4 = 1450
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(70, y4 - 110, W - 140, 210), 34, 34), stroke(with_alpha(GOLD, .5 + .3 * math.sin(t * 4)), 6))
    eq_row(c, ["L", "+", "M", "×", "N"], y4, T, app, res=res, res_col=col)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1800, 120, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > .6:
        K.tag(c, W / 2, 1790, "PRIMERO SE MULTIPLICA", lt - .6, accent=GOLD, size=48)
    if sid == "s3":
        if lt > 3.4:
            K.tag(c, W / 2, 1760, f"{L_} + {M} × {N_} = {L_} + {M * N_}", lt - 3.4, accent=WHITE, size=50)
    if sid == "s4":
        hc.big(c, f"{WRONG}", W / 2 - 200, 1790, 110, RED, lt, 0.0, outline=10)
        c.drawLine(W / 2 - 290, 1820, W / 2 - 110, 1740, stroke(RED, 14))
        hc.big(c, f"{ANSWER}", W / 2 + 200, 1790, 130, GREEN, lt, .5, outline=12)


V1802 = dict(slug="1802_frutas_que_suman", accent=GOLD, drone=0.02, scene=s_frutas, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", rehook=("s2", "AQUÍ ESTÁ LA TRAMPA"), reveal=("s3", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Mira bien la pizarra de frutas. ¿Sabes cuánto da la última línea?", cap="¿Cuánto da la *ÚLTIMA* línea?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Con la manzana sacas la naranja, y con la naranja el limón. Tienes cinco segundos.", cap="*5 segundos*. | ¿Cuánto da?", hold=4.2),
    dict(id="s2", who="nar", cut=True, say="Ojo con la trampa, porque en la última línea la multiplicación va antes que la suma.", cap="La *multiplicación* | va *ANTES*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="La manzana vale diez, la naranja cuatro y el limón dos, así que queda dos más cuarenta.", cap="Manzana *10*, | naranja *4*, | limón *2*", hold=0.5),
    dict(id="s4", who="nar", cut=True, say="El resultado es cuarenta y dos, y no cuarenta y ocho, que es lo que sale si sumas primero.", cap="Son *42*, | no *48*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta qué número te salió, y envíaselo a quien crea que lo saca a la primera.", cap="¿Qué te salió? | *COMENTA*"),
])

VIDEOS = {"1801": V1801, "1802": V1802}


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
