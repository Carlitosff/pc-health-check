"""31/10/2026 extra (612): LA MONTAÑA DE LA COMUNIDAD · actualización 1. El 611 (02:07) trajo 35 seguidores en una
noche (dato de Carlos): 25 -> 60 m. Se celebra el crecimiento, se da las gracias y se fija el siguiente hito
(100 m = nieve en la cima; faltan 40)."""
import math, sys
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import dia_20261031b as B  # noqa (612 montaña: archivo dia_20261031m.py)
from core import W, H, WHITE, clamp, lerp, ease_out, ease_in_out, with_alpha, fill, stroke, draw_text

OUT = "/home/claude/tiktok/outdaily"
OLD, N, GOAL = 25, 60, 100
GOLD = B.GOLD
BASE_Y = B.BASE_Y
FULL = 900  # px para N metros


def confetti(c, t, lt, k=1.0):
    import random
    R = random.Random(12)
    for i in range(140):
        x = R.uniform(0, W) + math.sin(lt * 3 + i) * 30
        y = -50 + (R.uniform(0, 600) + lt * R.uniform(300, 600)) % (H + 100)
        col = R.choice([0xFFFFC23A, 0xFFFE2C55, 0xFF3AC8FF, 0xFF2FD46B, WHITE])
        c.save(); c.translate(x, y); c.rotate(lt * 200 + i * 40)
        c.drawRect(skia.Rect.MakeXYWH(-9, -5, 18, 10), fill(with_alpha(col, 0.9 * k)))
        c.restore()


def s_monte2(c, t, P, V):
    sid, lt = B.seg(P, t)
    B.sky(c, t)
    B.far_range(c, t)
    if sid == "h":
        top = B.mountain(c, FULL * OLD / N, t)
        B.flag(c, W / 2, top, t, f"{OLD} m")
    elif sid == "s1":
        # ayer vs hoy
        m = OLD + (N - OLD) * ease_in_out(clamp(lt / 1.4))
        top = B.mountain(c, FULL * m / N, t)
        B.flag(c, W / 2, top, t, f"{int(round(m))} m")
        if lt > 1.4:
            confetti(c, t, lt - 1.4)
        y_old = BASE_Y - FULL * OLD / N
        c.drawLine(140, y_old, W - 140, y_old, stroke(with_alpha(WHITE, 0.85), 5))
        K.tag(c, W - 230, y_old - 40, f"AYER · {OLD} m", lt - 0.3, accent=WHITE, size=32)
        hc.big(c, f"+{N - OLD}", W / 2, 1860, 130, GOLD, lt, 0.6)
    elif sid == "s2":
        top = B.mountain(c, FULL, t)
        B.flag(c, W / 2, top, t, f"{N} m")
        confetti(c, t, lt, 0.7)
        hc.big(c, "GRACIAS", W / 2, 1860, 130, GOLD, lt, 0.3)
    elif sid == "s3":
        # edificio de 20 plantas al lado (3 m por planta)
        top = B.mountain(c, FULL, t)
        B.flag(c, W / 2, top, t, f"{N} m")
        bh = FULL * 60 / N * ease_out(clamp(lt / 1.2))
        x = W - 250
        c.drawRect(skia.Rect.MakeXYWH(x, BASE_Y - bh, 150, bh), fill(0xFF2A3044))
        for fl in range(20):
            yy = BASE_Y - (fl + 1) * bh / 20
            for j in range(3):
                on = (fl * 3 + j) % 5 != 0
                c.drawRect(skia.Rect.MakeXYWH(x + 14 + j * 46, yy + 10, 30, max(2, bh / 20 - 20)), fill(0xFFFFD27A if on else 0xFF1A1E2A))
        K.tag(c, x + 75, BASE_Y + 70, "20 PLANTAS", lt - 1.0, accent=GOLD, size=32)
    elif sid == "s4":
        # el siguiente hito: 100 m con nieve (silueta fantasma)
        sc = FULL * GOAL / N
        k = ease_in_out(clamp(lt / 1.4))
        zoom = lerp(1.0, 0.62, k)
        c.save(); c.translate(W / 2, BASE_Y); c.scale(zoom, zoom); c.translate(-W / 2, -BASE_Y)
        gtop = BASE_Y - sc
        g = skia.Path(); g.moveTo(W / 2 - 180 - sc * 0.9, BASE_Y); g.lineTo(W / 2, gtop); g.lineTo(W / 2 + 180 + sc * 0.9, BASE_Y); g.close()
        c.drawPath(g, stroke(with_alpha(GOLD, 0.5 + 0.4 * math.sin(t * 5)), 8))
        sn = skia.Path(); sn.moveTo(W / 2, gtop); sn.lineTo(W / 2 + sc * 0.26, gtop + sc * 0.3); sn.lineTo(W / 2 - sc * 0.26, gtop + sc * 0.3); sn.close()
        c.drawPath(sn, fill(with_alpha(0xFFF4F6FF, 0.28)))
        top = B.mountain(c, FULL, t)
        B.flag(c, W / 2, top, t, f"{N} m")
        c.restore()
        hc.big(c, f"FALTAN {GOAL - N}", W / 2, 1860, 120, GOLD, lt, 0.4)
    else:
        top = B.mountain(c, FULL, t, ghost=1.0)
        B.flag(c, W / 2, top - 46, t, f"{N + 1} m")


V612 = dict(slug="612_montana_60m", accent=GOLD, drone=0.03, scene=s_monte2, tease="HA PASADO ALGO INCREÍBLE",
            send="ENVÍASELO A UN AMIGO PARA QUE SUME 1 METRO", rehook=("s4", "Y AHORA EL SIGUIENTE RETO"),
            reveal=("s4", "EL NUEVO RETO"), segs=[
    dict(id="h", who="nar", say=f"Anoche esta montaña medía {OLD} metros. Mirad cuánto mide ahora.",
         cap=f"Anoche medía *{OLD} m*… | mira cuánto mide *AHORA*", hold=0.6),
    dict(id="s1", who="nar", cut=True, say=f"{N} metros. En una sola noche, {N - OLD} personas nuevas os habéis sumado.",
         cap=f"*{N} METROS*. En una noche, | *{N - OLD} personas* | nuevas os habéis sumado"),
    dict(id="s2", who="nar", cut=True, say="Así que: gracias. De verdad. Cada metro de esta montaña es uno de vosotros.",
         cap="Así que: *GRACIAS*. | Cada metro | es uno de *vosotros*"),
    dict(id="s3", who="nar", cut=True, say="Ya es tan alta como un edificio de veinte plantas.",
         cap="Ya es como un edificio | de *20 PLANTAS*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say=f"Siguiente reto: cien metros. Ahí le pongo nieve en la cima. Faltan solo {GOAL - N}.",
         cap=f"Siguiente reto: *100 m* | y nieve en la cima. | Faltan solo *{GOAL - N}*"),
    dict(id="cta", who="nar", cut=True, say="Si todavía no me sigues, súbela tú un metro. Comenta: yo subo. Y mañana vemos si llegamos a cien.",
         cap="Súbela tú *1 METRO*: | comenta *YO SUBO* | y mañana, ¿llegamos a *100*?"),
])

if __name__ == "__main__":
    pv = "auto" if len(sys.argv) > 2 else None
    K.run(V612, lambda c, t, P: V612["scene"](c, t, P, V612), OUT, preview=pv)
