"""Serie 'Cosas que tu cuerpo hace y nadie te contó' — 10 vídeos.

uso: python3 cuerpo.py <índices|all> [prev]
"""
import math, random, sys
import numpy as np
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, pill, glow

OUT = "/home/claude/tiktok/out40"


def cta_seg(say, cap):
    return dict(id="cta", who="nar", cut=True, say=say, cap=cap)


def nxt(n):
    return cta_seg(f"Sígueme para la parte {['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez'][n]}.",
                   f"*SÍGUEME* | para la *PARTE {n}*")


def teaser(c, t, lt, n, accent):
    if n:
        pill(c, W / 2, 1480, f"PARTE {n} →", 40, bg=WHITE, fg=INK, scale=ease_back(prog(lt, 0.6, 0.9)))


VIDEOS = []


# =============================================================== 1 · dedos
def s_dedos(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; tl = P["tl"]
    hc.aurora(c, t, V["accent"], V["a2"], 1)
    cx, cy = W / 2, 1080
    if sid in ("h", "s1", "s2", "s6", "cta"):
        gap = 60
        if sid == "s1":
            gap = lerp(60, 6, ease_in_out(prog(lt, 0.3, 2.0)))
        elif sid in ("s2", "s6", "cta"):
            gap = 6
        z = 1.0
        if sid == "s2":
            z = math.exp(ease_in_out(prog(lt, 0.2, 2.2)) * 3.2)
        if sid == "s6":
            z = math.exp((1 - ease_in_out(prog(lt, 0, 1.2))) * 3.2)
        c.save()
        c.translate(cx, cy)
        c.scale(z, z)
        c.translate(-cx, -cy)
        hc.finger(c, cx, cy + gap / 2 + 640, 0, 640, 150)
        hc.finger(c, cx, cy - gap / 2 - 640, 180, 640, 150)
        if sid in ("h",):
            glow(c, cx, cy, 120, V["accent"], 0.4 + 0.2 * math.sin(t * 6))
        c.restore()
        if sid == "s2" and lt > 1.6:
            c.drawPaint(fill(with_alpha(WHITE, clamp((lt - 1.6) / 0.5) * 0.9)))
        if sid == "s6":
            hc.big(c, "NADA", W / 2, 1520, 170, V["accent"], lt, 1.2)
        if sid == "cta":
            teaser(c, t, lt, 2, V["accent"])
        if sid == "h":
            hc.stamp(c, "NUNCA", W / 2, 1450, t, 1.2, 110)
        return
    # vista atómica
    l3 = t - tl["s3"][0]
    shake = lambda k: math.sin(t * 13 + k) * 6
    y1, y2 = 800 + shake(1), 1300 + shake(2)
    hc.atom(c, W / 2 + shake(3), y1, 300, t, V["accent"], 0)
    hc.atom(c, W / 2 + shake(4), y2, 300, t, V["a2"], 2)
    # líneas de repulsión
    for k in range(-3, 4):
        x = W / 2 + k * 70
        bend = 30 + 10 * math.sin(t * 5 + k)
        p = skia.Path()
        p.moveTo(x, y1 + 110)
        p.quadTo(x + (k * 0.6) * bend, (y1 + y2) / 2, x, y2 - 110)
        c.drawPath(p, stroke(with_alpha(WHITE, 0.25 + 0.15 * math.sin(t * 8 + k)), 3))
    if sid in ("s4",):
        x0 = W / 2 + 330
        c.drawLine(x0, y1 + 150, x0, y2 - 150, stroke(V["accent"], 6))
        c.drawLine(x0 - 20, y1 + 150, x0 + 20, y1 + 150, stroke(V["accent"], 6))
        c.drawLine(x0 - 20, y2 - 150, x0 + 20, y2 - 150, stroke(V["accent"], 6))
        K.tag(c, W / 2, 1640, "≈ 0,0000001 mm", lt - 0.4, accent=V["accent"], size=48)
    if sid == "s5":
        for sgn, yy in ((-1, y1 + 160), (1, y2 - 160)):
            a = 0.6 + 0.4 * math.sin(t * 8)
            p = skia.Path()
            p.moveTo(W / 2 - 40, yy); p.lineTo(W / 2 + 40, yy); p.lineTo(W / 2, yy + sgn * 70); p.close()
            c.drawPath(p, fill(with_alpha(WHITE, a)))
        hc.big(c, "FUERZA", W / 2, 1650, 120, V["accent"], lt, 0.3)
    if sid == "s3":
        K.tag(c, W / 2 + 280, y1 - 260, "ÁTOMO", l3 - 0.2, accent=WHITE)


VIDEOS.append(dict(slug="41_dedos", part=1, accent=0xFFFFB86B, a2=0xFF6A5AF0, scene=s_dedos, segs=[
    dict(id="h", who="nar", say="¿Sabías que tus dedos nunca se llegan a tocar? De hecho… nunca has tocado nada.",
         cap="Tus dedos *NUNCA* | se llegan a tocar… | nunca has tocado *NADA*"),
    dict(id="s1", who="nar", say="Junta las yemas de los dedos. Ahora mismo. Parece que se tocan, ¿verdad?",
         cap="Junta las *yemas*… | ahora mismo. | Parece que se tocan, ¿no?", hold=0.5),
    dict(id="s2", who="nar", cut=True, say="Pero si pudieras hacer zoom millones de veces…",
         cap="Pero si haces *ZOOM*… | millones de veces…"),
    dict(id="s3", who="nar", cut=True, say="verías átomos. Y sus electrones se repelen con muchísima fuerza.",
         cap="…verías *átomos*. | Y sus electrones | se *REPELEN*"),
    dict(id="s4", who="nar", say="Así que siempre queda un hueco: más o menos una diezmillonésima de milímetro.",
         cap="Siempre queda un *hueco*: | una *diezmillonésima* | de milímetro"),
    dict(id="s5", who="nar", say="Lo que sientes al tocar algo… es esa fuerza empujando.",
         cap="Lo que *sientes*… | es esa fuerza | *empujando*"),
    dict(id="s6", who="nar", cut=True, say="Ni el suelo, ni tu móvil, ni otra persona. Nunca has tocado nada.",
         cap="Ni el suelo, ni tu móvil… | nunca has tocado *NADA*"),
    nxt(2),
]))


# =============================================================== 2 · punto ciego
def test_card(c, dot_a=1.0, s=1.0):
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(90, 860, 900, 360), 40, 40)
    c.drawRRect(r.makeOffset(0, 14), fill(0x66000000))
    c.drawRRect(r, fill(WHITE))
    x, y = 250, 1040
    c.drawLine(x - 45, y, x + 45, y, stroke(INK, 16))
    c.drawLine(x, y - 45, x, y + 45, stroke(INK, 16))
    c.drawCircle(830, y, 48, fill(with_alpha(INK, dot_a)))


def s_ciego(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; tl = P["tl"]
    hc.aurora(c, t, V["accent"], V["a2"], 2)
    if sid in ("h", "s1", "s2", "s3"):
        dot = 1.0
        if sid == "s3":
            dot = 1 - 0.85 * ease_in_out(prog(lt, 0.2, 1.0))
        if sid == "h":
            pill(c, W / 2, 780, "PRUEBA", 40, bg=V["accent"], fg=INK, scale=ease_back(prog(t, 0.6, 0.9)))
        test_card(c, dot)
        if sid == "s1":
            hc.steps(c, [(0.1, "Tápate el ojo IZQUIERDO"), (1.2, "Mira la CRUZ con el derecho")], 160, 1370, lt, V["accent"])
        if sid == "s2":
            hc.steps(c, [(0.0, "Acerca el móvil despacio")], 200, 1370, lt, V["accent"])
            a, b = sg["speech"][1], sg["b"]
            if t > a:
                n = max(1, math.ceil(b - t))
                hc.timer(c, W / 2, 1580, 90, (t - a) / (b - a), n, V["accent"])
        if sid == "s3":
            K.tag(c, 830, 1290, "¡DESAPARECE!", lt - 0.9, accent=V["accent"], size=36)
        return
    if sid in ("s4", "s5"):
        hc.eye(c, 470, 1050, 270, t, nerve_glow=0.6 + 0.4 * math.sin(t * 5))
        K.tag(c, 780, 1330, "PUNTO CIEGO", lt - 0.5 if sid == "s4" else 1, accent=0xFFFF3B4A, line_to=(700, 1090))
        if sid == "s5":
            hc.big(c, "EL CEREBRO RELLENA", W / 2, 1600, 76, V["accent"], lt, 0.6)
        return
    test_card(c, 1.0)
    teaser(c, t, lt, 3, V["accent"])


VIDEOS.append(dict(slug="42_punto_ciego", part=2, accent=0xFF4DE1FF, a2=0xFFB04DFF, scene=s_ciego, segs=[
    dict(id="h", who="nar", say="Tienes un agujero en la vista… y ahora mismo te lo voy a enseñar.",
         cap="Tienes un *AGUJERO* | en la vista… | y te lo voy a *enseñar*"),
    dict(id="s1", who="nar", cut=True, say="Tápate el ojo izquierdo y mira fijamente la cruz con el derecho.",
         cap="Tápate el ojo *izquierdo*… | mira la *CRUZ*"),
    dict(id="s2", who="nar", say="Ahora acerca el móvil a tu cara, muy despacio.", cap="Acerca el móvil… | muy *despacio*", hold=4.5),
    dict(id="s3", who="nar", cut=True, say="¿Ha desaparecido el círculo? Es tu punto ciego.",
         cap="¿Ha *desaparecido*? | Es tu *punto ciego*"),
    dict(id="s4", who="nar", cut=True,
         say="Ahí es donde el nervio óptico sale del ojo. En ese sitio no hay células que detecten la luz.",
         cap="Ahí sale el *nervio óptico*… | y no hay células | que vean la luz"),
    dict(id="s5", who="nar", say="Tu cerebro rellena el hueco con lo que hay alrededor… y nunca te das cuenta.",
         cap="Tu cerebro *rellena* el hueco… | y nunca te das *cuenta*"),
    cta_seg("¿Te ha funcionado? Comenta, y sígueme para la parte tres.", "¿Te ha funcionado? | *COMENTA* | y *SÍGUEME*"),
]))


# =============================================================== 3 · dedo anular
def s_anular(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    hc.aurora(c, t, V["accent"], V["a2"], 3)
    ring = 0.0
    fold = 1.0
    if sid == "h":
        fold = 0.5 + 0.5 * math.sin(t * 2)
    if sid == "s1":
        fold = ease_in_out(prog(lt, 0.4, 1.4))
    if sid in ("s2", "s3"):
        ring = 0.12 * abs(math.sin(t * 9)) * (sid == "s2")
    cx, cy, s = W / 2 - 20, 1050, 1.45
    hc.hand_flat(c, cx, cy, s, t, ring_lift=ring, middle_fold=fold)
    if sid == "s2":
        hc.steps(c, [(0.0, "Levanta el ANULAR")], 230, 1620, lt, V["accent"])
        a, b = sg["speech"][1], sg["b"]
        if t > a:
            hc.timer(c, 880, 700, 80, (t - a) / (b - a), max(1, math.ceil(b - t)), V["accent"])
    if sid == "s3":
        hc.stamp(c, "BLOQUEADO", W / 2, 1600, lt, 0.2, 90)
    if sid == "s4":
        p = ease_out(prog(lt, 0.3, 1.3))
        for dx, hl in ((-45, True), (40, True), (-125, False), (122, False)):
            x0 = cx + dx * s
            col = 0xFFFF3B4A if hl else with_alpha(WHITE, 0.5)
            c.drawLine(x0, cy - 200 * s * 0.0, x0, lerp(cy - 50, cy + 330, p), stroke(col, 8 if hl else 4))
        if p > 0.6:
            yy = cy + 120
            c.drawLine(cx - 45 * s, yy, cx + 40 * s, yy + 20, stroke(0xFFFF3B4A, 10))
            glow(c, cx, yy + 10, 120, 0xFFFF3B4A, 0.7)
        K.tag(c, W / 2, 1640, "TENDONES CONECTADOS", lt - 1.0, accent=V["accent"], size=40)
    if sid == "s5":
        hc.big(c, "ÍNDICE: ✓", W / 2, 1620, 90, V["accent"], lt, 0.5)
    if sid == "cta":
        teaser(c, t, lt, 4, V["accent"])


VIDEOS.append(dict(slug="43_dedo_anular", part=3, accent=0xFFFFD23F, a2=0xFFFF6B8A, scene=s_anular, segs=[
    dict(id="h", who="nar", say="Este truco con tu mano te va a volver loco. Hazlo conmigo.",
         cap="Este truco con tu mano… | te va a volver *LOCO*"),
    dict(id="s1", who="nar", cut=True, say="Pon la mano sobre la mesa y dobla el dedo corazón por debajo.",
         cap="Mano en la *mesa*… | dobla el dedo *corazón*", hold=0.4),
    dict(id="s2", who="nar", say="Ahora intenta levantar el anular.", cap="Ahora levanta | el *ANULAR*", hold=3.0),
    dict(id="s3", who="nar", cut=True, say="¿No puedes? Normal.", cap="¿No *puedes*? | *Normal*"),
    dict(id="s4", who="nar",
         say="El anular y el corazón comparten conexiones en sus tendones. Si uno está doblado, el otro se queda bloqueado.",
         cap="Comparten *tendones*… | si uno se dobla, | el otro se *bloquea*"),
    dict(id="s5", who="nar", say="Con el índice o con el meñique sí puedes. Pruébalo.",
         cap="Con el *índice* | o el *meñique*… | ¡sí puedes!"),
    cta_seg("Comenta si lo has conseguido, y sígueme para la parte cuatro.", "¿Lo has conseguido? | *COMENTA* | y *SÍGUEME*"),
]))
VIDEOS[-1]["segs"][5]["cap"] = "Con el *índice* | o el *meñique*… | ¡sí puedes!"


# =============================================================== 4 · bostezo
def s_bostezo(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    hc.aurora(c, t, V["accent"], V["a2"], 4)
    for k in range(5):
        ph = (t * 0.35 + k / 5) % 1
        c.drawCircle(W / 2, 1080, 80 + ph * 520, stroke(with_alpha(V["accent"], 0.35 * (1 - ph)), 4))
    stretch = 1 + 0.25 * max(0, math.sin(t * 1.3)) ** 3
    if sid in ("h", "s1", "s2", "s5", "cta"):
        c.save()
        c.translate(W / 2, 1080)
        c.scale(1 / stretch ** 0.3, stretch)
        hc.big(c, "BOSTEZO", 0, 0, 170, WHITE, 1.0 if sid != "h" else t + 0.3)
        c.restore()
    if sid == "s2":
        hc.big(c, "NO LO HAGAS…", W / 2, 1450, 80, V["accent"], lt, 0.6)
    if sid in ("s3", "s4"):
        hc.brain(c, W / 2, 1080, 1.2, t, cereb=0)
        if sid == "s3":
            hc.big(c, "?", W / 2 + 290, 830, 200, V["accent"], lt, 0.3)
        else:
            glow(c, W / 2, 1050, 420, 0xFF4DE1FF, 0.5 + 0.2 * math.sin(t * 3))
            K.tag(c, W / 2, 1450, "TEORÍA: ENFRIAR EL CEREBRO", lt - 0.6, accent=V["accent"], size=38)
    if sid == "s5":
        hc.big(c, "¿YA?", W / 2, 1450, 120, V["accent"], lt, 2.5)
    if sid == "cta":
        teaser(c, t, lt, 5, V["accent"])


VIDEOS.append(dict(slug="44_bostezo", part=4, accent=0xFFB8FF3C, a2=0xFF3C8CFF, scene=s_bostezo, segs=[
    dict(id="h", who="nar", say="Te apuesto a que bostezas antes de que acabe este vídeo.",
         cap="Te apuesto a que | *BOSTEZAS* | antes de que acabe"),
    dict(id="s1", who="nar", cut=True,
         say="El bostezo es contagioso. A mucha gente le basta con oír o leer la palabra… bostezo.",
         cap="Es *contagioso*… | basta con leer la palabra… | *BOSTEZO*"),
    dict(id="s2", who="nar", say="Y cuanto más intentas no hacerlo… más ganas te dan.",
         cap="Y cuanto más lo evitas… | *más ganas* te dan"),
    dict(id="s3", who="nar", cut=True, say="Lo curioso es que la ciencia todavía no sabe del todo para qué sirve.",
         cap="La ciencia aún no sabe | del todo | para qué *sirve*"),
    dict(id="s4", who="nar", say="Una de las teorías dice que ayuda a refrescar el cerebro.",
         cap="Una teoría: | *refrescar* el cerebro"),
    dict(id="s5", who="nar", cut=True, say="Bostezo… bostezo… bostezo.", cap="Bostezo… | bostezo… | *bostezo*", hold=1.5),
    cta_seg("¿Has bostezado? Comenta, y sígueme para la parte cinco.", "¿Has bostezado? | *COMENTA* | y *SÍGUEME*"),
]))


# =============================================================== 5 · nariz
def s_nariz(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    hc.aurora(c, t, V["accent"], V["a2"], 5)
    if sid == "h":
        hc.nose(c, 1.0 - 0.6 * prog(t, 2.0, 3.0))
        K.tag(c, W / 2, 1000, "TU NARIZ", t - 0.8, accent=V["accent"], size=44, line_to=(W / 2, 1180))
    elif sid == "s1":
        hc.nose(c, 0.4 * (1 - prog(lt, 0.5, 2.5)) + 0.1)
        hc.big(c, "FILTRADO", W / 2, 1000, 130, V["accent"], lt, 1.0)
    elif sid == "s2":
        a = ease_in_out(prog(lt, 0.3, 1.0))
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W * 0.5 * a, H), fill(with_alpha(0xFF000000, 0.85)))
        hc.nose(c, 0.4 + 0.6 * a, one_eye=a)
    elif sid == "s3":
        hc.brain(c, W / 2, 1050, 1.15, t)
        K.tag(c, W / 2, 1420, "IGNORA LO QUE NO CAMBIA", lt - 0.5, accent=V["accent"], size=38)
    elif sid == "s4":
        hc.big(c, "LENGUA", W / 2, 1080, 170, WHITE, lt, 0.3)
        hc.big(c, "(ahora la notas)", W / 2, 1260, 56, V["accent"], lt, 1.2, outline=10)
    elif sid == "s5":
        br = 0.5 + 0.5 * math.sin(t * 1.6)
        glow(c, W / 2, 1080, 250 + 200 * br, V["accent"], 0.5)
        c.drawCircle(W / 2, 1080, 160 + 120 * br, stroke(WHITE, 6))
        hc.big(c, "RESPIRA", W / 2, 1080, 90, WHITE, 1)
    else:
        hc.nose(c, 0.25)
        teaser(c, t, lt, 6, V["accent"])


VIDEOS.append(dict(slug="45_nariz", part=5, accent=0xFFFF8FC7, a2=0xFF6A5AF0, scene=s_nariz, segs=[
    dict(id="h", who="nar", say="Ahora mismo estás viendo tu nariz… y tu cerebro te la esconde.",
         cap="Ahora mismo ves | tu *NARIZ*… | y tu cerebro la *esconde*"),
    dict(id="s1", who="nar", cut=True, say="Está siempre en tu campo de visión. Pero como nunca cambia, el cerebro la filtra.",
         cap="Siempre está ahí… | y el cerebro | la *FILTRA*"),
    dict(id="s2", who="nar", say="Cierra un ojo. Ahora sí la ves, ¿verdad?", cap="Cierra *un ojo*… | ahora sí la *ves*", hold=1.2),
    dict(id="s3", who="nar", cut=True, say="Tu cerebro ignora lo que no le aporta nada nuevo, para no saturarse.",
         cap="Ignora lo que | no aporta nada *nuevo*"),
    dict(id="s4", who="nar", cut=True, say="Por cierto… ahora también vas a notar tu lengua dentro de la boca.",
         cap="Por cierto… | ahora notas tu *LENGUA* | dentro de la boca"),
    dict(id="s5", who="nar", cut=True, say="Y tu respiración. De nada.", cap="Y tu *respiración*. | De nada.", hold=0.8),
    cta_seg("Sígueme para la parte seis. Cada día, una cosa de tu cuerpo que no sabías.",
            "*SÍGUEME* | para la *PARTE 6*"),
]))


# =============================================================== 6 · células en directo
_cr = random.Random(6)
CELLS = [(_cr.uniform(80, W - 80), _cr.uniform(650, 1350), _cr.uniform(35, 70), _cr.uniform(0, 5), _cr.choice(
    [0xFFFF6B8A, 0xFFFF9A6B, 0xFFB07AFF])) for _ in range(26)]


def rbc(c, x, y, r, ang):
    c.save(); c.translate(x, y); c.rotate(ang)
    c.drawOval(skia.Rect.MakeXYWH(-r, -r * 0.55, 2 * r, 1.1 * r), skia.Paint(Shader=skia.GradientShader.MakeRadial(
        (0, 0), r, [0xFF8A0A1E, 0xFFD8263A, 0xFFB01428], [0, 0.6, 1]), AntiAlias=True))
    c.restore()


def neuron(c, x, y, s, t, a=1.0):
    rnd = random.Random(9)
    for k in range(9):
        ang = k * 0.7 + rnd.uniform(-0.2, 0.2)
        L = rnd.uniform(180, 380) * s
        p = skia.Path()
        p.moveTo(x, y)
        mx, my = x + math.cos(ang) * L * 0.5, y + math.sin(ang) * L * 0.5
        ex, ey = x + math.cos(ang) * L, y + math.sin(ang) * L
        p.quadTo(mx + rnd.uniform(-40, 40), my + rnd.uniform(-40, 40), ex, ey)
        c.drawPath(p, stroke(with_alpha(0xFFB8FF3C, 0.8 * a), 7 * s))
        ph = (t * 0.8 + k / 9) % 1
        glow(c, lerp(x, ex, ph), lerp(y, ey, ph), 30, 0xFFE8FF9A, 0.8 * a)
    glow(c, x, y, 160 * s, 0xFFB8FF3C, 0.5 * a)
    c.drawCircle(x, y, 50 * s, fill(with_alpha(0xFFD8FF8A, a)))


def s_celulas(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    hc.aurora(c, t, V["accent"], V["a2"], 6)
    if sid in ("h", "s1", "s2", "s5", "s6", "cta"):
        for i, (x, y, r, ph, col) in enumerate(CELLS):
            cyc = (t * 0.4 + ph) % 2.5
            sp = clamp((cyc - 1.5) / 0.8)
            hc.cell(c, x + math.sin(t * 0.7 + i) * 15, y + math.cos(t * 0.6 + i) * 15, r, t, col, split=sp)
    elif sid == "s3":
        for k in range(14):
            x = (k * 150 + t * 90) % (W + 300) - 150
            y = 800 + (k % 4) * 140 + math.sin(t + k) * 30
            rbc(c, x, y, 70, t * 20 + k * 30)
        K.tag(c, W / 2, 1400, "GLÓBULO ROJO · ≈ 4 MESES", lt - 0.4, accent=V["accent"], size=38)
    elif sid == "s4":
        neuron(c, W / 2, 1020, 1.2, t)
        K.tag(c, W / 2, 1420, "NEURONAS: TODA LA VIDA", lt - 0.4, accent=0xFFB8FF3C, size=38)
    # contador en directo
    n = 3.8e6 * t
    s_ = 1 + (0.06 if sid == "s5" else 0.0) * math.sin(t * 10)
    c.save()
    c.translate(W / 2, 1560)
    c.scale(s_, s_)
    glow(c, 0, -30, 300, V["accent"], 0.2)
    hc.draw_text(c, K.fmt(n), 0, 45, 120, WHITE, outline=16)
    c.restore()
    pill(c, W / 2, 1660, "CÉLULAS NUEVAS DESDE QUE EMPEZÓ EL VÍDEO", 30, bg=V["accent"], fg=INK)
    if sid == "cta":
        teaser(c, t, lt, 7, V["accent"])


hc.draw_text = K.draw_text
VIDEOS.append(dict(slug="46_celulas", part=6, accent=0xFFFF6B8A, a2=0xFFFF9A3C, scene=s_celulas, segs=[
    dict(id="h", who="nar", say="Mientras ves este vídeo, tu cuerpo va a fabricar más de cien millones de células nuevas.",
         cap="Mientras ves este vídeo… | tu cuerpo fabrica | *+100 millones* de células"),
    dict(id="s1", who="nar", cut=True, say="Unos trescientos treinta mil millones al día. Casi cuatro millones por segundo.",
         cap="*330.000 millones* al día… | *≈ 4 millones* por segundo"),
    dict(id="s2", who="nar", say="Sobre todo de la sangre y del intestino, que se renuevan sin parar.",
         cap="Sobre todo de la *sangre* | y del *intestino*"),
    dict(id="s3", who="nar", cut=True, say="Un glóbulo rojo, por ejemplo, vive unos cuatro meses.",
         cap="Un glóbulo rojo | vive unos *4 meses*"),
    dict(id="s4", who="nar", cut=True, say="Pero la mayoría de tus neuronas te acompañan toda la vida.",
         cap="Pero casi todas tus *neuronas*… | te acompañan *toda la vida*"),
    dict(id="s5", who="nar", cut=True, say="Mira el contador: todo eso ha pasado mientras me escuchabas.",
         cap="Mira el *contador*… | todo eso, mientras | me *escuchabas*"),
    dict(id="s6", who="nar", say="Y de tu piel se caen miles de células muertas cada minuto. Sí, ahora también.",
         cap="Y de tu piel caen | *miles* de células | cada minuto", hold=0.6),
    nxt(7),
]))


# =============================================================== 7 · cosquillas
def robot_arm(c, x, y, t, s=1.0):
    a1 = math.radians(-60 + 8 * math.sin(t * 3))
    a2 = math.radians(50 + 12 * math.sin(t * 3 + 1))
    L1, L2 = 260 * s, 220 * s
    x1, y1 = x + math.cos(a1) * L1, y + math.sin(a1) * L1
    x2, y2 = x1 + math.cos(a1 + a2) * L2, y1 + math.sin(a1 + a2) * L2
    metal = lambda x0, y0, x1_, y1_: skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(x0, y0 - 30), (x0, y0 + 30)], [0xFFE8ECF2, 0xFF7A8290, 0xFFB8C0CC]), AntiAlias=True,
        StrokeWidth=44 * s, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
    c.drawRect(skia.Rect.MakeXYWH(x - 90 * s, y, 180 * s, 60 * s), fill(0xFF5A606A))
    c.drawLine(x, y, x1, y1, metal(x, y, x1, y1))
    c.drawLine(x1, y1, x2, y2, metal(x1, y1, x2, y2))
    for (px, py) in ((x, y), (x1, y1)):
        c.drawCircle(px, py, 30 * s, fill(0xFF3A3E46))
        c.drawCircle(px, py, 12 * s, fill(0xFF4DE1FF))
    c.drawLine(x2, y2, x2 + 30 * s, y2 + 40 * s, stroke(0xFF3A3E46, 12 * s))
    c.drawLine(x2, y2, x2 - 10 * s, y2 + 50 * s, stroke(0xFF3A3E46, 12 * s))


def s_cosquillas(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    hc.aurora(c, t, V["accent"], V["a2"], 7)
    if sid in ("h", "s1"):
        hc.big(c, "COSQUILLAS", W / 2 + math.sin(t * 30) * 6 * (sid == "h"), 1000, 150, WHITE, 1)
        hc.stamp(c, "IMPOSIBLE", W / 2, 1300, t if sid == "h" else 1, 1.2, 100)
        if sid == "s1":
            a, b = sg["speech"][1], sg["b"]
            if t > a:
                hc.timer(c, W / 2, 1600, 80, (t - a) / (b - a), max(1, math.ceil(b - t)), V["accent"])
    elif sid in ("s2", "s3"):
        hc.brain(c, W / 2, 1050, 1.2, t, cereb=ease_out(prog(lt, 0.4, 1.0)) * (0.7 + 0.3 * math.sin(t * 6)))
        K.tag(c, 900, 1430, "CEREBELO", lt - 0.8 if sid == "s2" else 1, accent=0xFF4DE1FF, line_to=(760, 1290))
        if sid == "s3":
            hc.big(c, "SIN SORPRESA = SIN COSQUILLAS", W / 2, 1600, 54, V["accent"], lt, 0.8)
    elif sid == "s4":
        robot_arm(c, 300, 1350, t, 1.3)
        K.tag(c, 760, 900, "RETRASO ≈ 0,2 s", lt - 1.0, accent=V["accent"], size=42)
        hc.big(c, "¡SÍ DABA COSQUILLAS!", W / 2, 1640, 70, WHITE, lt, 2.4)
    else:
        hc.big(c, "COSQUILLAS", W / 2, 1000, 150, WHITE, 1)
        teaser(c, t, lt, 8, V["accent"])


VIDEOS.append(dict(slug="47_cosquillas", part=7, accent=0xFFFFD23F, a2=0xFF4DE1FF, scene=s_cosquillas, segs=[
    dict(id="h", who="nar", say="No puedes hacerte cosquillas a ti mismo. Inténtalo.",
         cap="No puedes hacerte | *COSQUILLAS* | a ti mismo"),
    dict(id="s1", who="nar", say="Venga, hazlo. En las costillas, en el pie… nada.",
         cap="Venga, inténtalo… | en las costillas, en el pie… | *nada*", hold=2.0),
    dict(id="s2", who="nar", cut=True, say="Tu cerebelo predice exactamente lo que vas a sentir… y apaga la sensación.",
         cap="Tu *cerebelo* lo predice… | y *apaga* la sensación"),
    dict(id="s3", who="nar", say="Las cosquillas necesitan sorpresa. Y tú no puedes sorprenderte a ti mismo.",
         cap="Necesitan *sorpresa*… | y no puedes | *sorprenderte* a ti mismo"),
    dict(id="s4", who="nar", cut=True,
         say="Pero en un experimento, un robot copiaba tus movimientos con un pequeño retraso… y entonces sí daba cosquillas.",
         cap="Con un robot | y un pequeño *retraso*… | ¡*SÍ* daba cosquillas!"),
    cta_seg("¿Lo has intentado? Comenta, y sígueme para la parte ocho.", "¿Lo has intentado? | *COMENTA* | y *SÍGUEME*"),
]))


# =============================================================== 8 · ilusión de color (postimagen)
_E = {}


def neg_earth(c, x, y, R):
    if "img" not in _E:
        day = S.load("earth_atmos_2048.jpg")
        _E["img"] = S.render(2 * R, day, spin=math.radians(-20), lat0=0.35, light=(0, 0.2, 1), ambient=0.4, gain=1.25)
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(skia.ColorFilters.Matrix([-1, 0, 0, 0, 1, 0, -1, 0, 0, 1, 0, 0, -1, 0, 1, 0, 0, 0, 1, 0]))
    c.drawImageRect(_E["img"], skia.Rect.MakeXYWH(x - R, y - R, 2 * R, 2 * R), skia.SamplingOptions(skia.FilterMode.kLinear), p)


def s_color(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid in ("s3",):
        c.clear(WHITE)
        c.drawCircle(W / 2, 1050, 6, fill(0xFF888888))
        return
    c.clear(0xFF000000)
    neg_earth(c, W / 2, 1050, 420)
    c.drawCircle(W / 2, 1050, 9, fill(WHITE))
    c.drawCircle(W / 2, 1050, 9, stroke(INK, 2))
    if sid == "s2":
        a, b = sg["a"], sg["b"]
        hc.timer(c, W / 2, 1620, 80, (t - a) / (b - a), max(1, math.ceil(b - t)), V["accent"])
    if sid in ("s4", "cta"):
        c.drawPaint(fill(with_alpha(0xFF000000, 0.55)))
        if sid == "cta":
            teaser(c, t, lt, 9, V["accent"])


VIDEOS.append(dict(slug="48_ilusion_color", part=8, accent=0xFF6FE3FF, a2=0xFFFF8FC7, scene=s_color, segs=[
    dict(id="h", who="nar", say="Este vídeo va a hacer que veas colores que no existen.",
         cap="Vas a ver colores | que *NO EXISTEN*"),
    dict(id="s1", who="nar", say="Mira el punto blanco del centro, sin mover los ojos.",
         cap="Mira el *punto* del centro… | sin mover los ojos"),
    dict(id="s2", who="nar", say="Quince segundos. Aguanta.", cap="*15 segundos*… | aguanta", hold=12.5),
    dict(id="s3", who="nar", cut=True, say="¡Ahora! ¿La ves en color?", cap="¡AHORA! | ¿La ves en *color*?", hold=2.2),
    dict(id="s4", who="nar", cut=True,
         say="Las células de tu ojo que captan cada color se cansan… y al mirar el blanco, ves los colores contrarios.",
         cap="Tus células de color | se *cansan*… | y ves los *contrarios*"),
    cta_seg("¿Te ha funcionado? Comenta, y sígueme para la parte nueve.", "¿Te ha funcionado? | *COMENTA* | y *SÍGUEME*"),
]))


# =============================================================== 9 · cronostasis
def s_reloj(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    hc.aurora(c, t, V["accent"], V["a2"], 9)
    sec = int(t)
    if sid == "h":
        # el primer tic se queda congelado más tiempo
        sec = 0 if t < 1.6 else int(t - 0.6)
    frz = 1.0 if (sid == "h" and t < 1.6) else 0.0
    if sid == "s5":
        # trayectoria de los ojos: saltos (sacadas)
        rnd = random.Random(int(t * 3))
        pts = [(rnd.uniform(150, 930), rnd.uniform(650, 1450)) for _ in range(7)]
        pts = [(540, 1050)] + pts
        n = int((t * 3) % 7) + 1
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:n + 1]:
            p.lineTo(*q)
        c.drawPath(p, stroke(with_alpha(V["accent"], 0.7), 4))
        for q in pts[:n + 1]:
            c.drawCircle(q[0], q[1], 22, stroke(WHITE, 4))
        hc.big(c, "≈ 3 SALTOS / SEGUNDO", W / 2, 1600, 70, V["accent"], lt, 0.5)
        return
    if sid == "s2":
        blur = math.sin(clamp(lt / 1.2) * math.pi)
        p = skia.Paint(AntiAlias=True)
        c.saveLayer(None, None)
        clock(c, sec, frz, t)
        c.restore()
        if blur > 0.05:
            for k in range(6):
                c.drawPaint(fill(with_alpha(0xFF05060C, 0.12 * blur)))
            hc.big(c, "BORRADO", W / 2, 1080, 140, V["accent"], 1)
        return
    clock(c, sec, frz, t)
    if sid == "s1":
        hc.big(c, "CRONOSTASIS", W / 2, 1560, 110, V["accent"], lt, 0.5)
    if sid == "s3":
        K.tag(c, W / 2, 1560, "EL SEGUNDERO RELLENA EL HUECO", lt - 0.5, accent=V["accent"], size=38)
    if sid == "s4":
        hc.big(c, "1 s  >  1 s", W / 2, 1560, 110, V["accent"], lt, 0.4)
    if sid == "cta":
        teaser(c, t, lt, 10, V["accent"])


def clock(c, sec, frz, t):
    hc.clock(c, W / 2, 1050, 330, sec, t, frz)


VIDEOS.append(dict(slug="49_cronostasis", part=9, accent=0xFFFF8A4C, a2=0xFF4D7CFF, scene=s_reloj, segs=[
    dict(id="h", who="nar", say="¿Alguna vez has mirado un reloj… y el primer segundo parecía durar más?",
         cap="¿El primer segundo | de un reloj… | dura *MÁS*?"),
    dict(id="s1", who="nar", cut=True, say="No es tu imaginación. Tiene nombre: cronostasis.",
         cap="No es tu imaginación: | *CRONOSTASIS*"),
    dict(id="s2", who="nar", cut=True,
         say="Cuando mueves los ojos de golpe, durante el salto lo ves todo borroso… y tu cerebro borra ese momento.",
         cap="Al mover los ojos… | tu cerebro *BORRA* | el momento borroso"),
    dict(id="s3", who="nar", cut=True, say="Y para no dejar un hueco, lo rellena con la imagen de después: el segundero.",
         cap="Y lo *rellena* | con lo que viene después… | el *segundero*"),
    dict(id="s4", who="nar", say="Por eso ese primer segundo parece más largo.", cap="Por eso ese segundo | parece más *LARGO*"),
    dict(id="s5", who="nar", cut=True, say="Y tus ojos hacen estos saltos unas tres veces por segundo… todo el día.",
         cap="Tus ojos saltan | unas *3 veces* por segundo… | todo el día"),
    nxt(10),
]))


# =============================================================== 10 · mito de los vasos sanguíneos
_D = {}


def earth10(c, x, y, R, spin):
    if "day" not in _D:
        _D["day"] = S.load("earth_atmos_2048.jpg")
        _D["clouds"] = S.load("earth_clouds_1024.png", "A")
        _D["spec"] = S.load("earth_specular_2048.jpg", "L")
        _D["night"] = S.load("earth_lights_2048.png")
    img = S.render(2 * R, _D["day"], spin=spin, light=(-0.6, 0.3, 0.75), clouds=_D["clouds"], spec=_D["spec"],
                   night=_D["night"], lat0=0.25, gain=1.12)
    S.draw_planet(c, x, y, R, img)
    S.atmosphere(c, x, y, R)


def vessel_line(c, x, y, R, spin, turns, color, width=8, lat_amp=25):
    """Línea roja enrollada alrededor de la Tierra (sólo la cara visible)."""
    steps = int(360 * turns)
    prev = None
    for i in range(steps + 1):
        lon = -180 + i
        lat = lat_amp * math.sin(math.radians(i * 0.7)) - 10 + i * 0.02
        px, py, pz = S.project(lat, lon, spin=spin, lat0=0.25)
        cur = (x + px * R * 1.02, y + py * R * 1.02, pz)
        if prev and prev[2] > 0 and cur[2] > 0:
            c.drawLine(prev[0], prev[1], cur[0], cur[1], stroke(color, width))
        prev = cur


def s_vasos(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; tl = P["tl"]
    c.clear(0xFF02030A)
    STARS10.draw(c, t, camx=t * 10)
    spin = -1.2 + t * 0.25
    ex, ey, R = W / 2, 1060, 380
    earth10(c, ex, ey, R, spin)
    if sid in ("h", "s1", "s2"):
        turns = 2.5 * ease_out(prog(t, 0.2, 2.5))
        glow(c, ex, ey, R * 1.3, 0xFFFF2A3A, 0.15)
        vessel_line(c, ex, ey, R, spin, turns, 0xFFFF3B4A, 9)
        if sid == "h":
            hc.stamp(c, "FALSO", W / 2, 1560, t, 2.2, 110)
        if sid == "s1":
            K.counter(c, t, lt - 0.2, lambda p: K.fmt(100000 * p) + " km", "EL DATO DE SIEMPRE", 0xFFFF3B4A, y=1580, size=110)
        if sid == "s2":
            K.tag(c, W / 2, 1560, "CÁLCULO DE 1929 · MÚSCULOS DE ANIMALES", lt - 0.4, accent=WHITE, size=32)
        return
    if sid in ("s3", "s4", "s5"):
        a3 = tl["s3"][0]
        p = ease_out(prog(t - a3, 0.2, 1.4))
        hi = lerp(2.5, 19000 / 40075, p)
        lo = 9000 / 40075
        vessel_line(c, ex, ey, R, spin, hi, with_alpha(0xFFFF3B4A, 0.45), 14, lat_amp=0)
        vessel_line(c, ex, ey, R, spin, min(hi, lo), 0xFFFF3B4A, 9, lat_amp=0)
        if sid == "s3":
            K.counter(c, t, lt - 1.0, lambda q: K.fmt(9000 * q) + "–" + K.fmt(19000 * q) + " km", "ESTUDIO DE 2021",
                      V["accent"], y=1580, size=96)
        if sid == "s4":
            hc.big(c, "< MEDIA VUELTA", W / 2, 1580, 100, V["accent"], lt, 0.3)
        if sid == "s5":
            glow(c, ex, ey, R * 1.2, 0xFFFF2A3A, 0.25 + 0.1 * math.sin(t * 4))
        return
    pill(c, W / 2, 1480, "TU CUERPO · CADA DÍA", 40, bg=WHITE, fg=INK, scale=ease_back(prog(lt, 0.6, 0.9)))


STARS10 = K.Stars(seed=10)
VIDEOS.append(dict(slug="50_vasos_mito", part=10, accent=0xFFFFD23F, a2=0xFFFF3B4A, scene=s_vasos, segs=[
    dict(id="h", who="nar", say="Te han mentido: tus vasos sanguíneos no darían dos vueltas y media a la Tierra.",
         cap="Te han *MENTIDO*: | tus vasos sanguíneos | no dan *2,5 vueltas* a la Tierra"),
    dict(id="s1", who="nar", say="El dato está por todas partes: cien mil kilómetros.", cap="El dato de siempre: | *100.000 km*"),
    dict(id="s2", who="nar", say="Pero sale de un cálculo de mil novecientos veintinueve, hecho con músculos de animales.",
         cap="Viene de un cálculo | de *1929*… | con músculos de *animales*"),
    dict(id="s3", who="nar", cut=True, say="Un estudio de dos mil veintiuno calcula entre nueve mil y diecinueve mil kilómetros.",
         cap="Un estudio de 2021: | entre *9.000* | y *19.000 km*"),
    dict(id="s4", who="nar", say="Ni media vuelta al planeta.", cap="Ni *media vuelta* | al planeta"),
    dict(id="s5", who="nar", say="Aun así: miles de kilómetros de tubos… dentro de ti.",
         cap="Aun así… | *miles de km* | dentro de ti"),
    cta_seg("Sígueme: cada día, una cosa de tu cuerpo que no sabías.",
            "*SÍGUEME*: | cada día, algo de tu cuerpo | que no sabías"),
]))


# =============================================================== run
def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
        if V["slug"] != "48_ilusion_color" or K.seg_at(P, t)["id"] not in ("s1", "s2", "s3"):
            hc.badge(c, V["part"], V["accent"], t)
    return scene


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = "auto" if len(sys.argv) > 2 else None
    for i in idxs:
        V = VIDEOS[i]
        K.run(V, make_scene(V), OUT, preview=pv)
