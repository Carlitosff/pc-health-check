"""3304 SERIE 3D (doslunas.js): ¿Y si la Tierra tuviera dos lunas? Parte 22 de ¿QUÉ PASARÍA SI…? (prometida en la 21).
2024 PT5: Carlos y Raúl de la Fuente Marcos (Universidad Complutense de Madrid), 'A Two-month Mini-moon: 2024 PT5 Captured by Earth from
September to November', Research Notes of the AAS 8(9):224 (2024); sci.news (23/09/2024): 'from September 29 until November 25, 2024',
'until its next return in 2055', '~10 m'; Bolin et al. (arXiv 2411.08029): 'captured by the Earth-Moon system on 2024 September 29 and left
on 2024 November 25 UTC', diámetro 5,4 ± 1,2 m → el guion dice 'pocos metros'. HOY (25/11/2026) hace justo dos años que se fue.
Jutzi y Asphaug, Nature 04/08/2011 (Space.com 03/08/2011; UC Santa Cruz vía phys.org): segunda luna de ~1.200 km, 'one-third of our moon's
diameter', en un punto troyano 'tens of millions of years', choque a 7.200–10.800 km/h, 'would make up the highlands now seen on our moon's
far side'. Cálculo propio: dos lunas llenas iguales a la misma distancia → el doble de luz de luna."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; CYAN = 0xFF8FD0FF
assert 1200 / 3474 > .3 and 1200 / 3474 < .36 and 2026 - 2024 == 2
V = dict(slug="3304_tierra_dos_lunas", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 22",
         send="ENVÍASELO A QUIEN LE GUSTA LA LUNA", dare=("s4", "PREGÚNTALE CÓMO LA LLAMARÍA", 1840),
         rehook=("s2", "ESPERA… HUBO OTRA MUCHO MÁS GRANDE"), reveal=("s3", "LO QUE PASÓ"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra tuviera dos lunas? Hoy hace justo dos años que tuvo una segunda, y se escapó.",
         cap="¿Y si tuviéramos *DOS LUNAS*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Era una roca de pocos metros, que la Tierra atrapó durante dos meses, en dos mil veinticuatro.",
         cap="Una *MINILUNA* | en 2024", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="La estudiaron dos astrónomos de la Complutense de Madrid, y volverá a pasar en dos mil cincuenta y cinco.",
         cap="Vuelve en *2055*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero quizá hubo otra de mil doscientos kilómetros, que chocó despacio contra nuestra Luna.",
         cap="Otra luna: | *1.200 KILÓMETROS*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="De ese choque saldrían las montañas de la cara oculta. Y con dos lunas llenas, la noche tendría el doble de luz.",
         cap="*MONTAÑAS* en la cara oculta | y *EL DOBLE* de luz", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta cómo la llamarías. En la parte veintitrés, la Tierra se queda sin Luna.",
         cap="¿Cómo la llamarías? *COMENTA* | Parte 23: *SIN LUNA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 3.0:
        K.pill(c, W / 2, 1580, "29 SEP → 25 NOV 2024", 48, bg=0xEE000000, fg=GOLD, scale=K.ease_back(K.prog(lt, 3.0, 3.3)))
    if sid == "s2" and lt > 1.2:
        K.tag(c, W / 2, 1840, "C. Y R. DE LA FUENTE MARCOS · UCM", lt - 1.2, accent=WHITE, size=32)
    if sid == "s3" and lt > 3.4:
        K.pill(c, W / 2, 1580, "1/3 DE NUESTRA LUNA", 48, bg=0xEE000000, fg=CYAN, scale=K.ease_back(K.prog(lt, 3.4, 3.7)))
    if sid == "s4" and lt > 1.0:
        K.tag(c, W / 2, 1840, "JUTZI Y ASPHAUG · NATURE · 2011", lt - 1.0, accent=WHITE, size=32)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "doslunas.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "doslunas.js", overlay=overlay, keep=True)
