# 16/11 11:30: IGEV01 15/11 = 324 (+10 desde 314, el último N publicado; 13/11 313, 14/11 314). Dato real de Metricool.
# Cumple lo prometido el 15/11 ('la próxima ventana que se enciende es la tuya'): el foco recorre y enciende una a una las 10 ventanas nuevas.
# Novedad (v27): ESPECTÁCULO DE DRONES: despegan de las azoteas y dibujan '+10' y luego '324' sobre la ciudad. Las ventanas de colores siguen (state).
# 1.000 sigue como meta sin plazo. Sin sorteo.
CLOCK = dict(falta=676, secs=None)
NORIA = dict(at=[-6, 5.5], seg="s3", fill=.42)
SPOT = dict(sweep=True)
DRONES = dict(seg="s3", lines=["+10", "324"], at=[0, 20, 4], w=16)
FRESH = []
EXTRA = dict(badge="LA CIUDAD DE LA COMUNIDAD", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="Diez ventanas nuevas en un solo día, y esta noche lo celebramos con drones.", cap="*+10* ventanas… | y hoy hay *DRONES*", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Ayer éramos trescientas catorce ventanas, y hoy somos trescientas veinticuatro.", cap="De *314* | a *324*", hold=.5),
 dict(id="s2", who="nar", cut=True, say="Os lo prometí: la próxima ventana era la vuestra, y el foco las va encendiendo una a una.", cap="El foco enciende | *LAS 10*", hold=.4),
 dict(id="s3", who="nar", cut=True, say="Y para celebrarlo, los drones despegan de las azoteas, y dibujan vuestro número en el cielo.", cap="*DRONES* | sobre la ciudad", hold=1.6),
 dict(id="cta", who="nar", cut=True, say="Faltan seiscientas setenta y seis para las mil. Sígueme hoy, y mañana tu ventana también se enciende.", cap="Faltan *676*. | Mañana, *LA TUYA*"),
]
