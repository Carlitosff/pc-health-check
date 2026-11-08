"""Producción 08/11/2026 (1601 y 1603, motor actual; 1602 reto_plegado.py y 1604 serie_anillos.py en 3D, 1609 ciudad3d).
  1601 PRUEBA EN DIRECTO: ceguera inducida por movimiento (Bonneh, Cooperman y Sagi, Nature 411, 2001; versión de cruces azules de Michael Bach 2002).
       Tras ~10 s mirando el centro, 'uno o más puntos desaparecen' (Wikipedia, Motion-induced blindness). Los puntos amarillos NO se mueven nunca.
  1603 MITO CON 'TÚ': el azúcar no pone hiperactivo. Live Science (15/08/2016): estudio de 1994 (Journal of Abnormal Child Psychology), 35 niños de 5–7 años,
       bebida con aspartamo; a la mitad de las madres les dijeron 'azúcar' → los vieron más hiperactivos, se quedaban más cerca y los criticaban más (vídeo).
       Wolraich et al., JAMA 1995: revisión de 16 estudios, el azúcar no afecta al comportamiento ni al rendimiento cognitivo."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80; YEL = 0xFFFFE600; BLUE = 0xFF2F5BFF; PINK = 0xFFFF5FA8


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 1601 ceguera inducida por movimiento
MX, MY = W / 2, 1080           # centro de fijación (quieto siempre)
DOTS = [(MX - 250, MY - 230), (MX + 250, MY - 230), (MX, MY + 300)]  # los 3 amarillos: fijos todo el vídeo
GRID = [(i, j) for i in range(-7, 8) for j in range(-7, 8) if (i, j) != (0, 0)]


def s_mib(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.clear(0xFF000000)
    # rejilla de cruces azules que gira alrededor del centro (lo único que se mueve)
    ang = t * 0.9 * (1 if t > .0 else 0)
    ca, sa = math.cos(ang), math.sin(ang)
    sp = 92
    p = stroke(BLUE, 10)
    for i, j in GRID:
        x0, y0 = i * sp, j * sp
        if x0 * x0 + y0 * y0 > 640 * 640:
            continue
        x, y = MX + x0 * ca - y0 * sa, MY + x0 * sa + y0 * ca
        c.drawLine(x - 17, y, x + 17, y, p); c.drawLine(x, y - 17, x, y + 17, p)
    # los 3 puntos amarillos: tamaño y posición constantes
    for (x, y) in DOTS:
        c.drawCircle(x, y, 22, fill(YEL))
    # punto de fijación verde que parpadea (como en la versión de Bach)
    on = (int(t * 2.5) % 2) == 0
    c.drawCircle(MX, MY, 15, fill(GREEN if on else 0xFF1E7A3E))
    # rótulos solo fuera del círculo de la ilusión
    if sid == "s1" and lt > .8:
        K.tag(c, W / 2, 1790, "3 PUNTOS QUE NO SE MUEVEN", lt - .8, accent=GOLD, size=42)
    if sid == "s2":
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"AGUANTA {n}", W / 2, 1800, 84, WHITE, 1.0, 0.0, outline=10)
    if sid == "s4" and lt > .6:
        K.tag(c, W / 2, 1790, "BONNEH, COOPERMAN Y SAGI · NATURE 2001", lt - .6, accent=GOLD, size=34)


V1601 = dict(slug="1601_ceguera_movimiento", accent=GOLD, drone=0.012, scene=s_mib, mood="misterio", steady=True, music=0.03,
             send="ENVÍASELO: ¿A ÉL TAMBIÉN SE LE BORRAN?", rehook=("s3", "NO MUEVAS LOS OJOS"), reveal=("s4", "QUÉ HA PASADO"), segs=[
    dict(id="h", who="nar", say="Mira el punto verde del centro, sin mover los ojos. ¿Cuántos puntos amarillos ves?", cap="Mira el punto *VERDE*: ¿cuántos *AMARILLOS* ves?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Hay tres, y no se mueven en ningún momento. Tú sigue mirando el centro.", cap="Hay *tres*, | y *no se mueven*. | Mira solo *el centro*", hold=0.6),
    dict(id="s2", who="nar", cut=True, say="Aguanta unos segundos, sin mover los ojos.", cap="Aguanta | *sin mover los ojos*…", hold=3.6),
    dict(id="s3", who="nar", cut=True, say="Te parecerá que uno se apaga, o dos, o los tres, aunque siguen ahí todo el rato.", cap="Uno *se apaga*… | o dos… | o *los tres*", hold=0.8),
    dict(id="s4", who="nar", cut=True, say="Se llama ceguera inducida por movimiento, y salió en la revista Nature en dos mil uno.", cap="*Ceguera inducida* | por *movimiento*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta cuántos se te borraron, uno, dos o tres, y envíaselo a alguien, a ver si le pasa.", cap="¿Cuántos se te borraron? | *1, 2 o 3*: comenta"),
])


# ============================ 1603 mito del azúcar
def sugar_cube(c, x, y, s, rot=0.0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    top = skia.Path(); top.moveTo(0, -40); top.lineTo(46, -17); top.lineTo(0, 6); top.lineTo(-46, -17); top.close()
    lf = skia.Path(); lf.moveTo(-46, -17); lf.lineTo(0, 6); lf.lineTo(0, 56); lf.lineTo(-46, 33); lf.close()
    rf = skia.Path(); rf.moveTo(46, -17); rf.lineTo(0, 6); rf.lineTo(0, 56); rf.lineTo(46, 33); rf.close()
    c.drawPath(top, fill(with_alpha(0xFFFFFFFF, a))); c.drawPath(lf, fill(with_alpha(0xFFE3E7F0, a))); c.drawPath(rf, fill(with_alpha(0xFFC9CFDD, a)))
    rs = np.random.RandomState(int(abs(x * 7 + y)) % 999)
    for _ in range(14):
        c.drawCircle(rs.uniform(-30, 30), rs.uniform(-25, 40), 2.4, fill(with_alpha(0xFFB8BFD0, .7 * a)))
    c.restore()


def gauge(c, x, y, r, val, t, label):
    """velocímetro 'NIVEL DE NERVIOS' (val 0..1)"""
    c.drawCircle(x, y + 8, r + 26, fill(with_alpha(0xFF000000, .45)))
    c.drawCircle(x, y, r + 22, fill(0xFF1C2033)); c.drawCircle(x, y, r + 22, stroke(0xFF3A4060, 6))
    for k in range(41):
        a = math.radians(-210 + 240 * k / 40)
        col = GREEN if k < 18 else (GOLD if k < 30 else RED)
        L = 34 if k % 5 == 0 else 16
        c.drawLine(x + math.cos(a) * r, y + math.sin(a) * r, x + math.cos(a) * (r - L), y + math.sin(a) * (r - L), stroke(col, 9 if k % 5 == 0 else 5))
    v = clamp(val + .015 * math.sin(t * 23) * (val > .6))
    a = math.radians(-210 + 240 * v)
    pn = stroke(WHITE, 14); pn.setStrokeCap(skia.Paint.kRound_Cap)
    c.drawLine(x, y, x + math.cos(a) * (r - 40), y + math.sin(a) * (r - 40), pn)
    c.drawCircle(x, y, 26, fill(RED)); c.drawCircle(x, y, 10, fill(WHITE))
    draw_text(c, label, x, y + r * .62, 40, with_alpha(WHITE, .85), shadow=False)


def drink(c, x, y, s, t, lbl, lbl_col):
    c.save(); c.translate(x, y); c.scale(s, s)
    g = skia.Path(); g.moveTo(-90, -170); g.lineTo(90, -170); g.lineTo(70, 170); g.lineTo(-70, 170); g.close()
    c.save(); c.clipPath(g, doAntiAlias=True)
    lv = -110 + 6 * math.sin(t * 2.2)
    c.drawRect(skia.Rect.MakeLTRB(-100, lv, 100, 180), fill(0xFFE8572C))
    rs = np.random.RandomState(4)
    for i in range(18):
        bx = rs.uniform(-60, 60); by = 170 - ((t * (40 + 50 * rs.rand()) + rs.rand() * 300) % 280)
        c.drawCircle(bx, by, 4 + 4 * rs.rand(), fill(with_alpha(WHITE, .45)))
    c.restore()
    c.drawPath(g, stroke(with_alpha(WHITE, .8), 8))
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-155, 20, 310, 80), 16, 16)
    c.drawRRect(r, fill(lbl_col)); c.drawRRect(r, stroke(WHITE, 5))
    draw_text(c, lbl, 0, 75, 42, INK if lbl_col != RED else WHITE, shadow=False)
    c.restore()


def stamp(c, x, y, txt, col, k, rot=-8):
    if k <= 0:
        return
    s = 1.6 - .6 * ease_out(clamp(k))
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    fs_ = 70 if len(txt) <= 12 else 50
    w = 70 + (46 if len(txt) <= 12 else 33) * len(txt)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -62, w, 112), 14, 14)
    c.drawRRect(r, stroke(with_alpha(col, clamp(k * 3)), 12))
    draw_text(c, txt, 0, 18 if fs_ < 70 else 22, fs_, with_alpha(col, clamp(k * 3)), shadow=False)
    c.restore()


def rec_frame(c, t, x0, y0, x1, y1):
    L = 70; p = stroke(WHITE, 8)
    for (x, y, dx, dy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        c.drawLine(x, y, x + dx * L, y, p); c.drawLine(x, y, x, y + dy * L, p)
    if int(t * 2) % 2 == 0:
        c.drawCircle(x0 + 50, y0 + 60, 16, fill(RED))
    draw_text(c, "REC 1994", x0 + 170, y0 + 76, 40, WHITE, shadow=False)


def kid(c, x, y, s, t, jitter, glow_col=None):
    """niño visto como silueta a contraluz con aura (sin monigote de palo: volumen y relleno)"""
    jx = math.sin(t * 31) * jitter * 14; jy = abs(math.sin(t * 17)) * jitter * -18
    c.save(); c.translate(x + jx, y + jy); c.scale(s, s)
    if glow_col:
        c.drawCircle(0, -40, 230, skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(0, -40), 230, [with_alpha(glow_col, .5), with_alpha(glow_col, 0)], [0, 1])))
    body = skia.Path(); body.moveTo(-70, 160); body.cubicTo(-80, 40, -60, -20, 0, -20); body.cubicTo(60, -20, 80, 40, 70, 160); body.close()
    c.drawPath(body, fill(0xFF0D1020))
    c.drawCircle(0, -80, 62, fill(0xFF0D1020))
    a = math.sin(t * 9) * jitter * .6
    for sx in (-1, 1):
        c.save(); c.translate(sx * 60, 10); c.rotate(math.degrees(sx * (.35 + a)))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-16, 0, 32, 120), 16, 16), fill(0xFF0D1020)); c.restore()
    c.restore()


def bars(c, x, y, w, val_a, val_b, k, t):
    for i, (lab, v, col) in enumerate((("LES DIJERON 'AZÚCAR'", val_a, RED), ("NO LES DIJERON NADA", val_b, CYAN))):
        yy = y + i * 150
        draw_text(c, lab, x + w / 2, yy - 18, 40, WHITE, shadow=False)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, yy, w, 54), 27, 27), fill(with_alpha(0xFFFFFFFF, .15)))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, yy, max(54, w * v * ease_out(clamp(k))), 54), 27, 27), fill(col))


def s_azucar(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.clear(0xFF1A1030)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1100), 1100 + 40 * math.sin(t), [0xFF4A2A6E, 0xFF231538, 0xFF0C0816], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    # lluvia de terrones al fondo (siempre en movimiento)
    rs = np.random.RandomState(8)
    for i in range(16):
        x = rs.uniform(60, W - 60); sp = 140 + 160 * rs.rand(); y = (rs.rand() * 2400 + t * sp) % 2300 - 200
        sugar_cube(c, x, y, .5 + .4 * rs.rand(), rot=t * 40 * (rs.rand() - .5), a=.25)
    if sid == "h":
        val = .25 + .7 * ease_out(clamp(lt / 1.6))
        gauge(c, W / 2, 1180, 300, val, t, "NIVEL DE NERVIOS")
        sugar_cube(c, W / 2, 1600 + 10 * math.sin(t * 3), 1.6, rot=math.sin(t * 2) * 8)
    elif sid == "s1":
        drink(c, W / 2 - 210, 1190, 1.15, t, "¿AZÚCAR?", GOLD)
        drink(c, W / 2 + 210, 1190, 1.15, t + 1, "¿AZÚCAR?", GOLD)
        k = (lt - d * .55) / .5
        stamp(c, W / 2, 1600, "SIN AZÚCAR", RED, k)
        if lt > d * .55:
            K.tag(c, W / 2, 1760, "SOLO EDULCORANTE (ASPARTAMO)", lt - d * .55 - .3, accent=WHITE, size=38)
    elif sid == "s2":
        rec_frame(c, t, 90, 780, W - 90, 1700)
        kid(c, W / 2 - 220, 1300, 1.25, t, 0.08, glow_col=RED)
        kid(c, W / 2 + 220, 1300, 1.25, t + .5, 0.08, glow_col=CYAN)
        draw_text(c, "'AZÚCAR'", W / 2 - 220, 1590, 52, RED, shadow=False)
        draw_text(c, "NADA", W / 2 + 220, 1590, 52, CYAN, shadow=False)
        if lt > d * .45:
            K.tag(c, W / 2, 1640, "MISMA BEBIDA · MÁS RIÑAS", lt - d * .45, accent=RED, size=40)
    elif sid == "s3":
        # 16 estudios que se apilan y se sellan
        n = min(16, int(lt / max(.1, d * .6) * 16) + 1)
        for i in range(n):
            col_ = i % 4; row = i // 4
            x = 210 + col_ * 220; y = 930 + row * 190
            pop = ease_out(clamp((lt - i * d * .6 / 16) / .25))
            c.save(); c.translate(x, y); c.scale(pop * 1.2, pop * 1.2); c.rotate((i % 3 - 1) * 3)
            r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-75, -70, 150, 140), 10, 10)
            c.drawRRect(r, fill(0xFFF4F1EA)); c.drawRRect(r, stroke(0xFF2A2440, 4))
            for L in range(4):
                c.drawLine(-50, -40 + L * 22, 50 - (L == 3) * 40, -40 + L * 22, stroke(0xFF9A96A8, 6))
            draw_text(c, "= 0", 0, 58, 40, 0xFF1B8A4B, shadow=False)
            c.restore()
        if lt > d * .62:
            stamp(c, W / 2, 1720, "16 ESTUDIOS: SIN EFECTO", GREEN, (lt - d * .62) / .45, rot=-4)
    elif sid == "s4":
        val = .85 - .62 * ease_out(clamp(lt / 1.4))
        gauge(c, W / 2, 1150, 300, val, t, "NIVEL DE NERVIOS")
        if lt > 1.0:
            K.tag(c, W / 2, 1600, "WOLRAICH ET AL. · JAMA · 1995", lt - 1.0, accent=GOLD, size=40)
    else:
        sugar_cube(c, W / 2, 1220 + 14 * math.sin(t * 3), 2.4, rot=math.sin(t * 1.5) * 10)
    K.vignette(c, .35)


V1603 = dict(slug="1603_mito_azucar", accent=GOLD, drone=0.02, scene=s_azucar, mood="misterio",
             send="ENVÍASELO A QUIEN TE QUITABA LOS CARAMELOS", rehook=("s2", "ESPERA… MIRA QUÉ HICIERON LAS MADRES"), reveal=("s3", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿El azúcar te pone como una moto? Te lo contaron mal, y un experimento lo demuestra.", cap="¿El azúcar te pone *COMO UNA MOTO*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="En mil novecientos noventa y cuatro, a unas madres les dijeron que sus hijos habían tomado azúcar. Era mentira, solo llevaba edulcorante.", cap="Les dijeron: *mucho azúcar*. | Era mentira: | *solo edulcorante*", hold=0.4),
    dict(id="s2", who="nar", cut=True, say="Aun así, los vieron mucho más nerviosos, y en los vídeos les regañaban más.", cap="Los vieron *más nerviosos*… | y les *regañaban más*", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Al año siguiente, dieciséis estudios revisados en la revista JAMA no vieron que el azúcar cambie cómo se portan los niños.", cap="*16 estudios*: | el azúcar | *NO* los altera", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="No cambiaba el niño, cambiaba cómo lo miraban los mayores.", cap="No cambiaba *el niño*. | Cambiaba *cómo lo miraban*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Envíaselo a quien te quitaba los caramelos, y comenta quién te lo decía.", cap="¿Quién te lo decía? | *COMENTA*"),
])
VIDEOS = {"1601": V1601, "1603": V1603}


def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
    return scene


if __name__ == "__main__":
    arg = sys.argv[1]
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        K.run(VIDEOS[k], make_scene(VIDEOS[k]), OUT, preview=pv)
