# Videosparadormir: producción diaria automática (v3 · desde 01/11/2026: MENOS Y MEJOR)

> **AVISO 04/11 noche (decisión de Carlos, manda sobre todo lo anterior de voz):** la voz es ahora `supertonic:4` (la "voz 5" que eligió Carlos de Supertonic 3, femenina), porque no le gustaba `em_alex`, y pidió que respete más las pausas. Ya está en `core.VOICES`. Es local y se baja de GitHub en setup.sh. No la cambies sin un A/B que Carlos escuche. Si `voice.FALLBACK_USED` no está vacío, algún vídeo salió con Kokoro: dilo en el resumen. Guion: la voz se atropella y se entiende peor con frases muy cortas en cadena ('Míralos. Uno pisa.'), así que une ideas en frases de 5 palabras o más. Antes de renderizar cada vídeo ejecuta `sys.path.insert(0,'/home/claude/tts2'); import check_voice; print(check_voice.check(V['segs']))` y reescribe los segmentos que salgan: Whisper falla algo en frases cortas y con cifras, así que mira si el error es real. Las pausas alargan un 10-15 %: respeta 25-38 s.

> **AVISO 01/11 noche (cambio de Carlos en directo, manda sobre el prompt de la tarea programada):** la voz es ahora `kokoroN:em_alex` (muestra D, modelo Kokoro completo) y el reto diario es la CIUDAD (`real/ciudad.py`), no la montaña. Si el prompt de la tarea programada todavía dice "em_santa" o "montana.py", está desactualizado: no reviertas `core.VOICES` y usa `ciudad.py` (`montana.py` ya redirige a `ciudad.py`; desde 04/11 usa `ciudad3d.py`).

> **AVISO 02/11 (dato de Metricool):** los TRIAL REEL NO funcionan en esta cuenta: el 804 (mito perro y cola, 01/11 17:30) dio ERROR 'The instagram account does not meet the trial reel follower requirement' y NUNCA SE PUBLICÓ. Instagram no dice el mínimo en nada que hayamos podido leer. Hasta que la cuenta crezca, los 4 van como REEL normal aunque el prompt pida un Trial; reintenta un solo Trial cuando pase de 1.000 seguidores. Tras programar, revisa también el `status` de los posts del día anterior en `getScheduledPosts` (un post PENDING puede acabar en ERROR horas después).

**Cuenta:** @videosparadormir2018. **Desde el 27/10/2026 se publica SOLO en Instagram** (TikTok no daba alcance). Vídeos faceless de curiosidades, en español.

**Objetivo (Carlos, 31/10):** de ~100 a **1.000 seguidores**, y subir likes, envíos y comentarios. Diagnóstico 31/10 (155 reels): techo de ~1.300 vistas por reel, 0–1 envíos, likes 1,5–2,5%, tiempo medio 11–18 s; publicar 10 o 67 al día da las mismas ~1.050 vistas por reel → el volumen no ayuda, la calidad y la compartibilidad sí. Cada ejecución (05:47) hace lo siguiente:
1. Revisa lo publicado y cómo ha funcionado.
2. Investiga.
3. Mejora el motor.
4. Genera **4 vídeos de calidad + 1 montaña** y los programa en Metricool.
5. Limpia el repo.

El trabajo pesado tiene que estar terminado hacia las 07:00.

> **AVISO 04/11 (decisión de Carlos, manda sobre lo anterior):** 1) La CIUDAD ahora es 3D: `python3 real/ciudad3d.py <antes> <ahora> <slug>`, guion propio en `real/ciudad_guion_<slug>.py` (FRESH = ventanas de color nuevas), estado en `real/ciudad_state.json` (añade ahí las nuevas tras publicar). Hitos: 200, 250, 500… Cada edición trae algo nuevo y visible. 2) 2 de los 4 vídeos diarios van en 3D con `real/v3d/` (escena propia: añade `script` al job; ver `ciudad3d.py`), medidos frente a los no 3D durante 7 días. Render: ~1 s/frame con 2 CPU; Chromium puede caerse en renders largos y `render.mjs` retoma los frames ya hechos. 3) Voz v7: em_alex a 1,08 (preguntas 1,12) y mezcla sin aecho (`V['dry']`, por defecto True). Carlos eligió seguir con voz local (no externa) el 04/11; Hugging Face sigue bloqueado.

> **AVISO 04/11 mañana (motor v15):** para un vídeo 3D nuevo: escena en `real/v3d/<x>.js` que importa `./bloques.js` y un guion que llama a `v3d_run.run3d(V,'<x>.js',overlay=fn)`. Revisa stills con `run3d(...,stills=[t1,t2])` y `sheet.py` antes del render: la franja superior (hasta ~y=700) es de subtítulos y en el CTA el botón de seguir ocupa y=1120–1540; deja el sujeto fuera de ahí. Reutiliza capataz y abuela.

> **AVISO 05/11 (motor v16):** el reto de 1.000 en 24 h terminó sin llegar; 1.000 queda como meta sin plazo hasta que Carlos elija otro reto. Render 3D: `render.mjs` añade desenfoque de movimiento en los cortes; ~1,9–2,9 s/frame con dos a la vez. Para esperar un render usa `ps aux | grep "[n]ombre"`: `pgrep -f nombre` se encuentra a sí mismo y cuelga el bucle. Si lanzas varias esperas, en serie, no en paralelo.

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

## 4. Elegir los 4 vídeos del día (CALIDAD > CANTIDAD, decisión de Carlos 31/10)

Solo 4, así que cada uno tiene que poder ser el mejor de la semana. Criterio nº 1: **¿alguien se lo mandaría a un amigo?** (los envíos por DM son lo que hace que Instagram amplíe un reel; con 0–1 envíos nunca pasa del primer grupo de ~1.200).

Mezcla fija:

| Cantidad | Formato | Por qué |
|---|---|---|
| 1 | **Prueba con tu cuerpo / ilusión que se hace en directo** ("pon los dedos así", "mira el punto") con pregunta visual en el gancho | Únicos con 6–8 envíos (dedo flotante, dedos nunca se tocan) |
| 1 | **Reto para retar a un amigo** (conteo, "¿a que no lo ves?", 3 segundos) con respuesta CALCULADA y CTA "envíaselo a quien crea que lo saca" | Más comentarios (triángulos 1.727, 7 comentarios) |
| 1 | **Mito con "tú"** ("te enseñaron mal…", "tu perro…", "tu cuerpo…") con dato fuerte y fuente con nombre y fecha | Mejor view rate (70–77%) |
| 1 | **Serie** (ilusiones por temporadas, o historia en partes / espacio "lo prometido") que obligue a seguir para ver la siguiente | Da motivo para SEGUIR |

**Listón de calidad (obligatorio, no se publica si falla):**
- Gancho que se entiende sin sonido en el frame 0 (pregunta visual, no texto genérico). Nada de "3 datos de…" sin imagen que obligue a mirar.
- Guion corto: 25–38 s con la voz v5 (las pausas alargan); máx. 6 segmentos; un re-gancho a mitad; la revelación lo más tarde posible.
- Movimiento en todos los planos (cámara, partículas, transiciones); nada estático más de 1 s salvo que la ilusión lo exija.
- Revisa la preview de CADA vídeo (`prev`) y un frame del mp4 final; si algo se ve pobre o solapado, rehazlo antes de subir. Mejor 3 buenos que 4 flojos: si uno no llega, se publican 3 y se dice en el resumen.
- CTA final con acción concreta: comenta X / envíaselo a Y / sígueme para la parte 2.

Fuera: IA/noticias, debates, datos pasivos de espacio sin escala visual, números grandes sin imagen, "haz esto con tu cuerpo" sin pregunta visual (brazo flotante 281, Aristóteles 142).

- **Series:**
  - A veces explícitas ("Parte 1/3").
  - A veces **implícitas**, sin decir "parte": un cliffhanger tipo "lo que pasó después lo cuento mañana…" o "…y eso no fue lo más raro. Sígueme".
  - Las partes siguientes salen otro día. Anota las series abiertas en `used_topics.md` y dales prioridad.
- **(SUSPENDIDO 02/11, ver aviso arriba) TRIAL REEL (Metricool `instagramData.type: "TRIAL_REEL"`):** 1 de los 4 al día (el más experimental: gancho nuevo o formato nuevo) se publica como Trial Reel, que solo se enseña a gente que no te sigue. Así se prueban ganchos sin gastar el alcance de los seguidores. Anota en learnings cuál fue y cómo rindió frente a los REEL normales.

## 4b. LA CIUDAD DE LA COMUNIDAD (sustituye a la montaña desde 01/11 noche, decisión de Carlos)
`python3 real/ciudad.py <antes> <ahora> 8NN_ciudad_<ahora>`: 1 seguidor = 1 ventana encendida; los edificios se llenan de luz y la grúa levanta el siguiente. Estreno 01/11 23:45 con 113 (antes=0 = vídeo de estreno). Hitos: 250 = primer rascacielos, 500, 1.000, 2.000, 5.000, 10.000. Mismas reglas que la montaña (seguidores reales IGEV01, no publicar si no crece, 11:30, texto '…ventanas encendidas 🌃', firstComment 'Comenta ENCIENDE LA MÍA…').

## (Histórico) LA MONTAÑA DE LA COMUNIDAD (31/10–01/11)
Es el formato que más seguidores trae (611: +35 en una noche; 612 → 60; 613 → 90). Cada producción hace 1 vídeo extra (el nº 5):
1. Seguidores REALES: `getAnalyticsDataByMetrics` con IGEV01 (Instagram Evolution > Followers) de los últimos 3 días; usa el último valor. Si Metricool no trae el de hoy, usa el último disponible y no inventes. El 'antes' es el N del último vídeo de montaña (ver `used_topics.md` → MONTAÑA).
2. `python3 real/montana.py <antes> <ahora> 6NN_montana_<ahora>m` (preview con `prev` como 4º argumento). Hitos automáticos: 100 m nieve, 250, 500, 1.000, 2.000, 5.000, Everest 8.849.
3. Si no ha crecido (o ha bajado), NO publiques montaña ese día: no se celebra un estancamiento.
4. Prográmalo a las **11:30** (franja de máxima actividad según Metricool). Texto: 'La montaña ya mide N metros ⛰️ …' + firstCommentText 'Comenta YO SUBO…'.
5. Anota en `used_topics.md` → MONTAÑA el nuevo N y la fecha.

## 5. Reglas fijas del dueño

- **Voz v8 (desde 04/11 noche, ELEGIDA POR CARLOS: voz 5)**: `supertonic:4` = Supertonic 3 int8 a 44,1 kHz (`tts2/supertonic_tts.py`), speed 1,1 (preguntas 1,14), 20 pasos, misma cadena EQ + compresión. Pausas: silencio exacto entre frases (0,55 s) y dentro de la frase '...' en comas y dos puntos, para que pare el propio modelo, ajustando huecos a 0,30-0,38 s. NO sintetices por cláusulas ni cortes por posición estimada (probado: 'sin papaya', pausas a mitad de palabra). Frases cortas: regenera más despacio (RATE). Subtítulos con `voice.speech_warp`. Licencia del modelo: OpenRAIL-M, revisar antes de monetizar. Respaldo automático: Kokoro em_alex.
- **Voz v6 (desde 01/11 noche, ELEGIDA POR CARLOS: muestra D)**: `kokoroN:em_alex` = Kokoro v1.0 completo fp32 (`tts/kokoro-v1.0.onnx`, lo baja setup.sh) con síntesis por FRASE entera (entonación natural), comas alargadas a 0,22 s y cadena EQ + compresión (`voice._polish`). Motivo: em_santa sonaba plana/robótica y no le convencía el timbre. Es el valor por defecto de `core.VOICES`; no lo cambies sin un A/B que Carlos escuche. (v5 em_santa queda en `core.VOICES_SANTA`.)
- **Voz v5 (desde 31/10 noche, ELEGIDA POR CARLOS tras A/B de 4 muestras)**: Kokoro local `em_santa` con pausas reales (`kokoroP:em_santa` en `core.VOICES`, `tts/kokoro_tts.synth_paced`): cada cláusula se sintetiza con su puntuación y se insertan silencios (coma 0,24 s, punto 0,44 s, pregunta 0,48 s). Carlos pidió expresamente 'respeta los tiempos, las comas': no quites las pausas. Las pausas alargan ~25%: escribe guiones más cortos para seguir en 31–40 s. No vuelvas a Piper salvo fallo (queda en `core.VOICES_PIPER`).
- (Histórico) **Voz v4 (31/10, 'menos robótica')**: Piper `piperS:` = síntesis por FRASE completa (no por cláusula), narrador davefx a 1,04 (antes 1,12) y sala ligera (aecho). Ya está en `core.VOICES`; no lo devuelvas a `piper:`. Probadas también es_MX-claude-high y es_AR-daniela-high (sherpa-onnx): acento no peninsular, descartadas por ahora. Para una voz claramente más humana (XTTS/F5) hace falta huggingface.co, que está bloqueado en la sesión: si Carlos lo habilita, probar A/B.
- Español. **Voz v3 (desde 26/10): Piper local con voces de locutores reales** (`tts2/piper_tts.py`, definidas en `core.VOICES`: narrador `piper:es_ES-davefx-medium:0` a 1.12, preguntas `piper:es_ES-sharvard-medium:1` a 1.08). Síntesis por cláusulas con pausas naturales. Kokoro queda solo como respaldo. **Nunca Higgsfield ni servicios externos para la voz.** Si mejoras la voz (otro modelo alcanzable desde GitHub/npm/PyPI), compáralo con un A/B antes de cambiar.
- **Nada de monigotes ni stick figures.** Visuales reales y movimiento constante.
- 30–45 s, 1080×1920, 30 fps. Hook en el primer segundo. Subtítulos palabra a palabra con las keywords resaltadas.
- Marca de agua `@videosparadormir2018`. CTA final: seguir + comentar, con un teaser del siguiente.
- Desde 29/10 (motor v7): en los vídeos compartibles (tests, retos, animales/mascotas, espacio) añade `V['send']='ENVÍASELO A …'` (destinatario concreto: 'a alguien con perro', 'a un amigo y que lo pruebe'). Los envíos por DM son la señal de alcance más fuerte en IG.
- Desde 30/10 (motor v8): en todos los vídeos añade `V['rehook']=(seg_central, 'TEXTO')` (re-gancho a mitad: 'ESPERA… AHORA LO MÁS LOCO', 'AQUÍ FALLA CASI TODO EL MUNDO'). Duración objetivo 31–35 s (espacio/historias hasta 43 s): el tiempo medio se queda en 13–16 s.
- Desde 31/10 (motor v9): en los vídeos con respuesta o dato diferido (retos, ilusiones, mitos) añade `V['reveal']=(seg_revelación, 'LA RESPUESTA')`: cuenta atrás visible hasta ese segmento. Ojo: Metricool puede tardar >18 h en traer los reels del día anterior; si no están, usa el lote de hace 2 días.
- Franjas 12:30 y 15:00: el test del 30/10 las rehabilitó (Hermann 1.351 a las 15:00, Napoleón 1.413 a las 15:30): lo que fallaba era el contenido. Los mejores siguen yendo de noche.
- Desde 31/10 tarde (motor v10): cama musical procedural automática (`core.music_bed`). Elige `V['mood']` ('misterio', 'epico', 'luz') según el tema; `V['music']=0` la quita (p. ej. si un vídeo necesita silencio total). Necesita scipy (setup.sh).
- Desde 01/11 (motor v11): las ilusiones que se ven EN DIRECTO (fijar la vista) llevan `V['steady']=True` y `clean=True` (nada se mueve ni parpadea).
- Desde 02/11 (motor v12): `real/paisaje.py` da fondos fractales de verdad (`sunset`, `cliff_wall`, `miranda_texture`, `fbm`, `ridge`). Para animales, usa SILUETAS a contraluz (`dia_20261102.labrador`), no el perro de espaldas de 804.
- Cap del gancho: en UN SOLO bloque (sin `|`), porque el frame 0 solo enseña el primer bloque y sin sonido no se entendía.
- Antes del render final, revisa las previews (`python3 archivo.py <idx> prev`): sin texto solapado y sin nada cortado.

## 6. Render

- Crea `real/dia_YYYYMMDD.py`. Salida a `/home/claude/tiktok/outdaily/`.
- Ejecuta `python3 real/dia_YYYYMMDD.py all`.
- Comprueba duración y audio con ffprobe.

- Desde 03/11 (motor v13): pasa `python3 real/qa.py outdaily/*.mp4` antes de subir; si da FALLO, se rehace (`--steady` solo para ilusiones de fijar la vista).

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
- **Horario (desde 01/11, según `getBestTimeToPostByNetwork` de Metricool: pico 10–12 h ≈6.500, 17–18 h ≈4.800, 22–23 h solo ≈900):**
  - **10:00** vídeo · **11:30** MONTAÑA · **13:00** vídeo · **17:30** vídeo · **19:30** vídeo.
  - El mejor vídeo del día va a las 10:00 o 13:00. Revisa la curva de Metricool una vez por semana por si cambia.
  - Una serie no se publica antes que su parte anterior.
- **SOLO INSTAGRAM (decisión del dueño, desde el 27/10/2026):** no publiques nada en TikTok. providers = [{"network":"instagram"}] y sin `tiktokData`.
- **`createScheduledPost`**, con providers solo instagram:
  - `instagramData`: {type: "REEL", showReelOnFeed: true, isAiGenerated: true} (el Trial Reel del día: type "TRIAL_REEL").
  - **Audio en tendencia: RECHAZADO 01/11 (403, cuenta sin acceso al catálogo). No usar.** (Antes:) `instagramData.audioConfiguration` con un audio popular y `audioVolume` bajo (10–15) y `videoVolume` 100. Solo funciona si la cuenta es de empresa conectada a una página de Facebook: si Metricool lo rechaza, anótalo en learnings y no lo vuelvas a intentar.
  - `videoCoverMilliseconds`: 900 (portada = gancho XL ya dibujado; motor v5).
  - `firstCommentText`: la pregunta del CTA con respuesta concreta (desde 28/10).
  - `text`: una línea gancho con emoji (+ "· Parte N" si es una serie explícita), salto de línea y 5 hashtags (#sabiasque #curiosidades + 3 del tema).
- **Comprobación:** en la respuesta, `media` tiene que apuntar a `static.metricool.com`. Eso confirma que Metricool ya copió el vídeo. Verifica también con `getScheduledPosts`.

## 9. Limpiar el repo (cuando todos estén confirmados en Metricool)

```bash
cd /home/claude/vpd && git rm -q *.mp4 && git -c user.name=vpd -c user.email=vpd@users.noreply.github.com commit -qm "vpd YYYY-MM-DD clean" && git push origin media-tmp
```

Solo se borran los mp4 de la raíz; `engine/` y `stock/` se quedan. Si algún post falló en Metricool, no borres su vídeo hasta reintentarlo.

## 10. Registrar e informar

- Actualiza `used_topics.md` (temas, series abiertas, log del día) y `learnings.md`. Haz commit y push.
- Manda a Carlos con SendUserMessage:
  - Las 5 líneas: hora + título (4 vídeos + montaña).
  - 1 línea con la mejora del motor de hoy.
  - 1 línea con el aprendizaje principal sacado de las métricas.
  - Cualquier fallo, dicho claro.
