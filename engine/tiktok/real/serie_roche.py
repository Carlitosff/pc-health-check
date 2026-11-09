"""1704 SERIE 3D (roche.js): ¿Y si acercamos la Luna hasta que se rompe? Parte 6 de ¿QUÉ PASARÍA SI…? (prometida en la parte 5).
Cálculo propio con asserts: fuerza de marea ∝ 1/d³ (a mitad ×8, a 1/10 ×1.000); límite de Roche d = k·R_T·(ρ_T/ρ_L)^(1/3) con k = 2,44 (fluido) y 1,26 (rígido):
R_T 6.371 km, ρ_T 5,514 g/cm³, ρ_L 3,344 g/cm³ → ~18.400 km y ~9.500 km (los mismos órdenes que da la tabla de Wikipedia 'Roche limit', ~18.381 / 9.492, que no se pudo abrir hoy).
No se afirma altura de mareas en metros (depende de la dinámica de los océanos); solo la fuerza."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
D0 = 384_400
assert (D0 / (D0 / 2)) ** 3 == 8 and round((D0 / (D0 / 10)) ** 3) == 1000
RT, rT, rL = 6371, 5.514, 3.344
fluid, rigid = 2.44 * RT * (rT / rL) ** (1 / 3), 1.26 * RT * (rT / rL) ** (1 / 3)
assert 18_000 < fluid < 18_800 and 9_300 < rigid < 9_700, (fluid, rigid)
x_fluid = (D0 / fluid) ** 3
assert x_fluid > 9_000
V = dict(slug="1704_luna_hasta_romperse", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 6", send="ENVÍASELO A QUIEN LE GUSTE LA LUNA",
         rehook=("s3", "ESPERA… AQUÍ EMPIEZA A ROMPERSE"), reveal=("s4", "LO QUE QUEDA"), segs=[
    dict(id="h", who="nar", say="¿Y si acercamos la Luna, poco a poco, hasta que se rompe?", cap="Acercamos la *LUNA*… hasta que *SE ROMPE*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="A mitad de camino, la verías el doble de grande, y las mareas tirarían ocho veces más.",
         cap="A *mitad* de camino: | el *doble* de grande, | mareas *×8*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Y a una décima parte de la distancia, tirarían del mar mil veces más.", cap="A *una décima parte*: | mareas *×1.000*", hold=0.2),
    dict(id="s3", who="nar", cut=True, say="A unos dieciocho mil kilómetros, la Tierra tira más de su cara cercana que de la lejana, y la estira.",
         cap="A *18.000 km*, | la Tierra | la *ESTIRA*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Aunque fuera rígida, a unos nueve mil quinientos se rompe, y sus trozos forman un anillo, como en la parte cinco.",
         cap="Al final *SE ROMPE*… | y queda *UN ANILLO*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Sígueme, que en la parte siete la Tierra gira cada vez más deprisa. Comenta hasta dónde la acercarías.",
         cap="*Parte 7*: la Tierra | gira *más deprisa*. | ¿Hasta dónde? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    lab = {"s1": "192.200 KM · MAREAS ×8", "s2": "38.440 KM · MAREAS ×1.000", "s3": "18.400 KM · LÍMITE DE ROCHE",
           "s4": "9.500 KM: SE ROMPE"}.get(sid)
    if lab and lt > 1.2:
        K.tag(c, W / 2, 1760, lab, lt - 1.2, accent=GOLD, size=40)
    if sid in ("s3", "s4") and lt > 2.6:
        K.tag(c, W / 2, 1840, "CÁLCULO PROPIO · FÓRMULA DE ROCHE", lt - 2.6, accent=WHITE, size=26)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "roche.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "roche.js", overlay=overlay)
