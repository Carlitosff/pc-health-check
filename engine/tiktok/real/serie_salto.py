"""1404 SERIE 3D (isla.js): ¿Y si saltamos todos a la vez? Parte 3 de ¿QUÉ PASARÍA SI…?
Fuentes: Randall Munroe, What If? nº 8 'Everybody Jump' (Tierra: menos que el ancho de un átomo; nos supera en más de 10 billones de veces; idea de reunir a todos, él en Rhode Island).
Propio: Mallorca 3.640 km² (8.200 M / 3.640 km² = 2,25 personas/m²). Aena 13/01/2026: PMI 33.806.427 pasajeros en 2025 (el dato cuenta llegadas y salidas, así que salen ≈16,9 M/año: 8.200 / 16,9 = 485 años)."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE, clamp
GOLD = 0xFFFFC23A
YEARS = 8.2e9 / (33806427 / 2); assert 480 < YEARS < 490
assert 2.2 < 8.2e9 / 3640e6 < 2.3
V = dict(slug="1404_todos_saltan_mallorca", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 3", send="ENVÍASELO A QUIEN IRÍA CONTIGO",
         rehook=("s3", "ESPERA… LO PEOR ES VOLVER"), reveal=("s4", "LOS AÑOS DE COLA"), segs=[
    dict(id="h", who="nar", say="Hoy metemos a toda la humanidad en Mallorca, y saltamos todos a la vez.", cap="*TODA la humanidad* en Mallorca, saltando a la vez", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Aunque no lo parezca, cabemos de pie, a unas dos personas por metro cuadrado.", cap="*8.200 millones* | caben de pie: | *2 por metro cuadrado*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="A la de tres saltamos todos, y la Tierra se mueve menos que el ancho de un átomo.", cap="¡*SALTAMOS*! | La Tierra se mueve | *menos que un átomo*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero lo peor no es el salto, lo peor es volver a casa.", cap="Lo peor es | *VOLVER A CASA*", hold=0.2),
    dict(id="s4", who="nar", cut=True, say="El aeropuerto de Palma mueve casi treinta y cuatro millones de pasajeros al año. A ese ritmo, sacarnos a todos costaría casi quinientos años.", cap="*33,8 millones* de pasajeros al año. | Para sacarnos a todos: | *CASI 500 AÑOS*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Sígueme, que en la parte cuatro se apaga la gravedad. Y comenta con quién no harías esa cola.", cap="*Parte 4*: se apaga | la *gravedad*. | ¿Con quién *NO* harías la cola?"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "h":
        K.tag(c, W / 2, 1770, "CÁLCULO PROPIO · IDEA: RANDALL MUNROE, WHAT IF?", lt - 1.2, accent=GOLD, size=30)
    if sid == "s1":
        K.tag(c, W / 2, 1770, "ESTO ES 1 METRO CUADRADO", lt - 2.2, accent=GOLD, size=46)
    if sid == "s4":
        y = YEARS * K.smooth(clamp((lt - 3.2) / 4.5))
        if lt > 3.2:
            hc.big(c, f"{int(y)} AÑOS", W / 2, 1600, 118, GOLD, 1.0, 0.0, outline=12)
        K.tag(c, W / 2, 1770, "AENA 2025 · SALE LA MITAD · CÁLCULO PROPIO", lt - 3.0, accent=WHITE, size=30)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "isla.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "isla.js", overlay=overlay)
