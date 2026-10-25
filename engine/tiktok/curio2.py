"""Motor v2: más ritmo, transiciones deslizantes, zoom en palabras clave, subtítulos con caja,
sellos FALSO, contador #N, brillo, voz más rápida y audio masterizado (-14 LUFS).

uso: python3 curio2.py <índices | all> [auto]
"""
import math, os, random, subprocess, sys, types
import skia

import curio
import voice
import scripts2
from engine import (W, H, INK, WHITE, PINK, TF_BLACK, clamp, lerp, prog, ease_out, ease_back, with_alpha,
                    fill, stroke, font, text_w, draw_text, pill, draw_bit, Mixer)

voice.BASE_SPEED = 1.28
voice.MAX_SPEED = 1.6
curio.GAP = 0.06
curio.OUTDIR = "/home/claude/tiktok/out20"
curio.VIDEOS = scripts2.VIDEOS
VX, VY = curio.VX, curio.VY
RED = 0xFFFF3B4A


# ------------------------------------------------------------------ dibujos nuevos
def d_sugar(c, x, y, size, t):
    s = size / 300
    a = 110 * s
    top = [(x, y - a * 1.05), (x + a, y - a * 0.5), (x, y + 0.05 * a), (x - a, y - a * 0.5)]
    left = [(x - a, y - a * 0.5), (x, y + 0.05 * a), (x, y + a * 1.15), (x - a, y + a * 0.6)]
    right = [(x + a, y - a * 0.5), (x, y + 0.05 * a), (x, y + a * 1.15), (x + a, y + a * 0.6)]
    for pts, col in ((left, 0xFFE4E8F2), (right, 0xFFC9CFDF), (top, 0xFFFFFFFF)):
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        p.close()
        c.drawPath(p, fill(col))
        c.drawPath(p, stroke(0xFF9AA6C8, 4 * s))
    rnd = random.Random(3)
    for _ in range(40):
        u, v = rnd.random(), rnd.random()
        px = lerp(x - a, x + a, u)
        py = y - a * 0.5 + lerp(-0.5, 1.1, v) * a * 0.9
        c.drawCircle(px, py, 2.5 * s, fill(0x55FFFFFF))
    for k in range(3):
        ph = (t * 1.5 + k / 3) % 1
        sx, sy = x + (k - 1) * a * 0.7, y - a * 1.1 - ph * 30 * s
        c.drawCircle(sx, sy, (6 - 4 * ph) * s * 2, fill(with_alpha(0xFFFFFFFF, 1 - ph)))


def d_nstar(c, x, y, size, t):
    r = size * 0.22
    for k in range(5):
        c.drawCircle(x, y, r * (1.4 + k * 0.45), fill(with_alpha(0xFF8AB4FF, 0.10 - k * 0.015)))
    c.save()
    c.translate(x, y)
    c.rotate(t * 40)
    for sgn in (1, -1):
        p = skia.Path()
        p.moveTo(-r * 0.25, 0)
        p.lineTo(0, sgn * size * 0.75)
        p.lineTo(r * 0.25, 0)
        p.close()
        c.drawPath(p, fill(0x99D6E6FF))
    c.restore()
    sh = skia.GradientShader.MakeRadial((x - r * 0.3, y - r * 0.3), r * 1.5, [0xFFFFFFFF, 0xFFB8D4FF, 0xFF4A6FD8])
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, AntiAlias=True))


curio.CUSTOM["@sugar"] = d_sugar
curio.CUSTOM["@nstar"] = d_nstar


# ------------------------------------------------------------------ subtítulos v2 (caja en palabras clave)
def captions_draw(self, c, t):
    it = self.active(t)
    if not it:
        return
    f = font(self.size)
    space = self.size * 0.28
    lines, cur, cur_w = [], [], 0
    for i, (w, hlw) in enumerate(it["words"]):
        ww = text_w(w.upper(), f)
        extra = self.size * 0.36 if hlw else 0
        if cur and cur_w + space + ww + extra > self.max_w:
            lines.append((cur, cur_w))
            cur, cur_w = [], 0
        cur.append((i, w.upper(), hlw, ww, extra))
        cur_w += ww + extra + (space if len(cur) > 1 else 0)
    if cur:
        lines.append((cur, cur_w))
    lh = self.size * 1.22
    out = prog(t, it["b"] - 0.08, it["b"])
    y0 = self.y - (len(lines) - 1) * lh / 2
    for li, (ws, lw) in enumerate(lines):
        x = W / 2 - lw / 2
        y = y0 + li * lh
        for (i, w, hlw, ww, extra) in ws:
            tt = it["times"][i]
            p = prog(t, tt - 0.04, tt + 0.16)
            if p <= 0:
                x += ww + extra + space
                continue
            sc = ease_back(p, 2.6) * (1 - 0.2 * out)
            bw = ww + extra
            cx, cy = x + bw / 2, y - self.size * 0.35
            a = 1 - out
            c.save()
            c.translate(cx, cy)
            c.scale(sc, sc)
            if hlw:
                c.rotate(-2.5)
                r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-bw / 2, -self.size * 0.62, bw, self.size * 1.18),
                                          self.size * 0.22, self.size * 0.22)
                c.drawRRect(r.makeOffset(6, 9), fill(with_alpha(0xFF000000, 0.4 * a)))
                c.drawRRect(r, fill(with_alpha(self.hl, a)))
                c.drawString(w, -ww / 2, self.size * 0.36, f, fill(with_alpha(INK, a)))
            else:
                c.drawString(w, -ww / 2 + 6, self.size * 0.36 + 9, f, fill(with_alpha(0xFF000000, 0.45 * a)))
                c.drawString(w, -ww / 2, self.size * 0.36, f, stroke(with_alpha(INK, a), 17))
                c.drawString(w, -ww / 2, self.size * 0.36, f, fill(with_alpha(WHITE, a)))
            c.restore()
            x += bw + space


# ------------------------------------------------------------------ extras visuales
def draw_glow(c, t, lt, accent):
    a = clamp(lt / 0.3) * (0.75 + 0.25 * math.sin(t * 4))
    sh = skia.GradientShader.MakeRadial((VX, VY), 420, [with_alpha(accent, 0.55 * a), with_alpha(accent, 0)])
    c.drawCircle(VX, VY, 420, skia.Paint(Shader=sh, AntiAlias=True))


def draw_stamp(c, txt, lt, delay=0.35):
    p = prog(lt, delay, delay + 0.16)
    if p <= 0:
        return
    sc = lerp(2.4, 1.0, ease_out(p))
    a = clamp(p * 1.5)
    c.save()
    c.translate(VX + 20, VY + 40)
    c.rotate(-14)
    c.scale(sc, sc)
    f = font(130)
    w = text_w(txt, f)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 - 40, -95, w + 80, 175), 26, 26)
    c.drawRRect(r, fill(with_alpha(0xFFFFFFFF, 0.85 * a)))
    c.drawRRect(r, stroke(with_alpha(RED, a), 16))
    c.drawString(txt, -w / 2, 45, f, fill(with_alpha(RED, a)))
    c.restore()


def draw_num(c, n, t, lt, accent, fresh):
    sc = ease_back(prog(lt, 0, 0.3), 2.6) if fresh else 1.0
    c.save()
    c.translate(175, 720)
    c.rotate(-8 + 3 * math.sin(t * 3))
    c.scale(sc, sc)
    c.drawCircle(6, 9, 92, fill(0x55000000))
    c.drawCircle(0, 0, 92, fill(accent))
    c.drawCircle(0, 0, 92, stroke(INK, 8))
    draw_text(c, f"#{n}", 0, 36, 96, INK, shadow=False)
    c.restore()


def speed_lines(c, p, accent):
    rnd = random.Random(7)
    for k in range(18):
        y = rnd.uniform(500, 1500)
        L = rnd.uniform(200, 600) * (1 - p)
        x = rnd.uniform(0, W) * (1 - p) + W * p * 0.2
        c.drawLine(x, y, x + L, y, stroke(with_alpha(WHITE if k % 3 else accent, 0.5 * (1 - p)), 6))


# ------------------------------------------------------------------ frame
def make_frame(V, timeline, caps, total):
    hl_times = [tt for it in caps.items for (w, hl), tt in zip(it["words"], it["times"]) if hl and tt > 0.3]
    nums = [beat[2].get("num") for (_, _, beat) in timeline]

    def draw_frame(c, t):
        curio.background(c, t, V)
        bi = 0
        for i, (a, b, beat) in enumerate(timeline):
            if a <= t:
                bi = i
        a, b, beat = timeline[bi]
        lt = t - a
        v = beat[2]
        # zoom: lento + golpe en cada palabra clave
        z = 1 + 0.04 * prog(lt, 0, b - a)
        kick = 0.0
        for tw in hl_times:
            if 0 <= t - tw < 0.5:
                kick = max(kick, math.exp(-(t - tw) * 9))
        z += 0.055 * kick
        sx = math.sin(t * 61) * 5 * kick
        # entrada deslizante
        dx = 0.0
        if bi > 0 and lt < 0.2:
            dx = (1 - ease_out(lt / 0.2)) * W * 0.75
        c.save()
        c.translate(W / 2 + dx + sx, VY)
        c.scale(z, z)
        c.translate(-W / 2, -VY)
        if v.get("glow"):
            draw_glow(c, t, lt, V["accent"])
        scene_lt = lt + (0.35 if bi == 0 else 0.0)  # el gancho ya está en pantalla en el fotograma 0
        pose = curio.SCENES[v["v"]](c, t, scene_lt, b - a, v, V)
        if v.get("stamp"):
            draw_stamp(c, v["stamp"], lt)
        c.restore()
        if bi > 0 and lt < 0.2:
            speed_lines(c, lt / 0.2, V["accent"])
        if v.get("num"):
            fresh = bi == 0 or nums[bi - 1] != v["num"]
            draw_num(c, v["num"], t, lt, V["accent"], fresh)
        talk = caps.talk_amount(t)
        kw = dict(eyes="normal", arm_l=110, arm_r=-40, look=(1, -0.5))
        kw.update(pose)
        if v.get("stamp") and lt > 0.35:
            kw["eyes"] = "wide"
        hop = math.exp(-lt * 9) * 26 if bi > 0 else 0
        draw_bit(c, 175, 1700 - hop - talk * 10, 0.82, t, talk=talk, lean=talk * 4 * math.sin(t * 5), **kw)
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W * t / total, 12), fill(V["accent"]))
        curio.watermark(c, t)
        caps.draw(c, t)
    return draw_frame


# ------------------------------------------------------------------ audio
def build_audio(V, vo, caps, timeline, total, path):
    m = Mixer(total)
    n = min(len(m.buf), len(vo))
    m.buf[:n] += vo[:n]
    for i, (a, b, beat) in enumerate(timeline):
        v = beat[2]
        if i > 0:
            m.whoosh(a - 0.12, 0.3, 0.12)
        if v.get("stamp"):
            m.boom(a + 0.35, 0.28)
            m.pop(a + 0.35, 0.18, 300)
        if v["v"] == "count":
            m.riser(a + 0.1, min(1.4, (b - a) * 0.7 - 0.1), 300, 1000, 0.03)
            m.ding(a + min(1.6, (b - a) * 0.7), 1046.5, 0.08)
        if v["v"] == "row":
            for k in range(len(v["es"])):
                m.pop(a + k * min(0.45, (b - a) * 0.6 / len(v["es"])), 0.1, 700 + 150 * k)
        if v.get("num") and (i == 0 or timeline[i - 1][2][2].get("num") != v["num"]):
            m.ding(a + 0.05, [0, 1318.5, 1174.7, 1046.5][v["num"]], 0.09)
        if v["v"] == "cta":
            m.ding(a + 0.1, 1318.5, 0.07)
    for it in caps.items:
        for (w, hl), tt in zip(it["words"], it["times"]):
            if hl and tt > 0.2:
                m.pop(tt, 0.05, 1200)
    m.boom(V["punch_t"], 0.3)
    m.boom(0.0, 0.25)
    raw = path.replace(".wav", "_raw.wav")
    m.write(raw)
    af = ("highpass=f=70,equalizer=f=3200:t=q:w=1.2:g=3,equalizer=f=250:t=q:w=1:g=-2,"
          "acompressor=threshold=-20dB:ratio=3:attack=5:release=60:makeup=2,"
          "loudnorm=I=-14:TP=-1.5:LRA=9")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", "44100", path], check=True)
    os.remove(raw)


curio.make_frame = make_frame
curio.build_audio = build_audio

_orig_plan = curio.plan


def plan(V):
    vo, caps, timeline, total = _orig_plan(V)
    caps.size = 90
    caps.max_w = 900
    caps.y = 500
    caps.hl = V["accent"]
    caps.draw = types.MethodType(captions_draw, caps)
    return vo, caps, timeline, total


curio.plan = plan

if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(scripts2.VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = "auto" if len(sys.argv) > 2 and sys.argv[2] == "auto" else None
    for i in idxs:
        curio.run(i, pv)
