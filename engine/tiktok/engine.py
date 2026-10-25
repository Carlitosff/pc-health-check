"""Mini motor de animación 2D para vídeos verticales (1080x1920) con Skia + ffmpeg."""
import math, random, re, subprocess, wave
import numpy as np
import skia

W, H, FPS = 1080, 1920, 30
SR = 44100

FONT_DIR = "/usr/share/fonts/opentype/inter/"
TF_BLACK = skia.Typeface.MakeFromFile(FONT_DIR + "InterDisplay-Black.otf")
TF_XBOLD = skia.Typeface.MakeFromFile(FONT_DIR + "InterDisplay-ExtraBold.otf")
TF_BOLD = skia.Typeface.MakeFromFile(FONT_DIR + "Inter-Bold.otf")

# Paleta
INK = 0xFF101322
WHITE = 0xFFFFFFFF
CREAM = 0xFFF6F1E7
YELLOW = 0xFFFFE14D
LIME = 0xFFB8FF3C
PINK = 0xFFFF5C8A
CYAN = 0xFF4DE1FF


# ---------------------------------------------------------------- utilidades
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lerp(a, b, t):
    return a + (b - a) * t


def prog(t, a, b):
    """0..1 entre a y b."""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_back(x, s=1.9):
    x = clamp(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def ease_elastic(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1
    return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * (2 * math.pi / 3)) + 1


def lerp_color(c1, c2, t):
    t = clamp(t)
    out = 0
    for sh in (24, 16, 8, 0):
        a = (c1 >> sh) & 255
        b = (c2 >> sh) & 255
        out |= int(round(a + (b - a) * t)) << sh
    return out


def with_alpha(c, a):
    return (int(clamp(a) * 255) << 24) | (c & 0xFFFFFF)


def fill(color, aa=True):
    return skia.Paint(Color=color, AntiAlias=aa, Style=skia.Paint.kFill_Style)


def stroke(color, w, cap=skia.Paint.kRound_Cap):
    return skia.Paint(Color=color, AntiAlias=True, Style=skia.Paint.kStroke_Style,
                      StrokeWidth=w, StrokeCap=cap, StrokeJoin=skia.Paint.kRound_Join)


# ---------------------------------------------------------------- texto
def font(size, tf=None):
    return skia.Font(tf or TF_BLACK, size)


def text_w(s, f):
    return f.measureText(s)


def draw_text(c, s, x, y, size, color=WHITE, tf=None, align="center", outline=0, outline_color=INK,
              alpha=1.0, shadow=True):
    f = font(size, tf)
    w = text_w(s, f)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    if shadow:
        c.drawString(s, x + size * 0.05, y + size * 0.07, f, fill(with_alpha(0xFF000000, 0.35 * alpha)))
    if outline:
        c.drawString(s, x, y, f, stroke(with_alpha(outline_color, alpha), outline))
    c.drawString(s, x, y, f, fill(with_alpha(color, alpha)))
    return w


def pill(c, cx, cy, s, size, bg=YELLOW, fg=INK, tf=None, alpha=1.0, scale=1.0, pad=(26, 16)):
    """Etiqueta tipo 'pill' centrada en (cx, cy)."""
    f = font(size, tf or TF_XBOLD)
    w = text_w(s, f)
    c.save()
    c.translate(cx, cy)
    c.scale(scale, scale)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 - pad[0], -size / 2 - pad[1], w + pad[0] * 2,
                                                 size + pad[1] * 2), size * 0.6, size * 0.6)
    c.drawRRect(r.makeOffset(0, 8), fill(with_alpha(0xFF000000, 0.3 * alpha)))
    c.drawRRect(r, fill(with_alpha(bg, alpha)))
    c.drawString(s, -w / 2, size * 0.36, f, fill(with_alpha(fg, alpha)))
    c.restore()


# ---------------------------------------------------------------- subtítulos estilo TikTok
class Captions:
    """Frases con palabras que aparecen una a una. *palabra* = resaltada.

    lines: lista de (inicio, fin, texto). Las palabras se reparten en el primer 70% del tramo.
    """

    def __init__(self, lines, y=430, size=88, max_w=860, hl=YELLOW):
        self.items = []
        for line in lines:
            a, b, txt = line[:3]
            frac = line[3] if len(line) > 3 else 0.62
            words, cur, cur_hl, on = [], "", False, False
            for ch in txt + " ":
                if ch == "*":
                    on = not on
                    continue
                if ch == " ":
                    if cur:
                        words.append((cur, cur_hl))
                    cur, cur_hl = "", False
                    continue
                cur += ch
                cur_hl = cur_hl or on
            n = len(words)
            span = (b - a) * frac
            times = [a + span * i / max(1, n) for i in range(n)]
            self.items.append(dict(a=a, b=b, words=words, times=times))
        self.y, self.size, self.max_w, self.hl = y, size, max_w, hl

    def word_events(self):
        """Tiempos de aparición de cada palabra (para la voz)."""
        ev = []
        for it in self.items:
            for (w, hlw), tt in zip(it["words"], it["times"]):
                ev.append((tt, w, hlw))
        return ev

    def active(self, t):
        for it in self.items:
            if it["a"] <= t < it["b"]:
                return it
        return None

    def talk_amount(self, t):
        """Apertura de boca 0..1 según la última palabra que apareció."""
        it = self.active(t)
        if not it:
            return 0.0
        best = 0.0
        for (w, _), tt in zip(it["words"], it["times"]):
            d = t - tt
            if 0 <= d < 0.32:
                best = max(best, math.sin(d / 0.32 * math.pi) * (0.6 + 0.4 * min(1, len(w) / 6)))
        return best

    def draw(self, c, t):
        it = self.active(t)
        if not it:
            return
        f = font(self.size)
        space = self.size * 0.27
        # maquetar en líneas
        lines, cur, cur_w = [], [], 0
        for i, (w, hlw) in enumerate(it["words"]):
            ww = text_w(w.upper(), f)
            if cur and cur_w + space + ww > self.max_w:
                lines.append((cur, cur_w))
                cur, cur_w = [], 0
            cur.append((i, w.upper(), hlw, ww))
            cur_w += ww + (space if len(cur) > 1 else 0)
        if cur:
            lines.append((cur, cur_w))
        lh = self.size * 1.12
        out = prog(t, it["b"] - 0.12, it["b"])
        y0 = self.y - (len(lines) - 1) * lh / 2
        for li, (ws, lw) in enumerate(lines):
            x = W / 2 - lw / 2
            y = y0 + li * lh
            for (i, w, hlw, ww) in ws:
                tt = it["times"][i]
                p = prog(t, tt, tt + 0.22)
                if p <= 0:
                    x += ww + space
                    continue
                sc = ease_back(p) * (1 - 0.15 * out)
                cx, cy = x + ww / 2, y - self.size * 0.35
                c.save()
                c.translate(cx, cy)
                c.scale(sc, sc)
                if hlw:
                    c.rotate(-3 * math.sin(t * 6 + i))
                col = self.hl if hlw else WHITE
                a = 1 - out
                c.drawString(w, -ww / 2 + 6, self.size * 0.35 + 9, f, fill(with_alpha(0xFF000000, 0.45 * a)))
                c.drawString(w, -ww / 2, self.size * 0.35, f, stroke(with_alpha(INK, a), 16))
                c.drawString(w, -ww / 2, self.size * 0.35, f, fill(with_alpha(col, a)))
                c.restore()
                x += ww + space


# ---------------------------------------------------------------- personaje "Bit"
def draw_bit(c, x, y, s=1.0, t=0.0, talk=0.0, arm_l=-60, arm_r=-120, lean=0.0, eyes="normal",
             look=(0, 0), legs="stand", walk=0.0, body_col=WHITE, antenna=LIME, hold_r=None, hold_l=None,
             squash=0.0, blink=True):
    """Monigote original. (x, y) = punto entre los pies.

    Ángulos de brazos en grados (0 = derecha, -90 = arriba, 90 = abajo).
    Devuelve posiciones de las manos.
    """
    c.save()
    c.translate(x, y)
    c.scale(s * (1 + squash * 0.15), s * (1 - squash * 0.15))
    lw = 15
    leg_len, body_len, head_r = 150, 160, 74
    hip = (0, -leg_len)
    # piernas
    if legs == "walk":
        a1 = math.sin(walk * math.tau) * 28
        a2 = -a1
    elif legs == "sit":
        a1, a2 = -70, -60
    else:
        a1, a2 = 12, -12
    for a in (a1, a2):
        ar = math.radians(90 + a)
        fx, fy = hip[0] + math.cos(ar) * leg_len, hip[1] + math.sin(ar) * leg_len
        if legs == "sit":
            kx, ky = hip[0] + math.cos(math.radians(a * -1 + 180 if a < 0 else 0)) * 0, hip[1]
        c.drawLine(hip[0], hip[1], fx, fy, stroke(body_col, lw))
        c.drawLine(fx, fy, fx + 22, fy, stroke(body_col, lw))
    # torso (inclinado)
    lr = math.radians(lean)
    neck = (hip[0] + math.sin(lr) * body_len, hip[1] - math.cos(lr) * body_len)
    c.drawLine(hip[0], hip[1], neck[0], neck[1], stroke(body_col, lw))
    sh = (lerp(hip[0], neck[0], 0.82), lerp(hip[1], neck[1], 0.82))
    arm = 128
    hands = []
    for ang, held in ((arm_l, hold_l), (arm_r, hold_r)):
        r = math.radians(ang)
        ex, ey = sh[0] + math.cos(r) * arm * 0.55, sh[1] + math.sin(r) * arm * 0.55
        r2 = r + math.radians(-18 if math.cos(r) > 0 else 18)
        hx, hy = ex + math.cos(r2) * arm * 0.5, ey + math.sin(r2) * arm * 0.5
        c.drawLine(sh[0], sh[1], ex, ey, stroke(body_col, lw))
        c.drawLine(ex, ey, hx, hy, stroke(body_col, lw))
        c.drawCircle(hx, hy, 11, fill(body_col))
        hands.append((hx, hy))
    # cabeza
    hx, hy = neck[0] + math.sin(lr) * head_r * 0.9, neck[1] - head_r * 0.92
    # antena
    if antenna is not None:
        wob = math.sin(t * 7) * 6
        ax, ay = hx + 18 + wob, hy - head_r - 46
        c.drawLine(hx + 10, hy - head_r + 4, ax, ay, stroke(body_col, 8))
        glow = 0.5 + 0.5 * math.sin(t * 5)
        c.drawCircle(ax, ay, 20 + 6 * glow, fill(with_alpha(antenna, 0.25)))
        c.drawCircle(ax, ay, 14, fill(antenna))
    c.drawCircle(hx, hy, head_r, fill(CREAM))
    c.drawCircle(hx, hy, head_r, stroke(INK, 7))
    # ojos
    ex_off, ey_off = look[0] * 10, look[1] * 8
    bl = blink and (t % 3.7) < 0.12
    for sx in (-1, 1):
        exx, eyy = hx + sx * 25 + ex_off, hy - 8 + ey_off
        if eyes == "closed" or (bl and eyes in ("normal", "wide")):
            c.drawLine(exx - 11, eyy, exx + 11, eyy, stroke(INK, 7))
        elif eyes == "happy":
            p = skia.Path()
            p.moveTo(exx - 13, eyy + 5)
            p.quadTo(exx, eyy - 13, exx + 13, eyy + 5)
            c.drawPath(p, stroke(INK, 7))
        elif eyes == "wide":
            c.drawCircle(exx, eyy, 17, fill(WHITE))
            c.drawCircle(exx, eyy, 17, stroke(INK, 5))
            c.drawCircle(exx + look[0] * 4, eyy + look[1] * 4, 8, fill(INK))
        elif eyes == "strain":
            for d in (-1, 1):
                c.drawLine(exx - 11, eyy - 7 * d * sx, exx + 11, eyy, stroke(INK, 6))
        else:
            c.drawOval(skia.Rect.MakeXYWH(exx - 8, eyy - 12, 16, 24), fill(INK))
            c.drawCircle(exx + 2, eyy - 5, 3.5, fill(WHITE))
    # mejillas
    for sx in (-1, 1):
        c.drawCircle(hx + sx * 44 + ex_off * 0.5, hy + 18, 9, fill(with_alpha(PINK, 0.45)))
    # boca
    mx, my = hx + ex_off * 0.6, hy + 30
    if eyes == "strain":
        c.drawRect(skia.Rect.MakeXYWH(mx - 18, my - 6, 36, 14), fill(INK))
        for k in range(3):
            c.drawLine(mx - 12 + k * 12, my - 6, mx - 12 + k * 12, my + 8, stroke(WHITE, 3))
    elif talk > 0.05:
        oh = 6 + talk * 26
        c.drawOval(skia.Rect.MakeXYWH(mx - 16, my - oh / 2, 32, oh), fill(INK))
        c.drawOval(skia.Rect.MakeXYWH(mx - 9, my + oh / 2 - 9, 18, 8), fill(with_alpha(PINK, 0.9)))
    elif eyes == "wide":
        c.drawCircle(mx, my, 9, fill(INK))
    else:
        p = skia.Path()
        p.moveTo(mx - 18, my - 4)
        p.quadTo(mx, my + 12, mx + 18, my - 4)
        c.drawPath(p, stroke(INK, 6))
    c.restore()
    # posiciones de manos en coordenadas de pantalla
    out = []
    for (px, py) in hands + [(hx, hy)]:
        out.append((x + px * s * (1 + squash * 0.15), y + py * s * (1 - squash * 0.15)))
    return out  # [mano_izq, mano_der, centro_cabeza]


# ---------------------------------------------------------------- fondo
def bg_gradient(c, top, bottom):
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [top, bottom])
    c.drawPaint(skia.Paint(Shader=sh))


def bg_dots(c, t, color=0x14FFFFFF, spacing=90, speed=20):
    p = fill(color)
    off = (t * speed) % spacing
    for yy in range(-spacing, H + spacing, spacing):
        for xx in range(0, W + spacing, spacing):
            c.drawCircle(xx + (yy // spacing % 2) * spacing / 2, yy + off, 4, p)


def stars(c, seed, n, alpha=1.0, t=0.0, dy=0.0):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.uniform(1.5, 4.2)
        tw = 0.6 + 0.4 * math.sin(t * rnd.uniform(1, 4) + rnd.uniform(0, 6))
        yy = (y + dy * r * 0.4) % H
        c.drawCircle(x, yy, r, fill(with_alpha(WHITE, alpha * tw)))


def progress_bar(c, t, dur, color=YELLOW):
    p = t / dur
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 10), fill(0x33FFFFFF))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W * p, 10), fill(color))


# ---------------------------------------------------------------- audio
def _env(n, a=0.005, r=0.1):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e


class Mixer:
    def __init__(self, dur):
        self.buf = np.zeros(int(dur * SR) + SR)
        self.dur = dur

    def add(self, t, sig, gain=1.0):
        i = int(t * SR)
        if i < 0:
            sig = sig[-i:]
            i = 0
        if i >= len(self.buf):
            return
        j = min(len(self.buf), i + len(sig))
        self.buf[i:j] += sig[: j - i] * gain

    # --- instrumentos
    def kick(self, t, g=0.9):
        n = int(0.35 * SR)
        tt = np.arange(n) / SR
        f = 45 + 110 * np.exp(-tt * 28)
        ph = np.cumsum(2 * np.pi * f / SR)
        self.add(t, np.sin(ph) * np.exp(-tt * 9), g)

    def snare(self, t, g=0.35):
        n = int(0.22 * SR)
        rng = np.random.default_rng(int(t * 1000))
        s = rng.standard_normal(n) * _env(n, 0.001, 0.06)
        tt = np.arange(n) / SR
        s += np.sin(2 * np.pi * 190 * tt) * _env(n, 0.001, 0.05) * 0.6
        self.add(t, s, g)

    def hat(self, t, g=0.10):
        n = int(0.06 * SR)
        rng = np.random.default_rng(int(t * 997) + 7)
        s = np.diff(rng.standard_normal(n + 1)) * _env(n, 0.0005, 0.015)
        self.add(t, s, g)

    def bass(self, t, freq, dur, g=0.28):
        n = int(dur * SR)
        tt = np.arange(n) / SR
        s = np.sin(2 * np.pi * freq * tt) + 0.3 * np.sin(4 * np.pi * freq * tt)
        e = np.minimum(1, tt / 0.01) * np.minimum(1, (dur - tt) / 0.05)
        self.add(t, s * e, g)

    def pluck(self, t, freq, g=0.14, decay=0.25):
        n = int(decay * 3 * SR)
        tt = np.arange(n) / SR
        s = (np.sin(2 * np.pi * freq * tt) + 0.5 * np.sin(4 * np.pi * freq * tt) +
             0.25 * np.sin(6 * np.pi * freq * tt)) * _env(n, 0.003, decay)
        self.add(t, s, g)

    def blip(self, t, base=520, g=0.16, seed=0):
        """Sílaba de 'voz' de personaje (estilo animalese)."""
        rng = random.Random(seed)
        dur = rng.uniform(0.06, 0.1)
        n = int(dur * SR)
        tt = np.arange(n) / SR
        f0 = base * rng.uniform(0.85, 1.3)
        f = f0 * (1 + 0.25 * np.sin(np.pi * tt / dur) * rng.choice([1, -1]))
        ph = np.cumsum(2 * np.pi * f / SR)
        s = np.sign(np.sin(ph)) * 0.35 + np.sin(ph) * 0.65
        e = np.sin(np.pi * tt / dur) ** 0.6
        self.add(t, s * e, g)

    def pop(self, t, g=0.3, f=900):
        n = int(0.09 * SR)
        tt = np.arange(n) / SR
        fr = f * np.exp(-tt * 18) + 200
        self.add(t, np.sin(np.cumsum(2 * np.pi * fr / SR)) * _env(n, 0.001, 0.03), g)

    def whoosh(self, t, dur=0.45, g=0.25, up=True):
        n = int(dur * SR)
        rng = np.random.default_rng(int(t * 131))
        noise = rng.standard_normal(n)
        # filtro paso-bajo variable simple
        tt = np.linspace(0, 1, n)
        alpha = (0.02 + 0.5 * (tt if up else 1 - tt))
        out = np.zeros(n)
        acc = 0.0
        for i in range(n):
            acc += alpha[i] * (noise[i] - acc)
            out[i] = acc
        e = np.sin(np.pi * tt) ** 1.5
        self.add(t, out * e * 3, g)

    def ding(self, t, freq=1318.5, g=0.18):
        n = int(1.2 * SR)
        tt = np.arange(n) / SR
        s = (np.sin(2 * np.pi * freq * tt) + 0.4 * np.sin(2 * np.pi * freq * 2.76 * tt)) * np.exp(-tt * 4)
        self.add(t, s, g)

    def riser(self, t, dur, f0=200, f1=1200, g=0.08):
        n = int(dur * SR)
        tt = np.arange(n) / SR
        f = f0 * (f1 / f0) ** (tt / dur)
        ph = np.cumsum(2 * np.pi * f / SR)
        s = (np.sin(ph) + 0.3 * np.sin(ph * 2.01)) * (tt / dur) ** 1.2
        self.add(t, s, g)

    def boom(self, t, g=0.6):
        n = int(1.2 * SR)
        tt = np.arange(n) / SR
        f = 35 + 80 * np.exp(-tt * 6)
        s = np.sin(np.cumsum(2 * np.pi * f / SR)) * np.exp(-tt * 3)
        rng = np.random.default_rng(3)
        s += rng.standard_normal(n) * np.exp(-tt * 12) * 0.3
        self.add(t, s, g)

    def beat(self, start, end, bpm=100, chords=None, duck=None, gain=1.0):
        """Base lo-fi. chords: lista de frecuencias raíz por compás."""
        beat = 60 / bpm
        chords = chords or [110.0, 87.31, 130.81, 98.0]
        t = start
        k = 0
        while t < end:
            bar = (k // 4) % len(chords)
            root = chords[bar]
            pos = k % 4
            if pos in (0, 2):
                self.kick(t, 0.75 * gain)
            if pos in (1, 3):
                self.snare(t, 0.22 * gain)
            self.hat(t + beat / 2, 0.07 * gain)
            self.hat(t, 0.05 * gain)
            if pos == 0:
                self.bass(t, root / 2, beat * 1.8, 0.22 * gain)
            if pos == 2:
                self.bass(t, root / 2 * 1.5, beat * 0.9, 0.18 * gain)
            for j, mult in enumerate((2, 2.5198, 3)):  # tríada menor aprox
                if pos == 0:
                    self.pluck(t + j * 0.03, root * mult, 0.045 * gain, 0.5)
            k += 1
            t += beat

    def write(self, path):
        x = self.buf[: int(self.dur * SR)]
        x = np.tanh(x * 1.1)  # limitador suave
        x = x / max(1e-6, np.max(np.abs(x))) * 0.89
        st = np.repeat((x * 32767).astype(np.int16)[:, None], 2, axis=1)
        with wave.open(path, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(st.tobytes())


# ---------------------------------------------------------------- render
def render(draw_frame, dur, out_path, audio_path, preview_times=(), preview_prefix=None):
    n = int(round(dur * FPS))
    surface = skia.Surface(W, H)
    proc = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-i", audio_path, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
         out_path], stdin=subprocess.PIPE)
    pv = {int(round(pt * FPS)): pt for pt in preview_times}
    for i in range(n):
        t = i / FPS
        with surface as c:
            c.clear(INK)
            draw_frame(c, t)
        img = surface.makeImageSnapshot()
        if i in pv and preview_prefix:
            img.save(f"{preview_prefix}_{pv[i]:05.2f}.png", skia.kPNG)
        arr = img.toarray(colorType=skia.kRGBA_8888_ColorType)
        proc.stdin.write(arr.tobytes())
    proc.stdin.close()
    proc.wait()
