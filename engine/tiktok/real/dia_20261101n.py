"""01/11/2026 NOCHE (806–808) + ciudad (809, ciudad.py 0 113). Pedido de Carlos en directo: 4 vídeos más esta noche,
el reto de la comunidad cambia de montaña a CIUDAD que se ilumina, y voz nueva (muestra D elegida: em_alex, modelo
Kokoro fp32 completo, entonación por frase entera + pausas en comas + EQ/compresión -> core.VOICES 'kokoroN:em_alex').
  806 ILUSIÓN EN DIRECTO: extinción de Ninio (Jacques Ninio y Kent Stevens, Perception 2000; viral en 2016): 12 puntos
      negros en una rejilla gris, nunca se ven los 12 a la vez. steady=True.
  807 RETO: encuentra la Ñ entre las N (5 s) + ronda 2 más difícil: el 6 entre los 9. Posiciones fijas y comprobadas.
  808 MITO CON 'TÚ': afeitarse no hace que el pelo salga más fuerte (Mildred Trotter, Anatomical Record 1928; Journal
      of Investigative Dermatology 1970; pincha porque se corta por la parte gruesa del pelo; parece más oscuro por
      contraste con la piel — Live Science 25/08/2012)."""
import math, sys, random
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import dia_20261031 as D
from core import W, H, WHITE, INK, clamp, lerp, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow, draw_text

OUT = "/home/claude/tiktok/outdaily"
GREEN = 0xFF2FD46B
RED = 0xFFFF3B4A
seg = D.seg
blur = D.blur


# ====================================================================== 806 Extinción de Ninio
GX, GY, STEP = W / 2, 1230, 62
DOTS = [(r, cc) for r in (-8, 0, 8) for cc in (-12, -4, 4, 12)]  # 3 filas x 4 = 12 puntos en cruces de la rejilla
assert len(DOTS) == 12


def ninio(c, lines=1.0):
    c.clear(0xFFE4E4E4)
    if lines > 0:
        col = with_alpha(0xFF8C8C8C, lines)
        n = 9
        for k in range(-n, n + 1):  # diagonales en las dos direcciones (como el original)
            x = GX + k * STEP
            c.drawLine(x - 700, GY - 700, x + 700, GY + 700, stroke(col, 7))
            c.drawLine(x + 700, GY - 700, x - 700, GY + 700, stroke(col, 7))
    for r, cc in DOTS:
        # los puntos caen en cruces de las diagonales: (cc/2*STEP, r/2*STEP) con r y cc pares -> cruce
        x, y = GX + cc * STEP / 2 * 1.0, GY + r * STEP / 2
        c.drawCircle(x, y, 13, fill(0xFF000000))


def s_ninio(c, t, P, V):
    sid, lt = seg(P, t)
    k = 1.0
    if sid == "s3":
        k = 1.0 - ease_in_out(clamp((lt - 0.4) / 0.6))
    elif sid in ("s4",):
        k = ease_in_out(clamp((lt - 0.2) / 0.6))
    ninio(c, k)
    if sid == "s3" and lt > 1.0:
        hc.big(c, "12", W / 2, 1800, 150, V["accent"], lt, 1.0)


V806 = dict(slug="806_ninio_12_puntos", accent=0xFF3A8AFF, drone=0.0, music=0.035, scene=s_ninio, mood="misterio",
            steady=True, clean=True, tease="NADIE VE LOS 12", send="ENVÍASELO A UN AMIGO, A VER CUÁNTOS VE",
            rehook=("s2", "MIRA SOLO UNO"), reveal=("s3", "LOS 12"), segs=[
    dict(id="h", who="nar", say="¿Cuántos puntos negros ves a la vez? Hay doce.",
         cap="¿Cuántos *PUNTOS NEGROS* | ves a la vez? | Hay *12*", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="Intenta verlos todos al mismo tiempo. No puedes.",
         cap="Intenta verlos | *todos* a la vez… | *no puedes*", hold=1.0),
    dict(id="s2", who="nar", cut=True, say="Mira uno solo, y los demás desaparecen.",
         cap="Mira *uno solo*… | y los demás | *DESAPARECEN*", hold=1.4),
    dict(id="s3", who="nar", cut=True, say="Si quito las líneas, ahí están los doce.",
         cap="Quito las líneas… | y ahí están | los *DOCE*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Tu vista de reojo es borrosa, y tu cerebro rellena el hueco con las líneas. Lo publicaron Jacques Ninio y Kent Stevens, en el año dos mil.",
         cap="De reojo ves *borroso* | y tu cerebro *rellena* | con las líneas"),
    dict(id="cta", who="nar", cut=True, say="¿Cuántos veías tú a la vez? Comenta tu número. Y envíaselo a un amigo.",
         cap="¿Cuántos veías? | Comenta tu *NÚMERO*"),
])


# ====================================================================== 807 Encuentra la Ñ / el 6
ROWS, COLS = 10, 8
R1 = (6, 5)  # posición de la Ñ (fila, columna)
R2 = (3, 2)  # posición del 6
CELL_W, CELL_H = 118, 112
X0, Y0 = W / 2 - COLS * CELL_W / 2 + CELL_W / 2, 700


def cell_xy(r, cc):
    return X0 + cc * CELL_W, Y0 + r * CELL_H


def grid(c, t, base, odd, pos, accent, found=0.0):
    for r in range(ROWS):
        for cc in range(COLS):
            x, y = cell_xy(r, cc)
            y += math.sin(t * 1.6 + cc * 0.5 + r * 0.3) * 4
            txt = odd if (r, cc) == pos else base
            draw_text(c, txt, x, y + 28, 84, WHITE)
    if found > 0:
        x, y = cell_xy(*pos)
        s = ease_back(clamp(found / 0.4), 2.2)
        c.drawCircle(x, y, 74 * s, stroke(accent, 12))
        glow(c, x, y, 180, accent, 0.3 * clamp(found / 0.4))


def s_letras(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A2A4A, 0xFF3A0A3A, seed=807)
    if sid in ("h", "s1", "s2"):
        grid(c, t, "N", "Ñ", R1, GREEN, found=lt if sid == "s2" else 0.0)
        if sid in ("h", "s1"):
            t0 = P["tl"]["h"][0]
            el = t - t0
            dur = P["tl"]["s2"][0] - t0  # el reloj llega a 0 justo cuando sale la solución
            hc.timer(c, W / 2, 1880, 56, clamp(el / dur), str(max(0, math.ceil(dur - el))), V["accent"])
    else:
        grid(c, t, "9", "6", R2, GREEN, found=lt if sid in ("s4", "cta") else 0.0)
        if sid == "s3":
            dur = P["tl"]["s3"][1] - P["tl"]["s3"][0]
            hc.timer(c, W / 2, 1880, 56, clamp(lt / dur), str(max(0, math.ceil(dur - lt))), V["accent"])


V807 = dict(slug="807_encuentra_la_enie", accent=0xFFFFC23A, drone=0.02, scene=s_letras, mood="misterio",
            tease="SOLO 5 SEGUNDOS", send="RETA A UN AMIGO: ENVÍASELO", rehook=("s3", "AHORA MÁS DIFÍCIL"),
            reveal=("s2", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="Encuentra la eñe. Tienes cinco segundos.",
         cap="Encuentra la *Ñ* | en *5 segundos*", hold=1.4),
    dict(id="s1", who="q", cut=True, say="Tic, tac.", cap="*Tic*… *tac*…", hold=1.8),
    dict(id="s2", who="nar", cut=True, say="¡Aquí! ¿La viste a tiempo?", cap="¡*AQUÍ*! | ¿La viste?", hold=0.6),
    dict(id="s3", who="nar", cut=True, say="Ahora más difícil. Encuentra el seis entre los nueves.",
         cap="Ahora más *difícil*: | encuentra el *6*", hold=3.6),
    dict(id="s4", who="nar", cut=True, say="¡Aquí está! Casi todo el mundo tarda más de cinco segundos.",
         cap="¡Aquí está! | ¿Lo encontraste?", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="¿Encontraste los dos? Comenta sí o no. Y reta a un amigo.",
         cap="¿Los dos? | Comenta *SÍ* o *NO*"),
])


# ====================================================================== 808 Mito: afeitarse no hace el pelo más fuerte
SKIN_Y = 1250


def hair_path(x, base_y, length, w0, tip=True, cut_at=None):
    """Pelo cónico: grueso en la raíz, fino en la punta. Si cut_at (0..1) se corta en seco a esa altura."""
    L = length if cut_at is None else length * cut_at
    p = skia.Path()
    wt = w0 * (0.12 if cut_at is None else (1 - 0.88 * cut_at))
    bend = 0.18 * length
    p.moveTo(x - w0 / 2, base_y)
    p.quadTo(x - w0 / 2 + bend * (L / length) * 0.5, base_y - L * 0.5, x - wt / 2 + bend * (L / length) ** 2, base_y - L)
    p.lineTo(x + wt / 2 + bend * (L / length) ** 2, base_y - L)
    p.quadTo(x + w0 / 2 + bend * (L / length) * 0.5, base_y - L * 0.5, x + w0 / 2, base_y)
    p.close()
    return p


def skin(c, t):
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, SKIN_Y)], [0xFF1A2A3A, 0xFF2A3A4A])))
    c.drawRect(skia.Rect.MakeXYWH(0, SKIN_Y, W, H - SKIN_Y), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, SKIN_Y), (0, H)], [0xFFF0C0A0, 0xFFD08A70, 0xFF9A4A4A], [0, 0.3, 1])))
    for i in range(7):  # folículos
        x = 140 + i * 135
        c.drawOval(skia.Rect.MakeXYWH(x - 26, SKIN_Y + 120, 52, 120), fill(0xFFB06A5A))


def hairs(c, t, cut=None, x_off=0):
    for i in range(7):
        x = 140 + i * 135 + x_off
        p = hair_path(x, SKIN_Y + 150, 520 + (i % 3) * 60, 30, cut_at=cut)
        c.drawPath(p, fill(0xFF2A1A12))


def razor(c, x, y):
    c.save(); c.translate(x, y)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-60, -320, 120, 330), 30, 30), fill(0xFF3A5AD0))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-120, 0, 240, 60), 14, 14), fill(0xFFE0E4F0))
    c.drawRect(skia.Rect.MakeXYWH(-110, 46, 220, 8), fill(0xFF9AA0B0))
    c.restore()


def s_afeitar(c, t, P, V):
    sid, lt = seg(P, t)
    skin(c, t)
    if sid == "h":
        hairs(c, t)
        hc.stamp(c, "MITO", W / 2, 1650, lt, 0.8, 120, col=RED)
    elif sid == "s1":
        cut = 0.45
        k = ease_in_out(clamp(lt / 1.4))
        hairs(c, t, cut=cut if k > 0.5 else None)
        rx = lerp(-200, W + 200, k)
        razor(c, rx, SKIN_Y + 150 - 520 * cut - 40)
        hc.big(c, "1928", W / 2 - 230, 1650, 120, V["accent"], lt, 1.2)
        K.tag(c, W / 2 + 190, 1650, "MILDRED TROTTER", lt - 1.6, accent=WHITE, size=38)
    elif sid == "s2":
        # lupa: punta fina natural vs corte por la parte gruesa
        c.drawPaint(fill(0xFF101820))
        for j, (lab, cut) in enumerate((("SIN AFEITAR", None), ("AFEITADO", 0.5))):
            x = W / 2 + (j - 0.5) * 440
            p = hair_path(x, 1700, 900, 110, cut_at=cut)
            c.drawPath(p, fill(0xFF3A2418))
            c.drawPath(p, stroke(0xFF6A4430, 4))
            K.tag(c, x, 1800, lab, lt - 0.3 - 0.4 * j, accent=V["accent"] if j else WHITE, size=40)
        if lt > 1.4:
            y = 1700 - 450
            c.drawLine(W / 2 + 160, y, W / 2 + 280, y, stroke(RED, 8))
            K.tag(c, W / 2 + 220, y - 70, "PARTE GRUESA", lt - 1.4, accent=RED, size=34)
    elif sid == "s3":
        hairs(c, t, cut=0.08)
        for i in range(7):
            x = 140 + i * 135
            glow(c, x, SKIN_Y + 110, 60, 0xFF000000, 0.25)
        K.tag(c, W / 2, 1650, "CONTRASTE CON TU PIEL", lt - 0.3, accent=V["accent"], size=44)
    elif sid == "s4":
        hairs(c, t, cut=0.6 + 0.4 * ease_out(clamp(lt / 2.0)))
        hc.big(c, "1970", W / 2, 1650, 130, V["accent"], lt, 0.3)
        K.tag(c, W / 2, 1780, "NINGUNA DIFERENCIA", lt - 0.9, accent=GREEN, size=44)
    else:
        hairs(c, t)


V808 = dict(slug="808_mito_afeitarse_pelo_fuerte", accent=0xFF5AE0C8, drone=0.02, scene=s_afeitar, mood="luz",
            tease="TE LO HAN CONTADO MAL", send="ENVÍASELO A QUIEN SE LO CREA",
            rehook=("s2", "¿ENTONCES POR QUÉ PINCHA?"), reveal=("s2", "POR QUÉ PINCHA"), segs=[
    dict(id="h", who="nar", say="Si te afeitas, el pelo no te sale más fuerte. Es un mito.",
         cap="Afeitarte *NO* hace | que el pelo salga | más *FUERTE*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="En mil novecientos veintiocho, Mildred Trotter lo comprobó: afeitarse no cambia ni el color, ni el grosor, ni lo rápido que crece.",
         cap="*1928*, Mildred Trotter: | ni el *color*, ni el *grosor*, | ni lo *rápido* que crece"),
    dict(id="s2", who="nar", cut=True, say="¿Entonces por qué pincha? Cada pelo es fino en la punta. Al afeitarte, lo cortas por la parte gruesa.",
         cap="¿Por qué *pincha*? | Lo cortas por la | *parte gruesa*", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Y parece más oscuro, porque ves el corte justo contra tu piel.",
         cap="Y parece más *oscuro* | por el contraste | con tu *piel*"),
    dict(id="s4", who="nar", cut=True, say="En mil novecientos setenta, otro estudio lo volvió a medir. Ninguna diferencia.",
         cap="*1970*: otro estudio. | *Ninguna diferencia*"),
    dict(id="cta", who="nar", cut=True, say="¿Tú también te lo creías? Comenta sí o no. Y envíaselo a quien se lo crea.",
         cap="¿Te lo creías? | Comenta *SÍ* o *NO*"),
])

VIDEOS = [V806, V807, V808]


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
