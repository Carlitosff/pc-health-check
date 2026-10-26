"""Lote IA 26/10/2026 (101–106): noticias + historia de la IA. Voz v3 Piper."""
import math, sys, random
import skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
import hc
from core import W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, glow
from engine import TF_BLACK, TF_XBOLD, TF_BOLD

OUT = "/home/claude/tiktok/outia"
CTA = "¡Comenta y sígueme para más!"
MONO = skia.Typeface.MakeFromFile("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf") or TF_BOLD


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"]


def text(c, s, x, y, size, col, tf=TF_BOLD, center=True):
    f = skia.Font(tf, size)
    w = f.measureText(s)
    c.drawString(s, x - w / 2 if center else x, y, f, fill(col))


# ---------------------------------------------------------------- fondos IA
_NET = random.Random(11)
NODES = [(_NET.uniform(60, W - 60), _NET.uniform(520, 1560), _NET.uniform(0, 6.28)) for _ in range(46)]
EDGES = [(i, j) for i in range(len(NODES)) for j in range(i + 1, len(NODES))
         if (NODES[i][0] - NODES[j][0]) ** 2 + (NODES[i][1] - NODES[j][1]) ** 2 < 230 ** 2]


def neural(c, t, col, a=1.0):
    c.clear(0xFF03040C)
    g = skia.GradientShader.MakeRadial((W / 2, 1000), 1100, [with_alpha(col, 0.18 * a), 0x00000000])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))
    pts = [(x + math.sin(t * 0.6 + p) * 14, y + math.cos(t * 0.5 + p) * 14) for x, y, p in NODES]
    for k, (i, j) in enumerate(EDGES):
        (x1, y1), (x2, y2) = pts[i], pts[j]
        c.drawLine(x1, y1, x2, y2, stroke(with_alpha(col, 0.18 * a), 2))
        ph = (t * 0.7 + k * 0.137) % 1
        if k % 3 == 0:
            px, py = lerp(x1, x2, ph), lerp(y1, y2, ph)
            glow(c, px, py, 16, col, 0.8 * a)
    for (x, y) in pts:
        c.drawCircle(x, y, 7, fill(with_alpha(col, 0.9 * a)))
        glow(c, x, y, 22, col, 0.3 * a)


def chip(c, x, y, s, t, col, label="AI"):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(-3, 4):
        for side in (-1, 1):
            c.drawRect(skia.Rect.MakeXYWH(k * 40 - 8, side * 150 - (30 if side < 0 else 0), 16, 30), fill(0xFFB8B8C0))
            c.drawRect(skia.Rect.MakeXYWH(side * 150 - (30 if side < 0 else 0), k * 40 - 8, 30, 16), fill(0xFFB8B8C0))
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-125, -125, 250, 250), 26, 26)
    g = skia.GradientShader.MakeLinear([(-125, -125), (125, 125)], [0xFF2A2F3A, 0xFF0E1016])
    c.drawRRect(r, skia.Paint(Shader=g, AntiAlias=True))
    c.drawRRect(r, stroke(with_alpha(col, 0.6 + 0.4 * math.sin(t * 3)), 5))
    text(c, label, 0, 30, 96, col, TF_BLACK)
    c.restore()
    glow(c, x, y, 260 * s, col, 0.25 + 0.15 * math.sin(t * 3))


def phone(c, x, y, s, t, lines, col, lt):
    """Móvil con burbujas de chat que aparecen. lines: [(quién, texto)]"""
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-230, -440, 460, 880), 60, 60)
    c.drawRRect(body, fill(0xFF101216)); c.drawRRect(body, stroke(0xFF3A3F4A, 6))
    scr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-208, -418, 416, 836), 44, 44)
    c.drawRRect(scr, fill(0xFF0B0D12))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-60, -405, 120, 30), 15, 15), fill(0xFF000000))
    yy = -330
    for i, (who, s_) in enumerate(lines):
        a = clamp((lt - i * 0.9) / 0.3)
        if a <= 0:
            break
        f = skia.Font(TF_BOLD, 28)
        w = min(330, f.measureText(s_) + 40)
        me = who == "yo"
        bx = 190 - w if me else -190
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(bx, yy + (1 - a) * 20, w, 64), 24, 24),
                    fill(with_alpha(col if me else 0xFF2A2F3A, a)))
        c.drawString(s_, bx + 20, yy + 42 + (1 - a) * 20, f, fill(with_alpha(WHITE, a)))
        yy += 90
    c.restore()


def terminal(c, x, y, w, h, lines, lt, col):
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 22, 22)
    c.drawRRect(r, fill(with_alpha(0xFF050608, 0.92))); c.drawRRect(r, stroke(with_alpha(col, 0.7), 3))
    for k, cc in enumerate((0xFFFF5F57, 0xFFFEBC2E, 0xFF28C840)):
        c.drawCircle(x - w / 2 + 34 + k * 30, y - h / 2 + 30, 9, fill(cc))
    f = skia.Font(MONO, 34)
    chars = int(lt * 32)
    yy = y - h / 2 + 100
    for ln in lines:
        show = ln[:max(0, chars)]
        chars -= len(ln)
        c.drawString(show, x - w / 2 + 34, yy, f, fill(col))
        if 0 < len(show) < len(ln) or (chars <= 0 and show == ln and len(show)):
            pass
        yy += 52
        if chars <= 0:
            if int(lt * 3) % 2 == 0:
                c.drawRect(skia.Rect.MakeXYWH(x - w / 2 + 34 + f.measureText(show) + 4, yy - 90, 18, 40), fill(col))
            break


def news(c, lt, label, col):
    a = ease_back(prog(lt, 0, 0.4), 1.6)
    if a <= 0:
        return
    c.save(); c.translate(W / 2, 660); c.scale(a, a)
    f = skia.Font(TF_BLACK, 40); w = f.measureText(label) + 70
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -40, w, 76), 38, 38), fill(col))
    c.drawCircle(-w / 2 + 34, -2, 10, fill(WHITE if int(lt * 2) % 2 == 0 else with_alpha(WHITE, 0.3)))
    c.drawString(label, -w / 2 + 52, 12, f, fill(WHITE))
    c.restore()


# ---------------------------------------------------------------- 101 OpenAI Astra
def s_astra(c, t, P, V):
    sid, lt = seg(P, t)
    neural(c, t, 0xFF10A37F)
    chip(c, W / 2, 1040, 1.25, t, 0xFF10A37F, "6.1")
    if sid in ("h", "s1"):
        news(c, t, "ÚLTIMA HORA · IA", 0xFFE0263C)
    if sid == "s2":
        terminal(c, W / 2, 1520, 900, 300, ["> safety_eval --model astra", "> RESULT: FAIL", "> launch: CANCELLED"], lt, 0xFF3CFF8A)
    if sid == "s3":
        hc.stamp(c, "CANCELADO", W / 2, 1540, lt, 0.2, 130)
    if sid == "s4":
        hc.big(c, "AGENTES", W / 2, 1560, 140, V["accent"], lt, 0.1)


V101 = dict(slug="101_openai_astra", accent=0xFF10A37F, drone=0.02, scene=s_astra, segs=[
    dict(id="h", who="nar", say="OpenAI tenía un modelo nuevo listo para presentar… y lo frenó a última hora.",
         cap="OpenAI tenía un modelo *listo*… | y lo *FRENÓ* | a última hora"),
    dict(id="s1", who="nar", cut=True, say="Se llamaba GPT seis punto uno Astra, y su lanzamiento estaba previsto para octubre.",
         cap="*GPT-6.1 Astra*, | previsto para *octubre*"),
    dict(id="s2", who="nar", cut=True, say="Pero a finales de septiembre se publicó que no había superado sus pruebas internas de seguridad.",
         cap="No superó sus *pruebas* | internas de *seguridad*"),
    dict(id="s3", who="nar", cut=True, say="Y la empresa decidió no lanzarlo.", cap="Y decidieron | *no lanzarlo*"),
    dict(id="s4", who="nar", cut=True, say="Pasa justo cuando hay cada vez más vigilancia sobre las IAs que actúan solas, los llamados agentes.",
         cap="Cada vez más vigilancia | sobre las IAs que actúan *solas*: | los *agentes*"),
    dict(id="cta", who="nar", cut=True, say="¿Te parece bien que la frenen? Comenta y sígueme para más noticias de IA.",
         cap="¿Bien hecho? | *COMENTA* | y sígueme para más *IA*"),
])


# ---------------------------------------------------------------- 102 Siri en español
def s_siri(c, t, P, V):
    sid, lt = seg(P, t)
    neural(c, t, 0xFFB04DFF, 0.7)
    # orbe tipo asistente
    ox, oy = W / 2, 760
    for k in range(4):
        r = 110 + k * 26 + math.sin(t * 3 + k) * 12
        cols = [0xFF4DE1FF, 0xFFB04DFF, 0xFFFF4D9A, 0xFF6A5AF0]
        glow(c, ox + math.sin(t * 2 + k) * 20, oy + math.cos(t * 1.7 + k) * 20, r, cols[k], 0.5)
    if sid in ("s2", "s3", "s4"):
        phone(c, W / 2, 1300, 0.62, t, [("yo", "Oye, ¿qué tiempo hará?"), ("ia", "Mañana sol, 22 grados ☀"),
                                        ("yo", "Pon una alarma a las 7"), ("ia", "Hecho. Alarma 7:00")],
              0xFF6A5AF0, t - P["tl"]["s2"][0])
    if sid == "h":
        news(c, lt, "LLEGA EN ESPAÑOL", 0xFF6A5AF0)
    if sid == "s1":
        hc.big(c, "iOS 27.2", W / 2, 1450, 150, V["accent"], lt, 0.1)


V102 = dict(slug="102_siri_espanol", accent=0xFFB98CFF, drone=0.02, scene=s_siri, segs=[
    dict(id="h", who="nar", say="La nueva Siri con inteligencia artificial por fin va a hablar español.",
         cap="La nueva *Siri* con IA | por fin habla | *ESPAÑOL*"),
    dict(id="s1", who="nar", cut=True, say="Apple la ha metido en la beta de iOS veintisiete punto dos, junto a francés, japonés, coreano y portugués.",
         cap="Ya está en la *beta* | de *iOS 27.2*"),
    dict(id="s2", who="nar", cut=True, say="Hasta ahora, en España no podíamos usarla.", cap="Hasta ahora, en España… | *no podíamos usarla*"),
    dict(id="s3", who="nar", say="Con esto, el iPhone pasa a entenderte de forma mucho más natural… en tu idioma.",
         cap="El iPhone te entenderá | mucho más *natural*… | en *tu idioma*"),
    dict(id="s4", who="nar", cut=True, say="La versión para todos está prevista en las próximas semanas.", cap="Para todos: | en las *próximas semanas*"),
    dict(id="cta", who="nar", cut=True, say="¿La vas a usar o sigues sin fiarte? Comenta y sígueme para más IA.",
         cap="¿La vas a usar? | *COMENTA* | y *SÍGUEME*"),
])


# ---------------------------------------------------------------- 103 IA apagada por EE.UU.
def flag_stripes(c, t, a):
    for k in range(7):
        c.drawRect(skia.Rect.MakeXYWH(0, 1300 + k * 40, W, 20), fill(with_alpha(0xFFB22234, 0.25 * a)))


def s_apagon(c, t, P, V):
    sid, lt = seg(P, t)
    off = sid in ("s2",)
    neural(c, t, 0xFFD97757, 0.15 if off else 1.0)
    chip(c, W / 2, 1000, 1.2, t, 0xFF5A5A5A if off else 0xFFD97757, "OFF" if off else "AI")
    if sid in ("h", "s1"):
        news(c, t, "PASÓ ESTE AÑO", 0xFFD97757)
    if sid == "s1":
        hc.big(c, "12 JUNIO", W / 2, 1520, 140, V["accent"], lt, 0.1)
    if sid == "s2":
        hc.stamp(c, "SUSPENDIDO", W / 2, 1500, lt, 0.2, 120)
    if sid == "s3":
        K.counter(c, t, lt - 0.2, lambda p: str(int(round(19 * p))), "DÍAS APAGADA", V["accent"], y=1560)
    if sid == "s4":
        hc.big(c, "1 JULIO", W / 2, 1520, 140, 0xFF3CFF8A, lt, 0.1)


V103 = dict(slug="103_ia_apagada", accent=0xFFFFA27A, drone=0.02, scene=s_apagon, segs=[
    dict(id="h", who="nar", say="Este año, una empresa tuvo que apagar dos de sus inteligencias artificiales por orden del gobierno de Estados Unidos.",
         cap="Una empresa tuvo que *APAGAR* | sus IAs | por orden de *EE. UU.*"),
    dict(id="s1", who="nar", cut=True, say="Pasó el doce de junio. Anthropic, la empresa de Claude, acababa de lanzar dos modelos nuevos, Fable y Mythos.",
         cap="*12 de junio*. Anthropic | acababa de lanzar | *Fable* y *Mythos*"),
    dict(id="s2", who="nar", cut=True, say="Tres días después, tuvo que suspender el acceso para cumplir unos controles de exportación del Departamento de Comercio.",
         cap="Tuvo que *suspender* el acceso | por *controles de exportación*"),
    dict(id="s3", who="nar", cut=True, say="Estuvieron apagados casi tres semanas.", cap="Casi *3 semanas* | apagados"),
    dict(id="s4", who="nar", cut=True, say="El treinta de junio se levantaron los controles, y el uno de julio volvieron a estar disponibles.",
         cap="Se levantaron los controles | y el *1 de julio* | volvieron"),
    dict(id="cta", who="nar", cut=True, say="¿Sabías que esto había pasado? Comenta y sígueme para más noticias de IA.",
         cap="¿Lo sabías? | *COMENTA* | y *SÍGUEME*"),
])


# ---------------------------------------------------------------- 104 Jugada 37 (AlphaGo)
def go_board(c, t, lt, stones, hl=None):
    s = 52; n = 13; x0 = W / 2 - s * (n - 1) / 2; y0 = 1020 - s * (n - 1) / 2
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 - 50, y0 - 50, s * (n - 1) + 100, s * (n - 1) + 100), 18, 18), fill(0xFFDCB36A))
    for i in range(n):
        c.drawLine(x0, y0 + i * s, x0 + s * (n - 1), y0 + i * s, stroke(0xFF5A3A10, 3))
        c.drawLine(x0 + i * s, y0, x0 + i * s, y0 + s * (n - 1), stroke(0xFF5A3A10, 3))
    for k, (i, j, col) in enumerate(stones):
        if lt < k * 0.12:
            break
        x, y = x0 + i * s, y0 + j * s
        g = skia.GradientShader.MakeRadial((x - 8, y - 8), 30, [0xFF606060, 0xFF050505] if col else [0xFFFFFFFF, 0xFFC8C8C8])
        c.drawCircle(x + 3, y + 4, 23, fill(with_alpha(0xFF000000, 0.3)))
        c.drawCircle(x, y, 23, skia.Paint(Shader=g, AntiAlias=True))
    if hl:
        x, y = x0 + hl[0] * s, y0 + hl[1] * s
        glow(c, x, y, 90, 0xFF4DE1FF, 0.8 + 0.2 * math.sin(t * 6))
        c.drawCircle(x, y, 23, fill(0xFF050505)); c.drawCircle(x, y, 36, stroke(0xFF4DE1FF, 6))


_R = random.Random(37)
STONES = [(_R.randint(0, 12), _R.randint(0, 12), k % 2) for k in range(34)]


def s_go(c, t, P, V):
    sid, lt = seg(P, t)
    hc.aurora(c, t, 0xFF1A1206, 0xFF0A1A2A)
    hl = (9, 4) if sid in ("s2", "s3", "s4", "cta") else None
    go_board(c, t, t, STONES, hl)
    if sid == "s1":
        hc.big(c, "2016", W / 2, 1560, 160, V["accent"], lt, 0.1)
    if sid == "s2":
        hc.big(c, "JUGADA 37", W / 2, 1560, 140, V["accent"], lt, 0.1)
    if sid == "s3":
        hc.big(c, "1 / 10.000", W / 2, 1560, 140, V["accent"], lt, 0.1)
    if sid == "s4":
        hc.stamp(c, "GANÓ 4-1", W / 2, 1560, lt, 0.2, 130)


V104 = dict(slug="104_jugada_37", accent=0xFF4DE1FF, drone=0.02, scene=s_go, segs=[
    dict(id="h", who="nar", say="Hubo una jugada de una inteligencia artificial que dejó a los expertos convencidos de que era un error.",
         cap="Una jugada de una *IA* | que parecía | un *ERROR*"),
    dict(id="s1", who="nar", cut=True, say="Seúl, dos mil dieciséis. AlphaGo, de Google DeepMind, contra Lee Sedol, uno de los mejores jugadores de Go del mundo.",
         cap="*2016*. *AlphaGo* | contra *Lee Sedol*, | leyenda del Go"),
    dict(id="s2", who="nar", cut=True, say="En la segunda partida, la máquina hizo la jugada treinta y siete.", cap="Segunda partida: | la *jugada 37*"),
    dict(id="s3", who="nar", cut=True, say="Según la propia IA, un humano la habría hecho una vez de cada diez mil. Los comentaristas pensaron que se había equivocado.",
         cap="Un humano la haría | *1 vez de cada 10.000*. | Creyeron que era un error"),
    dict(id="s4", who="nar", cut=True, say="No lo era. Fue clave para ganar esa partida… y AlphaGo ganó la serie cuatro a uno.",
         cap="No lo era. | AlphaGo ganó | *4 a 1*"),
    dict(id="cta", who="nar", cut=True, say="Y en la cuarta partida, Lee Sedol hizo su propia jugada imposible. Te la cuento mañana. Sígueme.",
         cap="Y Lee Sedol respondió | con su *jugada imposible*… | mañana. *SÍGUEME*"),
])


# ---------------------------------------------------------------- 105 ELIZA
def s_eliza(c, t, P, V):
    sid, lt = seg(P, t)
    c.clear(0xFF020802)
    for k in range(0, H, 6):  # scanlines CRT
        c.drawRect(skia.Rect.MakeXYWH(0, k, W, 2), fill(with_alpha(0xFF3CFF6A, 0.03)))
    glow(c, W / 2, 1000, 700, 0xFF3CFF6A, 0.12)
    if sid in ("h", "s1"):
        hc.big(c, "1966", W / 2, 760, 200, 0xFF3CFF6A, t, 0.2)
    lines = ["ELIZA> HOLA. CUENTAME", "  QUE TE PREOCUPA.", "> ESTOY TRISTE", "ELIZA> POR QUE DICES", "  QUE ESTAS TRISTE?",
             "> MI MADRE NO ME ENTIENDE", "ELIZA> HABLAME DE TU", "  FAMILIA."]
    a = P["tl"]["s1"][0]
    if t > a:
        terminal(c, W / 2, 1180, 960, 560, lines, t - a, 0xFF3CFF6A)
    if sid == "s3":
        hc.stamp(c, "SALGA, POR FAVOR", W / 2, 1600, lt, 0.4, 90)
    if sid == "s4":
        hc.big(c, "EFECTO ELIZA", W / 2, 1600, 110, V["accent"], lt, 0.1)


V105 = dict(slug="105_eliza", accent=0xFF6CFF8A, drone=0.02, scene=s_eliza, segs=[
    dict(id="h", who="nar", say="El primer chatbot de la historia se creó en mil novecientos sesenta y seis. Y la gente ya se enganchaba a él.",
         cap="El primer *chatbot*: | *1966*. | Y la gente ya se *enganchaba*"),
    dict(id="s1", who="nar", cut=True, say="Se llamaba ELIZA, y lo programó Joseph Weizenbaum en el MIT. Imitaba a un psicoterapeuta, devolviéndote tus propias frases como preguntas.",
         cap="*ELIZA*, del *MIT*. | Imitaba a un *terapeuta* | con tus propias frases"),
    dict(id="s2", who="nar", say="No entendía nada. Solo buscaba palabras clave.", cap="No entendía *nada*. | Solo palabras clave"),
    dict(id="s3", who="nar", cut=True, say="Aun así, la secretaria de Weizenbaum, que sabía cómo funcionaba, le pidió que saliera de la sala para hablar con ELIZA en privado.",
         cap="Su propia *secretaria* | le pidió que *saliera de la sala* | para hablar con ELIZA a solas"),
    dict(id="s4", who="nar", cut=True, say="Hoy a eso se le llama efecto ELIZA: ver una mente donde solo hay un programa.",
         cap="Hoy se llama *efecto ELIZA*: | ver una *mente* | donde solo hay un programa"),
    dict(id="cta", who="nar", cut=True, say="¿Te ha pasado con alguna IA? " + CTA, cap="¿Te ha pasado? | *COMENTA* | y *SÍGUEME*"),
])


# ---------------------------------------------------------------- 106 Dartmouth: resolver la IA en un verano
def s_verano(c, t, P, V):
    sid, lt = seg(P, t)
    neural(c, t, 0xFFFFC23C, 0.6 if sid not in ("s4",) else 1.0)
    # documento máquina de escribir
    if sid in ("h", "s1", "s2", "s3"):
        c.save(); c.translate(W / 2, 1150); c.rotate(-3)
        c.drawRect(skia.Rect.MakeXYWH(-330, -380, 660, 760), fill(0xFFF3EBD6))
        f = skia.Font(MONO, 26)
        for k, ln in enumerate(["A PROPOSAL FOR THE", "DARTMOUTH SUMMER", "RESEARCH PROJECT ON", "ARTIFICIAL INTELLIGENCE", "",
                                "J. McCarthy, M. Minsky,", "N. Rochester, C. Shannon", "", "August 31, 1955", "",
                                "...a 2 month, 10 man study", "of artificial intelligence..."]):
            c.drawString(ln, -290, -300 + k * 50, f, fill(0xFF2A2418))
        if sid in ("s2", "s3"):
            c.drawRect(skia.Rect.MakeXYWH(-296, 196, 560, 36), fill(with_alpha(0xFFFFE14D, 0.45)))
        c.restore()
    if sid == "s1":
        hc.big(c, "1955", W / 2, 1640, 150, V["accent"], lt, 0.1)
    if sid == "s3":
        hc.big(c, "2 MESES · 10 PERSONAS", W / 2, 1640, 90, V["accent"], lt, 0.1)
    if sid == "s4":
        K.counter(c, t, lt - 0.2, lambda p: str(int(round(70 * p))) + " AÑOS", "DESPUÉS… SEGUIMOS", V["accent"], y=1560)


V106 = dict(slug="106_dartmouth", accent=0xFFFFC23C, drone=0.02, scene=s_verano, segs=[
    dict(id="h", who="nar", say="Los inventores de la inteligencia artificial creían que podían resolverla en un solo verano.",
         cap="Creían que podían resolver | la *IA* | en *UN VERANO*"),
    dict(id="s1", who="nar", cut=True, say="En mil novecientos cincuenta y cinco, John McCarthy y otros científicos escribieron una propuesta. Ahí apareció por primera vez el término inteligencia artificial.",
         cap="*1955*: John *McCarthy*. | Primera vez que se escribe | *inteligencia artificial*"),
    dict(id="s2", who="nar", cut=True, say="Pedían dinero para un taller en la universidad de Dartmouth, el verano siguiente.",
         cap="Un taller en *Dartmouth*, | el verano de *1956*"),
    dict(id="s3", who="nar", say="¿Su plan? Un estudio de dos meses, con diez personas.", cap="¿El plan? | *2 meses*, | *10 personas*"),
    dict(id="s4", who="nar", cut=True, say="Setenta años después… seguimos en ello.", cap="*70 años* después… | seguimos en ello"),
    dict(id="cta", who="nar", cut=True, say="¿Cuántos años crees que faltan? " + CTA, cap="¿Cuánto falta? | *COMENTA* | y *SÍGUEME*"),
])

VIDEOS = [V101, V102, V103, V104, V105, V106]


def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
    return scene


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = "auto" if len(sys.argv) > 2 else None
    for i in idxs:
        K.run(VIDEOS[i], make_scene(VIDEOS[i]), OUT, preview=pv)
