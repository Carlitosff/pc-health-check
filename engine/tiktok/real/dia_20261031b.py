"""31/10/2026 extra (611): LA MONTAÑA DE LA COMUNIDAD. Formato nuevo de crecimiento pedido por Carlos:
cada seguidor = 1 metro de montaña. Hoy somos 25 (Metricool, 30/10) -> 25 m. Serie implícita: cada día se enseña
cuánto ha crecido (actualizar N con los seguidores reales). Hitos: 100 m -> nieve en la cima; meta: Everest 8.849 m."""
import math, sys, random
import numpy as np
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow, pill
from core import draw_text, font, text_w

OUT = "/home/claude/tiktok/outdaily"
N = 25  # seguidores reales hoy
GOLD = 0xFFFFC23A
BASE_Y = 1700


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


def sky(c, t):
    c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)],
                [0xFF0B1030, 0xFF3A2A6A, 0xFFE07A5A, 0xFFFFC27A], [0, 0.45, 0.78, 1])))
    R = random.Random(1)
    for i in range(120):
        x, y = R.uniform(0, W), R.uniform(0, 800)
        a = 0.3 + 0.3 * math.sin(t * 2 + i)
        c.drawCircle(x, y, R.uniform(1, 2.6), fill(with_alpha(WHITE, a)))
    for k in range(5):
        x = (k * 330 + t * (20 + k * 6)) % (W + 600) - 300
        y = 700 + k * 90
        for j in range(5):
            c.drawOval(skia.Rect.MakeXYWH(x + j * 70 - 120, y - 30 - (j % 2) * 20, 220, 80),
                       skia.Paint(AntiAlias=True, Color=with_alpha(0xFFFFE0D0, 0.10), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18)))


def far_range(c, t):
    for k, (yb, col, amp) in enumerate(((1430, 0xFF5A3A6A, 120), (1520, 0xFF3A2A4A, 90))):
        p = skia.Path(); p.moveTo(0, H)
        for x in range(0, W + 30, 30):
            p.lineTo(x, yb - amp * abs(math.sin(x * 0.004 + k * 1.7)) - 30 * math.sin(x * 0.013 + k))
        p.lineTo(W, H); p.close()
        c.drawPath(p, fill(col))


def mountain(c, hpx, t, snow=0.0, ghost=0.0, wk=1.0):
    """Montaña central con roca procedural; hpx = altura en píxeles sobre BASE_Y."""
    top = BASE_Y - hpx
    half = (180 + hpx * 0.9) * wk
    pts = []
    R = random.Random(7)
    n = 26
    for i in range(n + 1):
        f = i / n
        x = W / 2 - half + 2 * half * f
        y = BASE_Y - hpx * (1 - abs(2 * f - 1)) ** 1.15 + R.uniform(-1, 1) * hpx * 0.035 * (1 - abs(2 * f - 1))
        pts.append((x, y))
    p = skia.Path(); p.moveTo(W / 2 - half - 60 * wk, H)
    for x, y in pts:
        p.lineTo(x, y)
    p.lineTo(W / 2 + half + 60 * wk, H); p.close()
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear(
        [(W / 2 - half, top), (W / 2 + half, BASE_Y)], [0xFF8A7A8A, 0xFF4A3A4A, 0xFF241A26])))
    c.save(); c.clipPath(p, doAntiAlias=True)
    # cara en sombra
    sh = skia.Path(); sh.moveTo(W / 2, top); sh.lineTo(W / 2 + half + 60, BASE_Y + 40); sh.lineTo(W / 2 + 40, BASE_Y + 40); sh.close()
    c.drawPath(sh, fill(with_alpha(0xFF0A0610, 0.35)))
    for i in range(60):  # vetas de roca
        x = R.uniform(W / 2 - half, W / 2 + half)
        y = R.uniform(top, BASE_Y)
        c.drawLine(x, y, x + R.uniform(-60, 60), y + R.uniform(20, 70), stroke(with_alpha(0xFF100810, 0.25), R.uniform(2, 5)))
    if snow > 0:
        sp = skia.Path(); sp.moveTo(W / 2, top - 4)
        sh_ = hpx * 0.28
        for k in range(9):
            f = k / 8
            sp.lineTo(W / 2 + (f * 2 - 1) * sh_ * 0.95, top + sh_ * (0.55 + 0.25 * (k % 2)))
        sp.close()
        c.drawPath(sp, fill(with_alpha(0xFFF4F6FF, snow)))
    c.restore()
    if ghost > 0:  # el siguiente metro: TÚ
        gh = 46
        g = skia.Path(); g.moveTo(W / 2, top - gh); g.lineTo(W / 2 + 70, top + 20); g.lineTo(W / 2 - 70, top + 20); g.close()
        a = ghost * (0.55 + 0.45 * math.sin(t * 6))
        c.drawPath(g, fill(with_alpha(GOLD, 0.35 * a)))
        c.drawPath(g, stroke(with_alpha(GOLD, a), 5))
    return top


def flag(c, x, y, t, label):
    c.drawLine(x, y, x, y - 130, stroke(0xFFEDEDED, 7))
    p = skia.Path(); p.moveTo(x, y - 130)
    for k in range(9):
        f = k / 8
        p.lineTo(x + 170 * f, y - 130 + 8 * math.sin(t * 6 + f * 5))
    for k in range(8, -1, -1):
        f = k / 8
        p.lineTo(x + 170 * f, y - 66 + 8 * math.sin(t * 6 + f * 5 + 0.4))
    p.close()
    c.drawPath(p, fill(0xFFFE2C55))
    draw_text(c, label, x + 85, y - 84, 38, WHITE, shadow=False)


def ruler(c, top, hpx, meters):
    x = 120
    c.drawLine(x, BASE_Y, x, top, stroke(with_alpha(WHITE, 0.8), 5))
    step = max(1, int(meters / 5)) if meters > 0 else 1
    for m in range(0, int(meters) + 1, step):
        y = BASE_Y - hpx * m / max(1, meters)
        c.drawLine(x - 18, y, x + 18, y, stroke(WHITE, 4))
        draw_text(c, f"{m}", x + 60, y + 12, 30, WHITE, shadow=True)


def s_monte(c, t, P, V):
    sid, lt = seg(P, t)
    sky(c, t)
    far_range(c, t)
    full = 760  # px para N metros
    if sid == "h":
        m = N
        hpx = full * ease_out(clamp(lt / 1.4)) if t > 0.01 else full
        top = mountain(c, hpx, t)
        flag(c, W / 2, top, t, f"{N} m")
    elif sid == "s1":
        m = min(N, int(N * clamp(lt / 3.0)) + 1)
        hpx = full * m / N
        top = mountain(c, hpx, t)
        ruler(c, top, hpx, m)
        flag(c, W / 2, top, t, f"{m} m")
        hc.big(c, f"{m}", W / 2, 1860, 120, GOLD, 1.0, 0.0)
    elif sid == "s2":
        top = mountain(c, full, t)
        flag(c, W / 2, top, t, f"{N} m")
        # comparativa: un edificio de 8 plantas al lado (3 m por planta)
        bh = full * 24 / N
        x = W - 270
        c.drawRect(skia.Rect.MakeXYWH(x, BASE_Y - bh * ease_out(clamp(lt / 1.0)), 170, bh * ease_out(clamp(lt / 1.0))), fill(0xFF2A3044))
        for fl in range(8):
            yy = BASE_Y - (fl + 1) * bh / 8 * ease_out(clamp(lt / 1.0))
            for j in range(3):
                on = (fl * 3 + j) % 4 != 0
                c.drawRect(skia.Rect.MakeXYWH(x + 18 + j * 52, yy + 18, 32, bh / 8 - 40), fill(0xFFFFD27A if on else 0xFF1A1E2A))
        K.tag(c, x + 85, BASE_Y + 70, "8 PLANTAS", lt - 0.8, accent=GOLD, size=32)
    elif sid == "s3":
        # zoom out: la montaña al lado del Everest
        k = ease_in_out(clamp(lt / 2.2))
        sc = lerp(1.0, 0.012, k)
        top = mountain(c, max(8, full * sc), t, wk=max(0.06, sc))
        if k > 0.3:
            a = clamp((k - 0.3) / 0.4)
            ev = skia.Path(); ev.moveTo(-200, BASE_Y); ev.lineTo(W * 0.35, 760); ev.lineTo(W * 0.42, 820); ev.lineTo(W * 0.55, 690)
            ev.lineTo(W + 200, BASE_Y); ev.close()
            c.drawPath(ev, fill(with_alpha(0xFF3A3448, 0.85 * a)))
            snow_p = skia.Path(); snow_p.moveTo(W * 0.47, 760); snow_p.lineTo(W * 0.55, 690); snow_p.lineTo(W * 0.63, 780); snow_p.close()
            c.drawPath(snow_p, fill(with_alpha(0xFFF4F6FF, a)))
            K.tag(c, W * 0.55, 640, "EVEREST · 8.849 m", lt - 1.2, accent=WHITE, size=36)
        c.save(); c.translate(0, 0)
        c.drawCircle(W / 2, BASE_Y - 10, 46 * k, stroke(with_alpha(0xFFFE2C55, k), 6))
        c.restore()
        K.tag(c, W / 2, BASE_Y + 80, f"NOSOTROS · {N} m", lt - 1.6, accent=GOLD, size=34)
    elif sid == "s4":
        top = mountain(c, full, t, snow=0.0, ghost=1.0)
        flag(c, W / 2, top - 46, t, f"{N + 1} m")
        hc.big(c, "+1 = TÚ", W / 2, 1860, 110, GOLD, lt, 0.2)
    elif sid == "s5":
        k = ease_in_out(clamp((lt - 0.3) / 1.6))
        top = mountain(c, full * lerp(1, 1.25, k), t, snow=k)
        flag(c, W / 2, top, t, "100 m")
        K.tag(c, W / 2, 1860, "A LOS 100: NIEVE EN LA CIMA", lt - 0.5, accent=WHITE, size=38)
    else:
        top = mountain(c, full, t, ghost=1.0)
        flag(c, W / 2, top - 46, t, f"{N + 1} m")


V611 = dict(slug="611_montana_comunidad", accent=GOLD, drone=0.03, scene=s_monte, tease="ESTA MONTAÑA ERES TÚ",
            send="ENVÍASELO A UN AMIGO PARA QUE SUME 1 METRO", rehook=("s3", "¿Y SI LLEGAMOS AL EVEREST?"),
            reveal=("s3", "EL RETO"), segs=[
    dict(id="h", who="nar", say=f"Esta montaña mide {N} metros. Uno por cada persona que me sigue.",
         cap=f"Esta montaña mide | *{N} METROS*", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Cada vez que alguien nuevo se suma, la montaña crece un metro. Así hemos llegado hasta aquí.",
         cap="Cada persona nueva | que se suma… | la montaña crece *1 METRO*"),
    dict(id="s2", who="nar", cut=True, say="Ahora mismo es como un edificio de ocho plantas. Está bien. Pero quiero más.",
         cap="Ahora es como un edificio | de *8 plantas*. | Pero quiero *MÁS*"),
    dict(id="s3", who="nar", cut=True, say="El reto: llegar a la altura del Everest. Ocho mil ochocientos cuarenta y nueve metros. Una persona, un metro.",
         cap="El reto: el *EVEREST*. | *8.849 metros*. | Una persona, un metro"),
    dict(id="s4", who="nar", cut=True, say="Y el siguiente metro puedes ser tú. Solo tienes que darle a seguir.",
         cap="El siguiente metro | puedes ser *TÚ*: | dale a *SEGUIR*", hold=0.3),
    dict(id="s5", who="nar", cut=True, say="Cuando lleguemos a cien, la montaña tendrá nieve en la cima. Y cada día te enseño cuánto ha crecido.",
         cap="A los *100*, nieve | en la cima. Y cada día | te enseño *cuánto crece*"),
    dict(id="cta", who="nar", cut=True, say="Sígueme y súbela un metro. Comenta: yo subo. Y mañana vemos cuánto ha crecido.",
         cap="*SÍGUEME* y súbela un metro. | Comenta *YO SUBO* | y mañana lo vemos"),
])

VIDEOS = [V611]


def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
    return scene


if __name__ == "__main__":
    pv = "auto" if len(sys.argv) > 2 else None
    K.run(V611, make_scene(V611), OUT, preview=pv)
