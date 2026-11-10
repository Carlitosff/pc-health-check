"""1803 MITO 3D (rayo.js): 'un rayo nunca cae dos veces en el mismo sitio'.
Fuentes: NOAA Lightning Safety, 'Myths and Truths' (versión del 20/06/2012, archivo UNT 13/02/2013): 'Lightning often strikes the same place repeatedly,
especially if it's a tall, pointy, isolated object. The Empire State Building is hit nearly 100 times a year' (otras fuentes dan ~20–25: el guion dice
'decenas', que cubre ambas). Guinness World Records, 26/01/2023 (Vicki Newman): Roy Sullivan, guardaparques de Shenandoah (Virginia), 7 rayos entre
abril de 1942 y junio de 1977, sobrevivió a todos. Consejo de seguridad estándar de NOAA: refugio en un edificio cerrado o en un coche de techo rígido."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; CYAN = 0xFF4DE3FF
V = dict(slug="1803_mito_rayo_dos_veces", accent=CYAN, drone=0.03, mood="misterio", badge=None, send="ENVÍASELO A QUIEN DICE ESE REFRÁN",
         rehook=("s3", "ESPERA… Y A UNA PERSONA"), reveal=("s2", "CUÁNTOS RAYOS"), segs=[
    dict(id="h", who="nar", say="Te dijeron que un rayo nunca cae dos veces en el mismo sitio. Mira esta torre.", cap="¿Un rayo *NUNCA* cae dos veces?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Los rayos buscan lo más alto, puntiagudo y aislado, y lo golpean una y otra vez.", cap="Buscan lo más *ALTO*… | y *repiten*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Al Empire State de Nueva York le caen decenas de rayos cada año, según el servicio meteorológico de Estados Unidos.",
         cap="Empire State: | *decenas de rayos* | *cada año*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Y a una persona le cayeron siete: Roy Sullivan, guarda forestal en Virginia, y sobrevivió a todos.",
         cap="Roy Sullivan: | *7 RAYOS* | y *sobrevivió*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Así que en una tormenta no te fíes del refrán, y métete en un edificio o en un coche.", cap="En tormenta: | a un *edificio* | o un *coche*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Envíaselo a quien todavía dice ese refrán, y comenta si tú te lo creías.", cap="¿Te lo creías? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2" and lt > 1.0:
        K.tag(c, W / 2, 1780, "NOAA · LIGHTNING SAFETY", lt - 1.0, accent=GOLD, size=36)
    if sid == "s3" and lt > 1.2:
        K.tag(c, W / 2, 1780, "GUINNESS WORLD RECORDS", lt - 1.2, accent=GOLD, size=36)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "rayo.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "rayo.js", overlay=overlay)
