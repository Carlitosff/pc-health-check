"""LA CIUDAD DE LA COMUNIDAD (sustituye a la montaña desde el 01/11 noche, pedido de Carlos: 'algo que se vea o se
construya mejor'). 1 seguidor = 1 ventana encendida. Los edificios se van llenando de luz y, cuando uno se llena,
la grúa ya está levantando el siguiente.
Uso: python3 ciudad.py <seguidores_antes> <seguidores_ahora> [slug] [prev]
     antes = 0 -> vídeo de ESTRENO ('la montaña se ha convertido en ciudad').
Hitos: 250 ventanas = primer rascacielos; 500, 1.000 (barrio), 2.000, 5.000, 10.000 (ciudad entera)."""
import math, sys, random
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow, draw_text

OUT = "/home/claude/tiktok/outdaily"
OLD = int(sys.argv[1]) if len(sys.argv) > 1 else 0
N = int(sys.argv[2]) if len(sys.argv) > 2 else 113
SLUG = sys.argv[3] if len(sys.argv) > 3 else f"ciudad_{N}"
INTRO = OLD <= 0
GOALS = [250, 500, 1000, 2000, 5000, 10000]
GOAL = next(g for g in GOALS if g > N)
GOLD = 0xFFFFC23A
WARM = [0xFFFFD27A, 0xFFFFC060, 0xFFFFE6A8, 0xFFFFB04A]
GROUND = 1560


def num(n):
    return f"{n:,}".replace(",", ".")


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


# ------------------------------------------------------------------ distribución de edificios y ventanas
def layout(n):
    """Edificios de izquierda a derecha (el orden de encendido va por edificio, de abajo arriba). El último es el
    que está en obras: tiene solo las plantas necesarias + 1 planta de estructura sin terminar."""
    R = random.Random(2018)
    blds, cap = [], 0
    x = 70
    while cap < n:
        cols = R.choice([3, 4, 3, 2])
        floors = R.randint(10, 14)
        w = cols * 58 + 44
        blds.append(dict(x=x, cols=cols, floors=floors, w=w, hue=R.choice([0xFF1E2438, 0xFF232A40, 0xFF1A2032, 0xFF262C44])))
        cap += cols * floors
        x += w + R.randint(18, 40)
    # escala para que quepan todos los edificios en el ancho
    total_w = x + 200  # + la grúa a la derecha
    sc = min(1.0, (W - 60) / total_w)
    return blds, sc, total_w


BLDS, SC, TW = layout(N)
WIN = []  # (edificio, planta, columna) en orden de encendido
for bi, b in enumerate(BLDS):
    for f in range(b["floors"]):
        for cc in range(b["cols"]):
            WIN.append((bi, f, cc))
LAST = BLDS[-1]
LAST_LIT = N - sum(b["cols"] * b["floors"] for b in BLDS[:-1])
LAST_BUILT = math.ceil(LAST_LIT / LAST["cols"])  # plantas que existen ya en el edificio en obras
MISSING = LAST["cols"] * LAST_BUILT - LAST_LIT    # ventanas que faltan para cerrar esa planta
FLOOR_H = 66


def sky(c, t):
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, GROUND)],
                [0xFF050818, 0xFF101A44, 0xFF2A2A66, 0xFF6A3A6A], [0, 0.4, 0.75, 1])))
    R = random.Random(5)
    for i in range(140):
        x, y = R.uniform(0, W), R.uniform(0, 1100)
        c.drawCircle(x, y, R.uniform(1, 2.6), fill(with_alpha(WHITE, 0.25 + 0.3 * math.sin(t * 2 + i))))
    # luna con halo
    glow(c, 170, 760, 240, 0xFFFFF0D0, 0.18)
    c.drawCircle(170, 760, 62, fill(0xFFF6F0DC))
    c.drawCircle(192, 746, 55, fill(with_alpha(0xFF101A44, 0.25)))
    # skyline lejano (parallax lento)
    for k, (col, base, amp, sp) in enumerate(((0xFF15183A, GROUND - 330, 260, 6), (0xFF10132C, GROUND - 200, 180, 12))):
        R2 = random.Random(40 + k)
        x = -((t * sp) % 120)
        while x < W + 120:
            w = R2.uniform(50, 120)
            h = R2.uniform(0.3, 1) * amp
            c.drawRect(skia.Rect.MakeXYWH(x, base + amp - h, w, GROUND - (base + amp - h)), fill(col))
            for j in range(int(h / 40)):
                if R2.random() < 0.25:
                    c.drawRect(skia.Rect.MakeXYWH(x + R2.uniform(6, w - 14), base + amp - h + 14 + j * 40, 8, 10), fill(with_alpha(0xFFFFD27A, 0.35)))
            x += w + 4


def street(c, t):
    c.drawRect(skia.Rect.MakeXYWH(0, GROUND, W, H - GROUND), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, GROUND), (0, H)], [0xFF14182A, 0xFF07080F])))
    c.drawRect(skia.Rect.MakeXYWH(0, GROUND, W, 6), fill(0xFF3A3F5A))
    # estelas de coches (movimiento constante)
    for k in range(9):
        y = GROUND + 50 + (k % 3) * 34
        d = 1 if k % 2 == 0 else -1
        x = ((t * (380 + k * 40) * d + k * 260) % (W + 400)) - 200
        col = 0xFFFFF0C0 if d > 0 else 0xFFFF4A4A
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 90 * d if d > 0 else x, y, 90, 7), 4, 4),
                    skia.Paint(AntiAlias=True, Color=with_alpha(col, 0.8), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4)))


def win_rect(bi, f, cc):
    b = BLDS[bi]
    x = b["x"] + 24 + cc * 58
    y = GROUND - 26 - (f + 1) * FLOOR_H
    return skia.Rect.MakeXYWH(x, y + 14, 38, FLOOR_H - 26)


def city(c, t, lit, flash_from=None, crane=True, build_k=1.0):
    """lit = ventanas encendidas (puede ser float para el encendido progresivo)."""
    c.save()
    c.translate((W - TW * SC) / 2, GROUND); c.scale(SC, SC); c.translate(0, -GROUND)
    nlit = int(lit)
    lit_per = {}
    for k, (bi, f, cc) in enumerate(WIN[:nlit]):
        lit_per[(bi, f, cc)] = k
    for bi, b in enumerate(BLDS):
        floors = b["floors"] if bi < len(BLDS) - 1 else LAST_BUILT
        hgt = 26 + floors * FLOOR_H
        y0 = GROUND - hgt
        body = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(b["x"], y0), (b["x"] + b["w"], y0)],
                          [b["hue"], 0xFF0E1220]))
        c.drawRect(skia.Rect.MakeXYWH(b["x"], y0, b["w"], hgt), body)
        c.drawRect(skia.Rect.MakeXYWH(b["x"] - 6, y0 - 10, b["w"] + 12, 12), fill(0xFF2E3550))
        if bi < len(BLDS) - 1 and bi % 2 == 0:  # antena con luz roja
            ax = b["x"] + b["w"] / 2
            c.drawLine(ax, y0 - 10, ax, y0 - 90, stroke(0xFF5A6080, 5))
            if int(t * 1.5 + bi) % 2 == 0:
                glow(c, ax, y0 - 92, 30, 0xFFFF3030, 0.7)
                c.drawCircle(ax, y0 - 92, 6, fill(0xFFFF5050))
        elif bi < len(BLDS) - 1:  # depósito de agua
            c.drawRect(skia.Rect.MakeXYWH(b["x"] + b["w"] * 0.6, y0 - 60, 44, 50), fill(0xFF3A3040))
        for f in range(floors):
            for cc in range(b["cols"]):
                r = win_rect(bi, f, cc)
                k = lit_per.get((bi, f, cc))
                if k is None:
                    c.drawRect(r, fill(0xFF0A0D18))
                    continue
                col = WARM[(bi * 7 + f * 3 + cc) % 4]
                pop = 1.0
                if flash_from is not None and k >= flash_from:
                    age = (lit - k)
                    pop = 1 + 0.6 * math.exp(-max(0, age) * 0.35)
                glow(c, r.centerX(), r.centerY(), 46 * pop, col, 0.22)
                c.drawRect(r, fill(col))
                c.drawRect(skia.Rect.MakeXYWH(r.left(), r.top(), r.width(), r.height() * 0.35), fill(with_alpha(WHITE, 0.25)))
        if bi == len(BLDS) - 1 and crane:
            # planta en construcción: vigas
            ys = y0 - FLOOR_H
            for cc in range(b["cols"] + 1):
                c.drawRect(skia.Rect.MakeXYWH(b["x"] + 12 + cc * 58, ys, 9, FLOOR_H), fill(0xFFE0A030))
            c.drawRect(skia.Rect.MakeXYWH(b["x"], ys, b["w"], 8), fill(0xFFE0A030))
            # grúa
            mx = b["x"] + b["w"] + 40
            top = ys - 360
            c.drawRect(skia.Rect.MakeXYWH(mx, top, 26, GROUND - top), fill(0xFFF0B030))
            for j in range(int((GROUND - top) / 40)):
                y = top + j * 40
                c.drawLine(mx, y, mx + 26, y + 40, stroke(0xFF9A6A10, 3))
            jib = skia.Rect.MakeXYWH(mx - 360, top - 20, 460, 22)
            c.drawRect(jib, fill(0xFFF0B030))
            c.drawRect(skia.Rect.MakeXYWH(mx + 60, top - 12, 60, 46), fill(0xFF6A6A7A))
            tx = mx - 140 + math.sin(t * 0.9) * 120
            ln = 200 + math.sin(t * 1.3) * 60
            c.drawLine(tx, top, tx, top + ln, stroke(0xFFCCCCCC, 3))
            sw = math.sin(t * 2.1) * 8
            c.drawRect(skia.Rect.MakeXYWH(tx - 50 + sw, top + ln, 100, 18), fill(0xFFB07A2A))
            # luz de aviso que parpadea
            if int(t * 2) % 2 == 0:
                glow(c, mx - 360, top - 30, 40, 0xFFFF3030, 0.8)
                c.drawCircle(mx - 360, top - 30, 8, fill(0xFFFF4040))
    c.restore()


def scene(c, t, P, V):
    sid, lt = seg(P, t)
    sky(c, t)
    zoom = 1.0 + 0.04 * math.sin(t * 0.25)
    c.save(); c.translate(W / 2, GROUND); c.scale(zoom, zoom); c.translate(-W / 2, -GROUND)
    if sid == "h":
        start = 0 if INTRO else OLD
        city(c, t, start + (3 if INTRO else 0) * clamp(t / 1.5))
        c.restore(); street(c, t)
        hc.big(c, "1 SEGUIDOR = 1 VENTANA" if INTRO else f"{num(OLD)}", W / 2, 1720, 72 if INTRO else 130, GOLD, lt, 0.4)
        return
    if sid == "s1":
        a0 = 0 if INTRO else OLD
        dur = max(1.5, (P["tl"]["s1"][1] - P["tl"]["s1"][0]) - 0.3)
        lit = a0 + (N - a0) * ease_in_out(clamp(lt / dur))
        city(c, t, lit, flash_from=a0)
        c.restore(); street(c, t)
        hc.big(c, num(int(lit)), W / 2, 1720, 150, GOLD, 1.0, 0.0)
        return
    city(c, t, N, flash_from=N - 3)
    c.restore(); street(c, t)
    if sid == "s2":
        hc.big(c, f"{num(N)} VENTANAS", W / 2, 1720, 110, GOLD, lt, 0.2)
        K.tag(c, W / 2, 1840, f"{len(BLDS)} EDIFICIOS", lt - 0.8, accent=WHITE, size=40)
    elif sid == "s3":
        K.tag(c, W / 2, 1720, "LA GRÚA NO PARA", lt - 0.2, accent=GOLD, size=46)
        if MISSING:
            K.tag(c, W / 2, 1820, f"FALTAN {MISSING} PARA CERRAR LA PLANTA", lt - 0.8, accent=WHITE, size=34)
    elif sid == "s4":
        hc.big(c, f"META: {num(GOAL)}", W / 2, 1720, 110, GOLD, lt, 0.2)
        K.tag(c, W / 2, 1840, f"FALTAN {num(GOAL - N)}", lt - 0.8, accent=WHITE, size=40)
    else:
        # la ventana 'tuya': parpadea la siguiente ventana libre
        pass


def goal_line():
    if GOAL == 250:
        return "doscientas cincuenta ventanas, y levantamos el primer rascacielos", "*250* = el primer *RASCACIELOS*"
    return f"{num(GOAL)} ventanas", f"*{num(GOAL)}* ventanas"


gsay, gcap = goal_line()
if INTRO:
    S_H = dict(id="h", who="nar", say="La montaña se ha convertido en una ciudad. Y cada ventana encendida, es una persona que me sigue.",
               cap="La montaña ahora es | una *CIUDAD*: cada *ventana* | es alguien que me sigue", hold=0.2)
    S_1 = dict(id="s1", who="nar", cut=True, say="Mira cuántas sois ya.", cap="Mira cuántas | *SOIS* ya…", hold=2.2)
    S_2 = dict(id="s2", who="nar", cut=True, say=f"¡{N} ventanas! {len(BLDS)} edificios, encendidos por vosotros.",
               cap=f"¡*{num(N)} VENTANAS*! | encendidas | por *vosotros*")
else:
    S_H = dict(id="h", who="nar", say=f"Ayer esta ciudad tenía {OLD} ventanas encendidas. Mira lo que habéis hecho.",
               cap=f"Ayer: *{num(OLD)} ventanas*… | mira lo que | habéis *HECHO*", hold=0.2)
    S_1 = dict(id="s1", who="nar", cut=True, say=f"{N - OLD} ventanas nuevas.", cap=f"*+{num(N - OLD)}* | ventanas nuevas", hold=1.8)
    S_2 = dict(id="s2", who="nar", cut=True, say=f"¡{N} ventanas! Cada una, una persona.", cap=f"¡*{num(N)} VENTANAS*! | cada una, | *una persona*")
V = dict(slug=SLUG, accent=GOLD, drone=0.03, scene=scene, tease="1 SEGUIDOR = 1 VENTANA", mood="epico",
         send="ENVÍASELO A UN AMIGO", rehook=("s3", "Y LA GRÚA NO PARA"),
         reveal=("s4", "EL NUEVO RETO"), segs=[
    S_H, S_1, S_2,
    dict(id="s3", who="nar", cut=True,
         say=("Y el último edificio, todavía está en obras. La grúa ya está subiendo la siguiente planta." if not MISSING else
              f"Y el último edificio todavía está en obras. Le faltan {MISSING} ventanas para cerrar la planta."),
         cap="El último sigue | en *OBRAS*… | la grúa *no para*"),
    dict(id="s4", who="nar", cut=True, say=f"Siguiente reto: {gsay}. Faltan {GOAL - N}.",
         cap=f"Siguiente reto: {gcap}. | Faltan *{num(GOAL - N)}*"),
    dict(id="cta", who="nar", cut=True, say="Si aún no me sigues, la próxima ventana es la tuya. Comenta: enciende la mía.",
         cap="La próxima ventana | es la *TUYA*: comenta | *ENCIENDE LA MÍA*"),
])

if __name__ == "__main__":
    pv = "auto" if (len(sys.argv) > 4 and sys.argv[4] == "prev") else None
    K.run(V, lambda c, t, P: V["scene"](c, t, P, V), OUT, preview=pv)
