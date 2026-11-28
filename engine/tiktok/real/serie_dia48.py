"""3604 SERIE 3D (dia48.js): ¿Y si el día durara 48 horas? Parte 25 de ¿QUÉ PASARÍA SI…? (prometida en la 24).
Fuentes: UW–Madison News 04/06/2018 (Meyers y Malinverno, PNAS 04/06/2018): '1.4 billion years ago, a day on Earth lasted just over 18 hours',
'As the moon moves away, the Earth is like a spinning figure skater who slows down'; National Geographic (Alejandra Borunda, 20/06/2018):
'This drag slows Earth's rotation rate by about 1.78 milliseconds each century'.
Cálculo propio: la báscula en el ecuador resta la aceleración centrífuga ω²R. Con 24 h (día sidéreo 86.164 s) son 0,0337 m/s²; con un día el
doble de largo, ω/2 → la cuarta parte → la báscula marca 80·(0,0337·3/4)/9,78 ≈ 0,21 kg más (≈ 200 g). Horas de sol en el equinoccio = mitad del día = 24 h.
Calor de tarde / frío de noche: cualitativo (más horas seguidas de sol y de oscuridad), sin cifras de temperatura."""
import sys, math
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; CYAN = 0xFF8FD0FF; RED = 0xFFFF6A4A; GREEN = 0xFF4ADE80
Rq, g0 = 6378137.0, 9.78
w24 = 2 * math.pi / 86164.0; w48 = w24 / 2
dkg = 80 * (w24 ** 2 - w48 ** 2) * Rq / g0
assert 0.19 < dkg < 0.22, dkg
READ = {"s3": round(80 + dkg, 1)}
assert READ["s3"] == 80.2
V = dict(slug="3604_dia_de_48_horas", accent=GOLD, drone=0.03, mood="epico", badge="¿QUÉ PASARÍA SI…? · PARTE 25",
         send="ENVÍASELO A QUIEN NUNCA LE DA TIEMPO", dare=("s1", "PREGÚNTALE QUÉ HARÍA CON 48 H", 1840),
         rehook=("s3", "ESPERA… LA BÁSCULA TAMBIÉN CAMBIA"), sfx=[("h", 1.0, "tick", .12), ("h", 2.0, "tick", .12), ("h", 3.0, "tick", .12)],
         segs=[
    dict(id="h", who="nar", say="¿Y si el día durara cuarenta y ocho horas? Mira lo despacio que se mueve el Sol.",
         cap="¿Un día de *48 HORAS*?", hold=0.25),
    dict(id="s1", who="nar", cut=True, say="Tendrías veinticuatro horas seguidas de sol, y después otras veinticuatro de noche.",
         cap="*24 horas* de sol, | *24 horas* de noche", hold=0.25),
    dict(id="s2", who="nar", cut=True, say="Con tantas horas de sol, las tardes se calentarían mucho más, y las noches serían mucho más frías.",
         cap="Tardes *MÁS CALIENTES*, | noches *MÁS FRÍAS*", hold=0.25),
    dict(id="s3", who="nar", cut=True, say="Y en el ecuador la báscula marcaría unos doscientos gramos más, porque la Tierra giraría más despacio.",
         cap="La báscula: | *200 GRAMOS MÁS*", hold=0.25),
    dict(id="s4", who="nar", cut=True, say="Y el día ya se alarga: hace mil cuatrocientos millones de años duraba dieciocho horas. La Luna nos va frenando.",
         cap="Hace 1.400 millones de años: | *DÍAS DE 18 HORAS*", hold=0.25),
    dict(id="cta", who="nar", cut=True, say="Comenta qué harías con un día de cuarenta y ocho horas. En la parte veintiséis, la Tierra se queda sin océanos.",
         cap="¿Qué harías tú? *COMENTA* | Parte 26: *SIN OCÉANOS*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; d = sg["b"] - sg["a"]
    if sid == "s1" and lt > .6:
        k = K.prog(lt, .8, d - .6)
        K.pill(c, W / 2, 1580, f"HORAS DE SOL: {int(round(24 * min(1, k * 2)))} · NOCHE: {int(round(24 * max(0, k * 2 - 1)))}", 44,
               bg=0xEE000000, fg=GOLD, scale=K.ease_back(K.prog(lt, .6, .9)))
    if sid == "s4" and lt > 1.2:
        k = K.prog(lt, 1.6, 4.0)
        K.pill(c, W / 2, 1580, f"1 DÍA = {18 + 6 * k:.0f} h" if k < 1 else "+1,78 ms CADA SIGLO", 52, bg=0xEE000000, fg=CYAN if k < 1 else GREEN,
               scale=K.ease_back(K.prog(lt, 1.2, 1.5)))
        K.tag(c, W / 2, 1840, "MEYERS Y MALINVERNO · PNAS · 2018", lt - 1.2, accent=WHITE, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1), {k: round(v[0], 1) for k, v in K.plan(V)["tl"].items()})
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "dia48.js", stills=sys.argv[2].split(","), extra_job=dict(read=READ))
    else:
        v3d_run.run3d(V, "dia48.js", overlay=overlay, keep=True, extra_job=dict(read=READ))
