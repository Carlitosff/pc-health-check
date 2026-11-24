"""3204 SERIE 3D (reves.js): ¿Y si la Tierra girara al revés? Parte 21 de ¿QUÉ PASARÍA SI…? (prometida en la 20).
Mikolajewicz et al., 'The climate of a retrograde rotating earth', Earth System Dynamics 9, 1191–1215, 2018 (Max Planck de Meteorología,
nota del 19/10/2018): 'the Sahara and the Arabian Desert green', 'Southern Brazil and Argentina become the Earth's biggest deserts and the
southern states of the USA see a dramatic climate shift ... towards a complete aridification', 'the direction of the ocean gyres reverses',
'the reversal of the prevailing wind directions', 'a significant cooling over Europe'. Eos (Bas den Hond, 10/04/2018): '7,000 years' de
calendario del modelo, 'reversed the daily path of the Sun', 'severe winters to western Europe', 'the Sahara Desert was gone'.
El guion dice 'miles de años de clima' y que el Sol saldría por el oeste (consecuencia directa de girar al revés)."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; GREEN = 0xFF4FD46B; SAND = 0xFFE8B86A
V = dict(slug="3204_tierra_gira_al_reves", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 21",
         send="ENVÍASELO A QUIEN SE QUEJA DEL CALOR", dare=("s3", "PREGÚNTALE DÓNDE VIVIRÍA", 1840),
         rehook=("s3", "ESPERA… MIRA EL SÁHARA"), reveal=("s4", "LOS NUEVOS DESIERTOS"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra girara al revés? El Sol saldría por el oeste, y el Sáhara se volvería verde.",
         cap="¿Y si la Tierra gira *AL REVÉS*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Un equipo del Max Planck lo simuló en un superordenador, con miles de años de clima.",
         cap="Simulado por | *MAX PLANCK*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Los vientos y las corrientes del océano cambiarían de sentido, y Europa tendría inviernos durísimos.",
         cap="Europa: | *INVIERNOS DUROS*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero lo más loco pasa en África: el Sáhara dejaría de ser un desierto, y se llenaría de verde.",
         cap="El Sáhara: | *VERDE*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="A cambio, el sur de Estados Unidos, Brasil y Argentina se convertirían en los nuevos desiertos.",
         cap="Nuevos desiertos: | *AMÉRICA*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta dónde vivirías tú. En la parte veintidós, la Tierra tiene dos lunas.",
         cap="¿Dónde vivirías? *COMENTA* | Parte 22: *DOS LUNAS*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 1.5:
        K.tag(c, W / 2, 1840, "MIKOLAJEWICZ ET AL. · EARTH SYST. DYNAM. · 2018", lt - 1.5, accent=WHITE, size=28)
    if sid == "s3" and lt > 3.3:
        K.tag(c, W / 2, 1840, "SIMULACIÓN DEL MAX PLANCK · 7.000 AÑOS DE MODELO", lt - 3.3, accent=GREEN, size=28)
    if sid in ("s3", "s4") and lt > 0.6:
        txt, col = ("SÁHARA", GREEN) if sid == "s3" else ("NUEVO DESIERTO", SAND)
        K.pill(c, W / 2, 1560, txt, 58, bg=0xEE0B0D14, fg=col, scale=K.ease_back(K.prog(lt, 0.6, 0.9)))
    if sid == "s4" and lt > 1.2:
        K.tag(c, W / 2, 1840, "SUR DE EE. UU. · BRASIL · ARGENTINA", lt - 1.2, accent=SAND, size=32)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "reves.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "reves.js", overlay=overlay, keep=True)
