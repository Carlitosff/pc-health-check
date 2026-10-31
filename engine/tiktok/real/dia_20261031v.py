"""31/10/2026 noche (614–615): PRUEBA DE VOZ pedida por Carlos ('la voz sigue sin gustarme, más natural').
Dos vídeos con Kokoro v1.0 local (otro modelo, más expresivo que Piper medium) a velocidad natural 1,0:
614 = em_alex (hombre), 615 = ef_dora (mujer). Comparar likes/1.000 vistas y tiempo medio con los Piper del día."""
import math, sys, random
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import dia_20261031 as D
from core import W, H, WHITE, INK, clamp, lerp, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, draw_text

OUT = "/home/claude/tiktok/outdaily"
GREEN = 0xFF2FD46B
RED = 0xFFFF3B4A


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


# ====================================================================== 614 ¿Cuántos cuadrados hay en un tablero de ajedrez? (204)
def board(c, x0, y0, cell, t):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 - 30, y0 - 30, cell * 8 + 60, cell * 8 + 60), 18, 18), skia.Paint(
        Shader=skia.GradientShader.MakeLinear([(x0, y0), (x0 + cell * 8, y0 + cell * 8)], [0xFF5A3418, 0xFF3A200C])))
    for i in range(8):
        for j in range(8):
            light = (i + j) % 2 == 0
            r = skia.Rect.MakeXYWH(x0 + i * cell, y0 + j * cell, cell, cell)
            c.drawRect(r, skia.Paint(Shader=skia.GradientShader.MakeLinear(
                [(r.left(), r.top()), (r.right(), r.bottom())],
                [0xFFF0D9B5, 0xFFE2C59A] if light else [0xFFB58863, 0xFF9A6E4A])))


def s_ajedrez(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF2A1A0A, 0xFF1A0A2A, seed=614)
    cell = 112
    x0, y0 = W / 2 - 4 * cell + math.sin(t * 0.5) * 3, 1230 - 4 * cell
    board(c, x0, y0, cell, t)
    sizes = {"s3": 1, "s4": 2, "s5": 3, "s6": 8}
    base = {"s3": 0, "s4": 64, "s5": 113, "s6": 203}
    if sid in sizes:
        sz = sizes[sid]
        m = 9 - sz
        cnt = m * m
        dur = max(1.2, (P["tl"][sid][1] - P["tl"][sid][0]) - 0.4)
        shown = min(cnt, int(lt / (dur / cnt)) + 1)
        q = shown - 1
        i, j = q % m, q // m
        r = skia.Rect.MakeXYWH(x0 + i * cell + 6, y0 + j * cell + 6, sz * cell - 12, sz * cell - 12)
        c.drawRect(r, fill(with_alpha(V["accent"], 0.4)))
        c.drawRect(r, stroke(V["accent"], 10))
        hc.big(c, str(base[sid] + shown), W / 2, 1800, 150, V["accent"], 1.0, 0.0)
    if sid == "s5b":
        for k, (lab, n) in enumerate((("4×4", 25), ("5×5", 16), ("6×6", 9), ("7×7", 4))):
            a = clamp((lt - 0.2 - 0.3 * k) / 0.3)
            K.tag(c, W / 2 + (k - 1.5) * 240, 1790, f"{lab}: {n}", lt - 0.2 - 0.3 * k, accent=V["accent"], size=34)
    if sid == "h":
        hc.timer(c, W / 2, 1830, 66, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s1":
        K.tag(c, W / 2, 1800, "COMENTA TU NÚMERO", lt - 0.2, accent=V["accent"], size=44)
    if sid == "cta":
        hc.stamp(c, "204", W / 2, 1790, lt, 0.1, 150, col=GREEN)


V614 = dict(slug="614_ajedrez_204_cuadrados", accent=0xFF3AC8FF, drone=0.02, scene=s_ajedrez, mood="misterio",
            tease="CASI NADIE DICE BIEN", send="RETA A UN AMIGO: ENVÍASELO", rehook=("s4", "AQUÍ FALLA CASI TODO EL MUNDO"),
            reveal=("cta", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="¿Cuántos cuadrados hay en un tablero de ajedrez? No, no son sesenta y cuatro.",
         cap="¿Cuántos *CUADRADOS* hay | en un tablero? | No son *64*", hold=1.0),
    dict(id="s1", who="nar", cut=True, say="Piénsalo un momento, y escribe tu número en los comentarios.",
         cap="Piénsalo… y escribe | tu número en | *COMENTARIOS*", hold=0.6),
    dict(id="s2", who="q", cut=True, say="¿Ya lo tienes? Vamos a contarlos.", cap="¿Ya? | Vamos a *contarlos*"),
    dict(id="s3", who="nar", cut=True, say="Los pequeños, de uno en uno: sesenta y cuatro.", cap="Los pequeños: | *64*", hold=1.0),
    dict(id="s4", who="nar", cut=True, say="Pero también hay cuadrados de dos por dos. Cuarenta y nueve más.", cap="De *2×2*: | *49* más", hold=1.0),
    dict(id="s5", who="nar", cut=True, say="De tres por tres, treinta y seis.", cap="De *3×3*: | *36*", hold=0.8),
    dict(id="s5b", who="nar", cut=True, say="Y siguen: veinticinco, dieciséis, nueve, cuatro.", cap="Y siguen: *25*, *16*, | *9*, *4*…", hold=0.6),
    dict(id="s6", who="nar", cut=True, say="Y el tablero entero, que también es un cuadrado.", cap="Y el *tablero entero*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="En total, doscientos cuatro. ¿Cuántos dijiste tú? Comenta, y sígueme para el próximo reto.",
         cap="Total: *204*. ¿Y tú? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 615 Mito: solo tenemos 5 sentidos (propiocepción)
def s_sentidos(c, t, P, V):
    sid, lt = seg(P, t)
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, 1150), 1300, [0xFF2A1640, 0xFF08040E])))
    if sid == "h":
        labs = ["VISTA", "OÍDO", "OLFATO", "GUSTO", "TACTO"]
        for k, lab in enumerate(labs):
            a = clamp((lt - 0.1 * k) / 0.25)
            y = 760 + k * 170
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - 300, y - 60, 600, 120), 30, 30), fill(with_alpha(0xFF3A2A5A, a)))
            draw_text(c, lab, W / 2, y + 22, 64, with_alpha(WHITE, a))
        if lt > 1.2:
            hc.stamp(c, "Y MUCHOS MÁS", W / 2, 1700, lt, 1.2, 100, col=RED)
    elif sid == "s1":
        hc.eye(c, W / 2, 1150, 300, t)
        k = ease_in_out(clamp((lt - 0.5) / 0.8))
        c.drawPaint(fill(with_alpha(0xFF06030A, 0.92 * k)))  # 'cierras los ojos': fundido a negro
        if k > 0.9:
            hc.timer(c, W / 2, 1650, 70, clamp((lt - 1.3) / 3.0), str(max(0, 3 - int(lt - 1.3))), V["accent"])
    elif sid == "s2":
        hc.brain(c, W / 2, 1100, 1.4, t)
        for k in range(6):  # señales que suben del cuerpo al cerebro
            ph = (t * 0.8 + k / 6) % 1
            y = lerp(1800, 1180, ph)
            c.drawCircle(W / 2 + (k - 2.5) * 70, y, 14, fill(with_alpha(V["accent"], 1 - ph)))
        K.tag(c, W / 2, 1700, "PROPIOCEPCIÓN", lt - 0.4, accent=V["accent"], size=52)
        K.tag(c, W / 2, 1810, "CHARLES SHERRINGTON · 1906", lt - 1.0, accent=WHITE, size=32)
    elif sid == "s3":
        # equilibrio: anillos del oído interno que giran + nivel de burbuja
        for k, (r, sp) in enumerate(((300, 0.6), (230, -0.9), (160, 1.3))):
            c.save(); c.translate(W / 2, 1100); c.rotate(math.degrees(t * sp)); c.scale(1, 0.45 + 0.15 * k)
            c.drawCircle(0, 0, r, stroke(with_alpha(0xFF7AD8FF, 0.8), 22))
            c.restore()
        bx = W / 2 + math.sin(t * 1.4) * 160
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - 280, 1560, 560, 90), 45, 45), fill(0xFF2AB070))
        c.drawCircle(bx, 1605, 34, fill(with_alpha(WHITE, 0.85)))
        K.tag(c, W / 2, 1760, "EQUILIBRIO · OÍDO INTERNO", lt - 0.4, accent=V["accent"], size=38)
    elif sid == "s4":
        D.thermo(c, W / 2 - 250, 1450, lerp(-5, 35, 0.5 + 0.5 * math.sin(t * 1.5)), t)
        hc.big(c, "+20", W / 2 + 170, 1150, 200, V["accent"], lt, 0.3)
        K.tag(c, W / 2 + 170, 1340, "SENTIDOS, SEGÚN QUIÉN CUENTE", lt - 0.8, accent=WHITE, size=30)
        K.tag(c, W / 2, 1760, "TEMPERATURA · DOLOR · HAMBRE · SED", lt - 1.2, accent=V["accent"], size=32)
    else:
        hc.brain(c, W / 2, 1100, 1.4, t)


V615 = dict(slug="615_mito_5_sentidos", accent=0xFFFF7AD9, drone=0.03, scene=s_sentidos, mood="luz",
            tease="TE LO ENSEÑARON MAL", send="ENVÍASELO A QUIEN CREA QUE SOLO HAY 5", rehook=("s3", "Y HAY MÁS"),
            reveal=("s2", "EL SEXTO SENTIDO"), segs=[
    dict(id="h", who="nar", say="No tienes cinco sentidos. Tienes muchos más. Y te lo voy a demostrar ahora mismo.",
         cap="No tienes *5 sentidos*. | Tienes *MUCHOS MÁS*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Cierra los ojos, y tócate la punta de la nariz con un dedo. ¿Lo has hecho sin mirar? Claro.",
         cap="Cierra los ojos | y tócate la *NARIZ*… | ¿sin mirar? *Claro*", hold=0.8),
    dict(id="s2", who="nar", cut=True, say="Eso es la propiocepción: tu cerebro sabe dónde está cada parte de tu cuerpo, sin verla. La bautizó Charles Sherrington en mil novecientos seis.",
         cap="Es la *propiocepción*: sabes | dónde está tu cuerpo | *sin verlo*"),
    dict(id="s3", who="nar", cut=True, say="Y hay más. El equilibrio, que nace en el oído interno, y te avisa de si estás de pie o cayendo.",
         cap="Y hay más: el *EQUILIBRIO*, | que nace en el | *oído interno*"),
    dict(id="s4", who="nar", cut=True, say="También sientes la temperatura, el dolor, el hambre, o la sed. Según cómo se cuenten, hay más de veinte.",
         cap="Temperatura, *dolor*, hambre… | según cómo se cuenten, | más de *20*"),
    dict(id="cta", who="nar", cut=True, say="¿Te enseñaron en clase que solo había cinco? Comenta sí o no. Y sígueme para más mitos.",
         cap="¿Te enseñaron que eran 5? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])

SANTA = {"nar": ("kokoroP:em_santa", 1.0), "q": ("kokoroP:em_santa", 1.06)}  # elegida por Carlos (muestra C) + pausas
TESTS = {"614": (V614, SANTA), "615": (V615, SANTA)}

if __name__ == "__main__":
    key = sys.argv[1]
    V, voices = TESTS[key]
    K.VOICES = voices  # PRUEBA DE VOZ: Kokoro local en vez de Piper
    pv = "auto" if len(sys.argv) > 2 else None
    K.run(V, lambda c, t, P: V["scene"](c, t, P, V), OUT, preview=pv)
