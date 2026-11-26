"""3404 SERIE 3D (sinluna.js): ¿Y si la Tierra se quedara sin Luna? Parte 23 de ¿QUÉ PASARÍA SI…? (prometida en la 22).
Mareas: la fuerza de marea del Sol es ~46 % de la de la Luna (NOAA, 'Tides and Water Levels') → sin Luna, mareas de menos de la mitad.
Eje: Jacques Laskar (IMCCE, 'The Earth without the Moon'; Laskar, Joutel y Robutel, Nature 361, 615–617, 18/02/1993): con la Luna la
oblicuidad oscila ~1,3° alrededor de 23,3°; sin ella 'wanders chaotically between 0 and more than 85 degrees' (en millones de años).
Noches: sin luna llena, solo la luz de las estrellas (cualitativo). Parte 24 prometida: la Luna al doble de cerca (cálculo propio: marea ∝ 1/d³ → ×8)."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; CYAN = 0xFF8FD0FF; RED = 0xFFFF6A4A
assert 0.46 < 0.5 and 2 ** 3 == 8
V = dict(slug="3404_tierra_sin_luna", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 23",
         send="ENVÍASELO A QUIEN LE GUSTA LA LUNA", dare=("s4", "PREGÚNTALE QUÉ ECHARÍA DE MENOS", 1840),
         rehook=("s3", "ESPERA… LO PEOR ES EL EJE"), reveal=("s3", "LO PEOR"), segs=[
    dict(id="h", who="nar", say="¿Y si esta noche la Luna desapareciera? Lo primero que notarías es el mar.",
         cap="¿Y si nos quedamos *SIN LUNA*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="La Luna es la que levanta las mareas. Sin ella solo tiraría el Sol, y las mareas serían de menos de la mitad.",
         cap="Mareas de | *MENOS DE LA MITAD*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Las noches serían mucho más oscuras, porque ya nunca habría luna llena, solo estrellas.",
         cap="Noches *MUCHO MÁS OSCURAS*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y lo peor sería el eje de la Tierra: sin la Luna que lo sujeta, podría bambolearse de cero a más de ochenta y cinco grados.",
         cap="El eje: | de *0 a 85 GRADOS*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="A lo largo de millones de años, media Tierra tendría veranos sin noche y unos inviernos eternos.",
         cap="*VERANOS SIN NOCHE* | e inviernos eternos", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta qué echarías de menos. En la parte veinticuatro, la Luna estará el doble de cerca.",
         cap="¿Qué echarías de menos? *COMENTA* | Parte 24: *LA LUNA, EL DOBLE DE CERCA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 3.6:
        K.pill(c, W / 2, 1580, "EL SOL TIRA UN 46 % DE LO QUE TIRA LA LUNA", 38, bg=0xEE000000, fg=CYAN, scale=K.ease_back(K.prog(lt, 3.6, 3.9)))
        K.tag(c, W / 2, 1840, "NOAA · TIDES AND WATER LEVELS", lt - 3.6, accent=WHITE, size=30)
    if sid == "s3" and lt > 2.6:
        K.tag(c, W / 2, 1840, "LASKAR, JOUTEL Y ROBUTEL · NATURE · 1993", lt - 2.6, accent=WHITE, size=30)
    if sid == "s4" and lt > .6:
        K.pill(c, W / 2, 1580, "HOY: 23° · SIN LUNA: 0°–85°", 46, bg=0xEE000000, fg=GOLD, scale=K.ease_back(K.prog(lt, .6, .9)))


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1), {k: round(v[0], 1) for k, v in K.plan(V)["tl"].items()})
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "sinluna.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "sinluna.js", overlay=overlay, keep=True)
