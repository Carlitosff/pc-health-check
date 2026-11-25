"""Producción 25/11/2026 (3301 y 3302, motor 2D; 3303 mito_gato.py y 3304 serie_doslunas.py en 3D; sin ciudad: IGEV01 330 < 332).
  3301 PRUEBA EN DIRECTO: RAYAS O ROMBO (motion binding). Cuatro rayas azules son los lados de un rombo que da vueltas en círculo; sus
       esquinas quedan tapadas por cuatro cuadros del MISMO gris que el fondo (invisibles) → se ven rayas sueltas que suben y bajan por
       parejas. Al pintar los cuadros de naranja aparece el rombo girando. Michael Bach ('Motion Binding'): 'Now the blue lines suddenly
       outline a diamond, which moves in a circular fashion!', 'the motion of the blue lines is exactly the same', 'Our percept, however,
       undergoes a striking change'; bibliografía: Lorenceau J, Shiffrar M (1992) 'The influence of terminators on motion integration
       across space', Vision Res 32:263–275. Assert: la máscara de píxeles azules es IDÉNTICA con tapas grises o naranjas (mismo t).
  3302 RETO: EL TRONCO. Cortarlo en 4 trozos lleva 12 minutos → 3 cortes → 4 min por corte; 8 trozos = 7 cortes = 28 minutos (24 es la
       respuesta rápida). Animación con sierra corte a corte y reloj (assert)."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80
BLUE = 0xFF2F5BFF; ORANGE = 0xFFFF8A1E; GRAY = 0xFF8E8E8E


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


def mix(a, b, k):
    k = clamp(k)
    ca = [(a >> s) & 255 for s in (24, 16, 8, 0)]; cb = [(b >> s) & 255 for s in (24, 16, 8, 0)]
    v = [int(round(x + (y - x) * k)) for x, y in zip(ca, cb)]
    return (v[0] << 24) | (v[1] << 16) | (v[2] << 8) | v[3]


# ============================ 3301 rayas o rombo
CX, CY, RD = W / 2, 1060, 340          # centro y semidiagonal del rombo
RM, PER = 60, 1.7                      # radio y periodo (s) del giro en círculo
S = 110                                # semilado de cada tapa (cubre vértice + giro + grosor)
LW = 16


def offs(t):
    a = 2 * math.pi * t / PER
    return RM * math.cos(a), RM * math.sin(a)


def binding(c, t, occ=0.0, ghost=0.0):
    c.drawRect(skia.Rect.MakeWH(W, H), fill(GRAY))
    dx, dy = offs(t)
    v = [(CX + RD + dx, CY + dy), (CX + dx, CY + RD + dy), (CX - RD + dx, CY + dy), (CX + dx, CY - RD + dy)]
    p = skia.Paint(Color=BLUE, StrokeWidth=LW, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kButt_Cap)
    for i in range(4):
        c.drawLine(*v[i], *v[(i + 1) % 4], p)
    col = mix(GRAY, ORANGE, occ)
    for (x, y) in [(CX + RD, CY), (CX, CY + RD), (CX - RD, CY), (CX, CY - RD)]:
        c.drawRect(skia.Rect.MakeXYWH(x - S, y - S, 2 * S, 2 * S), fill(col))
    if ghost > 0:    # contorno discontinuo del rombo entero (explicación, s4)
        g = skia.Paint(Color=with_alpha(WHITE, ghost), StrokeWidth=5, AntiAlias=True, Style=skia.Paint.kStroke_Style,
                       PathEffect=skia.DashPathEffect.Make([22, 16], t * 40 % 38))
        path = skia.Path(); path.moveTo(*v[0])
        for i in (1, 2, 3):
            path.lineTo(*v[i])
        path.close(); c.drawPath(path, g)


def _assert_binding():
    assert S > RM + LW and RD - S - RM > 60 and CX + RD + S < W     # tapas cubren los vértices en todo el giro; quedan rayas visibles
    for t in (0.0, 0.43, 1.1):
        m = []
        for occ in (0.0, 1.0):
            surf = skia.Surface(W, H); binding(surf.getCanvas(), t, occ)
            a = surf.makeImageSnapshot().toarray()[..., :3].astype(int)   # BGRA → B,G,R
            m.append((a[..., 0] > 200) & (a[..., 2] < 120))
        assert m[0].sum() > 12000 and (m[0] == m[1]).all(), (t, m[0].sum(), (m[0] != m[1]).sum())


_assert_binding()


def s_bind(c, t, P, V):
    sid, lt, d = seg(P, t)
    occ, ghost = 0.0, 0.0
    if sid == "s2":
        occ = ease_io((lt - .9) / .8)
    elif sid == "s3":
        occ = 1 - ease_io((lt - .3) / .7)
    elif sid == "s4":
        ghost = ease_io((lt - 1.2) / .8) * .9
    elif sid == "cta":
        occ = 1.0
    binding(c, t, occ, ghost)
    if sid == "s1" and lt > 1.0:
        K.tag(c, W / 2, 1600, "SOLO MIRA CÓMO SE MUEVEN", lt - 1.0, accent=GOLD, size=42)
    if sid == "s3" and lt > 1.6:
        K.tag(c, W / 2, 1600, "MISMO MOVIMIENTO EXACTO", lt - 1.6, accent=GREEN, size=44)
    if sid == "s4" and lt > 2.4:
        K.tag(c, W / 2, 1840, "LORENCEAU Y SHIFFRAR · VISION RESEARCH · 1992", lt - 2.4, accent=WHITE, size=30)
        K.tag(c, W / 2, 1600, "MICHAEL BACH · 'MOTION BINDING'", lt - 2.4, accent=GOLD, size=36)


V3301 = dict(slug="3301_rayas_o_rombo", accent=GOLD, drone=0.015, scene=s_bind, mood="misterio", music=0.04, clean=True, steady=True,
             send="ENVÍASELO Y QUE TE DIGA QUÉ VE", vote=("s2", ("RAYAS", "ROMBO"), 1, 1740), dare=("s1", "PREGÚNTALE QUÉ VE", 1840),
             rehook=("s3", "AHORA LAS QUITO"), reveal=("s2", "LA VERDAD"), segs=[
    dict(id="h", who="nar", say="¿Ves cuatro rayas sueltas, o una sola figura? Contesta antes de que ponga las tapas.",
         cap="¿Rayas sueltas o *UNA FIGURA*?", hold=0.6),
    dict(id="s1", who="nar", cut=True, say="Fíjate bien: casi todo el mundo ve dos parejas de rayas, que suben y bajan cada una por su cuenta.",
         cap="Dos *PAREJAS* de rayas", hold=0.6),
    dict(id="s2", who="nar", cut=True, say="Ahora pinto de naranja cuatro tapas que ya estaban ahí, y de repente aparece un rombo dando vueltas.",
         cap="¡Es un *ROMBO*!", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Las vuelvo a pintar de gris: las rayas se mueven igual, pero el rombo se esconde.",
         cap="Se mueven *IGUAL*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Sin ver las esquinas, tu cerebro no sabe que las rayas van juntas, y las tapas le dan la pista.",
         cap="Las tapas son *LA PISTA*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta rayas o rombo, según lo que viste al principio, y envíaselo a alguien para ver qué ve.",
         cap="¿Rayas o rombo? | *COMENTA*"),
])


# ============================ 3302 el tronco
PIECES0, MIN0, PIECES1 = 4, 12, 8
CUTS0, CUTS1 = PIECES0 - 1, PIECES1 - 1
PER_CUT = MIN0 / CUTS0
ANS = PER_CUT * CUTS1
assert (CUTS0, PER_CUT, CUTS1, ANS) == (3, 4, 7, 28) and MIN0 * PIECES1 / PIECES0 == 24
LX0, LX1, LY, LH = 90, W - 90, 1080, 170


def log_draw(c, t, n_pieces, cut_prog=0.0, gap=1.0, saw_x=None, shake=0.0):
    """Tronco dividido en n_pieces iguales; cut_prog (0–1) dibuja el corte en marcha en saw_x; gap separa los trozos."""
    L = LX1 - LX0; w = L / n_pieces; g = 18 * gap
    tot = L + g * (n_pieces - 1); x0 = W / 2 - tot / 2
    for i in range(n_pieces):
        x = x0 + i * (w + g); y = LY + math.sin(t * 2 + i) * 2 * gap
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - LH / 2, w, LH), 18, 18)
        c.drawRRect(r, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, y - LH / 2), skia.Point(0, y + LH / 2)],
                                                                         [0xFF9A6A3E, 0xFF6E4424, 0xFF4E2E16]), AntiAlias=True))
        for k in range(4):                                    # vetas
            yy = y - LH / 2 + 30 + k * 34
            c.drawLine(x + 14, yy, x + w - 14, yy + 6 * math.sin(k + i), stroke(0x55301A0A, 4))
        for side in (0, 1):                                   # caras cortadas con anillos
            cx = x + (0 if side == 0 else w)
            if (side == 0 and i > 0 and gap > .05) or (side == 1 and i < n_pieces - 1 and gap > .05):
                c.drawOval(skia.Rect.MakeXYWH(cx - 22, y - LH / 2 + 4, 44, LH - 8), fill(0xFFE8C48A))
                for rr in (.7, .45, .2):
                    c.drawOval(skia.Rect.MakeXYWH(cx - 22 * rr, y - (LH / 2 - 4) * rr, 44 * rr, (LH - 8) * rr), stroke(0xFFB88A4A, 3))
    if saw_x is not None:                                     # sierra entrando en el tronco
        dep = LH * cut_prog; sx = saw_x + 10 * math.sin(t * 40) * shake
        c.drawRect(skia.Rect.MakeXYWH(saw_x - 4, LY - LH / 2, 8, dep), fill(0xFF2A1A0E))
        blade = skia.Path(); top = LY - LH / 2 - 130 + dep
        blade.addRect(skia.Rect.MakeXYWH(sx - 160, top, 320, 46))
        c.drawPath(blade, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, top), skia.Point(0, top + 46)], [0xFFE8EEF4, 0xFF9AA4B0]), AntiAlias=True))
        for k in range(16):
            tx = sx - 160 + k * 20
            tri = skia.Path(); tri.moveTo(tx, top + 46); tri.lineTo(tx + 10, top + 66); tri.lineTo(tx + 20, top + 46); tri.close()
            c.drawPath(tri, fill(0xFFB8C2CC))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx + 140, top - 30, 120, 100), 30, 30), fill(0xFFD8442A))
        if shake > 0:
            for k in range(10):                               # serrín
                a = t * 7 + k; d = (t * 300 + k * 37) % 120
                c.drawCircle(saw_x + math.cos(a) * d * .6, LY + LH / 2 - 10 + d * .5, 5, fill(0xCCE8C48A))


def clock(c, x, y, mins, col=GOLD, r=96):
    c.drawCircle(x, y, r + 10, fill(0xEE000000)); c.drawCircle(x, y, r, stroke(col, 8))
    a = -math.pi / 2 + 2 * math.pi * (mins % 60) / 60
    c.drawLine(x, y, x + r * .78 * math.cos(a), y + r * .78 * math.sin(a), stroke(col, 9))
    draw_text(c, f"{int(round(mins))} min", x, y + r + 72, 56, col, outline=6)


def s_log(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)], [0xFF2E4A2A, 0xFF1A2A18])))
    for i in range(40):                                       # hierba que se mueve
        x = (i * 131) % W; y = 1300 + (i * 53) % 500
        c.drawLine(x, y, x + 8 * math.sin(t * 1.4 + i), y - 34, stroke(0xFF4A7A3A, 5))
    if sid in ("h", "s1", "s2"):
        log_draw(c, t, PIECES0, gap=1.0)
        K.pill(c, W / 2, 800, "4 TROZOS = 12 MINUTOS", 52, bg=0xEE000000, fg=WHITE)
        K.pill(c, W / 2, 1600, "¿Y EN 8 TROZOS?", 58, bg=0xEE000000, fg=GOLD)
        if sid == "s1" and d - lt <= 5:
            n = max(0, int(math.ceil(d - lt)))
            hc.big(c, f"{n}", W / 2, 1420, 200, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
        if sid == "s2":
            a = ease_out(clamp((lt - .3) / .4))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - 300, 1300, 600, 160), 30, 30), fill(with_alpha(0xFF000000, .85 * a)))
            draw_text(c, "¿24 min?", W / 2, 1410, int(84 * (.7 + .3 * a)), with_alpha(RED, a), outline=6)
            if lt > 1.6:
                K.tag(c, W / 2, 1840, "EL DOBLE DE TROZOS → ¿EL DOBLE DE TIEMPO?", lt - 1.6, accent=WHITE, size=32)
    elif sid == "s3":                                         # 3 cortes, 4 minutos cada uno
        u = clamp(lt / (d - .4)) * CUTS0; i = min(CUTS0 - 1, int(u)); f = u - i
        n = 1 + i if f < .85 else 2 + i
        L = LX1 - LX0
        log_draw(c, t, n, gap=1.0, saw_x=LX0 + L * (i + 1) / PIECES0 if n == 1 + i else None, cut_prog=ease_io(f / .85), shake=1.0 if f < .85 else 0)
        mins = PER_CUT * min(CUTS0, i + min(1, f / .85))
        clock(c, W / 2, 1460, mins)
        K.pill(c, W / 2, 800, f"CORTE {i + 1} DE 3", 54, bg=0xEE000000, fg=GOLD)
    elif sid == "s4":                                         # 7 cortes → 28 minutos
        u = clamp((lt - .2) / (d - 1.2)) * CUTS1; i = min(CUTS1 - 1, int(u)); f = u - i
        n = 1 + i if f < .8 else 2 + i
        if lt < .2:
            n, f = 1, 0
        L = LX1 - LX0
        log_draw(c, t, n, gap=1.0, saw_x=LX0 + L * (i + 1) / PIECES1 if n == 1 + i and lt >= .2 else None, cut_prog=ease_io(f / .8), shake=1.0 if f < .8 else 0)
        mins = PER_CUT * min(CUTS1, i + min(1, f / .8)) if lt >= .2 else 0
        done = mins >= ANS - 1e-6
        clock(c, W / 2, 1460, mins, col=GREEN if done else GOLD)
        K.pill(c, W / 2, 800, f"7 CORTES × 4 MIN" if done else f"CORTE {i + 1} DE 7", 54, bg=0xEE000000, fg=GREEN if done else GOLD)
    else:
        log_draw(c, t, PIECES1, gap=1.0)
        clock(c, W / 2, 1460, ANS, col=GREEN)
        K.pill(c, W / 2, 800, "28 MINUTOS, NO 24", 56, bg=0xEE000000, fg=GREEN)


V3302 = dict(slug="3302_tronco_ocho_trozos", accent=GOLD, drone=0.02, scene=s_log, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1840),
             rehook=("s3", "ESPERA… CUENTA LOS CORTES"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Cortar este tronco en cuatro trozos lleva doce minutos. ¿Cuánto tardas en cortarlo en ocho trozos?",
         cap="¿Cuánto tarda en *8 TROZOS*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos para pensarlo, sin hacer trampa.",
         cap="*5 segundos*", hold=2.6),
    dict(id="s2", who="nar", cut=True, say="Lo que sale rápido es veinticuatro minutos, porque son el doble de trozos.",
         cap="¿*24 minutos*?", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero cuenta los cortes: para tener cuatro trozos solo hacen falta tres, así que cada corte lleva cuatro minutos.",
         cap="3 cortes: | *4 MINUTOS* cada uno", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y para tener ocho trozos hacen falta siete cortes. Siete cortes de cuatro minutos son veintiocho minutos.",
         cap="7 cortes: | *28 MINUTOS*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta qué habías dicho, y envíaselo a un amigo para ver si dice veinticuatro.",
         cap="¿Qué dijiste tú? | *COMENTA*"),
])

VIDEOS = {"3301": V3301, "3302": V3302}


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
