"""2403 MITO 3D (mosquito.js): '¿a ti te pican más porque tienes la sangre dulce?' → no hay pruebas; es el olor de tu piel.
Rockefeller University, 18/10/2022 ('Why some people are mosquito magnets'), sobre De Obaldia, Morita, …, Vosshall, Cell (doi 10.1016/j.cell.2022.09.034),
'Differential Mosquito Attraction to Humans is Associated with Skin-Derived Carboxylic Acid Levels': 'eight participants', medias de nailon en el antebrazo
'for six hours a day', olfatómetro de dos tubos ('a plexiglass chamber divided into two tubes, each ending in a box that held a stocking'), estudio de tres años;
Subject 33 'four times more attractive… than the next most-attractive' y '100 times more appealing than the least attractive, Subject 19';
'mosquito magnets produced carboxylic acids at much higher levels' ('in the sebum'); 'if they were a mosquito magnet, they remained a mosquito magnet'.
Sangre dulce: 'Blood type, blood sugar level… are all popular theories' y 'for most of them, there is little credible data'."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; RED = 0xFFFF3A4A
V = dict(slug="2403_mito_sangre_dulce_mosquitos", accent=GOLD, drone=0.03, mood="misterio", badge=None, send="ENVÍASELO A QUIEN SIEMPRE LE PICAN",
         rehook=("s3", "ESPERA… MIRA LA GANADORA"), reveal=("s4", "EL MOTIVO"), segs=[
    dict(id="h", who="nar", say="¿A ti te pican más los mosquitos? Te dirán que tienes la sangre dulce, pero no es eso.",
         cap="¿A ti te pican *MÁS* los mosquitos?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Lo de la sangre dulce no tiene pruebas serias, así que en Nueva York lo midieron de verdad.",
         cap="¿Sangre dulce? | *SIN PRUEBAS*", hold=0.15),
    dict(id="s2", who="nar", cut=True, say="Ocho personas llevaron medias de nailon en el brazo, y los mosquitos elegían entre dos medias, durante tres años.",
         cap="*8 personas* · medias de nailon | *3 años*", hold=0.15),
    dict(id="s3", who="nar", cut=True, say="La persona número treinta y tres atraía cien veces más mosquitos que la que menos.",
         cap="La nº 33: | *×100*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="La diferencia estaba en unos ácidos de la grasa natural de su piel, y quien era un imán, lo seguía siendo años después.",
         cap="*ÁCIDOS* de tu piel. | Y no cambia con los años", hold=0.25),
    dict(id="cta", who="nar", cut=True, say="Comenta si a ti te comen vivo, y envíaselo a esa persona a la que siempre le pican.",
         cap="¿Te comen vivo? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s3" and lt > 2.2:
        K.tag(c, W / 2, 1840, "Y 4 VECES MÁS QUE LA SEGUNDA", lt - 2.2, accent=RED, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "mosquito.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "mosquito.js", overlay=overlay)
