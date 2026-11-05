"""Producción 05/11/2026 (1301–1302, motor actual; 1303–1304 en 3D aparte: mito_chicle.py, serie_luna.py).
  1301 ILUSIÓN EN DIRECTO: Pinna y Brelstaff, 'A new visual illusion of relative motion', Vision Research 40 (2000) 2091–2096 (Michael Bach, MathWorld).
       Inclinación ±20° con polaridad alterna: comprobado con flujo óptico (Lucas-Kanade sobre zoom simulado: componente tangencial de signo opuesto en aros vecinos; a 45° desaparece).
  1302 RETO: ruedas dentadas: 5 en círculo (ciclo impar) => bloqueo. Sentidos y bloqueo CALCULADOS por parejas de engrane (assert)."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; PINK = 0xFFFF5FC8


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 1301 aros que giran (imagen QUIETA)
CX, CY = 540, 1168
RINGS = [(400, 46, 20, 1), (285, 34, -20, -1), (175, 22, 20, 1)]
_ring = None


def ring_image():
    global _ring
    if _ring is not None:
        return _ring
    S = 2  # supermuestreo: los bordes finos no deben hacer moiré
    sf = skia.Surface(1000 * S, 1000 * S); c = sf.getCanvas(); c.clear(0)
    c.scale(S, S)
    c.drawCircle(500, 500, 468, fill(0xFF808080))
    for r, n, ti, po in RINGS:
        for k in range(n):
            th = 2 * math.pi * k / n; cx, cy = 500 + r * math.cos(th), 500 + r * math.sin(th); a = math.degrees(th) + ti
            c.save(); c.translate(cx, cy); c.rotate(a)
            hw = 20
            pts = [(-hw, -hw), (hw, -hw), (hw, hw), (-hw, hw)]
            cols = (0xFFFFFFFF, 0xFFFFFFFF, 0xFF000000, 0xFF000000) if po > 0 else (0xFF000000, 0xFF000000, 0xFFFFFFFF, 0xFFFFFFFF)
            for i in range(4):
                p = stroke(cols[i], 4.4); p.setStrokeCap(skia.Paint.kSquare_Cap)
                c.drawLine(*pts[i], *pts[(i + 1) % 4], p)
            c.restore()
    # cruz de fijación
    c.drawRect(skia.Rect.MakeXYWH(500 - 26, 500 - 5, 52, 10), fill(0xFF1E5BFF))
    c.drawRect(skia.Rect.MakeXYWH(500 - 5, 500 - 26, 10, 52), fill(0xFF1E5BFF))
    _ring = sf.makeImageSnapshot()
    return _ring


def phone_icon(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-30, -54, 60, 108), 12, 12)
    c.drawRRect(r, fill(with_alpha(0xFF10131F, a))); c.drawRRect(r, stroke(with_alpha(WHITE, a), 5))
    c.drawCircle(0, 0, 13, stroke(with_alpha(WHITE, a), 3))
    c.restore()


def s_aros(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.clear(0xFF0C0E16)
    img = ring_image()
    k = 0.42 if sid == "cta" else 1.0
    p = skia.Paint(); p.setAlphaf(k); p.setAntiAlias(True)
    samp = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
    c.drawImageRect(img, skia.Rect.MakeXYWH(CX - 500, CY - 500, 1000, 1000), samp, p)
    if sid in ("h", "s1", "s2"):
        u = 0.5 + 0.5 * math.sin(t * 2.1)
        phone_icon(c, 540, 1752, 0.8 + 0.5 * u, 1.0)
        draw_text(c, "ACERCA", 300, 1768, 46, with_alpha(WHITE, 0.45 + 0.55 * u))
        draw_text(c, "ALEJA", 780, 1768, 46, with_alpha(WHITE, 1 - 0.55 * u))
    if sid == "s3":  # marcas FIJAS: la prueba de que nada se mueve
        for j, ang in enumerate(range(0, 360, 45)):
            on = clamp((lt - 0.2 - j * 0.1) / 0.2)
            if on <= 0:
                continue
            a = math.radians(ang + 22.5)
            pa = stroke(with_alpha(RED, on), 7); pa.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawLine(CX + 120 * math.cos(a), CY + 120 * math.sin(a), CX + 450 * math.cos(a), CY + 450 * math.sin(a), pa)
        K.tag(c, W / 2, 1740, "CERO PÍXELES SE MUEVEN", lt - 1.0, accent=RED, size=46)
    if sid == "s4":
        K.tag(c, W / 2, 1740, "PINNA Y BRELSTAFF, 2000", lt - 0.3, accent=GOLD, size=46)


V1301 = dict(slug="1301_aros_que_giran", accent=GOLD, drone=0.015, scene=s_aros, mood="misterio", steady=True, clean=True,
             send="ENVÍASELO: ¿A ÉL TAMBIÉN LE GIRAN?", rehook=("s2", "¿GIRAN O NO GIRAN?"), reveal=("s3", "LA PRUEBA"), segs=[
    dict(id="h", who="nar", say="Esta imagen está quieta, pero si acercas el móvil, los aros van a girar.", cap="Acerca el móvil: ¿los aros *GIRAN*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Mira la cruz azul sin apartar los ojos, y acerca y aleja la pantalla, despacio, varias veces.", cap="Mira la *CRUZ* | y *acerca y aleja* | la pantalla", hold=1.5),
    dict(id="s2", who="nar", cut=True, say="¿Lo notas? Cada aro gira hacia un lado distinto, y cuando alejas el móvil, cambian de sentido.", cap="Cada aro gira | a un *lado distinto*", hold=1.0),
    dict(id="s3", who="nar", cut=True, say="Te pongo unas líneas rojas encima, y verás que no se ha movido ni un solo píxel.", cap="Líneas *ROJAS*: | no se mueve *NADA*", hold=1.0),
    dict(id="s4", who="nar", cut=True, say="La describieron Pinna y Brelstaff en el año dos mil. Tu cerebro lee mal esas piezas, y se inventa el giro.", cap="Tu cerebro *se inventa* | el giro", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="¿Te han girado los aros? Comenta sí o no, y mándaselo a alguien.", cap="¿Te han girado? | Comenta *SÍ* o *NO*"),
])

# ============================ 1302 ruedas dentadas
MOD = 2 * math.pi * 110 / 24  # paso entre dientes
def rad(n):
    return n * MOD / (2 * math.pi)
PC = (590.0, 1262.0); RP = 2 * rad(24) / (2 * math.sin(math.pi / 5))
G = {}
for i, ang in enumerate([162, 90, 18, 306, 234]):  # pentágono: índices 0(entrada) 1 2(salida) 3 4
    a = math.radians(ang)
    G[f"p{i}"] = dict(n=24, x=PC[0] + RP * math.cos(a), y=PC[1] - RP * math.sin(a))
def attach(name, base, n, dx, dy):
    b = G[base]; d = rad(b["n"]) + rad(n); l = math.hypot(dx, dy)
    G[name] = dict(n=n, x=b["x"] + d * dx / l, y=b["y"] + d * dy / l)
attach("a", "p0", 21, -0.60, -0.80)
attach("m", "a", 21, 0.20, -0.98)
attach("r", "p2", 21, 0.74, -0.67)
EDGES = [("m", "a"), ("a", "p0"), ("p0", "p1"), ("p1", "p2"), ("p2", "r"), ("p0", "p4"), ("p4", "p3"), ("p3", "p2")]
for u, v in EDGES:  # engrane exacto
    d = math.hypot(G[u]["x"] - G[v]["x"], G[u]["y"] - G[v]["y"])
    assert abs(d - rad(G[u]["n"]) - rad(G[v]["n"])) < 1.0, (u, v, d)
names = list(G)
for i, u in enumerate(names):  # nadie más se toca
    for v in names[i + 1:]:
        if (u, v) in EDGES or (v, u) in EDGES:
            continue
        d = math.hypot(G[u]["x"] - G[v]["x"], G[u]["y"] - G[v]["y"])
        assert d > rad(G[u]["n"]) + rad(G[v]["n"]) + 12, (u, v, d)
for g in G.values():
    assert g["x"] + rad(g["n"]) < 1050 and g["x"] - rad(g["n"]) > 30 and g["y"] - rad(g["n"]) > 700 and g["y"] + rad(g["n"]) < 1660, g
TOP = ["m", "a", "p0", "p1", "p2", "r"]; LOW = ["m", "a", "p0", "p4", "p3", "p2", "r"]
def dir_along(path):
    return {g: (1 if i % 2 == 0 else -1) for i, g in enumerate(path)}  # +1 = horario
DT, DL = dir_along(TOP), dir_along(LOW)
assert DT["r"] == -1 and DL["r"] == 1 and DT["p2"] != DL["p2"]  # por arriba: IZQUIERDA; por abajo: DERECHA; ciclo impar = bloqueo
# fase de cada rueda para que los dientes casen (en árbol; el círculo se cierra con la última)
G["m"]["ph"] = 0.0
for u, v in [("m", "a"), ("a", "p0"), ("p0", "p1"), ("p1", "p2"), ("p2", "r"), ("p0", "p4"), ("p4", "p3")] + [("p3", "p2")]:
    if "ph" in G[v]:
        continue
    gu, gv = G[u], G[v]; th = math.atan2(gv["y"] - gu["y"], gv["x"] - gu["x"])
    gv["ph"] = th + math.pi - (th - gu["ph"]) * gu["n"] / gv["n"] + math.pi / gv["n"]
_gp = {}
def gear_path(n, r):
    if (n, r) in _gp:
        return _gp[(n, r)]
    p = skia.Path(); ra, rb = r + 10, r - 11
    pts = []
    for i in range(n):
        a0 = 2 * math.pi * i / n; w = 2 * math.pi / n
        for f, q in [(-.27, rb), (-.13, ra), (.13, ra), (.27, rb)]:
            pts.append((q * math.cos(a0 + f * w), q * math.sin(a0 + f * w)))
    p.addPoly(pts, True)
    for i in range(5):  # huecos
        a = 2 * math.pi * i / 5; q = r * .55
        p.addCircle(q * math.cos(a), q * math.sin(a), r * .17)
    p.setFillType(skia.PathFillType.kEvenOdd)
    _gp[(n, r)] = p
    return p


def arrow(c, x, y, r, d, col, a=1.0, ph=0.0, w=13):
    """Flecha de giro: d=+1 horario."""
    if a <= 0:
        return
    s = math.degrees(ph); sw = 250 * d
    pa = stroke(with_alpha(col, a), w); pa.setStrokeCap(skia.Paint.kRound_Cap)
    path = skia.Path(); path.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), s, sw); c.drawPath(path, pa)
    e = math.radians(s + sw); ex, ey = x + r * math.cos(e), y + r * math.sin(e); tx, ty = -math.sin(e) * d, math.cos(e) * d; nx, ny = math.cos(e), math.sin(e); L = w * 2.1
    tri = skia.Path(); tri.moveTo(ex + tx * L, ey + ty * L); tri.lineTo(ex + nx * L * .8, ey + ny * L * .8); tri.lineTo(ex - nx * L * .8, ey - ny * L * .8); tri.close()
    c.drawPath(tri, fill(with_alpha(col, a)))


COLS = {1: CYAN, -1: PINK}


def s_ruedas(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.clear(0xFF0B1226)
    # plano técnico con polvo en movimiento
    grid = stroke(0x1A7FB4FF, 2)
    off = (t * 14) % 60
    for i in range(0, 20):
        c.drawLine(i * 60 - off, 0, i * 60 - off, H, grid)
    for i in range(0, 34):
        c.drawLine(0, i * 60 - off, W, i * 60 - off, grid)
    rs = np.random.RandomState(5)
    for i in range(50):
        x = (rs.rand() * W + t * (10 + 30 * rs.rand())) % W; y = (rs.rand() * H - t * (20 + 40 * rs.rand())) % H
        c.drawCircle(x, y, 2 + 3 * rs.rand(), fill(with_alpha(0xFFBFE2FF, .12 + .25 * rs.rand())))
    tl = P["tl"]; a4 = tl["s4"][0]; aC = tl["cta"][0]
    c.save()
    if sid == "cta":
        z = 1 - .36 * K.smooth(lt / .5); c.translate(W / 2, 730); c.scale(z, z); c.translate(-W / 2, -730)
    else:
        z = 1 + .012 * math.sin(t * .9); c.translate(W / 2, 1200); c.scale(z, z); c.translate(-W / 2, -1200)
    jam = 0.0
    if sid == "s4":
        jam = math.exp(-max(0, lt - .25) * 2.2) if lt > .25 else 0
    # giro de las ruedas: solo el tramo que se está explicando; al final, nada
    active, ang = [], 0.0
    if sid == "s1":
        active = ["m", "a", "p0"]; ang = (lt - .3) * 1.1 if lt > .3 else 0
    if sid == "h":
        active = ["m"]; ang = 0.11 * math.sin(t * 5)
    if sid == "s3":
        half = d / 2
        path = TOP if lt < half else LOW; u = lt / half if lt < half else (lt - half) / half
        active = path[:1 + int(u * 1.15 * (len(path) - 1))]; ang = lt * 1.3
    if sid == "s4":
        ang = 0.02 * jam * math.sin(t * 90); active = list(G)
    dsel = DT if sid != "s3" else (DT if lt < d / 2 else DL)
    if sid in ("h", "s1"):
        dsel = DT
    for name, g in G.items():
        r = rad(g["n"]); x, y = g["x"], g["y"]
        if jam:
            x += 7 * jam * math.sin(t * 77 + x); y += 7 * jam * math.cos(t * 83 + y)
        rot = g["ph"]
        if name in active and name in dsel:
            rot += dsel[name] * ang * G["m"]["n"] / g["n"]
        col = GOLD if name == "m" else (RED if name == "r" else 0xFF9FB2CC)
        dark = 0xFF7A5A10 if name == "m" else (0xFF7A0C18 if name == "r" else 0xFF3A465C)
        pa = fill(col)
        pa.setShader(skia.GradientShader.MakeLinear([skia.Point(x - r, y - r), skia.Point(x + r, y + r)], [skia.Color4f.FromColor(0xFFFFFFFF), skia.Color4f.FromColor(col), skia.Color4f.FromColor(dark)], [0, .4, 1]))
        c.save(); c.translate(x + 6, y + 10); c.rotate(math.degrees(rot)); c.drawPath(gear_path(g["n"], r), fill(0x66000000)); c.restore()
        path = skia.Path(); gear_path(g["n"], r).transform(skia.Matrix().setRotate(math.degrees(rot)).postTranslate(x, y), path)
        path.setFillType(skia.PathFillType.kEvenOdd)
        c.drawPath(path, pa)
        c.drawPath(path, stroke(0x88000000, 2.5))
        c.drawCircle(x, y, r * .2, fill(0xFF1C2333)); c.drawCircle(x, y, r * .2, stroke(0x99FFFFFF, 3)); c.drawCircle(x, y, r * .07, fill(0xFFCFD8E6))
    # flechas
    g = G["m"]
    if sid in ("h", "s1", "s2"):
        arrow(c, g["x"], g["y"], rad(21) * .62, 1, CYAN, 1, ph=t * 1.6)
    if sid == "s1":
        for j, nm in enumerate(["a", "p0"]):
            on = clamp((lt - 1.0 - j * 1.1) / .3)
            arrow(c, G[nm]["x"], G[nm]["y"], rad(G[nm]["n"]) * .62, DT[nm], COLS[DT[nm]], on, ph=t * 1.6 * DT[nm])
    if sid == "s3":
        half = d / 2; path = TOP if lt < half else LOW; u = lt / half if lt < half else (lt - half) / half
        for j, nm in enumerate(path):
            on = clamp((u * 1.15 * (len(path) - 1) - j + .4) / .4)
            arrow(c, G[nm]["x"], G[nm]["y"], rad(G[nm]["n"]) * .62, dsel[nm], COLS[dsel[nm]], on, ph=t * 1.6 * dsel[nm])
        if u > .8:
            lab = "IZQUIERDA" if lt < half else "DERECHA"
            K.tag(c, W / 2, 1680, f"ROJA: {lab}", (u - .8) * half, accent=COLS[dsel["r"]], size=54)
    if sid in ("h", "s2"):  # interrogante en la roja
        rg = G["r"]; hc.big(c, "?", rg["x"], rg["y"] + 28, 96 + 8 * math.sin(t * 5), WHITE, 1.0, 0.0, outline=9)
    if sid == "s4":
        rg = G["r"]
        arrow(c, rg["x"], rg["y"], rad(21) * .62, 1, CYAN, 1, ph=.5); arrow(c, rg["x"], rg["y"], rad(21) * .38, -1, PINK, 1, ph=2.1, w=10)
        # el círculo de 5 aparece numerado
        for j, nm in enumerate(["p0", "p1", "p2", "p3", "p4"]):
            on = clamp((lt - 1.3 - j * .3) / .2)
            if on > 0:
                hc.big(c, str(j + 1), G[nm]["x"], G[nm]["y"] + 26, 84, GOLD, lt - 1.3 - j * .3, 0.0, outline=9)
    c.restore()
    if sid == "s2" and d - lt < 3.0:
        hc.timer(c, W / 2, 1745, 76, clamp((d - lt) / 3.0), str(int(max(1, math.ceil(d - lt)))), GOLD)
    if sid == "s4" and lt > .35:
        s = K.ease_back(clamp((lt - .35) / .25), 2.2)
        c.save(); c.translate(W / 2, 1680); c.rotate(-5); c.scale(s, s)
        r_ = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-360, -76, 720, 142), 18, 18); c.drawRRect(r_, fill(RED)); c.drawRRect(r_, stroke(WHITE, 8))
        draw_text(c, "BLOQUEADA", 0, 32, 96, WHITE, shadow=False); c.restore()


V1302 = dict(slug="1302_ruedas_bloqueadas", accent=RED, drone=0.02, scene=s_ruedas, mood="epico", send="RETA A UN AMIGO: ¿HACIA DÓNDE GIRA?",
             rehook=("s3", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="Giro la rueda amarilla hacia la derecha. ¿Hacia dónde gira la rueda roja?", cap="¿Hacia dónde gira la rueda *ROJA*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Cada rueda empuja a su vecina hacia el lado contrario, así que basta con contar.", cap="Cada rueda empuja | al *lado contrario*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="¿Izquierda, derecha, o no se mueve? Tienes tres segundos.", cap="¿*Izquierda*, *derecha*… | o *NO se mueve*?", hold=3.0),
    dict(id="s3", who="nar", cut=True, say="Por el camino de arriba, la roja gira a la izquierda. Pero por el camino de abajo, gira a la derecha.", cap="Por *ARRIBA*: izquierda… | por *ABAJO*: derecha", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y las dos cosas a la vez no puede ser. Cinco ruedas en círculo es un número impar, y la máquina entera se bloquea.", cap="*5 ruedas* en círculo: | no se mueve *NINGUNA*", hold=0.8),
    dict(id="cta", who="nar", cut=True, say="¿Qué dijiste tú? Comenta tu respuesta, y mándaselo a quien se crea muy listo.", cap="¿Qué dijiste? | *COMENTA* tu respuesta"),
])
VIDEOS = [V1301, V1302]


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
