# 08/11 11:30: IGEV01 07/11 = 282 (+14 desde 268). Novedad visible: la noria pasa la MITAD (32/50 piezas), se cuelgan las cabinas 4 y 5 y se encienden por
# primera vez las GUIRNALDAS de bombillas (nuevo en ciudad.js v19). Gancho con 'tú' y una imagen que entiende quien no sigue. 1.000 sigue como meta sin plazo. Sin sorteo.
CLOCK = dict(falta=718, secs=None)
NORIA = dict(at=[-6, 5.5])
EXTRA = dict(badge="LA CIUDAD DE LA COMUNIDAD", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="Cada persona que me sigue pone una pieza en esta noria, y hoy ya pasa de la mitad.", cap="Cada seguidor pone *UNA PIEZA*: hoy pasa la *MITAD*", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Ayer éramos doscientas sesenta y ocho ventanas encendidas, y hoy ya somos doscientas ochenta y dos.", cap="De *268*… | a *282* ventanas", hold=.8),
 dict(id="s2", who="nar", cut=True, say="Son catorce piezas nuevas en la noria, y con ellas se cuelgan dos cabinas más.", cap="*14 piezas* nuevas | y *2 cabinas* más", hold=1.0),
 dict(id="s3", who="nar", cut=True, say="Al pasar la mitad, se encienden las guirnaldas de bombillas. Ahora faltan dieciocho piezas para que gire.", cap="Pasa la *MITAD*: | se encienden | las *guirnaldas*", hold=.5),
 dict(id="cta", who="nar", cut=True, say="En la ventana trescientos, la noria se enciende y gira. Sígueme, y envíaselo a un amigo para que ponga su pieza.", cap="En la *300*, | la noria *GIRA*. | ¿Pones *la tuya*?"),
]
