"""Plantilla de vídeos de curiosidades: escenas reutilizables + locución + marca de agua.

uso: python3 curio.py <índice 0-9 | all> [preview t1,t2,...]
"""
import math, random, sys
import numpy as np
import skia

from engine import (W, H, FPS, SR, INK, WHITE, CREAM, YELLOW, LIME, PINK, CYAN, TF_BLACK, TF_XBOLD, TF_BOLD,
                    clamp, lerp, prog, ease_out, ease_in_out, ease_back, ease_elastic, with_alpha, fill, stroke,
                    font, text_w, draw_text, pill, draw_bit, bg_gradient, Mixer, render)
import voice
from scripts import VIDEOS

HANDLE = "@videosparadormir2018"
GAP = 0.2
OUTDIR = "/home/claude/tiktok/out10"
VX, VY = 590, 930  # centro de la zona visual

# ------------------------------------------------------------------ emojis
EMOJI_TF = skia.Typeface.MakeFromFile("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf")
_EMOJI = {}
SAMPLING = skia.SamplingOptions(skia.CubicResampler.Mitchell())


def emoji_img(ch):
    ch = ch.replace("️", "")
    if ch not in _EMOJI:
        f = skia.Font(EMOJI_TF, 109)
        s = skia.Surface(160, 160)
        with s as c:
            c.clear(0x00000000)
            w = f.measureText(ch)
            c.drawString(ch, (160 - w) / 2, 128, f, skia.Paint(AntiAlias=True))
        _EMOJI[ch] = s.makeImageSnapshot()
    return _EMOJI[ch]


def sat_filter(s):
    """Saturación 0 (gris) .. 1 (normal)."""
    lr, lg, lb = 0.2126, 0.7152, 0.0722
    m = [lr * (1 - s) + s, lg * (1 - s), lb * (1 - s), 0, 0,
         lr * (1 - s), lg * (1 - s) + s, lb * (1 - s), 0, 0,
         lr * (1 - s), lg * (1 - s), lb * (1 - s) + s, 0, 0,
         0, 0, 0, 1, 0]
    return skia.ColorFilters.Matrix(m)


def draw_icon(c, e, x, y, size, t=0.0, rot=0.0, alpha=1.0, sat=1.0, shadow=True):
    """Dibuja un emoji o un dibujo propio ('@nombre') centrado en (x, y)."""
    if size <= 1 or alpha <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    if e.startswith("@"):
        if sat < 1 or alpha < 1:
            p = skia.Paint(Alphaf=alpha)
            if sat < 1:
                p.setColorFilter(sat_filter(sat))
            c.saveLayer(None, p)
        CUSTOM[e](c, 0, 0, size, t)
        if sat < 1 or alpha < 1:
            c.restore()
    else:
        img = emoji_img(e)
        s = size * 160 / 136
        dst = skia.Rect.MakeXYWH(-s / 2, -s / 2 - size * 0.04, s, s)
        if shadow:
            sp = skia.Paint(Alphaf=0.28 * alpha, ColorFilter=skia.ColorFilters.Blend(0xFF000000, skia.BlendMode.kSrcIn))
            c.drawImageRect(img, dst.makeOffset(size * 0.03, size * 0.05), SAMPLING, sp)
        p = skia.Paint(Alphaf=alpha)
        if sat < 1:
            p.setColorFilter(sat_filter(sat))
        c.drawImageRect(img, dst, SAMPLING, p)
    c.restore()


# ------------------------------------------------------------------ dibujos propios
def d_venus(c, x, y, size, t):
    r = size * 0.45
    sh = skia.GradientShader.MakeRadial((x - r * 0.35, y - r * 0.35), r * 1.6, [0xFFFFE3A3, 0xFFF0A040, 0xFFB5651D])
    c.drawCircle(x, y, r * 1.12, fill(0x33FFC870))
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, AntiAlias=True))
    c.save()
    c.clipPath(skia.Path().addCircle(x, y, r))
    off = (t * 40) % (r * 2)
    for k in range(-3, 5):
        yy = y - r + k * r * 0.45 + 10 * math.sin(k)
        p = skia.Path()
        p.moveTo(x - r * 1.5 + off - r, yy)
        p.cubicTo(x - r * 0.5 + off - r, yy - r * 0.15, x + off - r, yy + r * 0.15, x + r * 2 + off - r, yy)
        c.drawPath(p, stroke(0x40FFFFFF if k % 2 else 0x30A0521A, r * 0.12))
    c.drawCircle(x + r * 0.45, y + r * 0.35, r * 1.05, fill(0x30000000))
    c.restore()


def d_aztec(c, x, y, size, t):
    s = size / 300
    base = y + 130 * s
    cols = [0xFF8C7A5B, 0xFF9E8A66, 0xFFB09A72, 0xFFC2AA80]
    for i in range(4):
        w = (280 - i * 55) * s
        h = 45 * s
        top = base - (i + 1) * h
        c.drawRect(skia.Rect.MakeXYWH(x - w / 2, top, w, h), fill(cols[i]))
        c.drawRect(skia.Rect.MakeXYWH(x - w / 2, top, w, h), stroke(0x55000000, 3 * s))
    c.drawRect(skia.Rect.MakeXYWH(x - 22 * s, base - 180 * s, 44 * s, 180 * s), fill(0xFF6E5E44))
    for k in range(9):
        c.drawLine(x - 22 * s, base - k * 20 * s, x + 22 * s, base - k * 20 * s, stroke(0x66000000, 2 * s))
    top = base - 180 * s
    for dx, col in ((-38, 0xFFD64545), (38, 0xFF3A7BD5)):
        c.drawRect(skia.Rect.MakeXYWH(x + dx * s - 28 * s, top - 60 * s, 56 * s, 60 * s), fill(col))
        c.drawRect(skia.Rect.MakeXYWH(x + dx * s - 32 * s, top - 72 * s, 64 * s, 14 * s), fill(0xFFEFE3C2))


def d_pyramid(c, x, y, size, t):
    s = size / 300
    hgt, half = 230 * s, 160 * s
    base = y + 110 * s
    p = skia.Path()
    p.moveTo(x, base - hgt); p.lineTo(x + half, base); p.lineTo(x - half, base); p.close()
    c.drawPath(p, fill(0xFFF0B862))
    p2 = skia.Path()
    p2.moveTo(x, base - hgt); p2.lineTo(x + half, base); p2.lineTo(x, base); p2.close()
    c.drawPath(p2, fill(0xFFC98840))
    for i in range(1, 8):
        yy = base - hgt * i / 8
        hw = half * (1 - i / 8)
        c.drawLine(x - hw, yy, x + hw, yy, stroke(0x669E6430, 3 * s))


def d_wombat(c, x, y, size, t):
    s = size / 300
    fur, dark, light = 0xFF8B6B4A, 0xFF5E4630, 0xFFB08F6A
    bob = math.sin(t * 6) * 4 * s
    y += bob
    # patas
    for dx in (-80, -35, 35, 80):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + dx * s - 20 * s, y + 55 * s, 40 * s, 60 * s),
                                          16 * s, 16 * s), fill(dark))
    c.drawOval(skia.Rect.MakeXYWH(x - 140 * s, y - 70 * s, 280 * s, 170 * s), fill(fur))
    c.drawOval(skia.Rect.MakeXYWH(x - 90 * s, y - 10 * s, 180 * s, 90 * s), fill(light))
    # cabeza
    hx, hy = x + 95 * s, y - 55 * s
    for ex in (-40, 30):
        c.drawCircle(hx + ex * s, hy - 62 * s, 24 * s, fill(dark))
        c.drawCircle(hx + ex * s, hy - 62 * s, 12 * s, fill(0xFFD9A98A))
    c.drawCircle(hx, hy, 78 * s, fill(fur))
    c.drawOval(skia.Rect.MakeXYWH(hx + 20 * s, hy - 5 * s, 70 * s, 52 * s), fill(light))
    c.drawOval(skia.Rect.MakeXYWH(hx + 48 * s, hy - 2 * s, 38 * s, 26 * s), fill(0xFF2A1E14))
    blink = (t % 3.1) < 0.12
    for ex in (-18, 22):
        if blink:
            c.drawLine(hx + ex * s - 9 * s, hy - 22 * s, hx + ex * s + 9 * s, hy - 22 * s, stroke(INK, 5 * s))
        else:
            c.drawCircle(hx + ex * s, hy - 22 * s, 10 * s, fill(INK))
            c.drawCircle(hx + ex * s + 3 * s, hy - 26 * s, 3.5 * s, fill(WHITE))
    c.drawCircle(hx - 40 * s, hy + 15 * s, 12 * s, fill(with_alpha(PINK, 0.45)))


CUSTOM = {"@venus": d_venus, "@aztec": d_aztec, "@pyramid": d_pyramid, "@wombat": d_wombat}


# ------------------------------------------------------------------ utilidades de escena
def fmt_num(n, year=False):
    n = int(round(n))
    return str(n) if year else f"{n:,}".replace(",", ".")


def burst(c, x, y, r, t, col, alpha=1.0, n=14):
    c.save()
    c.translate(x, y)
    c.rotate(t * 18)
    for k in range(n):
        a0 = k * math.tau / n
        p = skia.Path()
        p.moveTo(0, 0)
        p.lineTo(math.cos(a0 - 0.1) * r, math.sin(a0 - 0.1) * r)
        p.lineTo(math.cos(a0 + 0.1) * r, math.sin(a0 + 0.1) * r)
        p.close()
        c.drawPath(p, fill(with_alpha(col, 0.13 * alpha)))
    c.restore()


def label_pill(c, txt, x, y, lt, accent, size=44, delay=0.35):
    sc = ease_back(prog(lt, delay, delay + 0.3))
    if sc > 0:
        pill(c, x, y, txt, size, bg=accent, fg=INK, scale=sc)


def pop(lt, d=0.0, dur=0.38):
    return ease_back(prog(lt, d, d + dur), 2.2)


# ------------------------------------------------------------------ escenas
def sc_hook(c, t, lt, dur, v, V):
    burst(c, VX, VY, 700, t, V["accent"], 1)
    s = pop(lt, 0.0, 0.5)
    wob = math.sin(t * 3) * 5
    draw_icon(c, v["e"], VX, VY + math.sin(t * 2.2) * 14, 400 * s * (1 + 0.06 * V["punch"](t)), t, rot=wob)
    if "badge" in v:
        draw_icon(c, v["badge"], VX + 200, VY - 170, 170 * pop(lt, 0.5), t, rot=-12 + 6 * math.sin(t * 4))
    tag_s = ease_elastic(prog(lt, 0.15, 0.9))
    c.save()
    c.translate(VX, VY - 240)
    c.rotate(-4 + 2 * math.sin(t * 2))
    if tag_s > 0:
        pill(c, 0, 0, v.get("tag", "¿SABÍAS QUE…?"), 50, bg=V["accent"], fg=INK, scale=tag_s)
    c.restore()
    return dict(eyes="wide", arm_l=-150, arm_r=-30, look=(1, -1))


def sc_emoji(c, t, lt, dur, v, V):
    s = pop(lt)
    x, y = VX, VY + math.sin(t * 2.4) * 16
    rot = 0.0
    if v.get("spin"):
        rot = lt * 360 * v["spin"]
    if v.get("shake"):
        k = math.exp(-lt * 2.5)
        x += math.sin(t * 70) * 14 * k
        y += math.cos(t * 63) * 10 * k
    if v.get("crawl"):
        x = lerp(VX + 260, VX - 80, ease_in_out(prog(lt, 0, dur)))
        y = VY + 120 + abs(math.sin(t * 7)) * -25
        rot = math.sin(t * 7) * 8
    sat = 1.0
    if "gray" in v:
        g0, g1 = v["gray"]
        sat = lerp(g0, g1, ease_in_out(prog(lt, 0.4, max(0.5, dur - 0.4))))
    burst(c, VX, VY, 560, t, V["accent"], 0.7 * s)
    draw_icon(c, v["e"], x, y, 380 * s, t, rot=rot, sat=sat)
    if "badge" in v:
        draw_icon(c, v["badge"], VX + 190, VY - 160, 160 * pop(lt, 0.35), t, rot=-10 + 8 * math.sin(t * 3))
    if "label" in v:
        label_pill(c, v["label"], VX, VY + 280, lt, V["accent"])
    return dict(arm_r=-40, arm_l=110, look=(1, -0.6))


def sc_row(c, t, lt, dur, v, V):
    es = v["es"]
    n = len(es)
    size = {1: 360, 2: 300, 3: 250, 4: 200}.get(n, 180)
    gap = min(310, 900 / n)
    x0 = VX - gap * (n - 1) / 2
    stagger = min(0.45, (dur * 0.6) / max(1, n))
    for i, e in enumerate(es):
        s = pop(lt, i * stagger)
        yy = VY + math.sin(t * 3 + i * 1.3) * 14
        draw_icon(c, e, x0 + i * gap, yy, size * s, t, rot=math.sin(t * 2 + i) * 6)
    if "label" in v:
        label_pill(c, v["label"], VX, VY + 260, lt, V["accent"], delay=n * stagger)
    return dict(arm_r=-35, arm_l=120, look=(1, -0.4), eyes="happy" if lt > 1 else "normal")


def sc_count(c, t, lt, dur, v, V):
    s = pop(lt)
    burst(c, VX, VY - 140, 480, t, V["accent"], 0.6 * s)
    draw_icon(c, v["e"], VX, VY - 150 + math.sin(t * 2.5) * 10, 250 * s, t)
    if "badge" in v:
        draw_icon(c, v["badge"], VX + 150, VY - 250, 130 * pop(lt, 0.3), t)
    p = ease_out(prog(lt, 0.15, min(1.6, dur * 0.7)))
    val = v["n"] * p
    txt = fmt_num(val, v.get("year")) + v.get("suffix", "")
    size = 150 if len(txt) <= 7 else (120 if len(txt) <= 10 else 96)
    sc = s * (1 + 0.08 * math.exp(-max(0, lt - min(1.6, dur * 0.7)) * 6) * (p >= 1))
    c.save()
    c.translate(VX, VY + 110)
    c.scale(sc, sc)
    draw_text(c, txt, 0, size * 0.36, size, V["accent"], outline=18)
    c.restore()
    if "label" in v:
        label_pill(c, v["label"], VX, VY + 250, lt, WHITE, size=38, delay=0.45)
    return dict(arm_r=-45, arm_l=100, look=(1, -0.3))


def sc_big(c, t, lt, dur, v, V):
    s = pop(lt)
    draw_icon(c, v["e"], VX, VY - 160, 240 * s, t)
    txt = v["text"]
    n = int(len(txt) * ease_out(prog(lt, 0.2, min(1.4, dur * 0.6))))
    size = 96 if len(txt) > 12 else 130
    draw_text(c, txt[:n], VX, VY + 110, size, V["accent"], outline=16)
    return dict(arm_r=-45, arm_l=100, look=(1, -0.3), eyes="wide")


def sc_versus(c, t, lt, dur, v, V):
    L, R = v["l"], v["r"]
    has_bars = L[3] is not None and R[3] is not None
    for side, (e, name, val_txt, val), xx, d in ((-1, L, 450, 0.0), (1, R, 860, 0.35)):
        s = pop(lt, d)
        top = VY - 250
        draw_icon(c, e, xx, top + math.sin(t * 2.6 + d * 5) * 10, 190 * s, t)
        if s > 0:
            draw_text(c, name, xx, top + 160, 52 if len(name) <= 8 else 38, WHITE, outline=12, alpha=clamp(s))
        if has_bars:
            mx = max(L[3], R[3])
            hmax = 270
            h = hmax * (val / mx) * ease_out(prog(lt, 0.4 + d, 1.4 + d))
            h = max(h, 14 * clamp(s))
            col = V["accent"] if val == mx else 0xFFB8C2DD
            base = VY + 320
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(xx - 85, base - h, xx + 85, base), 20, 20), fill(col))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(xx - 85, base - h, xx + 85, base), 20, 20),
                        stroke(INK, 6))
            label_pill(c, val_txt, xx, base + 55, lt, WHITE, size=34, delay=1.0 + d)
        else:
            label_pill(c, val_txt, xx, VY + 120, lt, V["accent"], size=46, delay=0.4 + d)
    vs = ease_elastic(prog(lt, 0.2, 0.9))
    if vs > 0:
        c.save()
        c.translate(655, VY - 60)
        c.scale(vs, vs)
        c.drawCircle(0, 0, 62, fill(PINK))
        c.drawCircle(0, 0, 62, stroke(INK, 7))
        draw_text(c, "VS", 0, 20, 56, WHITE, shadow=False)
        c.restore()
    return dict(arm_l=-100, arm_r=-60, look=(0.5, -1), eyes="normal")


def sc_timeline(c, t, lt, dur, v, V):
    pts = v["pts"]
    n = len(pts)
    x0, x1, y = 150, 1000, VY + 40
    first = v.get("from", 0)
    grow = 1.0 if first else ease_out(prog(lt, 0, 0.6))
    c.drawLine(x0, y, lerp(x0, x1, grow), y, stroke(0x66FFFFFF, 14))
    c.drawLine(x0, y, lerp(x0, x1, grow), y, stroke(WHITE, 7))
    stagger = min(0.6, dur * 0.5 / max(1, n - first))
    xs = [lerp(x0 + 60, x1 - 60, i / max(1, n - 1)) for i in range(n)]
    for i, (e, lab) in enumerate(pts):
        d = 0 if i < first else 0.3 + (i - first) * stagger
        s = 1.0 if i < first else pop(lt, d)
        if s <= 0:
            continue
        x = xs[i]
        c.drawCircle(x, y, 20 * s, fill(V["accent"]))
        c.drawCircle(x, y, 20 * s, stroke(INK, 5))
        draw_icon(c, e, x, y - 140 + math.sin(t * 2.5 + i) * 8, (190 if n <= 3 else 150) * s, t)
        pill(c, x, y + 80, lab, 38 if n <= 3 else 32, bg=WHITE, fg=INK, scale=s)
    if "span" in v:
        i0, i1, txt = v["span"]
        p = ease_out(prog(lt, 0.9, 1.6))
        if p > 0:
            yb = y + 170
            xa, xb = xs[i0], lerp(xs[i0], xs[i1], p)
            c.drawLine(xa, yb - 25, xa, yb, stroke(V["accent"], 8))
            c.drawLine(xa, yb, xb, yb, stroke(V["accent"], 8))
            if p >= 1:
                c.drawLine(xb, yb - 25, xb, yb, stroke(V["accent"], 8))
                pill(c, (xa + xb) / 2, yb + 70, txt, 46, bg=V["accent"], fg=INK, scale=ease_back(prog(lt, 1.6, 1.9)))
    return dict(arm_r=-40, arm_l=110, look=(1, -0.5))


def sc_cta(c, t, lt, dur, v, V):
    # botón seguir
    s = pop(lt)
    pulse = 1 + 0.05 * math.sin(t * 8)
    c.save()
    c.translate(VX, VY - 170)
    c.scale(s * pulse, s * pulse)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-250, -70, 500, 140), 70, 70)
    c.drawRRect(r.makeOffset(0, 10), fill(0x55000000))
    c.drawRRect(r, fill(0xFFFE2C55))
    draw_text(c, "+ SEGUIR", 0, 30, 76, WHITE, shadow=False)
    c.restore()
    # dedo que pulsa
    tap = (lt % 1.2) / 1.2
    fy = VY - 90 + 40 * math.sin(min(1, tap * 2) * math.pi)
    draw_icon(c, "👆", VX + 170, fy + 90, 150 * pop(lt, 0.3), t)
    # comentarios
    for i, e in enumerate(["💬", "❤", "🔔"]):
        sc = pop(lt, 0.5 + i * 0.25)
        draw_icon(c, e, VX - 260 + i * 260, VY + 150 + math.sin(t * 3 + i) * 15, 150 * sc, t)
    hs = ease_back(prog(lt, 0.9, 1.3))
    if hs > 0:
        pill(c, VX, VY + 330, HANDLE, 46, bg=V["accent"], fg=INK, scale=hs)
    return dict(arm_l=-120 + 25 * math.sin(t * 10), arm_r=40, eyes="happy", look=(1, 0))


SCENES = {"hook": sc_hook, "emoji": sc_emoji, "row": sc_row, "count": sc_count, "big": sc_big,
          "versus": sc_versus, "timeline": sc_timeline, "cta": sc_cta}


# ------------------------------------------------------------------ fondo, marca, frame
def background(c, t, V):
    top, bot = V["theme"]
    bg_gradient(c, top, bot)
    rnd = random.Random(V["seed"])
    for k in range(26):
        x = rnd.uniform(0, W)
        y0 = rnd.uniform(0, H)
        r = rnd.uniform(4, 14)
        sp = rnd.uniform(15, 45)
        y = (y0 - t * sp) % (H + 40) - 20
        c.drawCircle(x + math.sin(t + k) * 20, y, r, fill(with_alpha(WHITE, 0.06 + 0.05 * (k % 3))))


def watermark(c, t):
    f = font(36, TF_XBOLD)
    w = text_w(HANDLE, f)
    x, y = W / 2 - w / 2, 232
    c.drawString(HANDLE, x, y, f, stroke(with_alpha(INK, 0.45), 8))
    c.drawString(HANDLE, x, y, f, fill(with_alpha(WHITE, 0.72)))


def make_frame(V, timeline, caps, total):
    def draw_frame(c, t):
        background(c, t, V)
        # beat activo
        bi = 0
        for i, (a, b, beat) in enumerate(timeline):
            if a <= t:
                bi = i
        a, b, beat = timeline[bi]
        lt = t - a
        v = beat[2]
        z = 1 + 0.035 * prog(lt, 0, b - a)  # zoom lento
        c.save()
        c.translate(W / 2, VY)
        c.scale(z, z)
        c.translate(-W / 2, -VY)
        pose = SCENES[v["v"]](c, t, lt, b - a, v, V)
        c.restore()
        # personaje
        talk = caps.talk_amount(t)
        kw = dict(eyes="normal", arm_l=110, arm_r=-40, look=(1, -0.5))
        kw.update(pose)
        hop = math.exp(-lt * 9) * 18 if bi > 0 else 0
        draw_bit(c, 175, 1700 - hop, 0.82, t, talk=talk, **kw)
        # flash de corte
        if bi > 0 and lt < 0.14:
            c.drawPaint(fill(with_alpha(WHITE, 0.35 * (1 - lt / 0.14))))
        # barra de progreso
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W * t / total, 10), fill(V["accent"]))
        watermark(c, t)
        caps.draw(c, t)
    return draw_frame


# ------------------------------------------------------------------ montaje
def plan(V):
    beats = V["beats"]
    lines, timeline, cur = [], [], 0.0
    for spoken, cap, vis in beats:
        aud = voice._synth_cached(spoken, "em_alex", voice.BASE_SPEED)
        d = len(aud) / 24000
        b = cur + 0.05 + d + 0.12 + GAP
        lines.append((cur, b, cap, spoken))
        timeline.append((cur, b, (spoken, cap, vis)))
        cur = b
    total = cur + 0.5
    vo, caps, env = voice.build(lines)
    caps.y = 470
    caps.talk_amount = env
    first = caps.items[0]
    first["a"] = -0.5
    first["times"] = [-0.3 - 0.02 * i for i in range(len(first["times"]))][::-1]
    timeline[-1] = (timeline[-1][0], total + 1, timeline[-1][2])
    return vo, caps, timeline, total


def build_audio(V, vo, caps, timeline, total, path):
    m = Mixer(total)
    n = min(len(m.buf), len(vo))
    m.buf[:n] += vo[:n]
    hook_word = [w for (w, hl) in caps.items[0]["words"] if hl]
    for i, (a, b, beat) in enumerate(timeline):
        v = beat[2]
        if i > 0:
            m.whoosh(a - 0.15, 0.35, 0.07)
        m.pop(a + 0.05, 0.12, 900 + 80 * (i % 5))
        if v["v"] == "count":
            m.riser(a + 0.15, min(1.45, (b - a) * 0.7 - 0.15), 300, 900, 0.025)
            m.ding(a + min(1.6, (b - a) * 0.7), 1046.5, 0.07)
        if v["v"] == "row":
            for k in range(len(v["es"])):
                m.pop(a + k * min(0.45, (b - a) * 0.6 / len(v["es"])), 0.1, 700 + 150 * k)
        if v["v"] == "cta":
            m.ding(a + 0.1, 1318.5, 0.06)
    m.boom(V["punch_t"], 0.22)
    m.write(path)


def run(idx, preview=None):
    V = dict(VIDEOS[idx])
    V["seed"] = idx * 13 + 1
    vo, caps, timeline, total = plan(V)
    # golpe del gancho: palabra resaltada más tardía del primer beat
    hl_times = [tt for it in caps.items for (w, hl), tt in zip(it["words"], it["times"])
                if hl and it["b"] <= timeline[0][1] + 0.01]
    V["punch_t"] = max(max(hl_times) if hl_times else 2.0, 0.4)
    pt = V["punch_t"]
    V["punch"] = lambda t: math.exp(-max(0, t - pt) * 4) if t >= pt else 0
    draw_frame = make_frame(V, timeline, caps, total)
    print(f"{V['slug']}: {total:.1f}s, {len(timeline)} beats")
    if preview:
        if preview == "auto":
            preview = [a + min(1.9, (b - a) * 0.75) for (a, b, _) in timeline[:-1]] + [total - 0.6]
        s = skia.Surface(W, H)
        sc = 0.25
        cols = len(preview)
        sheet = skia.Surface(int(W * sc * cols), int(H * sc))
        imgs = []
        for t in preview:
            tt = t if t >= 0 else total + t
            with s as cc:
                cc.clear(INK)
                draw_frame(cc, tt)
            imgs.append(s.makeImageSnapshot())
        with sheet as cc:
            for i, im in enumerate(imgs):
                cc.save(); cc.translate(i * W * sc, 0); cc.scale(sc, sc); cc.drawImage(im, 0, 0); cc.restore()
        out = f"/tmp/claude-0/-home-claude/17e1b1a5-e9d8-514f-95d3-0b335f31f5e2/scratchpad/prev_{V['slug']}.png"
        sheet.makeImageSnapshot().save(out, skia.kPNG)
        print(out)
        return total
    import os
    os.makedirs(OUTDIR, exist_ok=True)
    wav = f"{OUTDIR}/{V['slug']}.wav"
    build_audio(V, vo, caps, timeline, total, wav)
    render(draw_frame, total, f"{OUTDIR}/{V['slug']}.mp4", wav)
    os.remove(wav)
    return total


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = None
    if len(sys.argv) > 2:
        pv = "auto" if sys.argv[2] == "auto" else [float(x) for x in sys.argv[2].split(",")]
    for i in idxs:
        run(i, pv)
