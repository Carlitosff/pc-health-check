"""Corre un vídeo 3D: V (guion del motor) + escena Three.js en v3d/<script>. Frames en JPEG, y K.run monta encima subtítulos, marca de agua, CTA y audio.
Uso desde un guion: run3d(V, 'playa.js', overlay=fn)  |  python3 x.py prev t1,t2,... guarda stills sin montar."""
import json, os, shutil, subprocess, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/claude/tiktok/outdaily"
VIG = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(K.W / 2, K.H * .56), K.H * .72, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, .42)], [0, .62, 1]))


def sat_matrix(sat, warm=0.0):
    """Matriz 4x5 de saturación (0 = blanco y negro, 1 = original) con tinte cálido opcional (sepia, 0–1)."""
    lr, lg, lb = .2126, .7152, .0722
    m = []
    for row, (r, g, b) in enumerate(((1, 0, 0), (0, 1, 0), (0, 0, 1))):
        m += [lr * (1 - sat) + r * sat, lg * (1 - sat) + g * sat, lb * (1 - sat) + b * sat, 0, 0]
    tint = (1 + .10 * warm, 1 + .02 * warm, 1 - .14 * warm)
    for row in range(3):
        for k in range(3):
            m[row * 5 + k] *= tint[row]
    return m + [0, 0, 0, 1, 0]


def grade_at(V, P, t):
    """v30 (19/11): V['grade'] = [(seg, segundos_desde_inicio, saturación[, sepia]), ...] → interpolación suave entre claves.
    Devuelve None si no hay gradación o la imagen va sin tocar (sat 1, sepia 0)."""
    G = V.get("grade")
    if not G:
        return None
    keys = sorted((P["tl"][g[0]][0] + g[1], g[2], g[3] if len(g) > 3 else 0.0) for g in G if g[0] in P["tl"])
    if t <= keys[0][0]:
        s, w = keys[0][1:]
    elif t >= keys[-1][0]:
        s, w = keys[-1][1:]
    else:
        for (ta, sa, wa), (tb, sb, wb) in zip(keys, keys[1:]):
            if ta <= t <= tb:
                x = (t - ta) / max(1e-6, tb - ta); x = x * x * (3 - 2 * x)
                s, w = sa + (sb - sa) * x, wa + (wb - wa) * x
                break
    return None if (s > .999 and w < .001) else (s, w)


def run3d(V, script, overlay=None, stills=None, extra_job=None, keep=False):
    P = K.plan(V)
    hop = 44100 // 30
    vo = P["vo"]["nar"]
    rms = np.sqrt(np.convolve(vo ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    rms = rms / (np.percentile(rms[rms > 1e-4], 95) + 1e-9)
    mouth = [round(float(min(1, max(0, (x - .1) * 1.3))), 2) for x in rms]
    FR = f"/home/claude/tiktok/v3d_frames/{V['slug']}"
    os.makedirs(FR, exist_ok=True)
    job = dict(script=script, tl={k: list(v) for k, v in P["tl"].items()}, total=P["total"], mouth=mouth, frames=FR, **(extra_job or {}))
    jf = f"{FR}/job.json"; json.dump(job, open(jf, "w"))
    print(f"{V['slug']}: {P['total']:.1f}s tl={ {k: round(v[0], 1) for k, v in P['tl'].items()} }", flush=True)
    env = dict(os.environ, NODE_PATH=subprocess.check_output(["npm", "root", "-g"], text=True).strip())
    cmd = ["node", os.path.join(HERE, "v3d/render.mjs"), jf]
    if stills:
        subprocess.run(cmd + [str(s) for s in stills], env=env, check=True)
        return FR
    for _ in range(5):  # render.mjs retoma donde se quedó si Chromium se cae
        if subprocess.run(cmd, env=env).returncode == 0:
            break
    else:
        raise SystemExit("render 3D fallido")

    def scene(c, t, P_):
        i = min(int(round(t * 30)), int(P["total"] * 30))
        p = f"{FR}/f{i:05d}.jpg"
        img = skia.Image.MakeFromEncoded(skia.Data.MakeWithCopy(open(p, "rb").read()))
        sat = grade_at(V, P, t)
        if sat is None:
            c.drawImage(img, 0, 0)
        else:  # v30: gradación de color por guion (blanco y negro ↔ color, sepia)
            c.drawImage(img, 0, 0, paint=skia.Paint(ColorFilter=skia.ColorFilters.Matrix(sat_matrix(*sat))))
        c.drawRect(skia.Rect.MakeWH(K.W, K.H), VIG)  # v16: viñeta de cine: centra la mirada sin coste de render
        if overlay:
            overlay(c, t, P)
    K.run(V, scene, OUT)
    if not keep:
        shutil.rmtree(FR, ignore_errors=True)
