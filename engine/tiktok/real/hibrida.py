"""Motor v29 (18/11/2026): IMÁGENES HÍBRIDAS por código (Oliva, Torralba y Schyns, 'Hybrid images', SIGGRAPH 2006).
Una palabra va en frecuencias BAJAS (manchas suaves: se lee de lejos o con la imagen pequeña) y otra en frecuencias ALTAS (bordes finos:
se lee de cerca). make(near, far) devuelve la imagen en gris (float 0..1) y sus dos componentes para enseñarlas por separado.
check(img) simula la distancia (reducir + desenfocar) y mide con correlación qué palabra domina: assert en el guion."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"


def word(txt, w=1000, h=760, size=430, dy=0):
    im = Image.new("L", (w, h), 0); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, size)
    bb = d.textbbox((0, 0), txt, font=f)
    d.text(((w - bb[2] - bb[0]) / 2, (h - bb[3] - bb[1]) / 2 + dy), txt, font=f, fill=255)
    return np.asarray(im, np.float32) / 255.0


def make(near="SÍ", far="NO", w=1000, h=760, s_low=22.0, s_high=5.0, k_low=0.75, k_high=1.0, sizes=(470, 430)):
    A = word(far, w, h, sizes[1]); B = word(near, w, h, sizes[0])
    low = gaussian_filter(A, s_low)
    high = B - gaussian_filter(B, s_high)
    low = (low - low.mean()) * k_low
    high = high * k_high
    img = np.clip(0.5 - low - high, 0, 1)   # tinta oscura sobre fondo claro
    return img, 0.5 - low, np.clip(0.5 - high, 0, 1), A, B


def view(img, scale):
    """cómo llega la imagen al ojo a 'scale' de su tamaño (1 = cerca, 0.12 = lejos): reducir + desenfoque de la vista."""
    h, w = img.shape
    small = np.asarray(Image.fromarray((img * 255).astype(np.uint8)).resize((max(8, int(w * scale)), max(8, int(h * scale))), Image.LANCZOS), np.float32) / 255
    return gaussian_filter(small, 1.2)


def score(img, A, B, scale):
    v = view(img, scale); h, w = v.shape
    a = np.asarray(Image.fromarray((A * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS), np.float32)
    b = np.asarray(Image.fromarray((B * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS), np.float32)
    a = gaussian_filter(a, 1.2); b = gaussian_filter(b, 1.2)
    cc = lambda x, y: float(np.corrcoef((-x).ravel(), y.ravel())[0, 1])
    return cc(v, a), cc(v, b)   # (parecido a la palabra de lejos, a la de cerca)
