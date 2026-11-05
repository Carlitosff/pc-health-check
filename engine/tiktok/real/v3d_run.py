"""Corre un vídeo 3D: V (guion del motor) + escena Three.js en v3d/<script>. Frames en JPEG, y K.run monta encima subtítulos, marca de agua, CTA y audio.
Uso desde un guion: run3d(V, 'playa.js', overlay=fn)  |  python3 x.py prev t1,t2,... guarda stills sin montar."""
import json, os, shutil, subprocess, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/claude/tiktok/outdaily"
VIG = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(K.W / 2, K.H * .56), K.H * .72, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, .42)], [0, .62, 1]))


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
        c.drawImage(skia.Image.MakeFromEncoded(skia.Data.MakeWithCopy(open(p, "rb").read())), 0, 0)
        c.drawRect(skia.Rect.MakeWH(K.W, K.H), VIG)  # v16: viñeta de cine: centra la mirada sin coste de render
        if overlay:
            overlay(c, t, P)
    K.run(V, scene, OUT)
    if not keep:
        shutil.rmtree(FR, ignore_errors=True)
