"""Producción 12/11/2026 (2001 y 2002, motor 2D; 2003 mito_aranas.py y 2004 serie_cerca.py en 3D). Sin ciudad: IGEV01 313 = último N publicado (313).
  2001 PRUEBA EN DIRECTO: el sonido que sube sin fin (glissando de Shepard–Risset; Roger N. Shepard, 'Circularity in judgements of relative pitch',
       JASA 36(12), dic-1964; versión continua de Jean-Claude Risset, JASA 46, 1969; Wikipedia 'Pitch circularity'). Sonido generado por código
       (ilusion_audio.py, motor v23): la hélice y las barras enseñan las mismas componentes que suenan.
  2002 RETO: balancín. Izquierda: 4 bloques a 1 paso + 1 a 2 pasos = 6; derecha: 2 bloques a 4 pasos = 8 → cae a la DERECHA aunque tenga menos
       bloques (ley de la palanca, Arquímedes). Assert abajo."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, ilusion_audio as IA
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80; PINK = 0xFFFF5FA8


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 2001 el sonido que sube sin fin
RATE = 1 / 7.0
HUE = [0xFF4DE3FF, 0xFF7A8CFF, 0xFFB46CFF, 0xFFFF5FA8, 0xFFFF8A4A, 0xFFFFC23A, 0xFF8AF05A, 0xFF4ADE80]


def helix(c, t, cx, cy, hgt, rad, alpha=1.0):
    """hélice de notas que sube sin fin: cada vuelta = una octava; el brillo sigue la misma campana que el sonido."""
    pos, amp = IA.layers(t, rate=RATE)
    turns = 8
    pts = []
    for i in range(240):
        u = i / 240.0
        uu = (u + (RATE * t) % 1.0 / turns) % 1.0      # sube con el sonido
        th = uu * turns * 2 * math.pi + t * 0.6
        x = cx + math.cos(th) * rad
        y = cy + hgt / 2 - uu * hgt
        z = math.sin(th)
        a = float(IA._amp(np.array([uu]))[0])
        pts.append((z, x, y, a, uu))
    pts.sort()
    for z, x, y, a, uu in pts:
        r = 9 + 7 * (z + 1)
        col = HUE[int(uu * 8) % 8]
        c.drawCircle(x, y, r, fill(with_alpha(col, alpha * (0.12 + 0.88 * a) * (0.45 + 0.55 * (z + 1) / 2))))
        if a > .6 and z > .3:
            K.glow(c, x, y, r * 3, col, .25 * alpha * a)


def bars(c, t, x0, y0, w, h):
    """eje de frecuencias (grave abajo, agudo arriba): las 8 notas que suenan a la vez, con su volumen."""
    pos, amp = IA.layers(t, rate=RATE)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y0, w, h), 30, 30), fill(with_alpha(0xFF000000, .45)))
    for k in range(9):
        yy = y0 + h - k * h / 8
        c.drawLine(x0 + 30, yy, x0 + w - 30, yy, stroke(with_alpha(WHITE, .08), 2))
    for p, a in zip(pos, amp):
        yy = y0 + h - p * h
        ww = 60 + (w - 200) * a
        col = HUE[int(p * 8) % 8]
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 + w / 2 - ww / 2, yy - 16, ww, 32), 16, 16), fill(with_alpha(col, .25 + .75 * a)))
    draw_text(c, "AGUDO", x0 + 90, y0 + 50, 30, with_alpha(WHITE, .7))
    draw_text(c, "GRAVE", x0 + 90, y0 + h - 30, 30, with_alpha(WHITE, .7))


def s_shep(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1150), 1100 + 40 * math.sin(t * .7), [0xFF1C1640, 0xFF0E0B24, 0xFF05040E], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    if sid in ("h", "s1", "cta"):
        helix(c, t, W / 2, 1260, 980, 300)
        # flecha que sube en bucle
        for k in range(3):
            yy = 1700 - ((t * 260 + k * 330) % 990)
            a = clamp(min((1700 - yy) / 200, (yy - 710) / 200))
            p = skia.Path(); p.moveTo(W - 120, yy - 40); p.lineTo(W - 80, yy + 10); p.lineTo(W - 160, yy + 10); p.close()
            c.drawPath(p, fill(with_alpha(GOLD, .8 * a)))
        if sid == "h" or (sid == "s1" and lt < 1.5):
            K.pill(c, W / 2, 1820, "SUBE EL VOLUMEN", 44, bg=with_alpha(0xFF000000, .65), fg=WHITE)
        if sid == "s1" and lt > P["segs"][1]["speech"][1] - P["segs"][1]["a"]:
            K.pill(c, W / 2, 1820, "ESCUCHA… ¿SUBE O BAJA?", 42, bg=with_alpha(0xFF000000, .65), fg=GOLD)
    elif sid == "s2":
        helix(c, t, W / 2, 1180, 760, 230, alpha=.55)
        # metro de 'altura real': la aguja vuelve siempre al mismo sitio
        pos, amp = IA.layers(t, rate=RATE)
        cen = float((pos * amp).sum() / amp.sum())
        x0, x1, y = 140, W - 140, 1680
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y - 22, x1 - x0, 44), 22, 22), fill(with_alpha(WHITE, .15)))
        xx = lerp(x0 + 40, x1 - 40, clamp((cen - .40) / .2))
        c.drawCircle(xx, y, 34, fill(GOLD)); K.glow(c, xx, y, 90, GOLD, .5)
        if lt > 1.0:
            K.tag(c, W / 2, 1790, "ALTURA MEDIA DEL SONIDO: NO SE MUEVE", lt - 1.0, accent=GOLD, size=36)
    elif sid == "s3":
        bars(c, t, 110, 760, W - 220, 900)
        if lt > 1.4:
            K.tag(c, W / 2, 1760, "LA DE ARRIBA SE APAGA · ENTRA UNA ABAJO", lt - 1.4, accent=CYAN, size=34)
    elif sid == "s4":
        helix(c, t, W / 2 - 170, 1250, 860, 170, alpha=.9)
        bars(c, t, W / 2 + 40, 830, 400, 820)
        if lt > 1.6:
            K.tag(c, W / 2, 1790, "ROGER SHEPARD · 1964", lt - 1.6, accent=GOLD, size=40)


def shep_gain(tt, P):
    """suena flojo bajo la voz y fuerte en las pausas; nunca en el CTA final."""
    g = np.full(len(tt), 0.0)
    for sg in P["segs"]:
        if sg["id"] == "cta":
            continue
        a, b = sg["a"], sg["b"]
        s0, s1 = sg["speech"]
        m = (tt >= a) & (tt < b)
        g[m] = np.where((tt[m] >= s0) & (tt[m] < s1), 0.22, 1.0)
    k = int(0.12 * IA.SR)
    return np.convolve(g, np.ones(k) / k, mode="same")


V2001 = dict(slug="2001_sonido_que_sube_sin_fin", accent=GOLD, drone=0.0, music=0, scene=s_shep, mood="misterio",
             send="ENVÍASELO A ALGUIEN CON CASCOS", rehook=("s3", "ESPERA… MIRA EL TRUCO"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Escucha este sonido. ¿Te parece que sube, que baja, o que se queda igual?", cap="¿Este sonido *SUBE* o *BAJA*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Ahora te dejo escucharlo un poco más, sin hablar.", cap="Escucha… | *sin hablar*", hold=3.8),
    dict(id="s2", who="nar", cut=True, say="Parece que no para de subir, pero no ha subido nada: suena igual que al principio.",
         cap="No ha subido *NADA*: | suena *igual* | que al principio", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Son varias notas a la vez, y cuando la más aguda se apaga, entra una grave sin que la notes.",
         cap="La de arriba *se apaga*… | y entra *una grave*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Lo inventó Roger Shepard en mil novecientos sesenta y cuatro: una escalera infinita, pero de sonido.",
         cap="Roger Shepard, *1964*: | la *escalera infinita* | del sonido", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta si te subía o te bajaba, y envíaselo a alguien con cascos, a ver qué oye.",
         cap="¿Te subía o te bajaba? | *COMENTA*"),
])


# ============================ 2002 balancín (respuesta calculada)
LEFT = [1, 1, 1, 1, 2]       # distancia al centro de cada bloque (pasos)
RIGHT = [4, 4]
TL_, TR_ = sum(LEFT), sum(RIGHT)
assert (TL_, TR_) == (6, 8) and len(LEFT) > len(RIGHT) and TR_ > TL_
ANSWER = "DERECHA"
STEP = 105
BCOL = [0xFFE5534B, 0xFF2A7DE1, 0xFFF2C230, 0xFF34B56A, 0xFF8A5CD6, 0xFFFF7A2E, 0xFF20C4C4]


def crate(c, x, y, s, col, t, k):
    c.save(); c.translate(x, y); c.scale(s, s)
    r = skia.Rect.MakeXYWH(-42, -84, 84, 84)
    c.drawRRect(skia.RRect.MakeRectXY(r, 12, 12), fill(col))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-42, -84, 84, 24), 12, 12), fill(with_alpha(WHITE, .22)))
    c.drawRRect(skia.RRect.MakeRectXY(r, 12, 12), stroke(with_alpha(INK, .55), 5))
    bl = 1 if (t * 0.9 + k * .37) % 3 > .12 else .1
    for ex in (-16, 16):
        c.drawOval(skia.Rect.MakeXYWH(ex - 8, -56 - 9 * bl, 16, 18 * bl), fill(INK))
    c.restore()


def seesaw(c, cx, cy, tilt, t, show_marks=True, hl=None, nums=False, sc=1.12):
    c.save(); c.translate(cx, cy); c.scale(sc, sc)
    # base triangular
    p = skia.Path(); p.moveTo(0, -10); p.lineTo(-100, 205); p.lineTo(100, 205); p.close()
    c.drawPath(p, fill(0xFF6A7088)); c.drawPath(p, stroke(0xFF3A4058, 6))
    c.drawCircle(0, -10, 18, fill(GOLD))
    c.rotate(tilt)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-470, -36, 940, 30), 12, 12), fill(0xFFC8A070))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-470, -36, 940, 30), 12, 12), stroke(0xFF7A5430, 5))
    if show_marks:
        for side in (-1, 1):
            for k in range(1, 5):
                x = side * k * STEP
                c.drawLine(x, -6, x, 16, stroke(with_alpha(WHITE, .7), 5))
                draw_text(c, str(k), x, 52, 30, with_alpha(WHITE, .75))
    for side, items in ((-1, LEFT), (1, RIGHT)):
        stack = {}
        for i, dd in enumerate(items):
            n = stack.get(dd, 0); stack[dd] = n + 1
            x = side * dd * STEP; y = -36 - n * 84
            col = BCOL[(i + (0 if side < 0 else 5)) % len(BCOL)]
            if hl == side:
                K.glow(c, x, y - 42, 80, GOLD, .35 + .15 * math.sin(t * 8))
            crate(c, x, y, 1.0, col, t, i + side)
    if nums:
        draw_text(c, f"{TL_}", -3 * STEP, -360, 110, GOLD, shadow=True)
        draw_text(c, f"{TR_}", 3 * STEP, -360, 110, GREEN, shadow=True)
    c.restore()


def s_bal(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1200), 1050 + 30 * math.sin(t), [0xFF1F3A5A, 0xFF142640, 0xFF08101E], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    rs = np.random.RandomState(7)
    for _ in range(40):
        x = rs.rand() * W; y = (rs.rand() * H - t * (20 + 30 * rs.rand())) % H
        c.drawCircle(x, y, 2 + 3 * rs.rand(), fill(with_alpha(WHITE, .12)))
    c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, 420), fill(0xFF0A1424))
    # balancín sujeto (calzas) hasta la revelación; tiembla un poco
    wob = 1.0 * math.sin(t * 2.3)
    tilt = wob
    hl = None
    if sid == "s3":
        hl = -1 if lt < d * .5 else 1
    if sid in ("s4", "cta"):
        k = clamp(lt / 1.1) if sid == "s4" else 1.0
        # caída con rebote amortiguado hacia la derecha (+)
        ang = 14 * (1 - math.exp(-5 * k) * math.cos(9 * k))
        tilt = ang
    seesaw(c, W / 2, 1270, tilt, t, hl=hl, nums=sid in ("s3", "s4", "cta") and (sid != "s3" or lt > d * .75))
    if sid not in ("s4", "cta"):  # calzas
        for sx in (-1, 1):
            c.drawRect(skia.Rect.MakeXYWH(W / 2 + sx * 420 - 45, 1270, 90, 250), fill(0xFF8A6A4A))
            c.drawRect(skia.Rect.MakeXYWH(W / 2 + sx * 420 - 45, 1270, 90, 250), stroke(0xFF4A3420, 5))
    if sid in ("h", "s1"):
        draw_text(c, "←  ¿IZQUIERDA", W / 2 - 230, 1640, 50, WHITE, shadow=True)
        draw_text(c, "o DERECHA?  →", W / 2 + 230, 1640, 50, WHITE, shadow=True)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1800, 110, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > 1.0:
        K.tag(c, W / 2, 1700, "PESO × DISTANCIA AL CENTRO", lt - 1.0, accent=GOLD, size=48)
    if sid == "s3" and lt > .6:
        K.tag(c, W / 2, 1700, "4×1 + 1×2 = 6   ·   2×4 = 8", lt - .6, accent=WHITE, size=44)
    if sid == "s4" and lt > .9:
        hc.big(c, ANSWER, W / 2, 1720, 120, GREEN, lt - .9, 0.0, outline=12)


V2002 = dict(slug="2002_balancin_izquierda_derecha", accent=GOLD, drone=0.02, scene=s_bal, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Si quito las calzas, ¿hacia qué lado cae el balancín, a la izquierda o a la derecha?", cap="¿Hacia dónde *CAE*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Todos los bloques pesan lo mismo, y tienes cinco segundos.", cap="Todos pesan *igual*. | *5 segundos*", hold=3.5),
    dict(id="s2", who="nar", cut=True, say="Casi todos dicen izquierda, porque hay más bloques, pero importa lo lejos que están del centro.",
         cap="No cuenta solo *cuántos*… | sino *lo lejos* | que están", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="A la izquierda, cuatro bloques a un paso y uno a dos, suman seis. A la derecha, dos a cuatro pasos, ocho.",
         cap="Izquierda: *6*. | Derecha: *8*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Cae a la derecha, aunque tenga menos bloques, por la ley de la palanca de Arquímedes.",
         cap="Cae a la *DERECHA*: | la ley de la *palanca*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta qué lado dijiste, y envíaselo a quien crea que lo saca a la primera.", cap="¿Qué dijiste? | *COMENTA*"),
])

VIDEOS = {"2001": V2001, "2002": V2002}
EXTRA = {"2001": None}


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
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        V = VIDEOS[k]
        ex = None
        if k == "2001":
            holder = {}
            ex = lambda m, P: IA.mixer_hook(lambda tt: shep_gain(tt, P))(m, P)
        K.run(V, make_scene(V), OUT, preview=pv, extra_audio=ex)
