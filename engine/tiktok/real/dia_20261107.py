"""Producción 07/11/2026 (1501–1502, motor actual; 1503 mito_zanahoria.py y 1504 serie_gravedad.py en 3D, 1509 ciudad3d).
  1501 PRUEBA CON TU CUERPO: ojo dominante con el test de Porta (Giambattista della Porta, 1593). Cleveland Clinic (act. 23/05/2024): 'about 30% of people have left-eye sighting dominance'; no siempre coincide con la mano.
  1502 RETO: ¿cuántas veces se juntan las agujas en 12 h? Calculado: t_k = 12k/11 h → 11 veces (assert), cada 1 h 5 min 27 s."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def motes(c, t, seed, col, n=44):
    rs = np.random.RandomState(seed)
    for i in range(n):
        x = (rs.rand() * W + t * (5 + 20 * rs.rand())) % W; y = (rs.rand() * H - t * (12 + 36 * rs.rand())) % H
        c.drawCircle(x, y, 2 + 6 * rs.rand(), fill(with_alpha(col, .05 + .13 * rs.rand())))


# ============================ 1501 ojo dominante (el punto NO se mueve nunca)
TX, TY = W / 2, 1010


def eye(c, x, y, s, closed, look=0.0, hi=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    if hi:
        c.drawCircle(0, 0, 112, fill(with_alpha(GOLD, .22)))
    p = skia.Path(); p.moveTo(-95, 0); p.quadTo(0, -70 * (1 - closed) - 4, 95, 0); p.quadTo(0, 70 * (1 - closed) + 4, -95, 0); p.close()
    c.drawPath(p, fill(0xFFF8F4EE))
    if closed < .9:
        c.save(); c.clipPath(p, doAntiAlias=True)
        c.drawCircle(look * 20, 0, 42, fill(0xFF3C7FC9)); c.drawCircle(look * 20, 0, 20, fill(0xFF0D0F18)); c.drawCircle(look * 20 + 12, -12, 8, fill(WHITE))
        c.restore()
    c.drawPath(p, stroke(0xFF10131F, 9))
    if closed >= .9:
        for k in (-50, 0, 50):
            c.drawLine(k, 8, k * 1.2, 34, stroke(0xFF10131F, 7))
    c.restore()


def ghost_finger(c, x, y, a=1.0):
    """punta de dedo semitransparente vista desde tu lado (demostración, nunca encima del punto real)."""
    w, L = 110, 230
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - 60, w, L), w / 2, w / 2)
    c.drawRRect(r, fill(with_alpha(0xFFF0C09A, .9 * a)))
    c.drawRRect(r, stroke(with_alpha(0xFF2A1408, .5 * a), 4))
    n = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 34, y - 44, 68, 80), 28, 28)
    c.drawRRect(n, fill(with_alpha(0xFFFFE9E0, .8 * a)))


def target(c, x, y, s=1.0):
    for r, col in ((150, RED), (118, WHITE), (86, RED), (54, WHITE), (24, RED)):
        c.drawCircle(x, y, r * s, fill(col))
    c.drawCircle(x, y, 150 * s, stroke(0xFF10131F, 6))


def s_ojo(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.clear(0xFF0E1424)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, TY), 980 + 40 * math.sin(t * .9), [0xFF2B3B66, 0xFF16203A, 0xFF0A0F1C], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    motes(c, t, 11, 0xFFBFD4FF)
    # anillos de radar que salen del punto (el punto queda quieto; esto da vida al plano)
    for k in range(3):
        ph = (t * .35 + k / 3) % 1
        c.drawCircle(TX, TY, 170 + ph * 420, stroke(with_alpha(WHITE, .16 * (1 - ph)), 4))
    target(c, TX, TY)
    # demostración abajo: dos ojos y un dedo-ejemplo con su propio mini-punto
    DY = 1560
    if sid in ("s1", "s2", "s3", "s4"):
        a = K.smooth(lt / .4) if sid == "s1" else 1.0
        c.saveLayerAlpha(None, int(255 * a))
        cl_l = cl_r = 0.0
        if sid == "s2":
            ph = lt / max(.1, d)
            cl_l = 1.0 if .08 < ph < .5 else 0.0
            cl_r = 1.0 if ph >= .55 else 0.0
        if sid == "s3":
            cyc = (lt % 2.4) / 2.4
            cl_l = 1.0 if cyc < .5 else 0.0
            cl_r = 1.0 - cl_l
        eye(c, W / 2 - 150, DY, .9, cl_l)
        eye(c, W / 2 + 150, DY, .9, cl_r)
        draw_text(c, "IZQ.", W / 2 - 150, DY + 120, 40, with_alpha(WHITE, .8), shadow=False)
        draw_text(c, "DER.", W / 2 + 150, DY + 120, 40, with_alpha(WHITE, .8), shadow=False)
        c.restore()
    # en s3 el dedo de ejemplo SALTA a un lado del punto pequeño (a la izquierda del plano, lejos del punto grande)
    if sid == "s3":
        mx, my = 905, 1250
        target(c, mx, my, .3)
        cyc = (lt % 2.4) / 2.4 if sid == "s3" else 0.0
        jump = 0.0 if (sid == "s4" or cyc < .5) else 1.0
        ghost_finger(c, mx - jump * 95, my, .85)
        if sid == "s3":
            draw_text(c, "SALTA" if jump else "QUIETO", mx - 50, my - 110, 40, GOLD if jump else GREEN, shadow=False)
    if sid == "h":
        K.tag(c, W / 2, 1300, "TÁPALO CON UN DEDO", lt - 1.0, accent=GOLD, size=46)
    if sid == "s2":
        hc.big(c, "CIERRA EL " + ("IZQUIERDO" if lt / max(.1, d) < .52 else "DERECHO"), W / 2, 1300, 70, WHITE, 1.0, 0.0, outline=10)
    if sid == "s4":
        K.tag(c, W / 2, 1790, "TEST DE PORTA · 1593", lt - .8, accent=GOLD, size=40)
        if lt > 3.2:
            hc.big(c, "~30% IZQUIERDO", W / 2, 1300, 92, GOLD, 1.0, 0.0, outline=12)
            K.tag(c, W / 2, 1400, "CLEVELAND CLINIC", lt - 3.4, accent=WHITE, size=30)
    K.vignette(c, .35)


V1501 = dict(slug="1501_ojo_dominante", accent=GOLD, drone=0.015, scene=s_ojo, mood="misterio", steady=True,
             send="ENVÍASELO: ¿LE SALE EL MISMO?", rehook=("s3", "AHORA MIRA TU DEDO"), reveal=("s4", "TU OJO"), segs=[
    dict(id="h", who="nar", say="Tapa este punto con un dedo, con los dos ojos abiertos. ¿Cuál es tu ojo dominante?", cap="¿Cuál es tu ojo *DOMINANTE*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Estira el brazo y tapa el punto rojo con la punta del dedo, sin cerrar ningún ojo.", cap="Tapa el punto | con *un dedo*, | con los *dos ojos abiertos*", hold=0.8),
    dict(id="s2", who="nar", cut=True, say="Ahora cierra el ojo izquierdo, y después ábrelo y cierra el derecho.", cap="Cierra el *izquierdo*… | y luego el *derecho*", hold=2.0),
    dict(id="s3", who="nar", cut=True, say="Con uno de los dos, el dedo sigue encima del punto. Con el otro, el dedo salta hacia un lado.", cap="Con un ojo, *no se mueve*. | Con el otro, *SALTA*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="El ojo con el que no se mueve es tu ojo dominante. Casi un tercio de la gente lo tiene en el izquierdo.", cap="Donde *no salta*: | tu ojo *DOMINANTE*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta derecho o izquierdo, y envíaselo a alguien, a ver si le sale el mismo.", cap="¿*DERECHO* o *IZQUIERDO*? | Comenta"),
])


# ============================ 1502 agujas del reloj
OVER = [12 * k / 11 for k in range(40) if 12 * k / 11 < 12 - 1e-9]
assert len(OVER) == 11
# comprobación por fuerza bruta: cambios de signo de la diferencia de ángulos minuto-hora en 12 h
_c = 0
for i in range(12 * 3600):
    a1 = ((i * 6 / 60) - (i * .5 / 60)) % 360; a2 = (((i + 1) * 6 / 60) - ((i + 1) * .5 / 60)) % 360
    if a2 < a1:
        _c += 1
assert _c == 11, _c
GAP = 12 / 11 * 3600; assert abs(GAP - (3600 + 5 * 60 + 27.27)) < .1
CX, CY, CR = W / 2, 1120, 330


def clock(c, hours, marks, lit_k, t):
    c.drawCircle(CX + 10, CY + 18, CR + 30, fill(with_alpha(0xFF000000, .4)))
    c.drawCircle(CX, CY, CR + 30, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(CX, CY - CR), skia.Point(CX, CY + CR)], [0xFFE7C873, 0xFF9A7426]), AntiAlias=True))
    c.drawCircle(CX, CY, CR, fill(0xFFFBF7EE))
    for i in range(60):
        a = math.radians(i * 6); L = 38 if i % 5 == 0 else 16
        x1, y1 = CX + math.sin(a) * (CR - 12), CY - math.cos(a) * (CR - 12)
        x2, y2 = CX + math.sin(a) * (CR - 12 - L), CY - math.cos(a) * (CR - 12 - L)
        c.drawLine(x1, y1, x2, y2, stroke(0xFF1C1F2B, 9 if i % 5 == 0 else 4))
    for n in range(1, 13):
        a = math.radians(n * 30)
        draw_text(c, str(n), CX + math.sin(a) * (CR - 92), CY - math.cos(a) * (CR - 92) + 22, 62, 0xFF1C1F2B, shadow=False)
    # marcas de los encuentros
    for k in range(marks):
        a = math.radians(360 * k / 11)
        x, y = CX + math.sin(a) * (CR + 62), CY - math.cos(a) * (CR + 62)
        pul = 1 + (.25 * math.sin(t * 9) if k == lit_k else 0)
        c.drawCircle(x, y, 36 * pul, fill(GOLD)); c.drawCircle(x, y, 36 * pul, stroke(WHITE, 5))
        draw_text(c, str(k + 1), x, y + 16, 44, INK, shadow=False)
    ha = math.radians((hours % 12) * 30); ma = math.radians((hours * 60 % 60) * 6)
    hand_ = lambda a, L, wdt, col: c.drawLine(CX - math.sin(a) * 30, CY + math.cos(a) * 30, CX + math.sin(a) * L, CY - math.cos(a) * L, (lambda p: (p.setStrokeCap(skia.Paint.kRound_Cap), p)[1])(stroke(col, wdt)))
    hand_(ha, CR * .55, 26, 0xFF1C1F2B)
    hand_(ma, CR * .86, 14, RED)
    c.drawCircle(CX, CY, 22, fill(0xFF1C1F2B)); c.drawCircle(CX, CY, 9, fill(GOLD))


def s_reloj(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.clear(0xFF141026)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, CY), 1000, [0xFF3A2A66, 0xFF1C1538, 0xFF0B0918], [0, .6, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    motes(c, t, 5, 0xFFE8D8FF)
    tl = P["tl"]
    marks, lit = 0, -1
    if sid == "h":
        hrs = 11.9 + .1 * K.smooth(lt / d)  # se acercan a las 12
    elif sid == "s1":
        hrs = 1.4 * K.smooth(lt / d)
    elif sid == "s2":
        hrs = 1.4 + .02 * lt
    elif sid in ("s3", "s4"):
        a3 = tl["s3"][0]; span = tl["cta"][0] - a3 - .3
        hrs = 12 * K.smooth(clamp((t - a3) / span) ** .9)
        marks = sum(1 for o in OVER if o <= hrs + 1e-6)
        lit = marks - 1
    else:
        hrs = 12 + .5 * lt / d; marks = 11; lit = -1
    sc = 1 + .015 * math.sin(t * 1.1)
    c.save(); c.translate(CX, CY); c.scale(sc, sc); c.translate(-CX, -CY)
    clock(c, hrs, marks, lit, t)
    c.restore()
    if sid in ("s3", "s4"):
        hh = int(hrs) % 12 or 12; mm = int(hrs * 60 % 60)
        hc.big(c, f"{hh}:{mm:02d}", W / 2, 1640, 96, WHITE, 1.0, 0.0, outline=10)
        hc.big(c, f"ENCUENTROS: {marks}", W / 2, 1770, 70, GOLD, 1.0, 0.0, outline=10)
    if sid == "s1" and lt > 1.4:
        K.tag(c, W / 2, 1640, "LA ROJA: 1 VUELTA POR HORA", lt - 1.4, accent=RED, size=42)
    if sid == "cta":
        s = ease_out(clamp(lt / .35))
        c.save(); c.translate(W / 2, 1680); c.rotate(-4); c.scale(s, s)
        r_ = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-330, -76, 660, 142), 18, 18); c.drawRRect(r_, fill(GOLD)); c.drawRRect(r_, stroke(WHITE, 8))
        draw_text(c, "SOLO 11", 0, 32, 100, INK, shadow=False); c.restore()
    K.vignette(c, .35)


V1502 = dict(slug="1502_agujas_reloj", accent=GOLD, drone=0.02, scene=s_reloj, mood="epico", send="RETA A UN AMIGO: ¿CUÁNTAS VECES?",
             rehook=("s3", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Cuántas veces se juntan las dos agujas del reloj en doce horas? Di un número.", cap="¿Cuántas veces se *JUNTAN* en 12 h?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Empiezan juntas a las doce. La larga da una vuelta cada hora, y la corta va mucho más despacio.", cap="La larga: | *una vuelta por hora*. | La corta: *muy lenta*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Tienes cinco segundos, y casi todo el mundo dice doce.", cap="*5 segundos*: | ¿cuántas veces?", hold=3.2),
    dict(id="s3", who="nar", cut=True, say="La trampa está al final: entre las once y las doce no se juntan, hasta que vuelven a ser las doce.", cap="Entre las *11* y las *12*… | no se juntan | hasta *las 12*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Se juntan cada hora, cinco minutos y veintisiete segundos. Así que en doce horas, solo se juntan once veces.", cap="Cada *1 h 5 min 27 s*. | En 12 horas: *SOLO 11*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Son once, no doce. Comenta tu número, y reta a un amigo a ver qué dice.", cap="¿Cuántas dijiste? | Comenta tu *NÚMERO*"),
])
VIDEOS = [V1501, V1502]


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
