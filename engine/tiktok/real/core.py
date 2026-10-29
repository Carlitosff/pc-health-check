"""Núcleo de los vídeos 'realistas': plan de voz multi-hablante, overlays (subtítulos, contador, quiz,
etiquetas), efectos de cámara, audio masterizado y render."""
import math, os, random, subprocess, sys, types
import numpy as np
import skia

sys.path.insert(0, "/home/claude/tiktok")
import voice, curio, curio2
from engine import (W, H, SR, INK, WHITE, TF_BLACK, TF_XBOLD, TF_BOLD, Captions, clamp, lerp, prog, ease_out,
                    ease_in_out, ease_back, ease_elastic, with_alpha, fill, stroke, font, text_w, draw_text, pill,
                    Mixer, render)

HANDLE = "@videosparadormir2018"
# v3 (26/10/2026): voces Piper de locutores reales (más humanas que Kokoro en español)
VOICES = {"nar": ("piper:es_ES-davefx-medium:0", 1.12), "q": ("piper:es_ES-sharvard-medium:1", 1.08)}
COUNT_DUR = 2.5
GAP = 0.08
GREEN = 0xFF2FD46B
QCOL = 0xFFFF7AD9
SCRATCH = "/home/claude/tiktok/prev/"
LOOP_DUR = 0.45  # v6: fundido final al frame 0 (bucle invisible)
os.makedirs(SCRATCH, exist_ok=True)


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ------------------------------------------------------------------ plan
def plan(V):
    """V['segs']: lista de dicts con id, who ('nar'|'q'), say, cap y opcional quiz=dict(a,b,ans).
    Tras un segmento con quiz se inserta la cuenta atrás 'id_count'."""
    segs = []
    for s in V["segs"]:
        segs.append(dict(s))
        if s.get("quiz"):
            segs.append(dict(id=s["id"] + "_count", kind="count", cap="¿*A* o *B*?"))
    cur = 0.0
    placed, cap_items = [], []
    for sg in segs:
        if sg.get("kind") == "count":
            a, b = cur, cur + COUNT_DUR
            cap_items.append((a, b, sg["cap"], [a + 0.05, a + 0.3, a + 0.55], "q"))
            sg["a"], sg["b"] = a, b
            cur = b
            continue
        vname, speed = VOICES[sg["who"]]
        aud = voice._synth_cached(sg["say"], vname, speed)
        d = len(aud) / 24000
        start = cur + 0.04
        placed.append((sg["who"], start, aud))
        b = start + d + GAP + sg.get("hold", 0.0)
        sg["a"], sg["b"], sg["speech"] = cur, b, (start, start + d)
        chunks = [ch.strip() for ch in sg["cap"].split("|") if ch.strip()]
        allw = [w for ch in chunks for w in ch.split()]
        tot = sum(len(w.strip("*¡!¿?")) + 1 for w in allw)
        acc, times = 0, []
        for w in allw:
            times.append(start + d * acc / tot)
            acc += len(w.strip("*¡!¿?")) + 1
        k = 0
        for ci, ch in enumerate(chunks):
            n = len(ch.split())
            t_in = times[k] - 0.08
            t_out = times[k + n] - 0.04 if k + n < len(times) else b
            cap_items.append((cur if ci == 0 else max(cur, t_in), t_out, ch, times[k:k + n], sg["who"]))
            k += n
        cur = b
    total = cur + 0.5
    segs[-1]["b"] = total + 1
    n = int((total + 1) * SR)
    vo = {"nar": np.zeros(n), "q": np.zeros(n)}
    for who, start, aud in placed:
        sig = voice._resample(aud)
        i = int(start * SR)
        j = min(n, i + len(sig))
        vo[who][i:j] += sig[: j - i]
    caps = Captions([(a, b, txt) for (a, b, txt, _, _) in cap_items], y=470, size=88, max_w=900, hl=V["accent"])
    for it, (_, _, _, times, who) in zip(caps.items, cap_items):
        it["times"] = (times + [times[-1]] * len(it["words"]))[: len(it["words"])] if times else [it["a"]] * len(it["words"])
        it["hl"] = QCOL if who == "q" else V["accent"]
    first = caps.items[0]
    first["a"] = -0.5
    first["times"] = [-0.3] * len(first["times"])
    caps.draw = types.MethodType(_cap_draw, caps)
    caps.hook_end = segs[0]["b"] - 0.05
    tl = {sg["id"]: (sg["a"], sg["b"]) for sg in segs}
    hl_times = [tt for it in caps.items for (w, hl), tt in zip(it["words"], it["times"]) if hl and tt > 0.3]
    return dict(segs=segs, tl=tl, vo=vo, caps=caps, total=total, hl_times=hl_times)


def _cap_draw(self, c, t):
    it = self.active(t)
    if not it:
        return
    old = self.hl
    self.hl = it.get("hl", old)
    if it["a"] < getattr(self, "hook_end", 0):
        # v5 (27/10): GANCHO XL. La frase del gancho sale un 20% más grande, sobre una banda oscura degradada
        # (legible sobre cualquier fondo) y ya completa en el frame 0 -> la miniatura/primer frame se entiende solo.
        # Motivo: en IG el 'reel view rate' (>3 s) separa los vídeos de 1.000-2.000 vistas (60-72%) de los de 100-250 (23-50%).
        os_, ow_ = self.size, self.max_w
        self.size, self.max_w = os_ * 1.2, 980
        out = prog(t, it["b"] - 0.08, it["b"])
        band = skia.GradientShader.MakeLinear([(0, self.y - 330), (0, self.y + 360)],
                                              [0x00000000, with_alpha(0xFF000000, 0.42 * (1 - out)),
                                               with_alpha(0xFF000000, 0.42 * (1 - out)), 0x00000000], [0, 0.3, 0.7, 1])
        c.drawRect(skia.Rect.MakeXYWH(0, self.y - 330, W, 690), skia.Paint(Shader=band))
        curio2.captions_draw(self, c, t)
        self.size, self.max_w = os_, ow_
    else:
        curio2.captions_draw(self, c, t)
    self.hl = old


def seg_at(P, t):
    cur = P["segs"][0]
    for sg in P["segs"]:
        if sg["a"] <= t:
            cur = sg
    return cur


def local(P, sid, t):
    a, b = P["tl"].get(sid, (1e9, 1e9))
    return t - a, b - a


# ------------------------------------------------------------------ fondo de estrellas con paralaje
class Stars:
    def __init__(self, seed=1, n=900):
        rnd = random.Random(seed)
        self.layers = []
        for depth, count, rmax in ((0.15, n // 2, 1.6), (0.35, n // 3, 2.4), (0.7, n // 6, 3.4)):
            pts = [(rnd.uniform(-1.5, 1.5) * W, rnd.uniform(-1.5, 1.5) * H, rnd.uniform(0.6, rmax),
                    rnd.uniform(0.35, 1.0), rnd.uniform(0, 6.28), rnd.random()) for _ in range(count)]
            self.layers.append((depth, pts))
        # banda de la Vía Láctea
        self.band = [(rnd.gauss(0, 1) * 1.4 * W, rnd.gauss(0, 0.16) * W, rnd.uniform(0.5, 1.6), rnd.uniform(0.1, 0.45))
                     for _ in range(2200)]

    def draw(self, c, t, camx=0.0, camy=0.0, zoom=1.0, alpha=1.0, streak=0.0, band=True):
        if band:
            c.save()
            c.translate(W / 2 - camx * 0.05, H / 2 - camy * 0.05)
            c.rotate(-32)
            sh = skia.GradientShader.MakeLinear([(0, -260), (0, 260)], [0x00000000, with_alpha(0xFF6A5A9A, 0.22 * alpha),
                                                                       with_alpha(0xFF9A8AC0, 0.30 * alpha),
                                                                       with_alpha(0xFF6A5A9A, 0.22 * alpha), 0x00000000],
                                                [0, 0.3, 0.5, 0.7, 1])
            c.drawRect(skia.Rect.MakeLTRB(-2 * W, -260, 2 * W, 260), skia.Paint(Shader=sh))
            p = skia.Paint(AntiAlias=True)
            for (x, y, r, a) in self.band:
                p.setColor(with_alpha(0xFFE8E4FF, a * alpha))
                c.drawCircle(x, y, r, p)
            c.restore()
        p = skia.Paint(AntiAlias=True)
        for depth, pts in self.layers:
            z = 1 + (zoom - 1) * depth
            for (x, y, r, a, ph, tint) in pts:
                sx = (x - camx * depth) * z + W / 2
                sy = (y - camy * depth) * z + H / 2
                sx = (sx + 3 * W) % (3 * W) - W
                sy = (sy + 3 * H) % (3 * H) - H
                if -20 < sx < W + 20 and -20 < sy < H + 20:
                    tw = 0.75 + 0.25 * math.sin(t * (1 + 2 * tint) + ph)
                    col = 0xFFFFFFFF if tint < 0.6 else (0xFFBFD4FF if tint < 0.85 else 0xFFFFE2B8)
                    if streak > 0.01:
                        dx, dy = sx - W / 2, sy - H / 2
                        L = streak * depth * 0.6
                        q = skia.Paint(AntiAlias=True, Color=with_alpha(col, a * tw * alpha), StrokeWidth=r * 1.4,
                                       Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
                        c.drawLine(sx, sy, sx + dx * L, sy + dy * L, q)
                    else:
                        p.setColor(with_alpha(col, a * tw * alpha))
                        c.drawCircle(sx, sy, r * z ** 0.3, p)


def glow(c, x, y, r, color, a=1.0):
    sh = skia.GradientShader.MakeRadial((x, y), r, [with_alpha(color, a), with_alpha(color, a * 0.35), with_alpha(color, 0)],
                                        [0, 0.25, 1])
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, AntiAlias=True, BlendMode=skia.BlendMode.kPlus))


def vignette(c, strength=0.55):
    sh = skia.GradientShader.MakeRadial((W / 2, H / 2), H * 0.72, [0x00000000, with_alpha(0xFF000000, strength)], [0.55, 1])
    c.drawPaint(skia.Paint(Shader=sh))


_grain = None


def grain(c, t, amount=0.05):
    global _grain
    if _grain is None:
        rng = np.random.default_rng(5)
        imgs = []
        for k in range(6):
            g = rng.normal(0.5, 0.2, (H // 2, W // 2))
            a = np.clip(g, 0, 1)
            rgba = np.zeros((H // 2, W // 2, 4), np.uint8)
            v = (a * 255).astype(np.uint8)
            rgba[..., 0] = rgba[..., 1] = rgba[..., 2] = v
            rgba[..., 3] = 255
            imgs.append(skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType))
        _grain = imgs
    img = _grain[int(t * 24) % len(_grain)]
    p = skia.Paint(Alphaf=amount, BlendMode=skia.BlendMode.kOverlay)
    c.drawImageRect(img, skia.Rect.MakeWH(W, H), skia.SamplingOptions(), p)


# ------------------------------------------------------------------ overlays
def counter(c, t, lt, text_fn, label, accent, y=1390, dur=1.6, size=128):
    """text_fn(p) devuelve el texto para el progreso p (0..1)."""
    if lt < 0:
        return
    s = ease_back(prog(lt, 0, 0.35), 2.2)
    p = ease_out(prog(lt, 0.1, dur))
    txt = text_fn(p)
    f = font(size)
    w = text_w(txt, f)
    if w > 980:
        size = size * 980 / w
    bump = 1 + 0.08 * math.exp(-max(0, lt - dur) * 6) * (lt > dur)
    c.save()
    c.translate(W / 2, y)
    c.scale(s * bump, s * bump)
    glow(c, 0, -size * 0.3, size * 2.2, accent, 0.18)
    draw_text(c, txt, 0, size * 0.36, size, WHITE, outline=16)
    c.restore()
    if label:
        pill(c, W / 2, y + size * 0.62 + 30, label, 38, bg=accent, fg=INK, scale=ease_back(prog(lt, 0.3, 0.6)))


def fmt(n, dec=0):
    if dec:
        s = f"{n:,.{dec}f}"
    else:
        s = f"{int(round(n)):,}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def tag(c, x, y, txt, lt, accent=WHITE, size=34, line_to=None):
    s = ease_back(prog(lt, 0, 0.3), 2.2)
    if s <= 0:
        return
    if line_to:
        c.drawLine(x, y, line_to[0], line_to[1], stroke(with_alpha(WHITE, 0.8 * clamp(s)), 3))
        c.drawCircle(line_to[0], line_to[1], 6, fill(WHITE))
    pill(c, x, y, txt, size, bg=accent, fg=INK, scale=s)


def quiz(c, t, P, sid, accent):
    """Panel A/B: aparece en el segmento sid, cuenta atrás en sid_count, revelación en el siguiente."""
    a0, _ = P["tl"].get(sid, (1e9, 0))
    if t < a0:
        return 0.0
    segs = P["segs"]
    idx = [i for i, s in enumerate(segs) if s["id"] == sid][0]
    q = segs[idx]["quiz"]
    ca, cb = P["tl"][sid + "_count"]
    ra, rb = segs[idx + 2]["a"], segs[idx + 2]["b"]
    rb = min(rb, ra + 1.7)
    if t > rb:
        return 0.0
    lt = t - a0
    rv = clamp((t - ra) / 0.45) if t >= ra else 0.0
    fade = 1 - prog(t, rb - 0.35, rb)
    dim = 0.45 * clamp(lt / 0.3) * fade
    c.drawRect(skia.Rect.MakeWH(W, H), fill(with_alpha(0xFF000000, dim)))
    y = 1330
    for side, (lab, xx) in enumerate(((q["a"], 285), (q["b"], 795))):
        s = ease_back(prog(lt, 0.05 + 0.12 * side, 0.4 + 0.12 * side), 2.0) * (0.7 + 0.3 * fade) * (fade > 0.01)
        if s <= 0:
            continue
        ok = q["ans"] == "ab"[side]
        state = "n" if rv == 0 else ("r" if ok else "w")
        c.save()
        c.translate(xx, y)
        sc = s * (1 + (0.08 * math.exp(-(t - ra) * 4) if state == "r" else 0) - (0.05 * rv if state == "w" else 0))
        c.scale(sc, sc)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-235, -95, 470, 190), 40, 40)
        c.drawRRect(rr.makeOffset(0, 10), fill(0x66000000))
        base = with_alpha(0xFF101426, 0.78)
        bord = WHITE
        if state == "r":
            base = with_alpha(GREEN, 0.35 + 0.4 * rv)
            bord = GREEN
        elif state == "w":
            base = with_alpha(0xFF101426, 0.6)
            bord = 0xFF6B7088
        c.drawRRect(rr, fill(base))
        c.drawRRect(rr, stroke(bord, 7))
        c.drawCircle(-175, 0, 42, fill(WHITE if state != "w" else 0xFF6B7088))
        draw_text(c, "AB"[side], -175, 22, 56, INK, shadow=False)
        f = font(52)
        lw = text_w(lab, f)
        sz = 52 if lw < 300 else 52 * 300 / lw
        draw_text(c, lab, 40, sz * 0.36, sz, WHITE if state != "w" else 0xFF9AA0B8, shadow=False)
        if state == "r":
            ps = ease_back(clamp(rv * 1.8), 2.5)
            c.save(); c.translate(205, -85); c.scale(ps, ps)
            c.drawCircle(0, 0, 40, fill(GREEN)); c.drawCircle(0, 0, 40, stroke(WHITE, 6))
            pth = skia.Path(); pth.moveTo(-17, 0); pth.lineTo(-4, 14); pth.lineTo(19, -13)
            c.drawPath(pth, stroke(WHITE, 9)); c.restore()
        c.restore()
    # cuenta atrás
    if ca <= t < cb:
        lt2 = t - ca
        step = (COUNT_DUR - 0.1) / 3
        n = 3 - min(2, int(lt2 / step))
        sub = (lt2 % step) / step
        x0, y0 = W / 2, 1110
        c.drawCircle(x0, y0 + 8, 105, fill(0x66000000))
        c.drawCircle(x0, y0, 105, fill(with_alpha(0xFF101426, 0.9)))
        arc = skia.Path()
        arc.addArc(skia.Rect.MakeXYWH(x0 - 90, y0 - 90, 180, 180), -90, 360 * (1 - clamp(lt2 / (COUNT_DUR - 0.1))))
        c.drawPath(arc, stroke(accent, 16))
        sc = 1 + 0.35 * math.exp(-sub * 7)
        c.save(); c.translate(x0, y0); c.scale(sc, sc)
        draw_text(c, str(n), 0, 46, 130, WHITE, shadow=False)
        c.restore()
    return dim


def cta(c, t, lt, accent, send=None):
    s = ease_back(prog(lt, 0, 0.35), 2.2)
    pulse = 1 + 0.05 * math.sin(t * 8)
    c.save()
    c.translate(W / 2, 1180)
    c.scale(s * pulse, s * pulse)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-250, -70, 500, 140), 70, 70)
    c.drawRRect(r.makeOffset(0, 10), fill(0x66000000))
    c.drawRRect(r, fill(0xFFFE2C55))
    draw_text(c, "+ SEGUIR", 0, 30, 76, WHITE, shadow=False)
    c.restore()
    hs = ease_back(prog(lt, 0.4, 0.8))
    if hs > 0:
        pill(c, W / 2, 1340, HANDLE, 44, bg=accent, fg=INK, scale=hs)
    if send:
        send_pill(c, t, lt, send)


def plane_icon(c, x, y, s, col=INK):
    """Avión de papel (icono de 'enviar' de Instagram)."""
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-18)
    p = skia.Path(); p.moveTo(-30, -4); p.lineTo(32, -26); p.lineTo(10, 30); p.lineTo(2, 6); p.close()
    c.drawPath(p, fill(col))
    q = skia.Path(); q.moveTo(2, 6); q.lineTo(32, -26); q.lineTo(-4, 2); q.close()
    c.drawPath(q, fill(with_alpha(WHITE, 0.55)))
    c.restore()


def send_pill(c, t, lt, txt):
    """v7 (29/10): llamada a ENVIAR. En IG 2026 los 'sends' (compartir por DM) son la señal que más alcance da a
    no-seguidores; el reel con más compartidos (dedo flotante, 8) fue de los que más vistas sumó. Pill blanca con
    avión de papel que sale volando en bucle hacia arriba a la derecha."""
    s = ease_back(prog(lt, 0.75, 1.1), 2.2)
    if s <= 0:
        return
    y = 1500
    f = font(40, TF_XBOLD)
    w = text_w(txt, f) + 70
    c.save(); c.translate(W / 2, y); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 - 34, -46, w + 68, 92), 46, 46)
    c.drawRRect(r.makeOffset(0, 8), fill(0x66000000))
    c.drawRRect(r, fill(WHITE))
    c.drawString(txt, -w / 2 + 70, 15, f, fill(INK))
    k = ((lt - 1.1) % 1.6) / 1.6 if lt > 1.1 else 0.0
    px, py = -w / 2 + 24 + 120 * ease_in_out(clamp(k * 1.6 - 0.6)), -30 * ease_in_out(clamp(k * 1.6 - 0.6))
    a = 1 - clamp((k - 0.75) / 0.25)
    c.saveLayerAlpha(None, int(255 * a))
    plane_icon(c, px, py, 1.0 + 0.1 * math.sin(t * 6))
    c.restore()
    c.restore()


def watermark(c):
    f = font(36, TF_XBOLD)
    w = text_w(HANDLE, f)
    x, y = W / 2 - w / 2, 232
    c.drawString(HANDLE, x, y, f, stroke(with_alpha(0xFF000000, 0.5), 8))
    c.drawString(HANDLE, x, y, f, fill(with_alpha(WHITE, 0.75)))


def kick(P, t):
    k = 0.0
    for tw in P["hl_times"]:
        if 0 <= t - tw < 0.5:
            k = max(k, math.exp(-(t - tw) * 9))
    return k


def hook_extras(c, t, V, total):
    """v4: insignia de serie (V['badge']) y aviso de bucle abierto (V['tease']) solo en los 3,5 s del gancho
    (después se quitan para no pisar subtítulos de 2-3 líneas). La insignia vuelve en el CTA final."""
    y = 288
    if V.get("badge"):
        on = t < 3.5 or t > total - 3.0
        if on:
            a = clamp(min(t - 0.15, 3.5 - t if t < 3.5 else t - (total - 3.0)) / 0.25)
            s = ease_back(prog(t, 0.15, 0.5), 2.0) if t < 3.5 else 1.0
            pill(c, W / 2, y, V["badge"], 28, bg=V["accent"], fg=INK, alpha=a, scale=s * (1 + 0.02 * math.sin(t * 3)))
    tease = V.get("tease")
    if tease and 0.5 < t < 3.5 and not V.get("badge"):
        a = clamp((t - 0.5) / 0.25) * clamp((3.5 - t) / 0.3)
        s = ease_back(prog(t, 0.5, 0.85), 2.4)
        pill(c, W / 2, y, tease, 28, bg=0xFFFE2C55, fg=WHITE, alpha=a, scale=s * (1 + 0.04 * math.sin(t * 10)))


# ------------------------------------------------------------------ frame + audio + run
def make_frame(V, P, scene):
    total = P["total"]

    def draw_frame(c, t):
        k = kick(P, t)
        c.save()
        # v4 (26/10): punch-in de gancho (zoom 1.22 -> 1 en 0,55 s) para cortar el scroll en el 1er segundo
        z = 1 + 0.035 * k + 0.22 * (1 - ease_out(clamp(t / 0.55)))
        c.translate(W / 2 + math.sin(t * 61) * 4 * k, H / 2)
        c.scale(z, z)
        c.translate(-W / 2, -H / 2)
        scene(c, t, P)
        c.restore()
        if not V.get("clean"):
            vignette(c)
            grain(c, t)
        quiz_dim = 0
        for sg in P["segs"]:
            if sg.get("quiz"):
                quiz(c, t, P, sg["id"], V["accent"])
        sg = seg_at(P, t)
        if sg["id"] == "cta":
            cta(c, t, t - sg["a"], V["accent"], V.get("send"))
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W * t / total, 10), fill(V["accent"]))
        watermark(c)
        hook_extras(c, t, V, total)
        P["caps"].draw(c, t)
        if 0.03 < t < 0.2:  # destello inicial (pattern interrupt); v5: el frame 0 queda limpio (portada/autoplay)
            c.drawPaint(fill(with_alpha(WHITE, 0.5 * (1 - (t - 0.03) / 0.17))))
        # flash de transición en cada segmento narrado nuevo
        for s2 in P["segs"]:
            if s2.get("cut") and 0 <= t - s2["a"] < 0.12:
                c.drawPaint(fill(with_alpha(WHITE, 0.25 * (1 - (t - s2["a"]) / 0.12))))

    # v6 (28/10): BUCLE INVISIBLE. En los últimos LOOP_DUR s el vídeo se funde con su propio frame 0 (gancho XL
    # + visual inicial), así al reiniciarse en IG no hay corte: el espectador 'cae' otra vez en el gancho y
    # se suman revisionados (sube el tiempo medio y las vistas). V['loop']=False lo desactiva.
    if not V.get("loop", True):
        return draw_frame

    def looped(c, t):
        draw_frame(c, t)
        k = (t - (total - LOOP_DUR)) / LOOP_DUR
        if k > 0:
            c.saveLayerAlpha(None, int(255 * smooth(k)))
            draw_frame(c, 0.0)
            c.restore()
    return looped


def build_audio(V, P, path, extra=None):
    total = P["total"]
    m = Mixer(total)
    n = min(len(m.buf), len(P["vo"]["nar"]))
    m.buf[:n] += P["vo"]["nar"][:n] + P["vo"]["q"][:n]
    for sg in P["segs"]:
        a = sg["a"]
        if sg.get("cut"):
            m.whoosh(a - 0.15, 0.35, 0.12)
        if sg.get("kind") == "count":
            step = (COUNT_DUR - 0.1) / 3
            for k in range(3):
                m.pop(a + k * step, 0.22, 1600 - k * 200)
            m.riser(a + 0.2, COUNT_DUR - 0.3, 300, 1200, 0.03)
        if sg.get("quiz"):
            m.pop(a + 0.1, 0.1, 700)
            m.pop(a + 0.22, 0.1, 900)
        if sg["id"] == "cta":
            m.ding(a + 0.1, 1318.5, 0.07)
            if V.get("send"):  # v7: 'swoosh' corto cuando aparece el avión de enviar
                m.whoosh(a + 0.8, 0.3, 0.08)
    for sg in P["segs"]:
        if sg.get("quiz"):
            idx = [i for i, s in enumerate(P["segs"]) if s["id"] == sg["id"]][0]
            ra = P["segs"][idx + 2]["a"]
            m.ding(ra + 0.02, 1046.5, 0.12)
            m.ding(ra + 0.14, 1568, 0.12)
            m.boom(ra, 0.18)
    for it in P["caps"].items:
        for (w, hl), tt in zip(it["words"], it["times"]):
            if hl and tt > 0.2:
                m.pop(tt, 0.035, 1200)
    # dron ambiental grave muy suave (sensación de espacio/profundidad)
    tt = np.arange(len(m.buf)) / SR
    drone = (np.sin(2 * np.pi * 55 * tt) * 0.5 + np.sin(2 * np.pi * 82.4 * tt + np.sin(tt * 0.3)) * 0.3) * \
        (0.6 + 0.4 * np.sin(tt * 0.5))
    # v4: ducking del dron bajo la voz (la voz se entiende mejor y el fondo 'respira' en las pausas)
    vo = np.abs(m.buf[:])
    win = int(0.12 * SR)
    env = np.convolve(vo, np.ones(win) / win, mode="same")
    env = env / (env.max() + 1e-9)
    m.buf += drone * V.get("drone", 0.02) * (1.0 - 0.65 * np.clip(env * 4, 0, 1))
    m.boom(0.0, 0.3)
    if extra:
        extra(m, P)
    # v6: cola de audio en fundido (los últimos LOOP_DUR s) para que el bucle no dé un 'clic' al reiniciar
    i0, i1 = int((total - LOOP_DUR) * SR), min(len(m.buf), int(total * SR))
    m.buf[i0:i1] *= np.linspace(1, 0, i1 - i0) ** 1.5
    m.buf[i1:] = 0
    raw = path.replace(".wav", "_raw.wav")
    m.write(raw)
    af = ("highpass=f=40,equalizer=f=3200:t=q:w=1.2:g=3,equalizer=f=250:t=q:w=1:g=-2,"
          "acompressor=threshold=-20dB:ratio=3:attack=5:release=60:makeup=2,"
          "loudnorm=I=-14:TP=-1.5:LRA=9")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", "44100", path], check=True)
    os.remove(raw)


def run(V, scene, outdir, preview=None, extra_audio=None):
    P = plan(V)
    draw_frame = make_frame(V, P, scene)
    print(f"{V['slug']}: {P['total']:.1f}s, {len(P['segs'])} segmentos")
    if preview:
        if preview == "auto":
            preview = [sg["a"] + min(1.6, (sg["b"] - sg["a"]) * 0.7) for sg in P["segs"][:-1]] + [P["total"] - 0.6]
        s = skia.Surface(W, H)
        sc = 0.22
        sheet = skia.Surface(int(W * sc * len(preview)), int(H * sc))
        imgs = []
        for tt in preview:
            with s as cc:
                cc.clear(0xFF000000)
                draw_frame(cc, tt)
            imgs.append(s.makeImageSnapshot())
        with sheet as cc:
            for i, im in enumerate(imgs):
                cc.save(); cc.translate(i * W * sc, 0); cc.scale(sc, sc); cc.drawImage(im, 0, 0); cc.restore()
        out = SCRATCH + f"prev_{V['slug']}.png"
        sheet.makeImageSnapshot().save(out, skia.kPNG)
        print(out)
        return P
    os.makedirs(outdir, exist_ok=True)
    wav = f"{outdir}/{V['slug']}.wav"
    build_audio(V, P, wav, extra_audio)
    render(draw_frame, P["total"], f"{outdir}/{V['slug']}.mp4", wav)
    os.remove(wav)
    return P
