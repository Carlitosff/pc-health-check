"""2104 SERIE 3D (lejos.js): ¿Y si la Tierra se aleja del Sol? Parte 10 de ¿QUÉ PASARÍA SI…? (prometida en la parte 9).
Flujo ∝ 1/d²: 10 % más lejos → 1/1,1² = 0,826 → −17 % ('casi una quinta parte menos', cálculo propio). Marte a 1,524 UA → 0,43 (43 %).
Temperatura de equilibrio ∝ 1/√d: 255 K → 255/√1,524 ≈ 207 K, unos −48 °C (cálculo propio; 'con el aire de hoy' = sin más invernadero).
Kopparapu et al., ApJ 765:131 (2013), resumen en vpl.uw.edu: 'the water-loss (inner HZ) and maximum greenhouse (outer HZ) limits for our solar
system are at 0.99 and 1.70 AU, respectively, suggesting that the present Earth lies near the inner edge'."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; ICE = 0xFF4DE3FF
f10 = 1 / 1.1 ** 2; fm = 1 / 1.524 ** 2; dT = 255 - 255 / 1.524 ** .5
assert round((1 - f10) * 100) == 17 and round(fm * 100) == 43 and 47 < dT < 49
V = dict(slug="2104_tierra_se_aleja_del_sol", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 10", send="ENVÍASELO A QUIEN SIEMPRE TIENE FRÍO",
         rehook=("s3", "ESPERA… EL LÍMITE"), reveal=("s4", "LO MÁS RARO"), segs=[
    dict(id="h", who="nar", say="¿Y si alejamos la Tierra del Sol? Mira hasta dónde podríamos llegar.", cap="¿Y si la Tierra *SE ALEJA* del Sol?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Si nos alejamos solo un diez por ciento, nos llega casi una quinta parte menos de luz.",
         cap="*10 %* más lejos: | *−17 %* de luz", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="A la distancia de Marte llega menos de la mitad de luz, y con el aire de hoy los mares serían hielo.",
         cap="Distancia de Marte: | *43 %* de luz: | mares de *HIELO*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Un estudio de dos mil trece puso el límite en uno coma siete veces la distancia de hoy: más lejos, ni con todo el efecto invernadero hay agua líquida.",
         cap="El límite: | *1,7 veces* | la distancia de hoy", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Lo curioso es que estamos pegados al borde caliente, así que alejarnos un poco sería más seguro que acercarnos.",
         cap="Estamos *pegados* | al *BORDE CALIENTE*", hold=0.45),
    dict(id="cta", who="nar", cut=True, say="Sígueme, que en la parte once la Tierra tiene dos soles. Comenta frío o calor.",
         cap="*Parte 11*: | *dos soles*. | ¿FRÍO o CALOR? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 2.0:
        K.tag(c, W / 2, 1840, "LA LUZ BAJA CON 1 / DISTANCIA² · CÁLCULO PROPIO", lt - 2.0, accent=WHITE, size=28)
    if sid == "s2" and lt > 2.4:
        K.tag(c, W / 2, 1840, "UNOS −48 °C DE EQUILIBRIO · CÁLCULO PROPIO", lt - 2.4, accent=ICE, size=28)
    if sid == "s3" and lt > 2.0:
        K.tag(c, W / 2, 1840, "KOPPARAPU ET AL. · ASTROPHYSICAL JOURNAL 2013", lt - 2.0, accent=WHITE, size=28)
    if sid == "s4" and lt > 1.6:
        K.tag(c, W / 2, 1840, "ZONA HABITABLE: 0,99 A 1,70 VECES LA DISTANCIA", lt - 1.6, accent=0xFF4ADE80, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "lejos.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "lejos.js", overlay=overlay)
