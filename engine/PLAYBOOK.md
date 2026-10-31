# Videosparadormir: producción diaria automática (v2)

**Cuenta:** @videosparadormir2018. **Desde el 27/10/2026 se publica SOLO en Instagram** (TikTok no daba alcance). Vídeos faceless de curiosidades, en español.

**Objetivo único:** crecer en alcance y seguidores, día tras día. Cada ejecución (05:47) hace lo siguiente:
1. Revisa lo publicado y cómo ha funcionado.
2. Investiga.
3. Mejora el motor.
4. Genera **10 vídeos** y los programa en Metricool.
5. Limpia el repo.

El trabajo pesado tiene que estar terminado hacia las 07:00.

## 0. Preparar el entorno (sesión nueva)

```bash
git clone --depth 1 -b media-tmp https://github.com/Carlitosff/pc-health-check /home/claude/vpd
bash /home/claude/vpd/engine/setup.sh      # recrea /home/claude/tiktok, /home/claude/tts y las texturas
```

Si el repo no está en la sesión: `add_repo` con owner=Carlitosff, repo=pc-health-check, access=push.

## 1. Revisar lo publicado (antes de idear nada)

- Lee `engine/used_topics.md` y los scripts de días anteriores en `engine/tiktok/real/dia_*.py`. **Prohibido repetir** un tema o un dato, incluso reformulado.
- Saca métricas de Metricool de los últimos 7–14 días:
  - Herramientas: `getAnalyticsAvailableMetrics` y luego `getAnalyticsDataByMetrics`.
  - Datos: Instagram reels (TikTok ya no se usa), con vistas, retención/tiempo medio, likes, comentarios, compartidos, guardados y seguidores ganados.
- Anota en `engine/learnings.md` qué formatos, hooks, duraciones y horas rinden más y cuáles menos (con números). Lo que funcione se repite con temas nuevos; lo que falle se cambia o se abandona.
- Si Metricool trae datos de competencia (connector competitors), úsalos.

## 2. Investigar (WebSearch, modo extended si hace falta)

- Busca qué está funcionando ahora en cuentas grandes de curiosidades, datos y "sabías que" en español e inglés, en TikTok y Reels:
  - Tipos de hook.
  - Duración.
  - Ritmo de cortes.
  - Formatos virales (tests, "no parpadees", "parte 2 en mi perfil", historias reales, comparativas de escala, experimentos famosos, rarezas históricas…).
- Busca **datos nuevos y potentes**, mejor si son concretos y con nombre y fecha. Ejemplos de tono: "En 1971 un profesor de Stanford…", "En 2018 un estudiante descubrió…", "Este pueblo…".
- **Cada dato se verifica en al menos una fuente fiable antes de usarlo.** Si es mito o no se puede confirmar, fuera. Antecedentes:
  - "100.000 km de vasos sanguíneos" es un mito.
  - Lo de que la Torre Eiffel crece 15 cm se descartó por no poder verificarse.

## 3. Mejorar el motor (cada día, al menos 1 mejora concreta)

- Mejora el código de `engine/tiktok` en alguno de estos frentes:
  - Visuales: más realismo, texturas, partículas, cámara, transiciones.
  - Animación y movimiento.
  - Voz: prosodia, pausas, énfasis, velocidad.
  - Subtítulos.
  - Mezcla de audio y SFX.
  - Hooks de los primeros 1,5 s.
- Las mejoras se guardan en el repo (`engine/tiktok/...`) y se registran en `learnings.md` → "Cambios del motor".
- Se pueden usar recursos gratuitos alcanzables desde la sesión (GitHub, npm, PyPI) si mejoran el resultado y la licencia lo permite. Nunca subas al repo público material con licencia restrictiva: se descarga en `setup.sh`.

## 4. Elegir los 10 vídeos del día

Mezcla orientativa (ajústala según `learnings.md`):

| Cantidad | Formato | Referencia |
|---|---|---|
| 3 | Dato de cuerpo / mente / ciencia cotidiana | `real/cuerpo.py` |
| 2 | Test interactivo ("haz esto mientras lo ves", "no dejes de mirar el punto") | `real/pruebas.py` |
| 2 | Espacio / Tierra / escala, con texturas reales | `real/v31…v35`, `spheres.py` |
| 2 | Historia real en partes (serie) | `real/historias.py` |
| 1 | Formato experimental nuevo, salido de la investigación | — |

Desde el 27/10: **nada de IA/noticias ni debates** (108–251 vistas, view rate 23–48%). Lo que decide es el view rate >3 s.

- **Series:**
  - A veces explícitas ("Parte 1/3").
  - A veces **implícitas**, sin decir "parte": un cliffhanger tipo "lo que pasó después lo cuento mañana…" o "…y eso no fue lo más raro. Sígueme".
  - Las partes siguientes salen otro día. Anota las series abiertas en `used_topics.md` y dales prioridad.
- Si queda algo en `stock/`, se puede usar 1 al día. Escribe tú su texto y quítalo de `stock/` al programarlo.

## 4b. LA MONTAÑA DE LA COMUNIDAD (OBLIGATORIO CADA DÍA, decisión de Carlos 31/10)
Es el formato que más seguidores trae (611: +35 en una noche; 612 → 60; 613 → 90). Cada producción hace 1 vídeo extra (el nº 11):
1. Seguidores REALES: `getAnalyticsDataByMetrics` con IGEV01 (Instagram Evolution > Followers) de los últimos 3 días; usa el último valor. Si Metricool no trae el de hoy, usa el último disponible y no inventes. El 'antes' es el N del último vídeo de montaña (ver `used_topics.md` → MONTAÑA).
2. `python3 real/montana.py <antes> <ahora> 6NN_montana_<ahora>m` (preview con `prev` como 4º argumento). Hitos automáticos: 100 m nieve, 250, 500, 1.000, 2.000, 5.000, Everest 8.849.
3. Si no ha crecido (o ha bajado), NO publiques montaña ese día: no se celebra un estancamiento.
4. Prográmalo en la franja de noche (22:00–23:30) en una hora libre (p. ej. 22:15 o 22:45), sin pisar otro post. Texto: 'La montaña ya mide N metros ⛰️ …' + firstCommentText 'Comenta YO SUBO…'.
5. Anota en `used_topics.md` → MONTAÑA el nuevo N y la fecha.

## 5. Reglas fijas del dueño

- **Voz v4 (desde 31/10, pedido de Carlos: 'menos robótica')**: Piper `piperS:` = síntesis por FRASE completa (no por cláusula), narrador davefx a 1,04 (antes 1,12) y sala ligera (aecho). Ya está en `core.VOICES`; no lo devuelvas a `piper:`. Probadas también es_MX-claude-high y es_AR-daniela-high (sherpa-onnx): acento no peninsular, descartadas por ahora. Para una voz claramente más humana (XTTS/F5) hace falta huggingface.co, que está bloqueado en la sesión: si Carlos lo habilita, probar A/B.
- Español. **Voz v3 (desde 26/10): Piper local con voces de locutores reales** (`tts2/piper_tts.py`, definidas en `core.VOICES`: narrador `piper:es_ES-davefx-medium:0` a 1.12, preguntas `piper:es_ES-sharvard-medium:1` a 1.08). Síntesis por cláusulas con pausas naturales. Kokoro queda solo como respaldo. **Nunca Higgsfield ni servicios externos para la voz.** Si mejoras la voz (otro modelo alcanzable desde GitHub/npm/PyPI), compáralo con un A/B antes de cambiar.
- **Nada de monigotes ni stick figures.** Visuales reales y movimiento constante.
- 30–45 s, 1080×1920, 30 fps. Hook en el primer segundo. Subtítulos palabra a palabra con las keywords resaltadas.
- Marca de agua `@videosparadormir2018`. CTA final: seguir + comentar, con un teaser del siguiente.
- Desde 29/10 (motor v7): en los vídeos compartibles (tests, retos, animales/mascotas, espacio) añade `V['send']='ENVÍASELO A …'` (destinatario concreto: 'a alguien con perro', 'a un amigo y que lo pruebe'). Los envíos por DM son la señal de alcance más fuerte en IG.
- Desde 30/10 (motor v8): en todos los vídeos añade `V['rehook']=(seg_central, 'TEXTO')` (re-gancho a mitad: 'ESPERA… AHORA LO MÁS LOCO', 'AQUÍ FALLA CASI TODO EL MUNDO'). Duración objetivo 31–35 s (espacio/historias hasta 43 s): el tiempo medio se queda en 13–16 s.
- Desde 31/10 (motor v9): en los vídeos con respuesta o dato diferido (retos, ilusiones, mitos) añade `V['reveal']=(seg_revelación, 'LA RESPUESTA')`: cuenta atrás visible hasta ese segmento. Ojo: Metricool puede tardar >18 h en traer los reels del día anterior; si no están, usa el lote de hace 2 días.
- Franjas 12:30 y 15:00: el test del 30/10 las rehabilitó (Hermann 1.351 a las 15:00, Napoleón 1.413 a las 15:30): lo que fallaba era el contenido. Los mejores siguen yendo de noche.
- Desde 31/10 tarde (motor v10): cama musical procedural automática (`core.music_bed`). Elige `V['mood']` ('misterio', 'epico', 'luz') según el tema; `V['music']=0` la quita (p. ej. si un vídeo necesita silencio total). Necesita scipy (setup.sh).
- Antes del render final, revisa las previews (`python3 archivo.py <idx> prev`): sin texto solapado y sin nada cortado.

## 6. Render

- Crea `real/dia_YYYYMMDD.py`. Salida a `/home/claude/tiktok/outdaily/`.
- Ejecuta `python3 real/dia_YYYYMMDD.py all`.
- Comprueba duración y audio con ffprobe.

## 7. Subir a una URL pública (rama media-tmp)

```bash
cd /home/claude/vpd
cp /home/claude/tiktok/outdaily/*.mp4 .
cp /home/claude/tiktok/real/dia_*.py engine/tiktok/real/
git add -A && git -c user.name=vpd -c user.email=vpd@users.noreply.github.com commit -qm "vpd YYYY-MM-DD media"
git push origin media-tmp                 # push normal, nunca --force ni borrar ramas
```

URL de cada vídeo: `https://raw.githubusercontent.com/Carlitosff/pc-health-check/media-tmp/<archivo>.mp4`

## 8. Programar en Metricool (todo el mismo día)

- **Marca y zona:** marca **Videosparadormir**, blogId **7644457** (NUNCA el 7439936). Zona horaria Europe/Madrid.
- **Horario de los 10 vídeos:** **12:00, 12:30, 15:00, 15:30, 21:00, 21:30, 22:00, 22:30, 23:00, 23:30**.
  - Los mejores (según `learnings.md`) van en la franja 21–23:30.
  - Una serie no se publica antes que su parte anterior.
- **SOLO INSTAGRAM (decisión del dueño, desde el 27/10/2026):** no publiques nada en TikTok. providers = [{"network":"instagram"}] y sin `tiktokData`.
- **`createScheduledPost`**, con providers solo instagram:
  - `instagramData`: {type: "REEL", showReelOnFeed: true, isAiGenerated: true}
  - `videoCoverMilliseconds`: 900 (portada = gancho XL ya dibujado; motor v5).
  - `firstCommentText`: la pregunta del CTA con respuesta concreta (desde 28/10).
  - `text`: una línea gancho con emoji (+ "· Parte N" si es una serie explícita), salto de línea y 5 hashtags (#sabiasque #curiosidades + 3 del tema).
- **Comprobación:** en la respuesta, `media` tiene que apuntar a `static.metricool.com`. Eso confirma que Metricool ya copió el vídeo. Verifica también con `getScheduledPosts`.

## 9. Limpiar el repo (cuando los 10 estén confirmados en Metricool)

```bash
cd /home/claude/vpd && git rm -q *.mp4 && git -c user.name=vpd -c user.email=vpd@users.noreply.github.com commit -qm "vpd YYYY-MM-DD clean" && git push origin media-tmp
```

Solo se borran los mp4 de la raíz; `engine/` y `stock/` se quedan. Si algún post falló en Metricool, no borres su vídeo hasta reintentarlo.

## 10. Registrar e informar

- Actualiza `used_topics.md` (temas, series abiertas, log del día) y `learnings.md`. Haz commit y push.
- Manda a Carlos con SendUserMessage:
  - Las 10 líneas: hora + título.
  - 1 línea con la mejora del motor de hoy.
  - 1 línea con el aprendizaje principal sacado de las métricas.
  - Cualquier fallo, dicho claro.
