# Aprendizajes (actualizar cada día con números)

## Métricas por formato
- 25/10: Instagram arranca bien (1.000–2.000 vistas por reel, likes, algún seguidor). TikTok ~0 vistas pese a publicar OK vía Metricool. Hipótesis: cuenta nueva + 26 vídeos en 1 día por API sin actividad nativa + sin sonido en tendencia. Vigilar: si TikTok sigue a 0, bajar TikTok a 2-3/día (los mejores) y mantener Instagram con volumen.
(sin datos aún — primera publicación 25/10/2026: serie "Tu cuerpo" 1–10 + historias Violet Jessop y Apolo 13)

- 26/10 (métricas a las 06:00, IG): el lote nocturno del 25/10 cayó a 130–560 vistas salvo los TESTS DE PERCEPCIÓN: 'punto verde que no existe' 1.340 (1er día ~6 h). En el acumulado de 'Tu cuerpo' los 5 mejores son todos interactivos/percepción: anular 2.012, colores que no existen 1.520, punto ciego 1.486, nariz 1.334, cosquillas 1.231; los datos pasivos de la misma serie se quedan en 150–250. Espacio puro: 130–208 salvo 'si el Sol desapareciera' 563. Números (baraja/contar/ajedrez): 64–136 en sus primeras 5 h. Tiempo medio de visionado 9–15 s en casi todo (retención IG no disponible: null).
- 26/10 TIKTOK: BLOQUEADO POR LÍMITE DE API. Todo lo programado del 25/10 21:45 al 26/10 01:30 dio error 403 'too many posts via OpenAPI in the last 24 hours'. Los 15 vídeos del 25/10 13:20–17:50 sí se publicaron, con 0–4 vistas. => TikTok: máximo 5 publicaciones/día vía Metricool, solo en la franja de noche y nunca dentro de las 24 h de un lote grande anterior. Instagram sigue con 10/día.
- Duración: el estudio de OpusClip 2026 (13,5 M clips) da mediana de 41 s en los virales y 80% con subtítulos quemados animados → mantener 30–45 s.

- 26/10 decisión: 5 de 10 son tests/percepción o mitos del cuerpo (lo que más rinde) y van a la noche; espacio y series a mediodía. Medir mañana: ¿los tests de noche superan 1.000? ¿TikTok vuelve a publicar sin 403?

## Hooks que funcionan / no funcionan
- IG 25/10 TOP (vistas): '3 cosas que hace tu cuerpo' 1633 · '3 mentiras que te creíste' 1474 (retención 70%) · cucharadita estrella de neutrones 1405 · miel no caduca 1390 (ret 69%) · humanidad en un terrón 1361 · medusa inmortal 1280 · 23 personas cumpleaños 1194 · más árboles que estrellas 1179.
- Patrón ganador: UN dato de escala/número imposible, dicho en la primera frase, o listas de cuerpo/mitos. Ganan los de 'te rompe la cabeza' con número concreto.
- FLOJOS (<200): quizzes de espacio/historia/verdad-mentira, wombat, plátano, flamencos, Venus, rayo, tiburones, hormigas. Los realistas de planetas del 25/10 (113–159) también flojos en sus primeras horas: espacio puro rinde menos que cuerpo/números/mitos.
- 25/10 23:59: lote de 4 'números que rompen la cabeza' (baraja 52!, contar hasta mil millones, ajedrez 10^120, luz 7,5 vueltas) → medir mañana.

## Formatos nuevos a medir (26/10)
- IA/noticias de IA (6 vídeos 13:30–14:40). Si rinden, meter 1–2 al día (noticias VERIFICADAS de la semana).
- DEBATE / 'esto divide a internet' (barra VS + quiz A/B, CTA 'escribe CON o SIN'): busca comentarios. Si sube comentarios/alcance, meter 1–2 al día. Nunca presentar como cierto algo falso: el 'polémico' es el debate, no el dato.

## Mejores horas
- 25/10: los reels de 12:00–14:30 (lote 'Tu cuerpo' + realistas) acumulan 1.200–2.000; los de 21:45–00:55 se quedan en 130–560 en sus primeras horas (falta ver el acumulado a 24 h antes de concluir).

## Cambios del motor
- 2026-10-26 (v4): (1) punch-in de gancho: zoom 1,22→1 en 0,55 s + destello blanco inicial (pattern interrupt); (2) `V['tease']` = pill roja 'MIRA HASTA EL FINAL' 0,5–3,5 s; (3) `V['badge']` = insignia de serie ('VOYAGER · PARTE 2') en el gancho y en el CTA; (4) ducking del dron bajo la voz (envolvente 120 ms, −65%); (5) setup.sh: `apt-get update` antes de espeak-ng (fallaba en sesión nueva) y stubs scripts.py/scripts2.py (core no importaba sin ellos); (6) previews a /home/claude/tiktok/prev/.
- 2026-10-26: VOZ v3 → Piper (davefx narrador, sharvard F preguntas) en vez de Kokoro em_alex 1.28 (sonaba acelerada y con acento raro). Síntesis por cláusulas con pausas por puntuación. Modelos desde GitHub releases de k2-fsa/sherpa-onnx (HF está bloqueado).
- 2026-10-25: motor v2 (core.py): voz Kokoro multi-voz, subtítulos con keywords, planetas con texturas reales (spheres.py), iconos hc.py.
