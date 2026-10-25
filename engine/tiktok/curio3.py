"""Motor v3: concurso a dos voces (Nia pregunta, Bit responde) con tarjetas A/B, cuenta atrás y revelación.

uso: python3 curio3.py <índices | all> [auto]
"""
import math, os, random, subprocess, sys, types
import numpy as np
import skia

import curio, curio2, voice
from engine import (W, H, SR, INK, WHITE, PINK, LIME, TF_BLACK, TF_XBOLD, Captions, clamp, lerp, prog, ease_out,
                    ease_in_out, ease_back, ease_elastic, with_alpha, fill, stroke, font, text_w, draw_text, pill,
                    draw_bit, Mixer, render)
from scripts3 import VIDEOS

OUTDIR = "/home/claude/tiktok/out30"
VX, VY = 590, 960
GREEN = 0xFF2FD46B
RED = 0xFFFF3B4A
NIA_COL = 0xFFFF7AD9
VOICES = {"nia": ("ef_dora", 1.22), "bit": ("em_alex", 1.28)}
COUNT_DUR = 2.5
GAP = 0.08
draw_icon = curio.draw_icon


# ------------------------------------------------------------------ dibujos nuevos
def d_pluto(c, x, y, size, t):
    r = size * 0.42
    sh = skia.GradientShader.MakeRadial((x - r * 0.3, y - r * 0.3), r * 1.6, [0xFFF2DCC2, 0xFFC49A74, 0xFF7A5A44])
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, AntiAlias=True))
    p = skia.Path()  # el "corazón" de Plutón
    hx, hy, s = x + r * 0.15, y + r * 0.1, r * 0.35
    p.moveTo(hx, hy + s)
    p.cubicTo(hx - s * 1.6, hy - s * 0.2, hx - s * 0.6, hy - s * 1.3, hx, hy - s * 0.45)
    p.cubicTo(hx + s * 0.6, hy - s * 1.3, hx + s * 1.6, hy - s * 0.2, hx, hy + s)
    c.drawPath(p, fill(0xCCFFF6EA))


def d_match(c, x, y, size, t):
    s = size / 300
    c.save()
    c.translate(x, y)
    c.rotate(25)
    c.drawRoundRect(skia.Rect.MakeXYWH(-14 * s, -90 * s, 28 * s, 210 * s), 8 * s, 8 * s, fill(0xFFE8C48A))
    c.drawOval(skia.Rect.MakeXYWH(-24 * s, -140 * s, 48 * s, 64 * s), fill(0xFFD83A2E))
    fl = 1 + 0.12 * math.sin(t * 18)
    c.drawOval(skia.Rect.MakeXYWH(-20 * s, (-215 - 10 * fl) * s, 40 * s, 80 * s * fl), fill(0xFFFFB000))
    c.drawOval(skia.Rect.MakeXYWH(-10 * s, -190 * s, 20 * s, 45 * s), fill(0xFFFFF2A0))
    c.restore()


def d_lighter(c, x, y, size, t):
    s = size / 300
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 55 * s, y - 40 * s, 110 * s, 160 * s), 18 * s, 18 * s, fill(0xFF3A7BD5))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 55 * s, y - 75 * s, 110 * s, 40 * s), 8 * s, 8 * s, fill(0xFFB8C2DD))
    c.drawCircle(x + 25 * s, y - 85 * s, 16 * s, fill(0xFF6E7898))
    fl = 1 + 0.12 * math.sin(t * 17)
    c.drawOval(skia.Rect.MakeXYWH(x - 30 * s, y - (175 + 12 * fl) * s, 44 * s, 95 * s * fl), fill(0xFFFFB000))
    c.drawOval(skia.Rect.MakeXYWH(x - 19 * s, y - 145 * s, 22 * s, 50 * s), fill(0xFFFFF2A0))


curio.CUSTOM.update({"@pluto": d_pluto, "@match": d_match, "@lighter": d_lighter})


# ------------------------------------------------------------------ personajes
def draw_nia(c, x, y, s, t, talk=0.0, **kw):
    kw.setdefault("antenna", None)
    pts = draw_bit(c, x, y, s, t, talk=talk, body_col=0xFFFFE4F2, **kw)
    hx, hy = pts[2]
    r = 74 * s
    # flequillo y coleta
    p = skia.Path()
    p.moveTo(hx - r * 1.02, hy - r * 0.05)
    p.cubicTo(hx - r * 1.1, hy - r * 1.35, hx + r * 1.1, hy - r * 1.35, hx + r * 1.02, hy - r * 0.05)
    p.cubicTo(hx + r * 0.7, hy - r * 0.55, hx - r * 0.2, hy - r * 0.75, hx - r * 1.02, hy - r * 0.05)
    c.drawPath(p, fill(0xFF5A2E6E))
    sw = math.sin(t * 5) * 0.25
    q = skia.Path()
    q.moveTo(hx + r * 0.8, hy - r * 0.6)
    q.cubicTo(hx + r * 1.9, hy - r * (0.9 + sw), hx + r * 1.7, hy + r * (0.6 + sw), hx + r * 1.25, hy + r * 0.9)
    q.cubicTo(hx + r * 1.3, hy + r * 0.2, hx + r * 1.1, hy - r * 0.2, hx + r * 0.8, hy - r * 0.6)
    c.drawPath(q, fill(0xFF5A2E6E))
    c.drawCircle(hx + r * 0.95, hy - r * 0.72, r * 0.2, fill(NIA_COL))
    c.drawCircle(hx + r * 1.2, hy - r * 0.62, r * 0.2, fill(NIA_COL))
    return pts


# ------------------------------------------------------------------ guion → segmentos
def segments(V):
    segs = [dict(kind="hook", who="nia", say=V["hook"][0], cap=V["hook"][1])]
    for qi, q in enumerate(V["qs"]):
        segs.append(dict(kind="q", who="nia", say=q["q"][0], cap=q["q"][1], qi=qi))
        segs.append(dict(kind="count", who=None, qi=qi, cap="¿*A* o *B*?"))
        segs.append(dict(kind="reveal", who="bit", say=q["r"][0], cap=q["r"][1], qi=qi))
        if q.get("react"):
            segs.append(dict(kind="react", who="nia", say=q["react"][0], cap=q["react"][1], qi=qi))
    segs.append(dict(kind="cta", who="nia", say=CTA_SAY, cap=CTA_CAP))
    return segs


from scripts3 import CTA
CTA_SAY, CTA_CAP = CTA


def _words(chunk):
    return [w for w in chunk.split()]


def plan(V):
    segs = segments(V)
    tracks = {"nia": None, "bit": None}
    cap_items = []
    cur = 0.0
    placed = []
    for sg in segs:
        if sg["kind"] == "count":
            a, b = cur, cur + COUNT_DUR
            cap_items.append((a, b, sg["cap"], [a + 0.05, a + 0.3, a + 0.55], None))
            sg["a"], sg["b"] = a, b
            cur = b
            continue
        vname, speed = VOICES[sg["who"]]
        aud = voice._synth_cached(sg["say"], vname, speed)
        d = len(aud) / 24000
        start = cur + 0.04
        placed.append((sg["who"], start, aud))
        b = start + d + GAP
        sg["a"], sg["b"] = cur, b
        chunks = [ch.strip() for ch in sg["cap"].split("|") if ch.strip()]
        allw = [(ci, w) for ci, ch in enumerate(chunks) for w in ch.split()]
        tot = sum(len(w.strip("*¡!¿?")) + 1 for _, w in allw)
        acc, times = 0, []
        for _, w in allw:
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
    total = cur + 0.6
    segs[-1]["b"] = total + 1
    n = int((total + 1) * SR)
    vo = {"nia": np.zeros(n), "bit": np.zeros(n)}
    for who, start, aud in placed:
        sig = voice._resample(aud)
        i = int(start * SR)
        j = min(n, i + len(sig))
        vo[who][i:j] += sig[: j - i]
    caps = Captions([(a, b, txt) for (a, b, txt, _, _) in cap_items], y=500, size=90, max_w=900, hl=V["accent"])
    for it, (_, _, _, times, who) in zip(caps.items, cap_items):
        it["times"] = (times + [times[-1]] * len(it["words"]))[: len(it["words"])] if times else [it["a"]] * len(it["words"])
        it["hl"] = NIA_COL if who == "nia" else V["accent"]
    # el primer trozo, ya visible en el fotograma 0
    first = caps.items[0]
    first["a"] = -0.5
    first["times"] = [-0.3] * len(first["times"])
    caps.draw = types.MethodType(captions_draw_who, caps)
    envs = {}
    hop = SR // 60
    for who in ("nia", "bit"):
        x = vo[who]
        rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, mode="same"))[::hop]
        ref = np.percentile(rms[rms > 1e-4], 95) if np.any(rms > 1e-4) else 1
        envs[who] = rms / (ref + 1e-9)
    return segs, vo, caps, envs, total


def captions_draw_who(self, c, t):
    it = self.active(t)
    if not it:
        return
    old = self.hl
    self.hl = it.get("hl", old)
    curio2.captions_draw(self, c, t)
    self.hl = old


def env_at(envs, who, t):
    e = envs[who]
    i = int(t * 60)
    if 0 <= i < len(e):
        return float(min(1.0, max(0.0, (e[i] - 0.08) * 1.4)))
    return 0.0


# ------------------------------------------------------------------ tarjetas
CX = (345, 835)


def draw_card(c, x, y, letter, label, icon, t, appear, state, rv, val=None):
    """state: neutral | right | wrong ; rv = progreso de la revelación 0..1"""
    if appear <= 0:
        return
    s = ease_back(appear, 2.0)
    bump = 1 + (0.08 * math.exp(-max(0, rv - 0.0) * 3) * (rv > 0) if state == "right" else 0)
    sc = s * bump * (1 - 0.06 * (state == "wrong") * rv)
    w, h = 410, 480
    c.save()
    c.translate(x, y)
    c.scale(sc, sc)
    c.rotate(math.sin(t * 2 + x) * 1.2)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 44, 44)
    c.drawRRect(r.makeOffset(0, 14), fill(0x55000000))
    base = 0x30FFFFFF
    border = WHITE
    if state == "right":
        base = lerp_col(base, with_alpha(GREEN, 0.35), rv)
        border = lerp_col(WHITE, GREEN, rv)
    elif state == "wrong":
        base = lerp_col(base, 0x40000000, rv)
        border = lerp_col(WHITE, 0xFF8A8FA8, rv)
    c.drawRRect(r, fill(base))
    c.drawRRect(r, stroke(border, 9 + 5 * (state == "right") * rv))
    sat = 1.0 - 0.85 * rv if state == "wrong" else 1.0
    draw_icon(c, icon, 0, -60 + math.sin(t * 2.6 + x) * 8, 210, t, sat=sat)
    f = font(56)
    lw = text_w(label, f)
    la = 1.0 - 0.4 * rv * (state == "wrong")
    if lw <= 360 or " " not in label:
        size = 56 if lw <= 360 else 56 * 360 / lw
        draw_text(c, label, 0, 175, size, WHITE, outline=12, alpha=la)
    else:
        ws = label.split()
        best = min(range(1, len(ws)), key=lambda k: abs(len(" ".join(ws[:k])) - len(" ".join(ws[k:]))))
        l1, l2 = " ".join(ws[:best]), " ".join(ws[best:])
        mw = max(text_w(l1, font(46)), text_w(l2, font(46)))
        size = 46 if mw <= 370 else 46 * 370 / mw
        draw_text(c, l1, 0, 150, size, WHITE, outline=11, alpha=la)
        draw_text(c, l2, 0, 150 + size * 1.05, size, WHITE, outline=11, alpha=la)
    if val and rv > 0:
        pill(c, 0, 95 if (lw <= 360 or " " not in label) else 62, val, 40, bg=GREEN if state == "right" else WHITE, fg=INK, scale=ease_back(prog(rv, 0.4, 1.0)))
    # letra
    c.drawCircle(-w / 2 + 40, -h / 2 + 40, 46, fill(INK))
    c.drawCircle(-w / 2 + 40, -h / 2 + 40, 46, stroke(WHITE, 6))
    draw_text(c, letter, -w / 2 + 40, -h / 2 + 62, 58, WHITE, shadow=False)
    # resultado
    if rv > 0 and state in ("right", "wrong"):
        ps = ease_back(clamp(rv * 2.2), 2.6)
        draw_icon(c, "✅" if state == "right" else "❌", w / 2 - 40, -h / 2 + 40, 130 * ps, t)
    c.restore()


def lerp_col(a, b, t):
    from engine import lerp_color
    return lerp_color(a, b, t)


def draw_countdown(c, t, lt, accent):
    p = clamp(lt / (COUNT_DUR - 0.1))
    n = 3 - min(2, int(lt / ((COUNT_DUR - 0.1) / 3)))
    sub = (lt % ((COUNT_DUR - 0.1) / 3)) / ((COUNT_DUR - 0.1) / 3)
    x, y = VX, VY - 20
    c.drawCircle(x, y + 8, 112, fill(0x55000000))
    c.drawCircle(x, y, 112, fill(INK))
    arc = skia.Path()
    arc.addArc(skia.Rect.MakeXYWH(x - 96, y - 96, 192, 192), -90, 360 * (1 - p))
    c.drawPath(arc, stroke(accent, 18))
    sc = 1 + 0.35 * math.exp(-sub * 7)
    c.save()
    c.translate(x, y)
    c.scale(sc, sc)
    draw_text(c, str(n), 0, 48, 140, WHITE, shadow=False)
    c.restore()


def draw_vs(c, t, a):
    if a <= 0:
        return
    s = ease_elastic(a)
    c.save()
    c.translate(VX, VY - 20)
    c.scale(s, s)
    c.drawCircle(0, 0, 66, fill(PINK))
    c.drawCircle(0, 0, 66, stroke(INK, 8))
    draw_text(c, "VS", 0, 21, 60, WHITE, shadow=False)
    c.restore()


# ------------------------------------------------------------------ frame
def make_frame(V, segs, caps, envs, total):
    hl_times = [tt for it in caps.items for (w, hl), tt in zip(it["words"], it["times"]) if hl and tt > 0.3]
    nq = len(V["qs"])

    def seg_at(t):
        cur = segs[0]
        for sg in segs:
            if sg["a"] <= t:
                cur = sg
        return cur

    def draw_frame(c, t):
        curio.background(c, t, V)
        sg = seg_at(t)
        lt = t - sg["a"]
        kind = sg["kind"]
        kick = 0.0
        for tw in hl_times:
            if 0 <= t - tw < 0.5:
                kick = max(kick, math.exp(-(t - tw) * 9))
        z = 1 + 0.05 * kick
        first_of_block = kind in ("hook", "q", "cta")
        dx = (1 - ease_out(lt / 0.2)) * W * 0.75 if (first_of_block and kind != "hook" and lt < 0.2) else 0
        c.save()
        c.translate(W / 2 + dx + math.sin(t * 61) * 4 * kick, VY)
        c.scale(z, z)
        c.translate(-W / 2, -VY)
        nia_pose = dict(arm_l=110, arm_r=-40, look=(1, -0.5))
        bit_pose = dict(arm_l=110, arm_r=-40, look=(1, -0.5))
        if kind == "hook":
            l2 = lt + 0.35
            curio.burst(c, VX, VY - 40, 720, t, V["accent"], 1)
            curio2.draw_glow(c, t, 1, V["accent"])
            draw_icon(c, V["topic"], VX, VY - 60 + math.sin(t * 2.2) * 12, 360 * ease_back(clamp(l2 / 0.5), 2.2), t)
            c.save()
            c.translate(VX, VY - 300)
            c.rotate(-4 + 2 * math.sin(t * 2))
            pill(c, 0, 0, V["title"], 56, bg=V["accent"], fg=INK, scale=ease_elastic(prog(l2, 0.1, 0.8)))
            c.restore()
            pill(c, VX, VY + 200, "¿CUÁNTAS ACIERTAS?", 50, bg=WHITE, fg=INK, scale=ease_back(prog(l2, 0.4, 0.75)))
            for k in range(nq):
                draw_icon(c, "❓", VX - 120 + k * 120, VY + 330, 90 * ease_back(prog(l2, 0.5 + k * 0.12, 0.8 + k * 0.12)), t)
            nia_pose = dict(arm_l=-150, arm_r=-30, eyes="wide", look=(1, -1))
            bit_pose = dict(arm_l=-120, arm_r=-60, eyes="happy", look=(-1, -0.5))
        elif kind == "cta":
            curio.sc_cta(c, t, lt, sg["b"] - sg["a"], {"v": "cta"}, V)
            pill(c, VX, VY - 330, f"¿ ? / {nq}", 64, bg=WHITE, fg=INK, scale=ease_back(prog(lt, 0.1, 0.4)))
            nia_pose = dict(arm_l=-120 + 25 * math.sin(t * 10), arm_r=40, eyes="happy", look=(1, 0))
            bit_pose = dict(arm_l=120, arm_r=-140 + 25 * math.sin(t * 10 + 1), eyes="happy", look=(-1, 0))
        else:
            q = V["qs"][sg["qi"]]
            # aparición de las tarjetas (en el segmento de pregunta)
            q_seg = [s for s in segs if s["kind"] == "q" and s["qi"] == sg["qi"]][0]
            lq = t - q_seg["a"]
            rv = 0.0
            if kind in ("reveal", "react"):
                r_seg = [s for s in segs if s["kind"] == "reveal" and s["qi"] == sg["qi"]][0]
                rv = clamp((t - r_seg["a"]) / 0.45)
            for side, (lab, ic) in enumerate((q["a"], q["b"])):
                letter = "AB"[side]
                ok = q["ans"] == "both" or q["ans"] == letter.lower()
                state = "right" if ok else "wrong"
                if rv == 0:
                    state = "neutral"
                vals = q.get("vals") or (None, None)
                draw_card(c, CX[side], VY, letter, lab, ic, t, prog(lq, 0.05 + side * 0.15, 0.4 + side * 0.15),
                          state, rv, vals[side])
            if q["ans"] == "both" and rv > 0:
                c.save()
                c.translate(VX, VY - 330)
                c.rotate(-6)
                pill(c, 0, 0, "¡TRAMPA! IGUAL", 60, bg=V["accent"], fg=INK, scale=ease_elastic(prog(rv, 0.2, 1)))
                c.restore()
            if kind == "count":
                draw_countdown(c, t, lt, V["accent"])
                nia_pose = dict(arm_l=-95, arm_r=-60, look=(0.5, -1), eyes="normal")
                bit_pose = dict(arm_l=-95, arm_r=-60, look=(0.5, -1), eyes="normal")
            elif kind == "q":
                draw_vs(c, t, prog(lq, 0.3, 0.9))
                nia_pose = dict(arm_l=110, arm_r=-35, look=(1, -0.6))
            elif kind in ("reveal", "react"):
                bit_pose = dict(arm_l=-150, arm_r=-30, eyes="happy" if lt > 0.5 else "wide", look=(1, -0.6))
                if kind == "react":
                    nia_pose = dict(arm_l=-160, arm_r=-20, eyes="wide", look=(-0.5, -0.5))
            # badge de pregunta
            if not (q["ans"] == "both" and rv > 0):
                pill(c, VX, VY - 330, f"PREGUNTA {sg['qi'] + 1}/{nq}", 46, bg=V["accent"], fg=INK,
                     scale=ease_back(prog(lq, 0, 0.3)) if kind == "q" else 1.0)
        c.restore()
        if dx:
            curio2.speed_lines(c, lt / 0.2, V["accent"])
        # personajes
        tn, tb = env_at(envs, "nia", t), env_at(envs, "bit", t)
        for who, x, pose, talk, fn in (("nia", 135, nia_pose, tn, draw_nia), ("bit", 380, bit_pose, tb, draw_bit)):
            spk = sg.get("who") == who
            sc = 0.86 * (1.06 if spk else 1.0)
            if spk:
                c.drawOval(skia.Rect.MakeXYWH(x - 90, 1712, 180, 30), fill(with_alpha(NIA_COL if who == "nia" else V["accent"], 0.5)))
            kw = dict(eyes="normal", arm_l=110, arm_r=-40, look=(1, -0.5))
            kw.update(pose)
            fn(c, x, 1725 - talk * 10, sc, t + (1.3 if who == "bit" else 0), talk=talk,
               lean=talk * 4 * math.sin(t * 5), **kw)
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W * t / total, 12), fill(V["accent"]))
        curio.watermark(c, t)
        caps.draw(c, t)
    return draw_frame


# ------------------------------------------------------------------ audio
def build_audio(V, segs, vo, caps, total, path):
    m = Mixer(total)
    n = min(len(m.buf), len(vo["nia"]))
    m.buf[:n] += vo["nia"][:n] + vo["bit"][:n]
    for sg in segs:
        a = sg["a"]
        if sg["kind"] == "q":
            m.whoosh(a - 0.12, 0.3, 0.12)
            m.pop(a + 0.1, 0.1, 700)
            m.pop(a + 0.25, 0.1, 900)
        if sg["kind"] == "count":
            step = (COUNT_DUR - 0.1) / 3
            for k in range(3):
                m.pop(a + k * step, 0.22, 1600 - k * 200)
                m.hat(a + k * step + step / 2, 0.08)
            m.riser(a + 0.2, COUNT_DUR - 0.3, 300, 1200, 0.03)
        if sg["kind"] == "reveal":
            m.ding(a + 0.02, 1046.5, 0.12)
            m.ding(a + 0.14, 1568, 0.12)
            m.boom(a, 0.18)
        if sg["kind"] == "cta":
            m.ding(a + 0.1, 1318.5, 0.07)
    for it in caps.items:
        for (w, hl), tt in zip(it["words"], it["times"]):
            if hl and tt > 0.2:
                m.pop(tt, 0.04, 1200)
    m.boom(0.0, 0.25)
    raw = path.replace(".wav", "_raw.wav")
    m.write(raw)
    af = ("highpass=f=70,equalizer=f=3200:t=q:w=1.2:g=3,equalizer=f=250:t=q:w=1:g=-2,"
          "acompressor=threshold=-20dB:ratio=3:attack=5:release=60:makeup=2,"
          "loudnorm=I=-14:TP=-1.5:LRA=9")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", "44100", path], check=True)
    os.remove(raw)


def run(idx, preview=None):
    V = dict(VIDEOS[idx])
    V["seed"] = idx * 17 + 3
    segs, vo, caps, envs, total = plan(V)
    draw_frame = make_frame(V, segs, caps, envs, total)
    print(f"{V['slug']}: {total:.1f}s, {len(segs)} segmentos")
    if preview:
        times = [sg["a"] + min(1.6, (sg["b"] - sg["a"]) * 0.7) for sg in segs[:-1]] + [total - 0.6]
        s = skia.Surface(W, H)
        sc = 0.22
        sheet = skia.Surface(int(W * sc * len(times)), int(H * sc))
        imgs = []
        for tt in times:
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
    os.makedirs(OUTDIR, exist_ok=True)
    wav = f"{OUTDIR}/{V['slug']}.wav"
    build_audio(V, segs, vo, caps, total, wav)
    render(draw_frame, total, f"{OUTDIR}/{V['slug']}.mp4", wav)
    os.remove(wav)
    return total


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = len(sys.argv) > 2 and sys.argv[2] == "auto"
    for i in idxs:
        run(i, pv)
