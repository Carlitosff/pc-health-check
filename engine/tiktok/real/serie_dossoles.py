"""2204 SERIE 3D (dossoles.js): ¿Y si la Tierra tuviera dos soles? Parte 11 de ¿QUÉ PASARÍA SI…? (prometida en la parte 10).
Kepler-16b: Smithsonian Science / CfA, 15/09/2011 (Doyle et al., Science 15/09/2011): 'Kepler-16b enjoys a double sunset as it circles a pair of stars';
estrellas de ~69 % y ~20 % de la masa del Sol; el planeta da la vuelta en 229 días; 'similar to Saturn in both size and mass'; superficie de -100 a -150 °F
(-73 a -101 °C); a unos 200 años luz.
Cálculo propio: otro Sol igual al lado → el doble de luz (2,00); Venus a 0,723 UA recibe 1/0,723² = 1,91 → más que Venus. Para recibir la luz de hoy:
d = √2 = 1,414 UA (41 % más lejos); con dos masas solares el año dura √(d³/2) = 1,19 años ≈ 434 días."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; ICE = 0xFF4DE3FF
venus = 1 / 0.723 ** 2; d = math.sqrt(2); yr = math.sqrt(d ** 3 / 2) * 365.25
assert 1.90 < venus < 1.92 and 2 > venus and round((d - 1) * 100) == 41 and round(yr) == 434
V = dict(slug="2204_tierra_con_dos_soles", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 11", send="ENVÍASELO A QUIEN ODIA EL CALOR",
         rehook=("s3", "ESPERA… AQUÍ EN LA TIERRA"), reveal=("s4", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra tuviera dos soles? Mira tu sombra, porque tendrías dos.", cap="¿Y si la Tierra tuviera *DOS SOLES*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Existe de verdad: en dos mil once, la NASA encontró un planeta que gira alrededor de dos estrellas.",
         cap="*Kepler-16b*: | gira alrededor | de *DOS ESTRELLAS*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Allí hay dos atardeceres cada tarde, pero es un mundo helado.",
         cap="*Dos atardeceres* | y un mundo *HELADO*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Si nos pusieran otro Sol igual al lado, nos llegaría el doble de luz, más de la que recibe Venus.",
         cap="Otro Sol igual: | el *DOBLE* de luz: | más que *VENUS*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Para no achicharrarnos, habría que alejarse un cuarenta por ciento, y el año duraría unos cuatrocientos treinta días.",
         cap="*41 %* más lejos | y años de *434 días*", hold=0.45),
    dict(id="cta", who="nar", cut=True, say="Sígueme, que en la parte doce la Tierra crece hasta el doble. Comenta si prefieres un sol o dos.",
         cap="*Parte 12*: | la Tierra *×2*. | ¿UN sol o DOS? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 2.4:
        K.tag(c, W / 2, 1840, "NASA KEPLER · SCIENCE · 15/09/2011", lt - 2.4, accent=WHITE, size=30)
    if sid == "s2" and lt > 2.0:
        K.tag(c, W / 2, 1840, "ENTRE −73 Y −101 °C · CFA HARVARD-SMITHSONIAN", lt - 2.0, accent=ICE, size=28)
    if sid == "s3" and lt > 2.4:
        K.tag(c, W / 2, 1840, "VENUS RECIBE 1,9 VECES NUESTRA LUZ · CÁLCULO PROPIO", lt - 2.4, accent=WHITE, size=27)
    if sid == "s4" and lt > 2.0:
        K.tag(c, W / 2, 1840, "√2 = 1,41 VECES LA DISTANCIA · CÁLCULO PROPIO", lt - 2.0, accent=0xFF4ADE80, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "dossoles.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "dossoles.js", overlay=overlay)
