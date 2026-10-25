"""Render de planetas con texturas reales (proyección equirectangular) en numpy → skia.Image."""
import math
import numpy as np
import skia
from PIL import Image

TEX = "/home/claude/t3d/tex/"
_cache = {}


def load(name, mode="RGB", width=None):
    key = (name, mode, width)
    if key not in _cache:
        im = Image.open(TEX + name)
        if mode == "A":  # canal alfa (nubes)
            im = im.convert("RGBA").split()[3]
            im = im.resize((2048, 1024), Image.BICUBIC)
        elif mode == "L":
            im = im.convert("L")
        else:
            im = im.convert(mode)
        if width and im.size[0] > width:
            im = im.resize((width, width // 2), Image.LANCZOS)
        _cache[key] = np.asarray(im).astype(np.float32) / 255.0
    return _cache[key]


def _grid(D):
    key = ("grid", D)
    if key not in _cache:
        c = (np.arange(D) + 0.5) / D * 2 - 1
        x, y = np.meshgrid(c, c)
        r2 = x * x + y * y
        mask = r2 <= 1.0
        z = np.sqrt(np.clip(1 - r2, 0, 1))
        r = np.sqrt(r2)
        edge = np.clip((1 - r) * D / 2, 0, 1)
        _cache[key] = (x, -y, z, mask, edge)
        if len([k for k in _cache if isinstance(k, tuple) and k[0] == "grid"]) > 40:
            for k in [k for k in _cache if isinstance(k, tuple) and k[0] == "grid"][:20]:
                del _cache[k]
    return _cache[key]


def _sample(tex, u, v):
    h, w = tex.shape[:2]
    xi = (u * w).astype(np.int32) % w
    yi = np.clip((v * h).astype(np.int32), 0, h - 1)
    return tex[yi, xi]


def _geom(D, tilt, lat0, light):
    key = ("geom", D, round(tilt, 3), round(lat0, 3), tuple(round(v, 3) for v in light))
    g = _cache.get(key)
    if g is not None:
        return g
    x, y, z, mask, edge = _grid(D)
    ct, st = math.cos(tilt), math.sin(tilt)
    xr = x * ct - y * st
    yr = x * st + y * ct
    cl, sl = math.cos(lat0), math.sin(lat0)
    y2 = yr * cl + z * sl
    z2 = -yr * sl + z * cl
    lon = np.arctan2(xr, z2)
    lat = np.arcsin(np.clip(y2, -1, 1))
    u0 = (lon / (2 * math.pi) + 0.5).astype(np.float32)
    v = (0.5 - lat / math.pi).astype(np.float32)
    L = np.array(light, dtype=np.float32)
    L = L / np.linalg.norm(L)
    ndl = x * L[0] + y * L[1] + z * L[2]
    dif = (np.clip((ndl + 0.08) / 1.08, 0, 1) ** 0.9).astype(np.float32)
    hx, hy, hz = L[0], L[1], L[2] + 1
    hn = math.sqrt(hx * hx + hy * hy + hz * hz)
    ndh = (np.clip((x * hx + y * hy + z * hz) / hn, 0, 1) ** 40).astype(np.float32)
    dark = np.clip(1 - (ndl + 0.15) / 0.3, 0, 1).astype(np.float32)
    a = (edge * mask).astype(np.float32)
    g = dict(u0=u0, v=v, dif=dif, ndh=ndh, dark=dark, a=a, z=z.astype(np.float32))
    keys = [k for k in _cache if isinstance(k, tuple) and k[0] == "geom"]
    if len(keys) > 24:
        for k in keys[:12]:
            del _cache[k]
    _cache[key] = g
    return g


def render(D, day, spin=0.0, tilt=0.0, light=(-0.6, 0.35, 0.72), night=None, spec=None, clouds=None,
           cloud_spin=0.0, ambient=0.06, emissive=False, limb=0.0, lat0=0.0, gain=1.0, tint=None, contrast=1.0):
    """D: diámetro en píxeles (se cuantiza). spin: radianes. tilt: inclinación (rad). lat0: latitud frontal."""
    D = max(8, int(D) // 8 * 8)
    g = _geom(D, tilt, lat0, light)
    off = spin / (2 * math.pi)
    u = g["u0"] + off
    v = g["v"]
    col = _sample(day, u, v)[..., :3]
    if emissive:
        out = (col ** contrast) * gain
        if tint is not None:
            out = out * np.array(tint, np.float32)
        if limb:
            out = out * (1 - limb + limb * g["z"][..., None] ** 0.5)
    else:
        lit = ambient + (1 - ambient) * g["dif"]
        out = col * (lit * gain)[..., None]
        if limb:
            out = out * (1 - limb + limb * g["z"][..., None] ** 0.4)
        if spec is not None:
            sp = _sample(spec, u, v)
            out = out + (sp * g["ndh"] * 0.5)[..., None] * np.array([1.0, 0.95, 0.85], np.float32)
        if clouds is not None:
            ca = _sample(clouds, u + cloud_spin / (2 * math.pi), v)
            ca = np.clip(ca * 1.15, 0, 1) * 0.9
            cc = (ambient * 0.6 + (1 - ambient) * g["dif"])[..., None]
            out = out * (1 - ca[..., None]) + cc * ca[..., None]
        if night is not None:
            n = _sample(night, u, v)[..., :3]
            out = out + n * g["dark"][..., None] * np.array([1.0, 0.8, 0.5], np.float32) * 1.3
    a = g["a"]
    out = np.clip(out, 0, 1) * a[..., None]
    rgba = np.empty((D, D, 4), np.uint8)
    rgba[..., :3] = (out * 255).astype(np.uint8)
    rgba[..., 3] = (a * 255).astype(np.uint8)
    return skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)


def draw_planet(c, x, y, R, img):
    """Dibuja la imagen del planeta centrada en (x, y) con radio R exacto (escala sub-píxel)."""
    c.drawImageRect(img, skia.Rect.MakeXYWH(x - R, y - R, 2 * R, 2 * R),
                    skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(AntiAlias=True))


def atmosphere(c, x, y, R, color=0xFF5AA8FF, strength=1.0, light=(-0.6, 0.35)):
    """Halo atmosférico alrededor de un planeta de radio R centrado en (x, y)."""
    a = int(255 * min(1, 0.55 * strength))
    col = (a << 24) | (color & 0xFFFFFF)
    sh = skia.GradientShader.MakeRadial((x, y), R * 1.16, [0x00000000, 0x00000000, col, 0x00000000],
                                        [0, R / (R * 1.16) * 0.97, R / (R * 1.16), 1.0])
    p = skia.Paint(Shader=sh, AntiAlias=True, BlendMode=skia.BlendMode.kPlus)
    c.drawCircle(x, y, R * 1.16, p)


def project(lat_deg, lon_deg, spin=0.0, tilt=0.0, lat0=0.0):
    """Proyecta (lat, lon) del planeta a coordenadas de pantalla unitarias (x, y_abajo, z). z>0 visible."""
    lat, lon = math.radians(lat_deg), math.radians(lon_deg) - spin
    y2 = math.sin(lat)
    xr = math.cos(lat) * math.sin(lon)
    z2 = math.cos(lat) * math.cos(lon)
    cl, sl = math.cos(lat0), math.sin(lat0)
    yr = y2 * cl - z2 * sl
    z = y2 * sl + z2 * cl
    ct, st = math.cos(tilt), math.sin(tilt)
    x = xr * ct + yr * st
    y = -xr * st + yr * ct
    return x, -y, z
