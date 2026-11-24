"""Producción 24/11/2026 (3201 y 3202, motor 2D; 3203 mito_calcetines.py y 3204 serie_reves.py en 3D; sin ciudad: IGEV01 330 < 332).
  3201 PRUEBA EN DIRECTO: EL CUADRADO QUE RESPIRA. Un cuadrado azul de tamaño constante gira despacio detrás de cuatro cuadros naranjas
       que tapan sus esquinas; casi todo el mundo lo ve hincharse y encogerse. Michael Bach ('Breathing Square'): 'to nearly every observer
       it looks like the square is changing its size', 'of constant size which slowly rotates'; cita a Shiffrar y Pavel (1991) y Bruno (2001).
       steady=True (sin zoom ni sacudidas: cualquier cambio de escala de la cámara falsearía la prueba). Assert: mismo número de píxeles azules
       a 0°, 20° y 45° sin los cuadros.
  3202 RETO: los nenúfares. Duplican su superficie cada día y cubren el lago el día 48 → la mitad el DÍA 47 (24 es la respuesta rápida).
       Animación día a día con 256 hojas: el día d hay 256·2^(d−48) (assert: 128 el día 47)."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80
BLUE = 0xFF2F6BFF; ORANGE = 0xFFFF8A1E


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


# ============================ 3201 el cuadrado que respira
CX, CY, A = W / 2, 1040, 235          # centro y medio lado del cuadrado azul (constante)
D, HH = 255, 192                     # cuadros naranjas en (±D, ±D) con medio lado HH → huecos de 2·(D−HH) en los ejes


def breathing(c, ang, occ=1.0, outline=0.0):
    c.drawRect(skia.Rect.MakeWH(W, H), fill(0xFFF4F1EA))
    c.save(); c.translate(CX, CY); c.rotate(ang)
    c.drawRect(skia.Rect.MakeXYWH(-A, -A, 2 * A, 2 * A), fill(BLUE))
    c.restore()
    if occ > 0:
        for sx in (-1, 1):
            for sy in (-1, 1):
                c.drawRect(skia.Rect.MakeXYWH(CX + sx * D - HH, CY + sy * D - HH, 2 * HH, 2 * HH), fill(with_alpha(ORANGE, occ)))
    if outline > 0:      # contorno fijo del cuadrado: demuestra que no cambia de tamaño
        c.save(); c.translate(CX, CY); c.rotate(ang)
        c.drawRect(skia.Rect.MakeXYWH(-A, -A, 2 * A, 2 * A), stroke(with_alpha(0xFF0B0D14, outline), 8))
        c.restore()
    c.drawCircle(CX, CY, 9, fill(0xFF0B0D14))   # punto de fijación


def _assert_breathing():
    n = []
    for ang in (0, 20, 45):
        surf = skia.Surface(W, H); cc = surf.getCanvas(); breathing(cc, ang, occ=0.0)
        a = surf.makeImageSnapshot().toarray()[..., :3].astype(int)   # BGRA → B,G,R
        n.append(int(((a[..., 0] > 200) & (a[..., 2] < 90)).sum()))
    assert max(n) / min(n) < 1.01, n
    assert D + HH > A * math.sqrt(2) + 20 and D - HH > 40


_assert_breathing()
SPIN = 22.0   # grados por segundo, constante


def s_breath(c, t, P, V):
    sid, lt, d = seg(P, t)
    occ, outl = 1.0, 0.0
    if sid == "s2":
        occ = 1 - .82 * ease_io((lt - .6) / 1.0); outl = ease_io((lt - 1.8) / .6)
    elif sid == "s3":
        occ = .18 + .82 * ease_io((lt - .2) / .9); outl = 1 - ease_io((lt - .2) / .5)
    breathing(c, t * SPIN, occ, outl)
    if sid == "h":
        K.pill(c, W / 2, 1590, "¿CAMBIA DE TAMAÑO?", 54, bg=0xEE000000, fg=GOLD)
    if sid == "s1" and lt > 1.0:
        K.tag(c, W / 2, 1590, "MIRA EL PUNTO DEL CENTRO", lt - 1.0, accent=GOLD, size=42)
    if sid == "s2" and lt > 2.2:
        K.tag(c, W / 2, 1590, "SIEMPRE EL MISMO TAMAÑO", lt - 2.2, accent=GREEN, size=44)
    if sid == "s4" and lt > 1.2:
        K.tag(c, W / 2, 1590, "CUADRADO QUE RESPIRA · MICHAEL BACH", lt - 1.2, accent=GOLD, size=36)
        if lt > 2.4:
            K.tag(c, W / 2, 1670, "SHIFFRAR Y PAVEL, 1991", lt - 2.4, accent=WHITE, size=30)


V3201 = dict(slug="3201_cuadrado_que_respira", accent=GOLD, drone=0.015, scene=s_breath, mood="misterio", music=0.04, clean=True, steady=True,
             send="ENVÍASELO Y QUE TE DIGA SI RESPIRA", vote=("s2", ("SÍ", "NO"), 1, 1740),
             rehook=("s3", "AHORA VUELVE A MIRAR"), reveal=("s2", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿El cuadrado azul se hace más grande y más pequeño? Míralo bien antes de contestar.",
         cap="¿Cambia de *TAMAÑO*?", hold=0.8),
    dict(id="s1", who="nar", cut=True, say="Mira el punto del centro. Casi todo el mundo lo ve hincharse y encogerse, como si respirara.",
         cap="Parece que *RESPIRA*", hold=0.6),
    dict(id="s2", who="nar", cut=True, say="Ahora quito los cuadros naranjas. El cuadrado solo gira, y siempre tiene el mismo tamaño.",
         cap="*EL MISMO TAMAÑO*", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Vuelvo a ponerlos, y otra vez parece que respira, aunque ya sabes que no cambia.",
         cap="Otra vez *RESPIRA*", hold=0.7),
    dict(id="s4", who="nar", cut=True, say="Tu cerebro solo ve trozos de los lados, y se inventa el resto mal.",
         cap="Tu cerebro *SE INVENTA* | el resto", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo viste respirar, y envíaselo a alguien para ver si le pasa lo mismo.",
         cap="¿Lo viste respirar? | *COMENTA*"),
])


# ============================ 3202 los nenúfares
FULL, NPAD = 48, 256
LX0, LX1, LY0, LY1 = 70, W - 70, 520, 1500


def pads_at(day):
    return int(round(NPAD * 2.0 ** (day - FULL)))


assert pads_at(47) == NPAD // 2 and pads_at(48) == NPAD and FULL / 2 == 24
_rng = np.random.default_rng(3202)
_cols, _rows = 16, 16
PADS = []
for i in range(_cols):
    for j in range(_rows):
        x = LX0 + (i + .5) * (LX1 - LX0) / _cols + _rng.uniform(-9, 9)
        y = LY0 + (j + .5) * (LY1 - LY0) / _rows + _rng.uniform(-8, 8)
        PADS.append((x, y, _rng.uniform(0, 6.28), _rng.uniform(.9, 1.1)))
# orden de crecimiento: de izquierda a derecha (la mitad = la mitad izquierda del lago), con un poco de ruido en la frontera
PADS.sort(key=lambda p: p[0] + 18 * math.sin(p[1] * .05))
assert all(p[0] < W / 2 + 40 for p in PADS[:NPAD // 2])
RX, RY = (LX1 - LX0) / _cols * .62, (LY1 - LY0) / _rows * .62


def pad(c, x, y, rot, s, a, t):
    c.save(); c.translate(x, y); c.rotate(math.degrees(rot) + 6 * math.sin(t * 1.3 + x)); c.scale(s * a, s * a)
    p = skia.Path(); p.addOval(skia.Rect.MakeXYWH(-RX, -RY, 2 * RX, 2 * RY))
    cut = skia.Path(); cut.moveTo(0, 0); cut.lineTo(RX * 1.2, -RY * .25); cut.lineTo(RX * 1.2, RY * .25); cut.close()
    p = skia.Op(p, cut, skia.PathOp.kDifference_PathOp)
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(-RX * .2, -RY * .2), RX * 1.2, [0xFF6CC24A, 0xFF2E7A2E]), AntiAlias=True))
    c.drawPath(p, stroke(0xFF1E5A22, 3))
    c.restore()


def lake(c, t, day_f):
    c.drawRect(skia.Rect.MakeWH(W, H), fill(0xFF5E8A3A))
    for i in range(70):                                       # hierba de la orilla
        x = (i * 151) % W; y = (i * 83) % H
        if LY0 - 40 < y < LY1 + 40 and LX0 - 40 < x < LX1 + 40:
            continue
        c.drawLine(x, y, x + 6 * math.sin(t + i), y - 26, stroke(0xFF7AB04A, 5))
    r = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(LX0 - 18, LY0 - 18, LX1 + 18, LY1 + 18), 60, 60)
    c.drawRRect(r, fill(0xFF8A6A42))
    r2 = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(LX0, LY0, LX1, LY1), 48, 48)
    c.drawRRect(r2, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, LY0), skia.Point(0, LY1)], [0xFF2F7FB8, 0xFF1A4F80]), AntiAlias=True))
    c.save(); c.clipRRect(r2, doAntiAlias=True)
    for i in range(14):                                       # brillos del agua
        x = LX0 + ((i * 97 + t * 35) % (LX1 - LX0)); y = LY0 + (i * 71) % (LY1 - LY0)
        c.drawLine(x, y, x + 40, y, stroke(0x44FFFFFF, 4))
    n = NPAD * 2.0 ** (day_f - FULL)
    for k, (x, y, rot, s) in enumerate(PADS):
        if k + 1 <= n:
            a = 1.0
        elif k < n:
            a = n - k
        else:
            break
        a = ease_out(clamp(a))
        if a > .02:
            pad(c, x, y, rot, s, a, t)
    c.restore()


def s_lily(c, t, P, V):
    sid, lt, d = seg(P, t)
    day = None
    if sid in ("h", "s1", "s2"):
        day_f = 48.0 if sid == "h" else 44.0
        day = 48 if sid == "h" else None
    elif sid == "s3":                                          # días 40 → 46, uno por paso
        u = clamp(lt / (d - .3)); day_f = 40 + 6 * u; day = int(day_f)
    elif sid == "s4":                                          # 46 → 47 (mitad) … y 48 (entero)
        day_f = 48 - ease_io((lt - d * .42) / 1.0); day = 48 if day_f > 47.5 else 47   # lleno el 48 → un día atrás: la mitad
    else:
        day_f = 47.0; day = 47
    lake(c, t, day_f)
    if sid == "s4" and day_f < 47.05:                         # línea de la mitad
        a = ease_out(clamp((lt - d * .42 - 1.0) / .4))
        c.drawLine(W / 2, LY0 - 30, W / 2, LY1 + 30, stroke(with_alpha(GOLD, a), 8))
        K.pill(c, W / 2, LY0 - 70, "LA MITAD", 46, bg=0xEE000000, fg=GOLD, alpha=a)
    if sid == "cta":
        c.drawLine(W / 2, LY0 - 30, W / 2, LY1 + 30, stroke(GOLD, 8))
    if sid in ("h", "s1"):
        K.pill(c, W / 2, 1600, "×2 CADA DÍA · LLENO EL DÍA 48", 40, bg=0xEE000000, fg=WHITE)
        K.pill(c, W / 2, 1700, "¿CUÁNDO CUBREN LA MITAD?", 48, bg=0xEE000000, fg=GOLD)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1010, 240, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2":
        a = ease_out(clamp((lt - .3) / .4))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - 300, 1620, 600, 150), 30, 30), fill(with_alpha(0xFF000000, .85 * a)))
        draw_text(c, "¿24 días?", W / 2, 1720, int(76 * (.7 + .3 * a)), with_alpha(RED, a), outline=6)
        if lt > 1.4:
            K.tag(c, W / 2, 1830, "48 ÷ 2 = 24", lt - 1.4, accent=WHITE, size=40)
    if day is not None and sid != "h":
        frac = 2.0 ** (day - FULL)
        txt = "TODO" if day >= 48 else ("LA MITAD" if day == 47 else f"1/{int(round(1 / frac))}")
        K.pill(c, 260, 1610, f"DÍA {day}", 56, bg=0xEE000000, fg=GREEN if day >= 47 else GOLD)
        K.pill(c, W - 270, 1610, txt, 50, bg=0xEE000000, fg=WHITE)


V3202 = dict(slug="3202_nenufares_mitad_del_lago", accent=GOLD, drone=0.02, scene=s_lily, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1840),
             rehook=("s3", "ESPERA… MIRA LOS ÚLTIMOS DÍAS"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Estos nenúfares duplican su tamaño cada día, y cubren el lago entero el día cuarenta y ocho. ¿Qué día cubren la mitad?",
         cap="¿Cuándo cubren *LA MITAD*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos para pensarlo, sin hacer trampa.",
         cap="*5 segundos*", hold=2.6),
    dict(id="s2", who="nar", cut=True, say="Lo que sale rápido es veinticuatro, porque es la mitad de cuarenta y ocho.",
         cap="¿*24 días*?", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero mira los últimos días: cada día ocupan el doble que el día anterior.",
         cap="Cada día, | *EL DOBLE*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Si el día cuarenta y ocho cubren todo el lago, el día anterior cubrían la mitad: el día cuarenta y siete.",
         cap="La mitad: | *DÍA 47*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta qué habías dicho, y envíaselo a un amigo para ver si dice veinticuatro.",
         cap="¿Qué dijiste tú? | *COMENTA*"),
])

VIDEOS = {"3201": V3201, "3202": V3202}


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
