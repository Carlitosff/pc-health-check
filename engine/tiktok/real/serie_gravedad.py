"""1504 SERIE 3D (gravedad.js): ¿Y si se apaga la gravedad 5 segundos? Parte 4 de ¿QUÉ PASARÍA SI…?
Cálculo propio (física de primer orden): sin gravedad sigues en línea recta con la velocidad que te da el giro de la Tierra; respecto al suelo te separas ½·ω²·r·t² desde el eje.
Madrid 40,4° N: r = R·cos φ; v ≈ 1.270 km/h (ya usado en la Parte 1). En 5 s: ~32 cm desde el eje → ~25 cm hacia arriba y ~21 cm hacia el sur.
Estación Espacial (~420 km): su aceleración centrípeta es la gravedad local g·(R/(R+h))² ≈ 8,6 m/s² → ½·8,6·25 ≈ 108 m fuera de su órbita en 5 s."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE, clamp
GOLD = 0xFFFFC23A
R_ = 6.371e6; w = 7.2921e-5; phi = math.radians(40.4); T = 5
v = w * R_ * math.cos(phi) * 3.6; assert 1265 < v < 1275, v
dr = .5 * w ** 2 * R_ * math.cos(phi) * T ** 2
up = dr * math.cos(phi); south = dr * math.sin(phi); assert .23 < up < .27 and .19 < south < .23, (up, south)
g_iss = 9.81 * (R_ / (R_ + 420e3)) ** 2; iss = .5 * g_iss * T ** 2; assert 100 < iss < 115, iss
V = dict(slug="1504_gravedad_5_segundos", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 4", send="ENVÍASELO A QUIEN SE CREE QUE SALE VOLANDO",
         rehook=("s3", "ESPERA… MIRA LA ESTACIÓN ESPACIAL"), reveal=("s4", "CUÁNTO SUBES"), segs=[
    dict(id="h", who="nar", say="Se apaga la gravedad cinco segundos. Tú, aquí en Madrid, ¿cuánto subirías?", cap="Sin *GRAVEDAD* 5 segundos: ¿cuánto subes?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="La Tierra gira y te lleva a unos mil doscientos setenta kilómetros por hora. Sin gravedad, sigues recto y el suelo se curva.", cap="La Tierra te lleva | a *1.270 km/h*. | Sin gravedad, *sigues recto*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Ahora cuenta conmigo cinco segundos, y mira cuánto te separas del suelo.", cap="*5 segundos* | sin gravedad…", hold=1.0),
    dict(id="s3", who="nar", cut=True, say="La Estación Espacial ni lo notaría, pero se saldría más de cien metros de su órbita.", cap="La *Estación Espacial*: | *más de 100 metros* | fuera de su órbita", hold=0.2),
    dict(id="s4", who="nar", cut=True, say="En Madrid subirías solo unos veinticinco centímetros. Luego vuelve la gravedad, y todo cae de golpe.", cap="En Madrid: | solo *25 cm*. | Y luego… *TODO CAE*", hold=0.8),
    dict(id="cta", who="nar", cut=True, say="Sígueme, que en la parte cinco la Tierra tiene anillos como Saturno. Comenta cuánto creías que subirías.", cap="*Parte 5*: la Tierra | con *anillos*. | ¿Cuánto creías? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; d = sg["b"] - sg["a"]
    if sid == "s2":
        n = max(1, 5 - int(lt / max(.1, d) * 5))
        hc.big(c, str(n), W * .78, 1060, 200, GOLD, 1.0, 0.0, outline=14)
    if sid == "s3":
        K.tag(c, W / 2, 1770, "CÁLCULO PROPIO · ~420 KM DE ALTURA", lt - 1.0, accent=GOLD, size=34)
    if sid == "s4":
        K.tag(c, W / 2, 1770, "CÁLCULO PROPIO · Y ~21 CM HACIA EL SUR", lt - 1.4, accent=GOLD, size=34)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "gravedad.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "gravedad.js", overlay=overlay)
