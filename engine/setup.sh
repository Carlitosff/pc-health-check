#!/usr/bin/env bash
# Recrea el entorno de render en /home/claude (mismas rutas que usa el código)
set -e
R=$(cd "$(dirname "$0")" && pwd)
mkdir -p /home/claude/tiktok /home/claude/tts /home/claude/t3d/tex
cp -r "$R/tiktok/." /home/claude/tiktok/; cp "$R/tts/"* /home/claude/tts/
pip install -q --break-system-packages skia-python onnxruntime numpy pillow
which espeak-ng >/dev/null || (apt-get install -y -q espeak-ng)
cd /home/claude/tts && [ -f kokoro-q8.onnx ] || { npm i -s kokoro-js kokoro-q8-shards >/dev/null; cat node_modules/kokoro-q8-shards/kokoro-q8.part{0..5}.bin > kokoro-q8.onnx; }
T3=https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets
TX=https://raw.githubusercontent.com/jeromeetienne/threex.planets/master/images
cd /home/claude/t3d/tex
for f in earth_atmos_2048.jpg earth_clouds_1024.png earth_lights_2048.png earth_normal_2048.jpg earth_specular_2048.jpg moon_1024.jpg; do [ -f $f ] || curl -sfO $T3/$f; done
for f in jupitermap.jpg marsmap1k.jpg mercurymap.jpg neptunemap.jpg saturnmap.jpg saturnringcolor.jpg sunmap.jpg uranusmap.jpg venusmap.jpg; do [ -f $f ] || curl -sfO $TX/$f; done
ls /home/claude/t3d/tex | wc -l
