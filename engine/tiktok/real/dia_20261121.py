"""Producción 21/11/2026 (2901 y 2902, motor 2D; 2903 mito_dossuenos.py y 2904 serie_lunag.py en 3D; sin ciudad: IGEV01 331 < 332).
  2901 PRUEBA EN DIRECTO: ILUSIÓN DE LA ACUARELA. Forma con borde morado oscuro y franja naranja por dentro: el interior blanco se ve
       teñido de naranja. Wikipedia (Watercolor illusion): 'Baingio Pinna discovered the watercolor illusion in 1987'; Pinna, Brelstaff y
       Spillmann, Vision Research 41(20):2669-2676 (2001), 'Surface color from boundaries: a new watercolor illusion'; 'a white area takes
       on a pale tint of a thin, bright, intensely colored polygon...'. Assert: el interior (lejos del borde) y el fondo son blanco puro.
  2902 RETO: ¿en qué plaza está el coche? 16, 06, 68, 88, [coche], 98 → girado 180°: 86, [87], 88, 89, 90, 91 → 87.
       Mental Floss (28/02/2018): 'The answer is 87!', 'flip your screen upside down', 'often attributed to a Hong Kong admissions test
       for first graders, which ... may not be true'; Business Insider: 'elementary school entrance exam in Hong Kong', '20 seconds'.
       Assert: los números girados son consecutivos y el hueco es el 87."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80; PINK = 0xFFFF5FA8
PURP = 0xFF4A1A7A; ORANGE = 0xFFFF9A1F; GREENF = 0xFF2FC24A; DKRED = 0xFF7A1430


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


# ============================ 2901 ilusión de la acuarela
SCX, SCY, SR = W / 2, 1150, 360


def blob(cx, cy, R, ph=0.0, n=19, amp=.05):
    p = skia.Path()
    for i in range(721):
        a = math.radians(i / 2)
        r = R * (1 + amp * math.sin(n * a + ph) + .03 * math.sin(3 * a - ph * .5))
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        (p.moveTo if i == 0 else p.lineTo)(x, y)
    p.close(); return p


def watercolor(c, cx, cy, R, ph, inner=ORANGE, outer=PURP, fringe=1.0, band=11):
    """Borde oscuro + franja interior de color (técnica de Pinna). fringe 0..1 hace aparecer o desaparecer la franja interior."""
    p = blob(cx, cy, R, ph)
    if fringe > 0:
        c.save(); c.clipPath(p, doAntiAlias=True)
        c.drawPath(p, skia.Paint(Color=with_alpha(inner, fringe), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=band * 3.2,
                                 StrokeJoin=skia.Paint.kRound_Join))
        c.restore()
    c.drawPath(p, skia.Paint(Color=outer, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=band * 1.6, StrokeJoin=skia.Paint.kRound_Join))


def _assert_white():
    surf = skia.Surface(1000, 1000); cc = surf.getCanvas(); cc.clear(0xFFFFFFFF)
    watercolor(cc, 500, 500, 360, 0.7)
    a = surf.makeImageSnapshot().toarray()[..., :3].astype(int)
    assert (a[500, 500] == 255).all() and (a[400:600, 400:600] == 255).all(), "el interior no es blanco"
    assert (a[20, 20] == 255).all() and (a[980, 980] == 255).all()
    assert (a != 255).any()  # sí hay borde de color


_assert_white()


TOP, BOT, RR = (W / 2, 1000), (W / 2, 1480), 215


def s_acuarela(c, t, P, V):
    """Dos formas iguales: la de ARRIBA con franja naranja fina por dentro del borde morado, la de ABAJO solo con el borde morado.
    La de arriba parece teñida de naranja; las dos son blanco puro por dentro (assert en _assert_white)."""
    sid, lt, d = seg(P, t)
    c.clear(0xFFFFFFFF)
    ph = t * .35
    fringe, inner = 1.0, ORANGE
    if sid == "s3":                                    # quito la franja y la vuelvo a poner
        fringe = 1 - ease_io((lt - d * .45) / .5) + ease_io((lt - d * .78) / .4)
    if sid in ("s4", "cta"):                           # misma forma con franja verde: ahora se ve verdosa
        inner = GREENF
    bob = 10 * math.sin(t * 1.1)
    watercolor(c, TOP[0], TOP[1] + bob, RR, ph, inner=inner, fringe=fringe, band=7)
    watercolor(c, BOT[0], BOT[1] - bob, RR, ph + 1.3, inner=inner, fringe=0.0, band=7)
    if sid == "h":
        K.pill(c, W / 2, 1780, "¿CUÁL ESTÁ PINTADA? ¿ARRIBA o ABAJO?", 44, bg=with_alpha(0xFF000000, .85), fg=GOLD)
    if sid == "s2":                                    # cuentagotas en el centro de las dos: blanco puro
        a = ease_out(clamp((lt - .5) / .4))
        for (px, py) in (TOP, BOT):
            c.drawCircle(px, py, 34 * a, stroke(with_alpha(INK, a), 7)); c.drawCircle(px, py, 6 * a, fill(with_alpha(RED, a)))
            if lt > .8:
                K.pill(c, px, py + 70, "R 255 · G 255 · B 255", 38, bg=0xEE000000, fg=WHITE, alpha=a)
    if sid == "s3" and lt > .3 and lt < d * .45:        # lupa sobre el borde de la de arriba
        a = ease_out(clamp((lt - .3) / .4))
        mx, my, mr = W / 2 + 250, 760, 150
        c.save(); p = skia.Path(); p.addCircle(mx, my, mr * a); c.clipPath(p, doAntiAlias=True)
        c.drawCircle(mx, my, mr, fill(0xFFFFFFFF))
        c.translate(mx, my); c.scale(4, 4); c.translate(-(TOP[0] + RR * .98), -(TOP[1] + bob))
        watercolor(c, TOP[0], TOP[1] + bob, RR, ph, inner=inner, fringe=1.0, band=7)
        c.restore()
        c.drawCircle(mx, my, mr * a, stroke(INK, 8))
        c.drawLine(mx - mr * .7 * a, my + mr * .7 * a, TOP[0] + RR * .95, TOP[1] + bob, stroke(with_alpha(INK, a), 6))
    if sid == "s3" and lt > d * .45:
        K.tag(c, W / 2, 1780, "SIN LA FRANJA: IGUALES" if fringe < .5 else "CON LA FRANJA", lt - d * .45, accent=GOLD, size=42)
    if sid == "s4" and lt > 1.0:
        K.tag(c, W / 2, 1780, "ILUSIÓN DE LA ACUARELA · BAINGIO PINNA, 1987", lt - 1.0, accent=GOLD, size=34)


V2901 = dict(slug="2901_ilusion_de_la_acuarela", accent=GOLD, drone=0.015, scene=s_acuarela, mood="luz", music=0.04,
             send="ENVÍASELO Y QUE TE DIGA QUÉ VE", dare=("s1", "PREGÚNTASELO A ALGUIEN", 1840),
             rehook=("s2", "AHORA MIRA ESTO"), reveal=("s3", "EL TRUCO"), segs=[
    dict(id="h", who="nar", say="¿Cuál de estas dos formas está pintada por dentro, la de arriba o la de abajo?",
         cap="¿Cuál está *PINTADA*?", hold=0.8),
    dict(id="s1", who="nar", cut=True, say="Casi todo el mundo ve la de arriba teñida de naranja clarito, como si fuera acuarela.",
         cap="¿La de arriba | *naranja*?", hold=0.5),
    dict(id="s2", who="nar", cut=True, say="Pero si mido el centro de las dos, las dos son blanco puro, igual que el fondo.",
         cap="Las dos: *BLANCO PURO*", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="La única diferencia es una franja naranja muy fina en el borde: si la quito, son iguales.",
         cap="Solo una *franja* | en el borde", hold=1.0),
    dict(id="s4", who="nar", cut=True, say="Es la ilusión de la acuarela: tu cerebro rellena la forma con el color de su borde.",
         cap="Tu cerebro | *rellena* el color", hold=0.8),
    dict(id="cta", who="nar", cut=True, say="Comenta si viste el naranja, y envíaselo a alguien para ver si le pasa lo mismo.",
         cap="¿Viste el naranja? | *COMENTA*"),
])


# ============================ 2902 ¿en qué plaza está el coche?
NUMS = ["16", "06", "68", "88", None, "98"]
FLIP = {"0": "0", "1": "1", "6": "9", "8": "8", "9": "6"}
def flip(s): return "".join(FLIP[ch] for ch in reversed(s))
_rot = [flip(n) if n else None for n in reversed(NUMS)]
_vals = [int(x) if x else None for x in _rot]
_gap = _rot.index(None)
assert _vals[0] == 86 and all(_vals[i] == 86 + i for i in range(6) if _vals[i] is not None)
ANS = 86 + _gap
assert ANS == 87  # el hueco es el 87 (visto del revés, "L8")

LCX, LCY = W / 2, 1150
SW_, SH_ = 150, 360


def car(c, x, y, s=1.0, col=0xFFE0343A):
    c.save(); c.translate(x, y); c.scale(s, s)
    for wx, wy in ((-58, -105), (58, -105), (-58, 105), (58, 105)):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(wx - 14, wy - 28, 28, 56), 8, 8), fill(0xFF15161C))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-62, -150, 124, 300), 46, 46), fill(col))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-50, -80, 100, 60), 18, 18), fill(0xFF1C2A3E))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-50, 50, 100, 46), 16, 16), fill(0xFF1C2A3E))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-46, -18, 92, 64), 14, 14), fill(with_alpha(0xFF000000, .12)))
    for hx in (-40, 40):
        c.drawCircle(hx, -142, 10, fill(0xFFFFF2B0))
    c.restore()


def lot(c, t, rot=0.0, wob=0.0):
    c.save(); c.translate(LCX, LCY); c.rotate(rot + wob)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-500, -330, 1000, 660), 30, 30), fill(0xFF3A3D44))
    rng = np.random.default_rng(3)
    for _ in range(260):                               # grano del asfalto
        x, y = rng.uniform(-490, 490), rng.uniform(-320, 320)
        c.drawCircle(x, y, rng.uniform(1, 3), fill(0x22FFFFFF if rng.random() < .5 else 0x22000000))
    x0 = -3 * SW_
    for i in range(7):
        c.drawRect(skia.Rect.MakeXYWH(x0 + i * SW_ - 4, -SH_ / 2 - 40, 8, SH_), fill(0xFFF2F2F2))
    c.drawRect(skia.Rect.MakeXYWH(x0 - 4, -SH_ / 2 - 40, 6 * SW_ + 8, 8), fill(0xFFF2F2F2))
    for i, n in enumerate(NUMS):
        cx = x0 + (i + .5) * SW_
        if n:
            draw_text(c, n, cx, 40, 96, 0xFFF4F4F4, outline=0)
        else:
            car(c, cx, -10, .95)
    c.restore()


def s_parking(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)], [0xFF4A7A3A, 0xFF35602B]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    for i in range(30):                                # hojas que caen despacio (movimiento constante)
        x = (i * 263 + 40 * math.sin(t + i)) % W; y = ((t * 50 + i * 211) % (H + 100)) - 50
        c.drawCircle(x, y, 7, fill(0x55C9E27A))
    rot = 0.0
    if sid == "s3":
        rot = 180 * ease_io((lt - d * .45) / 1.4)
    elif sid in ("s4", "cta"):
        rot = 180
    wob = 1.2 * math.sin(t * 1.1) if sid in ("h", "s1", "s2") else 0
    lot(c, t, rot, wob)
    if sid == "h":
        K.pill(c, W / 2, 1640, "¿QUÉ NÚMERO TAPA EL COCHE?", 54, bg=0xEE000000, fg=GOLD)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1620, 120, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s1" and lt > .6:
        K.tag(c, W / 2, 1780, "SIN CUENTAS", lt - .6, accent=GOLD, size=44)
    if sid == "s2" and lt > .6:
        K.tag(c, W / 2, 1640, "NO HAY FÓRMULA", lt - .6, accent=RED, size=48)
    if sid == "s3" and lt < d * .45 and lt > .4:
        K.tag(c, W / 2, 1640, "MÍRALO DESDE EL COCHE", lt - .4, accent=CYAN, size=46)
    if sid in ("s4", "cta"):
        k = ease_out(clamp(lt / .5)) if sid == "s4" else 1
        cx = LCX + (-3 * SW_ + (_gap + .5) * SW_)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 92, LCY - 300, 184, 140), 26, 26), fill(with_alpha(0xFF0B0B16, .9 * k)))
        draw_text(c, str(ANS), cx, LCY - 196, int(100 * (.6 + .4 * k)), with_alpha(GREEN, k), outline=8)
        if sid == "s4" and lt > 1.2:
            K.tag(c, W / 2, 1640, "86 · 87 · 88 · 89 · 90 · 91", lt - 1.2, accent=GREEN, size=48)


V2902 = dict(slug="2902_en_que_plaza_esta_el_coche", accent=GOLD, drone=0.02, scene=s_parking, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1840),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s3", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿En qué plaza está aparcado el coche? Dicen que es de un examen para niños de seis años.",
         cap="¿En qué plaza está *EL COCHE*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos, y no hace falta hacer ninguna cuenta.",
         cap="*5 segundos*. | Sin cuentas", hold=3.4),
    dict(id="s2", who="nar", cut=True, say="Casi todo el mundo se pone a buscar una fórmula con los números, y no la hay.",
         cap="No hay *fórmula*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="El truco es mirarlo desde el sitio del conductor, así que dale la vuelta a la imagen.",
         cap="*DALE LA VUELTA*", hold=1.0),
    dict(id="s4", who="nar", cut=True, say="Ahora los números van seguidos, del ochenta y seis al noventa y uno, y el coche tapa la ochenta y siete.",
         cap="El coche está en la *87*", hold=0.8),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo sacaste, y envíaselo a un amigo para ver cuánto tarda.",
         cap="¿Lo sacaste? | *COMENTA*"),
])

VIDEOS = {"2901": V2901, "2902": V2902}


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
