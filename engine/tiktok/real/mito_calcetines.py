"""3203 MITO 3D (calcetines.js): '¿Dormir con calcetines te ayuda a dormir?' → VERDAD (con un estudio pequeño).
Estudio: 'Effects of feet warming using bed socks on sleep quality and thermoregulatory responses in a cool environment',
Journal of Physiological Anthropology, 2018 (doi 10.1186/s40101-018-0172-z). Fortune (27/04/2024): 'men who wore socks fell asleep about
seven minutes faster, slept 32 minutes longer, and woke up about seven times less often'; HuffPost UK: 'One study involving a small number
of subjects found that young men wearing socks fell asleep 7.5 minutes faster, slept 32 minutes longer, and woke up 7.5 times less often';
mecanismo: 'distal vasodilation', 'That can help lower the body's core temperature, signalling the brain that it is time for bed'.
El guion dice 'unos siete minutos', '32 minutos', 'unas siete veces menos' y que fue un estudio PEQUEÑO, con chicos jóvenes, en una habitación fresca."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; RED = 0xFFFF6A4A; BLUE = 0xFF8FD0FF
V = dict(slug="3203_mito_calcetines_dormir", accent=GOLD, drone=0.02, mood="misterio", send="ENVÍASELO A QUIEN DUERME CON LOS PIES HELADOS",
         dare=("s1", "PREGÚNTALE A TU PAREJA", 1840), vote=("s2", ("SÍ", "NO"), 0, 1580),
         rehook=("s3", "ESPERA… MIRA LA DE LA IZQUIERDA"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Dormir con calcetines te ayuda a dormir antes? Un estudio lo midió.",
         cap="¿Calcetines para *DORMIR*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Pusieron a dormir a unos chicos jóvenes en una habitación fresca, con calcetines y sin ellos.",
         cap="*CON* o *SIN* calcetines", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Con calcetines se durmieron unos siete minutos antes, y durmieron treinta y dos minutos más.",
         cap="*+32 minutos* de sueño", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y además, se despertaron unas siete veces menos durante la noche.",
         cap="*7 veces menos* | despiertos", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Los pies calientes sueltan calor por la piel, y tu cuerpo se enfría por dentro, que es la señal para dormir.",
         cap="Pies calientes, | cuerpo *MÁS FRESCO*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Fue un estudio pequeño, pero comenta si duermes con calcetines, y envíaselo a quien tiene los pies helados.",
         cap="¿Con o sin? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 3.0:
        K.tag(c, W / 2, 1840, "J. PHYSIOL. ANTHROPOL. · 2018", lt - 3.0, accent=WHITE, size=32)
    if sid == "s2" and lt > 2.9:
        K.pill(c, W / 2 - 200, 1580, "−7 MIN", 56, bg=0xEE000000, fg=GOLD, scale=K.ease_back(K.prog(lt, 2.9, 3.2)))
        K.pill(c, W / 2 + 200, 1580, "+32 MIN", 56, bg=0xEE000000, fg=GOLD, scale=K.ease_back(K.prog(lt, 3.3, 3.6)))
    if sid == "s3" and lt > 2.0:
        K.tag(c, W / 2, 1840, "DESPERTARES: ~7 MENOS · ESTUDIO PEQUEÑO", lt - 2.0, accent=RED, size=30)
    if sid == "s4" and lt > 2.0:
        # termómetro de temperatura interna que baja (2D: las cifras que cambian van mejor en el overlay)
        k = K.smooth((lt - 2.0) / 3.0)
        x, y0, hh = 120, 900, 520
        c.drawRRect(K.skia.RRect.MakeRectXY(K.skia.Rect.MakeXYWH(x - 34, y0, 68, hh), 34, 34), K.fill(0xCC0B0D14))
        lvl = hh * (0.82 - 0.32 * k)
        c.drawRRect(K.skia.RRect.MakeRectXY(K.skia.Rect.MakeXYWH(x - 20, y0 + hh - lvl - 14, 40, lvl), 20, 20), K.fill(K.lerp_col(RED, BLUE, k) if hasattr(K, "lerp_col") else RED))
        c.drawCircle(x, y0 + hh + 20, 52, K.fill(0xCC0B0D14)); c.drawCircle(x, y0 + hh + 20, 38, K.fill(RED))
        K.pill(c, x + 20, y0 - 50, "POR DENTRO ↓", 34, bg=0xEE000000, fg=BLUE)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "calcetines.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "calcetines.js", overlay=overlay, keep=True)
