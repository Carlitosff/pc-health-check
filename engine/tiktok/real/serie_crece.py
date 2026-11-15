"""2304 SERIE 3D (crece.js): ¿Y si la Tierra fuera el doble de grande? Parte 12 de ¿QUÉ PASARÍA SI…? (prometida en la parte 11: 'la Tierra crece hasta el doble').
Cálculo propio (misma roca = misma densidad): radio ×2 → volumen y masa ×8; gravedad en superficie g = G·M/R² ∝ ρ·R → ×2;
80 kg en la báscula → 160; un salto de 50 cm → 25 cm (h = v²/2g); velocidad de escape √(2GM/R) ∝ R·√ρ → ×2: 11,2 → 22,4 km/s;
(no usado en el guion) horizonte a 1,7 m de altura d = √(2·R·h): 4,65 km → 6,58 km (+41 %).
NASA, 'What Is a Super-Earth?' (science.nasa.gov/exoplanets/super-earth, act. 22/10/2026): 'between twice the size of Earth and up to 10 times its mass';
'they are common among planets found so far in our galaxy'."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; GREEN = 0xFF4ADE80
R = 6371e3
d1 = math.sqrt(2 * R * 1.7) / 1000; d2 = math.sqrt(2 * 2 * R * 1.7) / 1000
assert 2 ** 3 == 8 and 8 / 2 ** 2 == 2 and 80 * 2 == 160 and 50 / 2 == 25
assert round(11.2 * math.sqrt(8 / 2), 1) == 22.4 and round(d1, 1) == 4.7 and round(d2, 1) == 6.6 and round((d2 / d1 - 1) * 100) == 41
V = dict(slug="2304_tierra_el_doble_de_grande", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 12", send="ENVÍASELO A QUIEN SE QUEJA DE LA BÁSCULA",
         rehook=("s3", "ESPERA… Y PARA IRSE"), reveal=("s4", "¿EXISTEN?"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra fuera el doble de grande? Súbete a la báscula: pesarías el doble.", cap="¿Y si la Tierra fuera el *DOBLE* de grande?", hold=0.1),
    dict(id="s1", who="nar", cut=True, say="Con la misma roca, tendría ocho veces más masa, y la gravedad del suelo sería el doble.",
         cap="×2 de ancho: | *×8* de masa | y *×2* de gravedad", hold=0.1),
    dict(id="s2", who="nar", cut=True, say="Con ochenta kilos marcarías ciento sesenta, y tu mejor salto se quedaría en la mitad.",
         cap="*80 kg* marcan *160* | y saltas la *MITAD*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y para escapar al espacio, un cohete tendría que ir el doble de rápido: a más de veintidós kilómetros por segundo.",
         cap="Para salir al espacio: | *22,4 km/s*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y no es ciencia ficción: la NASA ya ha encontrado muchos planetas así, las supertierras.",
         cap="Y existen: | las *SUPERTIERRAS*", hold=0.2),
    dict(id="cta", who="nar", cut=True, say="Sígueme: en la parte trece, la Tierra se encoge a la mitad. Comenta cuánto marcarías.",
         cap="*Parte 13*: | la Tierra *÷2*. | ¿Cuánto marcarías? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 2.4:
        K.tag(c, W / 2, 1840, "MISMA DENSIDAD · CÁLCULO PROPIO", lt - 2.4, accent=WHITE, size=30)
    if sid == "s3" and lt > 2.4:
        K.tag(c, W / 2, 1840, "HOY: 11,2 km/s · CÁLCULO PROPIO", lt - 2.4, accent=WHITE, size=30)
    if sid == "s4" and lt > 2.6:
        K.tag(c, W / 2, 1840, "NASA: HASTA EL DOBLE DE TAMAÑO · 'SON COMUNES'", lt - 2.6, accent=GREEN, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "crece.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "crece.js", overlay=overlay)
