"""2703 MITO 3D (suenos.js): '¿Tú sueñas en color o en blanco y negro?' → depende de la tele con la que creciste.
Eva Murzyn (Universidad de Dundee), 'Do we only dream in colour? A comparison of reported dream colour in younger and older adults with different
experiences of black and white media', Consciousness and Cognition 17(4):1228-1237, dic-2008 (doi 10.1016/j.concog.2008.09.002): 'people who had
access to black and white media before colour media experienced more greyscale dreams'. BPS Research Digest (Christian Jarrett, 17/11/2008):
'30 older (average age 64) and 30 younger people (average age 21)', diario de sueños; '22 per cent vs. 4 per cent' de sueños en blanco y negro;
'Research conducted in the early part of the last century consistently found that people reported dreaming most often in black and white'."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
assert 30 + 30 == 60
V = dict(slug="2703_mito_suenas_en_color", accent=GOLD, drone=0.02, mood="misterio", send="ENVÍASELO A TU ABUELA",
         rehook=("s3", "ESPERA… MIRA LA DIFERENCIA"), reveal=("s3", "LA RESPUESTA"),
         # v30: gradación de toda la imagen: el gancho arranca en blanco y negro y se tiñe de color; s1 (hace un siglo) en sepia
         grade=[("h", 0, 0.0), ("h", 1.4, 0.0), ("h", 2.6, 1.0), ("s1", 0, 1.0), ("s1", .5, 0.0, 0.8), ("s2", 0, 0.0, 0.8), ("s2", .6, 1.0)],
         segs=[
    dict(id="h", who="nar", say="¿Tú sueñas en color, o en blanco y negro? Depende de algo que veías de pequeño.",
         cap="¿Tú sueñas *EN COLOR*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Hace un siglo, casi todo el mundo decía que soñaba en blanco y negro.",
         cap="Hace un siglo: | casi todos en *BLANCO Y NEGRO*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="En dos mil ocho, Eva Murzyn, de la Universidad de Dundee, pidió a sesenta personas que apuntaran sus sueños.",
         cap="*60 personas* | apuntando sus sueños", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Los mayores, que crecieron con la tele en blanco y negro, soñaban en gris un veintidós por ciento de las veces. Los jóvenes, solo un cuatro.",
         cap="Mayores: *22 %* | Jóvenes: solo *4 %*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Así que tus sueños se parecen a la pantalla con la que creciste.",
         cap="Sueñas como *la tele* | con la que creciste", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta color o gris: ¿cómo fue tu último sueño? Y envíaselo a quien veía la tele en blanco y negro.",
         cap="¿*COLOR* o *GRIS*? | Comenta"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2" and lt > 1.2:
        K.tag(c, W / 2, 1840, "MURZYN · CONSCIOUSNESS AND COGNITION · 2008", lt - 1.2, accent=WHITE, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "suenos.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "suenos.js", overlay=overlay, keep=True)
