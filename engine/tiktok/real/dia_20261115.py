"""Producción 15/11/2026 (2301 y 2302, motor 2D; 2303 mito_pelo.py y 2304 serie_crece.py en 3D; 2309 ciudad 314).
  2301 PRUEBA EN DIRECTO: ¿esta imagen es en color o en blanco y negro? Ilusión de la REJILLA DE ASIMILACIÓN DE COLOR (colour assimilation grid
       illusion) de Øyvind Kolås (ScienceAlert, Peter Dockrill, 30/07/2019: 'simply laying a grid of selectively coloured lines over an original
       black-and-white image'; Bart Anderson, Universidad de Sídney: el sistema del color es 'low pass'). Imagen PROPIA por código: casas de colores
       junto a un canal; la foto se pasa a gris y solo las líneas finas llevan color. assert: todos los píxeles fuera de las líneas tienen R = G = B.
  2302 RETO: mueve 1 palillo: 3 + 8 = 5 → 3 + 6 = 9 (el palillo de arriba a la derecha del 8 pasa al 5, que se hace 9). Búsqueda exhaustiva
       (palillos.solutions): es la ÚNICA solución."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, palillos
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 2301 rejilla de asimilación de color (imagen propia)
TOP = 690           # la imagen empieza bajo la franja de subtítulos
GAP, LW = 26, 5     # rejilla: una línea de color cada 26 px, de 5 px de ancho
HOUSES = [0xFFE8382F, 0xFFF6C324, 0xFF2F7BE0, 0xFF27A660, 0xFFF2832A, 0xFFE95A9E, 0xFF7B4FD0, 0xFF1FB5C2]


def _town():
    s = skia.Surface(W, H); c = s.getCanvas()
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, TOP), skia.Point(0, 1000)], [0xFF3FA0FF, 0xFF9AD4FF], None)))
    c.drawCircle(860, 820, 70, fill(0xFFFFE27A))
    for (x, y, r) in ((200, 790, 40), (250, 775, 52), (310, 792, 38), (640, 840, 34), (690, 826, 44)):
        c.drawCircle(x, y, r, fill(0xFFFFFFFF))
    rs = np.random.RandomState(1115)
    x = -20; i = 0
    while x < W + 20:
        w = 150 + rs.randint(0, 60); h = 330 + rs.randint(0, 170); col = HOUSES[i % len(HOUSES)]
        y0 = 1400 - h
        c.drawRect(skia.Rect.MakeXYWH(x, y0, w, h), fill(col))
        c.drawRect(skia.Rect.MakeXYWH(x - 6, y0 - 22, w + 12, 26), fill(0xFFB8452E))                     # alero de tejas
        for ry in range(y0 + 50, 1300, 110):
            for rx in (x + 28, x + w - 72):
                c.drawRect(skia.Rect.MakeXYWH(rx - 12, ry - 4, 20, 78), fill(0xFF1E7A3A))                # contraventanas verdes
                c.drawRect(skia.Rect.MakeXYWH(rx + 36, ry - 4, 20, 78), fill(0xFF1E7A3A))
                c.drawRect(skia.Rect.MakeXYWH(rx + 8, ry, 28, 70), fill(0xFFFFFFFF))
                c.drawRect(skia.Rect.MakeXYWH(rx + 12, ry + 4, 20, 62), fill(0xFF22344F))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + w / 2 - 30, 1300, 60, 100), 26, 26), fill(0xFF4A2A1A))
        x += w; i += 1
    c.drawRect(skia.Rect.MakeXYWH(0, 1400, W, 30), fill(0xFFD8CBB0))                                       # muelle
    c.drawRect(skia.Rect.MakeXYWH(0, 1430, W, H - 1430), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 1430), skia.Point(0, H)], [0xFF1D6FB8, 0xFF0D3E78], None)))
    img = s.makeImageSnapshot()                                                                             # reflejo de las casas en el agua
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 1430, W, H - 1430)); c.translate(0, 2860); c.scale(1, -1)
    c.drawImage(img, 0, 0, skia.SamplingOptions(), skia.Paint(Color4f=skia.Color4f(1, 1, 1, .35))); c.restore()
    for k in range(12):
        c.drawLine(0, 1460 + k * 38, W, 1462 + k * 38, stroke(with_alpha(WHITE, .10), 3))
    for (bx, bc) in ((120, 0xFFFF3B30), (560, 0xFFFFCC00), (880, 0xFF34C759)):                          # barcas
        p = skia.Path(); p.moveTo(bx - 120, 1600); p.lineTo(bx + 120, 1600); p.lineTo(bx + 85, 1660); p.lineTo(bx - 85, 1660); p.close()
        c.drawPath(p, fill(bc)); c.drawRect(skia.Rect.MakeXYWH(bx - 110, 1592, 220, 12), fill(0xFFFFFFFF))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, TOP), fill(0xFF0E1020))
    return np.ascontiguousarray(s.makeImageSnapshot().toarray()[:, :, :3][..., ::-1]).astype(np.float32)   # BGRA → RGB


def _mask():
    yy, xx = np.mgrid[0:H, 0:W]
    m = ((xx % GAP) < LW) | (((yy - TOP) % GAP) < LW)
    m[:TOP] = False
    return m


_IMG = {}


def _imgs():
    if not _IMG:
        rgb = _town()
        Y = (.299 * rgb[..., 0] + .587 * rgb[..., 1] + .114 * rgb[..., 2])
        gray = np.repeat(Y[..., None], 3, axis=2)
        mean = rgb.mean(axis=2, keepdims=True)
        sat = np.clip(mean + (rgb - mean) * 1.6, 0, 255)                     # líneas sobresaturadas (como Kolås)
        m = _mask()
        grid = gray.copy(); grid[m] = sat[m]
        g8 = gray.astype(np.uint8); gr8 = grid.astype(np.uint8)
        off = ~m; off[:TOP] = True
        assert np.all(gr8[off][:, 0] == gr8[off][:, 1]) and np.all(gr8[off][:, 1] == gr8[off][:, 2]), "hay color fuera de las líneas"
        _IMG.update(g=g8, gr=gr8, o=rgb.astype(np.uint8))
        for k in ("g", "gr", "o"):
            a = np.dstack([_IMG[k], np.full(_IMG[k].shape[:2], 255, np.uint8)])
            _IMG[k + "i"] = skia.Image.fromarray(np.ascontiguousarray(a), colorType=skia.kRGBA_8888_ColorType)
        # píxel a medir: pared de la primera casa roja, fuera de las líneas
        px, py = 0, 0
        for yy in range(1080, 1120):
            for xx in range(40, 120):
                if not m[yy, xx] and abs(int(rgb[yy, xx, 0]) - 232) < 4 and rgb[yy, xx, 1] < 80:
                    px, py = xx, yy; break
            if px:
                break
        assert px, "no encuentro la pared roja"
        _IMG["pt"] = (px, py); _IMG["px"] = tuple(int(v) for v in gr8[py, px])
        print("píxel medido:", _IMG["pt"], _IMG["px"], "original:", tuple(int(v) for v in rgb[py, px]))
    return _IMG


def s_grid(c, t, P, V):
    I = _imgs(); sid, lt, d = seg(P, t)
    z = 1.0 + .025 * min(t, 25) / 25
    c.save(); c.translate(W / 2, 1300); c.scale(z, z); c.translate(-W / 2, -1300)
    img = I["gri"]
    if sid == "s3":                                          # quito las líneas (cortina) y las vuelvo a poner
        k = clamp((lt - .3) / 0.9); back = clamp((lt - (d * .5)) / 0.6)
        c.drawImage(img, 0, 0)
        xw = W * k * (1 - back)
        if xw > 0:
            c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, xw, H)); c.drawImage(I["gi"], 0, 0); c.restore()
            c.drawRect(skia.Rect.MakeXYWH(xw - 4, TOP, 8, H - TOP), fill(WHITE))
    else:
        c.drawImage(img, 0, 0)
    c.restore()
    if sid == "s3":
        on = lt < d * .5
        K.tag(c, W / 2, 1790, "SIN LÍNEAS: TODO GRIS" if on else "CON LÍNEAS: VUELVE EL COLOR", lt - (.6 if on else d * .5), accent=GOLD, size=40)
    if sid in ("s1", "s2"):                                  # cuentagotas que lee el píxel de verdad
        tx, ty = I["pt"]
        k = ease_out(clamp(lt / 1.2)) if sid == "s1" else 1.0
        px, py = lerp(900, tx, k), lerp(1700, ty, k)
        c.drawCircle(px, py, 60, stroke(WHITE, 10)); c.drawCircle(px, py, 60, stroke(INK, 3))
        c.drawLine(px + 44, py + 44, px + 110, py + 110, stroke(WHITE, 16)); c.drawLine(px + 44, py + 44, px + 110, py + 110, stroke(INK, 4))
        if (sid == "s1" and lt > 1.4) or sid == "s2":
            a = clamp((lt - 1.4) / .4) if sid == "s1" else 1.0
            r, g, b = I["px"]
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(140, 1460, W - 280, 250), 36, 36), fill(with_alpha(0xFF10131F, .92 * a)))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(175, 1495, 180, 180), 24, 24), fill(with_alpha(skia.Color(r, g, b), a)))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(175, 1495, 180, 180), 24, 24), stroke(with_alpha(WHITE, a), 5))
            draw_text(c, "ESTA PARED", 640, 1540, 44, with_alpha(WHITE, a))
            draw_text(c, f"R {r} · G {g} · B {b}", 640, 1610, 46, with_alpha(CYAN, a))
            if sid == "s2":
                hc.big(c, "GRIS", 640, 1670, 54, GOLD, lt, 0.0, outline=6)
    if sid == "s2" and lt > 2.2:
        K.tag(c, W / 2, 1790, "SOLO LAS LÍNEAS FINAS TIENEN COLOR", lt - 2.2, accent=GOLD, size=38)
    if sid == "s4" and lt > 1.6:
        K.tag(c, W / 2, 1790, "ØYVIND KOLÅS · 2019", lt - 1.6, accent=WHITE, size=36)


V2301 = dict(slug="2301_color_o_blanco_y_negro", accent=GOLD, drone=0.015, scene=s_grid, mood="misterio", music=0.04,
             send="ENVÍASELO A QUIEN LA VEA EN COLOR", dare=("s1", "PREGÚNTASELO A ALGUIEN", 1800),
             rehook=("s3", "ESPERA… QUITO LAS LÍNEAS"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Esta imagen es en color o en blanco y negro? Contesta rápido, antes de que la toque.", cap="¿En *COLOR* o en blanco y negro?", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo ve casas de colores. Vamos a medir un píxel de esta pared roja.",
         cap="Casi todos: *COLOR*. | Medimos *1 píxel*…", hold=0.7),
    dict(id="s2", who="nar", cut=True, say="Es gris: el rojo, el verde y el azul valen lo mismo. Solo tienen color estas líneas finas.",
         cap="Es *GRIS*. | Solo las *LÍNEAS* | tienen color", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Mira qué pasa si quito las líneas: el color desaparece. Y si las vuelvo a poner, regresa.",
         cap="Sin líneas: *GRIS*. | Con líneas: *COLOR*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Tu cerebro ve el color con poco detalle, y lo reparte por lo gris. Es una ilusión de Óivind Kólos, de dos mil diecinueve.",
         cap="Tu cerebro *REPARTE* el color | (Kolås, 2019)", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta si la viste en color, y envíaselo a alguien para ver si le pasa lo mismo.", cap="¿Color o gris? | *COMENTA*"),
])


# ============================ 2302 mueve un palillo: 3 + 8 = 5 (respuesta por búsqueda exhaustiva)
SEG7 = palillos.SEG7
SOL = palillos.solutions(3, '+', 8, 5)
assert 3 + 8 != 5 and len(SOL) == 1 and list(SOL)[0] == (3, '+', 6, 9, 2, 'b', 3, 'b'), SOL
assert 3 + 6 == 9 and set(SEG7[8]) - {'b'} == set(SEG7[6]) and set(SEG7[5]) | {'b'} == set(SEG7[9])
L7 = 150; CY = 1170
XS = [175, 355, 535, 718, 905]          # 3 · + · 8 · = · 5


def seg_line(cx, s_):
    h = L7 / 2
    return {'a': ((cx - h, CY - L7), (cx + h, CY - L7)), 'g': ((cx - h, CY), (cx + h, CY)), 'd': ((cx - h, CY + L7), (cx + h, CY + L7)),
            'f': ((cx - h, CY - L7), (cx - h, CY)), 'b': ((cx + h, CY - L7), (cx + h, CY)),
            'e': ((cx - h, CY), (cx - h, CY + L7)), 'c': ((cx + h, CY), (cx + h, CY + L7))}[s_]


def stick(c, p0, p1, alpha=1.0, glow=0.0, col=0xFFE9C68B):
    x0, y0 = p0; x1, y1 = p1
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)); L = math.hypot(x1 - x0, y1 - y0) - 18
    c.save(); c.translate((x0 + x1) / 2, (y0 + y1) / 2); c.rotate(ang)
    if glow > 0:
        K.glow(c, 0, 0, 120, GOLD, .5 * glow)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-L / 2, -11, L, 22), 8, 8)
    c.drawRRect(r.makeOffset(4, 7), fill(with_alpha(0xFF000000, .35 * alpha)))
    c.drawRRect(r, fill(with_alpha(col, alpha))); c.drawRRect(r, stroke(with_alpha(0xFF8A6430, alpha), 4))
    c.drawRect(skia.Rect.MakeXYWH(-L / 2 + 8, -5, L - 30, 4), fill(with_alpha(WHITE, .25 * alpha)))
    c.drawOval(skia.Rect.MakeXYWH(L / 2 - 26, -15, 32, 30), fill(with_alpha(0xFFD8232F, alpha)))
    c.restore()


def equation(c, t, digits, op, moving=None, hl=None, fail=None):
    for idx, xi in ((0, 0), (1, 2), (2, 4)):
        for s_ in sorted(digits[idx]):
            g = .6 + .4 * math.sin(t * 9) if hl == (idx, s_) else 0.0
            stick(c, *seg_line(XS[xi], s_), glow=g)
    ox = XS[1]
    stick(c, (ox - 62, CY), (ox + 62, CY))
    if 'v' in op:
        stick(c, (ox, CY - 62), (ox, CY + 62))
    ex = XS[3]
    stick(c, (ex - 62, CY - 32), (ex + 62, CY - 32)); stick(c, (ex - 62, CY + 32), (ex + 62, CY + 32))
    if moving:
        stick(c, *moving, glow=.8)
    if fail is not None:
        x = XS[fail]
        p = stroke(with_alpha(RED, .9), 18); p.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawLine(x - 95, CY - 190, x + 95, CY + 190, p); c.drawLine(x + 95, CY - 190, x - 95, CY + 190, p)


def s_match(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1200), 1050 + 30 * math.sin(t), [0xFF2A2A3E, 0xFF181828, 0xFF0A0A12], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(40, 900, W - 80, 540), 40, 40), fill(0xFF3A2A1C))
    for i in range(9):
        c.drawLine(60, 930 + i * 60, W - 60, 930 + i * 60 + 6 * math.sin(i), stroke(with_alpha(0xFF000000, .18), 3))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(40, 900, W - 80, 540), 40, 40), stroke(0xFF6A4A2E, 8))
    d1, d2, d3 = set(SEG7[3]), set(SEG7[8]), set(SEG7[5]); op = {'h', 'v'}
    mv = None; hl = None; fail = None
    if sid == "s2":                       # intentos típicos: tocar el 3 o el signo (no sale)
        k = lt % 2.4
        fail = 0 if lt % 4.8 < 2.4 else 1
        if k < 1.2:
            src = seg_line(XS[0], 'b') if fail == 0 else ((XS[1], CY - 62), (XS[1], CY + 62))
            off = 40 * math.sin(math.pi * k / 1.2)
            if fail == 0:
                d1 = d1 - {'b'}
            else:
                op = {'h'}
            mv = ((src[0][0], src[0][1] - off), (src[1][0], src[1][1] - off))
            fail = None
    if sid == "s3":
        hl = (1, 'b')
    if sid in ("s4", "cta"):
        k = clamp((lt - .3) / 1.5) if sid == "s4" else 1.0
        a0 = seg_line(XS[2], 'b'); a1 = seg_line(XS[4], 'b')
        if k < 1:
            d2 = d2 - {'b'}
            e = ease_out(k); lift = 240 * math.sin(math.pi * k)
            mv = tuple((lerp(a0[i][0], a1[i][0], e), lerp(a0[i][1], a1[i][1], e) - lift) for i in range(2))
        else:
            d2 = set(SEG7[6]); d3 = set(SEG7[9])
            if sid == "s4":
                hl = (2, 'b') if lt < 2.8 else None
    equation(c, t, [d1, d2, d3], op, moving=mv, hl=hl, fail=fail)
    if sid == "s1":
        hc.big(c, "MUEVE 1 PALILLO", W / 2, 1560, 74, GOLD, 1.0, 0.0, outline=10)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1800, 110, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > .6:
        K.tag(c, W / 2, 1640, "CON EL 3 O CON EL SIGNO: NO SALE", lt - .6, accent=RED, size=44)
    if sid == "s3" and lt > .8:
        K.tag(c, W / 2, 1640, "EL TRUCO: AL 8 LE SOBRA UNO", lt - .8, accent=GOLD, size=46)
    if (sid == "s4" and lt > 2.0) or sid == "cta":
        a = clamp((lt - 2.0) / .4) if sid == "s4" else 1.0
        if sid == "s4":
            hc.big(c, "3 + 6 = 9", W / 2, 1620, 120, GREEN, lt - 2.0, 0.0, outline=12)
        c.drawCircle(W - 150, 1010, 54 * a, fill(GREEN))
        p = stroke(INK, 12); p.setStrokeCap(skia.Paint.kRound_Cap)
        if a > .5:
            c.drawLine(W - 176, 1010, W - 156, 1032, p); c.drawLine(W - 156, 1032, W - 120, 986, p)


V2302 = dict(slug="2302_mueve_un_palillo_3_8_5", accent=GOLD, drone=0.02, scene=s_match, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1440),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Tres más ocho, igual a cinco. Mueve un solo palillo para que la cuenta sea correcta.", cap="Mueve *1 PALILLO* y arregla 3 + 8 = 5", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Solo uno, sin quitar ni añadir ninguno más. Tienes cinco segundos.", cap="Solo *UNO*. | *5 segundos*", hold=3.5),
    dict(id="s2", who="nar", cut=True, say="Casi todo el mundo intenta cambiar el tres o el signo, y así no sale de ninguna forma.",
         cap="Con el *3* o el *signo*… | *NO sale*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="El truco está en el ocho: le sobra el palillo de arriba a la derecha, y sin él es un seis.",
         cap="El truco: | al *8* le sobra uno", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Ponlo en el cinco del final, que se convierte en un nueve. Tres más seis, nueve.",
         cap="*3 + 6 = 9*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo sacaste, y envíaselo a quien crea que lo saca a la primera.", cap="¿Lo sacaste? | *COMENTA*"),
])

VIDEOS = {"2301": V2301, "2302": V2302}


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
    if arg == "img":
        I = _imgs(); import PIL.Image as PI
        PI.fromarray(I["gr"]).save("/tmp/grid.png"); PI.fromarray(I["g"]).save("/tmp/gray.png"); raise SystemExit
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        K.run(VIDEOS[k], make_scene(VIDEOS[k]), OUT, preview=pv)
