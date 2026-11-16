"""2404 SERIE 3D (encoge.js): ¿Y si la Tierra se encogiera a la mitad? Parte 13 de ¿QUÉ PASARÍA SI…? (prometida en la parte 12: 'la Tierra se encoge a la mitad').
Cálculo propio (misma roca = misma densidad): radio ÷2 → volumen y masa ÷8; gravedad en superficie g ∝ ρ·R → ÷2; 80 kg → 40; salto de 50 cm → 1 m (h = v²/2g);
velocidad de escape √(2GM/R) ∝ R·√ρ → ÷2: 11,2 → 5,6 km/s. Marte: radio 0,53 del terrestre (3.390 / 6.371 km).
NASA/LASP MAVEN, 30/03/2017: 'most of the gas ever present in the Mars atmosphere has been lost to space' (Bruce Jakosky); 'sputtering' por el viento solar.
El guion NO atribuye la pérdida a la gravedad (la fuente no lo dice): solo dice que Marte, de ese tamaño, perdió casi todo su aire."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; RED = 0xFFFF7A4A
assert 2 ** 3 == 8 and (1 / 8) / (1 / 2) ** 2 == .5 and 80 / 2 == 40 and 50 * 2 == 100
assert round(11.2 * math.sqrt((1 / 8) / (1 / 2)), 1) == 5.6 and round(3389.5 / 6371, 2) == .53
V = dict(slug="2404_tierra_a_la_mitad", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 13", send="ENVÍASELO A QUIEN QUIERE PESAR MENOS",
         rehook=("s3", "ESPERA… LO MALO"), reveal=("s4", "¿Y EL AIRE?"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra se encogiera a la mitad? Súbete a la báscula: pesarías la mitad.", cap="¿Y si la Tierra se encoge a la *MITAD*?", hold=0.1),
    dict(id="s1", who="nar", cut=True, say="Con la misma roca, tendría ocho veces menos masa, y la gravedad del suelo sería la mitad.",
         cap="÷2 de ancho: | *÷8* de masa | y *÷2* de gravedad", hold=0.1),
    dict(id="s2", who="nar", cut=True, say="Con ochenta kilos marcarías cuarenta, y tu mejor salto llegaría al doble de alto.",
         cap="*80 kg* marcan *40* | y saltas el *DOBLE*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero para escapar al espacio bastaría con la mitad de velocidad, unos cinco kilómetros y medio por segundo.",
         cap="Para salir al espacio: | solo *5,6 km/s*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y eso tiene un precio: Marte, que mide casi eso, perdió al espacio la mayor parte de su aire, según la NASA.",
         cap="Marte, de ese tamaño, | perdió casi todo su *AIRE*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Sígueme: en la parte catorce, la Tierra está hueca por dentro. Comenta cuánto marcarías.",
         cap="*Parte 14*: | la Tierra *HUECA*. | ¿Cuánto marcarías? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 2.4:
        K.tag(c, W / 2, 1840, "MISMA DENSIDAD · CÁLCULO PROPIO", lt - 2.4, accent=WHITE, size=30)
    if sid == "s3" and lt > 2.4:
        K.tag(c, W / 2, 1840, "HOY: 11,2 km/s · CÁLCULO PROPIO", lt - 2.4, accent=WHITE, size=30)
    if sid == "s4" and lt > 2.6:
        K.tag(c, W / 2, 1840, "NASA · MAVEN · 2017", lt - 2.6, accent=RED, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "encoge.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "encoge.js", overlay=overlay)
