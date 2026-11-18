"""Producción 18/11/2026 (2601 y 2602, motor 2D; 2603 mito_sapo.py y 2604 serie_caida.py en 3D; 2609 ciudad 332).
  2601 PRUEBA EN DIRECTO: imagen HÍBRIDA (motor v29, real/hibrida.py): de cerca pone 'SÍ' (solo bordes finos, frecuencias altas) y de lejos
       'NO' (solo manchas, frecuencias bajas). Técnica de Aude Oliva, Antonio Torralba y Philippe Schyns ('Hybrid images', SIGGRAPH 2006, MIT).
       Assert: con la imagen reducida al 10 % (como vista desde lejos) se parece mucho más a 'NO' que a 'SÍ'. El vídeo la encoge en directo.
  2602 RETO: el reloj del espejo. En el espejo se ve las 2:25; la hora real es 12:00 − 2:25 = 9:35 (simetría izquierda-derecha: ángulo → 360 − ángulo).
       Assert sobre los ángulos de las dos agujas."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, hibrida as Hb
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80; PINK = 0xFFFF5FA8


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


# ============================ 2601 imagen híbrida SÍ / NO
_HY = {}


def _gray_img(a):
    u = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    rgba = np.dstack([u, u, u, np.full_like(u, 255)])
    return skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType).withDefaultMipmaps()


def _hy():
    if not _HY:
        img, lo, hi, A, B = Hb.make(s_low=30, k_low=.42, s_high=3.5, k_high=1.3)
        far, near = Hb.score(img, A, B, .1)
        assert far > near + .3, (far, near)          # de lejos gana 'NO'
        print("híbrida: de lejos parecido a NO", round(far, 2), "a SÍ", round(near, 2))
        _HY.update(img=_gray_img(img), lo=_gray_img(lo), hi=_gray_img(hi), w=img.shape[1], h=img.shape[0])
    return _HY


SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
CX, CY = W / 2, 1180


def card(c, im, cx, cy, s, a=1.0, border=True):
    I = _hy(); w, h = I["w"] * s, I["h"] * s
    r = skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h)
    if border:
        c.drawRRect(skia.RRect.MakeRectXY(r.makeOutset(14 * s + 4, 14 * s + 4), 26 * s + 6, 26 * s + 6), fill(with_alpha(0xFF0B0D16, a)))
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(im, r, SAMP, p)


def phone_away(c, t, x, y, a):
    """pictograma: un móvil que se aleja y vuelve (indica 'aléjate')."""
    k = .5 + .5 * math.sin(t * 2.2)
    s = lerp(1.0, .45, k)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-55, -95, 110, 190), 20, 20), fill(with_alpha(0xFF2A2F45, a)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-45, -80, 90, 160), 10, 10), fill(with_alpha(0xFF9AA0B8, a)))
    c.restore()
    for d in (-1, 1):
        c.drawLine(x + d * 100, y, x + d * 160, y, stroke(with_alpha(GOLD, a * (1 - k)), 8))


def s_hyb(c, t, P, V):
    I = _hy(); sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1150), 1150 + 40 * math.sin(t * .6),
                                                         [0xFF2A2E40, 0xFF161926, 0xFF07080E], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    s = 1.0
    if sid == "s2":                                     # la encojo (= alejarse) y la devuelvo
        k = ease_io((lt - .3) / 1.6) * (1 - ease_io((lt - (d - 1.4)) / 1.1))
        s = lerp(1.0, .10, k)
    if sid in ("h", "s1", "s2", "cta"):
        card(c, I["img"], CX, CY, s)
        if sid == "s2" and s < .35:
            K.tag(c, W / 2, 1640, "ASÍ LA VE QUIEN ESTÁ LEJOS", lt - .9, accent=GOLD, size=42)
        if sid == "h":
            K.pill(c, W / 2, 1720, "¿SÍ o NO?", 60, bg=with_alpha(0xFF000000, .7), fg=GOLD)
        if sid == "s1":
            phone_away(c, t, W / 2, 1850, clamp(lt / .5) * .9)
            K.tag(c, W / 2, 1610, "ESTIRA EL BRAZO O ALÉJATE 2 METROS", lt - .5, accent=WHITE, size=36)
    elif sid == "s3":                                   # las dos capas por separado
        k = ease_out(clamp(lt / .9))
        card(c, I["img"], CX, CY, lerp(1.0, .62, k), a=1 - k)
        card(c, I["hi"], lerp(CX, W / 2, k), lerp(CY, 990, k), lerp(1.0, .62, k), a=k)
        card(c, I["lo"], lerp(CX, W / 2, k), lerp(CY, 1520, k), lerp(1.0, .62, k), a=k)
        if lt > 1.0:
            K.tag(c, W / 2 + 330, 760, "BORDES FINOS", lt - 1.0, accent=CYAN, size=32)
        if lt > 1.8:
            K.tag(c, W / 2 + 330, 1820, "MANCHAS BORROSAS", lt - 1.8, accent=GOLD, size=32)
    elif sid == "s4":                                   # ojo que 'enfoca': de cerca bordes, de lejos manchas
        u = .5 + .5 * math.sin(lt * 1.6 - 1.5)
        card(c, I["hi"], W / 2, 1000, .58, a=1 - .8 * u)
        card(c, I["lo"], W / 2, 1000, .58, a=.2 + .8 * u)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(140, 1360, W - 280, 140), 70, 70), fill(with_alpha(0xFF000000, .5)))
        xx = lerp(220, W - 220, u)
        c.drawCircle(xx, 1430, 40, fill(GOLD)); K.glow(c, xx, 1430, 100, GOLD, .5)
        draw_text(c, "CERCA", 250, 1550, 36, CYAN); draw_text(c, "LEJOS", W - 250, 1550, 36, GOLD)
        if lt > 1.5:
            K.tag(c, W / 2, 1700, "OLIVA, TORRALBA Y SCHYNS · MIT · 2006", lt - 1.5, accent=WHITE, size=32)


V2601 = dict(slug="2601_si_o_no_imagen_hibrida", accent=GOLD, drone=0.015, scene=s_hyb, mood="misterio", music=0.04,
             send="ENVÍASELO A ALGUIEN Y QUE LO LEA", dare=("s1", "PREGÚNTASELO A ALGUIEN", 1720),
             rehook=("s3", "ESPERA… MIRA EL TRUCO"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Qué pone en esta imagen, sí o no? Fíjate bien antes de seguir.", cap="¿Qué pone *AQUÍ*?", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="De cerca, casi todo el mundo lee que sí. Ahora estira el brazo, o aléjate, y vuelve a mirarla.",
         cap="De cerca pone *SÍ*. | Ahora *ALÉJATE*", hold=2.2),
    dict(id="s2", who="nar", cut=True, say="Si la hago pequeña, como si estuvieras lejos, el sí desaparece y sale un no.",
         cap="De lejos… | pone *NO*", hold=1.0),
    dict(id="s3", who="nar", cut=True, say="Es una imagen híbrida: el sí está hecho solo de bordes finos, y el no, solo de manchas borrosas.",
         cap="*SÍ* = bordes finos | *NO* = manchas", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="De cerca tu vista se queda con los bordes, y de lejos solo le llegan las manchas.",
         cap="De lejos, los bordes | *DESAPARECEN*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta qué leíste de lejos, y envíaselo a alguien para ver qué lee.",
         cap="¿Qué leíste? | *COMENTA*"),
])


# ============================ 2602 el reloj del espejo (respuesta calculada)
REAL_H, REAL_M = 9, 35
def hand_angles(h, m):
    return (h % 12) * 30 + m * 0.5, m * 6.0
RH, RM = hand_angles(REAL_H, REAL_M)
MH, MM = (360 - RH) % 360, (360 - RM) % 360         # en el espejo: izquierda ↔ derecha
assert (MH, MM) == hand_angles(2, 25)                 # lo que se ve: las 2:25
assert (12 * 60 - (2 * 60 + 25)) == REAL_H * 60 + REAL_M  # regla: 12:00 − hora del espejo
TILE = 0xFFDCE6EE


def bathroom(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), fill(0xFFB8C7D3))
    for y in range(0, H, 120):
        for x in range(-60 * ((y // 120) % 2), W, 120):
            c.drawRect(skia.Rect.MakeXYWH(x + 3, y + 3, 114, 114), fill(TILE))
    c.drawRect(skia.Rect.MakeXYWH(0, 1700, W, 220), fill(0xFFF4F6F8))     # lavabo
    c.drawRect(skia.Rect.MakeXYWH(0, 1700, W, 16), fill(0xFFC9D2DA))


def clock(c, cx, cy, R, hA, mA, mirror=False, t=0.0, sx=1.0):
    c.save(); c.translate(cx, cy); c.scale(sx, 1)
    c.drawCircle(0, 8, R + 18, fill(0x44000000))
    c.drawCircle(0, 0, R + 18, fill(0xFFB23A2E)); c.drawCircle(0, 0, R, fill(0xFFFFFBF2))
    for i in range(60):
        a = math.radians(i * 6); l = 34 if i % 5 == 0 else 14
        c.drawLine(math.sin(a) * (R - 12), -math.cos(a) * (R - 12), math.sin(a) * (R - 12 - l), -math.cos(a) * (R - 12 - l),
                   stroke(INK, 9 if i % 5 == 0 else 4))
    for n in (range(1, 13) if not mirror else []):   # en el espejo, reloj sin números (si no, se leería bien)
        a = math.radians(n * 30); x, y = math.sin(a) * (R - 92), -math.cos(a) * (R - 92)
        if mirror:
            x = -x
        c.save(); c.translate(x, y)
        if mirror:
            c.scale(-1, 1)
        draw_text(c, str(n), 0, 22, 62, INK)
        c.restore()
    def hand(ang, L, wdt, col):
        a = math.radians(-ang if mirror else ang)
        c.drawLine(0, 0, math.sin(a) * L, -math.cos(a) * L, stroke(col, wdt))
    hand(hA, R * .52, 22, INK)
    hand(mA, R * .80, 14, INK)
    # segundero que avanza (movimiento constante)
    sa = (t * 6) % 360
    hand(sa, R * .86, 5, RED)
    c.drawCircle(0, 0, 18, fill(INK))
    c.restore()


def s_mirror(c, t, P, V):
    sid, lt, d = seg(P, t)
    bathroom(c, t)
    MX, MY, MW, MHh = 90, 700, W - 180, 960
    # espejo con marco y reflejo
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(MX - 24, MY - 24, MW + 48, MHh + 48), 40, 40), fill(0xFF6B4A2E))
    gp = skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(MX, MY), skia.Point(MX + MW, MY + MHh)], [0xFFAFC3D1, 0xFFE3EEF5, 0xFF9DB2C2]))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(MX, MY, MW, MHh), 24, 24), gp)
    sh = (t * 90) % (MW + 600) - 300
    p = skia.Path(); p.moveTo(MX + sh, MY); p.lineTo(MX + sh + 120, MY); p.lineTo(MX + sh - 180, MY + MHh); p.lineTo(MX + sh - 300, MY + MHh); p.close()
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(MX, MY, MW, MHh), 24, 24)); c.drawPath(p, fill(0x33FFFFFF)); c.restore()
    flip = 0.0
    if sid == "s3":
        flip = ease_io((lt - .4) / 1.2)
    elif sid in ("s4", "cta"):
        flip = 1.0
    sx = math.cos(math.pi * flip)                       # el reloj se da la vuelta: del espejo a la realidad
    mirror = flip < .5
    z = 1 + .03 * math.sin(t * .8)
    clock(c, W / 2, MY + MHh / 2, 360 * z, RH, RM, mirror=mirror, t=t, sx=abs(sx) if abs(sx) > .02 else .02)
    if sid in ("h", "s1", "s2"):
        K.pill(c, W / 2, MY + 60, "EN EL ESPEJO", 40, bg=with_alpha(0xFF000000, .7), fg=WHITE)
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1880, 100, RED if n <= 3 else INK, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > .8:
        K.tag(c, W / 2, 1790, "PARECEN LAS 2:25… PERO ESTÁ AL REVÉS", lt - .8, accent=GOLD, size=38)
    if sid in ("s3", "s4") and flip > .9:
        K.pill(c, W / 2, MY + 60, "DE VERDAD", 40, bg=with_alpha(0xFF000000, .7), fg=GREEN)
    if sid == "s4":
        hc.big(c, "9:35", W / 2, 1800, 120, GREEN, lt - .2, 0.0, outline=12)
    if sid == "s3" and lt > 1.5:
        K.tag(c, W / 2, 1790, "12:00 − 2:25 = 9:35", lt - 1.5, accent=WHITE, size=46)


V2602 = dict(slug="2602_reloj_del_espejo", accent=GOLD, drone=0.02, scene=s_mirror, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1745),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s3", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Este reloj lo estás viendo en el espejo. ¿Qué hora es de verdad?", cap="¿Qué hora es *DE VERDAD*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Es un reloj sin números, reflejado en el espejo, y tienes cinco segundos para decirlo.",
         cap="Reflejado *en el espejo*. | *5 segundos*", hold=3.4),
    dict(id="s2", who="nar", cut=True, say="Casi todo el mundo dice las dos y veinticinco, porque lo lee como un reloj normal.",
         cap="Casi todos dicen | *2:25*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero el espejo cambia la izquierda por la derecha, y hay un truco: a las doce le restas lo que ves.",
         cap="Truco: *12:00* | menos lo que ves", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Doce menos dos y veinticinco: son las nueve y treinta y cinco. Dale la vuelta y lo ves.",
         cap="Son las *9:35*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta qué hora dijiste tú, y envíaselo a quien crea que lo saca a la primera.", cap="¿Qué hora dijiste? | *COMENTA*"),
])

VIDEOS = {"2601": V2601, "2602": V2602}


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
        K.run(V, make_scene(V), OUT, preview=pv)
