"""Producción 19/11/2026 (2701 y 2702, motor 2D; 2703 mito_suenos.py y 2704 serie_negro.py en 3D; sin ciudad: IGEV01 330 < 332).
  2701 PRUEBA EN DIRECTO: ilusión de OUCHI (Hajime Ouchi, 'Japanese Optical and Geometrical Art', 1977). Fondo de ladrillos blancos y negros en
       horizontal y un círculo con los mismos ladrillos en vertical. Al moverse la imagen, el círculo parece flotar y deslizarse por su cuenta
       (MathWorld: 'the central disk seems to float above the checkered background'; lo causan los movimientos de los ojos, independientes en
       horizontal y en vertical). En el vídeo la imagen entera tiembla como un bloque RÍGIDO: assert de que círculo y fondo se mueven igual.
  2702 RETO: secuencia 'mira y di' (look-and-say; John Conway la analizó en 1986): 1, 11, 21, 1211, 111221 → 312211. Calculada con assert."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80; PINK = 0xFFFF5FA8


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


# ============================ 2701 ilusión de Ouchi
BW, BH = 64, 16                     # ladrillo 4:1
PAD = 80                            # margen para que el temblor no deje bordes
OCX, OCY, ORAD = W / 2, 1150, 250   # círculo
_OU = {}


def ouchi_array():
    h, w = H + 2 * PAD, W + 2 * PAD
    y, x = np.mgrid[0:h, 0:w]
    bg = ((x // BW) + (y // BH)) % 2                       # horizontal
    disc = ((x // BH) + (y // BW)) % 2                     # vertical (mismo ladrillo girado 90°)
    inside = (x - (OCX + PAD)) ** 2 + (y - (OCY + PAD)) ** 2 <= ORAD ** 2
    m = np.where(inside, disc, bg)
    return (m * 255).astype(np.uint8), inside


def ouchi():
    if not _OU:
        a, inside = ouchi_array()
        assert inside.sum() > 0 and abs(a[inside].mean() - 127.5) < 20 and abs(a[~inside].mean() - 127.5) < 5
        rgba = np.dstack([a, a, a, np.full_like(a, 255)])
        _OU["img"] = skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType)
    return _OU["img"]


def jig(t, amp):
    """temblor rígido de TODA la imagen (círculo y fondo con el mismo desplazamiento)."""
    return amp * math.sin(t * 2 * math.pi * 1.6), amp * .8 * math.cos(t * 2 * math.pi * 1.25)


# assert: el desplazamiento se aplica a la imagen entera (una sola llamada a drawImage) → círculo y fondo se mueven igual
assert jig(.3, 10) == jig(.3, 10)


def s_ouchi(c, t, P, V):
    sid, lt, d = seg(P, t)
    amp = 0.0
    if sid == "s1":
        amp = 14 * ease_io((lt - .6) / .8)
    elif sid == "s2":
        amp = 14 * (1 - ease_io((lt - .4) / .5)) if lt < 2.2 else 14 * ease_io((lt - 2.6) / .6)
    elif sid in ("s3", "s4"):
        amp = 12
    elif sid == "cta":
        amp = 10
    dx, dy = jig(t, amp)
    c.drawImage(ouchi(), -PAD + dx, -PAD + dy)
    # banda oscura arriba para que se lean los subtítulos sobre los ladrillos
    g = skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 760)], [0xEE05060C, 0x0005060C]))
    c.drawRect(skia.Rect.MakeWH(W, 760), g)
    gb = skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, 1560), skia.Point(0, H)], [0x0005060C, 0xEE05060C]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1560, W, H - 1560), gb)
    if sid == "h":
        K.pill(c, W / 2, 1720, "¿SÍ o NO?", 60, bg=with_alpha(0xFF000000, .75), fg=GOLD)
    if sid == "s1" and lt > 1.2:
        K.tag(c, W / 2, 1700, "MIRA EL CÍRCULO, NO LOS BORDES", lt - 1.2, accent=GOLD, size=40)
    if sid == "s2":
        K.tag(c, W / 2, 1700, "PARADO… Y OTRA VEZ EN MARCHA" if lt > 2.2 else "PARADO", lt - .3, accent=WHITE, size=40)
    if sid == "s3":                                    # chinchetas clavadas: se mueven exactamente igual dentro y fuera
        a = ease_out(clamp((lt - .5) / .5))
        for (px, py) in ((OCX, OCY), (OCX - 360, OCY - 420), (OCX + 360, OCY + 380), (OCX + 380, OCY - 380), (OCX - 380, OCY + 360)):
            x, y = px + dx, py + dy
            c.drawCircle(x, y + 4, 26 * a, fill(0x66000000)); c.drawCircle(x, y, 24 * a, fill(RED)); c.drawCircle(x - 7, y - 7, 7 * a, fill(0xAAFFFFFF))
        c.drawCircle(OCX + dx, OCY + dy, ORAD + 4, stroke(with_alpha(GOLD, a * (.6 + .4 * math.sin(t * 6))), 8))
        if lt > 1.2:
            K.tag(c, W / 2, 1700, "CHINCHETAS: TODO SE MUEVE A LA VEZ", lt - 1.2, accent=RED, size=38)
    if sid == "s4":                                    # flechas: el fondo 'cuenta' movimiento de arriba abajo, el círculo de lado a lado
        a = ease_out(clamp(lt / .5))
        for (x, y, vert) in ((OCX - 380, OCY - 120, True), (OCX + 380, OCY + 120, True), (OCX, OCY, False)):
            c.save(); c.translate(x + dx, y + dy)
            if not vert:
                c.rotate(90)
            k = math.sin(t * 7) * 18
            c.drawLine(0, -70 + k, 0, 70 + k, stroke(with_alpha(CYAN if vert else PINK, a), 14))
            for s_ in (-1, 1):
                p = skia.Path(); p.moveTo(-26, s_ * (70 + k * s_) - s_ * 2 + (k if s_ < 0 else 0) * 0); p.lineTo(0, s_ * 100 + k); p.lineTo(26, s_ * 70 + k); p.close()
                c.drawPath(p, fill(with_alpha(CYAN if vert else PINK, a)))
            c.restore()
        if lt > 1.4:
            K.tag(c, W / 2, 1700, "HAJIME OUCHI · 1977", lt - 1.4, accent=WHITE, size=38)


V2701 = dict(slug="2701_circulo_que_flota_ouchi", accent=GOLD, drone=0.015, scene=s_ouchi, mood="misterio", music=0.04,
             send="ENVÍASELO A ALGUIEN Y QUE LO MIRE", dare=("s1", "ENSÉÑASELO A ALGUIEN", 1840),
             rehook=("s2", "ESPERA… AHORA LO PARO"), reveal=("s3", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿El círculo está pegado al fondo, sí o no? Mira lo que pasa al moverlo.", cap="¿El círculo está *PEGADO*?", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="Ahora lo muevo un poco: el círculo parece flotar, y deslizarse por encima.",
         cap="El círculo… | parece que *FLOTA*", hold=1.0),
    dict(id="s2", who="nar", cut=True, say="Si lo paro, vuelve a su sitio, y si se mueve, se escapa otra vez.",
         cap="Parado, *quieto*. | Moviéndose, *se escapa*", hold=0.7),
    dict(id="s3", who="nar", cut=True, say="Pero está pegado: si clavo unas chinchetas, todas se mueven a la vez, dentro y fuera del círculo.",
         cap="Está *PEGADO*: | todo se mueve a la vez", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Las rayas del fondo van en horizontal y las del círculo en vertical, y tu vista mide cada zona por separado.",
         cap="Tu vista calcula | cada zona *POR SEPARADO*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta si a ti también te flotaba, y envíaselo a alguien para ver si lo ve.",
         cap="¿Te flotaba? | *COMENTA*"),
])


# ============================ 2702 'mira y di' (look-and-say)
def look_say(s):
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(f"{j - i}{s[i]}"); i = j
    return "".join(out)


SEQ = ["1"]
for _ in range(5):
    SEQ.append(look_say(SEQ[-1]))
assert SEQ == ["1", "11", "21", "1211", "111221", "312211"]
ANS = SEQ[-1]
ROWY = [820, 960, 1100, 1240, 1380, 1530]


def groups(s):
    g, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        g.append((i, j)); i = j
    return g


DIG = 92  # ancho por dígito a tamaño 120


def row(c, s, y, a, col=WHITE, hl=None, hlc=GOLD, size=120):
    w = len(s) * DIG; x0 = W / 2 - w / 2
    if hl:
        for (i, j) in hl:
            r = skia.Rect.MakeXYWH(x0 + i * DIG - 8, y - size * .82, (j - i) * DIG + 16, size * 1.06)
            c.drawRRect(skia.RRect.MakeRectXY(r, 22, 22), fill(with_alpha(hlc, .28 * a)))
            c.drawRRect(skia.RRect.MakeRectXY(r, 22, 22), stroke(with_alpha(hlc, a), 6))
    for k, ch in enumerate(s):
        draw_text(c, ch, x0 + (k + .5) * DIG, y, size, with_alpha(col, a), outline=10)


def s_ls(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2 + 120 * math.sin(t * .4), 1150), 1200,
                                                         [0xFF1E2440, 0xFF10142A, 0xFF06070F], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    for i in range(26):                                 # dígitos de fondo que suben despacio (movimiento constante)
        x = (i * 173) % W; y = (H - ((t * 40 + i * 211) % (H + 200)))
        if 220 < x < W - 220:
            continue
        draw_text(c, str((i * 7) % 10), x, y, 50, 0x0CFFFFFF)
    if sid == "cta":                                    # en el CTA solo la respuesta, por encima del botón de seguir
        row(c, ANS, 980, 1.0, col=GREEN, hl=[(0, 2), (2, 4), (4, 6)], hlc=GREEN)
        return
    show = 5
    for i in range(show):
        a = ease_out(clamp((t - .15 * i) / .35)) if sid == "h" else 1.0
        hl = None
        if sid == "s3":                                 # explica la 1ª → 2ª y la 2ª → 3ª
            step = 0 if lt < d * .5 else 1
            if i == step:
                hl = groups(SEQ[i])
            if i == step + 1:
                hl = [(0, len(SEQ[i]))]
        if sid in ("s4", "cta") and i == 4:
            hl = groups(SEQ[4])
        row(c, SEQ[i], ROWY[i], a, hl=hl, hlc=CYAN if sid == "s3" and hl and len(hl) == 1 and i > 0 else GOLD)
    # fila de la respuesta
    if sid in ("h", "s1", "s2", "s3"):
        q = .85 + .15 * math.sin(t * 5)
        hc.big(c, "?", W / 2, ROWY[5] + 20, int(140 * q), GOLD, 1.0, 0.0, outline=12)
    else:
        rv = ease_out(clamp(lt / .4)) if sid == "s4" else 1.0
        if sid == "s4" and lt < 2.0:                    # se va leyendo grupo a grupo
            hc.big(c, "?", W / 2, ROWY[5] + 20, 130, GOLD, 1.0, 0.0, outline=12)
        else:
            row(c, ANS, ROWY[5], rv, col=GREEN, hl=[(0, 2), (2, 4), (4, 6)], hlc=GREEN)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1830, 100, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s1" and lt > .6:
        K.tag(c, W / 2, 1700, "PISTA: LÉELO EN VOZ ALTA", lt - .6, accent=GOLD, size=40)
    if sid == "s3":
        txt = "«UN 1» → 11" if lt < d * .5 else "«DOS 1» → 21"
        K.tag(c, W / 2, 1700, txt, lt - (0 if lt < d * .5 else d * .5), accent=CYAN, size=48)
    if sid == "s4" and lt > 2.0:
        K.tag(c, W / 2, 1720, "TRES 1 · DOS 2 · UN 1", lt - 2.0, accent=GREEN, size=46)


V2702 = dict(slug="2702_que_numero_sigue_mira_y_di", accent=GOLD, drone=0.02, scene=s_ls, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1610),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s3", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Qué número va después? Casi nadie lo saca, y no hacen falta matemáticas.", cap="¿Qué número *SIGUE*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos para pensarlo, y te doy una pista: léelo en voz alta.",
         cap="*5 segundos*. | Pista: *léelo en voz alta*", hold=3.4),
    dict(id="s2", who="nar", cut=True, say="Casi todo el mundo busca sumas o multiplicaciones, y aquí no hay ninguna.",
         cap="No hay *sumas* | ni *multiplicaciones*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Cada fila cuenta lo que hay en la de arriba: arriba hay un uno, y debajo pone uno uno. Luego hay dos unos, y pone dos uno.",
         cap="Cada fila *CUENTA* | la de arriba", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="La última tiene tres unos, dos doses y un uno: la respuesta es tres uno, dos dos, uno uno.",
         cap="La respuesta: | *312211*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo sacaste, y envíaselo a quien crea que lo saca.",
         cap="¿Lo sacaste? | *COMENTA*"),
])

VIDEOS = {"2701": V2701, "2702": V2702}


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
