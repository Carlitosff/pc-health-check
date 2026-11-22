"""3003 MITO 3D (cafe.js): '¿El café te deshidrata?' → con 4 tazas al día, no.
EurekAlert (09/01/2014, Universidad de Birmingham): Killer, Blannin y Jeukendrup, PLOS ONE 2014, 'No evidence of dehydration with moderate
daily coffee intake: a counterbalanced cross-over study in a free-living population'. 'Fifty male participants were tested in two phases',
'four mugs (200ml) of either black coffee or water per day for three days', 'ten day wash out period'; 'drinking moderate amounts of coffee
does not result in dehydration'; financiado por el Institute for Scientific Information on Coffee (ISIC) → se dice en pantalla."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; GREEN = 0xFF4ADE80; CYAN = 0xFF4DE3FF
V = dict(slug="3003_mito_el_cafe_deshidrata", accent=GOLD, drone=0.02, mood="luz", send="ENVÍASELO A QUIEN NO SUELTA EL CAFÉ",
         rehook=("s3", "ESPERA… ¿Y EL RESULTADO?"), reveal=("s3", "EL RESULTADO"), dare=("s2", "¿CUÁNTOS TOMAS TÚ?", 1840),
         segs=[
    dict(id="h", who="nar", say="¿De verdad el café deshidrata? Seguro que te lo han dicho mil veces.",
         cap="¿El café te *DESHIDRATA*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="En dos mil catorce, la Universidad de Birmingham lo puso a prueba con cincuenta hombres que tomaban café a diario.",
         cap="*50 hombres* · Birmingham, 2014", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Durante tres días bebieron cuatro tazas de café, y otros tres días, cuatro vasos de agua.",
         cap="*4 cafés* frente a | *4 vasos de agua*", hold=0.2),
    dict(id="s3", who="nar", cut=True, say="Les midieron la sangre, la orina y el agua del cuerpo, y no encontraron diferencias.",
         cap="*NINGUNA* diferencia", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Con cuatro tazas al día, el café te hidrata casi igual que el agua.",
         cap="Te hidrata | *casi igual que el agua*", hold=0.3),
    dict(id="cta", who="nar", cut=True, say="Comenta cuántos cafés tomas al día, y envíaselo a quien no suelta la taza.",
         cap="¿Cuántos tomas? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 3.0:
        K.tag(c, W / 2, 1840, "KILLER, BLANNIN Y JEUKENDRUP · PLOS ONE, 2014", lt - 3.0, accent=WHITE, size=28)
    if sid == "s2" and lt > 3.4:
        K.tag(c, W / 2, 1840, "TAZAS DE 200 ml · 3 DÍAS CADA FASE", lt - 3.4, accent=WHITE, size=30)
    if sid == "s4" and lt > 1.6:
        K.tag(c, W / 2, 1840, "OJO: LO FINANCIÓ UN INSTITUTO DEL SECTOR DEL CAFÉ", lt - 1.6, accent=GOLD, size=26)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "cafe.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "cafe.js", overlay=overlay, keep=True)
