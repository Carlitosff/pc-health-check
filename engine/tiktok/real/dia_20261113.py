"""Producción 13/11/2026 (2101 y 2102, motor 2D; 2103 mito_sonambulo.py y 2104 serie_lejos.py en 3D). Sin ciudad: IGEV01 313 (dato del 12/11) = último N publicado (313).
  2101 PRUEBA EN DIRECTO: el agujero que se expande. Laeng, Nabil y Kitaoka, 'The eye pupil adjusts to illusorily expanding holes', Frontiers in Human
       Neuroscience, 30/05/2022 (nota de Frontiers 01/06/2022 y EurekAlert 31/05/2022): 50 personas; 'approximately 86% of people' lo ven crecer;
       'black holes promoted strong reflex dilations of the participants' pupils'; el efecto es más fuerte con el agujero negro. Imagen PROPIA
       dibujada por código (fondo menta, puntos propios), con el mismo principio (centro oscuro difuminado rodeado de manchas que se oscurecen hacia dentro).
  2102 RETO: mueve 1 palillo: 5 + 7 = 2 → 9 − 7 = 2 (el palillo de pie del '+' pasa al 5, que se hace 9). Búsqueda exhaustiva con dígitos de
       7 segmentos: es la ÚNICA solución moviendo un palillo (assert abajo)."""
import math, sys, itertools
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 2101 el agujero que crece
HX, HY = W / 2, 1185


def _hole_picture():
    """Se dibuja UNA vez (la imagen no cambia en todo el vídeo): manchas elípticas que se oscurecen, crecen y se difuminan hacia el centro."""
    s = skia.Surface(W, H); c = s.getCanvas()
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(HX, HY), 1150, [0xFFE4F5EC, 0xFFCFEBDD, 0xFFB8DCCB], [0, .6, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    rs = np.random.RandomState(2022)
    pts = []
    for _ in range(2600):
        r = 150 + 380 * rs.rand() ** 1.6
        a = rs.rand() * 2 * math.pi
        x, y = HX + math.cos(a) * r, HY + math.sin(a) * r
        if y < 640 or y > 1720:
            continue
        pts.append((r, a, x, y))
    pts.sort(key=lambda p: -p[0])
    for r, a, x, y in pts:
        k = clamp((530 - r) / 380)              # 0 fuera, 1 cerca del agujero
        rx = 7 + 15 * k + rs.rand() * 4; ry = rx * (0.55 + .2 * rs.rand())
        p = fill(with_alpha(0xFF06120E, .35 + .6 * k))
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.0 + 9 * k * k))
        c.save(); c.translate(x, y); c.rotate(math.degrees(a) + 90); c.drawOval(skia.Rect.MakeXYWH(-rx, -ry, 2 * rx, 2 * ry), p); c.restore()
    hole = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(HX, HY), 330, [0xFF000000, 0xFF000000, 0xE0000000, 0x00000000], [0, .42, .62, 1]))
    c.drawCircle(HX, HY, 330, hole)
    return s.makeImageSnapshot()


_HOLE = None


def eye(c, cx, cy, sc, pupil):
    c.save(); c.translate(cx, cy); c.scale(sc, sc)
    p = skia.Path(); p.moveTo(-170, 0); p.quadTo(0, -150, 170, 0); p.quadTo(0, 150, -170, 0); p.close()
    c.drawPath(p, fill(0xFFF8F6F0)); c.save(); c.clipPath(p, doAntiAlias=True)
    c.drawCircle(0, 0, 82, fill(0xFF3A8A6A)); c.drawCircle(0, 0, 82, stroke(0xFF1E5A44, 8))
    c.drawCircle(0, 0, pupil, fill(0xFF050505)); c.drawCircle(-22, -26, 14, fill(with_alpha(WHITE, .85)))
    c.restore(); c.drawPath(p, stroke(INK, 10)); c.restore()


def s_hole(c, t, P, V):
    global _HOLE
    if _HOLE is None:
        _HOLE = _hole_picture()
    sid, lt, d = seg(P, t)
    c.drawImage(_HOLE, 0, 0)
    if sid == "s2" and lt > 1.0:
        K.tag(c, W / 2, 1800, "PÍXELES QUE SE MUEVEN: 0", lt - 1.0, accent=GOLD, size=40)
    if sid == "s3":
        k = clamp((lt - .6) / 2.2)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(150, 1500, W - 300, 330), 50, 50), fill(with_alpha(0xFF000000, .78 * clamp(lt / .4))))
        eye(c, W / 2 - 170, 1660, .62 * clamp(lt / .4), 30 + 30 * ease_out(k))
        draw_text(c, "PUPILA", W / 2 + 190, 1630, 46, WHITE)
        draw_text(c, "SE AGRANDA", W / 2 + 190, 1700, 50, GOLD)
    if sid == "s4" and lt > 1.4:
        K.tag(c, W / 2, 1800, "LAENG · FRONTIERS IN HUMAN NEUROSCIENCE · 2022", lt - 1.4, accent=WHITE, size=30)


V2101 = dict(slug="2101_agujero_que_crece", accent=GOLD, drone=0.012, scene=s_hole, mood="misterio", steady=True, clean=True, music=0.03,
             send="ENVÍASELO, A VER SI LO VE", rehook=("s3", "ESPERA… TUS PUPILAS"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Mira el centro del agujero negro. ¿A que te parece que crece, como si te fuera a tragar?", cap="¿Ves cómo el agujero *CRECE*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Quédate mirando el centro unos segundos, sin mover los ojos.", cap="Mira *el centro*… | sin mover los ojos", hold=3.2),
    dict(id="s2", who="nar", cut=True, say="La imagen está completamente quieta, pero casi nueve de cada diez personas la ven crecer.",
         cap="La imagen está *QUIETA*. | Casi *9 de cada 10* | la ven crecer", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y lo más loco es que tus pupilas se agrandan, como si de verdad entraras en un sitio oscuro.",
         cap="Tus *pupilas* | se *AGRANDAN*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Lo midió Bruno Laeng, de la Universidad de Oslo, con cincuenta personas, en dos mil veintidós.",
         cap="Bruno Laeng, *Oslo*, | *2022*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta sí si lo viste crecer, y envíaselo a un amigo, a ver si a él también le pasa.", cap="¿Lo viste crecer? | *SÍ o NO*: comenta"),
])


# ============================ 2102 mueve un palillo (respuesta por búsqueda exhaustiva)
SEG7 = {0: 'abcdef', 1: 'bc', 2: 'abged', 3: 'abgcd', 4: 'fgbc', 5: 'afgcd', 6: 'afgedc', 7: 'abc', 8: 'abcdefg', 9: 'abcdfg'}
INV = {frozenset(v): k for k, v in SEG7.items()}


def _solutions(a, op, b, c_):
    st = [set(SEG7[a]), {'h', 'v'} if op == '+' else {'h'}, set(SEG7[b]), set(SEG7[c_])]
    slots = ['abcdefg', 'hv', 'abcdefg', 'abcdefg']; out = set()
    for i in range(4):
        for s_ in list(st[i]):
            for j in range(4):
                for t_ in slots[j]:
                    n = [set(x) for x in st]; n[i].discard(s_)
                    if t_ in n[j] or (i == j and t_ == s_):
                        continue
                    n[j].add(t_)
                    A, B, C = INV.get(frozenset(n[0])), INV.get(frozenset(n[2])), INV.get(frozenset(n[3]))
                    O = '+' if n[1] == {'h', 'v'} else '-' if n[1] == {'h'} else None
                    if None not in (A, B, C, O) and (A + B if O == '+' else A - B) == C:
                        out.add((A, O, B, C, i, s_, j, t_))
    return out


SOL = _solutions(5, '+', 7, 2)
assert 5 + 7 != 2 and len(SOL) == 1 and list(SOL)[0][:4] == (9, '-', 7, 2) and list(SOL)[0][4:] == (1, 'v', 0, 'b'), SOL
L7 = 150; CY = 1170
XS = [175, 355, 535, 718, 905]          # 5 · + · 7 · = · 2


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
    """digits: [d1,d2,d3] (cada uno = set de segmentos); op: set {'h','v'}; moving=(p0,p1) palillo en vuelo."""
    for idx, xi in ((0, 0), (1, 2), (2, 4)):
        for s_ in sorted(digits[idx]):
            stick(c, *seg_line(XS[xi], s_), glow=1.0 if hl == (idx, s_) else 0.0)
    ox = XS[1]
    if 'h' in op:
        stick(c, (ox - 62, CY), (ox + 62, CY))
    if 'v' in op:
        stick(c, (ox, CY - 62), (ox, CY + 62), glow=(.6 + .4 * math.sin(t * 9)) if hl == 'v' else 0.0)
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
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1200), 1050 + 30 * math.sin(t), [0xFF2A3A2A, 0xFF1A2618, 0xFF0A100A], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    # tablero de madera
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(40, 900, W - 80, 540), 40, 40), fill(0xFF3A2A1C))
    for i in range(9):
        c.drawLine(60, 930 + i * 60, W - 60, 930 + i * 60 + 6 * math.sin(i), stroke(with_alpha(0xFF000000, .18), 3))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(40, 900, W - 80, 540), 40, 40), stroke(0xFF6A4A2E, 8))
    d1, d2, d3 = set(SEG7[5]), set(SEG7[7]), set(SEG7[2]); op = {'h', 'v'}
    mv = None; hl = None; fail = None
    if sid == "s2":
        k = lt % 2.4
        fail = 2 if lt % 4.8 < 2.4 else 4
        # 'intento' fantasma: un palillo del 7 o del 2 se levanta y vuelve
        if k < 1.2:
            src = seg_line(XS[2], 'a') if fail == 2 else seg_line(XS[4], 'g')
            off = 40 * math.sin(math.pi * k / 1.2)
            if fail == 2:
                d2 = d2 - {'a'}
            else:
                d3 = d3 - {'g'}
            mv = ((src[0][0], src[0][1] - off), (src[1][0], src[1][1] - off))
            fail = None
    if sid == "s3":
        hl = 'v'
    if sid in ("s4", "cta"):
        k = clamp((lt - .3) / 1.3) if sid == "s4" else 1.0
        op = {'h'}
        a0 = ((XS[1], CY - 62), (XS[1], CY + 62)); a1 = seg_line(XS[0], 'b')
        if k < 1:
            e = ease_out(k); lift = 160 * math.sin(math.pi * k)
            mv = tuple((lerp(a0[i][0], a1[i][0], e), lerp(a0[i][1], a1[i][1], e) - lift) for i in range(2))
        else:
            d1 = set(SEG7[9])
            if sid == "s4":
                hl = (0, 'b') if lt < 2.6 else None
    equation(c, t, [d1, d2, d3], op, moving=mv, hl=hl, fail=fail)
    if sid == "s1":
        hc.big(c, "MUEVE 1 PALILLO", W / 2, 1560, 74, GOLD, 1.0, 0.0, outline=10)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1800, 110, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > .6:
        K.tag(c, W / 2, 1640, "CON EL 7 O CON EL 2: NO SALE", lt - .6, accent=RED, size=44)
    if sid == "s3" and lt > .8:
        K.tag(c, W / 2, 1640, "EL TRUCO ESTÁ EN EL SIGNO", lt - .8, accent=GOLD, size=46)
    if (sid == "s4" and lt > 1.8) or sid == "cta":
        a = clamp((lt - 1.8) / .4) if sid == "s4" else 1.0
        if sid == "s4":
            hc.big(c, "9 − 7 = 2", W / 2, 1620, 120, GREEN, lt - 1.8, 0.0, outline=12)
        c.drawCircle(W - 150, 1010, 54 * a, fill(GREEN))
        p = stroke(INK, 12); p.setStrokeCap(skia.Paint.kRound_Cap)
        if a > .5:
            c.drawLine(W - 176, 1010, W - 156, 1032, p); c.drawLine(W - 156, 1032, W - 120, 986, p)


V2102 = dict(slug="2102_mueve_un_palillo", accent=GOLD, drone=0.02, scene=s_match, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1440),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Mueve un solo palillo para que esta cuenta sea correcta. ¿Ya lo tienes?", cap="Mueve *1 PALILLO* y arregla la cuenta", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Solo uno, sin quitar ni añadir ninguno más. Tienes cinco segundos.", cap="Solo *UNO*. | *5 segundos*", hold=3.5),
    dict(id="s2", who="nar", cut=True, say="Lo normal es intentar cambiar el siete o el dos, pero así no sale de ninguna forma.",
         cap="Con el *7* o el *2*… | *NO sale*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="El truco está en el signo: quita el palillo de pie del más, y la suma se convierte en una resta.",
         cap="El truco: | *el signo*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Ponlo en el cinco, que se convierte en un nueve. Nueve menos siete, dos.",
         cap="El 5 se hace *9*: | *9 − 7 = 2*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo sacaste, y envíaselo a quien crea que lo saca a la primera.", cap="¿Lo sacaste? | *COMENTA*"),
])

VIDEOS = {"2101": V2101, "2102": V2102}


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
