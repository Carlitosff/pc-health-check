"""Lote diario 27/10/2026 (201–210). Motor v5 (GANCHO XL: frase del gancho +20% sobre banda oscura y frame 0 limpio,
portada fijada en Metricool con videoCoverMilliseconds). Mezcla según métricas del 26/10 (IA y debates fuera: 108-251 vistas):
3 tests de percepción, 2 mitos (prometidos), 1 cuerpo, 2 espacio con texturas reales (mediodía rinde), 1 números,
1 serie (Phineas Gage P2, prometida). Serie implícita nueva: Júpiter -> 'mañana, Europa'."""
import math, sys, random
import numpy as np
import skia
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


def gray(v):
    v = int(clamp(v / 255) * 255)
    return 0xFF000000 | (v << 16) | (v << 8) | v


# ====================================================================== 201 Tablero de Adelson
LIGHT_SQ, DARK_SQ, SHADOW = 205, 123, 0.6  # B (claro en sombra) = 205*0.6 = 123 = A (oscuro al sol)
A_SQ, B_SQ = (1, 2), (3, 3)  # A oscura al sol, B clara en sombra
CYL = (4.6, 2.6)
SHC = (3.2, 3.0)


def board_xy(i, j, cx=W / 2, cy=1120, s=118):
    """Rejilla isométrica: casilla (i, j) -> centro en pantalla."""
    x = cx + (i - j) * s * 0.92
    y = cy + (i + j - 5) * s * 0.52
    return x, y


def shade_at(i, j):
    if (i, j) == B_SQ:
        return SHADOW
    d = math.hypot(i - SHC[0], j - SHC[1])
    return lerp(SHADOW, 1.0, clamp((d - 0.9) / 1.2))


def s_adelson(c, t, P, V):
    sid, lt = seg(P, t)
    g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF2A3A4A, 0xFF0E141C])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    rev = 0.0
    if "s2" in P["tl"]:
        a2 = P["tl"]["s2"][0]
        rev = ease_in_out(clamp((t - a2 - 0.2) / 1.0))
        if sid in ("s4", "cta"):
            rev = 1 - ease_in_out(clamp((t - P["tl"]["s4"][0]) / 0.8))
    sway = math.sin(t * 0.6) * 10
    c.save(); c.translate(sway, 0)
    s = 118
    for i in range(6):
        for j in range(6):
            x, y = board_xy(i, j)
            base = LIGHT_SQ if (i + j) % 2 == 0 else DARK_SQ
            v = base * shade_at(i, j)
            keep = (i, j) in (A_SQ, B_SQ)
            col = gray(v)
            if not keep and rev > 0:
                col = K.with_alpha(col, 1 - 0.92 * rev)
            p = skia.Path()
            p.moveTo(x, y - s * 0.52); p.lineTo(x + s * 0.92, y); p.lineTo(x, y + s * 0.52); p.lineTo(x - s * 0.92, y); p.close()
            c.drawPath(p, fill(col))
    # borde del tablero
    if rev < 1:
        x0, y0 = board_xy(-0.5, -0.5); x1, y1 = board_xy(5.5, -0.5); x2, y2 = board_xy(5.5, 5.5); x3, y3 = board_xy(-0.5, 5.5)
        e = skia.Path(); e.moveTo(x3, y3); e.lineTo(x2, y2); e.lineTo(x2, y2 + 40); e.lineTo(x3, y3 + 40); e.close()
        c.drawPath(e, fill(with_alpha(0xFF3A2A1A, 1 - rev)))
        e2 = skia.Path(); e2.moveTo(x1, y1); e2.lineTo(x2, y2); e2.lineTo(x2, y2 + 40); e2.lineTo(x1, y1 + 40); e2.close()
        c.drawPath(e2, fill(with_alpha(0xFF2A1E12, 1 - rev)))
        # cilindro verde
        cx, cy = board_xy(*CYL)
        al = 1 - rev
        body = skia.Rect.MakeXYWH(cx - 95, cy - 330, 190, 330)
        gg = skia.GradientShader.MakeLinear([(cx - 95, 0), (cx + 95, 0)], [with_alpha(0xFF1E6A2A, al), with_alpha(0xFF5AD06A, al),
                                                                           with_alpha(0xFF2A8A3A, al), with_alpha(0xFF0E3A16, al)], [0, 0.35, 0.6, 1])
        c.drawRect(body, skia.Paint(Shader=gg, AntiAlias=True))
        c.drawOval(skia.Rect.MakeXYWH(cx - 95, cy - 30, 190, 60), skia.Paint(Shader=gg, AntiAlias=True))
        c.drawOval(skia.Rect.MakeXYWH(cx - 95, cy - 360, 190, 60), fill(with_alpha(0xFF7AE08A, al)))
    # puentes de prueba (mismo gris) que unen A y B
    xa, ya = board_xy(*A_SQ); xb, yb = board_xy(*B_SQ)
    if sid in ("s3",):
        k = ease_out(clamp(lt / 0.8))
        c.drawRect(skia.Rect.MakeLTRB(xa - 30, ya, xa + 30, ya + (1500 - ya) * k), fill(gray(DARK_SQ)))
        c.drawRect(skia.Rect.MakeLTRB(xb - 30, yb, xb + 30, yb + (1500 - yb) * k), fill(gray(DARK_SQ)))
        c.drawRect(skia.Rect.MakeLTRB(xa - 30, 1500 - 60 * k, xb + 30, 1500), fill(gray(DARK_SQ)))
    for lab, (x, y) in (("A", (xa, ya)), ("B", (xb, yb))):
        draw_text(c, lab, x, y + 26, 74, WHITE if lab == "A" else 0xFFFFE04D, outline=10)
    c.restore()
    if sid == "s2":
        hc.stamp(c, "MISMO GRIS", W / 2, 1640, lt, 0.9, 120, col=0xFF2FD46B)
    if sid == "s4":
        hc.big(c, "1995 · MIT", W / 2, 1660, 120, V["accent"], lt, 0.2)
    if sid in ("h", "q"):
        hc.timer(c, W / 2, 1650, 70, clamp(t / 4.5), str(max(0, 4 - int(t))), V["accent"])


V201 = dict(slug="201_tablero_adelson", accent=0xFFFFE04D, drone=0.02, scene=s_adelson, tease="EL 95% FALLA ESTO", segs=[
    dict(id="h", who="nar", say="¿Qué casilla es más oscura, la A o la B? Responde antes de que acabe el tiempo.",
         cap="¿Qué casilla es | más *OSCURA*: | la *A* o la *B*?", hold=0.6),
    dict(id="s1", who="nar", cut=True, say="Seguro que has dicho la A. Casi todo el mundo lo dice.",
         cap="Has dicho la *A*, ¿verdad? | Casi *todo el mundo*"),
    dict(id="s2", who="nar", cut=True, say="Ahora quito todo lo demás. Mira. Son exactamente del mismo color.",
         cap="Quito todo lo demás… | son *EXACTAMENTE* | del mismo gris"),
    dict(id="s3", who="nar", cut=True, say="Si las uno con una barra del mismo gris, ya no hay ninguna diferencia.",
         cap="Las uno con el | *mismo gris*… | y desaparece la diferencia"),
    dict(id="s4", who="nar", cut=True, say="Es la ilusión del tablero de Adelson. La creó Edward Adelson, del MIT, en mil novecientos noventa y cinco.",
         cap="Ilusión de *Adelson*: | Edward Adelson, del *MIT*, | en *1995*"),
    dict(id="s5", who="nar", say="Tu cerebro sabe que la B está en sombra, y la aclara por su cuenta. No ves la luz: ves lo que tu cerebro calcula.",
         cap="Tu cerebro sabe que B | está en *sombra*… | y la *ACLARA* solo"),
    dict(id="cta", who="nar", cut=True, say="Y aunque ya lo sabes, vuelve a mirarlo: sigue engañándote. Comenta si caíste, y sígueme para otra.",
         cap="Ahora que lo sabes… | ¿*caíste*? *COMENTA* | y *SÍGUEME*"),
])
V201["segs"][0]["hold"] = 0.9


# ====================================================================== 202 Müller-Lyer
def ml_line(c, cx, y, L, fin, out, t, col, alpha=1.0):
    """Línea con aletas: out=True -> >—< (parece más larga); False -> <—> (más corta)."""
    w = 16
    x0, x1 = cx - L / 2, cx + L / 2
    p = stroke(with_alpha(col, alpha), w)
    p.setStrokeCap(skia.Paint.kRound_Cap)
    c.drawLine(x0, y, x1, y, p)
    if fin <= 0:
        return
    a = math.radians(38 + 4 * math.sin(t * 2.5))
    fl = 110 * fin
    for x, sgn in ((x0, -1), (x1, 1)):
        d = sgn if not out else -sgn
        pf = stroke(with_alpha(col, alpha * fin), w)
        pf.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawLine(x, y, x + d * fl * math.cos(a), y - fl * math.sin(a), pf)
        c.drawLine(x, y, x + d * fl * math.cos(a), y + fl * math.sin(a), pf)


def s_muller(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF103A5A, 0xFF3A1050, seed=3)
    L = 560
    fin = 1.0
    guide = 0.0
    if sid in ("s2", "s3"):
        guide = ease_out(clamp(lt / 0.6)) if sid == "s2" else 1.0
    if sid == "s3":
        fin = 1 - ease_in_out(clamp((lt - 0.3) / 1.0))
    if sid == "s4":
        fin = ease_in_out(clamp(lt / 0.8))
    y1, y2 = 930, 1330
    ml_line(c, W / 2, y1, L, fin, False, t, 0xFFFF7A3A)  # >—< arriba (parece más larga)
    ml_line(c, W / 2, y2, L, fin, True, t, 0xFF3AC8FF)
    if guide > 0:
        for x in (W / 2 - L / 2, W / 2 + L / 2):
            pp = stroke(with_alpha(WHITE, 0.9 * guide), 5)
            pp.setPathEffect(skia.DashPathEffect.Make([22, 16], -t * 60))
            c.drawLine(x, y1 - 160, x, y1 - 160 + (y2 - y1 + 320) * guide, pp)
    if sid in ("h",):
        K.tag(c, W / 2, y1 - 150, "ARRIBA", lt - 0.2, accent=0xFFFF7A3A, size=36)
        K.tag(c, W / 2, y2 + 150, "ABAJO", lt - 0.35, accent=0xFF3AC8FF, size=36)
        hc.timer(c, W / 2, 1650, 70, clamp(t / 4.0), str(max(0, 3 - int(t))), V["accent"])
    if sid == "s2":
        hc.stamp(c, "IGUALES", W / 2, 1650, lt, 0.5, 130, col=0xFF2FD46B)
    if sid == "s4":
        hc.big(c, "1889", W / 2, 1650, 160, V["accent"], lt, 0.2)
    if sid == "s5":
        K.tag(c, W / 2, 1650, "ESQUINAS Y PAREDES", lt - 0.3, accent=V["accent"], size=40)


V202 = dict(slug="202_muller_lyer", accent=0xFF9AE66E, drone=0.02, scene=s_muller, tease="RESPONDE ANTES DE 3 SEG", segs=[
    dict(id="h", who="nar", say="¿Qué línea es más larga, la de arriba o la de abajo? Tres segundos.",
         cap="¿Qué línea es | más *LARGA*: | arriba o abajo?", hold=1.2),
    dict(id="s1", who="nar", cut=True, say="La de arriba parece bastante más larga, ¿verdad?", cap="La de arriba parece | *bastante más larga*…"),
    dict(id="s2", who="nar", cut=True, say="Pues mira estas guías. Miden exactamente lo mismo.", cap="Mira las guías: | miden *EXACTAMENTE* | lo mismo"),
    dict(id="s3", who="nar", say="Quito las flechas… y ahora lo ves.", cap="Quito las *flechas*… | y ahora *lo ves*"),
    dict(id="s4", who="nar", cut=True, say="Es la ilusión de Müller-Lyer. La publicó el psiquiatra alemán Franz Müller-Lyer en mil ochocientos ochenta y nueve.",
         cap="Ilusión de *Müller-Lyer*, | publicada en *1889* | por Franz Müller-Lyer"),
    dict(id="s5", who="nar", cut=True, say="Y lo más curioso: en los años sesenta se vio que a pueblos que vivían sin edificios con esquinas, como algunos cazadores del Kalahari, les engañaba mucho menos.",
         cap="En los años *60*: a pueblos | sin *esquinas* ni edificios | les engañaba *mucho menos*"),
    dict(id="s6", who="nar", say="Tu cerebro ha aprendido de las paredes y las esquinas a calcular distancias… y aquí se equivoca.",
         cap="Tu cerebro aprendió de las | *paredes y esquinas*… | y aquí se *equivoca*"),
    dict(id="cta", who="nar", cut=True, say="¿Caíste? Comenta arriba o abajo. Y sígueme, que mañana te traigo una todavía más fuerte.",
         cap="¿*Caíste*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 203 Encuentra la diferente (Treisman)
def letter_grid(c, t, target_pos, base, odd, lt, found=0.0, seed=0, col=WHITE):
    rows, cols = 9, 7
    x0, y0, dx, dy = 150, 760, 130, 120
    r = random.Random(seed)
    f = font(92)
    for i in range(rows):
        for j in range(cols):
            x = x0 + j * dx + r.uniform(-18, 18) + math.sin(t * 1.3 + i + j * 0.7) * 4
            y = y0 + i * dy + r.uniform(-14, 14) + math.cos(t * 1.1 + j + i * 0.5) * 4
            ch = odd if (i, j) == target_pos else base
            a = 1.0 - 0.75 * found * ((i, j) != target_pos)
            ww = text_w(ch, f)
            c.save(); c.translate(x, y); c.rotate(r.uniform(-12, 12))
            c.drawString(ch, -ww / 2, 32, f, fill(with_alpha(col, a)))
            c.restore()
            if (i, j) == target_pos and found > 0:
                rr = 75 + 10 * math.sin(t * 8)
                c.drawCircle(x, y, rr * ease_back(clamp(found), 2.4), stroke(0xFFFF3B4A, 12))


def s_buscar(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF1A3A6A, 0xFF4A1A4A, seed=9)
    tl = P["tl"]
    if sid in ("h", "g1", "s1"):
        found = clamp((t - tl["s1"][0]) / 0.4) if t >= tl["s1"][0] else 0.0
        letter_grid(c, t, (5, 4), "O", "Q", lt, found, seed=1)
        if sid in ("h", "g1"):
            hc.timer(c, W / 2, 1830, 60, clamp(t / tl["g1"][1]), str(min(9, int(t) + 1)), V["accent"])
    elif sid in ("s2", "g2", "s3"):
        found = clamp((t - tl["s3"][0]) / 0.4) if t >= tl["s3"][0] else 0.0
        letter_grid(c, t, (2, 1), "Q", "O", lt, found, seed=2)
        if sid in ("s2", "g2"):
            a = tl["s2"][0]
            hc.timer(c, W / 2, 1830, 60, clamp((t - a) / (tl["g2"][1] - a)), str(min(9, int(t - a) + 1)), V["accent"])
    else:
        hc.brain(c, W / 2, 1150, 1.2, t)
        if sid == "s4":
            hc.big(c, "1985", W / 2, 1600, 150, V["accent"], lt, 0.2)
        if sid == "s5":
            K.tag(c, W / 2 - 230, 1600, "Q: TIENE ALGO DE MÁS", lt - 0.2, accent=0xFF2FD46B, size=30)
            K.tag(c, W / 2 + 230, 1700, "O: LE FALTA ALGO", lt - 0.8, accent=0xFFFF3B4A, size=30)


V203 = dict(slug="203_encuentra_letra", accent=0xFF6FD6FF, drone=0.015, scene=s_buscar, tease="ENCUENTRA LA DIFERENTE", segs=[
    dict(id="h", who="nar", say="Encuentra la Q escondida entre las O. ¿En qué segundo la ves?", cap="Encuentra la *Q* | entre las *O*"),
    dict(id="g1", who="q", say="Rápido.", cap="*Rápido*…", hold=1.6),
    dict(id="s1", who="nar", cut=True, say="Aquí. Fácil, ¿no? Salta a la vista.", cap="Fácil, ¿no? | *Salta* a la vista"),
    dict(id="s2", who="nar", cut=True, say="Ahora al revés: busca la única O entre las Q.", cap="Ahora al *REVÉS*: | busca la *O* | entre las Q"),
    dict(id="g2", who="q", say="Venga, búscala.", cap="*Búscala*…", hold=3.2),
    dict(id="s3", who="nar", cut=True, say="Aquí estaba. Mucho más difícil, ¿verdad? Y son las mismas dos letras.",
         cap="Aquí estaba. | *Mucho más difícil*… | con las *mismas* letras"),
    dict(id="s4", who="nar", cut=True, say="Lo demostró la psicóloga Anne Treisman en mil novecientos ochenta y cinco. Se llama asimetría de búsqueda.",
         cap="Lo demostró *Anne Treisman* | en *1985*: | asimetría de búsqueda"),
    dict(id="s5", who="nar", say="A tu cerebro le salta a la vista lo que tiene algo de más, como el rabito de la Q. Pero lo que le falta algo, tiene que buscarlo una a una.",
         cap="Lo que tiene algo *DE MÁS* | salta a la vista. | Lo que le *FALTA*, no"),
    dict(id="cta", who="nar", cut=True, say="¿En qué segundo encontraste la O? Comenta tu número. Y sígueme para más retos.",
         cap="¿En qué *segundo* | encontraste la O? | *COMENTA* y *SÍGUEME*"),
])


# ====================================================================== 204 Eres más alto por la mañana
def vertebra(c, x, y, w, h, col=0xFFF2E6CC):
    g = skia.GradientShader.MakeLinear([(x - w / 2, 0), (x + w / 2, 0)], [0xFFB8A882, col, 0xFFFFFBF0, 0xFFA8986E], [0, 0.3, 0.55, 1])
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), h * 0.35, h * 0.35), skia.Paint(Shader=g, AntiAlias=True))
    # apófisis
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + w / 2 - 10, y - h * 0.18, 70, h * 0.36), 12, 12), fill(0xFFD8C8A2))


def disc(c, x, y, w, h, glowk=0.0):
    g = skia.GradientShader.MakeLinear([(0, y - h / 2), (0, y + h / 2)], [0xFF6AB8E8, 0xFFBFE6FF, 0xFF4A8AC0])
    c.drawOval(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), skia.Paint(Shader=g, AntiAlias=True))
    if glowk > 0:
        glow(c, x, y, w * 0.6, 0xFF6FD6FF, 0.4 * glowk)


def spine(c, x, ytop, n, vh, dh, t, glowk=0.0):
    y = ytop
    for k in range(n):
        vertebra(c, x, y + vh / 2, 230 - k * 2, vh)
        y += vh
        if k < n - 1:
            disc(c, x, y + dh / 2, 210, dh, glowk)
            y += dh
    return y


def ruler(c, x, y0, y1, t):
    c.drawRect(skia.Rect.MakeLTRB(x - 40, y0, x + 40, y1), fill(0xFFFFD43B))
    for k in range(int((y1 - y0) / 20) + 1):
        yy = y0 + k * 20
        L = 40 if k % 5 == 0 else 20
        c.drawLine(x - 40, yy, x - 40 + L, yy, stroke(INK, 4))


def s_altura(c, t, P, V):
    sid, lt = seg(P, t)
    tl = P["tl"]
    if sid in ("s4", "s5"):
        c.clear(0xFF020308)
        EARTH_STARS.draw(c, t, camx=t * 12, alpha=0.9)
        R = 520
        img = S.render(2 * R, DAY, spin=t * 0.04, light=(-0.5, 0.3, 0.8), night=NIGHT, clouds=CLOUDS, lat0=0.5, gain=1.1)
        S.draw_planet(c, W / 2, 2050, R * 1.6, img); S.atmosphere(c, W / 2, 2050, R * 1.6)
        dh = 26 + 12 * ease_in_out(clamp(lt / 2.0)) if sid == "s4" else 38
        spine(c, W / 2 - 60, 640, 7, 92, dh, t, 1.0)
        if sid == "s4":
            K.counter(c, t, lt - 0.3, lambda p: "+" + K.fmt(3 * p) + " %", "DE ALTURA EN EL ESPACIO", V["accent"], y=1500)
        else:
            hc.big(c, "+5 cm", W / 2, 1500, 170, V["accent"], lt, 0.2)
            K.tag(c, W / 2, 1650, "SCOTT KELLY · 2016", lt - 0.5, accent=WHITE, size=38)
        return
    hc.aurora(c, t, 0xFF0A3A5A, 0xFF1A1A4A, seed=4)
    # día: los discos se aplastan; noche: se recuperan
    if sid in ("h", "s1"):
        squash = 0.0
    elif sid == "s2":
        squash = ease_in_out(clamp(lt / 2.2))
    elif sid == "s3":
        squash = 1 - ease_in_out(clamp(lt / 2.2))
    else:
        squash = 0.0
    dh = lerp(34, 18, squash)
    yb = spine(c, W / 2 - 60, 700, 7, 92, dh, t, 1 - squash)
    ruler(c, W / 2 + 230, 700, 1560, t)
    c.drawLine(W / 2 - 220, yb, W / 2 + 280, yb, stroke(0xFFFF3B4A, 6))
    c.drawLine(W / 2 - 220, 700, W / 2 + 280, 700, stroke(with_alpha(WHITE, 0.6), 4))
    if sid == "h":
        hc.big(c, "+1 cm", W / 2, 1720, 150, V["accent"], lt, 0.3)
    if sid == "s2":
        K.tag(c, W / 2, 1720, "DE DÍA: LA GRAVEDAD APLASTA LOS DISCOS", lt - 0.3, accent=V["accent"], size=30)
    if sid == "s3":
        K.tag(c, W / 2, 1720, "DE NOCHE: SE VUELVEN A HINCHAR", lt - 0.3, accent=0xFF6FD6FF, size=32)


EARTH_STARS = K.Stars(seed=204)
DAY = S.load("earth_atmos_2048.jpg")
NIGHT = S.load("earth_lights_2048.png")
SPEC = S.load("earth_specular_2048.jpg", "L")
CLOUDS = S.load("earth_clouds_1024.png", "A")

V204 = dict(slug="204_mas_alto_manana", accent=0xFFFFD43B, drone=0.02, scene=s_altura, tease="MÍDETE MAÑANA", segs=[
    dict(id="h", who="nar", say="Ahora mismo eres más bajo que esta mañana. Casi un centímetro.",
         cap="Ahora eres *más bajo* | que esta mañana. | Casi *1 cm*"),
    dict(id="s1", who="nar", cut=True, say="Entre tus vértebras hay unos discos blanditos, llenos de agua, que hacen de amortiguador.",
         cap="Entre tus vértebras hay | *discos* llenos de agua | que *amortiguan*"),
    dict(id="s2", who="nar", cut=True, say="Durante el día, la gravedad y tu propio peso los van aplastando poco a poco.",
         cap="De día, la *gravedad* | y tu peso | los van *aplastando*"),
    dict(id="s3", who="nar", cut=True, say="Y por la noche, tumbado, se vuelven a hinchar. Por eso por la mañana eres más alto.",
         cap="De noche, tumbado, | se vuelven a *hinchar*. | Por la mañana: *más alto*"),
    dict(id="s4", who="nar", cut=True, say="En el espacio, sin gravedad, es todavía más exagerado: según la NASA, los astronautas crecen hasta un tres por ciento.",
         cap="En el espacio, según la *NASA*, | los astronautas crecen | hasta un *3%*"),
    dict(id="s5", who="nar", say="El astronauta Scott Kelly volvió en dos mil dieciséis de casi un año en el espacio cinco centímetros más alto. En unos días, lo perdió.",
         cap="*Scott Kelly* volvió en *2016* | *5 cm más alto*. | En unos días, lo *perdió*"),
    dict(id="cta", who="nar", cut=True, say="Mídete mañana al levantarte y por la noche, y comenta cuánto cambia. Sígueme para más cosas de tu cuerpo.",
         cap="Mídete mañana y | por la noche: *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 205 Mito: el avestruz no esconde la cabeza
def egg(c, x, y, rx, ry, t, col=(0xFFFFF8E8, 0xFFE8DCC0, 0xFFA8987A), rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawOval(skia.Rect.MakeXYWH(-rx * 1.05, ry * 0.7, rx * 2.1, ry * 0.5), fill(0x55000000))
    g = skia.GradientShader.MakeRadial((-rx * 0.35, -ry * 0.4), max(rx, ry) * 1.5, list(col))
    pth = skia.Path()
    pth.moveTo(0, -ry)
    pth.cubicTo(rx * 0.75, -ry, rx, -ry * 0.1, rx, ry * 0.25)
    pth.cubicTo(rx, ry * 0.8, rx * 0.5, ry, 0, ry)
    pth.cubicTo(-rx * 0.5, ry, -rx, ry * 0.8, -rx, ry * 0.25)
    pth.cubicTo(-rx, -ry * 0.1, -rx * 0.75, -ry, 0, -ry)
    c.drawPath(pth, skia.Paint(Shader=g, AntiAlias=True))
    r = random.Random(int(rx))
    for k in range(40):  # poros de la cáscara
        px, py = r.uniform(-rx * 0.7, rx * 0.7), r.uniform(-ry * 0.7, ry * 0.7)
        c.drawCircle(px, py, 1.6, fill(with_alpha(0xFF8A7A5A, 0.35)))
    c.restore()


def dunes(c, t, sunset=1.0):
    g = skia.GradientShader.MakeLinear([(0, 0), (0, 1300)], [0xFF2A3A7A, 0xFFE87A4A, 0xFFFFC27A], [0, 0.6, 1])
    c.drawRect(skia.Rect.MakeWH(W, 1300), skia.Paint(Shader=g))
    glow(c, 760, 980, 380, 0xFFFFB04D, 0.7)
    c.drawCircle(760, 980, 110, fill(0xFFFFE0A0))
    for k, (yb, cl, sp) in enumerate(((1050, 0xFFC8743A, 8), (1200, 0xFFD88A4A, 18), (1380, 0xFFE8A060, 30))):
        p = skia.Path(); p.moveTo(0, H)
        for x in range(0, W + 41, 40):
            p.lineTo(x, yb + math.sin((x + t * sp) / 230 + k * 2) * 60 + math.sin((x + t * sp) / 90 + k) * 14)
        p.lineTo(W, H); p.close()
        c.drawPath(p, fill(cl))


def s_avestruz(c, t, P, V):
    sid, lt = seg(P, t)
    dunes(c, t)
    if sid in ("h", "s1", "s2"):
        # nido excavado con huevos que se giran
        c.drawOval(skia.Rect.MakeXYWH(W / 2 - 420, 1380, 840, 260), fill(0xFFB8682E))
        c.drawOval(skia.Rect.MakeXYWH(W / 2 - 380, 1395, 760, 210), fill(0xFF8A4A1E))
        for k in range(5):
            rot = math.sin(t * 1.5 + k) * (14 if sid == "s2" else 4)
            egg(c, W / 2 - 260 + k * 130, 1490 + (k % 2) * 30, 70, 88, t, rot=rot)
        if sid == "s2":
            K.tag(c, W / 2, 1750, "GIRA LOS HUEVOS CON EL PICO", lt - 0.3, accent=V["accent"], size=36)
        if sid == "h":
            hc.stamp(c, "¿MITO?", W / 2, 1180, lt, 0.4, 130)
    elif sid == "s3":
        egg(c, W / 2 - 120, 1350, 230, 290, t)
        egg(c, W / 2 + 230, 1530, 62, 82, t, col=(0xFFFFF0E0, 0xFFE8C8A8, 0xFFA87A5A))
        K.counter(c, t, lt - 0.2, lambda p: "≈ " + str(int(round(24 * p))), "HUEVOS DE GALLINA", V["accent"], y=820)
    elif sid == "s4":
        K.counter(c, t, lt - 0.2, lambda p: str(int(round(70 * p))) + " km/h", "CORRIENDO", V["accent"], y=1350)
        for k in range(12):  # estelas de velocidad
            y = 1500 + k * 30
            x = (t * 2400 + k * 377) % (W + 600) - 300
            c.drawLine(x, y, x + 260, y, stroke(with_alpha(WHITE, 0.4), 6))
    elif sid == "s5":
        hc.big(c, "PLINIO EL VIEJO", W / 2, 1380, 110, V["accent"], lt, 0.2)
        K.tag(c, W / 2, 1520, "HACE CASI 2.000 AÑOS", lt - 0.5, accent=WHITE, size=40)
    else:
        egg(c, W / 2, 1420, 150, 190, t)


V205 = dict(slug="205_avestruz_mito", accent=0xFFFFB04D, drone=0.02, scene=s_avestruz, tease=TEASE, segs=[
    dict(id="h", who="nar", say="¿El avestruz mete la cabeza bajo tierra cuando tiene miedo? Es mentira.",
         cap="¿El avestruz mete | la *cabeza bajo tierra*? | Es *MENTIRA*"),
    dict(id="s1", who="nar", cut=True, say="Si lo hiciera, se ahogaría. Lo que pasa es que pone sus huevos en un agujero que excava en el suelo.",
         cap="Si lo hiciera, se *ahogaría*. | Pone sus huevos en un | *agujero* en el suelo"),
    dict(id="s2", who="nar", cut=True, say="Y varias veces al día baja la cabeza para darles la vuelta con el pico. De lejos, parece que la ha enterrado.",
         cap="Baja la cabeza para | *girar los huevos*. | De lejos parece *enterrada*"),
    dict(id="s3", who="nar", cut=True, say="Y menudos huevos: el más grande de cualquier ave viva. Uno equivale a unos veinticuatro de gallina.",
         cap="El huevo más grande | de cualquier ave: | ≈ *24 de gallina*"),
    dict(id="s4", who="nar", cut=True, say="¿Y cuando hay peligro? O se tumba pegada al suelo para camuflarse… o sale corriendo a unos setenta kilómetros por hora.",
         cap="Ante el peligro: se *tumba*… | o corre a | *70 km/h*"),
    dict(id="s5", who="nar", cut=True, say="El mito viene de muy atrás: ya lo escribió el romano Plinio el Viejo hace casi dos mil años.",
         cap="El mito lo escribió | *Plinio el Viejo* | hace casi *2.000 años*"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo creías? Comenta. Y sígueme, que mañana desmonto otro mito de animales.",
         cap="¿Te lo *creías*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 206 Mito: la Gran Muralla desde el espacio
STARS6 = K.Stars(seed=206)
CHINA_LON = 116.0  # Pekín ~116° E, 40° N


def earth_at(c, x, y, R, lon_center, lat0, night_only=False, t=0.0):
    spin = math.radians(lon_center)  # comprobado en preview: el centro visible = lon de spin
    light = (0.9, 0.2, -0.4) if night_only else (-0.45, 0.35, 0.8)
    img = S.render(2 * R, DAY, spin=spin, light=light, night=NIGHT, spec=None if night_only else SPEC,
                   clouds=None if night_only else CLOUDS, lat0=lat0, gain=1.1, ambient=0.02 if night_only else 0.06)
    S.draw_planet(c, x, y, R, img); S.atmosphere(c, x, y, R)


def s_muralla(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020308)
    STARS6.draw(c, t, camx=t * 8, alpha=0.9)
    if sid in ("h", "s1", "s2"):
        zoom = 1.0 + (0.5 * ease_in_out(clamp(lt / 3)) if sid == "s2" else 0)
        R = 430 * zoom
        earth_at(c, W / 2, 1150 + (R - 430) * 0.6, R, CHINA_LON - 20 + t * 1.2, math.radians(30), t=t)
        if sid == "h":
            hc.stamp(c, "¿SE VE?", W / 2, 1720, lt, 0.5, 120)
        if sid == "s1":
            hc.big(c, "15 OCT. 2003", W / 2, 1720, 110, V["accent"], lt, 0.2)
            K.tag(c, W / 2, 1840, "YANG LIWEI · SHENZHOU 5", lt - 0.4, accent=WHITE, size=34)
    elif sid == "s3":
        # escala: muralla de unos metros vs 400 km de altura
        g = skia.GradientShader.MakeLinear([(0, 700), (0, 1900)], [0xFF1A2A4A, 0xFF7A9A6A])
        c.drawRect(skia.Rect.MakeXYWH(0, 700, W, 1220), skia.Paint(Shader=g))
        p = skia.Path(); p.moveTo(-50, 1600)
        for x in range(-50, W + 60, 60):
            p.lineTo(x, 1600 + math.sin(x / 140 + 1) * 120 + math.sin(x / 50) * 18)
        c.drawPath(p, stroke(0xFFC8B89A, 4 + 2 * math.sin(t)))
        K.counter(c, t, lt - 0.2, lambda q: K.fmt(400 * q) + " km", "DE ALTURA", V["accent"], y=1050)
        K.tag(c, W / 2, 1780, "COMO VER UN PELO A 3 KM", lt - 1.2, accent=WHITE, size=40)
    else:
        earth_at(c, W / 2, 1150, 470, CHINA_LON - 5 + t * 0.8, math.radians(25), night_only=True, t=t)
        if sid == "s4":
            K.tag(c, W / 2, 1720, "LO QUE SÍ SE VE: LAS CIUDADES", lt - 0.3, accent=V["accent"], size=36)


V206 = dict(slug="206_muralla_espacio", accent=0xFF6FD6FF, drone=0.03, scene=s_muralla, tease=TEASE, segs=[
    dict(id="h", who="nar", say="¿La Gran Muralla China se ve desde el espacio? Te lo contaron mil veces. Es falso.",
         cap="¿La *Gran Muralla* se ve | desde el *espacio*? | Es *FALSO*"),
    dict(id="s1", who="nar", cut=True, say="El quince de octubre de dos mil tres, Yang Liwei se convirtió en el primer astronauta chino. Al volver le preguntaron por la muralla.",
         cap="*15 de octubre de 2003*: | Yang Liwei, primer astronauta *chino*. | Le preguntaron por la muralla"),
    dict(id="s2", who="nar", say="Y su respuesta decepcionó a todo el país: no la vio.", cap="Y respondió: | *«no la vi»*"),
    dict(id="s3", who="nar", cut=True, say="Tiene miles de kilómetros de largo, sí, pero solo unos metros de ancho. Desde cuatrocientos kilómetros, es como intentar ver un pelo a tres kilómetros.",
         cap="Miles de km de largo… | pero solo *unos metros* de ancho. | Como ver un *pelo a 3 km*"),
    dict(id="s4", who="nar", cut=True, say="Lo que sí se ve de noche, y muy bien, son las luces de las ciudades.",
         cap="Lo que *SÍ* se ve de noche: | las *luces* | de las ciudades"),
    dict(id="cta", who="nar", cut=True, say="¿Te lo creías? Comenta. Y sígueme, que mañana desmonto otro mito que te enseñaron en el colegio.",
         cap="¿Te lo *creías*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 207 Júpiter: 1.300 Tierras
JUP = S.load("jupitermap.jpg")
STARS7 = K.Stars(seed=207)


def s_jupiter(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020308)
    STARS7.draw(c, t, camx=t * 14, alpha=0.9)
    L = (-0.6, 0.25, 0.76)
    if sid in ("h", "s1", "s2"):
        zoom = 1.0 if sid != "h" else lerp(1.35, 1.0, ease_out(clamp(lt / 2.2)))
        R = 470 * zoom
        img = S.render(2 * R, JUP, spin=t * 0.35, light=L, gain=1.15, limb=0.35)
        S.draw_planet(c, W / 2, 1120, R, img)
        S.atmosphere(c, W / 2, 1120, R, color=0xFFFFD8A0, strength=0.5)
        er = 43
        eimg = S.render(2 * er, DAY, spin=t * 0.5, light=L, clouds=CLOUDS, gain=1.1)
        ex = W / 2 + 380 if sid != "s2" else lerp(W / 2 + 380, W / 2 + 120, ease_in_out(clamp(lt / 1.2)))
        S.draw_planet(c, ex, 1120 - 470 - 30, er, eimg)
        K.tag(c, ex, 1120 - 470 - 110, "TIERRA", lt - 0.3, accent=WHITE, size=28)
        if sid == "s1":
            K.counter(c, t, lt - 0.2, lambda p: K.fmt(1300 * p), "TIERRAS CABRÍAN DENTRO", V["accent"], y=1720)
        if sid == "s2":
            K.tag(c, W / 2, 1720, "GRAN MANCHA ROJA", lt - 0.4, accent=0xFFFF7A4A, size=40)
    elif sid == "s3":
        R = 470
        img = S.render(2 * R, JUP, spin=t * 2.4, light=L, gain=1.15, limb=0.35)
        S.draw_planet(c, W / 2, 1120, R, img)
        K.counter(c, t, lt - 0.2, lambda p: f"{int(round(10 * p))} h", "DURA UN DÍA", V["accent"], y=1720)
    else:
        R = 470
        img = S.render(2 * R, JUP, spin=t * 0.35, light=L, gain=1.15, limb=0.35)
        S.draw_planet(c, W / 2, 1120, R, img)
        # Europa: pequeña luna helada que asoma
        mr = 70
        mx = lerp(W + 100, W / 2 + 360, ease_out(clamp(lt / 1.4)))
        glow(c, mx, 560, 160, 0xFFBFE6FF, 0.35)
        mimg = S.render(2 * mr, S.load("moon_1024.jpg"), spin=0.3, light=L, gain=1.25, tint=None)
        S.draw_planet(c, mx, 560, mr, mimg)
        c.drawCircle(mx, 560, mr, fill(with_alpha(0xFFBFD8F0, 0.35)))
        if sid == "s4":
            K.tag(c, mx - 120, 680, "EUROPA", lt - 0.6, accent=0xFFBFE6FF, size=34)


V207 = dict(slug="207_jupiter_1300", accent=0xFFFFB86A, drone=0.035, scene=s_jupiter, tease=TEASE, segs=[
    dict(id="h", who="nar", say="Este punto de aquí es la Tierra. Y esto otro… es Júpiter.",
         cap="Ese puntito es la *Tierra*. | Y esto… | es *JÚPITER*"),
    dict(id="s1", who="nar", cut=True, say="Dentro de Júpiter cabrían unas mil trescientas Tierras.",
         cap="Dentro cabrían unas | *1.300 Tierras*"),
    dict(id="s2", who="nar", cut=True, say="Y esa mancha roja es una tormenta que se observa desde hace casi doscientos años… y es más ancha que la Tierra entera.",
         cap="Esa mancha es una *tormenta* | de casi *200 años*… | más *ancha que la Tierra*"),
    dict(id="s3", who="nar", cut=True, say="Y aun siendo tan gigante, gira rapidísimo. Un día en Júpiter dura menos de diez horas.",
         cap="Y gira rapidísimo: | un día dura | menos de *10 horas*"),
    dict(id="s4", who="nar", cut=True, say="Pero lo más increíble no es Júpiter. Es una de sus lunas, que podría esconder más agua que todos los océanos de la Tierra.",
         cap="Lo más increíble: | una de sus *lunas* podría | esconder *más agua que la Tierra*"),
    dict(id="cta", who="nar", cut=True, say="Qué hay debajo de su hielo… te lo cuento mañana. Sígueme para no perdértelo, y comenta qué planeta quieres ver.",
         cap="Lo que hay bajo su *hielo*… | te lo cuento *MAÑANA*. | *SÍGUEME*"),
])


# ====================================================================== 208 ISS: 16 amaneceres al día
STARS8 = K.Stars(seed=208)


def iss(c, x, y, s, ang):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-160, -6, 320, 12), fill(0xFFB8BCC8))
    for side in (-1, 1):
        for k in range(2):
            px = side * (60 + k * 55)
            g = skia.GradientShader.MakeLinear([(px - 22, -90), (px + 22, 90)], [0xFF2A3A8A, 0xFF6A7ADA, 0xFF1A2A6A])
            c.drawRect(skia.Rect.MakeXYWH(px - 22, -95, 44, 190), skia.Paint(Shader=g))
            for j in range(6):
                c.drawLine(px - 22, -95 + j * 32, px + 22, -95 + j * 32, stroke(0xFF101830, 2))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-30, -22, 60, 44), 12, 12), fill(0xFFE8ECF4))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-70, -14, 40, 28), 10, 10), fill(0xFFD8DCE4))
    c.restore()


def s_iss(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020308)
    STARS8.draw(c, t, camx=t * 40, alpha=0.9)
    R = 760
    # la Tierra gira rápido bajo la estación (se ve el terminador día/noche pasar)
    sp = 0.12 if sid not in ("s2", "s3") else 0.35
    img = S.render(2 * R, DAY, spin=-2.0 + t * sp, light=(-0.75, 0.2, 0.62), night=NIGHT, spec=SPEC, clouds=CLOUDS,
                   lat0=0.62, gain=1.12)
    S.draw_planet(c, W / 2, 2050, R, img); S.atmosphere(c, W / 2, 2050, R, strength=1.3)
    # amanecer en el limbo
    if sid in ("s2", "s3"):
        ph = (t * 0.9) % 1
        glow(c, W / 2 - 420 + ph * 840, 1300, 260, 0xFFFFC870, 0.6 * math.sin(ph * math.pi))
    ang = math.sin(t * 0.4) * 8
    iss(c, W / 2 + math.sin(t * 0.7) * 30, 900 + math.cos(t * 0.9) * 18, 1.6, ang)
    if sid == "h":
        K.tag(c, W / 2, 1150, "MADRID → BARCELONA ≈ 1 MIN", lt - 0.5, accent=V["accent"], size=36)
    if sid == "s1":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(28000 * p) + " km/h", "VELOCIDAD DE LA ISS", V["accent"], y=1250, size=110)
    if sid == "s2":
        K.counter(c, t, lt - 0.2, lambda p: f"{int(round(90 * p))} min", "UNA VUELTA A LA TIERRA", V["accent"], y=1250)
    if sid == "s3":
        K.counter(c, t, lt - 0.2, lambda p: str(int(round(16 * p))), "AMANECERES AL DÍA", V["accent"], y=1250)
    if sid == "s4":
        K.tag(c, W / 2, 1200, "HORARIO DE LONDRES (UTC)", lt - 0.3, accent=V["accent"], size=36)


V208 = dict(slug="208_iss_amaneceres", accent=0xFFFFC870, drone=0.03, scene=s_iss, tease=TEASE, segs=[
    dict(id="h", who="nar", say="Hay una nave que va de Madrid a Barcelona en poco más de un minuto. Y lleva gente dentro.",
         cap="Va de Madrid a Barcelona | en *1 minuto*… | y lleva *gente* dentro", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Es la Estación Espacial Internacional. Vuela a unos veintiocho mil kilómetros por hora.",
         cap="Es la *Estación Espacial*. | Vuela a unos | *28.000 km/h*"),
    dict(id="s2", who="nar", cut=True, say="A esa velocidad, da una vuelta completa a la Tierra cada noventa minutos.",
         cap="Da la vuelta | a la Tierra cada | *90 minutos*", hold=0.5),
    dict(id="s3", who="nar", cut=True, say="Así que los astronautas ven unos dieciséis amaneceres… y dieciséis atardeceres al día.",
         cap="Ven unos | *16 amaneceres* | al día", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="¿Y cómo saben cuándo dormir? Siguen el horario de Londres, el UTC, y duermen unas ocho horas con un saco atado a la pared.",
         cap="¿Cuándo duermen? | Con el horario de *Londres*… | en un saco *atado a la pared*"),
    dict(id="cta", who="nar", cut=True, say="¿Tú aguantarías seis meses ahí arriba? Comenta. Y sígueme para más espacio.",
         cap="¿Aguantarías *6 meses*? | *COMENTA* | y *SÍGUEME*"),
])


# ====================================================================== 209 Cubo de Rubik
RUB = [0xFFFFFFFF, 0xFFFFD500, 0xFFFF5800, 0xFFC41E3A, 0xFF0051BA, 0xFF009E60]


def rubik(c, x, y, s, t, scramble=True, solved_k=0.0, seed=0):
    """Cubo isométrico con pegatinas; scramble cambia los colores a ritmo de giros."""
    step = int(t * 7) if scramble else 0
    r = random.Random(seed * 1000 + step)
    faces = []
    # top, left, right
    for fi, (ox, oy, ux, uy, vx, vy, shade) in enumerate((
            (0, -1, 0.866, 0.5, -0.866, 0.5, 1.0),
            (-0.866, -0.5, 0.866, 0.5, 0, 1, 0.78),
            (0, 0, 0.866, -0.5, 0, 1, 0.62))):
        faces.append((fi, ox, oy, ux, uy, vx, vy, shade))
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(math.sin(t * 0.5) * 6)
    for fi, ox, oy, ux, uy, vx, vy, shade in faces:
        for i in range(3):
            for j in range(3):
                if solved_k > 0.5:
                    col = RUB[fi]
                else:
                    col = RUB[r.randrange(6)]
                rr = ((col >> 16) & 255) * shade; gg = ((col >> 8) & 255) * shade; bb = (col & 255) * shade
                colx = 0xFF000000 | (int(rr) << 16) | (int(gg) << 8) | int(bb)
                p = skia.Path()
                def pt(a, b):
                    return (ox + ux * a + vx * b) * 100, (oy + uy * a + vy * b) * 100
                m = 0.07
                q = [pt(i / 3 + m / 3, j / 3 + m / 3), pt((i + 1) / 3 - m / 3, j / 3 + m / 3),
                     pt((i + 1) / 3 - m / 3, (j + 1) / 3 - m / 3), pt(i / 3 + m / 3, (j + 1) / 3 - m / 3)]
                bg = [pt(i / 3, j / 3), pt((i + 1) / 3, j / 3), pt((i + 1) / 3, (j + 1) / 3), pt(i / 3, (j + 1) / 3)]
                pb = skia.Path(); pb.addPoly([skia.Point(*a) for a in bg], True)
                c.drawPath(pb, fill(0xFF0A0A0E))
                p.addPoly([skia.Point(*a) for a in q], True)
                c.drawPath(p, fill(colx))
    c.restore()


def s_rubik(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF3A1A5A, 0xFF0A3A4A, seed=5)
    solved = 1.0 if sid in ("s4",) and lt > 1.2 else 0.0
    sc = 3.3 + 0.1 * math.sin(t * 1.3)
    rubik(c, W / 2, 1180, sc, t, scramble=(solved == 0), solved_k=solved, seed=209)
    if sid == "h":
        hc.big(c, "43 TRILLONES", W / 2, 1650, 120, V["accent"], lt, 0.3)
    if sid == "s1":
        pill(c, W / 2, 1650, "43.252.003.274.489.856.000", 52, bg=WHITE, fg=INK, scale=ease_back(prog(lt, 0.2, 0.5)))
    if sid == "s2":
        K.counter(c, t, lt - 0.2, lambda p: K.fmt(1.37 * p, 2), "BILLONES DE AÑOS", V["accent"], y=1650)
    if sid == "s3":
        K.counter(c, t, lt - 0.2, lambda p: "×" + str(int(round(100 * p))), "LA EDAD DEL UNIVERSO", V["accent"], y=1650)
    if sid == "s4":
        K.counter(c, t, lt - 0.2, lambda p: str(int(round(20 * p))), "MOVIMIENTOS COMO MÁXIMO", V["accent"], y=1650)
    if sid == "s5":
        hc.big(c, "2010", W / 2, 1650, 150, V["accent"], lt, 0.2)


V209 = dict(slug="209_rubik_combinaciones", accent=0xFFFFD500, drone=0.02, scene=s_rubik, tease=TEASE, segs=[
    dict(id="h", who="nar", say="Si giraras un cubo de Rubik una vez por segundo, ¿cuándo pasarías por todas sus combinaciones?",
         cap="Si giras un *Rubik* | una vez por segundo… | ¿cuándo las ves *TODAS*?"),
    dict(id="s1", who="nar", cut=True, say="Tiene cuarenta y tres trillones de combinaciones posibles. Un cuatro y un tres seguidos de dieciocho ceros.",
         cap="Tiene *43 trillones* | de combinaciones: | un 43 y *18 ceros*"),
    dict(id="s2", who="nar", cut=True, say="A una por segundo, sin parar, tardarías un billón trescientos mil millones de años.",
         cap="A una por segundo: | *1,3 billones* | de años"),
    dict(id="s3", who="nar", cut=True, say="Unas cien veces la edad del universo.", cap="Unas *100 veces* | la edad del universo"),
    dict(id="s4", who="nar", cut=True, say="Y aun así, cualquier cubo, por muy revuelto que esté, se puede resolver en veinte movimientos o menos.",
         cap="Y cualquier cubo | se resuelve en | *20 movimientos* o menos"),
    dict(id="s5", who="nar", say="Se demostró en dos mil diez, con superordenadores de Google. Lo llaman el número de Dios.",
         cap="Se demostró en *2010* | con ordenadores de *Google*: | el *número de Dios*"),
    dict(id="cta", who="nar", cut=True, say="¿Tú sabes resolverlo? Comenta tu tiempo. Y sígueme para más números que rompen la cabeza.",
         cap="¿Sabes *resolverlo*? | *COMENTA* tu tiempo | y *SÍGUEME*"),
])


# ====================================================================== 210 Phineas Gage · Parte 2
import dia_20261026 as D26


def s_gage2(c, t, P, V):
    sid, lt = seg(P, t)
    g = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [0xFF0A0C18, 0xFF1A1410])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    glow(c, 860 + math.sin(t * 7) * 6, 420, 420, 0xFFFF9A3A, 0.22 + 0.05 * math.sin(t * 11))
    if sid in ("h", "s1", "s5"):
        D26.skull(c, W / 2 + math.sin(t * 0.8) * 15, 1050, 1.05, t, 0.62 if sid != "s5" else 0.0, 1.0 if sid == "h" else 0.0)
        if sid == "s1":
            K.tag(c, W / 2, 1720, "JOHN HARLOW · 1868", lt - 0.3, accent=V["accent"], size=36)
        if sid == "s5":
            K.tag(c, W / 2, 1650, "MUSEO WARREN · HARVARD", lt - 0.3, accent=V["accent"], size=36)
            K.tag(c, W / 2, 1760, "CRÁNEO + BARRA DE HIERRO", lt - 0.6, accent=WHITE, size=32)
    elif sid == "s2":
        hc.brain(c, W / 2, 1100, 1.3, t)
        glow(c, W / 2 - 170, 1000, 230, 0xFFFF3B2A, 0.6 + 0.2 * math.sin(t * 6))
        for k, w in enumerate(("IMPACIENTE", "MALHABLADO", "TERCO")):
            K.tag(c, W / 2, 1520 + k * 100, w, lt - 0.4 - 0.4 * k, accent=[0xFFFF7A4A, 0xFFFF4D6D, 0xFFFFC34D][k], size=40)
    elif sid == "s3":
        # diligencia en los Andes: montañas y camino
        sky = skia.GradientShader.MakeLinear([(0, 600), (0, 1500)], [0xFF3A5A9A, 0xFFE8B88A])
        c.drawRect(skia.Rect.MakeXYWH(0, 600, W, 900), skia.Paint(Shader=sky))
        for k, (yb, cl) in enumerate(((1200, 0xFF5A6A8A), (1320, 0xFF3A4A5A))):
            p = skia.Path(); p.moveTo(0, 1500)
            for x in range(0, W + 61, 60):
                p.lineTo(x, yb - abs(math.sin(x / 170 + k * 2)) * 260 - math.sin(x / 60) * 20)
            p.lineTo(W, 1500); p.close(); c.drawPath(p, fill(cl))
            # nieve en las cumbres
        c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, 500), fill(0xFF8A6A4A))
        # ruedas de diligencia girando
        for wx in (W / 2 - 170, W / 2 + 170):
            c.drawCircle(wx, 1560, 95, stroke(0xFF3A2410, 16))
            for k in range(10):
                a = t * 4 + k * math.pi / 5
                c.drawLine(wx, 1560, wx + math.cos(a) * 90, 1560 + math.sin(a) * 90, stroke(0xFF5A3A1A, 8))
        hc.big(c, "CHILE", W / 2, 1800, 130, V["accent"], lt, 0.2)
    elif sid == "s4":
        hc.big(c, "21 MAYO 1860", W / 2, 1100, 120, V["accent"], lt, 0.2)
        K.tag(c, W / 2, 1260, "SAN FRANCISCO · 36 AÑOS", lt - 0.5, accent=WHITE, size=38)
    else:
        hc.brain(c, W / 2, 1100, 1.3, t)
        glow(c, W / 2 - 170, 1000, 260, 0xFF6FD6FF, 0.5 + 0.2 * math.sin(t * 4))
        K.tag(c, W / 2, 1560, "LÓBULO FRONTAL", lt - 0.3, accent=0xFF6FD6FF, size=44)


V210 = dict(slug="210_phineas_gage_p2", accent=0xFFFF9A3A, drone=0.035, scene=s_gage2, badge="HISTORIA REAL · PARTE 2", segs=[
    dict(id="h", who="nar", say="Te prometí contarte qué le pasó a Phineas Gage, el hombre al que una barra de hierro le atravesó la cabeza.",
         cap="Lo prometido: qué le pasó | a *Phineas Gage* | después de la barra"),
    dict(id="s1", who="nar", cut=True, say="Sobrevivió, sí. Pero en mil ochocientos sesenta y ocho, su médico John Harlow escribió que había cambiado por completo.",
         cap="Sobrevivió… pero su médico | *John Harlow* escribió | que había *CAMBIADO*"),
    dict(id="s2", who="nar", cut=True, say="Antes era un capataz responsable. Después se volvió impaciente, malhablado y terco.",
         cap="Antes: *responsable*. | Después: impaciente, | malhablado y *terco*"),
    dict(id="s3", who="nar", cut=True, say="Y aun así, años después se fue a Chile, y trabajó como conductor de diligencias en las carreteras de montaña.",
         cap="Y aun así, se fue a *Chile* | a conducir *diligencias* | por la montaña"),
    dict(id="s4", who="nar", cut=True, say="Murió en mil ochocientos sesenta, en San Francisco, por ataques epilépticos. Tenía treinta y seis años.",
         cap="Murió en *1860*, | en San Francisco, | con *36 años*"),
    dict(id="s5", who="nar", cut=True, say="Su cráneo y la barra se conservan hoy en el museo Warren de la Universidad de Harvard.",
         cap="Su *cráneo* y la *barra* | siguen hoy en | *Harvard*"),
    dict(id="s6", who="nar", cut=True, say="Fue una de las primeras pistas de que el lóbulo frontal tiene que ver con quién eres.",
         cap="Fue una de las primeras pistas: | el *lóbulo frontal* | tiene que ver con *quién eres*"),
    dict(id="cta", who="nar", cut=True, say="¿Quieres otra historia real así? Comenta otra. Y sígueme para no perdértela.",
         cap="¿Otra historia así? | Comenta *«OTRA»* | y *SÍGUEME*"),
])

VIDEOS = [V201, V202, V203, V204, V205, V206, V207, V208, V209, V210]


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
