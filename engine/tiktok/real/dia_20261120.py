"""Producción 20/11/2026 (2801 y 2802, motor 2D; 2803 mito_nudillos.py y 2804 serie_cubo.py en 3D; sin ciudad: IGEV01 331 < 332).
  2801 PRUEBA EN DIRECTO: DISCO DE BENHAM (colores de Fechner). Disco con media cara negra y arcos negros sobre blanco que, al girar, hace ver
       anillos de color pálido. Michael Bach (Optical Illusions, 'Benham's Top'): 'In 1894, toy maker Charles E Benham discovered...'; Fechner (1838)
       lo describió primero; 'If the direction of rotation is reversed, the order of these tints is also reversed' (Nature, 1894); 'nobody knows
       for certain why the colours appear'. Wikipedia (Fechner color effect): Benham 'in 1895 sold a top' → el guion no da año (las fuentes
       discrepan 1894/1895). Assert: el disco dibujado es 100 % gris (R=G=B en todos los píxeles del disco).
  2802 RETO: ¿qué letra sigue? U, D, T, C, C, S, S → O (iniciales de uno…ocho). Assert sobre la lista de números."""
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


# ============================ 2801 disco de Benham
DCX, DCY, DR = W / 2, 1130, 400


def benham(c, cx, cy, R, ang):
    """Disco de Benham clásico: media cara negra; la otra mitad blanca con 4 sectores de 45° y 3 arcos negros cada uno, a radios distintos."""
    c.save(); c.translate(cx, cy); c.rotate(ang)
    c.drawCircle(0, 0, R + 10, fill(0xFF2A2A2A))
    c.drawCircle(0, 0, R, fill(0xFFFFFFFF))
    p = skia.Path(); p.moveTo(0, 0); p.arcTo(skia.Rect.MakeXYWH(-R, -R, 2 * R, 2 * R), 180, 180, False); p.close()
    c.drawPath(p, fill(0xFF000000))
    sw = R * .034
    pen = skia.Paint(Color=0xFF000000, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=sw, StrokeCap=skia.Paint.kButt_Cap)
    for k in range(4):
        for j in range(3):
            r = R * (.90 - .205 * k - .06 * j)
            c.drawArc(skia.Rect.MakeXYWH(-r, -r, 2 * r, 2 * r), 45 * k, 45, False, pen)
    c.drawCircle(0, 0, R * .05, fill(0xFF000000))
    c.restore()


def _assert_gray():
    surf = skia.Surface(900, 900); cc = surf.getCanvas(); cc.clear(0xFF000000)
    benham(cc, 450, 450, 400, 23.0)
    a = surf.makeImageSnapshot().toarray()[..., :3].astype(int)
    assert (a[..., 0] == a[..., 1]).all() and (a[..., 1] == a[..., 2]).all(), "el disco tiene color"
    assert a.max() == 255 and a.min() == 0


_assert_gray()


def spin_angle(t, P):
    """Ángulo acumulado (grados). Quieto en el gancho; acelera a ~4,3 vueltas/s (≈ 52°/frame: no múltiplo de 360, sin estrobo fijo);
    se para en s3 para medirlo y en s4 gira AL REVÉS (los colores cambian de orden)."""
    tl = P["tl"]; f = 0.0
    def integ(a, b, w):  # integra la velocidad w(t) (vueltas/s) de a a b en pasos de 1/120 s
        n = max(0, int((b - a) * 120)); return sum(w(a + (i + .5) / 120) for i in range(n)) / 120
    v = 4.3
    def w(x):
        s1a = tl["s1"][0]; s3a, s3b = tl["s3"]; s4a = tl["s4"][0]; ca = tl["cta"][0]
        if x < s1a: return 0
        if x < s3a: return v * ease_io((x - s1a) / 1.2)
        if x < s3a + .6: return v * (1 - ease_io((x - s3a) / .6))
        if x < s4a: return 0
        if x < ca: return -v * ease_io((x - s4a) / 1.0)
        return v * ease_io((x - ca) / 1.0)
    return 360 * integ(0, t, w)


_ANG = {}


def s_benham(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(0xFF14151A))
    for i in range(40):                                  # motas grises que suben despacio (movimiento constante, sin color)
        x = (i * 271) % W; y = H - ((t * 35 + i * 197) % (H + 100))
        c.drawCircle(x, y, 3 + (i % 3), fill(0x22FFFFFF))
    key = round(t * 30)
    if key not in _ANG:
        _ANG[key] = spin_angle(key / 30, P)
    ang = _ANG[key]
    # sombra suave del disco
    c.drawCircle(DCX, DCY + 18, DR + 22, fill(0x55000000))
    benham(c, DCX, DCY, DR, ang)
    if sid == "h":
        K.pill(c, W / 2, 1640, "SOLO BLANCO Y NEGRO", 50, bg=0xEE000000, fg=WHITE)
        K.pill(c, W / 2, 1760, "¿VES COLORES? SÍ o NO", 54, bg=with_alpha(0xFF000000, .8), fg=GOLD)
    if sid == "s1" and lt > 1.0:
        K.tag(c, W / 2, 1700, "SUBE EL BRILLO · MIRA LOS ANILLOS", lt - 1.0, accent=GOLD, size=40)
    if sid == "s3":                                      # cuentagotas que lee el píxel real: negro y blanco puros
        a = ease_out(clamp((lt - .7) / .4))
        for (px, py, lab) in ((DCX - 150, DCY + 120, "R 0 · G 0 · B 0"), (DCX + 120, DCY - 200, "R 255 · G 255 · B 255")):
            c.drawCircle(px, py, 34 * a, stroke(with_alpha(GOLD, a), 7)); c.drawCircle(px, py, 6 * a, fill(with_alpha(GOLD, a)))
        if lt > .9:
            K.pill(c, W / 2, 1640, "NEGRO: R 0 · G 0 · B 0", 46, bg=0xEE000000, fg=WHITE, alpha=a)
            K.pill(c, W / 2, 1750, "BLANCO: R 255 · G 255 · B 255", 46, bg=0xEE000000, fg=WHITE, alpha=a)
    if sid == "s4":
        k = ease_out(clamp(lt / .5))
        for s_ in (-1, 1):                               # flechas de giro al revés
            c.save(); c.translate(DCX, DCY); c.rotate(-t * 120 + s_ * 90)
            c.drawArc(skia.Rect.MakeXYWH(-DR - 60, -DR - 60, 2 * DR + 120, 2 * DR + 120), 0, 50, False, stroke(with_alpha(CYAN, k), 14))
            c.restore()
        if lt > 1.0:
            K.tag(c, W / 2, 1700, "AL REVÉS: LOS COLORES CAMBIAN DE ORDEN", lt - 1.0, accent=CYAN, size=36)
    if sid == "s2" and lt > 1.2:
        K.tag(c, W / 2, 1700, "NI UN PÍXEL DE COLOR", lt - 1.2, accent=WHITE, size=42)


V2801 = dict(slug="2801_disco_de_benham_colores", accent=GOLD, drone=0.015, scene=s_benham, mood="misterio", music=0.04,
             send="ENVÍASELO Y QUE TE DIGA QUÉ VE", dare=("s2", "PREGÚNTASELO A ALGUIEN", 1840),
             rehook=("s2", "¿LOS VES?"), reveal=("s3", "LA PRUEBA"), segs=[
    dict(id="h", who="nar", say="Este disco solo tiene blanco y negro. Cuando gire, ¿vas a ver colores, sí o no?",
         cap="¿Vas a ver *COLORES*?", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Míralo girar unos segundos, con el brillo alto, y fíjate en los anillos.",
         cap="Míralo *girar*… | fíjate en *los anillos*", hold=2.4),
    dict(id="s2", who="nar", cut=True, say="Mucha gente ve anillos marrones, rojizos o azulados, aunque no hay ni un píxel de color.",
         cap="¿*Marrón*? ¿*Rojizo*? ¿*Azul*?", hold=0.8),
    dict(id="s3", who="nar", cut=True, say="Si lo paro y mido los píxeles, solo hay negro y blanco puros.",
         cap="Parado: *SOLO BLANCO Y NEGRO*", hold=0.6),
    dict(id="s4", who="nar", cut=True, say="Es el disco de Benham, un juguete de hace más de cien años, y si gira al revés, los colores cambian de orden.",
         cap="Al revés: | los colores *CAMBIAN*", hold=1.0),
    dict(id="cta", who="nar", cut=True, say="Comenta qué color has visto tú, y envíaselo a alguien para ver si ve lo mismo.",
         cap="¿Qué color viste? | *COMENTA*"),
])


# ============================ 2802 ¿qué letra sigue?
NUMS = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho"]
LET = [n[0].upper() for n in NUMS]
assert "".join(LET) == "UDTCCSSO"
SHOWN, ANS = LET[:7], LET[7]


def s_letras(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2 + 120 * math.sin(t * .4), 1150), 1200,
                                                         [0xFF2A1E40, 0xFF15102A, 0xFF07060F], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    for i in range(26):                                  # letras de fondo que suben despacio
        x = (i * 173) % W; y = (H - ((t * 40 + i * 211) % (H + 200)))
        if 200 < x < W - 200:
            continue
        draw_text(c, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[(i * 7) % 26], x, y, 54, 0x0EFFFFFF)
    # 8 casillas en 2 filas de 4 (la 8ª es la incógnita)
    pos = [(W / 2 + (i % 4 - 1.5) * 220, 930 + (i // 4) * 300) for i in range(8)]
    explain = sid in ("s3", "s4", "cta")
    nlit = 0
    if sid == "s3":
        nlit = min(7, int(lt / (d * .82 / 7)) + 1)
    elif sid in ("s4", "cta"):
        nlit = 8
    for i, (x, y) in enumerate(pos):
        a = ease_out(clamp((t - .12 * i) / .35)) if sid == "h" else 1.0
        bob = 8 * math.sin(t * 2.2 + i)
        r = skia.Rect.MakeXYWH(x - 95, y - 120 + bob, 190, 210)
        lit = i < nlit
        col = GREEN if (i == 7 and nlit == 8) else (CYAN if lit else GOLD)
        c.drawRRect(skia.RRect.MakeRectXY(r, 30, 30), fill(with_alpha(0xFF0B0B16, .85 * a)))
        c.drawRRect(skia.RRect.MakeRectXY(r, 30, 30), stroke(with_alpha(col, a * (1 if lit or i == 7 else .55)), 7))
        if i < 7:
            draw_text(c, SHOWN[i], x, y + 30 + bob, 150, with_alpha(WHITE, a), outline=10)
        elif nlit == 8:
            k = ease_out(clamp(lt / .4)) if sid == "s4" else 1
            draw_text(c, ANS, x, y + 30 + bob, int(150 * (.6 + .4 * k)), with_alpha(GREEN, k), outline=10)
        else:
            q = .85 + .15 * math.sin(t * 5)
            hc.big(c, "?", x, y + 40 + bob, int(150 * q), GOLD, 1.0, 0.0, outline=12)
        if lit and explain:
            draw_text(c, NUMS[i].upper(), x, y + 128 + bob, 40, with_alpha(CYAN if i < 7 else GREEN, 1), outline=6)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1600, 110, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s1" and lt > .6:
        K.tag(c, W / 2, 1760, "PISTA: CUENTA", lt - .6, accent=GOLD, size=44)
    if sid == "s2" and lt > .6:
        K.tag(c, W / 2, 1640, "NO ES EL ABECEDARIO", lt - .6, accent=RED, size=48)


V2802 = dict(slug="2802_que_letra_sigue_udtccss", accent=GOLD, drone=0.02, scene=s_letras, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1840),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s3", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Qué letra va después? No es el abecedario, y casi nadie lo saca a la primera.", cap="¿Qué letra *SIGUE*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Tienes cinco segundos para pensarlo, y te doy una pista: cuenta.",
         cap="*5 segundos*. | Pista: *cuenta*", hold=3.4),
    dict(id="s2", who="nar", cut=True, say="Casi todo el mundo busca un orden en el abecedario, o letras que se saltan, y no lo hay.",
         cap="No es *el abecedario*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Son las iniciales de los números: uno, dos, tres, cuatro, cinco, seis y siete.",
         cap="Son *LOS NÚMEROS*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Así que la siguiente letra es la O, la de ocho.",
         cap="La respuesta: *O* de *OCHO*", hold=0.8),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo sacaste, y envíaselo a quien crea que lo saca.",
         cap="¿Lo sacaste? | *COMENTA*"),
])

VIDEOS = {"2801": V2801, "2802": V2802}


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
