"""Producción 23/11/2026 (3101 y 3102, motor 2D; 3103 mito_queso.py y 3104 serie_urano.py en 3D; sin ciudad: IGEV01 330 < 332).
  3101 PRUEBA EN DIRECTO: CONTRASTE SIMULTÁNEO. Una barra de un gris uniforme (128) sobre un fondo en degradado (negro → blanco) parece más clara a
       la izquierda y más oscura a la derecha; al quitar el degradado (fondo gris uniforme) se ve igual de punta a punta. El cuentagotas lee el píxel
       DIBUJADO en el frame (core.eyedropper, v34) y el assert comprueba la barra entera. Princeton ('The Chevreul Illusion'): Michel Eugène Chevreul
       (1786-1889), químico francés, 'a concept known as simultaneous contrast'. V['clean']=True: sin viñeta ni grano, que oscurecerían los bordes.
  3102 RETO: el caracol en el pozo. Pozo de 10 m; sube 3 m de día y resbala 2 m de noche. Sale el DÍA 8 (al amanecer del 8 está a 7 m, sube 3 y
       ya está fuera, no vuelve a resbalar). Simulación con assert; 10 es la respuesta rápida (1 m por día)."""
import math, sys
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


# ============================ 3101 contraste simultáneo
BY, BH, BX0, BX1 = 980, 220, 70, W - 70


def contrast(c, grad=1.0, yoff=0.0):
    """grad 1: fondo degradado horizontal negro → blanco; grad 0: gris 128 uniforme. Barra gris 128 en medio."""
    lo, hi = int(lerp(128, 0, grad)), int(lerp(128, 255, grad))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(W, 0)], [skia.Color(lo, lo, lo), skia.Color(hi, hi, hi)])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=sh))
    c.drawRect(skia.Rect.MakeXYWH(BX0, BY + yoff, BX1 - BX0, BH), fill(GRAY))


def _assert_contrast():
    surf = skia.Surface(W, H); cc = surf.getCanvas(); contrast(cc, 1.0)
    a = surf.makeImageSnapshot().toarray()[..., :3].astype(int)
    bar = a[BY + 5:BY + BH - 5, BX0 + 2:BX1 - 2]
    assert (bar == 128).all(), np.unique(bar)
    assert a[300, 5].max() < 10 and a[300, W - 5].min() > 245


_assert_contrast()


def s_contrast(c, t, P, V):
    sid, lt, d = seg(P, t)
    grad = 1.0
    if sid == "s2":
        grad = 1 - ease_io((lt - 1.0) / 1.2)
    elif sid == "s3":
        grad = ease_io((lt - .3) / 1.0)
    yoff = 10 * math.sin(t * 1.2) if sid != "s2" else 0.0
    contrast(c, grad, yoff)
    if sid == "h":
        K.pill(c, W / 2, 1420, "¿LA DERECHA ES MÁS OSCURA?", 50, bg=0xEE000000, fg=GOLD)
        K.pill(c, W / 2, 1530, "¿SÍ o NO?", 56, bg=0xEE000000, fg=WHITE)
    if sid == "s1" and lt > d * .35:
        a = ease_out(clamp((lt - d * .35) / .4))
        for x, txt in ((260, "¿MÁS CLARA?"), (W - 260, "¿MÁS OSCURA?")):
            c.drawLine(x, BY - 20, x, BY - 140, stroke(with_alpha(GOLD, a), 5))
            K.pill(c, x, BY - 190, txt, 40, bg=0xEE000000, fg=GOLD, alpha=a)
    if sid == "s2" and lt > 2.3:
        K.tag(c, W / 2, 1420, "SIN DEGRADADO: UN SOLO GRIS", lt - 2.3, accent=GOLD, size=44)
    if sid == "s3" and lt > 1.3:                     # cuentagotas que mide el píxel de verdad en tres puntos de la barra
        a = ease_out(clamp((lt - 1.3) / .4))
        for i, x in enumerate((240, W / 2, W - 240)):
            if lt > 1.3 + i * .5:
                K.eyedropper(c, x, BY + BH / 2 + yoff, a, label_dy=-230 if i % 2 == 0 else 260)
    if sid == "s4" and lt > 1.0:
        K.tag(c, W / 2, 1420, "CONTRASTE SIMULTÁNEO · CHEVREUL", lt - 1.0, accent=GOLD, size=38)


V3101 = dict(slug="3101_barra_gris_degradado", accent=GOLD, drone=0.015, scene=s_contrast, mood="misterio", music=0.04, clean=True,
             send="ENVÍASELO Y QUE TE DIGA QUÉ VE", dare=("s1", "PREGÚNTASELO A ALGUIEN", 1840),
             rehook=("s2", "MIRA AHORA"), reveal=("s3", "LA MEDIDA"), segs=[
    dict(id="h", who="nar", say="¿Esta barra es más oscura a la derecha que a la izquierda? Contesta antes de que la mida.",
         cap="¿Es *MÁS OSCURA* a la derecha?", hold=0.8),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo la ve clara por un lado y oscura por el otro, como si fuera otro degradado.",
         cap="Clara aquí, | *oscura* allí", hold=0.6),
    dict(id="s2", who="nar", cut=True, say="Ahora mira la barra mientras quito el fondo. ¿Ves cómo se queda igual de punta a punta?",
         cap="*SIN FONDO*", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Vuelvo a poner el degradado y la mido en tres puntos: es exactamente el mismo gris.",
         cap="*EL MISMO GRIS*", hold=1.2),
    dict(id="s4", who="nar", cut=True, say="Es el contraste simultáneo, que estudió el químico Chevreul: tu cerebro juzga cada trozo por lo que tiene alrededor.",
         cap="Tu cerebro *compara* | con lo de alrededor", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Comenta si la viste cambiar, y envíaselo a alguien para ver si le pasa lo mismo.",
         cap="¿La viste cambiar? | *COMENTA*"),
])


# ============================ 3102 el caracol en el pozo
DEPTH, UP, DOWN = 10, 3, 2


def snail_days():
    h, day, log = 0, 0, []
    while True:
        day += 1; start = h; h += UP
        if h >= DEPTH:
            log.append((day, start, DEPTH, None)); return day, log
        log.append((day, start, h, h - DOWN)); h -= DOWN


DAYS, LOG = snail_days()
assert DAYS == 8 and LOG[-1][1] == 7 and DEPTH / (UP - DOWN) == 10
WX0, WX1, WTOP, WBOT = 250, 830, 560, 1640           # pozo en pantalla: 10 m = WBOT − WTOP
MPX = (WBOT - WTOP) / DEPTH


def snail_y(m):
    return WBOT - m * MPX


def snail(c, x, y, t, s=1.0, moving=0.0):
    """Caracol de perfil subiendo por la pared derecha (mira hacia arriba): cuerpo, concha en espiral, cuernos."""
    c.save(); c.translate(x, y); c.rotate(-90); c.scale(s, s)
    stretch = 1 + .08 * math.sin(t * 9) * moving
    body = skia.Path(); body.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-70 * stretch, -10, 150 * stretch, 34), 17, 17))
    c.drawPath(body, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, -10), skia.Point(0, 24)], [0xFFD8C08A, 0xFFA88A58]), AntiAlias=True))
    hx = 80 * stretch
    for dx, ln in ((-6, 46), (10, 40)):
        c.drawLine(hx + dx - 8, -2, hx + dx + 6, -ln, stroke(0xFFA88A58, 7))
        c.drawCircle(hx + dx + 6, -ln, 7, fill(0xFF2A2018))
    sh = skia.GradientShader.MakeRadial(skia.Point(-14, -48), 70, [0xFFF2B060, 0xFFC0702C, 0xFF7A3E18], [0, .6, 1])
    c.drawCircle(-10, -40, 52, skia.Paint(Shader=sh, AntiAlias=True))
    p = skia.Path(); a0 = t * .0
    for i in range(80):
        a = i * .26 + a0; r = 46 - i * .55
        px, py = -10 + r * math.cos(a), -40 + r * math.sin(a)
        (p.moveTo if i == 0 else p.lineTo)(px, py)
    c.drawPath(p, stroke(0xFF5A2A10, 5))
    c.restore()


def well(c, t, night, water=True):
    sky_d = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, WTOP)], [0xFF6EC1FF, 0xFFBFE6FF])
    sky_n = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, WTOP)], [0xFF050A20, 0xFF1A2550])
    c.drawRect(skia.Rect.MakeWH(W, H), fill(0xFF2A2418))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, WTOP), skia.Paint(Shader=sky_d))
    if night > 0:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, WTOP), skia.Paint(Shader=sky_n, Alphaf=night))
        for i in range(40):
            x, y = (i * 263) % W, (i * 97) % (WTOP - 60)
            c.drawCircle(x, y, 2 + (i % 3), fill(with_alpha(WHITE, night * (.5 + .5 * math.sin(t * 3 + i)))))
    # sol / luna recorriendo el cielo
    ang = (t * .35) % 1
    cx = W * (.15 + .7 * ang); cy = 260 - 120 * math.sin(math.pi * ang)
    K.glow(c, cx, cy, 120, 0xFFFFE070 if night < .5 else 0xFFDDE6FF, .6)
    c.drawCircle(cx, cy, 52, fill(0xFFFFE070 if night < .5 else 0xFFF2F4FF))
    # tierra y hierba
    c.drawRect(skia.Rect.MakeXYWH(0, WTOP - 30, W, 60), fill(0xFF4FA84A))
    soil = skia.GradientShader.MakeLinear([skia.Point(0, WTOP), skia.Point(0, H)], [0xFF6A4A2E, 0xFF3A2818])
    c.drawRect(skia.Rect.MakeXYWH(0, WTOP + 30, W, H - WTOP), skia.Paint(Shader=soil))
    # interior del pozo (corte) con piedras
    inner = skia.GradientShader.MakeLinear([skia.Point(WX0, 0), skia.Point(WX1, 0)], [0xFF0E0C08, 0xFF3A3226, 0xFF0E0C08], [0, .5, 1])
    c.drawRect(skia.Rect.MakeXYWH(WX0, WTOP - 30, WX1 - WX0, WBOT - WTOP + 30), skia.Paint(Shader=inner))
    for i in range(9):                                  # gotas que caen por el pozo
        f = (t * .5 + i * .37) % 1; x = WX0 + 40 + (i * 53) % (WX1 - WX0 - 80)
        c.drawCircle(x, WTOP + f * (WBOT - WTOP), 5, fill(with_alpha(0xFF9AD8FF, .6 * (1 - f))))
    lit = skia.GradientShader.MakeLinear([skia.Point(0, WTOP), skia.Point(0, WTOP + 500)], [0x55FFF2C0, 0x00FFF2C0])
    c.drawRect(skia.Rect.MakeXYWH(WX0, WTOP - 30, WX1 - WX0, 530), skia.Paint(Shader=lit))
    for row in range(int((WBOT - WTOP) / 60) + 1):
        for side, x0 in ((0, WX0 - 70), (1, WX1)):
            y = WTOP + row * 60 + (30 if (row + side) % 2 else 0)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 + 4, y + 3, 62, 54), 10, 10), fill(0xFF8A8478 if (row + side) % 3 else 0xFF9C968A))
    if water:
        wy = WBOT + 6
        c.drawRect(skia.Rect.MakeXYWH(WX0, wy, WX1 - WX0, 60), fill(0xFF2A5A8A))
        for i in range(8):
            x = WX0 + ((i * 70 + t * 40) % (WX1 - WX0)); c.drawLine(x, wy + 12, x + 30, wy + 12, stroke(0x55FFFFFF, 3))
    # regla de metros en la pared izquierda
    for m in range(DEPTH + 1):
        y = snail_y(m); c.drawLine(WX0 + 4, y, WX0 + (44 if m % 5 == 0 else 26), y, stroke(0xFFFFE070, 4))
        if m % 2 == 0 or m == DEPTH:
            draw_text(c, f"{m} m", WX0 - 130, y + 14, 38, 0xFFFFE070, outline=5)


def s_snail(c, t, P, V):
    sid, lt, d = seg(P, t)
    night, m, moving, day_lbl = 0.0, 0.0, 0.0, None
    if sid in ("h", "s1", "s2"):
        m = 0.0 if sid != "s2" else 0.0
    if sid == "s3":                                   # días 1–7 a cámara rápida: sube 3 (día), resbala 2 (noche)
        per = (d - .8) / 7
        i = min(6, int(lt // per)); ph = (lt - i * per) / per
        dd, start, top, end = LOG[i]
        if ph < .55:
            m = start + (top - start) * ease_io(ph / .55); moving = 1; night = 0
        else:
            m = top - (top - end) * ease_io((ph - .6) / .35); night = ease_io((ph - .55) / .15)
        day_lbl = f"DÍA {dd}"
        if lt > 7 * per:
            m, night, day_lbl = 7.0, 1 - ease_io((lt - 7 * per) / .6), "DÍA 8"
    if sid == "s4":                                   # día 8: de 7 a 10 y fuera
        m = 7 + 3 * ease_io((lt - .5) / 1.6) + 1.2 * ease_io((lt - 2.2) / .8); moving = 1; day_lbl = "DÍA 8"
    if sid == "cta":
        m = 11.2; day_lbl = "DÍA 8"
    well(c, t, night)
    sx = WX1 - 52
    snail(c, sx, snail_y(m) - 70, t, 1.65, moving)
    if m >= DEPTH:
        K.glow(c, sx, snail_y(m) - 40, 160, GREEN, .35)
    if sid in ("h", "s1"):
        K.pill(c, W / 2, 1180, "¿CUÁNTOS DÍAS TARDA EN SALIR?", 48, bg=0xEE000000, fg=GOLD)
        K.pill(c, W / 2, 1280, "SUBE 3 m DE DÍA · BAJA 2 m DE NOCHE", 36, bg=0xEE000000, fg=WHITE)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 930, 220, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2":
        a = ease_out(clamp((lt - .3) / .4))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - 300, 1690, 600, 150), 30, 30), fill(with_alpha(0xFF000000, .85 * a)))
        draw_text(c, "¿10 días?", W / 2, 1790, int(76 * (.7 + .3 * a)), with_alpha(RED, a), outline=6)
        if lt > 1.6:
            K.tag(c, W / 2, 1430 - 600, "3 − 2 = 1 m POR DÍA", lt - 1.6, accent=WHITE, size=40)
    if day_lbl:
        K.pill(c, 400, 1260, day_lbl, 54, bg=0xEE000000, fg=GOLD if day_lbl != "DÍA 8" else GREEN)
        K.pill(c, 400, 1360, f"{min(m, 10):.0f} m".replace(".", ","), 46, bg=0xEE000000, fg=WHITE)
    if sid == "s4" and lt > 2.6:
        K.tag(c, W / 2, 1790, "7 + 3 = 10 → ¡FUERA! · NO VUELVE A BAJAR", lt - 2.6, accent=GREEN, size=36)


V3102 = dict(slug="3102_caracol_en_el_pozo", accent=GOLD, drone=0.02, scene=s_snail, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1840),
             rehook=("s3", "ESPERA… MIRA EL DÍA OCHO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Un caracol está en el fondo de un pozo de diez metros. Cada día sube tres metros, y cada noche resbala dos. ¿Cuántos días tarda en salir?",
         cap="¿Cuántos días *TARDA EN SALIR*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos para pensarlo, sin hacer trampa.",
         cap="*5 segundos*", hold=2.6),
    dict(id="s2", who="nar", cut=True, say="Lo que sale rápido es diez días, porque cada día avanza un metro en total.",
         cap="¿*10 días*?", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero míralo día a día: al terminar la séptima noche, el caracol ya está a siete metros.",
         cap="Tras 7 noches: | *7 metros*", hold=0.8),
    dict(id="s4", who="nar", cut=True, say="El octavo día sube tres metros, llega arriba y sale. Ya no vuelve a resbalar.",
         cap="Sale el *DÍA 8*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta cuántos días habías dicho, y envíaselo a un amigo para ver si dice diez.",
         cap="¿Qué dijiste tú? | *COMENTA*"),
])

VIDEOS = {"3101": V3101, "3102": V3102}


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
