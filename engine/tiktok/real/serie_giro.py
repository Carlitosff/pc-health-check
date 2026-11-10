"""1804 SERIE 3D (giro.js): ¿Y si la Tierra gira cada vez más deprisa? Parte 7 de ¿QUÉ PASARÍA SI…? (prometida en la parte 6).
Cálculo propio (Tierra rígida, sin deformarse): en el ecuador el giro 'quita' peso a = ω²·R. Hoy (día sidéreo 86.164 s, R = 6.378 km) ≈ 0,035 m/s² = 0,35 % de g
→ a una persona de 80 kg, ~280 g. Con un día de 6 h, ω ×4 → ×16 → ~4,4 kg. Se pesa cero cuando ω²·R = g_grav (9,814 m/s² en el ecuador sin el giro):
T = 2π·√(R/g) ≈ 5.065 s ≈ 1 h 24 min, y entonces el ecuador va a 2πR/T ≈ 28.500 km/h, del orden de la Estación Espacial (~28.000 km/h, ya usado el 27/10).
Velocidad del ecuador hoy: 1.670 km/h (Astronomy feb 2026 daba 1.668, usado el 04/11)."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE, clamp
GOLD = 0xFFFFC23A
R_, g0, Tsid = 6.378e6, 9.814, 86164
w = 2 * math.pi / Tsid
v_eq = w * R_ * 3.6; assert 1665 < v_eq < 1675, v_eq
f_now = w ** 2 * R_ / g0; assert .0033 < f_now < .0036, f_now
loss_now = 80 * f_now; assert .26 < loss_now < .29, loss_now
w6 = 2 * math.pi / (6 * 3600); loss6 = 80 * w6 ** 2 * R_ / g0 * (Tsid / 86400) ** 0; assert 4.2 < loss6 < 4.6, loss6
T0 = 2 * math.pi * math.sqrt(R_ / g0); assert 5000 < T0 < 5100, T0  # ≈ 1 h 24 min
v0 = 2 * math.pi * R_ / T0 * 3.6; assert 28_000 < v0 < 29_000, v0
READ = dict(s2=round(80 - loss_now, 2), s3=round(80 - loss6, 1), s4=0)
V = dict(slug="1804_tierra_gira_mas_deprisa", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 7", send="ENVÍASELO A QUIEN QUIERA PESAR MENOS",
         rehook=("s3", "ESPERA… AHORA MÁS DEPRISA"), reveal=("s4", "CUÁNTO PESAS"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra girara cada vez más deprisa? Mira esta báscula.", cap="¿Y si la Tierra gira *MÁS DEPRISA*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Hoy, en el ecuador, ya vas a mil seiscientos setenta kilómetros por hora sin notarlo.",
         cap="Hoy, en el *ecuador*, | vas a *1.670 km/h*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Y ese giro ya te quita unos doscientos ochenta gramos, si pesas ochenta kilos.",
         cap="El giro ya te quita | unos *280 gramos*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Con un día de solo seis horas, perderías más de cuatro kilos.",
         cap="Día de *6 horas*: | *−4 kilos*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y con un día de una hora y veinticuatro minutos, irías a veintiocho mil kilómetros por hora, y no pesarías nada.",
         cap="Día de *1 h 24 min*: | *0 kilos*. | Sales *FLOTANDO*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Sígueme, que en la parte ocho la Tierra se queda sin inclinación. Comenta cuántas horas querrías que durara el día.",
         cap="*Parte 8*: la Tierra | *sin inclinación*. | ¿Cuántas horas? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    lab = {"s2": "DÍA DE 24 h", "s3": "DÍA DE 6 h", "s4": "DÍA DE 1 h 24 min · 28.500 km/h"}.get(sid)
    if lab and lt > .8:
        K.tag(c, W / 2, 1760, lab, lt - .8, accent=GOLD, size=40)
    if sid in ("s3", "s4") and lt > 2.4:
        K.tag(c, W / 2, 1840, "CÁLCULO PROPIO · EN EL ECUADOR", lt - 2.4, accent=WHITE, size=26)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "giro.js", stills=sys.argv[2].split(","), extra_job=dict(read=READ))
    else:
        v3d_run.run3d(V, "giro.js", overlay=overlay, extra_job=dict(read=READ))
