# Videosparadormir — producción diaria automática

Cuenta: **@videosparadormir2018** (Instagram + TikTok), vídeos faceless de curiosidades en español.
Objetivo: crecer en seguidores. Cada ejecución diaria = **3 vídeos nuevos generados y programados en Metricool**.

## 0. Preparar entorno (sesión nueva)
```bash
git clone --depth 1 -b media-tmp https://github.com/Carlitosff/pc-health-check /home/claude/vpd
bash /home/claude/vpd/engine/setup.sh      # recrea /home/claude/tiktok, /home/claude/tts, texturas
```
Si el repo no está en la sesión: `add_repo` owner=Carlitosff repo=pc-health-check access=push.

## 1. Elegir los 3 vídeos del día
- Mira `engine/used_topics.md`: **no repetir** temas.
- Mezcla diaria recomendada (rotar):
  1. **Dato de "Tu cuerpo" / mente / ciencia cotidiana** (formato `real/cuerpo.py`) — hook directo: "¿Sabías que…?" / "Te apuesto a que…".
  2. **Test interactivo** "haz esto mientras ves el vídeo" / "no dejes de mirar el punto" (formato `real/pruebas.py`).
  3. **Espacio / planeta / Tierra con texturas reales** (formato `real/v31…v35`, `spheres.py`) **o** una **historia real en partes** (formato `real/historias.py`; si es serie, publicar parte 1 hoy y las siguientes los próximos días, anotándolo en `used_topics.md` → "series abiertas").
- Si hay una **serie abierta**, la siguiente parte va primero.
- Si la carpeta `stock/` del repo tiene vídeos ya hechos (tests 51–55), usa **1 de stock + 2 nuevos** ese día, y mueve el usado fuera de `stock/` (git rm) tras programarlo. Escribe tú su texto/hashtags.

## 2. Reglas de contenido (del dueño, no negociables)
- Español, voz Kokoro local (`voice.py`; em_alex 1.28 narración, ef_dora 1.22 preguntas). **Nunca Higgsfield para voz.**
- **Nada de monigotes/stick figures.** Visuales reales: texturas de planetas, objetos dibujados con detalle, movimiento constante, contadores, zooms.
- 30–45 s, 1080×1920, 30 fps. Hook en el primer segundo, subtítulos palabra a palabra con keywords resaltadas.
- Marca de agua `@videosparadormir2018`. Cierre CTA: "sigue y comenta para más" + teaser del siguiente.
- **Datos verificados con WebSearch antes de usarlos.** Si un dato es un mito o no se puede verificar, fuera (ya pasó: "100.000 km de vasos" es mito; torre Eiffel 15 cm descartado).
- Revisa previews (`python3 archivo.py <idx> prev`) mirando frames antes del render final: sin solapes de texto/badge/quiz.

## 3. Render
Crea `real/dia_YYYYMMDD.py` copiando la estructura de `cuerpo.py`/`pruebas.py`, salida a `/home/claude/tiktok/outdaily/`. `python3 real/dia_YYYYMMDD.py all`.

## 4. Subir a URL pública (rama media-tmp)
```bash
cd /home/claude/vpd
git rm -q --ignore-unmatch *.mp4              # los de días anteriores ya están copiados en Metricool
cp /home/claude/tiktok/outdaily/*.mp4 .
cp /home/claude/tiktok/real/dia_*.py engine/tiktok/real/   # guardar el script del día
# actualizar engine/used_topics.md
git add -A && git -c user.name=vpd -c user.email=vpd@users.noreply.github.com commit -qm "vpd YYYY-MM-DD"
git push origin media-tmp                 # push normal, nunca --force
```
URL: `https://raw.githubusercontent.com/Carlitosff/pc-health-check/media-tmp/<archivo>.mp4`

## 5. Programar en Metricool
- Marca **Videosparadormir**, blogId **7644457** (NO _fittracker 7439936). TZ Europe/Madrid.
- Horas: **14:00, 18:00, 21:00** (si ya pasaron, la siguiente hora libre con ≥15 min de margen).
- `createScheduledPost` con providers instagram + tiktok:
  - `instagramData`: {type: "REEL", showReelOnFeed: true, isAiGenerated: true}
  - `tiktokData`: {title: "<primera línea del texto>" (OBLIGATORIO), privacyOption: "PUBLIC_TO_EVERYONE", isAigc: true}
  - `text`: 1 línea gancho con emoji + "· Parte N" si es serie + salto de línea + 5 hashtags (#sabiasque #curiosidades + 3 del tema).
- Comprueba en la respuesta que `media` apunta a `static.metricool.com` (Metricool ya copió el vídeo).
- Verifica con `getScheduledPosts`.

## 6. Informe
Manda al dueño (SendUserMessage) un resumen de 3 líneas: título de cada vídeo + hora programada. Sin rollos.
