"""LA MONTAÑA DE LA COMUNIDAD — generador reutilizable (1 seguidor = 1 metro).
Uso: python3 montana.py <seguidores_antes> <seguidores_ahora> [slug] [prev]
Es el formato que más seguidores ha traído (611: +35 en una noche; 612: 60 m). La producción diaria lo genera cada día
con los seguidores REALES de Metricool (IGEV01) y lo programa en la franja de noche.
Hitos: 100 m = nieve en la cima; luego 250, 500, 1.000, 2.000, 5.000 y Everest 8.849."""
import math, sys, random
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
import dia_20261031b as B
from core import W, H, WHITE, clamp, lerp, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, draw_text

OUT = "/home/claude/tiktok/outdaily"
OLD = int(sys.argv[1]) if len(sys.argv) > 1 else 60
N = int(sys.argv[2]) if len(sys.argv) > 2 else 90
SLUG = sys.argv[3] if len(sys.argv) > 3 else f"montana_{N}m"
GOALS = [100, 250, 500, 1000, 2000, 5000, 8849]
GOAL = next(g for g in GOALS if g > N)
GOLD = B.GOLD
BASE_Y = B.BASE_Y
FULL = 980
SNOW = N >= 100


def num(n):
    return f"{n:,}".replace(",", ".")


def confetti(c, lt, k=1.0, seed=12):
    R = random.Random(seed)
    for i in range(170):
        x = R.uniform(0, W) + math.sin(lt * 3 + i) * 30
        y = -50 + (R.uniform(0, 700) + lt * R.uniform(300, 650)) % (H + 100)
        col = R.choice([0xFFFFC23A, 0xFFFE2C55, 0xFF3AC8FF, 0xFF2FD46B, WHITE])
        c.save(); c.translate(x, y); c.rotate(lt * 220 + i * 40)
        c.drawRect(skia.Rect.MakeXYWH(-10, -5, 20, 10), fill(with_alpha(col, 0.9 * k)))
        c.restore()


def fireworks(c, lt, seed=3):
    R = random.Random(seed)
    for b in range(5):
        t0 = b * 0.45
        x, y = R.uniform(180, W - 180), R.uniform(380, 900)
        col = R.choice([0xFFFFC23A, 0xFFFE2C55, 0xFF3AC8FF, 0xFF9AF07A])
        tt = lt - t0
        if tt < 0 or tt > 1.6:
            continue
        if tt < 0.35:  # cohete subiendo
            yy = lerp(1700, y, ease_out(tt / 0.35))
            c.drawCircle(x, yy, 7, fill(WHITE))
            continue
        k = ease_out((tt - 0.35) / 1.25)
        for j in range(26):
            a = j / 26 * 6.283
            r = 230 * k
            px, py = x + math.cos(a) * r, y + math.sin(a) * r + 60 * k * k
            c.drawCircle(px, py, 7 * (1 - k) + 2, skia.Paint(AntiAlias=True, Color=with_alpha(col, 1 - k),
                                                                MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 3)))


def clouds_mid(c, t, y, k=1.0):
    """Nubes que pasan por DELANTE de la montaña: da escala (ya es alta)."""
    for i in range(4):
        x = (i * 380 + t * (60 + i * 15)) % (W + 700) - 350
        for j in range(6):
            c.drawOval(skia.Rect.MakeXYWH(x + j * 60 - 150, y + i * 40 - (j % 3) * 22, 240, 90),
                       skia.Paint(AntiAlias=True, Color=with_alpha(0xFFFFE6DA, 0.18 * k),
                                  MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22)))


def scene(c, t, P, V):
    sid, lt = B.seg(P, t)
    B.sky(c, t)
    B.far_range(c, t)
    if sid == "h":
        top = B.mountain(c, FULL * OLD / N, t, snow=0.0)
        B.flag(c, W / 2, top, t, f"{num(OLD)} m")
    elif sid == "s1":
        m = OLD + (N - OLD) * ease_in_out(clamp(lt / 1.6))
        # temblor de 'crecimiento' mientras sube
        sh = math.sin(lt * 60) * 6 * (1 - clamp(lt / 1.6))
        c.save(); c.translate(sh, 0)
        top = B.mountain(c, FULL * m / N, t)
        c.restore()
        B.flag(c, W / 2 + sh, top, t, f"{int(round(m))} m")
        y_old = BASE_Y - FULL * OLD / N
        c.drawLine(140, y_old, W - 140, y_old, stroke(with_alpha(WHITE, 0.85), 5))
        K.tag(c, W - 240, y_old - 40, f"ANTES · {num(OLD)} m", lt - 0.3, accent=WHITE, size=32)
        if lt > 1.6:
            confetti(c, lt - 1.6)
        hc.big(c, f"+{num(N - OLD)}", W / 2, 1860, 140, GOLD, lt, 0.8)
    elif sid == "s2":
        top = B.mountain(c, FULL, t)
        clouds_mid(c, t, top + 220)
        B.flag(c, W / 2, top, t, f"{num(N)} m")
        fireworks(c, lt)
        hc.big(c, "GRACIAS", W / 2, 1860, 140, GOLD, lt, 0.3)
    elif sid == "s3":
        top = B.mountain(c, FULL, t)
        B.flag(c, W / 2, top, t, f"{num(N)} m")
        floors = max(1, round(N / 3))
        bh = FULL * (floors * 3) / N * ease_out(clamp(lt / 1.2))
        x = W - 240
        c.drawRect(skia.Rect.MakeXYWH(x, BASE_Y - bh, 140, bh), fill(0xFF2A3044))
        nf = min(floors, 40)
        for fl in range(nf):
            yy = BASE_Y - (fl + 1) * bh / nf
            for j in range(3):
                on = (fl * 3 + j) % 5 != 0
                c.drawRect(skia.Rect.MakeXYWH(x + 12 + j * 44, yy + 6, 28, max(2, bh / nf - 12)), fill(0xFFFFD27A if on else 0xFF1A1E2A))
        K.tag(c, x + 70, BASE_Y + 70, f"{floors} PLANTAS", lt - 1.0, accent=GOLD, size=32)
    elif sid == "s4":
        sc = FULL * GOAL / N
        k = ease_in_out(clamp(lt / 1.4))
        zoom = lerp(1.0, min(1.0, 0.9 * FULL / sc + 0.05), k)
        c.save(); c.translate(W / 2, BASE_Y); c.scale(zoom, zoom); c.translate(-W / 2, -BASE_Y)
        gtop = BASE_Y - sc
        g = skia.Path(); g.moveTo(W / 2 - 180 - sc * 0.9, BASE_Y); g.lineTo(W / 2, gtop); g.lineTo(W / 2 + 180 + sc * 0.9, BASE_Y); g.close()
        c.drawPath(g, stroke(with_alpha(GOLD, 0.5 + 0.4 * math.sin(t * 5)), 8 / max(zoom, 0.2)))
        sn = skia.Path(); sn.moveTo(W / 2, gtop); sn.lineTo(W / 2 + sc * 0.26, gtop + sc * 0.3); sn.lineTo(W / 2 - sc * 0.26, gtop + sc * 0.3); sn.close()
        c.drawPath(sn, fill(with_alpha(0xFFF4F6FF, 0.5 + 0.2 * math.sin(t * 4))))
        top = B.mountain(c, FULL, t)
        B.flag(c, W / 2, top, t, f"{num(N)} m")
        c.restore()
        hc.big(c, f"FALTAN {num(GOAL - N)}", W / 2, 1860, 130, GOLD, lt, 0.4)
    else:
        top = B.mountain(c, FULL, t, ghost=1.0)
        B.flag(c, W / 2, top - 46, t, f"{num(N + 1)} m")


def goal_line():
    if GOAL == 100:
        return "cien metros, y ahí le pongo nieve en la cima", "*100 m* = *NIEVE* en la cima"
    if GOAL == 8849:
        return "la altura del Everest", "el *EVEREST*"
    return f"{num(GOAL)} metros", f"*{num(GOAL)} m*"


gsay, gcap = goal_line()
close = GOAL - N <= max(15, N // 5)
V = dict(slug=SLUG, accent=GOLD, drone=0.03, scene=scene, tease="LO HABÉIS VUELTO A HACER", mood="epico",
         send="ENVÍASELO A UN AMIGO PARA QUE SUME 1 METRO", rehook=("s4", "Y AHORA EL SIGUIENTE RETO"),
         reveal=("s4", "EL NUEVO RETO"), segs=[
    dict(id="h", who="nar", say=f"Esta montaña medía {OLD} metros. Uno por cada persona que me sigue. Mira lo que habéis hecho.",
         cap=f"Medía *{num(OLD)} metros*… | mira lo que | habéis *HECHO*", hold=0.4),
    dict(id="s1", who="nar", cut=True, say=f"¡{N} metros! {N - OLD} personas nuevas. Otra vez.",
         cap=f"¡*{num(N)} METROS*! | *{num(N - OLD)}* personas nuevas. | Otra vez"),
    dict(id="s2", who="nar", cut=True, say="Gracias. De verdad. Cada metro de esta montaña tiene vuestro nombre.",
         cap="*GRACIAS*. Cada metro | tiene *vuestro nombre*"),
    dict(id="s3", who="nar", cut=True, say=f"Ya es más alta que un edificio de {round(N / 3)} plantas. Y ya toca las nubes.",
         cap=f"Ya es como un edificio | de *{round(N / 3)} PLANTAS*… | y toca las *nubes*", hold=0.2),
    dict(id="s4", who="nar", cut=True,
         say=(f"Siguiente reto: {gsay}. Faltan solo {GOAL - N}. Esto lo sacamos esta misma noche." if close
              else f"Siguiente reto: {gsay}. Faltan {GOAL - N}. Vamos a por ello."),
         cap=f"Siguiente reto: {gcap}. | Faltan solo *{num(GOAL - N)}*"),
    dict(id="cta", who="nar", cut=True, say="Si aún no me sigues, el siguiente metro eres tú. Comenta: yo subo. Y mañana vemos cuánto ha crecido.",
         cap="El siguiente metro | eres *TÚ*: comenta *YO SUBO* | y mañana lo vemos"),
])

if __name__ == "__main__":
    pv = "auto" if (len(sys.argv) > 4 and sys.argv[4] == "prev") else None
    K.run(V, lambda c, t, P: V["scene"](c, t, P, V), OUT, preview=pv)
