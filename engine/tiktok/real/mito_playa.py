import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run, skia
from core import W, H, WHITE, clamp, with_alpha, fill, stroke
RED = 0xFFFF2D3F; GOLD = 0xFFFFC23A; CYAN = 0xFF7DE8FF
V = dict(slug="1203_corte_digestion", accent=GOLD, drone=0.015, mood="luz", send="ENVÍASELO A QUIEN TE HIZO ESPERAR",
         rehook=("s2", "ENTONCES… ¿POR QUÉ SE DESMAYAN?"), segs=[
    dict(id="h", who="nar", say="¿Dos horas sin bañarte después de comer? Te engañaron.", cap="¿*2 HORAS* sin bañarte después de comer?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="En dos mil once, la Cruz Roja americana buscó pruebas. Ninguna relación entre comer y ahogarse. Lo llamó mito.",
         cap="*Cruz Roja* americana, 2011: | *ninguna* prueba. | Es un *MITO*", hold=0.5),
    dict(id="s2", who="nar", cut=True, say="Entonces, ¿por qué hay gente que se desmaya en el agua? Por el frío. Se llama hidrocución.",
         cap="¿Por qué se *desmayan*? | Por el *FRÍO*: | *hidrocución*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Al entrar de golpe en agua fría, tu corazón frena y la tensión cae. Y te puede pasar aunque no hayas comido.",
         cap="Agua fría de golpe: | tu *corazón frena*… | aunque no hayas *comido*", hold=0.2),
    dict(id="s4", who="nar", cut=True, say="Importa cómo entras: despacio, mojando pies, muñecas y nuca. Y tras una comilona con agua fría, más calma.",
         cap="Importa cómo *ENTRAS*: | pies, muñecas, *nuca*. | Comilona y agua fría: | *más calma*", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="¿A ti quién te lo decía? Comenta madre, o abuela.", cap="¿Quién te lo decía? | *MADRE* o *ABUELA*", hold=0.6),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; d = sg["b"] - sg["a"]
    if sid == "s1":
        K.tag(c, W / 2, 1730, "CRUZ ROJA AMERICANA, 2011", lt - 0.3, accent=GOLD, size=44)
        b = d - 1.9
        if lt > b:
            hc.stamp(c, "MITO", W / 2, 1010, lt - b, delay=0.0, size=170, col=RED)
    if sid == "s2":
        if lt > 2.8:
            K.tag(c, W / 2, 1730, "SEMES · URGENCIAS", lt - 2.8, accent=CYAN, size=44)
    if sid == "s3":
        # electro: el intervalo entre latidos se alarga como en la escena
        y0 = 1700; u = clamp(lt / d)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(90, y0 - 110, W - 180, 200), 24, 24), fill(with_alpha(0xFF04121C, 0.8)))
        pa = skia.Path(); first = True
        for x in range(110, W - 110, 3):
            xn = (x - 110) / (W - 220)
            lo = xn * 4 + t * 1.1
            per = 0.55 + 0.95 * u
            ph = (lo / per) % 1
            yy = -90 * math.exp(-((ph - .5) / .03) ** 2) + 28 * math.exp(-((ph - .56) / .03) ** 2)
            pa.moveTo(x, y0 + yy) if first else pa.lineTo(x, y0 + yy)
            first = False
        c.drawPath(pa, stroke(0xFF41F28C, 7))
    if sid == "s4":
        items = [("PIES", 0.9), ("MUÑECAS", 1.7), ("NUCA", 2.4)]
        for i, (txt, a) in enumerate(items):
            if lt > a:
                K.tag(c, W / 2, 1520 + i * 85, txt, lt - a, accent=CYAN, size=46)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "playa.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "playa.js", overlay=overlay)
