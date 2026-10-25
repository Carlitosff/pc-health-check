"""34 · Si metieras el Everest en la fosa de las Marianas…"""
import math, random, sys
import numpy as np
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, pill
from engine import lerp_color

V = dict(slug="34_marianas", accent=0xFF4DE1FF, drone=0.03, segs=[
    dict(id="h", who="nar", say="Si metieras el Everest aquí… su cima quedaría a dos kilómetros bajo el agua.",
         cap="Si metieras el *Everest* aquí… | su cima quedaría | a *2 km* bajo el agua"),
    dict(id="s1", who="nar", cut=True,
         say="Es la fosa de las Marianas. Su punto más hondo, el abismo Challenger, está a casi once mil metros.",
         cap="Fosa de las *Marianas*: | casi *11.000 m*"),
    dict(id="s2", who="nar", cut=True, say="Bajemos. A doscientos metros, la luz del sol ya casi no llega.",
         cap="Bajemos… | a *200 m*: | casi *sin luz*"),
    dict(id="s3", who="nar", say="A partir de mil… oscuridad total.", cap="A *1.000 m*: | oscuridad *TOTAL*"),
    dict(id="q", who="q", say="¿Ha llegado más gente al fondo de la fosa… o a la Luna?",
         cap="¿Más gente en el fondo… | o en la *Luna*?", quiz=dict(a="LA LUNA", b="EL FONDO", ans="b")),
    dict(id="r", who="nar", cut=True,
         say="Al fondo. Pero durante casi sesenta años, solo tres personas lo habían conseguido.",
         cap="Al *FONDO*… | pero durante 60 años | solo *3 personas*"),
    dict(id="s4", who="nar", say="Aquí abajo, la presión es más de mil veces la de la superficie.",
         cap="Aquí la presión es | *+1.000 veces* | la de la superficie"),
    dict(id="s5", who="nar", say="Y aun así, hay vida: se han filmado peces a más de ocho mil metros de profundidad.",
         cap="Y aun así… hay *vida*: | peces a más de | *8.000 m*"),
    dict(id="cta", who="nar", cut=True, say="¿Bajarías tú? ¡Comenta y sígueme para más!",
         cap="¿Bajarías tú? | *COMENTA* | y *SÍGUEME*"),
])

ACC = V["accent"]
_r = random.Random(4)
SNOW = [(_r.uniform(0, W), _r.uniform(0, 4000), _r.uniform(1, 4), _r.uniform(0.2, 0.8), _r.uniform(0.2, 1.0)) for _ in range(380)]
BIO = [(_r.uniform(0, W), _r.uniform(0, 3000), _r.uniform(2, 6), _r.uniform(0, 6.28), _r.choice([0xFF4DE1FF, 0xFF7CFFCB, 0xFFB08CFF]))
       for _ in range(50)]
DEPTH_MAX = 10935.0


def depth_at(t, tl):
    """Profundidad en metros a lo largo del vídeo."""
    keys = [(tl["s2"][0], 0), (tl["s2"][0] + 2.4, 200), (tl["s3"][0] + 0.2, 200), (tl["s3"][0] + 2.0, 1000),
            (tl["q"][0], 1200), (tl["r"][0], 7000), (tl["r"][0] + 3.0, 10935)]
    if t <= keys[0][0]:
        return 0.0
    for (t0, d0), (t1, d1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            return lerp(d0, d1, ease_in_out(prog(t, t0, t1)))
    return DEPTH_MAX


def water_color(d):
    stops = [(0, 0xFF1C8FC8), (150, 0xFF0D5E95), (400, 0xFF06345E), (1000, 0xFF021428), (3000, 0xFF01070F), (11000, 0xFF000204)]
    for (d0, c0), (d1, c1) in zip(stops, stops[1:]):
        if d <= d1:
            return lerp_color(c0, c1, (d - d0) / (d1 - d0))
    return stops[-1][1]


def everest_path(base_x, base_y, h, w):
    rnd = random.Random(8)
    p = skia.Path()
    p.moveTo(base_x - w, base_y)
    n = 22
    for i in range(1, n):
        f = i / n
        x = base_x - w + 2 * w * f
        prof = 1 - abs(f - 0.47) / 0.53
        y = base_y - h * (prof ** 1.25) + rnd.uniform(-1, 1) * h * 0.04 * (1 - prof)
        p.lineTo(x, y)
    p.lineTo(base_x + w, base_y)
    p.close()
    return p


def cross_section(c, t, lt, P, everest_a=1.0, ruler_a=0.0):
    tl = P["tl"]
    top, bottom = 640.0, 1720.0
    sc = (bottom - top) / DEPTH_MAX
    # cielo y agua
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, top), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, 0), (0, top)], [0xFF0A1A33, 0xFF4A86B8])))
    c.drawRect(skia.Rect.MakeLTRB(0, top, W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, top), (0, bottom)], [0xFF1C8FC8, 0xFF06345E, 0xFF01070F], [0, 0.3, 1])))
    # oleaje
    wave = skia.Path()
    wave.moveTo(0, top)
    for x in range(0, W + 20, 20):
        wave.lineTo(x, top + math.sin(x / 60 + t * 2) * 5)
    c.drawPath(wave, stroke(0xFFBFEFFF, 4))
    # fondo marino con la fosa
    rnd = random.Random(2)
    sea = skia.Path()
    sea.moveTo(0, H)
    pts = [(0, top + 4200 * sc), (180, top + 5200 * sc), (330, top + 6500 * sc), (440, top + 9800 * sc),
           (520, bottom), (600, bottom - 20), (690, top + 8800 * sc), (820, top + 6200 * sc), (1000, top + 5600 * sc),
           (W, top + 5400 * sc)]
    for x, y in pts:
        sea.lineTo(x, y + rnd.uniform(-8, 8))
    sea.lineTo(W, H)
    sea.close()
    c.drawPath(sea, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, top + 4000 * sc), (0, H)],
                                                                    [0xFF3A3328, 0xFF15110C]), AntiAlias=True))
    c.drawPath(sea, stroke(0xFF6A5A44, 3))
    # Everest dentro de la fosa
    if everest_a > 0:
        h = 8849 * sc * ease_out(clamp(everest_a))
        ev = everest_path(560, bottom, h, 260)
        c.drawPath(ev, skia.Paint(Shader=skia.GradientShader.MakeLinear([(560, bottom - h), (560, bottom)],
                                                                         [0xFFB8C2D8, 0xFF5A6070, 0xFF2A2E38]),
                                  AntiAlias=True, Alphaf=clamp(everest_a)))
        c.save()
        c.clipPath(ev)
        c.drawRect(skia.Rect.MakeLTRB(0, bottom - h - 5, W, bottom - h + 150 * ease_out(clamp(everest_a))),
                   fill(with_alpha(0xFFFFFFFF, 0.85 * clamp(everest_a))))
        c.restore()
        peak = bottom - h
        if everest_a >= 1:
            # cota de 2 km
            x0 = 780
            c.drawLine(x0, top, x0, peak, stroke(ACC, 6))
            c.drawLine(x0 - 20, top, x0 + 20, top, stroke(ACC, 6))
            c.drawLine(x0 - 20, peak, x0 + 20, peak, stroke(ACC, 6))
            c.drawLine(560, peak, x0 - 20, peak, stroke(with_alpha(ACC, 0.5), 3))
            pill(c, x0 + 110, (top + peak) / 2, "≈ 2 km", 40, bg=ACC, fg=INK, scale=ease_back(prog(lt, 1.0, 1.3)))
            pill(c, 560, peak - 50, "EVEREST", 32, bg=WHITE, fg=INK, scale=ease_back(prog(lt, 0.7, 1.0)))
    if ruler_a > 0:
        x0 = 980
        c.drawLine(x0, top, x0, lerp(top, bottom, ease_out(ruler_a)), stroke(WHITE, 4))
        for k in range(0, 12):
            y = top + k * 1000 * sc
            if y <= lerp(top, bottom, ease_out(ruler_a)):
                c.drawLine(x0 - (22 if k % 5 == 0 else 12), y, x0, y, stroke(WHITE, 3))
        if ruler_a >= 1:
            ring = (t * 1.2) % 1
            c.drawCircle(560, bottom - 4, 10 + ring * 40, stroke(with_alpha(ACC, 1 - ring), 4))
            c.drawCircle(560, bottom - 4, 9, fill(ACC))
            pill(c, 560, bottom - 70, "ABISMO CHALLENGER", 30, bg=ACC, fg=INK)


def submarine(c, x, y, t, light=1.0):
    bob = math.sin(t * 1.6) * 8
    y += bob
    # haz de luz
    if light > 0:
        beam = skia.Path()
        beam.moveTo(x + 120, y + 10)
        beam.lineTo(x + 700, y - 220)
        beam.lineTo(x + 700, y + 380)
        beam.close()
        g = skia.GradientShader.MakeLinear([(x + 120, y), (x + 700, y)],
                                           [with_alpha(0xFFBFEFFF, 0.45 * light), with_alpha(0xFFBFEFFF, 0)])
        c.drawPath(beam, skia.Paint(Shader=g, AntiAlias=True, BlendMode=skia.BlendMode.kPlus))
        K.glow(c, x + 125, y + 10, 70, 0xFFE8FBFF, 0.9 * light)
    body = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 150, y - 70, 280, 150), 75, 75)
    c.drawRRect(body, skia.Paint(Shader=skia.GradientShader.MakeLinear([(x, y - 70), (x, y + 80)],
                                                                       [0xFFFFFFFF, 0xFFE8EEF4, 0xFF8A96A6]), AntiAlias=True))
    c.drawRect(skia.Rect.MakeXYWH(x - 150, y + 20, 280, 22), fill(0xFFFF7A1A))
    c.drawCircle(x + 70, y - 5, 34, fill(0xFF1A2E44))
    c.drawCircle(x + 70, y - 5, 34, stroke(0xFF6A7A8A, 7))
    c.drawCircle(x + 60, y - 15, 9, fill(with_alpha(WHITE, 0.5)))
    c.drawRect(skia.Rect.MakeXYWH(x - 185, y - 30, 40, 60), fill(0xFF6A7A8A))
    a = t * 20
    c.drawLine(x - 190, y, x - 190 + 6 * math.cos(a), y - 34 * math.sin(a), stroke(0xFF3A4450, 8))
    # burbujas
    for k in range(6):
        ph = (t * 0.8 + k / 6) % 1
        c.drawCircle(x - 120 + math.sin(k * 3 + t) * 15, y - 80 - ph * 300, 4 + 4 * (1 - ph),
                     stroke(with_alpha(0xFFBFEFFF, 0.6 * (1 - ph)), 2))


def dive(c, t, P):
    tl = P["tl"]
    d = depth_at(t, tl)
    c.drawPaint(fill(water_color(d)))
    # rayos de sol cerca de la superficie
    ra = clamp(1 - d / 350)
    if ra > 0:
        for k in range(6):
            x = 120 + k * 180 + math.sin(t * 0.5 + k) * 40
            ray = skia.Path()
            ray.moveTo(x - 30, -50); ray.lineTo(x + 30, -50); ray.lineTo(x + 260, H); ray.lineTo(x + 80, H); ray.close()
            g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [with_alpha(0xFFBFEFFF, 0.22 * ra), with_alpha(0xFFBFEFFF, 0)])
            c.drawPath(ray, skia.Paint(Shader=g, BlendMode=skia.BlendMode.kPlus))
    # nieve marina (sube al bajar)
    off = d * 1.4
    p = skia.Paint(AntiAlias=True)
    for (x, y, r, a, dep) in SNOW:
        yy = (y - off * dep) % 4000 - 1000
        if -10 < yy < H + 10:
            p.setColor(with_alpha(0xFFDDEFFF, a * (0.5 if d < 300 else 0.8)))
            c.drawCircle(x + math.sin(t + y) * 6, yy, r * dep, p)
    # bioluminiscencia en lo profundo
    ba = prog(d, 1200, 3000)
    if ba > 0:
        for (x, y, r, ph, col) in BIO:
            yy = (y - off * 0.6) % 3000 - 500
            if -20 < yy < H + 20:
                fl = 0.5 + 0.5 * math.sin(t * 3 + ph)
                K.glow(c, x, yy, r * 6, col, 0.6 * ba * fl)
    # fondo marino al llegar
    fa = prog(d, 10200, 10935)
    if fa > 0:
        yb = lerp(H + 200, 1500, ease_out(fa))
        sea = skia.Path()
        sea.moveTo(0, H)
        for x in range(0, W + 40, 40):
            sea.lineTo(x, yb + math.sin(x / 90) * 25)
        sea.lineTo(W, H)
        sea.close()
        c.drawPath(sea, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, yb), (0, H)], [0xFF4A4438, 0xFF15120E]),
                                   AntiAlias=True))
    submarine(c, 380, 1050, t, light=prog(d, 120, 400))
    # profundímetro lateral
    x0 = 1000
    c.drawLine(x0, 600, x0, 1700, stroke(with_alpha(WHITE, 0.35), 4))
    yy = lerp(600, 1700, d / DEPTH_MAX)
    c.drawCircle(x0, yy, 12, fill(ACC))
    return d


def fish(c, t, lt):
    """Pez caracol: cuerpo translúcido rosado, iluminado por el foco."""
    x = lerp(1250, 700, ease_out(prog(lt, 0, 2.5))) + math.sin(t * 1.3) * 20
    y = 1060 + math.sin(t * 2.1) * 25
    sw = math.sin(t * 7) * 18
    body = skia.Path()
    body.moveTo(x - 70, y)
    body.cubicTo(x - 70, y - 65, x + 40, y - 70, x + 120, y - 25)
    body.cubicTo(x + 200, y - 10 + sw * 0.3, x + 240, y + sw, x + 260, y + 5 + sw)
    body.cubicTo(x + 230, y + 30 + sw, x + 150, y + 40, x + 60, y + 55)
    body.cubicTo(x - 10, y + 65, x - 70, y + 45, x - 70, y)
    c.drawPath(body, skia.Paint(Shader=skia.GradientShader.MakeLinear([(x - 70, y), (x + 260, y)],
                                                                      [0xEEF4C8D2, 0xCCE8A8B8, 0x66D890A6]), AntiAlias=True))
    c.drawPath(body, stroke(0x88FFFFFF, 2))
    c.drawCircle(x - 30, y - 18, 9, fill(0xFF1A1018))
    c.drawCircle(x - 33, y - 21, 3, fill(WHITE))
    K.glow(c, x + 60, y, 220, 0xFFFFE0E8, 0.12)


def scene(c, t, P):
    tl = P["tl"]
    sg = K.seg_at(P, t)
    sid = sg["id"]
    lt = t - sg["a"]
    c.clear(0xFF000000)
    if sid == "h":
        cross_section(c, t, t + 1.4, P, everest_a=1.0)
    elif sid == "s1":
        cross_section(c, t, lt, P, everest_a=1 - prog(lt, 0, 0.6), ruler_a=prog(lt, 0.5, 1.6))
        K.counter(c, t, lt - 1.4, lambda p: K.fmt(10935 * p) + " m", "PROFUNDIDAD", ACC, y=1330, size=110)
    else:
        d = dive(c, t, P)
        if sid in ("s2", "s3"):
            K.counter(c, t, 0.0 + (t - tl["s2"][0]), lambda p: K.fmt(d) + " m",
                      "CASI SIN LUZ" if sid == "s2" else "OSCURIDAD TOTAL", ACC, y=1560, size=110, dur=0.01)
        elif sid == "r":
            if lt > 1.7:
                K.counter(c, t, lt - 1.7, lambda p: K.fmt(d) + " m", "EL FONDO", ACC, y=1560, size=110, dur=0.01)
        elif sid == "s4":
            shake = math.sin(t * 50) * 3 * prog(lt, 0.5, 1.0)
            c.translate(shake, 0)
            K.counter(c, t, lt - 0.3, lambda p: "+" + K.fmt(1000 * p) + " ×", "LA PRESIÓN DE LA SUPERFICIE", ACC, y=1560, size=110)
        elif sid == "s5":
            fish(c, t, lt)
            K.tag(c, W / 2, 1560, "PEZ CARACOL · +8.000 m", lt - 0.8, accent=ACC, size=36)
        elif sid == "cta":
            pass


if __name__ == "__main__":
    K.run(V, scene, "/home/claude/tiktok/out35", preview="auto" if len(sys.argv) > 1 else None)
