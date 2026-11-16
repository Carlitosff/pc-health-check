"""Producción 16/11/2026 (2401 y 2402, motor 2D; 2403 mito_mosquitos.py y 2404 serie_encoge.py en 3D; 2409 ciudad 324).
  2401 PRUEBA EN DIRECTO: ¿estos dos cuadros son del mismo color? CUBO DE COLORES con luz cálida arriba y sombra azulada en el lado (constancia del color).
       Imagen PROPIA por código: cada cara = reflectancia × luz de esa cara; las dos casillas objetivo se calculan para dar EXACTAMENTE el mismo RGB en pantalla
       (assert sobre los píxeles renderizados). Arriba se ve marrón y en el lado naranja. No se atribuye a ningún autor (no se pudo confirmar en fuente).
  2402 RETO: mueve 1 palillo: 3 − 6 = 9 → 9 − 6 = 3 (el palillo de arriba a la izquierda del 9 pasa al 3, que se hace 9). Búsqueda exhaustiva
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


# ============================ 2401 cubo: mismo color arriba y en el lado
X = (76, 48, 20)                                   # RGB exacto de las dos casillas en pantalla
L_TOP = (1.00, 0.90, 0.50)                          # luz cálida de arriba
L_LEFT = (0.70, 0.66, 0.60)
L_RIGHT = (0.30, 0.36, 0.70)                        # sombra azulada del lado
S = 128; C30 = math.cos(math.radians(30))
O = np.array([540.0, 820.0])
u = np.array([C30, .5]) * S; v = np.array([-C30, .5]) * S; w = np.array([0, 1.0]) * S
REFL = {'W': (.95, .95, .95), 'Y': (.98, .86, .12), 'R': (.86, .10, .12), 'B': (.10, .32, .86), 'G': (.10, .70, .30), 'O': (.98, .50, .06)}
TOPC = ['Y', 'W', 'Y', 'W', None, 'Y', 'O', 'Y', 'W']
LEFTC = ['G', 'R', 'W', 'Y', 'B', 'R', 'W', 'G', 'Y']
RIGHTC = ['G', 'R', 'B', 'R', None, 'G', 'B', 'G', 'R']
TOP_T = (1, 1); RIGHT_T = (1, 1)


def faces():
    """[(cara, i, j, quad 4 puntos, rgb)] con el color de pantalla ya multiplicado por la luz."""
    out = []
    for name, org, a, b, cols, L in (("top", O, u, v, TOPC, L_TOP), ("left", O + 3 * v, u, w, LEFTC, L_LEFT), ("right", O + 3 * u + 3 * v, -v, w, RIGHTC, L_RIGHT)):
        for i in range(3):
            for j in range(3):
                k = cols[j * 3 + i]
                if k is None:
                    rgb = X                                                  # casilla objetivo: color de pantalla fijado
                    refl = tuple(round(X[c] / 255 / L[c], 3) for c in range(3))
                    assert max(refl) <= 1.0, refl
                else:
                    rgb = tuple(int(round(255 * REFL[k][c] * L[c])) for c in range(3))
                g = .08
                p0 = org + (i + g) * a + (j + g) * b; p1 = org + (i + 1 - g) * a + (j + g) * b
                p2 = org + (i + 1 - g) * a + (j + 1 - g) * b; p3 = org + (i + g) * a + (j + 1 - g) * b
                out.append((name, i, j, [p0, p1, p2, p3], rgb, k is None))
    return out


def quad(pts):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close(); return p


def centre(pts):
    return tuple(np.mean(np.array(pts), axis=0))


_CUBE = {}


def _cube():
    if not _CUBE:
        s = skia.Surface(W, H); c = s.getCanvas()
        c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 600), skia.Point(0, H)], [0xFF2A3348, 0xFF161B28], None)))
        c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, H - 1500), fill(0xFF3A2E26))                               # mesa
        sh = skia.Path(); sh.moveTo(*(O + 3 * u + 3 * v + 3 * w)); sh.lineTo(*(O + 3 * u + 3 * w + np.array([260, 40]))); sh.lineTo(*(O + 3 * u + 3 * w)); sh.close()
        c.drawPath(sh, fill(0x66000000))
        body = [O, O + 3 * u, O + 3 * u + 3 * w, O + 3 * u + 3 * v + 3 * w, O + 3 * v + 3 * w, O + 3 * v]
        c.drawPath(quad(body), fill(0xFF0E0E12))                                                          # plástico negro
        F = faces()
        for (_, _, _, pts, rgb, _) in F:
            c.drawPath(quad(pts), skia.Paint(Color=skia.Color(*rgb), AntiAlias=True))
        arr = s.makeImageSnapshot().toarray()[:, :, :3][..., ::-1]                                          # BGRA → RGB
        tg = [f for f in F if f[5]]
        assert len(tg) == 2
        pts = [tuple(int(round(v_)) for v_ in centre(f[3])) for f in tg]
        vals = [tuple(int(x) for x in arr[y, x_]) for (x_, y) in pts]
        assert vals[0] == vals[1] == X, vals
        _CUBE.update(img=s.makeImageSnapshot(), pts=pts, quads=[f[3] for f in tg], px=vals[0])
        print("píxeles medidos:", pts, vals)
    return _CUBE


def s_cube(c, t, P, V):
    I = _cube(); sid, lt, d = seg(P, t)
    z = 1.0 + .03 * min(t, 30) / 30
    c.save(); c.translate(W / 2, 1150); c.scale(z, z); c.translate(-W / 2, -1150)
    c.drawImage(I["img"], 0, 0)
    (ta, ra) = I["quads"]
    if sid == "s3":                                          # tapo todo menos las dos casillas y las uno con un puente del mismo color
        k = clamp((lt - .2) / .7) * (1 - clamp((lt - d * .5) / .5))
        if k > 0:
            m = skia.Path(); m.addRect(skia.Rect.MakeWH(W, H)); m.setFillType(skia.PathFillType.kEvenOdd)
            m.addPath(quad(ta)); m.addPath(quad(ra))
            c.drawPath(m, fill(with_alpha(0xFF8A8A8A, k)))
            ca, cb = centre(ta), centre(ra)
            p = stroke(with_alpha(skia.Color(*I["px"]), k), 46); p.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawLine(ca[0], ca[1], cb[0], cb[1], p)
    if sid in ("h", "s1", "s2"):                             # marcas sobre las dos casillas
        a = .6 + .4 * math.sin(t * 5)
        for q_ in (ta, ra):
            cc = centre(q_)
            c.drawCircle(cc[0], cc[1], 92, stroke(with_alpha(WHITE, a), 7))
        if sid == "h":
            for q_, lab in ((ta, "A"), (ra, "B")):
                cc = centre(q_)
                hc.big(c, lab, cc[0] + (-150 if lab == "A" else 150), cc[1] - 40, 80, GOLD, 1.0, 0.0, outline=10)
    c.restore()
    if sid in ("s1", "s2"):                                  # cuentagotas que lee los dos píxeles de verdad
        r, g, b = I["px"]
        for n_, (tx, ty) in enumerate(I["pts"]):
            st_ = 1.0 + n_ * 1.6
            k = ease_out(clamp((lt - st_) / 1.0)) if sid == "s1" else 1.0
            if k <= 0:
                continue
            px, py = lerp(900, tx, k), lerp(1750, ty, k)
            c.drawCircle(px, py, 50, stroke(WHITE, 9)); c.drawCircle(px, py, 50, stroke(INK, 3))
            c.drawLine(px + 36, py + 36, px + 96, py + 96, stroke(WHITE, 14)); c.drawLine(px + 36, py + 36, px + 96, py + 96, stroke(INK, 4))
            if k >= 1:
                a = clamp((lt - st_ - 1.0) / .4) if sid == "s1" else 1.0
                y0 = 1540 + n_ * 150
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(120, y0, W - 240, 130), 30, 30), fill(with_alpha(0xFF10131F, .92 * a)))
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(145, y0 + 15, 100, 100), 18, 18), fill(with_alpha(skia.Color(r, g, b), a)))
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(145, y0 + 15, 100, 100), 18, 18), stroke(with_alpha(WHITE, a), 4))
                draw_text(c, "A" if n_ == 0 else "B", 300, y0 + 82, 54, with_alpha(GOLD, a))
                draw_text(c, f"R {r} · G {g} · B {b}", 640, y0 + 82, 46, with_alpha(CYAN, a))
    if sid == "s2" and lt > 1.0:
        K.tag(c, W / 2, 1480, "A = B: EL MISMO PÍXEL", lt - 1.0, accent=GREEN, size=44)
    if sid == "s3":
        on = lt < d * .5
        K.tag(c, W / 2, 1720, "TAPADO: IGUALES" if on else "DESTAPADO: OTRA VEZ DISTINTOS", lt - (.4 if on else d * .5), accent=GOLD, size=40)
    if sid == "s4" and lt > 1.6:
        K.tag(c, W / 2, 1720, "CONSTANCIA DEL COLOR", lt - 1.6, accent=WHITE, size=40)


V2401 = dict(slug="2401_mismo_color_cubo", accent=GOLD, drone=0.015, scene=s_cube, mood="misterio", music=0.04,
             send="ENVÍASELO A QUIEN LOS VEA DISTINTOS", dare=("s1", "PREGÚNTASELO A ALGUIEN", 1440),
             rehook=("s3", "ESPERA… TAPO LO DEMÁS"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿El cuadro de arriba y el del lado son del mismo color? Uno parece marrón, y el otro naranja.", cap="¿A y B son del *MISMO* color?", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo dice que no. Vamos a medir un píxel de cada uno, con el cuentagotas.",
         cap="Casi todos: *NO*. | Medimos *1 píxel* de cada uno", hold=0.9),
    dict(id="s2", who="nar", cut=True, say="Dan exactamente los mismos tres números. En la pantalla son el mismo color, píxel a píxel.",
         cap="*IDÉNTICOS*. | Píxel a píxel", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Si tapo todo lo demás, por fin los ves iguales. Y si lo destapo, vuelven a cambiar.",
         cap="Tapado: *IGUALES*. | Destapado: *DISTINTOS*", hold=0.5),
    dict(id="s4", who="nar", cut=True, say="Tu cerebro cree que arriba hay sol, y que el lado está en sombra, así que te corrige el color sin preguntarte.",
         cap="Tu cerebro *CORRIGE* | la luz por ti", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta si los veías distintos, y envíaselo a alguien para ver si le pasa lo mismo.", cap="¿Los veías distintos? | *COMENTA*"),
])


# ============================ 2402 mueve un palillo: 3 − 6 = 9 (respuesta por búsqueda exhaustiva)
SEG7 = palillos.SEG7
SOL = palillos.solutions(3, '-', 6, 9)
assert 3 - 6 != 9 and len(SOL) == 1 and list(SOL)[0] == (9, '-', 6, 3, 3, 'f', 0, 'f'), SOL
assert 9 - 6 == 3 and set(SEG7[9]) - {'f'} == set(SEG7[3]) and set(SEG7[3]) | {'f'} == set(SEG7[9])
L7 = 150; CY = 1170
XS = [175, 355, 535, 718, 905]          # 3 · − · 6 · = · 9


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
    d1, d2, d3 = set(SEG7[3]), set(SEG7[6]), set(SEG7[9]); op = {'h'}
    mv = None; hl = None; fail = None
    if sid == "s2":                       # intentos típicos: tocar el 6 (no sale)
        k = lt % 2.4
        cyc = 0 if lt % 4.8 < 2.4 else 1
        s_ = 'e' if cyc == 0 else 'g'
        if k < 1.2:
            src = seg_line(XS[2], s_)
            off = 40 * math.sin(math.pi * k / 1.2)
            d2 = d2 - {s_}
            mv = ((src[0][0], src[0][1] - off), (src[1][0], src[1][1] - off))
        else:
            fail = 2
    if sid == "s3":
        hl = (2, 'f')
    if sid in ("s4", "cta"):
        k = clamp((lt - .3) / 1.5) if sid == "s4" else 1.0
        a0 = seg_line(XS[4], 'f'); a1 = seg_line(XS[0], 'f')
        if k < 1:
            d3 = d3 - {'f'}
            e = ease_out(k); lift = 240 * math.sin(math.pi * k)
            mv = tuple((lerp(a0[i][0], a1[i][0], e), lerp(a0[i][1], a1[i][1], e) - lift) for i in range(2))
        else:
            d1 = set(SEG7[9]); d3 = set(SEG7[3])
            if sid == "s4":
                hl = (0, 'f') if lt < 2.8 else None
    equation(c, t, [d1, d2, d3], op, moving=mv, hl=hl, fail=fail)
    if sid == "s1":
        hc.big(c, "MUEVE 1 PALILLO", W / 2, 1560, 74, GOLD, 1.0, 0.0, outline=10)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1800, 110, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > .6:
        K.tag(c, W / 2, 1640, "TOCANDO EL 6: NO SALE", lt - .6, accent=RED, size=44)
    if sid == "s3" and lt > .8:
        K.tag(c, W / 2, 1640, "EL TRUCO: AL 9 LE SOBRA UNO", lt - .8, accent=GOLD, size=46)
    if (sid == "s4" and lt > 2.0) or sid == "cta":
        a = clamp((lt - 2.0) / .4) if sid == "s4" else 1.0
        if sid == "s4":
            hc.big(c, "9 − 6 = 3", W / 2, 1620, 120, GREEN, lt - 2.0, 0.0, outline=12)
        c.drawCircle(W - 150, 1010, 54 * a, fill(GREEN))
        p = stroke(INK, 12); p.setStrokeCap(skia.Paint.kRound_Cap)
        if a > .5:
            c.drawLine(W - 176, 1010, W - 156, 1032, p); c.drawLine(W - 156, 1032, W - 120, 986, p)


V2402 = dict(slug="2402_mueve_un_palillo_3_6_9", accent=GOLD, drone=0.02, scene=s_match, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1440),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Tres menos seis, igual a nueve. Mueve un solo palillo para que la cuenta sea correcta.", cap="Arregla *3−6=9* moviendo 1 palillo", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Solo uno, sin quitar ni añadir ninguno más. Tienes cinco segundos.", cap="Solo *UNO*. | *5 segundos*", hold=3.5),
    dict(id="s2", who="nar", cut=True, say="Casi todo el mundo intenta cambiar el seis, y así no sale de ninguna forma.",
         cap="Tocando el *6*… | *NO sale*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="El truco está en el nueve del final: le sobra el palillo de arriba a la izquierda, y sin él es un tres.",
         cap="El truco: | al *9* le sobra uno", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Ponlo en el tres del principio, que se convierte en un nueve. Nueve menos seis, tres.",
         cap="*9 − 6 = 3*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo sacaste, y envíaselo a quien crea que lo saca a la primera.", cap="¿Lo sacaste? | *COMENTA*"),
])

VIDEOS = {"2401": V2401, "2402": V2402}


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
        I = _cube(); I["img"].save("/tmp/cube.png"); raise SystemExit
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        K.run(VIDEOS[k], make_scene(VIDEOS[k]), OUT, preview=pv)
