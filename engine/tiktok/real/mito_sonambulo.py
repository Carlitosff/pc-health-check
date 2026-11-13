"""2103 MITO 3D (sonambulo.js): 'nunca despiertes a un sonámbulo, le puede dar un infarto'.
Fuentes: UAMS Health, 'Is It Dangerous to Wake a Sleepwalker?' (08/03/2019, Dr. Raghu Reddy, neumólogo y especialista en sueño de la
Universidad de Arkansas): 'waking a sleepwalker will not cause them to have a heart attack'; 'Try to ease them back to bed without making forceful attempts'.
BrainFacts/SfN (Kayt Sukel, 11/10/2019): 'They may lash out or fall, which could injure them or the person waking them'; 'it is best to gently encourage
or lead a sleepwalker back to bed'; Randall Wright: 'Imagine waking up and having no idea how you got to where you are'. Sleep Foundation (2025):
'Waking someone who's sleepwalking isn't inherently dangerous'; 'A sleepwalker could fall down the stairs or leave the house'; 'If they are at risk
(near stairs or doors), it's okay to wake them, but do it gently'."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
V = dict(slug="2103_mito_despertar_sonambulo", accent=GOLD, drone=0.03, mood="misterio", badge=None, send="ENVÍASELO A QUIEN HABLA DORMIDO",
         rehook=("s3", "ESPERA… EL PELIGRO DE VERDAD"), reveal=("s4", "QUÉ HACER"), segs=[
    dict(id="h", who="nar", say="Te han dicho que nunca despiertes a un sonámbulo, porque le daría un infarto. Es mentira.",
         cap="¿Despertar a un *SONÁMBULO* es peligroso?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Raghu Reddy, médico del sueño en Arkansas, lo dice claro: despertarle no provoca ningún infarto.",
         cap="¿Infarto? | *NO*", hold=0.2),
    dict(id="s2", who="nar", cut=True, say="Lo que pasa es que se despierta confundido, sin saber cómo ha llegado ahí, y puede asustarse.",
         cap="Se despierta | *CONFUNDIDO*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="El peligro real es dejarle caminar dormido, porque puede caerse por la escalera.",
         cap="El peligro real: | *LA ESCALERA*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Lo mejor es llevarle a la cama con calma, y despertarle con cuidado solo si está en peligro.",
         cap="Llévale *a la cama* | con *CALMA*", hold=0.45),
    dict(id="cta", who="nar", cut=True, say="Comenta si te lo creías, y envíaselo a alguien que camina dormido.",
         cap="¿Te lo creías? | *COMENTA*"),
])


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]
    if sid == "s1" and lt > 2.2:
        K.tag(c, W / 2, 1800, "UAMS HEALTH · 08/03/2019", lt - 2.2, accent=WHITE, size=30)
    if sid == "s3" and lt > 1.6:
        K.tag(c, W / 2, 1800, "SLEEP FOUNDATION · BRAINFACTS 2019", lt - 1.6, accent=WHITE, size=30)
    if sid == "s4" and lt > 1.6:
        K.tag(c, W / 2, 1800, "SIN GRITOS NI SACUDIDAS", lt - 1.6, accent=GOLD, size=34)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "sonambulo.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "sonambulo.js", overlay=overlay)
