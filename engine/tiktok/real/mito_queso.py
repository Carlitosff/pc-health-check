"""3103 MITO 3D (queso.js): '¿El queso antes de dormir te da pesadillas?'
British Cheese Board, 2005. The Scotsman ('Nightmare is over as study says cheese doesn't cause bad dreams'): '200 volunteers in a week-long
cheese-eating experiment', 'After eating a 20g piece of cheese 30 minutes before going to sleep', '72 per cent of the volunteers slept very well
every night', 'none reported nightmares', Stilton: '75 per cent of men and 85 per cent of women experiencing bizarre and vivid dreams';
'perhaps unsurprisingly carried out by the British Cheese Board'. Live Science ('Does cheese give you nightmares?'): 'a cheese industry group',
'None reported nightmares', 'warrior kittens and vegetarian crocodiles', 'The researchers didn't have a control group'."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A; BLUE = 0xFF6AA8FF
assert 72 < 100 and min(75, 85) > 50  # 'la mayoría' con Stilton
V = dict(slug="3103_mito_queso_pesadillas", accent=GOLD, drone=0.02, mood="misterio", send="ENVÍASELO A QUIEN PICA QUESO DE NOCHE",
         dare=("s2", "PREGÚNTALE A TU MADRE", 1840),
         rehook=("s3", "ESPERA… LO RARO VIENE AHORA"), reveal=("s2", "LA RESPUESTA"), segs=[
    dict(id="h", who="nar", say="¿El queso, antes de dormir, te da pesadillas? Lo comprobaron con doscientas personas.",
         cap="¿El queso te da *PESADILLAS*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="En dos mil cinco, doscientos voluntarios comieron veinte gramos de queso, media hora antes de dormir.",
         cap="*200 personas* | *20 g* de queso", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Ninguno tuvo pesadillas, y setenta y dos de cada cien durmieron muy bien.",
         cap="*0 pesadillas*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="Pero con el queso azul, la mayoría tuvo sueños rarísimos, con gatitos guerreros y cocodrilos vegetarianos.",
         cap="Queso azul: | sueños *RARÍSIMOS*", hold=0.4),
    dict(id="s4", who="nar", cut=True, say="Eso sí, el estudio lo pagaron los propios queseros, y no hubo un grupo sin queso para comparar.",
         cap="Lo pagaron | *LOS QUESEROS*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta cuál es tu queso favorito, y envíaselo a quien cena queso todas las noches.",
         cap="¿Tu queso favorito? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "h":
        K.pill(c, W / 2, 1640, "¿SÍ o NO?", 60, bg=0xEE000000, fg=GOLD)
    if sid == "s1" and lt > 1.2:
        K.tag(c, W / 2, 1840, "BRITISH CHEESE BOARD · 2005", lt - 1.2, accent=WHITE, size=32)
    if sid == "s3" and lt > 1.5:
        K.tag(c, W / 2, 1840, "STILTON: 75 % HOMBRES · 85 % MUJERES", lt - 1.5, accent=BLUE, size=30)
    if sid == "s4" and lt > 1.5:
        K.tag(c, W / 2, 1840, "SIN GRUPO DE CONTROL · LIVE SCIENCE", lt - 1.5, accent=WHITE, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "queso.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "queso.js", overlay=overlay, keep=True)
