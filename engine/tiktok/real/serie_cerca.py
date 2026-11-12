"""2004 SERIE 3D (cerca.js): ¿Y si la Tierra se acerca al Sol? Parte 9 de ¿QUÉ PASARÍA SI…? (prometida en la parte 8: 'la Tierra se acerca al Sol').
Distancia media ≈ 150 millones de km (1 UA); la luz tarda ~8 min 20 s. Flujo ∝ 1/d²: 10 % más cerca → 1/0,9² = 1,235 → +23 % (cálculo propio).
Kopparapu et al., 'Habitable Zones around Main-sequence Stars: New Estimates', The Astrophysical Journal 765:131 (2013), resumen en vpl.uw.edu:
'the water-loss (inner HZ) and maximum greenhouse (outer HZ) limits for our solar system are at 0.99 and 1.70 AU, respectively, suggesting that the
present Earth lies near the inner edge' → el guion dice 'un uno por ciento más cerca… el agua empezaría a escaparse al espacio, poco a poco'.
Venus a 0,723 UA → 1/0,723² = 1,91 ('casi el doble de luz', cálculo propio); superficie a más de 450 °C (NASA da ~465–475 °C según la página)."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
f10 = 1 / 0.9 ** 2
fv = 1 / 0.723 ** 2
assert round((f10 - 1) * 100) == 23 and 1.85 < fv < 1.95
V = dict(slug="2004_tierra_se_acerca_al_sol", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 9", send="ENVÍASELO A QUIEN SIEMPRE TIENE CALOR",
         rehook=("s3", "ESPERA… CON MUCHO MENOS"), reveal=("s4", "MIRA VENUS"), segs=[
    dict(id="h", who="nar", say="¿Y si la Tierra se acercara un poco al Sol? Bastaría muy poco para perder los océanos.", cap="¿Y si nos *ACERCAMOS* al Sol?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Hoy estamos a unos ciento cincuenta millones de kilómetros del Sol.",
         cap="*150 millones* | de kilómetros", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Si nos acercáramos solo un diez por ciento, nos llegaría un veintitrés por ciento más de luz.",
         cap="*10 %* más cerca: | *23 %* más luz", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero un estudio de dos mil trece calculó que, con solo un uno por ciento, el agua ya empezaría a escaparse al espacio.",
         cap="Con solo un *1 %*: | el agua | *se escapa*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Venus está más cerca, recibe casi el doble de luz, y su suelo pasa de los cuatrocientos cincuenta grados.",
         cap="Venus: | casi *el doble* de luz | y *más de 450 °C*", hold=0.45),
    dict(id="cta", who="nar", cut=True, say="Sígueme, que en la parte diez la Tierra se aleja del Sol. Comenta si te mudarías a Venus.",
         cap="*Parte 10*: | nos *alejamos*. | ¿Te mudarías? *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2" and lt > 2.0:
        K.tag(c, W / 2, 1840, "LA LUZ CRECE CON 1 / DISTANCIA² · CÁLCULO PROPIO", lt - 2.0, accent=WHITE, size=28)
    if sid == "s3" and lt > 2.0:
        K.tag(c, W / 2, 1840, "KOPPARAPU ET AL. · ASTROPHYSICAL JOURNAL 2013", lt - 2.0, accent=WHITE, size=28)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "cerca.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "cerca.js", overlay=overlay)
