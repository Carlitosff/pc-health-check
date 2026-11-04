import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run, skia
from core import W, H, WHITE, clamp, with_alpha, fill, stroke, draw_text, ease_out
RED = 0xFFFF2D3F; GOLD = 0xFFFFC23A; CYAN = 0xFF7DE8FF
V = dict(slug="1204_si_la_tierra_frena", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 1", send="ENVÍASELO A UN AMIGO",
         rehook=("s3", "ESPERA… FALTA EL MAR"), segs=[
    dict(id="h", who="nar", say="Si la Tierra frenara de golpe, saldrías volando. Y no sería lo peor.", cap="Si la Tierra *FRENA*… *sales volando*", hold=0.1),
    dict(id="s1", who="nar", cut=True, say="Ahora mismo, en España, vas a unos mil doscientos setenta kilómetros por hora. No lo notas, porque el suelo y el aire van contigo.",
         cap="En España vas a | *1.270 km/h*. | Y no lo *notas*", hold=0.1),
    dict(id="s2", who="nar", cut=True, say="Pero si el suelo para, tú, los coches y el aire seguís a esa velocidad. Casi ningún edificio aguantaría.",
         cap="El suelo *PARA*… | y *TÚ NO* | Casi ningún *edificio* aguanta", hold=0.2),
    dict(id="s3", who="nar", cut=True, say="Y falta el mar. Los océanos se irían hacia los polos. Y en el ecuador, saldría tierra nueva.",
         cap="Los *océanos* | se van a los *POLOS*. | Tierra nueva en el *ecuador*", hold=0.2),
    dict(id="s4", who="nar", cut=True, say="Y un día duraría seis meses. Seis de sol, y seis de noche.", cap="Un *DÍA* duraría | *6 MESES*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Tranquilo, no va a pasar. Sígueme: en la parte dos, desaparece la Luna. Comenta qué pasaría.",
         cap="*Parte 2*: desaparece | la *LUNA*. | ¿Qué pasaría? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1":
        v = 1270 * ease_out(clamp((lt - .3) / 1.9))
        hc.big(c, f"{int(v):,}".replace(",", ".") + " km/h", W / 2, 1650, 110, WHITE, 1.0, 0.0, outline=14)
        K.tag(c, W / 2, 1770, "ECUADOR: 1.668 KM/H · ASTRONOMY", lt - 1.4, accent=GOLD, size=36)
    if sid == "s4":
        K.tag(c, W / 2, 1720, "SMITHSONIAN", lt - 0.8, accent=GOLD, size=40)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        v3d_run.run3d(V, "frena.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "frena.js", overlay=overlay)
