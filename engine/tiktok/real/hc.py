"""Gráficos de la serie 'Tu cuerpo': fondo aurora, insignia, temporizadores, mano, ojo, cerebro, reloj, células, átomos."""
import math, random
import numpy as np
import skia
from core import (W, H, WHITE, INK, clamp, lerp, prog, ease_out, ease_in_out, ease_back, with_alpha, fill, stroke, pill,
                  font, text_w, draw_text, glow)
from engine import ease_elastic

SKIN = (0xFFF4CDB0, 0xFFE3A989, 0xFFB8735A)
RED = 0xFFFF3B4A


def aurora(c, t, a1, a2, seed=1):
    c.clear(0xFF05060C)
    rnd = random.Random(seed)
    for k in range(4):
        cx = W * (0.2 + 0.6 * rnd.random()) + math.sin(t * (0.15 + 0.1 * k) + k) * 220
        cy = H * (0.25 + 0.55 * rnd.random()) + math.cos(t * (0.12 + 0.08 * k) + 2 * k) * 260
        col = a1 if k % 2 == 0 else a2
        sh = skia.GradientShader.MakeRadial((cx, cy), 700, [with_alpha(col, 0.20), with_alpha(col, 0)])
        c.drawCircle(cx, cy, 700, skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kPlus))
    p = skia.Paint(AntiAlias=True)
    for k in range(70):
        x = (rnd.uniform(0, W) + math.sin(t * 0.3 + k) * 30)
        y = (rnd.uniform(0, H) - t * rnd.uniform(10, 40)) % H
        p.setColor(with_alpha(WHITE, rnd.uniform(0.05, 0.25)))
        c.drawCircle(x, y, rnd.uniform(1, 3), p)


def badge(c, part, accent, t):
    txt = f"TU CUERPO · PARTE {part}"
    c.save()
    c.translate(W / 2, 292)
    pill(c, 0, 0, txt, 30, bg=accent, fg=INK, scale=1 + 0.02 * math.sin(t * 3))
    c.restore()


def big(c, txt, x, y, size, color, lt, delay=0.0, outline=16):
    s = ease_back(prog(lt, delay, delay + 0.3), 2.4)
    if s <= 0:
        return
    f = font(size)
    w = text_w(txt, f)
    if w > 980:
        size = size * 980 / w
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    draw_text(c, txt, 0, size * 0.36, size, color, outline=outline)
    c.restore()


def stamp(c, txt, x, y, lt, delay=0.3, size=130, col=RED):
    p = prog(lt, delay, delay + 0.16)
    if p <= 0:
        return
    sc = lerp(2.4, 1.0, ease_out(p))
    a = clamp(p * 1.5)
    c.save()
    c.translate(x, y)
    c.rotate(-12)
    c.scale(sc, sc)
    f = font(size)
    w = text_w(txt, f)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 - 40, -size * 0.75, w + 80, size * 1.35), 26, 26)
    c.drawRRect(r, fill(with_alpha(0xFFFFFFFF, 0.9 * a)))
    c.drawRRect(r, stroke(with_alpha(col, a), 16))
    c.drawString(txt, -w / 2, size * 0.35, f, fill(with_alpha(col, a)))
    c.restore()


def timer(c, x, y, r, frac, num, accent):
    c.drawCircle(x, y + 8, r, fill(0x66000000))
    c.drawCircle(x, y, r, fill(with_alpha(0xFF101426, 0.92)))
    arc = skia.Path()
    arc.addArc(skia.Rect.MakeXYWH(x - r * 0.86, y - r * 0.86, r * 1.72, r * 1.72), -90, 360 * (1 - clamp(frac)))
    c.drawPath(arc, stroke(accent, r * 0.14))
    draw_text(c, str(num), x, y + r * 0.42, r * 1.15, WHITE, shadow=False)


def steps(c, items, x, y, lt, accent, gap=110, size=44):
    """Lista de pasos numerados que aparecen escalonados: items = [(t_aparición, texto)]."""
    for i, (ta, txt) in enumerate(items):
        s = ease_back(prog(lt, ta, ta + 0.3), 2.0)
        if s <= 0:
            continue
        yy = y + i * gap
        c.save()
        c.translate(x, yy)
        c.scale(s, s)
        f = font(size)
        w = text_w(txt, f)
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-60, -size * 0.95, w + 130, size * 1.9), 30, 30)
        c.drawRRect(r.makeOffset(0, 8), fill(0x66000000))
        c.drawRRect(r, fill(with_alpha(0xFF101426, 0.88)))
        c.drawRRect(r, stroke(with_alpha(WHITE, 0.25), 3))
        c.drawCircle(-10, 0, size * 0.62, fill(accent))
        draw_text(c, str(i + 1), -10, size * 0.36, size * 0.85, INK, shadow=False)
        c.drawString(txt, 40, size * 0.36, f, fill(WHITE))
        c.restore()


# ------------------------------------------------------------------ dedos y mano
def finger(c, x, y, ang, length, width, nail=True, bend=0.0):
    """Dedo semirrealista. (x, y) = base, ang en grados (0 = hacia arriba)."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    L = length * (1 - 0.45 * bend)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-width / 2, -L, width, L + width * 0.3), width / 2, width / 2)
    sh = skia.GradientShader.MakeLinear([(-width / 2, 0), (width / 2, 0)], [SKIN[2], SKIN[1], SKIN[0], SKIN[1], SKIN[2]],
                                        [0, 0.2, 0.5, 0.8, 1])
    c.drawRRect(r.makeOffset(width * 0.08, width * 0.12), fill(0x44000000))
    c.drawRRect(r, skia.Paint(Shader=sh, AntiAlias=True))
    # pliegues de los nudillos
    for k in (0.38, 0.68):
        yy = -L * k
        if bend and k > 0.5:
            continue
        c.drawLine(-width * 0.28, yy, width * 0.28, yy, stroke(with_alpha(SKIN[2], 0.55), 2.5))
        c.drawLine(-width * 0.2, yy + 7, width * 0.2, yy + 7, stroke(with_alpha(SKIN[2], 0.35), 2))
    if nail and not bend:
        nr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-width * 0.32, -L + width * 0.12, width * 0.64, width * 0.75),
                                   width * 0.3, width * 0.3)
        c.drawRRect(nr, skia.Paint(Shader=skia.GradientShader.MakeLinear(
            [(0, -L), (0, -L + width)], [0xFFFFF1EA, 0xFFF3C9C0]), AntiAlias=True))
        c.drawRRect(nr, stroke(with_alpha(SKIN[2], 0.5), 2))
    if bend:
        c.drawCircle(0, -L + width * 0.15, width * 0.5, skia.Paint(Shader=skia.GradientShader.MakeRadial(
            (0, -L), width * 0.7, [SKIN[0], SKIN[2]]), AntiAlias=True))
    c.restore()


def hand_flat(c, cx, cy, s, t, ring_lift=0.0, middle_fold=1.0):
    """Mano apoyada vista desde arriba con el dedo corazón doblado."""
    palm = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 170 * s, cy - 40 * s, 340 * s, 330 * s), 110 * s, 110 * s)
    c.drawRRect(palm.makeOffset(10, 18), fill(0x55000000))
    c.drawRRect(palm, skia.Paint(Shader=skia.GradientShader.MakeRadial((cx, cy + 100 * s), 260 * s,
                                                                       [SKIN[0], SKIN[1], SKIN[2]]), AntiAlias=True))
    # meñique, anular, corazón, índice
    specs = [(-125, 210, 64, -6), (-45, 270, 72, -2), (40, 290, 76, 1), (122, 260, 72, 5)]
    for i, (dx, ln, wd, ang) in enumerate(specs):
        lift = 0.0
        if i == 1:
            lift = ring_lift
        bend = middle_fold if i == 2 else 0.0
        finger(c, cx + dx * s, cy - 10 * s - lift * 30 * s, ang, ln * s * (1 + 0.06 * lift), wd * s, bend=bend)
    finger(c, cx + 185 * s, cy + 150 * s, 55, 200 * s, 78 * s)


def atom(c, x, y, r, t, col, seed=0):
    sh = skia.GradientShader.MakeRadial((x, y), r, [with_alpha(col, 0.5), with_alpha(col, 0.18), with_alpha(col, 0)],
                                        [0, 0.6, 1])
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, AntiAlias=True, BlendMode=skia.BlendMode.kPlus))
    for k in range(3):
        c.save()
        c.translate(x, y)
        c.rotate(k * 60 + t * 20 * (1 if k % 2 else -1) + seed * 30)
        c.drawOval(skia.Rect.MakeXYWH(-r * 0.75, -r * 0.28, r * 1.5, r * 0.56), stroke(with_alpha(WHITE, 0.35), 2.5))
        a = t * 4 + k * 2.1 + seed
        c.drawCircle(math.cos(a) * r * 0.75, math.sin(a) * r * 0.28, r * 0.05, fill(WHITE))
        c.restore()
    glow(c, x, y, r * 0.25, 0xFFFFE6B0, 0.9)
    c.drawCircle(x, y, r * 0.07, fill(0xFFFFE6B0))


# ------------------------------------------------------------------ ojo, cerebro, reloj, células
def eye(c, x, y, R, t, nerve_glow=0.0):
    c.drawCircle(x + 10, y + 16, R, fill(0x55000000))
    c.drawCircle(x, y, R, skia.Paint(Shader=skia.GradientShader.MakeRadial((x - R * 0.3, y - R * 0.3), R * 1.4,
                                                                           [0xFFFFFFFF, 0xFFF2E8E8, 0xFFD8B8B8]), AntiAlias=True))
    # retina
    c.drawArc(skia.Rect.MakeXYWH(x - R * 0.93, y - R * 0.93, R * 1.86, R * 1.86), 40, 280, False,
              stroke(0xFFE86A6A, R * 0.05))
    # nervio óptico
    nerve = skia.Path()
    nerve.moveTo(x + R * 0.82, y + R * 0.15)
    nerve.cubicTo(x + R * 1.3, y + R * 0.2, x + R * 1.5, y + R * 0.5, x + R * 2.0, y + R * 0.4)
    c.drawPath(nerve, stroke(0xFFF2D27A, R * 0.22))
    if nerve_glow > 0:
        glow(c, x + R * 0.86, y + R * 0.13, R * 0.5, 0xFFFF3B4A, 0.9 * nerve_glow)
    # córnea, iris, cristalino
    c.drawArc(skia.Rect.MakeXYWH(x - R * 1.12, y - R * 0.55, R * 0.6, R * 1.1), 90, 180, False, stroke(with_alpha(0xFFBFE8FF, 0.8), 6))
    c.drawRect(skia.Rect.MakeXYWH(x - R * 0.92, y - R * 0.42, R * 0.08, R * 0.84), fill(0xFF3A7BD5))
    c.drawOval(skia.Rect.MakeXYWH(x - R * 0.82, y - R * 0.3, R * 0.3, R * 0.6), fill(with_alpha(0xFFFFF4D0, 0.85)))
    # rayos de luz
    for k in (-1, 0, 1):
        yy = y + k * R * 0.22
        c.drawLine(x - R * 2.0, yy, x - R * 0.7, yy, stroke(with_alpha(0xFFFFF2A0, 0.7), 4))
        c.drawLine(x - R * 0.7, yy, x + R * 0.9, y - k * R * 0.25, stroke(with_alpha(0xFFFFF2A0, 0.5), 3))


def brain(c, x, y, s, t, cereb=0.0):
    rnd = random.Random(5)
    p = skia.Path()
    n = 48
    for i in range(n + 1):
        a = math.pi * 2 * i / n
        rx, ry = 300 * s, 210 * s
        bump = 1 + 0.035 * math.sin(a * 11 + 1) + 0.02 * math.sin(a * 23)
        px, py = x + math.cos(a) * rx * bump, y - 30 * s + math.sin(a) * ry * bump
        if i == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    p.close()
    # cerebelo y tronco
    cb = skia.Rect.MakeXYWH(x + 90 * s, y + 110 * s, 200 * s, 120 * s)
    c.drawRoundRect(skia.Rect.MakeXYWH(x + 40 * s, y + 140 * s, 60 * s, 170 * s), 30 * s, 30 * s, fill(0xFFD89A9A))
    c.drawOval(cb, fill(0xFFE8A8A8))
    for k in range(6):
        c.drawArc(skia.Rect.MakeXYWH(x + 100 * s, y + 120 * s + k * 14 * s, 180 * s, 50 * s), 200, 140, False,
                  stroke(0xFFC07A7A, 3))
    if cereb > 0:
        glow(c, cb.centerX(), cb.centerY(), 220 * s, 0xFF4DE1FF, 0.9 * cereb)
        c.drawOval(cb, stroke(with_alpha(0xFF4DE1FF, cereb), 6))
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeRadial((x - 80 * s, y - 100 * s), 380 * s,
                                                                   [0xFFFFD0D0, 0xFFF0A8A8, 0xFFC87878]), AntiAlias=True))
    for k in range(16):
        sx = x + rnd.uniform(-240, 240) * s
        sy = y - 30 * s + rnd.uniform(-150, 150) * s
        q = skia.Path()
        q.moveTo(sx, sy)
        q.cubicTo(sx + 40 * s, sy - 30 * s, sx + 60 * s, sy + 30 * s, sx + 100 * s, sy)
        c.drawPath(q, stroke(0xFFC07878, 4))
    c.drawPath(p, stroke(0xFFB06868, 4))


def clock(c, x, y, R, sec, t, freeze=0.0):
    c.drawCircle(x + 10, y + 16, R * 1.08, fill(0x66000000))
    c.drawCircle(x, y, R * 1.08, skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(x - R, y - R), (x + R, y + R)], [0xFFE8ECF2, 0xFF7A8290, 0xFFD8DCE4, 0xFF5A606A]), AntiAlias=True))
    c.drawCircle(x, y, R, skia.Paint(Shader=skia.GradientShader.MakeRadial((x, y - R * 0.3), R * 1.3,
                                                                           [0xFFFFFFFF, 0xFFE8E6E0]), AntiAlias=True))
    for k in range(60):
        a = math.radians(k * 6)
        r1 = R * (0.86 if k % 5 == 0 else 0.92)
        c.drawLine(x + math.sin(a) * r1, y - math.cos(a) * r1, x + math.sin(a) * R * 0.97, y - math.cos(a) * R * 0.97,
                   stroke(INK, 7 if k % 5 == 0 else 3))
    for k, lbl in ((0, "12"), (3, "3"), (6, "6"), (9, "9")):
        a = math.radians(k * 30)
        draw_text(c, lbl, x + math.sin(a) * R * 0.7, y - math.cos(a) * R * 0.7 + R * 0.08, R * 0.2, INK, shadow=False, outline=0)
    for ang, ln, wd, col in ((math.radians(305), 0.5, 14, INK), (math.radians(60), 0.72, 9, INK)):
        c.drawLine(x, y, x + math.sin(ang) * R * ln, y - math.cos(ang) * R * ln, stroke(col, wd))
    a = math.radians(sec * 6)
    if freeze > 0:
        glow(c, x + math.sin(a) * R * 0.6, y - math.cos(a) * R * 0.6, R * 0.5, RED, 0.5 * freeze)
    c.drawLine(x - math.sin(a) * R * 0.15, y + math.cos(a) * R * 0.15, x + math.sin(a) * R * 0.85, y - math.cos(a) * R * 0.85,
               stroke(RED, 5))
    c.drawCircle(x, y, 14, fill(RED))


def cell(c, x, y, r, t, col=0xFFFF6B8A, split=0.0, seed=0):
    """Célula con núcleo; split 0..1 la divide en dos."""
    if split <= 0:
        pts = [(x, y, r)]
    else:
        d = r * 1.1 * ease_out(split)
        pts = [(x - d, y, r * (1 - 0.25 * split)), (x + d, y, r * (1 - 0.25 * split))]
    for (cx, cy, rr) in pts:
        c.drawCircle(cx, cy, rr, skia.Paint(Shader=skia.GradientShader.MakeRadial(
            (cx - rr * 0.3, cy - rr * 0.3), rr * 1.3, [with_alpha(col, 0.95), with_alpha(col, 0.6), with_alpha(col, 0.25)]),
            AntiAlias=True))
        c.drawCircle(cx, cy, rr, stroke(with_alpha(WHITE, 0.45), max(1, rr * 0.06)))
        c.drawCircle(cx + rr * 0.1, cy + rr * 0.05, rr * 0.35, fill(with_alpha(0xFF6A1E5A, 0.85)))
        c.drawCircle(cx - rr * 0.05, cy - rr * 0.08, rr * 0.1, fill(with_alpha(WHITE, 0.4)))
    if 0 < split < 1:
        c.drawLine(x, y - r * 0.9, x, y + r * 0.9, stroke(with_alpha(WHITE, 0.3 * (1 - split)), 3))


def nose(c, alpha, one_eye=0.0):
    """Silueta difusa de la nariz en la parte baja del campo visual."""
    if alpha <= 0:
        return
    p = skia.Path()
    cx = W / 2 + one_eye * 160
    p.moveTo(cx - 260, H + 40)
    p.cubicTo(cx - 200, 1500, cx - 60, 1180, cx, 1120)
    p.cubicTo(cx + 60, 1180, cx + 200, 1500, cx + 260, H + 40)
    p.close()
    paint = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(cx, 1120), (cx, H)],
                                                                             [with_alpha(SKIN[1], 0.55 * alpha),
                                                                              with_alpha(SKIN[2], 0.85 * alpha)]))
    paint.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
    c.drawPath(p, paint)
