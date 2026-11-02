"""v12 (02/11/2026): PAISAJES PROCEDURALES con ruido fractal (fbm) en numpy: sin licencias y sin descargas.
Hasta ahora los fondos eran auroras y degradados; con esto hay terreno de verdad con perspectiva atmosférica.
  fbm(h, w, seed, ...)    ruido fractal 2D en [0,1] (octavas por interpolación bilineal de rejillas aleatorias)
  ridge(w, seed, ...)     línea de cresta 1D
  sunset(w, h, seed)      atardecer: cielo, sol, 5 cordilleras con perspectiva atmosférica, lago con reflejo
  chroma_invert / gray    para la postimagen de foto: invierte SOLO el color (misma luminancia) o lo quita
  cliff_wall(w, h, seed)  pared de hielo con estratos y grietas, iluminada de lado y que repite en vertical
  miranda_texture(path)   mapa equirectangular de Miranda: coronas con surcos sobre terreno viejo con cráteres
  to_image(rgb)           numpy float [0,1] -> skia.Image"""
import numpy as np
import skia
from PIL import Image, ImageFilter


def _resize(g, h, w):
    gy = np.linspace(0, g.shape[0] - 1, h)
    gx = np.linspace(0, g.shape[1] - 1, w)
    y0 = np.floor(gy).astype(int).clip(0, g.shape[0] - 2)
    x0 = np.floor(gx).astype(int).clip(0, g.shape[1] - 2)
    fy = (gy - y0)[:, None]
    fy = fy * fy * (3 - 2 * fy)
    fx = gx - x0
    fx = fx * fx * (3 - 2 * fx)
    a = g[y0][:, x0] * (1 - fx) + g[y0][:, x0 + 1] * fx
    b = g[y0 + 1][:, x0] * (1 - fx) + g[y0 + 1][:, x0 + 1] * fx
    return a * (1 - fy) + b * fy


def fbm(h, w, seed=1, base=(4, 4), octaves=6, gain=0.5, wrap_y=False):
    rnd = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    gy, gx = base
    for _ in range(octaves):
        g = rnd.random((gy + 1, gx + 1)).astype(np.float32)
        if wrap_y:
            g[-1] = g[0]
        out += _resize(g, h, w) * amp
        tot += amp
        amp *= gain
        gy, gx = gy * 2, gx * 2
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-9)


def ridge(w, seed=1, base=5, octaves=7, gain=0.55):
    rnd = np.random.default_rng(seed)
    out = np.zeros(w, np.float32)
    amp, n = 1.0, base
    xs = np.linspace(0, 1, w)
    for _ in range(octaves):
        pts = rnd.random(n + 1)
        out += np.interp(xs, np.linspace(0, 1, n + 1), pts) * amp
        amp *= gain
        n *= 2
    return (out - out.min()) / (out.max() - out.min() + 1e-9)


def _mix(a, b, k):
    k = np.asarray(k, np.float32)
    if k.ndim == 2:
        k = k[..., None]
    return a * (1 - k) + b * k


def sunset(w=960, h=960, seed=20261102):
    """Atardecer con mucho color y zonas grandes: lo que mejor funciona para una postimagen (detalle fino = se pierde)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = yy / h
    horizon = 0.62
    sky_top = np.array([0.10, 0.22, 0.62], np.float32)
    sky_mid = np.array([0.93, 0.30, 0.38], np.float32)
    sky_low = np.array([1.00, 0.72, 0.18], np.float32)
    s = np.clip(v / horizon, 0, 1)
    img = _mix(sky_top[None, None], sky_mid[None, None], np.clip(s / 0.62, 0, 1))
    img = _mix(img, sky_low[None, None], np.clip((s - 0.62) / 0.38, 0, 1))
    # nubes alargadas
    cl = fbm(h, w, seed + 1, base=(5, 2), octaves=5)
    cl = np.clip((cl - 0.52) / 0.22, 0, 1) * np.clip(1.15 - s, 0, 1)
    img = _mix(img, np.array([1.0, 0.55, 0.62], np.float32)[None, None], cl * 0.8)
    # sol con halo
    sx, sy = w * 0.68, h * horizon * 0.80
    d = np.hypot(xx - sx, yy - sy)
    img = img + np.array([1.0, 0.75, 0.35], np.float32) * (np.exp(-(d / (w * 0.20)) ** 2) * 0.55)[..., None]
    img = _mix(img, np.array([1.0, 0.96, 0.75], np.float32)[None, None], np.clip((w * 0.075 - d) / 3, 0, 1))
    # cordilleras: de lejos (color cielo) a cerca (verde oscuro)
    far = np.array([0.72, 0.36, 0.52], np.float32)
    near = np.array([0.03, 0.26, 0.17], np.float32)
    layers = 5
    for i in range(layers):
        k = i / (layers - 1)
        rd = ridge(w, seed + 10 + i, base=3 + i, octaves=6)
        top = h * (horizon - 0.16 + 0.03 * i) + (1 - rd) * h * (0.17 - 0.02 * i)
        mask = np.clip(yy - top[None, :], 0, 1)
        tex = fbm(h, w, seed + 30 + i, base=(10, 10), octaves=5)
        col = _mix(far, near, k)[None, None] * (0.85 + 0.3 * tex[..., None])
        img = _mix(img, col, mask * (yy < h * horizon + 1))
    # lago: reflejo vertical con ondas
    hz = int(h * horizon)
    wave = fbm(h - hz, w, seed + 50, base=(14, 3), octaves=4) - 0.5
    rows = np.arange(hz, h)
    src_y = np.clip(2 * hz - rows - 1 + (wave[:, w // 2] * (6 + (rows - hz) * 0.25)).astype(int), 0, hz - 1)
    off = (wave * (10 + (rows - hz)[:, None] * 0.18)).astype(int)
    src_x = np.clip(np.arange(w)[None, :] + off, 0, w - 1)
    refl = img[src_y[:, None], src_x]
    water = np.array([0.03, 0.18, 0.34], np.float32)
    dep = ((rows - hz) / max(1, h - hz))[:, None, None]
    img[hz:] = refl * (0.75 - 0.25 * dep) + water * (0.25 + 0.25 * dep)
    lake = Image.fromarray((np.clip(img[hz:], 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(w / 160))
    img[hz:] = np.asarray(lake, np.float32) / 255  # reflejo difuso: sin manchas duras
    return np.clip(img, 0, 1).astype(np.float32)


LUMA = np.array([0.299, 0.587, 0.114], np.float32)


def gray(rgb):
    y = (rgb * LUMA).sum(-1, keepdims=True)
    return np.repeat(y, 3, axis=-1)


def chroma_invert(rgb, sat=1.45):
    """Mismo brillo, color opuesto: al mirarla la retina se adapta y, sobre la versión gris, se ve el color real."""
    y = (rgb * LUMA).sum(-1, keepdims=True)
    return np.clip(y - (rgb - y) * sat, 0, 1).astype(np.float32)


def cliff_wall(w=760, h=2400, seed=7):
    """Pared de hielo gris azulada que repite en vertical: estratos + grietas + luz rasante desde la derecha."""
    n = fbm(h, w, seed, base=(8, 6), octaves=7, gain=0.55, wrap_y=True)
    strata = fbm(h, 8, seed + 1, base=(40, 1), octaves=4, wrap_y=True)[:, :1]
    gy, gx = np.gradient(n)
    relief = np.clip(0.5 + gx * 26 + gy * 6, 0, 1)
    v = 0.30 + 0.42 * relief + 0.20 * (strata - 0.5)
    cr = fbm(h, w, seed + 2, base=(16, 10), octaves=5, wrap_y=True)
    crack = np.clip(1 - np.abs(cr - 0.5) / 0.012, 0, 1)
    v = v * (1 - 0.65 * crack)
    # la zona pegada al borde de luz es más clara
    v = v * np.linspace(0.62, 1.12, w)[None, :]
    img = np.stack([v * 0.86, v * 0.92, v * 1.04], -1)
    return np.clip(img, 0, 1).astype(np.float32)


def miranda_texture(path, w=2048, h=1024, seed=1986):
    n = fbm(h, w, seed, base=(4, 8), octaves=7)
    v = 0.46 + 0.30 * n
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rnd = np.random.default_rng(seed)
    # cráteres en el terreno viejo
    for _ in range(170):
        cx, cy, r = rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(5, 24)
        x0, x1, y0, y1 = int(max(cx - 2 * r, 0)), int(min(cx + 2 * r, w)), int(max(cy - 2 * r, 0)), int(min(cy + 2 * r, h))
        d = np.hypot(xx[y0:y1, x0:x1] - cx, yy[y0:y1, x0:x1] - cy) / r
        v[y0:y1, x0:x1] += np.where(d < 1, -0.10, 0) + np.exp(-((d - 1) / 0.16) ** 2) * 0.09
    # coronas: bandas de surcos que no encajan con el resto (lo que hace única a Miranda)
    for (cx, cy, rx, ry, ang) in ((0.22, 0.55, 300, 190, 0.3), (0.56, 0.42, 330, 230, -0.5), (0.84, 0.62, 260, 170, 1.1)):
        X, Y = xx - cx * w, yy - cy * h
        ca, sa = np.cos(ang), np.sin(ang)
        U, V_ = (X * ca + Y * sa) / rx, (-X * sa + Y * ca) / ry
        rr = np.sqrt(U * U + V_ * V_)
        mask = np.clip((1 - rr) / 0.06, 0, 1)
        warp = fbm(h, w, seed + 9, base=(4, 8), octaves=4)
        gr = 0.5 + 0.5 * np.sin(V_ * 34 + warp * 26 + U * 4)
        v = v * (1 - mask) + mask * (0.40 + 0.24 * gr * (0.6 + 0.6 * n) + 0.10 * n)
    img = np.stack([v * 0.96, v * 0.97, v * 1.02], -1)
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    im.save(path)


def to_image(rgb):
    h, w = rgb.shape[:2]
    a = np.zeros((h, w, 4), np.uint8)
    a[..., :3] = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    a[..., 3] = 255
    return skia.Image.fromarray(a, colorType=skia.kRGBA_8888_ColorType)
