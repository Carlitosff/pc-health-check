"""Lote diario 26/10/2026 (101–110). Motor v4 (punch-in de gancho, tease 'mira hasta el final', insignia de serie,
ducking del dron). Mezcla: 3 tests de percepción (lo que más rinde en IG), 2 mitos, 2 series (Voyager P2, Luna P2),
1 historia en partes (Phineas Gage P1, cliffhanger implícito), 1 récord real (Vesna Vulović), 1 test de espejo."""
import math, sys, random
import numpy as np
import skia
from PIL import Image, ImageFilter
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import spheres as S
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow, pill
from core import draw_text, font, text_w

OUT = "/home/claude/tiktok/outdaily"
TEASE = "MIRA HASTA EL FINAL"


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


def img_from(arr):
    a = np.ascontiguousarray(arr.astype(np.uint8))
    return skia.Image.fromarray(a, colorType=skia.kRGBA_8888_ColorType)


# ====================================================================== 101 Stroop
COLS = {"ROJO": 0xFFFF3B3B, "AZUL": 0xFF3B7BFF, "VERDE": 0xFF2FD46B, "AMARILLO": 0xFFFFD43B, "MORADO": 0xFFB04DFF,
        "NARANJA": 0xFFFF8A2A}
STROOP = [("AZUL", "ROJO"), ("VERDE", "AMARILLO"), ("ROJO", "VERDE"), ("AMARILLO", "AZUL"), ("MORADO", "NARANJA"),
          ("NARANJA", "MORADO"), ("AZUL", "VERDE"), ("ROJO", "AZUL"), ("VERDE", "ROJO"), ("AMARILLO", "MORADO")]


def s_stroop(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF2A1050, 0xFF0A2A4A)
    if sid in ("h", "g1", "g2"):
        a0 = P["tl"]["h"][0]
        # palabras: una cada 1,05 s desde el gancho
        k = int(max(0, t) / 1.05)  # primera palabra ya en el frame 0 (gancho visual inmediato)
        word, col = STROOP[k % len(STROOP)]
        lk = max(0, t) % 1.05
        s = ease_back(clamp(lk / 0.22), 2.6)
        c.save(); c.translate(W / 2 + math.sin(t * 2) * 10, 1150); c.scale(s, s); c.rotate(math.sin(k * 1.7) * 4)
        glow(c, 0, -60, 420, COLS[col], 0.22)
        draw_text(c, word, 0, 70, 190 if len(word) < 7 else 160, COLS[col], outline=14)
        c.restore()
        # pista de lo que hay que decir
        if sid == "h":
            pill(c, W / 2, 1480, "DI EL COLOR, NO LA PALABRA", 40, bg=WHITE, fg=INK, scale=ease_back(prog(lt, 0.3, 0.6)))
        hc.timer(c, W / 2, 1640, 70, clamp((t - 0.6) / 12.0), str(min(10, k + 1)), V["accent"])
    else:
        hc.brain(c, W / 2, 1150, 1.25, t)
        # dos señales que chocan
        for side, (lab, col) in enumerate((("LEER", 0xFF4DE1FF), ("COLOR", 0xFFFF7AD9))):
            x = W / 2 + (-1 if side == 0 else 1) * lerp(420, 120, ease_in_out(clamp(lt / 1.2)))
            glow(c, x, 1100, 120, col, 0.8)
            K.tag(c, x, 1480 + side * 0, lab, lt - 0.1 - 0.15 * side, accent=col, size=40)
        if sid == "s1":
            hc.big(c, "1935", W / 2, 1650, 150, V["accent"], lt, 0.2)
        if sid == "s2":
            hc.stamp(c, "AUTOMÁTICO", W / 2, 1650, lt, 0.3, 110)


V101 = dict(slug="101_stroop", accent=0xFFFFD43B, drone=0.015, scene=s_stroop, tease=TEASE, segs=[
    dict(id="h", who="nar", say="Di en voz alta el color… no la palabra. Rápido.", cap="Di el *COLOR*… | no la *palabra*"),
    dict(id="g1", who="q", say="Vamos. No pares.", cap="*Vamos*… | no pares", hold=3.2),
    dict(id="g2", who="q", say="Más rápido.", cap="*Más rápido*", hold=3.0),
    dict(id="s1", who="nar", cut=True, say="¿Te has trabado? Le pasa a casi todo el mundo. Se llama efecto Stroop, y lo publicó John Ridley Stroop en mil novecientos treinta y cinco.",
         cap="¿Te has *trabado*? | Es el efecto *Stroop*. | Lo publicó en *1935*"),
    dict(id="s2", who="nar", cut=True, say="Leer es tan automático para tu cerebro, que lee la palabra antes de que puedas evitarlo.",
         cap="Leer es tan *automático*… | que tu cerebro lee | *antes* de que puedas evitarlo"),
    dict(id="s3", who="nar", say="Y esas dos órdenes chocan dentro de tu cabeza.", cap="Y las dos órdenes | *chocan*"),
    dict(id="cta", who="nar", cut=True, say="¿Cuántas acertaste sin trabarte? Comenta tu número. Y sígueme, que mañana viene otro más difícil.",
         cap="¿Cuántas *acertaste*? | *COMENTA* tu número | y *SÍGUEME*"),
])


# ====================================================================== 102 Agujero que se expande (Laeng 2022)
_HOLE = None


def hole_img():
    global _HOLE
    if _HOLE is None:
        S2 = 1400
        im = Image.new("L", (S2, S2), 245)
        arr = np.full((S2, S2), 245.0)
        rng = np.random.default_rng(7)
        yy, xx = np.mgrid[0:S2, 0:S2]
        cx = cy = S2 / 2
        r = np.hypot(xx - cx, yy - cy)
        # agujero central difuso
        arr -= 245 * np.exp(-(r / 300) ** 3.0)
        # puntos negros con densidad y tamaño que crecen hacia el centro
        from PIL import ImageDraw
        dots = Image.new("L", (S2, S2), 0)
        d = ImageDraw.Draw(dots)
        for _ in range(2400):
            ang = rng.uniform(0, 2 * math.pi)
            rr = 230 + rng.gamma(1.4, 130)
            if rr > S2 * 0.7:
                continue
            x, y = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr
            rad = max(3, 24 - rr / 32) * rng.uniform(0.6, 1.1)
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=int(255 * min(1, 1.25 - rr / 700)))
        dots = dots.filter(ImageFilter.GaussianBlur(5))
        arr -= np.asarray(dots, float) * 0.75
        im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
        g = (255 * (np.asarray(im, float) / 255) ** 2.2).astype(np.uint8)  # centro negro profundo
        rgba = np.zeros((S2, S2, 4), np.uint8)
        rgba[..., 0] = g; rgba[..., 1] = g; rgba[..., 2] = np.clip(g * 1.0 + 4, 0, 255); rgba[..., 3] = 255
        _HOLE = img_from(rgba)
    return _HOLE


def s_hole(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFFE9E9ED)  # = blanco de la textura tras la corrección gamma (sin bordes visibles)
    im = hole_img()
    z = 1.05 + 0.10 * ease_in_out(clamp(t / 40))  # zoom muy lento: acompaña la ilusión
    sz = 1400 * z
    c.drawImageRect(im, skia.Rect.MakeXYWH(W / 2 - sz / 2, 1060 - sz / 2, sz, sz), skia.SamplingOptions(skia.FilterMode.kLinear))
    # punto de fijación
    if sid in ("h", "s1", "s4"):
        c.drawCircle(W / 2, 1060, 9 + 3 * math.sin(t * 6), fill(0xFFFF3B4A))
    if sid == "s2":
        K.counter(c, t, lt - 0.2, lambda p: f"{int(round(86 * p))}%", "LO VE MOVERSE", 0xFFFF3B4A, y=1640)
    if sid == "s3":
        # pupila que se dilata
        R = 90; pr = lerp(28, 62, ease_in_out(clamp(lt / 1.8)))
        c.drawCircle(W / 2, 1650, R + 10, fill(0x66000000))
        c.drawCircle(W / 2, 1650, R, fill(0xFF5A8A6A))
        c.drawCircle(W / 2, 1650, pr, fill(0xFF050505))
        c.drawCircle(W / 2 - 30, 1620, 12, fill(with_alpha(WHITE, 0.8)))
        K.tag(c, W / 2, 1800, "LA PUPILA SE DILATA", lt - 0.4, accent=0xFFFF3B4A, size=32)


V102 = dict(slug="102_agujero", accent=0xFFFF3B4A, drone=0.03, scene=s_hole, clean=True, tease="NO APARTES LA VISTA", segs=[
    dict(id="h", who="nar", say="Mira el punto rojo y no apartes la vista. ¿Notas cómo el agujero se hace más grande?",
         cap="Mira el *punto rojo*… | ¿el agujero se hace | más *GRANDE*?", hold=0.8),
    dict(id="s1", who="nar", say="Como si te fueras metiendo dentro. Pues no se mueve. Es una imagen quieta.",
         cap="Como si *cayeras* dentro… | No se mueve. | Es una imagen *QUIETA*", hold=0.6),
    dict(id="s2", who="nar", cut=True, say="En dos mil veintidós, el psicólogo Bruno Laeng la probó con cincuenta personas. Al ochenta y seis por ciento le pasa lo mismo que a ti.",
         cap="En *2022*, Bruno *Laeng* | la probó con 50 personas: | al *86%* le pasa"),
    dict(id="s3", who="nar", cut=True, say="Y lo más loco: sus pupilas se dilataban, como si de verdad entraran en la oscuridad.",
         cap="Lo más loco: | sus *pupilas* se dilataban | como entrando en la *oscuridad*"),
    dict(id="s4", who="nar", say="Tu ojo no reacciona a la luz real… sino a lo que tu cerebro cree que está viendo. Vuelve a mirar el punto rojo.",
         cap="Tu ojo reacciona a lo que | tu cerebro *CREE* que ve. | Vuelve a mirar el *punto*"),
    dict(id="cta", who="nar", cut=True, say="¿Tú lo has visto moverse? Comenta sí o no. Y sígueme para más ilusiones.",
         cap="¿Lo has visto *moverse*? | Comenta *SÍ* o *NO* | y *SÍGUEME*"),
])


# ====================================================================== 103 Ebbinghaus
def ebb(c, cx, cy, ring_r, ring_n, ring_size, core_r, t, spread=0.0, col=0xFFFF8A2A):
    for k in range(ring_n):
        a = 2 * math.pi * k / ring_n + t * 0.15
        rr = ring_r * (1 + spread * 1.8)
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        al = 1 - spread * 0.8
        c.drawCircle(x, y + 6, ring_size, fill(with_alpha(0xFF000000, 0.3 * al)))
        g = skia.GradientShader.MakeRadial((x - ring_size * 0.3, y - ring_size * 0.3), ring_size * 1.4,
                                           [with_alpha(0xFFC8CCD8, al), with_alpha(0xFF6A7080, al)])
        c.drawCircle(x, y, ring_size, skia.Paint(Shader=g, AntiAlias=True))
    c.drawCircle(cx, cy + 8, core_r, fill(0x55000000))
    g = skia.GradientShader.MakeRadial((cx - core_r * 0.3, cy - core_r * 0.3), core_r * 1.4, [0xFFFFC27A, col, 0xFFB84A08])
    c.drawCircle(cx, cy, core_r, skia.Paint(Shader=g, AntiAlias=True))


def s_ebb(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF0A2A4A, 0xFF2A1A40)
    reveal = 0.0
    if "s1" in P["tl"]:
        reveal = ease_in_out(clamp((t - P["tl"]["s1"][0] - 0.3) / 1.6))
    if sid in ("s4", "cta"):
        reveal = 1 - ease_in_out(clamp((t - P["tl"]["s4"][0]) / 0.8))
    core = 62
    lx, rx, y = 290, 790, 980
    lx2 = lerp(lx, 380, reveal); rx2 = lerp(rx, 700, reveal)
    ebb(c, lx2, y, 175, 6, 92, core, t, reveal)
    ebb(c, rx2, y, 112, 9, 22, core, t, reveal)
    if reveal > 0.6:
        a = clamp((reveal - 0.6) / 0.4)
        c.drawLine(lx2 + core, y - core - 30, rx2 - core, y - core - 30, stroke(with_alpha(WHITE, a), 5))
        c.drawLine(lx2 + core, y + core + 30, rx2 - core, y + core + 30, stroke(with_alpha(WHITE, a), 5))
    if sid in ("h", "q"):
        K.tag(c, lx, y - 270, "A", lt - 0.2, accent=WHITE, size=50)
        K.tag(c, rx, y - 270, "B", lt - 0.3, accent=WHITE, size=50)
    if sid == "s2":
        hc.stamp(c, "IGUALES", W / 2, 1560, lt, 0.1, 140, col=0xFF2FD46B)
    if sid == "s3":
        hc.big(c, "1901", W / 2, 1560, 150, V["accent"], lt, 0.2)


V103 = dict(slug="103_ebbinghaus", accent=0xFFFF8A2A, drone=0.02, scene=s_ebb, tease=TEASE, segs=[
    dict(id="h", who="nar", say="Fíjate en los dos círculos naranjas. ¿Cuál es más grande?", cap="¿Qué círculo *naranja* | es más *GRANDE*?"),
    dict(id="q", who="q", say="¿Son distintos, o son iguales?", cap="¿*Distintos* o *iguales*?",
         quiz=dict(a="DISTINTOS", b="IGUALES", ans="b")),
    dict(id="r", who="nar", cut=True, say="Son exactamente iguales.", cap="Son *EXACTAMENTE* | iguales"),
    dict(id="s1", who="nar", say="Quita los círculos de alrededor… y compruébalo tú mismo.", cap="Quita lo de alrededor… | y *compruébalo*"),
    dict(id="s2", who="nar", cut=True, say="Tu cerebro no mide el tamaño de las cosas. Lo compara con lo que tienen al lado.",
         cap="Tu cerebro no *mide*. | *Compara* con lo que | hay al lado"),
    dict(id="s3", who="nar", cut=True, say="Se llama ilusión de Ebbinghaus. Edward Titchener la hizo famosa en mil novecientos uno, y todavía engaña a casi todos.",
         cap="Ilusión de *Ebbinghaus*. | Famosa desde *1901*… | y aún *engaña*"),
    dict(id="s4", who="nar", say="Y lo mejor: aunque ya lo sabes, vuelve a mirarlo. El de la derecha te sigue pareciendo más grande.",
         cap="Aunque ya lo sabes… | el de la derecha | *sigue pareciendo* más grande"),
    dict(id="cta", who="nar", cut=True, say="¿Acertaste a la primera? Comenta. Y sígueme, que la próxima es más difícil.",
         cap="¿Acertaste a la *primera*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 104 Mito: uñas y pelo después de morir
def finger_close(c, cx, cy, s, t, retract=0.0, nail_extra=0.0):
    """Dedo en primer plano (vista superior) con uña: la piel se retrae y deja ver más uña."""
    c.save(); c.translate(cx, cy); c.scale(s, s)
    skin = skia.GradientShader.MakeLinear([(-170, 0), (170, 0)], [0xFFB8735A, 0xFFF4CDB0, 0xFFE3A989, 0xFFB8735A], [0, 0.4, 0.7, 1])
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -380, 340, 1200), 170, 170), skia.Paint(Shader=skia.GradientShader.MakeLinear([(-170, 0), (170, 0)], [0xFF8A4A38, 0xFFD89A7A, 0xFFC8866A, 0xFF8A4A38], [0, 0.4, 0.7, 1]), AntiAlias=True))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-165, -375, 330, 1190), 165, 165), skia.Paint(Shader=skin, AntiAlias=True))
    # pliegues de nudillo
    for k in range(3):
        c.drawArc(skia.Rect.MakeXYWH(-90, 380 + k * 22, 180, 40), 200, 140, False, stroke(with_alpha(0xFF8A4A38, 0.5), 4))
    # uña
    top = -340 - nail_extra * 60
    base = lerp(-60, 20, retract)
    nail = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-115, top, 115, base), 105, 105)
    g = skia.GradientShader.MakeLinear([(0, top), (0, base)], [0xFFF8F2EA, 0xFFF2C8C0, 0xFFE8B0A8], [0, 0.25, 1])
    c.drawRRect(nail, skia.Paint(Shader=g, AntiAlias=True))
    c.drawRRect(nail, stroke(with_alpha(0xFFB87A6A, 0.7), 4))
    # lúnula
    c.drawOval(skia.Rect.MakeLTRB(-70, base - 70, 70, base + 10), fill(with_alpha(WHITE, 0.45)))
    # cutícula (se retrae)
    c.drawArc(skia.Rect.MakeLTRB(-125, base - 40, 125, base + 40), 180, 180, False, stroke(0xFFC8866A, 10))
    c.drawOval(skia.Rect.MakeXYWH(-60, top + 30, 50, 160), fill(with_alpha(WHITE, 0.35)))
    c.restore()


def s_unas(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF2A1A10, 0xFF101A2A)
    retract = 0.0; extra = 0.0
    if sid in ("s2", "s3"):
        retract = ease_in_out(clamp(lt / 1.5)) if sid == "s2" else 1.0
    if sid == "s4":
        extra = (lt * 0.25) % 1
    finger_close(c, W / 2, 1180, 0.95 + 0.02 * math.sin(t), t, retract, extra)
    if sid == "h":
        hc.big(c, "¿SIGUEN CRECIENDO?", W / 2, 1720, 90, V["accent"], lt, 0.2)
    if sid == "s1":
        hc.stamp(c, "MITO", W / 2, 1700, lt, 0.1, 160)
    if sid == "s2":
        K.tag(c, 780, 1050, "LA PIEL SE RETRAE", lt - 0.5, accent=V["accent"], size=34, line_to=(590, 1130))
    if sid == "s3":
        K.tag(c, W / 2, 1720, "SIN GLUCOSA NO HAY CRECIMIENTO", lt - 0.2, accent=V["accent"], size=34)
    if sid == "s4":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(3.5 * p, 1) + " mm", "AL MES (UÑAS DE LAS MANOS)", V["accent"], y=1690, size=120)
    if sid == "s5":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(1.0 * p, 1) + " cm", "PELO AL MES", V["accent"], y=1690, size=120)


V104 = dict(slug="104_unas_mito", accent=0xFFFFC27A, drone=0.02, scene=s_unas, segs=[
    dict(id="h", who="nar", say="¿Es verdad que el pelo y las uñas siguen creciendo después de morir?",
         cap="¿El pelo y las *uñas* | siguen creciendo | después de *morir*?"),
    dict(id="s1", who="nar", cut=True, say="Es un mito. Y muy extendido.", cap="Es un *MITO*"),
    dict(id="s2", who="nar", cut=True, say="Lo que pasa es que la piel se deshidrata y se retrae… y deja a la vista más uña y más pelo.",
         cap="La piel se *deshidrata* | y se *retrae*… | y se ve *más uña*"),
    dict(id="s3", who="nar", say="Para crecer hacen falta células que se dividan, y glucosa. Y eso se para.",
         cap="Para crecer hacen falta | células *vivas* y *glucosa*. | Y eso *se para*"),
    dict(id="s4", who="nar", cut=True, say="En vida, en cambio, las uñas de tus manos crecen unos tres milímetros y medio al mes.",
         cap="En vida, tus uñas | crecen unos | *3,5 mm al mes*"),
    dict(id="s5", who="nar", say="Y el pelo, alrededor de un centímetro al mes. Una uña entera tarda unos seis meses en renovarse.",
         cap="El pelo: | *1 cm al mes*. | Una uña entera: *6 meses*"),
    dict(id="cta", who="nar", cut=True, say="¿Qué mito te creías tú? Comenta, y sígueme: mañana desmonto otro.",
         cap="¿Qué *mito* te creías? | *COMENTA* | y *SÍGUEME*", hold=0.8),
])


# ====================================================================== 105 Mito: los toros y el rojo
def cloth(c, cx, cy, w, h, t, col, amp=1.0):
    """Capa/muleta ondeando: tiras con desplazamiento sinusoidal y sombreado por pendiente."""
    n = 40
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        def pt(u, v):
            wave = math.sin(u * 7 - t * 5.5) * 38 * amp * u + math.sin(u * 3 + v * 2 - t * 3) * 20 * amp
            return cx - w / 2 + u * w + wave * 0.3, cy + v * h + wave
        p = skia.Path()
        a = pt(u0, 0); p.moveTo(*a)
        for v in np.linspace(0, 1, 8):
            p.lineTo(*pt(u1, v))
        for v in np.linspace(1, 0, 8):
            p.lineTo(*pt(u0, v))
        p.close()
        slope = math.cos(u0 * 7 - t * 5.5)
        shade = 0.72 + 0.28 * slope
        r = ((col >> 16) & 255) * shade; g = ((col >> 8) & 255) * shade; b = (col & 255) * shade
        c.drawPath(p, fill(0xFF000000 | (int(r) << 16) | (int(g) << 8) | int(b)))
    # palo
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2 - 20, cy - 24, w + 60, 26), 13, 13), fill(0xFF6A4A2A))


def bull_vision(col, k):
    """Mezcla hacia la visión dicromática aproximada del toro (rojo -> pardo apagado)."""
    r, g, b = (col >> 16) & 255, (col >> 8) & 255, col & 255
    y = 0.45 * r + 0.45 * g + 0.1 * b
    tr, tg, tb = y * 0.82, y * 0.78, y * 0.55 + b * 0.3
    return 0xFF000000 | (int(lerp(r, tr, k)) << 16) | (int(lerp(g, tg, k)) << 8) | int(lerp(b, tb, k))


def s_toro(c, t, P, V):
    sid, lt = seg(P, t)
    vis = 0.0
    if sid in ("s1", "s2", "s4"):
        vis = ease_in_out(clamp(lt / 1.0)) if sid in ("s1", "s4") else 1.0
    sky_top = bull_vision(0xFF2A6ACF, vis); sky_bot = bull_vision(0xFFF2C28A, vis)
    g = skia.GradientShader.MakeLinear([(0, 0), (0, 1250)], [sky_top, sky_bot])
    c.drawRect(skia.Rect.MakeWH(W, 1250), skia.Paint(Shader=g))
    # graderío
    for k in range(6):
        c.drawRect(skia.Rect.MakeXYWH(0, 900 + k * 50, W, 50), fill(bull_vision([0xFF8A2A2A, 0xFFE8E0D0][k % 2], vis)))
    for i in range(0, W, 26):
        for k in range(6):
            col = bull_vision([0xFFFF4D6D, 0xFF4DA8FF, 0xFFFFE04D, 0xFF2A2A2A][(i // 26 + k) % 4], vis)
            c.drawCircle(i + 13 + (k % 2) * 13, 920 + k * 50 + math.sin(t * 3 + i + k) * 2, 9, fill(with_alpha(col, 0.8)))
    # barrera y arena
    c.drawRect(skia.Rect.MakeXYWH(0, 1200, W, 70), fill(bull_vision(0xFFB8221E, vis)))
    sand = skia.GradientShader.MakeLinear([(0, 1270), (0, H)], [bull_vision(0xFFE8B070, vis), bull_vision(0xFFC88A4A, vis)])
    c.drawRect(skia.Rect.MakeXYWH(0, 1270, W, H - 1270), skia.Paint(Shader=sand))
    swing = math.sin(t * 1.4) * 60
    if sid == "s2":
        # varias capas: roja, azul, blanca
        for k, col in enumerate((0xFFD0141E, 0xFF2A5ADF, 0xFFF2F2F2)):
            cloth(c, 190 + k * 350, 1330 + math.sin(t * 2 + k) * 20, 260, 330, t + k, bull_vision(col, 0.0 if lt < 1.2 else 1.0), 0.8)
            K.tag(c, 190 + k * 350, 1720, ["ROJA", "AZUL", "BLANCA"][k], lt - 0.3 * k, accent=[0xFFFF4D6D, 0xFF6FA8FF, WHITE][k], size=30)
    else:
        amp = 1.4 if sid in ("s3",) else 1.0
        cloth(c, W / 2 + swing, 1330, 560, 470, t, bull_vision(0xFFD0141E, vis), amp)
    # astas del toro en primer plano
    for side in (-1, 1):
        p = skia.Path()
        x0 = W / 2 + side * 160
        p.moveTo(x0, H + 20); p.cubicTo(x0 + side * 120, H - 220, x0 + side * 60, H - 360, x0 - side * 40, H - 420)
        p.cubicTo(x0 + side * 120, H - 330, x0 + side * 210, H - 200, x0 + side * 120, H + 20); p.close()
        c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeLinear([(x0, H - 420), (x0, H)], [0xFFF2E8D0, 0xFF6A5A40]), AntiAlias=True))
    if sid == "s1":
        K.tag(c, W / 2, 1210, "ASÍ LO VE EL TORO", lt - 0.6, accent=WHITE, size=40)
    if sid == "s4":
        K.tag(c, W / 2, 1210, "VISIÓN DE 2 COLORES", lt - 0.5, accent=WHITE, size=40)
    if sid == "s3":
        hc.stamp(c, "MOVIMIENTO", W / 2, 1110, lt, 0.2, 120, col=0xFFFF3B4A)
    if sid == "h":
        hc.big(c, "¿EL ROJO?", W / 2, 1120, 140, V["accent"], lt, 0.2)


V105 = dict(slug="105_toro_rojo", accent=0xFFFF4D6D, drone=0.02, scene=s_toro, tease=TEASE, segs=[
    dict(id="h", who="nar", say="¿Los toros embisten porque odian el color rojo?", cap="¿Los toros odian | el color *ROJO*?"),
    dict(id="s1", who="nar", cut=True, say="Pues casi ni lo distinguen. Tienen solo dos tipos de conos en los ojos, y el rojo lo ven apagado, como pardo.",
         cap="Casi *ni lo distinguen*: | solo 2 tipos de *conos*. | El rojo lo ven *apagado*"),
    dict(id="s2", who="nar", cut=True, say="En dos mil siete, el programa MythBusters lo probó con capas rojas, azules y blancas. El toro embistió a las tres con la misma rabia.",
         cap="En *2007*, *MythBusters* | probó rojo, azul y blanco: | embistió a las *TRES*"),
    dict(id="s3", who="nar", cut=True, say="Lo que le provoca es el movimiento. Una persona quieta vestida de rojo… y el toro ni la miró.",
         cap="Lo que le provoca: | el *MOVIMIENTO*. | Quieto y de rojo… *ni lo miró*"),
    dict(id="s4", who="nar", say="Su vista se parece a la de una persona daltónica al rojo y al verde. La capa podría ser de cualquier color.",
         cap="Ve como un *daltónico* | al rojo y al verde. | La capa podría ser de *cualquier color*"),
    dict(id="cta", who="nar", cut=True, say="¿Lo sabías? Comenta. Y sígueme, que mañana desmonto otro mito de animales.",
         cap="¿Lo *sabías*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 106 Voyager · Parte 2: el Disco de Oro
STARS = K.Stars(seed=106)


def golden_disc(c, x, y, R, t, tilt=1.0):
    c.save(); c.translate(x, y); c.scale(1, tilt)
    glow(c, 0, 0, R * 1.6, 0xFFFFC34D, 0.25)
    g = skia.GradientShader.MakeRadial((-R * 0.3, -R * 0.3), R * 1.5, [0xFFFFF0B0, 0xFFE8B23A, 0xFF8A5A10])
    c.drawCircle(0, 0, R, skia.Paint(Shader=g, AntiAlias=True))
    for k in range(34):  # surcos
        rr = R * (0.36 + 0.62 * k / 34)
        c.drawCircle(0, 0, rr, stroke(with_alpha(0xFF5A3A08, 0.18 + 0.1 * (k % 3 == 0)), 2))
    # brillo que gira
    sw = skia.GradientShader.MakeSweep(0, 0, [with_alpha(WHITE, 0), with_alpha(WHITE, 0.45), with_alpha(WHITE, 0),
                                              with_alpha(WHITE, 0), with_alpha(WHITE, 0.35), with_alpha(WHITE, 0)],
                                       [0, 0.08, 0.18, 0.5, 0.58, 0.68], skia.TileMode.kClamp, 0, 360, 0,
                                       skia.Matrix.RotateDeg(t * 40))
    c.drawCircle(0, 0, R, skia.Paint(Shader=sw, AntiAlias=True, BlendMode=skia.BlendMode.kPlus))
    c.drawCircle(0, 0, R * 0.32, fill(0xFFD8A23A))
    c.drawCircle(0, 0, R * 0.05, fill(0xFF3A2808))
    c.restore()


def cover(c, x, y, s, t, a):
    """Tapa del disco con diagramas grabados (reproducción, púlsar, hidrógeno)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    col = with_alpha(0xFFFFE8A0, a)
    c.drawCircle(0, 0, 260, fill(with_alpha(0xFF6A4A10, 0.9 * a)))
    c.drawCircle(0, 0, 260, stroke(col, 4))
    c.drawCircle(-120, -110, 70, stroke(col, 3)); c.drawLine(-120, -110, -60, -170, stroke(col, 3))
    for k in range(14):  # mapa de púlsares
        ang = k * 25.7
        L = 60 + (k * 37) % 70
        c.drawLine(-110, 120, -110 + math.cos(math.radians(ang)) * L, 120 + math.sin(math.radians(ang)) * L, stroke(col, 2))
    c.drawCircle(130, 140, 20, stroke(col, 3)); c.drawCircle(190, 140, 20, stroke(col, 3)); c.drawLine(150, 140, 170, 140, stroke(col, 3))
    for k in range(6):
        c.drawLine(60 + k * 22, -150, 60 + k * 22, -60 - (k % 3) * 18, stroke(col, 3))
    c.restore()


def s_voyager2(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF010208)
    STARS.draw(c, t, camx=t * 30, zoom=1.0, alpha=1.0)
    spin = t * 0.9
    if sid in ("h", "s1", "s2", "s3", "s4"):
        tilt = 0.55 + 0.45 * abs(math.cos(t * 0.35))
        golden_disc(c, W / 2, 1050, 330, t, tilt)
    if sid == "h":
        K.tag(c, W / 2, 1480, "DISCO DE ORO · 1977", lt - 0.5, accent=V["accent"], size=36)
    if sid == "s1":
        K.counter(c, t, lt - 0.2, lambda p: str(int(round(55 * p))), "IDIOMAS", V["accent"], y=1600)
    if sid == "s2":
        pill(c, W / 2, 1560, "«HOLA Y SALUDOS A TODOS»", 44, bg=WHITE, fg=INK, scale=ease_back(prog(lt, 0.3, 0.6)))
    if sid == "s3":
        # latido sobre el disco
        b = math.exp(-((t * 1.2) % 1 - 0.05) ** 2 / 0.003)
        glow(c, W / 2, 1050, 260 + 60 * b, 0xFFFF3B5A, 0.4 + 0.4 * b)
        K.tag(c, W / 2, 1520, "JOHNNY B. GOODE · CHUCK BERRY", lt - 0.3, accent=V["accent"], size=32)
        K.tag(c, W / 2, 1620, "UN LATIDO HUMANO", lt - 1.6, accent=0xFFFF7A8A, size=32)
    if sid == "s4":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(4468 * p) + " M", "DE AÑOS: SEMIVIDA DEL URANIO-238", V["accent"], y=1600, size=110)
    if sid in ("s5", "cta"):
        cover(c, W / 2, 1050, 1.25, t, ease_out(clamp(lt / 0.6)) if sid == "s5" else 1.0)


V106 = dict(slug="106_voyager_disco", accent=0xFFFFC34D, drone=0.03, scene=s_voyager2, badge="VOYAGER · PARTE 2", segs=[
    dict(id="h", who="nar", say="Te prometí contarte qué lleva la Voyager uno para los extraterrestres. Es un disco de oro.",
         cap="Lo prometido: | lo que lleva la *Voyager 1*… | un *DISCO DE ORO*"),
    dict(id="s1", who="nar", cut=True, say="Lo preparó un equipo dirigido por Carl Sagan en mil novecientos setenta y siete. Lleva saludos en cincuenta y cinco idiomas.",
         cap="Equipo de *Carl Sagan*, *1977*. | Saludos en | *55 idiomas*"),
    dict(id="s2", who="nar", cut=True, say="Incluido el español. Lo que se oye es: hola y saludos a todos.",
         cap="Incluido el *español*: | «Hola y saludos | a todos»"),
    dict(id="s3", who="nar", cut=True, say="También lleva música, desde Bach hasta Johnny B. Goode de Chuck Berry… y el latido de un corazón humano.",
         cap="Música: de *Bach* | a *Chuck Berry*… | y un *latido humano*"),
    dict(id="s4", who="nar", cut=True, say="En la tapa hay una pizca de uranio doscientos treinta y ocho. Funciona como un reloj: quien lo encuentre sabrá cuánto tiempo lleva viajando.",
         cap="En la tapa: *uranio-238*. | Es un *RELOJ* para saber | cuánto lleva viajando"),
    dict(id="s5", who="nar", say="Y unos dibujos que explican cómo reproducirlo… y dónde está la Tierra.",
         cap="Y dibujos que explican | cómo *reproducirlo*… | y dónde está la *Tierra*"),
    dict(id="cta", who="nar", cut=True, say="¿Qué canción habrías mandado tú? Comenta. Y sígueme, que esta serie sigue.",
         cap="¿Qué *canción* habrías mandado? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 107 La Luna se aleja · Parte 2
DAY = S.load("earth_atmos_2048.jpg")
NIGHT = S.load("earth_lights_2048.png")
SPEC = S.load("earth_specular_2048.jpg", "L")
CLOUDS = S.load("earth_clouds_1024.png", "A")
MOON = S.load("moon_1024.jpg")
SUN = S.load("sunmap.jpg")
LIGHT = (-0.55, 0.35, 0.75)
STARS2 = K.Stars(seed=107)


def earth(c, x, y, R, spin, lat0=0.4):
    img = S.render(2 * R, DAY, spin=spin, light=LIGHT, night=NIGHT, spec=SPEC, clouds=CLOUDS, lat0=lat0, gain=1.12)
    S.draw_planet(c, x, y, R, img); S.atmosphere(c, x, y, R)


def moon(c, x, y, R, spin=0.3, light=LIGHT, ambient=0.04):
    img = S.render(2 * R, MOON, spin=spin, light=light, ambient=ambient, gain=1.1)
    S.draw_planet(c, x, y, R, img)


def sun(c, x, y, R, t):
    glow(c, x, y, R * 2.4, 0xFFFFA030, 0.9)
    img = S.render(2 * R, SUN, spin=t * 0.05, emissive=True, gain=1.25, tint=(1.0, 0.82, 0.45), contrast=1.4, limb=0.5)
    S.draw_planet(c, x, y, R, img)


def s_luna2(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020308)
    STARS2.draw(c, t, camx=t * 10, alpha=0.9)
    if sid in ("h", "s1", "s2"):
        earth(c, 330, 1180, 250, t * (0.35 if sid == "s1" else 0.07))
        drift = ease_in_out(prog(t, 0.0, 14.0)) * 160
        moon(c, 800 + drift * 0.6, 640 - drift * 0.4, 110 - drift * 0.15, spin=0.2 + t * 0.01)
        if sid == "s1":
            K.counter(c, t, lt - 0.2, lambda p: K.fmt(1.8 * p, 1) + " ms", "MÁS LARGO CADA SIGLO", V["accent"], y=1620)
        if sid == "s2":
            K.counter(c, t, lt - 0.2, lambda p: f"{int(round(lerp(24, 18, p)))} h", "HACE 1.400 MILLONES DE AÑOS", V["accent"], y=1620)
    elif sid in ("s3", "s4"):
        # mareas: océano que sube y baja
        earth(c, W / 2, 1060, 300, t * 0.1)
        ph = math.sin(t * 1.6)
        c.drawOval(skia.Rect.MakeXYWH(W / 2 - 330 - 25 * ph, 1060 - 300 + 10, 660 + 50 * ph, 580), stroke(with_alpha(0xFF4DA8FF, 0.5), 10))
        moon(c, 930, 520, 60, spin=0.2)
        if sid == "s3":
            K.tag(c, W / 2, 1520, "MAREAS MÁS DÉBILES", lt - 0.3, accent=V["accent"], size=38)
        else:
            hc.big(c, "¿Y LOS ECLIPSES?", W / 2, 1560, 110, V["accent"], lt, 0.2)
    else:
        # eclipse: la Luna pasa por delante del Sol y ya no lo tapa entero
        p = clamp(lt / 3.0) if sid == "s5" else 1.0
        sun(c, W / 2, 1050, 260, t)
        mR = 230 if sid == "s5" else 230
        mx = lerp(W / 2 - 520, W / 2, ease_out(p))
        moon(c, mx, 1050, mR, spin=0.3, light=(0.6, 0.0, -0.8), ambient=0.0)
        c.drawCircle(mx, 1050, mR, fill(with_alpha(0xFF050508, 0.92)))
        if sid == "s5":
            K.counter(c, t, lt - 0.3, lambda q: K.fmt(600 * q) + " M", "DE AÑOS: ÚLTIMO ECLIPSE TOTAL", V["accent"], y=1600, size=110)
        if sid == "s6":
            K.tag(c, W / 2, 1450, "SOLO UN ANILLO DE FUEGO", lt - 0.3, accent=V["accent"], size=38)


V107 = dict(slug="107_luna_parte2", accent=0xFFBFD7FF, drone=0.03, scene=s_luna2, badge="LA LUNA · PARTE 2", segs=[
    dict(id="h", who="nar", say="La Luna se aleja de nosotros tres coma ocho centímetros cada año. ¿Y qué le pasa a la Tierra?",
         cap="La *Luna* se aleja | *3,8 cm* al año… | ¿qué le pasa a la *Tierra*?"),
    dict(id="s1", who="nar", cut=True, say="Primero: los días se alargan. Muy poco, menos de dos milésimas de segundo por siglo.",
         cap="Los días se *alargan*: | menos de *2 milésimas* | por siglo"),
    dict(id="s2", who="nar", cut=True, say="Pero en dos mil dieciocho, unos geólogos calcularon que hace mil cuatrocientos millones de años un día duraba poco más de dieciocho horas.",
         cap="En *2018* calcularon: | hace 1.400 millones de años, | un día duraba *18 horas*"),
    dict(id="s3", who="nar", cut=True, say="Segundo: con la Luna más lejos, las mareas serán cada vez más débiles.",
         cap="Mareas | cada vez | más *débiles*"),
    dict(id="s4", who="nar", say="Y tercero, lo más triste.", cap="Y lo más *triste*…"),
    dict(id="s5", who="nar", cut=True, say="Dentro de unos seiscientos millones de años, la Luna se verá demasiado pequeña para tapar el Sol entero.",
         cap="En unos *600 millones* de años, | será demasiado *pequeña* | para tapar el Sol"),
    dict(id="s6", who="nar", say="Se acabarán los eclipses totales. Solo quedará un anillo de fuego.",
         cap="Adiós a los *eclipses totales*. | Solo un *anillo de fuego*"),
    dict(id="cta", who="nar", cut=True, say="Tú y yo, por suerte, aún los veremos. ¿Has visto alguno? Comenta, y sígueme.",
         cap="¿Has visto un *eclipse*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 108 Phineas Gage · Parte 1
def skull(c, x, y, s, t, rod_p=0.0, crack=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    # cráneo de perfil (mirando a la izquierda), con sombreado de hueso
    p = skia.Path()
    p.moveTo(-210, 40); p.cubicTo(-260, -120, -170, -330, 30, -340)
    p.cubicTo(230, -345, 300, -160, 270, 20); p.cubicTo(255, 120, 200, 170, 140, 190)
    p.lineTo(120, 290); p.cubicTo(60, 330, -40, 330, -90, 300)
    p.lineTo(-120, 230); p.cubicTo(-170, 220, -200, 190, -190, 150); p.cubicTo(-230, 120, -230, 80, -210, 40); p.close()
    g = skia.GradientShader.MakeRadial((-40, -180), 520, [0xFFFFF8EA, 0xFFE8DCC0, 0xFFA89A7A])
    c.drawPath(p, skia.Paint(Shader=g, AntiAlias=True))
    c.drawPath(p, stroke(0xFF6A5A40, 5))
    # órbita, nariz, pómulo, dientes
    c.drawOval(skia.Rect.MakeXYWH(-175, -60, 110, 95), fill(0xFF2A2018))
    nz = skia.Path(); nz.moveTo(-205, 60); nz.lineTo(-165, 140); nz.lineTo(-205, 150); nz.close(); c.drawPath(nz, fill(0xFF2A2018))
    c.drawArc(skia.Rect.MakeXYWH(-120, 40, 200, 90), 180, 150, False, stroke(0xFF8A7A5A, 6))
    for k in range(6):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-120 + k * 28, 225, 24, 40), 6, 6), fill(0xFFF8F0E0))
    c.drawCircle(150, 60, 22, fill(0xFF3A3020))  # conducto auditivo
    # suturas
    q = skia.Path(); q.moveTo(-20, -338)
    for k in range(12):
        q.lineTo(-10 + k * 14 + (8 if k % 2 else -8), -330 + k * 22)
    c.drawPath(q, stroke(with_alpha(0xFF6A5A40, 0.6), 3))
    if crack > 0:
        glow(c, -40, -150, 220, 0xFFFF3B2A, 0.6 * crack)
    c.restore()
    # barra de hierro: entra bajo el pómulo izquierdo (-90, 90) y sale por la coronilla (20, -340)
    if rod_p > 0:
        ex, ey = -90, 90
        ox, oy = 20, -340
        dx, dy = ox - ex, oy - ey
        n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
        L = 1100  # largo visible de la barra (en px de cráneo)
        head = lerp(-500, 1400, rod_p)  # posición de la punta a lo largo del eje desde la entrada
        tail = head - L
        hx, hy = x + s * (ex + dx * head), y + s * (ey + dy * head)
        tx, ty = x + s * (ex + dx * tail), y + s * (ey + dy * tail)
        c.drawLine(tx, ty, hx, hy, stroke(0xFF1A1A20, 46 * s))
        c.drawLine(tx, ty, hx, hy, stroke(0xFF7A7A88, 32 * s))
        c.drawLine(tx - 8 * s, ty, hx - 8 * s, hy, stroke(with_alpha(WHITE, 0.45), 8 * s))
        glow(c, x + s * ex, y + s * ey, 90 * s, 0xFFFF3B2A, 0.5)


def s_gage(c, t, P, V):
    sid, lt = seg(P, t)
    # noche, vía de tren, farol
    g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF070A18, 0xFF1A1410])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    glow(c, 860 + math.sin(t * 7) * 6, 420, 420, 0xFFFF9A3A, 0.25 + 0.05 * math.sin(t * 11))
    for k in range(14):  # traviesas en perspectiva
        yy = 1500 + k * k * 4.2
        w = 300 + k * 60
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - w / 2, yy, w, 10 + k), fill(0xFF3A2A1A))
    c.drawLine(W / 2 - 120, 1500, W / 2 - 520, H, stroke(0xFF8A8A90, 8)); c.drawLine(W / 2 + 120, 1500, W / 2 + 520, H, stroke(0xFF8A8A90, 8))
    rod = 0.0
    if sid == "s2":
        rod = 0.62 * clamp((lt - 1.6) / 0.35) if lt > 1.6 else 0.0
    elif sid == "s3":
        rod = 0.62
    shake = 14 * math.exp(-max(0, lt) * 5) if sid == "s2" else 0
    sc = 1.05 if sid not in ("s1",) else 0.95
    skull(c, W / 2 + math.sin(t * 50) * shake, 1050, sc, t, rod, 1.0 if sid in ("s2", "s3") else 0.0)
    # chispas de la explosión
    if sid == "s2":
        r = random.Random(3)
        for k in range(60):
            a = r.uniform(0, 6.28); sp = r.uniform(300, 1200)
            d = lt * sp
            if d < 900:
                x = W / 2 - 80 + math.cos(a) * d; y = 1510 + math.sin(a) * d * 0.6
                c.drawCircle(x, y, 4, fill(with_alpha(0xFFFFC34D, 1 - d / 900)))
    if sid == "h":
        hc.big(c, "13 SEPT. 1848", W / 2, 1700, 110, V["accent"], lt, 0.2)
    if sid == "s1":
        K.tag(c, W / 2, 1700, "CAVENDISH, VERMONT (EE. UU.)", lt - 0.3, accent=V["accent"], size=34)
    if sid == "s3":
        K.tag(c, 820, 400, "1,1 m · 6 kg", lt - 0.4, accent=V["accent"], size=40)
    if sid == "s4":
        hc.stamp(c, "CONSCIENTE", W / 2, 1720, lt, 0.2, 120, col=0xFF2FD46B)
    if sid == "s5":
        hc.brain(c, W / 2, 1720, 0.45, t, 0.0)
    if sid == "s6":
        hc.big(c, "«YA NO ERA GAGE»", W / 2, 1720, 100, V["accent"], lt, 0.2)


V108 = dict(slug="108_phineas_gage_p1", accent=0xFFFF9A3A, drone=0.035, scene=s_gage, badge="HISTORIA REAL · PARTE 1", segs=[
    dict(id="h", who="nar", say="En mil ochocientos cuarenta y ocho, una barra de hierro le atravesó la cabeza a un hombre. Y sobrevivió.",
         cap="En *1848*, una barra de hierro | le *atravesó la cabeza*… | y *sobrevivió*"),
    dict(id="s1", who="nar", cut=True, say="Se llamaba Phineas Gage. Era capataz en las obras del ferrocarril, en Vermont, Estados Unidos.",
         cap="Se llamaba *Phineas Gage*. | Capataz del *ferrocarril* | en Vermont"),
    dict(id="s2", who="nar", cut=True, say="El trece de septiembre, estaba apretando pólvora en una roca… y saltó una chispa.",
         cap="Apretaba *pólvora* | en una roca… | y saltó una *CHISPA*"),
    dict(id="s3", who="nar", say="La barra, de más de un metro y seis kilos, le entró por debajo del pómulo y le salió por lo alto del cráneo. Cayó a veinticinco metros.",
         cap="Más de *1 metro* y *6 kilos*. | Entró bajo el pómulo… | y *salió por arriba*"),
    dict(id="s4", who="nar", cut=True, say="Y lo increíble: es posible que ni siquiera perdiera el conocimiento.", cap="Puede que ni | *perdiera el conocimiento*"),
    dict(id="s5", who="nar", cut=True, say="Su médico, John Harlow, lo curó. A las diez semanas volvió a casa.",
         cap="Su médico, *John Harlow*, | lo curó. A las *10 semanas* | volvió a casa"),
    dict(id="s6", who="nar", cut=True, say="Pero sus amigos dijeron algo escalofriante: ya no era Gage.", cap="Pero sus amigos dijeron: | *«ya no era Gage»*"),
    dict(id="cta", who="nar", cut=True, say="Lo que le pasó a su cabeza después… te lo cuento mañana. Sígueme para no perdértelo, y comenta si lo conocías.",
         cap="Lo que pasó *después*… | te lo cuento *MAÑANA*. | *SÍGUEME*"),
])


# ====================================================================== 109 Vesna Vulović: 10.160 m sin paracaídas
def cloud_layer(c, t, y, seed, speed, alpha, scale=1.0):
    r = random.Random(seed)
    for k in range(9):
        x = r.uniform(-100, W + 100)
        yy = (y + r.uniform(-200, 200) - t * speed) % (H + 600) - 300
        for j in range(6):
            rr = r.uniform(90, 190) * scale
            c.drawCircle(x + r.uniform(-160, 160) * scale, yy + r.uniform(-50, 50), rr, fill(with_alpha(0xFFF2F4FA, alpha * r.uniform(0.5, 0.9))))


def fuselage(c, x, y, ang, s):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    body = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-260, -70, 520, 140), 70, 70)
    g = skia.GradientShader.MakeLinear([(0, -70), (0, 70)], [0xFFF8F8FA, 0xFFC8CCD4, 0xFF6A707A])
    c.drawRRect(body, skia.Paint(Shader=g, AntiAlias=True))
    c.drawRect(skia.Rect.MakeXYWH(-260, -10, 520, 14), fill(0xFF1A3A8A))
    for k in range(8):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-200 + k * 52, -40, 26, 30), 10, 10), fill(0xFF1A2030))
    # borde roto
    p = skia.Path(); p.moveTo(250, -70)
    for k in range(8):
        p.lineTo(250 + (25 if k % 2 else -5), -70 + k * 20)
    p.lineTo(250, 70); p.lineTo(300, 70); p.lineTo(300, -70); p.close()
    c.drawPath(p, fill(0xFF0A1020))
    c.restore()


def s_vesna(c, t, P, V):
    sid, lt = seg(P, t)
    tl = P["tl"]
    f0 = tl["s1"][0]; f1 = tl["s3"][1]
    fall = clamp((t - f0) / (f1 - f0)) if t >= f0 else 0.0
    alt = 10160 * (1 - fall)
    k = 1 - alt / 10160
    from engine import lerp_color
    top = lerp_color(0xFF081640, 0xFF8AB4E8, k); bot = lerp_color(0xFF2A5AB0, 0xFFE8EEF6, k)
    g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [top, bot])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    sp = 900 if sid in ("s1", "s2", "s3") else 60
    cloud_layer(c, t, 400, 1, sp * 0.5, 0.35, 0.8)
    if sid in ("s4", "s5", "s6", "cta"):
        # ladera nevada con bosque
        c.drawRect(skia.Rect.MakeXYWH(0, 1350, W, H - 1350), fill(0xFFE8EEF4))
        r = random.Random(9)
        for j in range(40):
            x = r.uniform(0, W); y = r.uniform(1320, 1800); s = r.uniform(0.6, 1.3)
            p = skia.Path(); p.moveTo(x, y - 160 * s); p.lineTo(x - 55 * s, y); p.lineTo(x + 55 * s, y); p.close()
            c.drawPath(p, fill(0xFF1A3A2A)); c.drawPath(p, stroke(with_alpha(WHITE, 0.5), 3))
    else:
        fuselage(c, W / 2 + math.sin(t * 0.8) * 80, 1050 + math.sin(t * 1.3) * 40, t * 25, 1.2)
        cloud_layer(c, t, 1200, 2, sp, 0.6, 1.2)
    if sid in ("h", "s1", "s2", "s3"):
        K.counter(c, t, 9.0, lambda p: K.fmt(alt) + " m", "ALTITUD", V["accent"], y=1640)
    if sid == "s4":
        hc.big(c, "VIVA", W / 2, 1150, 200, 0xFF2FD46B, lt, 0.2)
    if sid == "s5":
        K.tag(c, W / 2, 1150, "RÉCORD GUINNESS", lt - 0.2, accent=V["accent"], size=48)
        K.tag(c, W / 2, 1260, "CAÍDA MÁS ALTA SIN PARACAÍDAS", lt - 0.5, accent=WHITE, size=32)


V109 = dict(slug="109_vesna_vulovic", accent=0xFF6FD6FF, drone=0.035, scene=s_vesna, tease=TEASE, segs=[
    dict(id="h", who="nar", say="Cayó desde más de diez kilómetros de altura, sin paracaídas… y sobrevivió.",
         cap="Cayó desde *10 km*… | *sin paracaídas*… | y *sobrevivió*"),
    dict(id="s1", who="nar", cut=True, say="Se llamaba Vesna Vulović, y era azafata de la aerolínea yugoslava JAT.",
         cap="*Vesna Vulović*, | azafata de la aerolínea | yugoslava *JAT*"),
    dict(id="s2", who="nar", cut=True, say="El veintiséis de enero de mil novecientos setenta y dos, su avión explotó en pleno vuelo sobre Checoslovaquia.",
         cap="*26 de enero de 1972*: | su avión *explotó* | en pleno vuelo"),
    dict(id="s3", who="nar", cut=True, say="Según el informe oficial, a diez mil ciento sesenta metros. Ella cayó atrapada dentro de un trozo del avión.",
         cap="A *10.160 metros*. | Cayó atrapada en un | *trozo del avión*"),
    dict(id="s4", who="nar", cut=True, say="Fue la única superviviente. Estuvo días en coma, con huesos rotos… pero vivió.",
         cap="*Única superviviente*. | Días en coma… | pero *VIVIÓ*"),
    dict(id="s5", who="nar", cut=True, say="Hoy sigue teniendo el récord Guinness de la caída más alta sobrevivida sin paracaídas.",
         cap="Sigue teniendo | el *récord Guinness* | de la caída más alta"),
    dict(id="cta", who="nar", cut=True, say="¿Tú habrías vuelto a subir a un avión? Comenta. Y sígueme para más historias reales.",
         cap="¿Habrías vuelto | a *volar*? | *COMENTA* y *SÍGUEME*"),
])


# ====================================================================== 110 Test del espejo (enmascaramiento sacádico)
def eye_front(c, x, y, R, gx, gy, blink, t):
    """Ojo frontal realista: piel, párpados, esclerótica, iris con estrías, pupila y brillos."""
    c.save(); c.translate(x, y)
    clip = skia.Path()
    op = 1 - blink
    clip.moveTo(-R * 1.5, 0); clip.cubicTo(-R * 0.7, -R * 1.25 * op, R * 0.7, -R * 1.25 * op, R * 1.5, 0)
    clip.cubicTo(R * 0.7, R * 0.95 * op, -R * 0.7, R * 0.95 * op, -R * 1.5, 0); clip.close()
    c.save(); c.clipPath(clip, doAntiAlias=True)
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeRadial((0, 0), R * 1.6, [0xFFFFFFFF, 0xFFF0E4E0, 0xFFC8A8A0])))
    ix, iy = gx * R * 0.55, gy * R * 0.3
    ir = R * 0.62
    g = skia.GradientShader.MakeRadial((ix, iy), ir, [0xFF2A5A3A, 0xFF5A8A5A, 0xFF7A9A5A, 0xFF1A2A1A], [0, 0.45, 0.8, 1])
    c.drawCircle(ix, iy, ir, skia.Paint(Shader=g, AntiAlias=True))
    for k in range(48):
        a = k * 7.5
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        c.drawLine(ix + ca * ir * 0.38, iy + sa * ir * 0.38, ix + ca * ir * 0.95, iy + sa * ir * 0.95, stroke(with_alpha(0xFFB8D8A0, 0.25), 2))
    c.drawCircle(ix, iy, ir * 0.36, fill(0xFF050505))
    c.drawCircle(ix - ir * 0.3, iy - ir * 0.32, ir * 0.14, fill(with_alpha(WHITE, 0.9)))
    c.drawCircle(ix + ir * 0.25, iy + ir * 0.2, ir * 0.06, fill(with_alpha(WHITE, 0.6)))
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, -R), (0, -R * 0.2)], [0x88000000, 0x00000000])))
    c.restore()
    # piel y pestañas
    c.drawPath(clip, stroke(0xFF4A2A20, 7))
    for k in range(14):
        u = k / 13
        px = lerp(-R * 1.2, R * 1.2, u); py = -math.sin(u * math.pi) * R * 0.95 * op
        c.drawLine(px, py, px + (u - 0.5) * 30, py - 34, stroke(0xFF1A1010, 4))
    c.drawArc(skia.Rect.MakeXYWH(-R * 1.4, -R * 1.6, R * 2.8, R * 1.2), 200, 140, False, stroke(with_alpha(0xFF8A5A48, 0.6), 6))
    c.restore()


def s_espejo(c, t, P, V):
    sid, lt = seg(P, t)
    g = skia.GradientShader.MakeRadial((W / 2, 1000), 900, [0xFFE8B898, 0xFFC8886A, 0xFF5A3020])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    # sacadas: el ojo salta de izquierda a derecha cada ~0,7 s
    period = 0.7
    ph = (t % period) / period
    k = int(t / period)
    target = -1 if k % 2 == 0 else 1
    jump = clamp((ph - 0.85) / 0.15)
    gx = target * (1 - 2 * ease_in_out(jump)) if jump > 0 else target
    blink = max(0, 1 - abs(((t + 1.3) % 4.5) - 0.12) / 0.12)
    for side in (-1, 1):
        eye_front(c, W / 2 + side * 255, 1000, 175, gx, 0.0, blink, t)
    if sid in ("s2", "s3") and jump > 0:
        c.drawPaint(fill(with_alpha(0xFF000000, 0.85 * math.sin(jump * math.pi))))  # el cerebro 'apaga' la vista
    if sid == "h":
        K.tag(c, W / 2, 1450, "OJO IZQUIERDO → OJO DERECHO", lt - 0.4, accent=V["accent"], size=36)
    if sid == "s1":
        hc.stamp(c, "NUNCA", W / 2, 1480, lt, 0.2, 150)
    if sid == "s3":
        K.counter(c, t, lt - 0.2, lambda p: str(int(round(3 * p))), "SALTOS POR SEGUNDO", V["accent"], y=1520)
    if sid == "s5":
        K.tag(c, W / 2, 1480, "GRÁBATE CON EL MÓVIL", lt - 0.2, accent=V["accent"], size=40)
    if sid == "s4":
        K.tag(c, W / 2, 1480, "ENMASCARAMIENTO SACÁDICO", lt - 0.2, accent=V["accent"], size=36)


V110 = dict(slug="110_espejo_ojos", accent=0xFF8AE0FF, drone=0.02, scene=s_espejo, tease="HAZLO HOY EN EL ESPEJO", segs=[
    dict(id="h", who="nar", say="Hoy, delante del espejo, haz esto: mira tu ojo izquierdo… y luego el derecho.",
         cap="En el espejo: | mira tu ojo *izquierdo*… | y luego el *derecho*"),
    dict(id="s1", who="nar", cut=True, say="Por mucho que lo intentes, nunca vas a ver tus ojos moverse. Pero alguien a tu lado, sí.",
         cap="*NUNCA* verás | tus ojos *moverse*. | Pero otra persona *sí*"),
    dict(id="s2", who="nar", cut=True, say="Cada vez que tus ojos saltan, tu cerebro apaga la vista durante una fracción de segundo.",
         cap="Cada vez que saltan, | tu cerebro *APAGA* | la vista"),
    dict(id="s3", who="nar", say="Y lo hacen unas tres veces por segundo. Todo el día.", cap="Unas *3 veces* | por segundo. | Todo el día"),
    dict(id="s4", who="nar", cut=True, say="Se llama enmascaramiento sacádico. Tu cerebro rellena esos huecos… y tú nunca te enteras.",
         cap="*Enmascaramiento sacádico*: | tu cerebro *rellena* los huecos… | y no te enteras"),
    dict(id="s5", who="nar", say="El truco para verlo: grábate con la cámara del móvil mientras lo haces. En el vídeo, sí verás cómo se mueven.",
         cap="El truco: *grábate* | con el móvil. | En el vídeo *SÍ* se mueven"),
    dict(id="cta", who="nar", cut=True, say="Pruébalo y cuéntame en comentarios. Sígueme, que mañana te enseño otro fallo de tu cerebro.",
         cap="*Pruébalo* y cuéntamelo. | *COMENTA* | y *SÍGUEME*"),
])

VIDEOS = [V101, V102, V103, V104, V105, V106, V107, V108, V109, V110]


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
