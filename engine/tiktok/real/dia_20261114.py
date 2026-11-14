"""Producción 14/11/2026 (2201 y 2202, motor 2D; 2203 mito_leer.py y 2204 serie_dossoles.py en 3D). Sin ciudad: IGEV01 313 (dato del 13/11) = último N publicado (313).
  2201 PRUEBA EN DIRECTO: fresas que ves rojas sin un solo píxel rojo (constancia del color). La versión famosa es de Akiyoshi Kitaoka (Twitter, 28/02/2017;
       HuffPost UK: 'there's not a single red pixel in that image', 'This particular effect is called colour constancy'). Imagen PROPIA dibujada por código:
       fresas, cuenco y mesa con una luz cian encima; assert: NINGÚN píxel del cuadro tiene R mayor que G y que B a la vez. El cuentagotas lee el píxel de verdad.
  2202 RETO: mueve 1 palillo: 7 + 6 = 1 → 1 + 6 = 7 (el palillo de arriba del 7 vuela al 1, que se hace 7). Búsqueda exhaustiva con dígitos de 7 segmentos:
       es la ÚNICA solución moviendo un palillo (assert abajo)."""
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


# ============================ 2201 fresas sin píxeles rojos
BX, BY = W / 2, 1230          # centro del cuenco


def _berry(c, x, y, s, rot, rs):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, 95); p.cubicTo(-40, 80, -78, 20, -74, -30); p.cubicTo(-70, -70, -30, -78, 0, -70)
    p.cubicTo(30, -78, 70, -70, 74, -30); p.cubicTo(78, 20, 40, 80, 0, 95); p.close()
    c.drawPath(p.makeOffset(6, 10) if hasattr(p, 'makeOffset') else p, fill(with_alpha(0xFF000000, .25)))
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(-22, -28), 130, [0xFFFF9A9A, 0xFFF44A58, 0xFFCC2A3A, 0xFF8A1A2A], [0, .35, .75, 1]), AntiAlias=True)
    c.drawPath(p, g)
    c.save(); c.clipPath(p, doAntiAlias=True)
    for row in range(7):
        for col in range(-4, 5):
            sx = col * 22 + (11 if row % 2 else 0); sy = -50 + row * 22
            if abs(sx) > 70 - row * 6:
                continue
            c.drawOval(skia.Rect.MakeXYWH(sx - 3.5, sy - 5, 7, 10), fill(0xFFF2D25A))
            c.drawOval(skia.Rect.MakeXYWH(sx - 1.5, sy - 4, 3, 4), fill(with_alpha(WHITE, .7)))
    c.drawOval(skia.Rect.MakeXYWH(-46, -52, 30, 46), fill(with_alpha(WHITE, .28)))
    c.restore()
    for i in range(6):                       # cáliz verde
        a = -math.pi / 2 + (i - 2.5) * .42
        lp = skia.Path(); lp.moveTo(0, -70); lp.quadTo(math.cos(a) * 30 - 12, -70 + math.sin(a) * 30, math.cos(a) * 62, -70 + math.sin(a) * 40 + 30)
        lp.quadTo(math.cos(a) * 30 + 12, -70 + math.sin(a) * 30 + 14, 0, -70); lp.close()
        c.drawPath(lp, fill(0xFF2F9A3A)); c.drawPath(lp, stroke(0xFF1C6A24, 2))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-5, -102, 10, 34), 5, 5), fill(0xFF3AA048))
    c.restore()


def _scene_colors():
    s = skia.Surface(W, H); c = s.getCanvas()
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 900)], [0xFFF4EEE4, 0xFFE6DCCB], None)))
    c.drawRect(skia.Rect.MakeXYWH(0, 880, W, H - 880), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 880), skia.Point(0, H)], [0xFFC89A6A, 0xFF9A6A40], None)))
    for i in range(14):
        c.drawLine(0, 920 + i * 75, W, 900 + i * 80, stroke(with_alpha(0xFF5A3A20, .18), 3))
    c.drawOval(skia.Rect.MakeXYWH(BX - 430, BY + 90, 860, 150), fill(with_alpha(0xFF000000, .22)))      # sombra
    c.drawOval(skia.Rect.MakeXYWH(BX - 440, BY - 90, 880, 230), fill(0xFFF8F8F6))                     # borde del cuenco
    c.drawOval(skia.Rect.MakeXYWH(BX - 405, BY - 70, 810, 190), fill(0xFFE4E2DC))
    rs = np.random.RandomState(17)
    berries = []
    for row in range(3):
        n = 5 - row
        for i in range(n):
            x = BX + (i - (n - 1) / 2) * 150 + rs.randn() * 14
            y = BY - 10 - row * 95 + rs.randn() * 8
            berries.append((y, x, 1.05 - row * .06 + rs.rand() * .08, rs.randn() * 22))
    for y, x, s_, r_ in sorted(berries):
        _berry(c, x, y, s_, r_, rs)
    bowl = skia.Path(); bowl.moveTo(BX - 440, BY + 25); bowl.cubicTo(BX - 420, BY + 260, BX + 420, BY + 260, BX + 440, BY + 25)
    bowl.cubicTo(BX + 300, BY + 70, BX - 300, BY + 70, BX - 440, BY + 25); bowl.close()
    c.drawPath(bowl, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(BX - 440, 0), skia.Point(BX + 440, 0)], [0xFFDCDAD4, 0xFFFFFFFF, 0xFFCFCDC6], [0, .4, 1]), AntiAlias=True))
    c.drawPath(bowl, stroke(0xFFBEBBB2, 4))
    for (x, y, r) in ((170, 1640, 1.0), (930, 1700, .9)):   # hojas sueltas en la mesa
        c.save(); c.translate(x, y); c.scale(r, r)
        lp = skia.Path(); lp.moveTo(-60, 0); lp.quadTo(0, -50, 60, 0); lp.quadTo(0, 50, -60, 0)
        c.drawPath(lp, fill(0xFF3A9A40)); c.drawLine(-55, 0, 55, 0, stroke(0xFF1C6A24, 3)); c.restore()
    return s.makeImageSnapshot().toarray()[:, :, :3].astype(np.float32)     # RGBA→RGB (orden BGRA en skia N32)


def _filtered(rgb):
    """'Luz cian': mezcla al 50 % con cian y tope de rojo. Devuelve uint8 sin ningún píxel rojo (R nunca gana a G y B a la vez)."""
    out = rgb * np.array([.32, .95, 1.0], np.float32)          # filtro multiplicativo = luz cian real
    out = 255 * (np.clip(out, 0, 255) / 255) ** .8 + 8         # algo más de luz para que no se vean negras
    out[..., 0] = np.minimum(out[..., 0], np.maximum(out[..., 1], out[..., 2]))
    return np.clip(out, 0, 255).astype(np.uint8)


_IMG = {}


def _imgs():
    if not _IMG:
        bgr = _scene_colors()
        rgb = np.ascontiguousarray(bgr[..., ::-1])
        f = _filtered(rgb)
        r, g, b = f[..., 0].astype(int), f[..., 1].astype(int), f[..., 2].astype(int)
        assert not np.any((r > g) & (r > b)), "hay píxeles rojos"
        _IMG["f"] = f; _IMG["o"] = rgb.astype(np.uint8)
        for k in ("f", "o"):
            a = np.dstack([_IMG[k], np.full(_IMG[k].shape[:2], 255, np.uint8)])
            _IMG[k + "i"] = skia.Image.fromarray(np.ascontiguousarray(a), colorType=skia.kRGBA_8888_ColorType)
        _IMG["px"] = tuple(int(v) for v in f[BY - 30, int(BX), :])       # píxel que lee el cuentagotas (centro de la fresa del medio)
        print("píxel medido:", _IMG["px"], "original:", tuple(_IMG["o"][BY - 30, int(BX)]))
    return _IMG


def s_berries(c, t, P, V):
    I = _imgs(); sid, lt, d = seg(P, t)
    z = 1.0 + .03 * min(t, 20) / 20                          # acercamiento muy lento (sin tirones)
    c.save(); c.translate(W / 2, BY); c.scale(z, z); c.translate(-W / 2, -BY)
    c.drawImage(I["fi"], 0, 0)
    if sid == "s3":                                          # cortina: sin la luz cian, el color de verdad
        k = clamp((lt - .5) / 1.6) * (1 - clamp((lt - (d - 1.0)) / .8))
        if k > 0:
            xw = W * k
            c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, xw, H)); c.drawImage(I["oi"], 0, 0); c.restore()
            c.drawRect(skia.Rect.MakeXYWH(xw - 4, 0, 8, H), fill(WHITE))
    c.restore()
    if sid == "s3" and lt > .8:
        K.tag(c, W / 2, 1560, "SIN LA LUZ AZUL: ASÍ SON DE VERDAD", lt - .8, accent=GOLD, size=40)
    if sid in ("s1", "s2"):                                  # cuentagotas que lee el píxel de verdad
        k = ease_out(clamp(lt / 1.2)) if sid == "s1" else 1.0
        px, py = lerp(900, BX, k), lerp(1650, BY - 30, k)
        c.drawCircle(px, py, 70, stroke(WHITE, 10)); c.drawCircle(px, py, 70, stroke(INK, 3))
        c.drawLine(px + 50, py + 50, px + 120, py + 120, stroke(WHITE, 16)); c.drawLine(px + 50, py + 50, px + 120, py + 120, stroke(INK, 4))
        if (sid == "s1" and lt > 1.4) or sid == "s2":
            a = clamp((lt - 1.4) / .4) if sid == "s1" else 1.0
            r, g, b = I["px"]
            col = skia.Color(r, g, b)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(140, 1440, W - 280, 250), 36, 36), fill(with_alpha(0xFF10131F, .92 * a)))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(175, 1475, 180, 180), 24, 24), fill(with_alpha(col, a)))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(175, 1475, 180, 180), 24, 24), stroke(with_alpha(WHITE, a), 5))
            draw_text(c, "ESTE PÍXEL", 640, 1520, 44, with_alpha(WHITE, a))
            draw_text(c, f"R {r} · G {g} · B {b}", 640, 1590, 46, with_alpha(CYAN, a))
            if sid == "s2":
                hc.big(c, "GRIS AZULADO", 640, 1650, 50, GOLD, lt, 0.0, outline=6)
    if sid == "s2" and lt > 1.6:
        K.tag(c, W / 2, 1760, "PÍXELES ROJOS EN TODA LA IMAGEN: 0", lt - 1.6, accent=GOLD, size=40)
    if sid == "s4" and lt > 1.4:
        K.tag(c, W / 2, 1760, "CONSTANCIA DEL COLOR · KITAOKA, 2017", lt - 1.4, accent=WHITE, size=34)


V2201 = dict(slug="2201_fresas_sin_rojo", accent=GOLD, drone=0.015, scene=s_berries, mood="misterio", music=0.04,
             send="ENVÍASELO A QUIEN LAS VEA ROJAS", dare=("s1", "PREGÚNTASELO A ALGUIEN", 1800),
             rehook=("s3", "ESPERA… MIRA ESTO"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿De qué color ves estas fresas? Contesta rápido, sin pensarlo mucho.", cap="¿De qué color ves estas *FRESAS*?", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo dice que rojas. Vamos a medir el color de verdad de este píxel.",
         cap="Casi todos: *ROJAS*. | Medimos *1 píxel*…", hold=1.0),
    dict(id="s2", who="nar", cut=True, say="Es gris azulado. En toda la imagen no hay ni un solo píxel rojo.",
         cap="Es *GRIS*. | En la imagen hay | *0 píxeles rojos*", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Tu cerebro nota que la luz es azulada, se la quita a todo, y pinta las fresas del rojo que espera.",
         cap="Tu cerebro *quita* la luz azul | y *PINTA* el rojo", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Se llama constancia del color, y esta versión la hizo famosa Akiyoshi Kitaoka en dos mil diecisiete.",
         cap="*Constancia del color* | (Kitaoka, 2017)", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta de qué color las viste, y envíaselo a alguien que jure que son rojas.", cap="¿Rojas o grises? | *COMENTA*"),
])


# ============================ 2202 mueve un palillo: 7 + 6 = 1 (respuesta por búsqueda exhaustiva)
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


SOL = _solutions(7, '+', 6, 1)
assert 7 + 6 != 1 and len(SOL) == 1 and list(SOL)[0] == (1, '+', 6, 7, 0, 'a', 3, 'a'), SOL
L7 = 150; CY = 1170
XS = [175, 355, 535, 718, 905]          # 7 · + · 6 · = · 1


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
            g = 0.0
            if hl == (idx, s_):
                g = .6 + .4 * math.sin(t * 9)
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
    d1, d2, d3 = set(SEG7[7]), set(SEG7[6]), set(SEG7[1]); op = {'h', 'v'}
    mv = None; hl = None; fail = None
    if sid == "s2":                       # intentos típicos: tocar el 6 o el signo
        k = lt % 2.4
        fail = 2 if lt % 4.8 < 2.4 else 1
        if k < 1.2:
            src = seg_line(XS[2], 'e') if fail == 2 else ((XS[1], CY - 62), (XS[1], CY + 62))
            off = 40 * math.sin(math.pi * k / 1.2)
            if fail == 2:
                d2 = d2 - {'e'}
            else:
                op = {'h'}
            mv = ((src[0][0], src[0][1] - off), (src[1][0], src[1][1] - off))
            fail = None
    if sid == "s3":
        hl = (0, 'a')
    if sid in ("s4", "cta"):
        k = clamp((lt - .3) / 1.5) if sid == "s4" else 1.0
        a0 = seg_line(XS[0], 'a'); a1 = seg_line(XS[4], 'a')
        if k < 1:
            d1 = d1 - {'a'}
            e = ease_out(k); lift = 260 * math.sin(math.pi * k)
            mv = tuple((lerp(a0[i][0], a1[i][0], e), lerp(a0[i][1], a1[i][1], e) - lift) for i in range(2))
        else:
            d1 = set(SEG7[1]); d3 = set(SEG7[7])
            if sid == "s4":
                hl = (2, 'a') if lt < 2.8 else None
    equation(c, t, [d1, d2, d3], op, moving=mv, hl=hl, fail=fail)
    if sid == "s1":
        hc.big(c, "MUEVE 1 PALILLO", W / 2, 1560, 74, GOLD, 1.0, 0.0, outline=10)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1800, 110, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > .6:
        K.tag(c, W / 2, 1640, "CON EL 6 O CON EL SIGNO: NO SALE", lt - .6, accent=RED, size=44)
    if sid == "s3" and lt > .8:
        K.tag(c, W / 2, 1640, "EL TRUCO: EL TECHO DEL 7", lt - .8, accent=GOLD, size=46)
    if (sid == "s4" and lt > 2.0) or sid == "cta":
        a = clamp((lt - 2.0) / .4) if sid == "s4" else 1.0
        if sid == "s4":
            hc.big(c, "1 + 6 = 7", W / 2, 1620, 120, GREEN, lt - 2.0, 0.0, outline=12)
        c.drawCircle(W - 150, 1010, 54 * a, fill(GREEN))
        p = stroke(INK, 12); p.setStrokeCap(skia.Paint.kRound_Cap)
        if a > .5:
            c.drawLine(W - 176, 1010, W - 156, 1032, p); c.drawLine(W - 156, 1032, W - 120, 986, p)


V2202 = dict(slug="2202_mueve_un_palillo_7_6_1", accent=GOLD, drone=0.02, scene=s_match, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1440),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Siete más seis, igual a uno. Mueve un solo palillo para que la cuenta sea correcta.", cap="Mueve *1 PALILLO* y arregla 7 + 6 = 1", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Solo uno, sin quitar ni añadir ninguno más. Tienes cinco segundos.", cap="Solo *UNO*. | *5 segundos*", hold=3.5),
    dict(id="s2", who="nar", cut=True, say="Casi todo el mundo intenta cambiar el seis o el signo, y así no sale de ninguna forma.",
         cap="Con el *6* o el *signo*… | *NO sale*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="El truco está en el techo del siete: si lo quitas, el siete se convierte en un uno.",
         cap="El truco: | el *techo del 7*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Ponlo encima del uno del final, que se convierte en un siete. Uno más seis, siete.",
         cap="*1 + 6 = 7*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo sacaste, y envíaselo a quien crea que lo saca a la primera.", cap="¿Lo sacaste? | *COMENTA*"),
])

VIDEOS = {"2201": V2201, "2202": V2202}


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
        PI.fromarray(I["f"]).save("/tmp/fresas_f.png"); PI.fromarray(I["o"]).save("/tmp/fresas_o.png"); raise SystemExit
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        K.run(VIDEOS[k], make_scene(VIDEOS[k]), OUT, preview=pv)
