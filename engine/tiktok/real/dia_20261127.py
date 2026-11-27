"""Producción 27/11/2026 (3501 y 3502, motor 2D; 3503 mito_perro.py y 3504 serie_luna2x.py en 3D; sin ciudad: IGEV01 329 < 332).
  3501 PRUEBA EN DIRECTO: ¿QUÉ MESA ES MÁS LARGA? (mesas de Shepard). Roger N. Shepard (Stanford), 'Turning the Tables', en su libro
       'Mind Sights' (W. H. Freeman, 1990, p. 48); Wikipedia 'Shepard tables': 'two parallelograms, identical aside from a rotation of 90 degrees';
       Michael Bach 'Shepard's Rotated Tables'. Dibujo propio. Assert: el tablero izquierdo es EXACTAMENTE el derecho girado 90° (vértices) y,
       en píxeles, al girarlo y ponerlo encima los dos coinciden (XOR de máscaras < 0,5 % del área, solo bordes).
  3502 RETO BLACK FRIDAY (viernes 27/11/2026): un precio de 100 € sube un 20 % y luego se rebaja un 20 % → 96 € (no 100: el 20 % de la rebaja
       se calcula sobre 120 → 24 €). Assert con fracciones."""
import math, sys
from fractions import Fraction as Fr
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


# ============================ 3501 mesas de Shepard
U = np.array([340.0, -150.0])     # lado largo del tablero DERECHO (casi horizontal)
VV = np.array([100.0, -130.0])   # lado corto, que se va hacia el fondo
CR = np.array([760.0, 1140.0])   # centro del tablero derecho
CL = np.array([300.0, 1080.0])   # centro del tablero izquierdo


def rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return np.array([c * p[0] - s * p[1], s * p[0] + c * p[1]])


def top_pts(center, ang):
    """Vértices del tablero (paralelogramo U×VV centrado) girado ang radianes alrededor de su centro."""
    base = [-(U + VV) / 2, U - (U + VV) / 2, U + VV - (U + VV) / 2, VV - (U + VV) / 2]
    return [center + rot(p, ang) for p in base]


LEFT_ANG = -math.pi / 2           # el izquierdo es el derecho girado 90°


def _poly(pts):
    pa = skia.Path(); pa.moveTo(*pts[0])
    for p in pts[1:]:
        pa.lineTo(*p)
    pa.close(); return pa


def _assert_shepard():
    L, R = top_pts(CL, LEFT_ANG), top_pts(CR, 0.0)
    # (1) mismos lados: el largo mide lo mismo en las dos mesas
    la = np.linalg.norm(L[1] - L[0]); ra = np.linalg.norm(R[1] - R[0])
    assert abs(la - ra) < 1e-9 and abs(np.linalg.norm(L[3] - L[0]) - np.linalg.norm(R[3] - R[0])) < 1e-9
    # (2) en píxeles: girar el izquierdo +90° y llevarlo al centro derecho lo deja encima, exacto
    moved = top_pts(CR, LEFT_ANG + math.pi / 2)
    m = []
    for pts in (moved, R):
        s = skia.Surface(W, H); c = s.getCanvas(); c.clear(0xFF000000); c.drawPath(_poly(pts), fill(WHITE))
        m.append(s.makeImageSnapshot().toarray()[..., 0] > 127)
    xor = np.logical_xor(*m).sum(); area = m[1].sum()
    assert area > 20000 and xor / area < 0.005, (xor, area)
    # (3) y en el dibujo el izquierdo PARECE más largo: su lado largo es casi vertical (va 'hacia el fondo')
    d = L[1] - L[0]; assert abs(d[1]) > abs(d[0]) * 2


_assert_shepard()

WOOD, WOOD_D, WOOD_S, LEG = 0xFFB9783F, 0xFF8A5229, 0xFF6E3F1E, 0xFF5A3216


def table(c, pts, legs_a=1.0, wood=WOOD):
    """Tablero + canto + 4 patas. Las patas y el canto cuelgan de los vértices 'delanteros' (los más bajos en pantalla)."""
    ys = sorted(range(4), key=lambda i: pts[i][1])
    if legs_a > 0:
        th = 34 * legs_a
        # canto: bajo las dos aristas que tocan el vértice más bajo
        lo = ys[3]
        for nb in ((lo + 1) % 4, (lo + 3) % 4):
            a, b = pts[lo], pts[nb]
            q = [a, b, b + (0, th), a + (0, th)]
            c.drawPath(_poly(q), fill(with_alpha(WOOD_S, legs_a)))
        for i in range(4):
            p = pts[i]; back = i == ys[0]
            h = 230 * legs_a
            col = with_alpha(LEG if not back else 0xFF3E2210, legs_a)
            c.drawRect(skia.Rect.MakeXYWH(p[0] - 13, p[1] + (8 if not back else -2), 26, h), fill(col))
    c.drawPath(_poly(pts), fill(wood))
    # vetas que siguen el lado largo
    pa = _poly(pts); c.save(); c.clipPath(pa, doAntiAlias=True)
    u = pts[1] - pts[0]; v = pts[3] - pts[0]
    for k in range(1, 9):
        a = pts[0] + v * (k / 9); b = a + u
        c.drawLine(*a, *b, stroke(with_alpha(WOOD_D, .35), 3))
    c.restore()
    c.drawPath(pa, stroke(with_alpha(0xFF3A1E0C, .8), 4))


def room(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)], [0xFF2E3A4E, 0xFF151A24])))
    for i in range(26):   # polvo que flota en la luz (movimiento sin tocar las mesas)
        x = (i * 211 + t * (12 + i % 5 * 4)) % W; y = 720 + (i * 131 + math.sin(t * .7 + i) * 30) % 900
        c.drawCircle(x, y, 2.2 + (i % 3), fill(with_alpha(0xFFFFE6B0, .22)))
    c.drawOval(skia.Rect.MakeXYWH(40, 1380, W - 80, 140), fill(with_alpha(0xFF000000, .35)))


def s_tables(c, t, P, V):
    sid, lt, d = seg(P, t)
    room(c, t)
    legs = 1.0; angL = LEFT_ANG; cL = CL; wood_l = WOOD; overlay_ruler = False
    if sid == "s2":                      # quitar patas y llevar el tablero encima
        legs = 1 - ease_io((lt - .2) / .8)
        k = ease_io((lt - 1.2) / (d - 1.8))
        angL = LEFT_ANG + math.pi / 2 * k
        cL = CL + (CR - CL) * k
        wood_l = 0xD0E8A14F
    elif sid in ("s3", "s4"):
        legs = 0.0; angL = 0.0; cL = CR; wood_l = 0xD0E8A14F
        if sid == "s3":   # vuelve a su sitio para que lo veas otra vez
            k = ease_io((lt - 1.6) / 1.4)
            angL = math.pi / 2 * (k * -1); cL = CR + (CL - CR) * k; legs = ease_io((lt - 2.6) / .8)
            overlay_ruler = lt > 3.2
        else:
            angL = LEFT_ANG; cL = CL; legs = 1.0; overlay_ruler = True
    elif sid == "cta":
        overlay_ruler = True
    R = top_pts(CR, 0.0)
    L = top_pts(cL, angL)
    if sid in ("h", "s1", "cta") or (sid == "s4"):
        table(c, R, 1.0); table(c, L, legs, wood_l if sid == "s2" else WOOD)
    else:
        table(c, R, legs if sid == "s2" else (1.0 if sid != "s3" else max(legs, 0.0)))
        table(c, L, legs, wood_l)
    if overlay_ruler:     # mismo lado largo marcado en las dos con la misma barra
        for pts in (L, R):
            a, b = pts[0], pts[1]
            c.drawLine(*a, *b, stroke(GREEN, 12))
            c.drawCircle(*a, 10, fill(GREEN)); c.drawCircle(*b, 10, fill(GREEN))
    if sid == "s1" and lt > 1.0:
        K.tag(c, W / 2, 1600, "¿IZQUIERDA O DERECHA?", lt - 1.0, accent=GOLD, size=42)
    if sid == "s3" and lt > .4 and lt < 1.8:
        K.pill(c, W / 2, 1620, "ENCAJA PERFECTO", 54, bg=0xEE000000, fg=GREEN, scale=K.ease_back(K.prog(lt, .4, .7)))
    if sid == "s4" and lt > 2.4:
        K.tag(c, W / 2, 1840, "ROGER SHEPARD · MIND SIGHTS · 1990", lt - 2.4, accent=WHITE, size=32)


V3501 = dict(slug="3501_mesas_shepard", accent=GOLD, drone=0.015, scene=s_tables, mood="misterio", music=0.04, clean=True,
             send="ENVÍASELO Y QUE ELIJA UNA MESA", vote=("s2", ("IZQUIERDA", "IGUALES"), 1, 1740), dare=("s1", "PREGÚNTALE CUÁL ELIGE", 1840),
             rehook=("s2", "MIRA LO QUE PASA"), reveal=("s2", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Qué mesa es más larga? Contesta antes de que mueva la de la izquierda.",
         cap="¿Qué mesa es *MÁS LARGA*?", hold=0.6),
    dict(id="s1", who="nar", cut=True, say="La de la izquierda parece una mesa de comedor, larga y estrecha, y la de la derecha casi cuadrada.",
         cap="¿La de *LA IZQUIERDA*?", hold=0.8),
    dict(id="s2", who="nar", cut=True, say="Ahora le quito las patas, giro el tablero de la izquierda, y lo pongo encima del otro.",
         cap="Le quito *LAS PATAS*…", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="Encaja perfecto. Son el mismo tablero, exactamente igual, solo que girado.",
         cap="*EL MISMO* tablero", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Tu cerebro lo ve en tres dimensiones y alarga lo que se aleja de ti. La dibujó Roger Shepard, de Stanford, en mil novecientos noventa.",
         cap="Roger Shepard, *1990*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta cuál te parecía más larga, y envíaselo a alguien para ver si se lo cree.",
         cap="¿Cuál elegiste? | *COMENTA*"),
])


# ============================ 3502 Black Friday +20 % −20 %
P0 = Fr(100); UP = Fr(20, 100); DN = Fr(20, 100)
P1 = P0 * (1 + UP); CUT = P1 * DN; P2 = P1 - CUT
assert (P1, CUT, P2) == (120, 24, 96) and P0 * (1 - DN) * (1 + UP) == 96 and P2 != P0


def price_tag(c, x, y, txt, col, t, sw=0.0, s=1.0, strike=False):
    """Etiqueta de precio de cartón con agujero y cordel, que se balancea (sw)."""
    c.save(); c.translate(x, y); c.rotate(math.degrees(sw * math.sin(t * 2.2))); c.scale(s, s)
    c.drawLine(0, -260, 0, -150, stroke(0xFFE8E0D0, 5))
    pa = skia.Path(); w, h = 520, 300
    pa.moveTo(0, -170); pa.lineTo(w / 2, -110); pa.lineTo(w / 2, h - 150); pa.lineTo(-w / 2, h - 150); pa.lineTo(-w / 2, -110); pa.close()
    c.drawPath(pa, fill(col)); c.drawPath(pa, stroke(0xFF1A1A1A, 6))
    c.drawCircle(0, -120, 18, fill(0xFF1A1A1A))
    draw_text(c, txt, 0, 70, 150, INK)
    if strike:
        c.drawLine(-200, 20, 200, 20, stroke(RED, 16))
    c.restore()


def bars(c, vals, t, hi=None, y0=1480, sc=5.0):
    xs = [270, 540, 810]
    lab = ["ANTES", "+20 %", "−20 %"]
    for i, v in enumerate(vals):
        if v is None:
            continue
        h = float(v) * sc
        col = GREEN if i == 2 and hi == 2 else (GOLD if i == 1 else 0xFF8FA3C8)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(xs[i] - 95, y0 - h, 190, h), 18, 18), fill(col))
        draw_text(c, f"{float(v):g} €", xs[i], y0 - h - 30, 60, WHITE, outline=6)
        draw_text(c, lab[i], xs[i], y0 + 70, 46, WHITE, outline=6)
    c.drawLine(120, y0 - 100 * sc, 960, y0 - 100 * sc, stroke(with_alpha(WHITE, .5), 4))
    draw_text(c, "100 €", 1000, y0 - 100 * sc + 14, 34, with_alpha(WHITE, .7))


def shop_bg(c, t, hide_title=False):
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)], [0xFF15121E, 0xFF07060B])))
    for i in range(18):     # luces de escaparate que parpadean
        x = 60 + i * 56; a = .4 + .4 * math.sin(t * 3 + i * 1.3)
        c.drawCircle(x, 720 + 14 * math.sin(i), 9, fill(with_alpha([GOLD, RED, CYAN, GREEN][i % 4], a)))
    if not hide_title:
        draw_text(c, "BLACK FRIDAY", W / 2, 800, 64, with_alpha(WHITE, .9 + .1 * math.sin(t * 4)), outline=8)


def s_friday(c, t, P, V):
    sid, lt, d = seg(P, t)
    shop_bg(c, t, hide_title=sid in ("s3", "s4"))
    if sid == "h":
        k = ease_io((lt - 1.4) / .8); k2 = ease_io((lt - 3.2) / .8)
        txt = "100 €" if k < .5 else ("120 €" if k2 < .5 else "¿?")
        price_tag(c, W / 2, 1180, txt, 0xFFF2E6C8 if k2 < .5 else 0xFFFFD54A, t, sw=.06)
        pu = 1 + .12 * math.sin(t * 6) * (1 if 1.4 < lt < 2.6 else 0); pd = 1 + .12 * math.sin(t * 6) * (1 if lt > 3.2 else 0)
        K.pill(c, W / 2 - 170, 1540, "+20 %", 64, bg=GOLD, fg=INK, scale=pu)
        draw_text(c, "→", W / 2, 1562, 60, WHITE, outline=6)
        K.pill(c, W / 2 + 170, 1540, "−20 %", 64, bg=RED, fg=WHITE, scale=pd)
    elif sid == "s1":
        price_tag(c, W / 2, 1180, "¿?", 0xFFFFD54A, t, sw=.08)
        if d - lt <= 5:
            n = max(0, int(math.ceil(d - lt)))
            hc.big(c, f"{n}", W / 2, 1640, 150, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    elif sid == "s2":
        price_tag(c, W / 2, 1180, "100 €", 0xFFF2E6C8, t, sw=.05, strike=lt > d * .55)
        if lt > d * .55:
            K.pill(c, W / 2, 1560, "¿SUBE 20 Y BAJA 20?", 52, bg=0xEE000000, fg=RED)
    elif sid == "s3":
        k = ease_io(lt / 1.2)
        bars(c, [P0, P0 + (P1 - P0) * Fr(round(k * 100), 100), None], t)
        if lt > 1.8:
            K.pill(c, W / 2, 1620, "20 % DE 120 = 24 €", 56, bg=0xEE000000, fg=GOLD, scale=K.ease_back(K.prog(lt, 1.8, 2.1)))
    elif sid == "s4":
        k = ease_io((lt - .3) / 2.0)
        bars(c, [P0, P1, P1 - CUT * Fr(round(k * 100), 100)], t, hi=2 if k >= 1 else None)
        if k >= 1:
            K.pill(c, W / 2, 1620, "96 €: PAGAS 4 € MENOS", 56, bg=0xEE000000, fg=GREEN, scale=K.ease_back(K.prog(lt, 2.3, 2.6)))
    else:
        price_tag(c, W / 2, 1000, "96 €", 0xFF8BE3A8, t, sw=.05, s=.8)


V3502 = dict(slug="3502_black_friday_20", accent=GOLD, drone=0.02, scene=s_friday, mood="misterio",
             send="ENVÍASELO A QUIEN SE VA DE COMPRAS", dare=("s1", "RETA A UN AMIGO YA", 1840),
             vote=("s4", ("IGUAL", "MENOS"), 1, 1740),
             rehook=("s3", "ESPERA… NO SE QUEDA EN 100"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Hoy es Black Friday. Un precio de cien euros sube un veinte por ciento, y luego lo rebajan un veinte por ciento. ¿Cuánto pagas?",
         cap="¿Cuánto *PAGAS*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos para pensarlo, sin calculadora.",
         cap="*5 segundos*", hold=2.6),
    dict(id="s2", who="nar", cut=True, say="Lo que sale rápido es decir cien euros, porque sube veinte y baja veinte.",
         cap="¿Los mismos *100 €*?", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero la rebaja se calcula sobre ciento veinte, y su veinte por ciento son veinticuatro euros.",
         cap="20 % de 120 = *24 €*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Esta cuenta dice que ciento veinte menos veinticuatro son noventa y seis euros, cuatro menos que al principio.",
         cap="Pagas *96 €*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta qué habías dicho, y envíaselo a quien se vaya hoy de compras.",
         cap="¿Qué dijiste tú? | *COMENTA*"),
])

VIDEOS = {"3501": V3501, "3502": V3502}


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
