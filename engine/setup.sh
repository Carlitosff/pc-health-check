#!/usr/bin/env bash
# Recrea el entorno de render en /home/claude (mismas rutas que usa el código)
set -e
R=$(cd "$(dirname "$0")" && pwd)
mkdir -p /home/claude/tiktok /home/claude/tts /home/claude/tts2 /home/claude/t3d/tex
cp -r "$R/tiktok/." /home/claude/tiktok/; cp "$R/tts/"* /home/claude/tts/; cp "$R/tts2/"* /home/claude/tts2/
pip install -q --break-system-packages skia-python onnxruntime numpy pillow scipy
which espeak-ng >/dev/null || (apt-get update -qq && apt-get install -y -q espeak-ng) || echo "aviso: espeak-ng no instalado"
cd /home/claude/tts && [ -f kokoro-q8.onnx ] || { npm i -s kokoro-js kokoro-q8-shards >/dev/null; cat node_modules/kokoro-q8-shards/kokoro-q8.part{0..5}.bin > kokoro-q8.onnx; }
# v6 voz (01/11 noche): modelo Kokoro v1.0 COMPLETO fp32 (GitHub kokoro-onnx), usado por core.VOICES kokoroN:em_alex
cd /home/claude/tts && [ -f kokoro-v1.0.onnx ] || curl -sfL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
T3=https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets
TX=https://raw.githubusercontent.com/jeromeetienne/threex.planets/master/images
cd /home/claude/t3d/tex
for f in earth_atmos_2048.jpg earth_clouds_1024.png earth_lights_2048.png earth_normal_2048.jpg earth_specular_2048.jpg moon_1024.jpg; do [ -f $f ] || curl -sfO $T3/$f; done
for f in jupitermap.jpg marsmap1k.jpg mercurymap.jpg neptunemap.jpg saturnmap.jpg saturnringcolor.jpg sunmap.jpg uranusmap.jpg venusmap.jpg; do [ -f $f ] || curl -sfO $TX/$f; done
ls /home/claude/t3d/tex | wc -l
# Voces Piper (locutores reales, voz v3): narrador davefx (es_ES) + preguntas sharvard F (es_ES)
cd /home/claude/tts2
for m in es_ES-davefx-medium es_ES-sharvard-medium; do
  [ -d vits-piper-$m ] || { curl -sfL -o $m.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-$m.tar.bz2 && tar xjf $m.tar.bz2 && rm $m.tar.bz2; }
done
ls -d /home/claude/tts2/vits-piper-* | wc -l
# v14 (04/11): 3D con Three.js (real/v3d, render determinista con el Chromium preinstalado)
cd /home/claude/tiktok/real/v3d && [ -d node_modules/three ] || npm i --silent three@0.187.0
