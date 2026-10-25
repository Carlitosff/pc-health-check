"""5 vídeos interactivos 'haz esto mientras miras'.

uso: python3 pruebas.py <índices|all> [prev]
"""
import math, random, sys
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, pill, glow
from engine import lerp_color

OUT = "/home/claude/tiktok/out50"
VIDEOS = []
CTA_MAS = "y sígueme para más pruebas como esta."


def label(c, t, txt, accent):
    pill(c, W / 2, 292, txt, 30, bg=accent, fg=INK)


def stare_timer(c, sg, t, accent, y=1640):
    a, b = sg["speech"][1], sg["b"]
    if t > a:
        hc.timer(c, W / 2, y, 70, (t - a) / (b - a), max(1, math.ceil(b - t)), accent)


# =============================================================== 1 · espiral (efecto cascada)
_EARTH = {}


def spiral(c, cx, cy, R, ang, arms=3):
    c.save()
    c.translate(cx, cy)
    c.rotate(ang)
    c.drawCircle(0, 0, R, fill(0xFF101010))
    for k in range(arms):
        p = skia.Path()
        a0 = k * 2 * math.pi / arms
        pts = []
        for i in range(0, 121):
            f = i / 120
            r = R * f
            th = a0 + f * 4.0 * math.pi
            pts.append((math.cos(th) * r, math.sin(th) * r))
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, skia.Paint(AntiAlias=True, Color=0xFFF4F4F4, Style=skia.Paint.kStroke_Style,
                                 StrokeWidth=R * 0.06, StrokeCap=skia.Paint.kRound_Cap))
    c.restore()
    c.drawCircle(cx, cy, R, stroke(0xFF2A2A2A, 6))
    c.drawCircle(cx, cy, 14, fill(0xFFFF2A3A))


def s_espiral(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    c.clear(0xFF15161C)
    if sid in ("h", "s1"):
        spiral(c, W / 2, 1050, 470, -t * 220)
        if sid == "s1":
            stare_timer(c, sg, t, V["accent"])
        label(c, t, "PRUEBA · NO APARTES LA VISTA", V["accent"])
        return
    if sid == "s2":
        if "img" not in _EARTH:
            _EARTH["img"] = S.render(840, S.load("earth_atmos_2048.jpg"), spin=-0.2, lat0=0.4,
                                     clouds=S.load("earth_clouds_1024.png", "A"), gain=1.15)
        S.draw_planet(c, W / 2, 1050, 420, _EARTH["img"])
        S.atmosphere(c, W / 2, 1050, 420)
        return
    hc.aurora(c, t, V["accent"], V["a2"], 11)
    spiral(c, W / 2, 1000, 260, -t * 220)
    if sid == "s3":
        K.tag(c, W / 2, 1420, "EFECTO CASCADA", lt - 0.4, accent=V["accent"], size=44)


VIDEOS.append(dict(slug="51_espiral", accent=0xFFFF4D6D, a2=0xFF6A5AF0, scene=s_espiral, clean=True, segs=[
    dict(id="h", who="nar", say="Mira el punto rojo del centro durante veinte segundos… y después mira tu mano.",
         cap="Mira el *punto rojo*… | *20 segundos*… | y luego mira tu *mano*"),
    dict(id="s1", who="nar", say="No apartes la vista.", cap="No apartes | la *vista*", hold=15.5),
    dict(id="s2", who="nar", cut=True, say="¡Ahora! Mira esta imagen… o tu mano. ¿Se mueve?",
         cap="¡*AHORA*! | ¿Se *mueve*?", hold=2.5),
    dict(id="s3", who="nar", cut=True,
         say="Es el efecto cascada: las neuronas que detectan ese movimiento se cansan… y tu cerebro ve el movimiento contrario.",
         cap="Tus neuronas del movimiento | se *cansan*… | y ves el *contrario*"),
    dict(id="cta", who="nar", cut=True, say="Comenta qué has visto, " + CTA_MAS, cap="¿Qué has visto? | *COMENTA* | y *SÍGUEME*"),
]))


# =============================================================== 2 · efecto Troxler
_tr = random.Random(12)
BLOBS = [(_tr.uniform(120, W - 120), _tr.uniform(700, 1550), _tr.uniform(110, 190),
          _tr.choice([0xFFE89AB8, 0xFF9AC8E8, 0xFFB8E89A, 0xFFE8D29A, 0xFFC4A8E8])) for _ in range(9)]


def blobs(c, a=1.0):
    for (x, y, r, col) in BLOBS:
        if abs(x - W / 2) < 160 and abs(y - 1080) < 160:
            continue
        p = skia.Paint(AntiAlias=True, Color=with_alpha(col, 0.85 * a))
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.55))
        c.drawCircle(x, y, r, p)


def s_troxler(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    c.clear(0xFF8E8E92)
    if sid in ("h", "s1", "s3"):
        blobs(c)
        c.drawCircle(W / 2, 1080, 13, fill(0xFFFF1A2A))
        if sid == "s1":
            stare_timer(c, sg, t, V["accent"])
        label(c, t, "PRUEBA · NO MUEVAS LOS OJOS", V["accent"])
        return
    if sid == "s2":
        blobs(c, 0.35)
        c.drawCircle(W / 2, 1080, 13, fill(0xFFFF1A2A))
        K.tag(c, W / 2, 1400, "EFECTO TROXLER", lt - 0.5, accent=V["accent"], size=44)
        return
    blobs(c, 0.5)


VIDEOS.append(dict(slug="52_troxler", accent=0xFFFFD23F, a2=0xFF4DE1FF, scene=s_troxler, clean=True, segs=[
    dict(id="h", who="nar", say="Mira fijamente el punto rojo y no muevas los ojos. Los colores van a desaparecer.",
         cap="Mira el *punto rojo*… | y no muevas los ojos. | Los colores van a *desaparecer*"),
    dict(id="s1", who="nar", say="Sigue mirando.", cap="Sigue *mirando*", hold=14.0),
    dict(id="s2", who="nar", cut=True,
         say="¿Han desaparecido? Es el efecto Troxler: si algo de tu vista lateral no cambia, tu cerebro deja de verlo.",
         cap="¿Han *desaparecido*? | Si algo no cambia… | tu cerebro deja de *verlo*"),
    dict(id="s3", who="nar", say="Mueve un poco los ojos… y vuelven.", cap="Mueve los ojos… | y *vuelven*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="¿Te ha funcionado? Comenta, " + CTA_MAS, cap="¿Te ha funcionado? | *COMENTA* | y *SÍGUEME*"),
]))


# =============================================================== 3 · lilac chaser
def lilac(c, t, run=True):
    n = 12
    R = 330
    cx, cy = W / 2, 1080
    off = int((t / 0.1)) % n if run else -1
    for k in range(n):
        if k == off:
            continue
        a = k * 2 * math.pi / n
        p = skia.Paint(AntiAlias=True, Color=0xFFE07AD8)
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26))
        c.drawCircle(cx + math.cos(a) * R, cy + math.sin(a) * R, 52, p)
    c.drawLine(cx - 22, cy, cx + 22, cy, stroke(INK, 6))
    c.drawLine(cx, cy - 22, cx, cy + 22, stroke(INK, 6))


def s_lilac(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    c.clear(0xFFB4B4B8)
    if sid in ("h", "s1", "s2"):
        lilac(c, t)
        if sid == "s1":
            stare_timer(c, sg, t, V["accent"])
        label(c, t, "PRUEBA · MIRA LA CRUZ", V["accent"])
        return
    lilac(c, t, run=False)
    if sid == "s3":
        K.tag(c, W / 2, 1520, "TU CEREBRO INVENTA EL VERDE", lt - 0.6, accent=V["accent"], size=40)


VIDEOS.append(dict(slug="53_punto_verde", accent=0xFF2FD46B, a2=0xFFE07AD8, scene=s_lilac, clean=True, segs=[
    dict(id="h", who="nar", say="Mira la cruz del centro. En unos segundos vas a ver algo que no existe.",
         cap="Mira la *cruz*… | vas a ver algo | que *NO EXISTE*"),
    dict(id="s1", who="nar", say="No apartes la vista de la cruz.", cap="No apartes la vista | de la *cruz*", hold=12.0),
    dict(id="s2", who="nar", cut=True,
         say="¿Ves un punto verde dando vueltas? No existe. Y los puntos rosas… han desaparecido.",
         cap="¿Ves un punto *VERDE*? | No existe… | y los rosas *desaparecen*"),
    dict(id="s3", who="nar", cut=True,
         say="Tu ojo se cansa del rosa y ve su color contrario, el verde. Y el cerebro borra lo que no cambia.",
         cap="Tu ojo se cansa del rosa… | y ve su *contrario*: el verde"),
    dict(id="cta", who="nar", cut=True, say="¿Lo has visto? Comenta, " + CTA_MAS, cap="¿Lo has visto? | *COMENTA* | y *SÍGUEME*"),
]))


# =============================================================== 4 · el pie y el 6
def foot_circle(c, x, y, R, t, direction=1.0, a=1.0):
    arc = skia.Path()
    ang = (t * 240 * direction) % 360
    arc.addArc(skia.Rect.MakeXYWH(x - R, y - R, 2 * R, 2 * R), ang, 290 * direction)
    c.drawPath(arc, stroke(with_alpha(WHITE, a), 18))
    end = math.radians(ang + 290 * direction)
    ex, ey = x + math.cos(end) * R, y + math.sin(end) * R
    tang = end + math.pi / 2 * direction
    p = skia.Path()
    p.moveTo(ex + math.cos(tang) * 40, ey + math.sin(tang) * 40)
    p.lineTo(ex + math.cos(tang + 2.3) * 32, ey + math.sin(tang + 2.3) * 32)
    p.lineTo(ex + math.cos(tang - 2.3) * 32, ey + math.sin(tang - 2.3) * 32)
    p.close()
    c.drawPath(p, fill(with_alpha(WHITE, a)))


def six_path(x, y, s):
    p = skia.Path()
    p.moveTo(x + 60 * s, y - 170 * s)
    p.cubicTo(x - 60 * s, y - 170 * s, x - 110 * s, y - 40 * s, x - 100 * s, y + 50 * s)
    p.cubicTo(x - 90 * s, y + 160 * s, x + 90 * s, y + 160 * s, x + 95 * s, y + 60 * s)
    p.cubicTo(x + 100 * s, y - 30 * s, x - 70 * s, y - 40 * s, x - 100 * s, y + 50 * s)
    return p


def s_pie(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    hc.aurora(c, t, V["accent"], V["a2"], 14)
    label(c, t, "PRUEBA · HAZLO AHORA", V["accent"])
    if sid in ("h", "s1", "s2"):
        foot_circle(c, 300, 1150, 170, t, 1.0)
        pill(c, 300, 1400, "PIE DERECHO ↻", 36, bg=WHITE, fg=INK)
    if sid in ("s1", "s2"):
        p = six_path(800, 1130, 1.3)
        meas = skia.PathMeasure(p, False)
        seg = skia.Path()
        f = ((t - P["tl"]["s1"][0]) * 0.6) % 1.0
        meas.getSegment(0, meas.getLength() * f, seg, True)
        c.drawPath(p, stroke(with_alpha(WHITE, 0.15), 18))
        c.drawPath(seg, stroke(V["accent"], 18))
        pill(c, 800, 1400, "MANO: DIBUJA UN 6", 36, bg=V["accent"], fg=INK)
        if sid == "s1":
            stare_timer(c, sg, t, V["accent"], y=1600)
    if sid == "s2":
        hc.big(c, "¿HA CAMBIADO?", W / 2, 820, 100, V["accent"], lt, 0.3)
    if sid == "s3":
        hc.brain(c, W / 2, 1050, 1.15, t)
        K.tag(c, W / 2, 1450, "ÓRDENES CONTRARIAS = LÍO", lt - 0.5, accent=V["accent"], size=40)


VIDEOS.append(dict(slug="54_pie_y_seis", accent=0xFFFFB86B, a2=0xFF3C8CFF, scene=s_pie, segs=[
    dict(id="h", who="nar", say="Haz esto ahora: mueve el pie derecho en círculos, como las agujas del reloj.",
         cap="Haz esto *AHORA*: | pie derecho en *círculos*"),
    dict(id="s1", who="nar", say="Sin parar… dibuja un seis en el aire con la mano derecha.",
         cap="Sin parar… | dibuja un *6* | con la mano derecha", hold=4.0),
    dict(id="s2", who="nar", cut=True, say="¿Tu pie ha cambiado de dirección? A casi todo el mundo le pasa.",
         cap="¿Tu pie ha *cambiado*? | A casi todos | les *pasa*"),
    dict(id="s3", who="nar", cut=True,
         say="A tu cerebro le cuesta muchísimo dar órdenes contrarias a la mano y al pie del mismo lado.",
         cap="A tu cerebro le cuesta | dar órdenes *contrarias* | al mismo lado"),
    dict(id="cta", who="nar", cut=True, say="¿Lo has conseguido? Comenta, " + CTA_MAS,
         cap="¿Lo has conseguido? | *COMENTA* | y *SÍGUEME*"),
]))


# =============================================================== 5 · ceguera al cambio
_cb = random.Random(21)
FLASHES = sorted([_cb.uniform(0.8, 13.0) for _ in range(9)])
FPOS = [(_cb.uniform(150, W - 150), _cb.uniform(700, 1500)) for _ in range(9)]
DIST = [(_cb.uniform(0, W), _cb.uniform(650, 1550), _cb.uniform(20, 60), _cb.uniform(0, 6.28)) for _ in range(14)]
C0, C1 = 0xFF1B3A8A, 0xFF8A1B4A


def s_cambio(c, t, P, V):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    tl = P["tl"]
    a1, b1 = tl["s1"]
    p = clamp((t - a1) / (b1 - a1))
    if sid in ("h",):
        p = 0.0
    if sid in ("s2", "s3", "s4", "cta"):
        p = 1.0
    bg = lerp_color(C0, C1, ease_in_out(p))
    c.clear(bg)
    if sid in ("h", "s1"):
        for (x, y, r, ph) in DIST:
            c.drawCircle(x + math.sin(t + ph) * 40, y + math.cos(t * 0.8 + ph) * 40, r, fill(with_alpha(WHITE, 0.10)))
        if sid == "s1":
            for ft, (x, y) in zip(FLASHES, FPOS):
                d = (t - a1) - ft
                if 0 <= d < 0.35:
                    c.drawCircle(x, y, 26, fill(with_alpha(WHITE, 1 - d / 0.35)))
        label(c, t, "PRUEBA · CUENTA LOS PUNTOS", V["accent"])
        return
    if sid == "s2":
        hc.big(c, "9", W / 2, 1050, 300, WHITE, lt, 0.8)
        return
    if sid in ("s3", "s4"):
        sp = ease_out(prog(t - tl["s3"][0], 0.3, 1.0))
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W / 2 * sp, H), fill(C0))
        if sp > 0.95:
            pill(c, W / 4, 1150, "AL EMPEZAR", 34, bg=WHITE, fg=INK)
            pill(c, W * 3 / 4, 1150, "AHORA", 34, bg=WHITE, fg=INK)
        if sid == "s4":
            K.tag(c, W / 2, 1450, "CEGUERA AL CAMBIO", lt - 0.5, accent=V["accent"], size=44)


VIDEOS.append(dict(slug="55_ceguera_cambio", accent=0xFF4DE1FF, a2=0xFFFF4D6D, scene=s_cambio, segs=[
    dict(id="h", who="nar", say="Cuenta cuántas veces aparece un punto blanco. Concéntrate.",
         cap="Cuenta los puntos | *BLANCOS*. | Concéntrate"),
    dict(id="s1", who="nar", say="Empieza ya.", cap="*Cuenta*…", hold=12.8),
    dict(id="s2", who="nar", cut=True, say="¿Cuántos has contado? Eran nueve.", cap="¿Cuántos? | Eran *9*"),
    dict(id="s3", who="nar", cut=True, say="Pero la pregunta de verdad es: ¿te has dado cuenta de que el fondo ha cambiado de color?",
         cap="Pero… ¿te has dado cuenta | de que el *FONDO* | ha cambiado de color?"),
    dict(id="s4", who="nar", say="Si un cambio es lento, tu cerebro no lo registra. Se llama ceguera al cambio.",
         cap="Si el cambio es *lento*… | tu cerebro | no lo *registra*"),
    dict(id="cta", who="nar", cut=True, say="¿Te habías dado cuenta? Comenta, " + CTA_MAS,
         cap="¿Te habías dado cuenta? | *COMENTA* | y *SÍGUEME*"),
]))


def make_scene(V):
    return lambda c, t, P: V["scene"](c, t, P, V)


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = "auto" if len(sys.argv) > 2 else None
    for i in idxs:
        V = VIDEOS[i]
        K.run(V, make_scene(V), OUT, preview=pv)
