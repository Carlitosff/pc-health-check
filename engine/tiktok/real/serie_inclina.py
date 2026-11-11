"""1904 SERIE 3D (inclina.js): ¿Y si la Tierra se queda sin inclinación? Parte 8 de ¿QUÉ PASARÍA SI…? (prometida en la parte 7).
Oblicuidad de la eclíptica ≈ 23,44° (NASA / IAU). Madrid, latitud 40,4° N. Cálculo propio (sin refracción ni tamaño del disco solar):
altura del sol a mediodía = 90 − φ + δ → junio (δ = +23,44) 73,0°; diciembre (δ = −23,44) 26,2°; equinoccio / sin inclinación (δ = 0) 49,6° todos los días.
Duración del día: cos H = −tan φ · tan δ → junio ≈ 14,9 h, diciembre ≈ 9,1 h (con refracción, ~15,1 h y ~9,3 h); con δ = 0, H = 90° → 12 h en
cualquier latitud (salvo los polos, donde el sol queda en el horizonte y da la vuelta). El guion dice 'unos cincuenta grados', '12 horas'."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
phi, eps = 40.4, 23.44
alt = lambda d: 90 - phi + d
jun, dic, eq = alt(eps), alt(-eps), alt(0)
assert round(jun) == 73 and round(dic) == 26 and 49 < eq < 50, (jun, dic, eq)
dayh = lambda d: 2 * math.degrees(math.acos(-math.tan(math.radians(phi)) * math.tan(math.radians(d)))) / 15
assert 14.7 < dayh(eps) < 15.1 and 8.9 < dayh(-eps) < 9.3 and abs(dayh(0) - 12) < 1e-9
V = dict(slug="1904_tierra_sin_inclinacion", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 8", send="ENVÍASELO A QUIEN ODIA EL INVIERNO",
         rehook=("s3", "ESPERA… LA ENDEREZAMOS"), reveal=("s4", "CUÁNTO DURA EL DÍA"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra se quedara sin inclinación? Se acabarían el verano y el invierno.", cap="¿Y si la Tierra se *ENDEREZA*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Hoy su eje está inclinado veintitrés grados y medio, y por eso tenemos estaciones.", cap="Hoy está inclinada | *23,5 grados*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="En Madrid, el sol de mediodía sube a setenta y tres grados en junio, y solo a veintiséis en diciembre.",
         cap="Madrid: | *73°* en junio, | *26°* en diciembre", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Con el eje recto, subiría siempre a unos cincuenta grados, como en marzo, todos los días del año.",
         cap="Sin inclinación: | *50°* | *TODO EL AÑO*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y el día duraría doce horas en todo el planeta, mientras en los polos el sol daría vueltas pegado al horizonte.",
         cap="*12 horas* de día | en todo el planeta", hold=0.45),
    dict(id="cta", who="nar", cut=True, say="Sígueme, que en la parte nueve la Tierra se acerca al Sol. Comenta si echarías de menos el verano.",
         cap="*Parte 9*: | más cerca del *Sol*. | ¿Y el verano? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid in ("s2", "s3") and lt > 1.0:
        K.tag(c, W / 2, 1790, "ALTURA DEL SOL A MEDIODÍA · MADRID", lt - 1.0, accent=GOLD, size=34)
    if sid == "s4" and lt > 2.0:
        K.tag(c, W / 2, 1840, "CÁLCULO PROPIO", lt - 2.0, accent=WHITE, size=28)


JOB = dict(alt=dict(jun=round(jun, 1), dic=round(dic, 1), eq=round(eq, 1)))
if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "inclina.js", stills=sys.argv[2].split(","), extra_job=JOB)
    else:
        v3d_run.run3d(V, "inclina.js", overlay=overlay, extra_job=JOB)
