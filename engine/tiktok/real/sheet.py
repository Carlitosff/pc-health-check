"""Hoja de stills: python3 sheet.py <dir o lista de jpg> salida.jpg [ancho] [--noguides]
v36 (25/11): dibuja encima de cada still las ZONAS PROHIBIDAS del montaje (franja de subtítulos y<700, botón de seguir del CTA y=1120–1540,
pill de voto/dato y≈1580 y rótulo de fuente K.tag y≈1840) y el segundo de cada still, en filas de 6. Así se ve de un vistazo si un rótulo 3D
o el sujeto caen debajo de un texto del motor (fallo repetido en 2003, 2803, 3003, 3103, 3203)."""
import sys, glob, re, os
from PIL import Image, ImageDraw
a = sys.argv[1]; out = sys.argv[2]
args = [x for x in sys.argv[3:] if not x.startswith("--")]
w = int(args[0]) if args else 240
guides = "--noguides" not in sys.argv
fs = glob.glob(a + "/still_*.jpg") if os.path.isdir(a) else a.split(",")
tof = lambda f: float(re.findall(r"still_([\d.]+?)\.jpg", f)[0]) if "still_" in f else 0
fs.sort(key=tof)
h = int(w * 16 / 9); per = 6; rows = (len(fs) + per - 1) // per
s = Image.new("RGB", (w * min(per, len(fs)), h * rows), (0, 0, 0))
k = w / 1080
ZONES = [(0, 700, (255, 60, 60), "SUBT"), (1120, 1540, (255, 200, 40), "CTA"), (1545, 1625, (80, 200, 255), "PILL"), (1800, 1880, (180, 120, 255), "TAG")]
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB").resize((w, h))
    if guides:
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for y0, y1, col, name in ZONES:
            d.rectangle([0, int(y0 * k), w, int(y1 * k)], outline=col + (255,), width=1, fill=col + (38,))
            d.text((3, int(y0 * k) + 2), name, fill=col + (255,))
        d.text((w - 46, h - 14), f"{tof(f):.1f}s", fill=(255, 255, 255, 255))
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    s.paste(im, ((i % per) * w, (i // per) * h))
s.save(out, quality=85); print(out, len(fs))
