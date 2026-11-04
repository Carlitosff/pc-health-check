"""Hoja de stills: python3 sheet.py <dir o lista de jpg> salida.jpg [ancho]"""
import sys, glob, re, os
from PIL import Image
a = sys.argv[1]; out = sys.argv[2]; w = int(sys.argv[3]) if len(sys.argv) > 3 else 240
fs = glob.glob(a + "/still_*.jpg") if os.path.isdir(a) else a.split(",")
fs.sort(key=lambda f: float(re.findall(r"still_([\d.]+?)\.jpg", f)[0]) if "still_" in f else 0)
h = int(w * 16 / 9); s = Image.new("RGB", (w * len(fs), h))
for i, f in enumerate(fs):
    s.paste(Image.open(f).resize((w, h)), (i * w, 0))
s.save(out, quality=85); print(out, len(fs))
