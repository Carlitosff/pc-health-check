# 17/11 11:30: IGEV01 16/11 = 329 (+5 desde 324, el último N publicado; 14/11 314, 15/11 324). Dato real de Metricool.
# Cumple lo prometido el 16/11 ('sígueme hoy y mañana tu ventana también se enciende'): el foco recorre y enciende una a una las 5 ventanas nuevas.
# Novedad (v28): PRIMERA NEVADA sobre la ciudad (copos + suelo que se cubre de blanco). Gancho en pregunta con 'tú' (el 16/11 la ciudad dio 47,5 % de view rate).
# 1.000 sigue como meta sin plazo. Sin sorteo.
CLOCK = dict(falta=671, secs=None)
NORIA = dict(at=[-6, 5.5], seg="s3", fill=.42)
SPOT = dict(sweep=True)
SNOW = dict(seg="s3", ground=True)
FRESH = []
EXTRA = dict(badge="LA CIUDAD DE LA COMUNIDAD", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="¿Una de estas cinco ventanas nuevas es la tuya? Hoy el foco las busca una a una.", cap="¿Una de estas *5* ventanas es *LA TUYA*?", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Ayer éramos trescientas veinticuatro ventanas, y hoy ya somos trescientas veintinueve.", cap="De *324* | a *329*", hold=.5),
 dict(id="s2", who="nar", cut=True, say="Os lo prometí: vuestra ventana también se enciende, y el foco las va encendiendo una a una.", cap="El foco enciende | *LAS 5*", hold=.4),
 dict(id="s3", who="nar", cut=True, say="Y esta noche, por primera vez, empieza a nevar sobre la ciudad de la comunidad.", cap="Primera *NEVADA* | en la ciudad", hold=1.8),
 dict(id="cta", who="nar", cut=True, say="Faltan seiscientas setenta y una para las mil. Sígueme hoy, y en la próxima tu ventana se enciende bajo la nieve.", cap="Faltan *671*. | La próxima, *LA TUYA*"),
]
