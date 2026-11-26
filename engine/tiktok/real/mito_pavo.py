"""3403 MITO 3D (pavo.js): '¿El pavo te da sueño porque tiene mucho triptófano?' → NO. Hoy (jueves 26/11/2026) es Acción de Gracias en EE. UU.
Fuentes: Harvard Health Publishing, Robert H. Shmerling, 'The turkey coma: fact or fiction?' (2013, act. 24/04/2026): 'There's not enough
tryptophan in a serving of turkey to have much of an effect', 'a 3-ounce serving of turkey contains about 250 mg, similar to the amount in chicken
or beef', suplementos para dormir '1,000 milligrams (mg) to 3,000 mg daily', 'it's more likely just from digesting a big meal' (o el alcohol).
Scientific American (Ferris Jabr): 'turkey contains about the same amount of tryptophan as chicken, beef and other meats', 'Studies have confirmed
big meals of any kind make people drowsy'. Cálculo propio: 1.000/250 = 4 y 3.000/250 = 12 raciones."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; RED = 0xFFFF6A4A; GREEN = 0xFF4ADE80
assert 1000 / 250 == 4 and 3000 / 250 == 12
V = dict(slug="3403_mito_pavo_sueno", accent=GOLD, drone=0.02, mood="luz", send="ENVÍASELO A QUIEN CULPA AL PAVO",
         dare=("s1", "MÁNDASELO A QUIEN SE DUERME", 1840), vote=("s2", ("SÍ", "NO"), 1, 1580),
         rehook=("s3", "ESPERA… EL CULPABLE ESTÁ EN EL PLATO"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Te entra sueño después de comer pavo, porque tiene mucho triptófano?",
         cap="¿El pavo te da *SUEÑO*?", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Hoy es Acción de Gracias en Estados Unidos, y millones de personas acabarán dormidas en el sofá.",
         cap="Hoy es | *ACCIÓN DE GRACIAS*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Pero una ración de pavo tiene unos doscientos cincuenta miligramos de triptófano, más o menos lo mismo que el pollo.",
         cap="*LO MISMO* que el pollo", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Las pastillas de triptófano llevan de mil a tres mil miligramos, como comerte de cuatro a doce raciones.",
         cap="Como comer | *HASTA 12 RACIONES*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Según Harvard, el sueño viene de la comilona: el plato enorme, el postre y, a veces, el vino.",
         cap="La culpa es | *LA COMILONA*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta quién se duerme primero en tu casa, y envíaselo a quien culpa al pavo.",
         cap="¿Quién se duerme primero? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 3.2:
        K.pill(c, W / 2, 1580, "JUEVES 26 DE NOVIEMBRE", 48, bg=0xEE000000, fg=GOLD, scale=K.ease_back(K.prog(lt, 3.2, 3.5)))
    if sid == "s2" and lt > 3.6:
        K.tag(c, W / 2, 1840, "PAVO ≈ POLLO ≈ TERNERA · ~250 mg", lt - 3.6, accent=WHITE, size=32)
    if sid == "s3" and lt > 1.0:
        K.pill(c, W / 2, 1580, "1.000–3.000 mg = 4 A 12 RACIONES", 44, bg=0xEE000000, fg=RED, scale=K.ease_back(K.prog(lt, 1.0, 1.3)))
    if sid == "s4" and lt > 1.0:
        K.tag(c, W / 2, 1840, "HARVARD HEALTH · R. H. SHMERLING", lt - 1.0, accent=WHITE, size=32)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1), {k: round(v[0], 1) for k, v in K.plan(V)["tl"].items()})
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "pavo.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "pavo.js", overlay=overlay, keep=True)
