"""Producción 17/11/2026 (2501 y 2502, motor 2D; 2503 mito_bizco.py y 2504 serie_hueca.py en 3D; 2509 ciudad 329).
  2501 PRUEBA EN DIRECTO: ¿el centro de la flor brilla más que el fondo? Ilusión de BRILLO (pétalos oscuros con degradado hacia un centro blanco).
       Imagen PROPIA por código: el centro y el fondo son el MISMO blanco (assert sobre los píxeles renderizados: 255·255·255).
       Fuente de la pupila: Laeng y Endestad, Universidad de Oslo, PNAS 23/01/2012 ('Bright illusions reduce the eye's pupil'; Phys.org 25/01/2012:
       'the pupil constricted slightly more when the focus was on the image that appeared brighter'; estímulos equiluminantes).
  2502 RETO: tres dados apilados, ¿cuánto suman las 5 caras escondidas? Caras opuestas suman 7 → 7 + 7 + (7 − 5) = 16 (calculado y comprobado
       con caras visibles coherentes: ninguna cara visible es opuesta de otra del mismo dado)."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


def dropper(c, px, py):
    c.drawCircle(px, py, 50, stroke(WHITE, 9)); c.drawCircle(px, py, 50, stroke(INK, 3))
    c.drawLine(px + 36, py + 36, px + 96, py + 96, stroke(WHITE, 14)); c.drawLine(px + 36, py + 36, px + 96, py + 96, stroke(INK, 4))


def readout(c, y0, lab, rgb, a):
    r, g, b = rgb
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(120, y0, W - 240, 130), 30, 30), fill(with_alpha(0xFF10131F, .92 * a)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(145, y0 + 15, 100, 100), 18, 18), fill(with_alpha(skia.Color(r, g, b), a)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(145, y0 + 15, 100, 100), 18, 18), stroke(with_alpha(0xFF888888, a), 4))
    draw_text(c, lab, 380, y0 + 82, 48, with_alpha(GOLD, a))
    draw_text(c, f"R {r} · G {g} · B {b}", 720, y0 + 82, 44, with_alpha(CYAN, a))


# ============================ 2501 flor que brilla (centro = fondo = 255)
FC = (540, 1080)            # centro de la flor
PANEL = skia.Rect.MakeXYWH(0, 560, W, 1020)
NP = 12
BG_PT = (90, 1500)          # punto del fondo que se mide (esquina inferior izquierda del panel)


def _petals(c, alpha=1.0):
    for i in range(NP):
        a = 2 * math.pi * i / NP
        c.save(); c.translate(*FC); c.rotate(math.degrees(a))
        # pétalo a lo largo del eje x: oscuro fuera (x=420), se funde a blanco hacia el centro (x=130)
        sh = skia.GradientShader.MakeLinear([skia.Point(140, 0), skia.Point(400, 0)], [skia.Color4f(1, 1, 1, 0), skia.Color4f(.05, .05, .09, alpha)], [0, .78])
        p = skia.Paint(Shader=sh, AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9))
        c.drawOval(skia.Rect.MakeLTRB(110, -62, 440, 62), p)
        c.restore()


_FL = {}


def _flower():
    if not _FL:
        s = skia.Surface(W, H); c = s.getCanvas()
        c.drawRect(PANEL, fill(0xFFFFFFFF))
        _petals(c)
        arr = s.makeImageSnapshot().toarray()[:, :, :3][..., ::-1]
        vc = tuple(int(x) for x in arr[FC[1], FC[0]]); vb = tuple(int(x) for x in arr[BG_PT[1], BG_PT[0]])
        assert vc == vb == (255, 255, 255), (vc, vb)
        # el centro entero (radio 90) es blanco puro: ningún píxel del centro supera al fondo
        yy, xx = np.mgrid[FC[1] - 90:FC[1] + 90, FC[0] - 90:FC[0] + 90]
        m = (xx - FC[0]) ** 2 + (yy - FC[1]) ** 2 < 90 ** 2
        assert arr[FC[1] - 90:FC[1] + 90, FC[0] - 90:FC[0] + 90][m].max() <= 255 and arr[FC[1] - 90:FC[1] + 90, FC[0] - 90:FC[0] + 90][m].min() >= 250
        _FL.update(img=s.makeImageSnapshot(), vc=vc, vb=vb)
        print("píxeles medidos: centro", vc, "fondo", vb)
    return _FL


def eye(c, x, y, r, pupil, a=1.0):
    c.drawOval(skia.Rect.MakeXYWH(x - r * 1.6, y - r, r * 3.2, r * 2), fill(with_alpha(WHITE, a)))
    c.drawCircle(x, y, r * .78, fill(with_alpha(0xFF3A7A5A, a)))
    c.drawCircle(x, y, r * .78 * pupil, fill(with_alpha(0xFF050508, a)))
    c.drawCircle(x - r * .25, y - r * .25, r * .12, fill(with_alpha(WHITE, .9 * a)))
    c.drawOval(skia.Rect.MakeXYWH(x - r * 1.6, y - r, r * 3.2, r * 2), stroke(with_alpha(INK, a), 8))


def s_flower(c, t, P, V):
    I = _flower(); sid, lt, d = seg(P, t)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(0xFF14161F))
    z = 1.0 + .04 * min(t, 30) / 30
    c.save(); c.translate(*FC); c.scale(z, z); c.translate(-FC[0], -FC[1])
    c.drawImage(I["img"], 0, 0)
    if sid == "s4":                                   # quito los pétalos: el centro deja de brillar
        k = clamp((lt - .3) / .8) * (1 - clamp((lt - d * .62) / .6))
        if k > 0:
            c.drawRect(PANEL, fill(with_alpha(0xFFFFFFFF, k)))
            c.drawCircle(*FC, 150, stroke(with_alpha(0xFFDDDDDD, k), 4))
    c.restore()
    if sid in ("s1", "s2"):
        pts = [FC, BG_PT]
        for n_, (tx, ty) in enumerate(pts):
            st_ = 1.0 + n_ * 1.6
            k = ease_out(clamp((lt - st_) / 1.0)) if sid == "s1" else 1.0
            if k <= 0:
                continue
            dropper(c, lerp(900, tx, k), lerp(1750, ty, k))
            if k >= 1:
                a = clamp((lt - st_ - 1.0) / .4) if sid == "s1" else 1.0
                readout(c, 1600 + n_ * 150, "CENTRO" if n_ == 0 else "FONDO", I["vc"] if n_ == 0 else I["vb"], a)
    if sid == "s2" and lt > 1.0:
        K.tag(c, W / 2, 1490, "EL MISMO BLANCO: 255", lt - 1.0, accent=GREEN, size=44)
    if sid == "s3":                                   # ojo cuya pupila se cierra un poco al mirar la flor
        a = clamp(lt / .5)
        p = 1.0 - .22 * ease_out(clamp((lt - 1.0) / 2.0))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(140, 1440, W - 280, 330), 40, 40), fill(with_alpha(0xF010131F, a)))
        eye(c, W / 2, 1600, 90, .72 * p, a)
        draw_text(c, f"PUPILA {int(round(100 * p))} %", W / 2, 1745, 40, with_alpha(CYAN, a))
        if lt > 2.2:
            K.tag(c, W / 2, 1830, "LAENG Y ENDESTAD · OSLO · PNAS 2012", lt - 2.2, accent=WHITE, size=30)
    if sid == "s4":
        on = lt < d * .62
        K.tag(c, W / 2, 1720, "SIN PÉTALOS: BLANCO NORMAL" if on else "CON PÉTALOS: OTRA VEZ BRILLA", lt - (.4 if on else d * .62), accent=GOLD, size=40)


V2501 = dict(slug="2501_centro_que_brilla", accent=GOLD, drone=0.015, scene=s_flower, mood="misterio", music=0.04,
             send="ENVÍASELO A QUIEN LO VEA BRILLAR", dare=("s1", "PREGÚNTASELO A ALGUIEN", 1440),
             rehook=("s3", "ESPERA… LO MÁS LOCO"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿El centro de esta flor brilla más que el fondo blanco? Míralo bien, sin apartar la vista.", cap="¿El centro *BRILLA* más que el fondo?", hold=0.5),
    dict(id="s1", who="nar", cut=True, say="A casi todo el mundo le parece una luz. Vamos a medir un píxel del centro y otro del fondo.",
         cap="Parece una *LUZ*. | Medimos *1 píxel* de cada", hold=0.9),
    dict(id="s2", who="nar", cut=True, say="Los dos dan exactamente el mismo blanco. El centro no tiene ni una pizca más de luz que el resto.",
         cap="*EL MISMO* blanco. | Ni un píxel más", hold=0.4),
    dict(id="s3", who="nar", cut=True, say="Y lo más loco: en la Universidad de Oslo vieron que tus pupilas se cierran un poco, como ante una luz de verdad.",
         cap="Tus pupilas *SE CIERRAN* | como ante una luz", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Sin los pétalos, es un blanco normal. Tu cerebro ve las sombras y se inventa un foco que deslumbra.",
         cap="Tu cerebro *INVENTA* | un foco", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo ves brillar, y envíaselo a alguien para ver si a él también le deslumbra.", cap="¿Lo ves brillar? | *COMENTA*"),
])


# ============================ 2502 tres dados: ¿cuánto suman las caras que no ves?
OPP = {1: 6, 6: 1, 2: 5, 5: 2, 3: 4, 4: 3}
# visibles por dado (abajo → arriba): (izquierda, derecha, arriba o None si está tapada)
DICE = [(2, 3, None), (6, 4, None), (1, 3, 5)]
HID = [(1, 6), (2, 5), (2,)]                         # caras tapadas: dado de abajo (arriba, abajo), medio (arriba, abajo), de arriba (abajo)
for (l, r_, tp), hd in zip(DICE, HID):
    vis = [x for x in (l, r_, tp) if x]
    assert all(OPP[a] != b for a in vis for b in vis), vis
    assert all(h not in vis and OPP[h] not in vis or (tp and h == OPP[tp]) for h in hd), (vis, hd)
assert sum(sum(h) for h in HID) == 16 == 7 + 7 + (7 - DICE[2][2])
PIPS = {1: [(.5, .5)], 2: [(.25, .25), (.75, .75)], 3: [(.25, .25), (.5, .5), (.75, .75)], 4: [(.25, .25), (.75, .25), (.25, .75), (.75, .75)],
        5: [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)], 6: [(.25, .22), (.75, .22), (.25, .5), (.75, .5), (.25, .78), (.75, .78)]}
DS = 230; C30 = math.cos(math.radians(30))
DU = np.array([C30, .5]) * DS; DV = np.array([-C30, .5]) * DS; DW = np.array([0, 1.0]) * DS
BASE = np.array([540.0, 1500.0])                     # vértice inferior delantero del dado de abajo


def die_face(c, o, a, b, n, col, a_=1.0, pip=0xFF14161F, hl=0.0):
    p = skia.Path(); p.moveTo(*o); p.lineTo(*(o + a)); p.lineTo(*(o + a + b)); p.lineTo(*(o + b)); p.close()
    c.drawPath(p, skia.Paint(Color=with_alpha(col, a_), AntiAlias=True))
    c.drawPath(p, skia.Paint(Color=with_alpha(0xFF9A9AA6, a_), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    if n:
        c.save(); c.concat(skia.Matrix.MakeAll(a[0], b[0], o[0], a[1], b[1], o[1], 0, 0, 1))
        for (x, y) in PIPS[n]:
            c.drawCircle(x, y, .09, skia.Paint(Color=with_alpha(pip, a_), AntiAlias=True))
        c.restore()


def cube_pts(i, lift=0.0):
    """Esquina delantera superior del dado i (0 = abajo) y los tres vectores."""
    ftop = BASE - DW * (i + 1) - np.array([0, lift])
    return ftop


def die(c, i, t, lift=0.0, top_n=None, alpha=1.0, glowtop=0.0):
    f = cube_pts(i, lift)
    l, r_, tp = DICE[i]
    L = -DU; Rr = -DV                                 # desde la arista delantera: izquierda = -DU (hacia atrás-izq), derecha = -DV (atrás-dcha)
    # cara izquierda: paralelogramo f, f+L, f+L+DW, f+DW  → origen f+L (arriba-izq), a=-L (hacia la arista), b=DW
    die_face(c, f + L, -L, DW, l, 0xFFF2F2F6, alpha)
    die_face(c, f, -Rr * -1, DW, r_, 0xFFDCDCE6, alpha)
    # cara de arriba: rombo f, f+L, f+L+Rr, f+Rr
    if top_n is not None:
        die_face(c, f + L + Rr, -Rr, -L, top_n, 0xFFFFFFFF, alpha)
        if glowtop > 0:
            K.glow(c, *(f + (L + Rr) / 2), 160, GOLD, .45 * glowtop)


def s_dice(c, t, P, V):
    sid, lt, d = seg(P, t)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1100), 1100 + 30 * math.sin(t), [0xFF2A3A2E, 0xFF162019, 0xFF0A0F0B], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    # tapete verde
    tp = skia.Path(); tp.moveTo(540, 1240); tp.lineTo(1080, 1550); tp.lineTo(540, 1860); tp.lineTo(0, 1550); tp.close()
    c.drawPath(tp, fill(0xFF1E6A3A)); c.drawPath(tp, stroke(0xFF2C8A50, 6))
    sh = skia.Path(); sh.moveTo(*(BASE)); sh.lineTo(*(BASE + np.array([300, 60]))); sh.lineTo(*(BASE - DV + np.array([300, 60]))); sh.lineTo(*(BASE - DV)); sh.close()
    c.drawPath(sh, fill(0x55000000))
    # en s3 los dados se separan un poco para enseñar las caras que se tocan; en s4 se marcan
    sep = 0.0
    if sid == "s3":
        sep = 70 * ease_out(clamp((lt - .2) / .8))
    if sid == "s4":
        sep = 70 * (1 - ease_out(clamp((lt - d * .8) / .8)))
    for i in range(3):
        lift = sep * i
        die(c, i, t, lift=lift, top_n=(DICE[i][2] if i == 2 else None), glowtop=(.6 + .4 * math.sin(t * 6)) if sid == "s1" and i == 2 else 0.0)
    # marcas de las caras escondidas (entre dados y debajo)
    hid_y = [BASE[1] - 4, BASE[1] - DS - 4 - 0, BASE[1] - 2 * DS - 4]   # aristas delanteras de contacto
    if sid in ("h", "s1", "s2"):
        a = .55 + .45 * math.sin(t * 5)
        labels = ["?", "?", "?"]
        for k_, y in enumerate(hid_y):
            yy = y - (sep * k_)
            c.drawCircle(860, yy - 40, 46, fill(with_alpha(RED, a)))
            draw_text(c, "?", 860, yy - 22, 56, with_alpha(WHITE, a))
            c.drawLine(812, yy - 40, 700, yy - 40, stroke(with_alpha(RED, a), 6))
    if sid == "s1" and d - lt <= 5:
        n = max(0, int(math.ceil(d - lt)))
        hc.big(c, f"{n}", W / 2, 1880, 110, RED if n <= 3 else WHITE, 1.0, 0.0, outline=12)
    if sid == "s2" and lt > .6:
        K.tag(c, W / 2, 1720, "CARA A CARA: IMPOSIBLE", lt - .6, accent=RED, size=44)
    if sid == "s3":                                   # chips de pares opuestos
        for k_, (a_, b_) in enumerate(((1, 6), (2, 5), (3, 4))):
            k = ease_out(clamp((lt - .5 - k_ * .6) / .4))
            if k <= 0:
                continue
            x = 220 + k_ * 320; y = 1720
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 140, y - 70, 280, 140), 30, 30), fill(with_alpha(0xF010131F, k)))
            draw_text(c, f"{a_} + {b_}", x, y - 2, 52, with_alpha(WHITE, k)); draw_text(c, "= 7", x, y + 52, 40, with_alpha(GOLD, k))
    if sid == "s4":
        parts = [("ABAJO", "7", .3), ("MEDIO", "7", 1.3), ("ARRIBA", "7 − 5 = 2", 2.6)]
        for k_, (lab, val, st_) in enumerate(parts):
            k = ease_out(clamp((lt - st_) / .5))
            if k <= 0:
                continue
            y = BASE[1] - DS * k_ - DS * .5
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(760, y - 55, 300, 110), 26, 26), fill(with_alpha(0xF010131F, k)))
            draw_text(c, lab, 910, y - 10, 30, with_alpha(CYAN, k)); draw_text(c, val, 910, y + 38, 44, with_alpha(GOLD, k))
        if lt > 4.4:
            hc.big(c, "= 16", W / 2, 1760, 140, GREEN, lt - 4.4, 0.0, outline=14)
    if sid == "cta":
        hc.big(c, "16", 870, 1000, 120, GREEN, 1.0, 0.0, outline=12)


V2502 = dict(slug="2502_dados_caras_escondidas", accent=GOLD, drone=0.02, scene=s_dice, mood="misterio",
             send="ENVÍASELO A QUIEN CREA QUE LO SACA", dare=("s1", "RETA A UN AMIGO YA", 1440),
             rehook=("s2", "AQUÍ FALLA CASI TODO EL MUNDO"), reveal=("s4", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="Tres dados apilados. ¿Cuánto suman los puntos de todas las caras que no ves?", cap="¿Cuánto suman los puntos que *NO* ves?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Son cinco caras escondidas, y arriba solo ves un cinco. Tienes cinco segundos.", cap="*5 caras* escondidas. | *5 segundos*", hold=3.5),
    dict(id="s2", who="nar", cut=True, say="Casi todo el mundo intenta adivinarlas una por una, y así es imposible.",
         cap="Cara a cara… | *imposible*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="El truco es que en un dado, las caras opuestas siempre suman siete.",
         cap="Caras opuestas: | siempre suman *7*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Los dos de abajo suman siete cada uno, y el de arriba, siete menos cinco, que son dos: dieciséis en total.",
         cap="7 + 7 + 2 = *16*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Comenta si lo sacaste, y envíaselo a quien crea que lo saca a la primera.", cap="¿Lo sacaste? | *COMENTA*"),
])

VIDEOS = {"2501": V2501, "2502": V2502}


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
    if arg == "img":
        s = skia.Surface(W, H); c = s.getCanvas()
        P = K.plan(VIDEOS[sys.argv[2]])
        for tt in sys.argv[3].split(","):
            c.clear(0xFF000000); VIDEOS[sys.argv[2]]["scene"](c, float(tt), P, VIDEOS[sys.argv[2]]); s.makeImageSnapshot().save(f"/tmp/claude-0/img_{sys.argv[2]}_{tt}.png")
        raise SystemExit
    keys = list(VIDEOS) if arg == "all" else arg.split(",")
    pv = "auto" if len(sys.argv) > 2 else None
    for k in keys:
        K.run(VIDEOS[k], make_scene(VIDEOS[k]), OUT, preview=pv)
