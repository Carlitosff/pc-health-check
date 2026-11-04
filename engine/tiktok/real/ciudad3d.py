"""LA CIUDAD DE LA COMUNIDAD en 3D (motor v14, 04/11). 1 seguidor = 1 ventana; Three.js dibuja la ciudad y el motor skia pone subtítulos, marca de agua, CTA y audio.
Uso: python3 ciudad3d.py <antes> <ahora> <slug> [--voz-rapida] [--prev t1,t2,..]
Estado de ventanas de colores: engine/ciudad_state.json ({'special':[{'idx':..,'color':'#ff1f2e'}]}).
Las líneas del guion del día van en real/ciudad_guion_<slug>.py si existe (define SEGS y opcional FRESH); si no, se usa el guion estándar."""
import json, os, shutil, subprocess, sys, importlib.util
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, draw_text, fill, with_alpha
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/claude/tiktok/outdaily"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
OLD, N, SLUG = int(args[0]), int(args[1]), args[2]
prev = None
if "--prev" in sys.argv:
    prev = sys.argv[sys.argv.index("--prev") + 1]; args = [a for a in args if a != prev]
GOALS = [200, 250, 500, 1000, 2000, 5000, 10000]
GOAL = next(g for g in GOALS if g > N)
for a_ in sys.argv:
    if a_.startswith("--goal="):
        GOAL = int(a_[7:])
GOLD = 0xFFFFC23A
STATE = os.environ.get("CIUDAD_STATE", os.path.join(HERE, "ciudad_state.json"))
st = json.load(open(STATE)) if os.path.exists(STATE) else {"special": []}
num = lambda n: f"{n:,}".replace(",", ".")
FRESH = []
SEGS = None
gp = os.path.join(HERE, f"ciudad_guion_{SLUG}.py")
if os.path.exists(gp):
    sp = importlib.util.spec_from_file_location("g", gp); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g)
    SEGS, FRESH = g.SEGS, getattr(g, "FRESH", [])
if SEGS is None:
    SEGS = [dict(id="h", who="nar", say=f"Solo faltan {GOAL - N} para las {GOAL} ventanas.", cap=f"Solo faltan *{num(GOAL - N)}* para las *{num(GOAL)}*", hold=.1),
            dict(id="s1", who="nar", cut=True, say=f"Cada ventana es una persona. Ayer eran {OLD}. Mirad ahora.", cap=f"Cada *ventana* | es un seguidor: | de *{num(OLD)}*… a *{num(N)}*", hold=1.2),
            dict(id="s2", who="nar", cut=True, say="Y estas de colores, las habéis elegido vosotros.", cap="Las de *colores* | las elegís | *vosotros*"),
            dict(id="s3", who="nar", cut=True, say=f"Quedan {GOAL - N} a oscuras.", cap=f"Quedan *{num(GOAL - N)}* | a oscuras"),
            dict(id="cta", who="nar", cut=True, say="Sígueme, y la siguiente ventana es la tuya.", cap="La siguiente | ventana | es la *TUYA*")]
V = dict(slug=SLUG, accent=GOLD, drone=0.02, mood="epico", tease=None, rehook=None, segs=SEGS)
if SEGS and globals().get("g") is not None:
    V.update(getattr(g, "EXTRA", {}))
P = K.plan(V)
hop = K.voice.SR // 30 if hasattr(K.voice, "SR") else 44100 // 30
vo = P["vo"]["nar"]
rms = np.sqrt(np.convolve(vo ** 2, np.ones(hop) / hop, mode="same"))[::hop]
rms = rms / (np.percentile(rms[rms > 1e-4], 95) + 1e-9)
mouth = [round(float(min(1, max(0, (x - .1) * 1.3))), 2) for x in rms]
idx = len(st["special"])
fresh_idx = {s["idx"] for s in FRESH}
special = [dict(s, fresh=False, seq=0) for s in st["special"] if s["idx"] not in fresh_idx]
for i, s in enumerate(FRESH):
    special.append(dict(s, fresh=True, seq=i))
FR = f"/home/claude/tiktok/v3d_frames/{SLUG}"
job = dict(clock=getattr(globals().get("g"), "CLOCK", None), hito=getattr(globals().get("g"), "HITO", None), vote=getattr(globals().get("g"), "VOTE", False), old=OLD, n=N, goal=GOAL, tl={k: list(v) for k, v in P["tl"].items() if k in ("h", "s1", "s2", "s3", "cta")}, total=P["total"], mouth=mouth, special=special, frames=FR)
os.makedirs(FR, exist_ok=True)
jf = f"{FR}/job.json"; json.dump(job, open(jf, "w"))
print(f"{SLUG}: {P['total']:.1f}s  tl={job['tl']}")
env = dict(os.environ, NODE_PATH=subprocess.check_output(["npm", "root", "-g"], text=True).strip())
render = [ "node", os.path.join(HERE, "v3d/render.mjs"), jf]
if prev:
    subprocess.run(render + prev.split(","), env=env, check=True)
    sys.exit(0)
for intento in range(4):  # Chromium puede caerse en renders largos: render.mjs retoma donde se quedó
    if subprocess.run(render, env=env).returncode == 0:
        break
else:
    raise SystemExit("render 3D fallido tras 4 intentos")
tl = job["tl"]
surface_cache = {}
def scene(c, t, P_):
    i = int(round(t * 30))
    p = f"{FR}/f{min(i, int(P['total'] * 30)):05d}.jpg"
    im = skia.Image.MakeFromEncoded(skia.Data.MakeWithCopy(open(p, "rb").read()))
    c.drawImage(im, 0, 0)
    a1, b1 = tl["s1"]
    if t >= a1:
        k = K.smooth((t - a1 - .5) / max(.1, b1 - a1 - .75))
        n = OLD + (N - OLD) * k
        if tl["s2"][0] - .1 < t < tl["s2"][1] - .3:
            if getattr(globals().get("g"), "HITO", None) and t > tl["s2"][0] + 1.4:
                K.tag(c, W / 2, 1730, f"VENTANA Nº {g.HITO}", t - tl["s2"][0] - 1.4, accent=GOLD, size=52)
            return
        x, y, w = 190, 790, W - 380
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, 30), 15, 15), fill(with_alpha(0xFF000000, .6)))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w * min(1, n / GOAL), 30), 15, 15), fill(GOLD))
        hc.big(c, f"{num(int(n))}/{num(GOAL)}", W / 2, 725, 80, WHITE, 1.0, 0.0, outline=12)
if __name__ == "__main__":
    K.run(V, scene, OUT)
    if "--keep" not in sys.argv:
        shutil.rmtree(FR, ignore_errors=True)
