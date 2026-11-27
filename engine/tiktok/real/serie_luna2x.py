"""3504 SERIE 3D (luna2x.js): ¿Y si la Luna estuviera el doble de cerca? Parte 24 de ¿QUÉ PASARÍA SI…? (prometida en la 23).
Distancia media ~384.400 km y alejamiento ~3,8 cm al año medido con láser en los retrorreflectores de Apolo 11, 14 y 15 y Lunojod 1 y 2
(Royal Museums Greenwich, 'How far away is the Moon?'; Space.com 01/03/2012: 'The average distance is around 384,400 kilometers', 'about 3.8 centimeters per year').
Cálculo propio: a la mitad de distancia → tamaño aparente ×2, área ×4 → luz de la luna llena ×4 (∝ 1/d²); fuerza de marea ∝ 1/d³ → ×8.
'Hace muchísimo tiempo estaba más cerca' se sigue del alejamiento medido (cualitativo, sin cifra). Parte 25 prometida: un día de 48 horas."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; CYAN = 0xFF8FD0FF; RED = 0xFFFF6A4A; GREEN = 0xFF4ADE80
assert 384400 / 2 == 192200 and 2 ** 2 == 4 and 2 ** 3 == 8
V = dict(slug="3504_luna_doble_de_cerca", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 24",
         send="ENVÍASELO A QUIEN LE GUSTA LA LUNA", dare=("s1", "PREGÚNTALE SI LA QUERRÍA ASÍ", 1840),
         rehook=("s2", "ESPERA… LO SERIO SON LAS MAREAS"), reveal=("s2", "LAS MAREAS"), segs=[
    dict(id="h", who="nar", say="¿Y si esta noche la Luna estuviera el doble de cerca? Mírala salir sobre el puerto.",
         cap="¿La Luna *EL DOBLE DE CERCA*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Ahora está a unos trescientos ochenta y cuatro mil kilómetros. A la mitad, la verías el doble de ancha y con cuatro veces más luz.",
         cap="El doble de ancha, | *CUATRO VECES MÁS LUZ*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Pero lo serio serían las mareas, porque la fuerza que las levanta sería ocho veces mayor.",
         cap="Mareas con | *OCHO VECES MÁS FUERZA*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y la Luna se mueve de verdad: se aleja unos tres coma ocho centímetros al año, medido con láser.",
         cap="Se aleja *3,8 cm al año*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Así que hace muchísimo tiempo estaba más cerca, y las mareas eran mucho más fuertes.",
         cap="Antes estaba | *MÁS CERCA*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta si la querrías así de grande. En la parte veinticinco, el día dura cuarenta y ocho horas.",
         cap="¿La querrías así? *COMENTA* | Parte 25: *UN DÍA DE 48 HORAS*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 1.0:
        k = K.prog(lt, 2.4, 4.6)
        km = int(round((384400 - 192200 * k) / 100.0)) * 100
        K.pill(c, W / 2, 1580, f"{km:,} km".replace(",", "."), 52, bg=0xEE000000, fg=GOLD if k < 1 else GREEN, scale=K.ease_back(K.prog(lt, 1.0, 1.3)))
    if sid == "s2" and lt > 2.0:
        K.pill(c, W / 2, 1580, "MITAD DE DISTANCIA → ×8 FUERZA DE MAREA", 40, bg=0xEE000000, fg=CYAN, scale=K.ease_back(K.prog(lt, 2.0, 2.3)))
    if sid == "s3" and lt > 2.0:
        K.pill(c, W / 2, 1580, "+3,8 cm CADA AÑO", 52, bg=0xEE000000, fg=GREEN, scale=K.ease_back(K.prog(lt, 2.0, 2.3)))
        K.tag(c, W / 2, 1840, "LÁSER EN LOS ESPEJOS DEL APOLO · RMG", lt - 2.0, accent=WHITE, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1), {k: round(v[0], 1) for k, v in K.plan(V)["tl"].items()})
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "luna2x.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "luna2x.js", overlay=overlay, keep=True)
