# 18/11 11:30: IGEV01 17/11 = 332 (+3 desde 329, el último N publicado; 15/11 324, 16/11 329). Dato real de Metricool.
# Cumple lo prometido el 17/11 ('en la próxima tu ventana se enciende bajo la nieve'): nieva desde el primer plano y el foco enciende las 3 nuevas una a una.
# Novedad (v29): PRIMER MUÑECO DE NIEVE de la ciudad, que se monta bola a bola y levanta un cartel con el 332. +3 se dice tal cual (no es hito).
# 1.000 sigue como meta sin plazo. Sin sorteo.
CLOCK = dict(falta=668, secs=None)
NORIA = dict(at=[-6, 5.5], seg="s3", fill=.42)
SPOT = dict(sweep=True, nodim=True, shot=[6, 10, 24])
SNOW = dict(seg="h", ground=True)
SNOWMAN = dict(seg="s3", at=[-3.3, 10], s=1, sign="332", shot=[0.6, 2.4, 10, 3.2])
FRESH = []
EXTRA = dict(badge="LA CIUDAD DE LA COMUNIDAD", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="¿Eres tú una de las tres ventanas que se encienden hoy bajo la nieve?", cap="¿Eres tú una de las *3* ventanas de *HOY*?", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Ayer éramos trescientas veintinueve ventanas, y hoy ya somos trescientas treinta y dos.", cap="De *329* | a *332*", hold=.5),
 dict(id="s2", who="nar", cut=True, say="Lo prometido: vuestras tres ventanas se encienden una a una, mientras sigue nevando.", cap="Las *3* nuevas, | bajo la *NIEVE*", hold=.4),
 dict(id="s3", who="nar", cut=True, say="Y con tanta nieve, la ciudad ha hecho su primer muñeco, que sujeta nuestro número.", cap="Nuestro primer | *MUÑECO DE NIEVE*", hold=1.8),
 dict(id="cta", who="nar", cut=True, say="Faltan seiscientas sesenta y ocho para las mil. Comenta qué nombre le pondrías al muñeco, y sígueme: la próxima ventana puede ser la tuya.", cap="¿Cómo lo *LLAMARÍAS*? | La próxima ventana, *LA TUYA*"),
]
