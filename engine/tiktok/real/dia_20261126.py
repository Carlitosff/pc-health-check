"""Producción 26/11/2026 (3401 y 3402, motor 2D; 3403 mito_pavo.py y 3404 serie_sinluna.py en 3D; sin ciudad: IGEV01 330 < 332).
  3401 PRUEBA EN DIRECTO: ¿HACIA DÓNDE VAN LAS RAYAS? (ilusión de apertura / poste de barbería, `apertura.py`). Rayas '\\' que se mueven
       SIEMPRE hacia la derecha, vistas por una ranura alta → se ven SUBIR; ventana ancha → van a la derecha; sin ventana, un punto pintado
       en una raya va a la derecha. Wallach 1935 (Psychologische Forschung 20: 325–380); Guilford 1929; Wikipedia 'Barberpole illusion':
       'A vertically elongated aperture makes vertical motion dominant whereas a horizontally elongated aperture makes horizontal motion dominant'.
       Assert: en una columna de la ranura el borde de una raya SUBE entre dos frames (medido en píxeles) y el movimiento real es solo horizontal.
  3402 RETO: LA ESCALERA. Del 1º al 3º = 30 s → 2 tramos → 15 s por tramo; del 1º al 6º = 5 tramos = 75 s (60 es la respuesta rápida)."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, apertura as AP
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


# ============================ 3401 rayas por la ranura
CX, CY = W / 2, 1110
SLOPE, VX = 1.0, 150.0
TALL, WIDE, OPEN = (190, 760), (940, 200), (960, 760)
BG = 0xFF2B2F3A


def _assert_aperture():
    assert AP.slit_dir(SLOPE, VX) == "ARRIBA"
    ys = []
    for t in (0.50, 0.54):
        surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(BG)
        AP.stripes(c, CX, CY, *TALL, t, vx=VX, slope=SLOPE)
        a = surf.makeImageSnapshot().toarray()[..., :3].astype(int)   # BGRA
        col = a[CY - 300:CY + 300, int(CX), :]
        red = (col[:, 2] > 200) & (col[:, 1] < 100)                    # raya roja
        edges = np.where(np.diff(red.astype(int)) == 1)[0]
        ys.append(edges[0])
    assert ys[1] < ys[0], ys     # el borde sube en pantalla
    assert abs((ys[0] - ys[1]) - VX * 0.04 * SLOPE) <= 2, ys


_assert_aperture()


def win_at(sid, lt, d):
    if sid in ("h", "s1"):
        return TALL
    if sid == "s2":
        k = ease_io((lt - 1.2) / 1.0)
        return (lerp(TALL[0], WIDE[0], k), lerp(TALL[1], WIDE[1], k))
    if sid == "s3":
        k = ease_io(lt / .8); k2 = ease_io((lt - (d - 1.2)) / 1.0)
        w = lerp(WIDE[0], OPEN[0], k); h = lerp(WIDE[1], OPEN[1], k)
        return (lerp(w, TALL[0], k2), lerp(h, TALL[1], k2))
    return TALL


def s_bar(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(BG))
    w, h = win_at(sid, lt, d)
    mk = (0, 0xFFFFC23A) if sid == "s3" and lt > .8 and lt < d - .6 else None
    AP.stripes(c, CX, CY, w, h, t, vx=VX, slope=SLOPE, marker=mk)
    if sid == "s1" and lt > 1.2:
        K.tag(c, W / 2, 1600, "MIRA SOLO LA RANURA", lt - 1.2, accent=GOLD, size=42)
    if sid == "s3" and lt > 1.4 and lt < d - .8:
        K.tag(c, W / 2, 1600, "EL PUNTO VA A LA DERECHA", lt - 1.4, accent=GREEN, size=42)
    if sid == "s4" and lt > 2.6:
        K.tag(c, W / 2, 1840, "HANS WALLACH · 1935", lt - 2.6, accent=WHITE, size=34)


V3401 = dict(slug="3401_rayas_ranura", accent=GOLD, drone=0.015, scene=s_bar, mood="misterio", music=0.04, clean=True, steady=True,
             send="ENVÍASELO Y QUE TE DIGA QUÉ VE", vote=("s2", ("ARRIBA", "DERECHA"), 1, 1740), dare=("s1", "PREGÚNTALE QUÉ VE", 1840),
             rehook=("s3", "MIRA ESTE PUNTO"), reveal=("s2", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Hacia dónde se mueven estas rayas? Contesta antes de que abra la ventana.",
         cap="¿Hacia dónde *SE MUEVEN*?", hold=0.6),
    dict(id="s1", who="nar", cut=True, say="Fíjate en la ranura: casi todo el mundo las ve subir, como en el poste de una barbería.",
         cap="¿Las ves *SUBIR*?", hold=0.6),
    dict(id="s2", who="nar", cut=True, say="Ahora abro la ventana a lo ancho, y de repente van hacia la derecha.",
         cap="¡Van a *LA DERECHA*!", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Mira el punto amarillo: las rayas siempre han ido hacia la derecha, solo cambia la ventana.",
         cap="Solo cambia *LA VENTANA*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Como no ve dónde acaban las rayas, tu cerebro elige el lado largo del hueco. Lo estudió Hans Wallach en mil novecientos treinta y cinco.",
         cap="Hans Wallach, *1935*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta qué viste al principio, arriba o derecha, y envíaselo a alguien para ver qué ve.",
         cap="¿Arriba o derecha? | *COMENTA*"),
])


# ============================ 3402 la escalera
F0, S0, F1 = 3, 30, 6
TR0, TR1 = F0 - 1, F1 - 1
PER = S0 / TR0
ANS = PER * TR1
assert (TR0, PER, TR1, ANS) == (2, 15, 5, 75) and S0 * F1 / F0 == 60
FL_Y0, FL_H, BX0, BX1 = 1540, 130, 150, 700      # suelo del 1º, altura de planta, paredes del edificio


def floor_y(n):            # suelo de la planta n (1..6)
    return FL_Y0 - (n - 1) * FL_H


def stair_pos(u):
    """u en tramos (0 = 1º, 5 = 6º): zigzag; tramo impar sube hacia la derecha, par hacia la izquierda."""
    i = min(int(u), 4); f = u - i
    y = floor_y(1 + i) - f * FL_H
    xa, xb = (BX0 + 80, BX1 - 80) if i % 2 == 0 else (BX1 - 80, BX0 + 80)
    return lerp(xa, xb, f), y


def climber(c, x, y, t, moving):
    """Personaje de bloques en 2D (no de palo): cuerpo, cabeza y casco con piernas que alternan."""
    b = math.sin(t * 14) * (1 if moving else 0)
    for s, k in ((-1, b), (1, -b)):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + s * 12 - 9, y - 40 + abs(k) * -6, 18, 40), 6, 6), fill(0xFF154F5C))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 26, y - 100, 52, 64), 12, 12), fill(0xFF1F7A8C))
    c.drawRect(skia.Rect.MakeXYWH(x - 26, y - 70, 52, 8), fill(0xFFFFE25A))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 22, y - 142, 44, 42), 10, 10), fill(0xFFD9A06A))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 28, y - 156, 56, 20), 8, 8), fill(0xFFFFC42E))
    c.drawCircle(x - 8, y - 122, 4, fill(INK)); c.drawCircle(x + 8, y - 122, 4, fill(INK))


def building(c, t, upto=None):
    c.drawRect(skia.Rect.MakeXYWH(BX0 - 30, floor_y(6) - FL_H - 20, BX1 - BX0 + 60, FL_Y0 - floor_y(6) + FL_H + 40), fill(0xFF2A2236))
    for n in range(1, 7):
        y = floor_y(n)
        hl = upto is not None and n <= upto
        c.drawRect(skia.Rect.MakeXYWH(BX0 - 30, y, BX1 - BX0 + 60, 16), fill(0xFF6A5A7A if not hl else 0xFF8A7A3A))
        draw_text(c, f"{n}º", BX0 - 90, y - 50, 54, GOLD if hl else WHITE, outline=6)
        for wx in (BX0 + 30, BX1 - 90):   # ventanas con luz que parpadea suave
            a = .55 + .45 * math.sin(t * 1.3 + n * 1.7 + wx)
            c.drawRect(skia.Rect.MakeXYWH(wx, y - 100, 60, 60), fill(with_alpha(0xFFFFD27A, .35 + .4 * a)))
    for i in range(5):    # tramos de escalera
        xa, ya = stair_pos(i); xb, yb = stair_pos(i + .999)
        for k in range(8):
            f = k / 8
            sx = lerp(xa, xb, f); sy = lerp(ya, yb, f)
            c.drawRect(skia.Rect.MakeXYWH(sx - 30, sy - 4, 60, 14), fill(0xFF9A8AAE))


def clock(c, x, y, secs, col=GOLD, r=86):
    c.drawCircle(x, y, r + 10, fill(0xEE000000)); c.drawCircle(x, y, r, stroke(col, 8))
    a = -math.pi / 2 + 2 * math.pi * (secs % 60) / 60
    c.drawLine(x, y, x + r * .78 * math.cos(a), y + r * .78 * math.sin(a), stroke(col, 9))
    draw_text(c, f"{int(round(secs))} s", x, y + r + 64, 52, col, outline=6)


def s_stairs(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)], [0xFF1E2440, 0xFF0E1020])))
    for i in range(30):    # estrellas que titilan
        x = (i * 173) % W; y = 60 + (i * 97) % 640
        c.drawCircle(x, y, 2 + math.sin(t * 2 + i), fill(with_alpha(WHITE, .5)))
    CXK = 885
    if sid in ("h", "s1", "s2"):
        u = (ease_io((lt % 4.0) / 3.0)) * TR0 if sid == "h" else TR0
        building(c, t, upto=3)
        x, y = stair_pos(u); climber(c, x, y, t, sid == "h")
        K.pill(c, W / 2, 1600, "1º → 3º = 30 SEGUNDOS", 52, bg=0xEE000000, fg=WHITE)
        if sid == "s1" and d - lt <= 5:
            n = max(0, int(math.ceil(d - lt)))
            hc.big(c, f"{n}", CXK, 820, 170, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
        elif sid != "s2":
            draw_text(c, "¿1º → 6º?", CXK, 820, 64, GOLD, outline=6)
        if sid == "s2":
            a = ease_out(clamp((lt - .3) / .4))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - 260, 760, 520, 150), 30, 30), fill(with_alpha(0xFF000000, .85 * a)))
            draw_text(c, "¿60 s?", W / 2, 865, int(84 * (.7 + .3 * a)), with_alpha(RED, a), outline=6)
            if lt > 1.6:
                K.tag(c, W / 2, 1840, "EL DOBLE DE PISOS → ¿EL DOBLE DE TIEMPO?", lt - 1.6, accent=WHITE, size=32)
    elif sid == "s3":                    # 2 tramos de 15 s
        u = clamp(lt / (d - .4)) * TR0
        building(c, t, upto=1 + int(u))
        x, y = stair_pos(u); climber(c, x, y, t, u < TR0)
        clock(c, CXK, 830, PER * u)
        K.pill(c, W / 2, 1600, f"TRAMO {min(TR0, int(u) + 1)} DE 2 · 15 s", 52, bg=0xEE000000, fg=GOLD)
    elif sid == "s4":                    # 5 tramos → 75 s
        u = clamp((lt - .2) / (d - 1.0)) * TR1
        done = u >= TR1 - 1e-6
        building(c, t, upto=1 + int(u))
        x, y = stair_pos(u); climber(c, x, y, t, not done)
        clock(c, CXK, 830, PER * u, col=GREEN if done else GOLD)
        K.pill(c, W / 2, 1600, "5 TRAMOS × 15 s" if done else f"TRAMO {min(TR1, int(u) + 1)} DE 5", 52, bg=0xEE000000, fg=GREEN if done else GOLD)
    else:
        building(c, t, upto=6)
        x, y = stair_pos(TR1); climber(c, x, y, t, False)
        clock(c, CXK, 830, ANS, col=GREEN)
        K.pill(c, W / 2, 1600, "75 SEGUNDOS, NO 60", 54, bg=0xEE000000, fg=GREEN)


V3402 = dict(slug="3402_escalera_sexto_piso", accent=GOLD, drone=0.02, scene=s_stairs, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1840),
             rehook=("s3", "ESPERA… CUENTA LOS TRAMOS"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Subir del primer piso al tercero te lleva treinta segundos. ¿Cuánto tardas en llegar al sexto?",
         cap="¿Cuánto tardas *AL 6º*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos para pensarlo, sin hacer trampa.",
         cap="*5 segundos*", hold=2.6),
    dict(id="s2", who="nar", cut=True, say="Lo que sale rápido es sesenta segundos, porque el sexto es el doble que el tercero.",
         cap="¿*60 segundos*?", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero del primero al tercero solo subes dos tramos de escalera, así que cada tramo te lleva quince segundos.",
         cap="2 tramos: | *15 s* cada uno", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y del primero al sexto subes cinco tramos. Esta cuenta dice que cinco tramos de quince segundos son setenta y cinco segundos.",
         cap="5 tramos: | *75 SEGUNDOS*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta qué habías dicho, y envíaselo a un amigo para ver si cae en la trampa de los sesenta.",
         cap="¿Qué dijiste tú? | *COMENTA*"),
])

VIDEOS = {"3401": V3401, "3402": V3402}


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
