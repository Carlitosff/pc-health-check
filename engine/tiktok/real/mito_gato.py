"""3303 MITO 3D (gato.js): '¿Tu gato siempre cae de pie, y por eso no se hace daño?' → NO.
Fuentes: 'High-rise syndrome in cats', J Am Vet Med Assoc 1987 Dec 1;191(11):1399-403 (PubMed 3692980): 'High-rise syndrome was diagnosed in
132 cats over a 5-month period', 'Ninety percent of the treated cats survived', 'Ninety percent of the cats had some form of thoracic trauma'.
Animal Medical Center de Nueva York (AMC, 'High Rise Syndrome in Cats', act. 17/06/2024): 'over the course of five months, AMC treated 132 cats
who had fallen from buildings', 'righting reflex allows her to twist her body and land on her feet most of the time, she still may get hurt',
'chest trauma, head/facial injuries, and limb fractures'. Amy Attas (veterinaria, interna en el AMC en 1987; Literary Hub, 'Pets and the City'):
'Cats that fell from much higher floors... weren't included in the study, because, sadly, those cats typically died and so weren't brought
to a veterinary hospital'. NO se usa el '7 pisos' ni velocidades terminales (no verificados hoy)."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; RED = 0xFFFF6A4A; GREEN = 0xFF4ADE80
V = dict(slug="3303_mito_gato_cae_de_pie", accent=GOLD, drone=0.02, mood="misterio", send="ENVÍASELO A ALGUIEN CON GATO",
         dare=("s1", "MÁNDASELO A QUIEN TIENE GATO", 1840), vote=("s2", ("SÍ", "NO"), 1, 1580),
         rehook=("s3", "ESPERA… LO PEOR NO SALE EN EL ESTUDIO"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿Tu gato siempre cae de pie, y por eso no se hace daño?",
         cap="¿Cae de pie y *NO SE HACE DAÑO*?", hold=0.4),
    dict(id="s1", who="nar", cut=True, say="Es verdad que se gira en el aire, y casi siempre cae con las patas hacia abajo.",
         cap="Se gira *EN EL AIRE*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Pero eso no le salva. Un hospital de Nueva York atendió a ciento treinta y dos gatos caídos de edificios en cinco meses.",
         cap="*132 gatos* en 5 meses", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Nueve de cada diez se salvaron, pero muchos con golpes graves en el pecho, en la cara y en las patas.",
         cap="Golpes en *EL PECHO*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Y los que caían desde muy alto casi nunca llegaban al hospital: el estudio solo cuenta a los que vivieron.",
         cap="Solo cuenta | a *LOS QUE VIVIERON*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta si tu gato sale al balcón, y envíaselo a alguien con gato para que ponga una red.",
         cap="¿Sale al balcón? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s2" and lt > 3.4:
        K.tag(c, W / 2, 1840, "ANIMAL MEDICAL CENTER · NUEVA YORK · 1987", lt - 3.4, accent=WHITE, size=30)
    if sid == "s3" and lt > 1.0:
        K.pill(c, W / 2, 1580, "9 DE CADA 10 SE SALVARON", 48, bg=0xEE000000, fg=GREEN, scale=K.ease_back(K.prog(lt, 1.0, 1.3)))
        if lt > 3.2:
            K.tag(c, W / 2, 1840, "J. AM. VET. MED. ASSOC. · 1987", lt - 3.2, accent=WHITE, size=30)
    if sid == "s4" and lt > 3.0:
        K.pill(c, W / 2, 1580, "LOS DE MUY ARRIBA NO SALEN", 44, bg=0xEE000000, fg=RED, scale=K.ease_back(K.prog(lt, 3.0, 3.3)))


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "gato.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "gato.js", overlay=overlay, keep=True)
