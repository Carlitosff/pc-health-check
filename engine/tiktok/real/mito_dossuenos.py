"""2903 MITO 3D (dossuenos.js): '¿Despertarte a mitad de la noche es malo?' → hace siglos se dormía en DOS turnos.
BBC Future (22/02/2012, 'The myth of the eight-hour sleep'): 'In 2001, historian Roger Ekirch of Virginia Tech published a seminal paper,
drawn from 16 years of research' que 'unearths more than 500 references to a segmented sleeping pattern'; el primer sueño 'began about two
hours after dusk, followed by waking period of one or two hours and then a second sleep'; 'Most people stayed in bed, read, wrote and often
prayed', 'some even visited neighbours'. 'In the early 1990s, psychiatrist Thomas Wehr conducted an experiment in which a group of people were
plunged into darkness for 14 hours every day for a month' → 'They slept first for four hours, then woke for one or two hours before falling
into a second four-hour sleep'. Gregg Jacobs: 'Waking up during the night is part of normal human physiology.'
National Geographic (04/01/2024): Ekirch, 'a professor of history at Virginia Tech'; Wehr '1992'.
Matiz obligatorio: la BBC recoge que Ekirch ve aquí una posible raíz del insomnio de mantenimiento → el guion NO dice que nunca sea un problema."""
import sys
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, v3d_run
from core import W, H, WHITE
GOLD = 0xFFFFC23A
V = dict(slug="2903_mito_dormir_de_un_tiron", accent=GOLD, drone=0.02, mood="misterio", send="ENVÍASELO A QUIEN SE DESVELA",
         rehook=("s3", "ESPERA… ¿QUÉ HACÍAN?"), reveal=("s4", "EL EXPERIMENTO"), dare=("s2", "ENVÍASELO A QUIEN SE DESVELA", 1840),
         grade=[("s1", 0, 1), ("s1", .6, .35, .9), ("s3", 3.0, .35, .9), ("s4", .3, 1, 0)],
         segs=[
    dict(id="h", who="nar", say="¿Te despiertas a mitad de la noche? Hace siglos, eso era lo normal.",
         cap="¿Te despiertas *A LAS 3*?", hold=0.3),
    dict(id="s1", who="nar", cut=True, say="Mucha gente dormía en dos turnos, con un rato despierta en medio.",
         cap="Antes se dormía | en *DOS TURNOS*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="El historiador Roger Ekirch encontró más de quinientas menciones a ese primer y segundo sueño.",
         cap="*+500 menciones*: | primer y segundo *SUEÑO*", hold=0.3),
    dict(id="s3", who="nar", cut=True, say="En ese rato rezaban, leían, charlaban, y algunos hasta visitaban a los vecinos.",
         cap="Rezaban, leían… | y *visitaban al vecino*", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="En los noventa, el psiquiatra Thomas Wehr dejó a varias personas catorce horas a oscuras cada día.",
         cap="*14 horas* a oscuras | cada día", hold=0.2),
    dict(id="s5", who="nar", cut=True, say="Acabaron durmiendo cuatro horas, despiertos un rato, y otras cuatro horas más.",
         cap="*4 h* · despiertos · *4 h*", hold=0.4),
    dict(id="cta", who="nar", cut=True, say="Comenta a qué hora te despiertas tú, y envíaselo a quien se desvela.",
         cap="¿A qué hora te despiertas? | *COMENTA*"),
])


def _ss(a, b, x):
    x = min(1, max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x)


def night_bar(c, t, f, y=1450):
    """Barra de la noche 20:00 → 08:00 (2D): primer sueño 4 h, despiertos 1,5 h, segundo sueño 4 h; f 0..1 la recorre con una luna."""
    import skia
    from core import fill, stroke, draw_text, with_alpha
    x0, bw, h = 110, W - 220, 74
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 - 14, y - 70, bw + 28, h + 150), 30, 30), fill(0xD807080D))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y, bw, h), 18, 18), fill(0xFF1B2140))
    x = x0 + bw * 2 / 12
    for w, col, lab in ((4 / 12, 0xFF3A6FD8, "1er SUEÑO · 4 h"), (1.5 / 12, 0xFFFFC23A, "DESPIERTOS"), (4 / 12, 0xFF3A6FD8, "2º SUEÑO · 4 h")):
        vis = min(1, max(0, (f * bw - (x - x0)) / (w * bw)))
        if vis > 0:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y + 6, w * bw * vis, h - 12), 12, 12), fill(col))
        if vis > .5:
            ly = y - 30 if col == 0xFFFFC23A else y + h + 46
            draw_text(c, lab, x + w * bw / 2, ly, 34, with_alpha(col if col != 0xFF3A6FD8 else 0xFF9FC0FF, min(1, (vis - .5) * 4)), outline=6)
        x += w * bw
    draw_text(c, "20:00", x0 + 50, y + h + 46, 28, 0xAAFFFFFF, outline=0)
    draw_text(c, "08:00", x0 + bw - 50, y + h + 46, 28, 0xAAFFFFFF, outline=0)
    mx = x0 + f * bw
    c.drawCircle(mx, y - 6, 22, fill(0xFFFFF4C8))


def overlay(c, t, P):
    sg = K.seg_at(P, t); sid = sg["id"]; lt = t - sg["a"]; d = sg["b"] - sg["a"]
    if sid in ("s1", "s5"):
        night_bar(c, t, _ss(.3 if sid == "s1" else .2, d - .4 if sid == "s1" else d - .5, lt))
    if sid == "s2" and lt > .2:
        n = round(500 * _ss(.2, d * .7, lt))
        K.pill(c, W / 2, 1480, f"+{n} MENCIONES", 64, bg=0xEE000000, fg=GOLD)
    if sid == "s4" and lt > .8:
        K.pill(c, W / 2, 1480, "14 HORAS A OSCURAS", 60, bg=0xEE000000, fg=0xFF9FB4FF)
    if sid == "h":  # gancho visual sin sonido: despertador gigante a las 03:00 que parpadea
        import skia, math
        from core import fill, stroke, draw_text, with_alpha, ease_out, clamp
        a = ease_out(clamp(lt / .3)) if t > .05 else 1.0
        r = skia.Rect.MakeXYWH(W / 2 - 250, 1330, 500, 230)
        c.drawRRect(skia.RRect.MakeRectXY(r, 40, 40), fill(with_alpha(0xFF07080D, .92 * a)))
        c.drawRRect(skia.RRect.MakeRectXY(r, 40, 40), stroke(with_alpha(0xFFFF3A3A, a), 8))
        on = (t % 1.0) < .7 or t < 1.0
        draw_text(c, "03:00" if on else "03 00", W / 2, 1490, 170, with_alpha(0xFFFF4A4A, a), outline=0)
    if sid == "s2" and lt > 1.0:
        K.tag(c, W / 2, 1840, "ROGER EKIRCH · VIRGINIA TECH · 2001", lt - 1.0, accent=GOLD, size=32)
    if sid == "s4" and lt > 1.2:
        K.tag(c, W / 2, 1840, "THOMAS WEHR · AÑOS 90 · UN MES DE PRUEBA", lt - 1.2, accent=WHITE, size=30)
    if sid == "s5" and lt > 1.4:
        K.tag(c, W / 2, 1840, "SI TE CUESTA CADA NOCHE, CONSÚLTALO", lt - 1.4, accent=WHITE, size=30)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.path.insert(0, '/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))
    elif sys.argv[1:] == ["dur"]:
        print(round(K.plan(V)["total"], 1))
    elif len(sys.argv) > 2:
        v3d_run.run3d(V, "dossuenos.js", stills=sys.argv[2].split(","))
    else:
        v3d_run.run3d(V, "dossuenos.js", overlay=overlay, keep=True)
