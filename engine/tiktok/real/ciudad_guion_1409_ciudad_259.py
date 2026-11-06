# 06/11 11:30: IGEV01 05/11 = 259 (+9). Novedad visible: LA NORIA: cada seguidor desde la 250 pone 1 pieza de 50; en la ventana 300 se enciende y gira. 1.000 sigue como meta sin plazo.
CLOCK = dict(falta=741, secs=None)
NORIA = dict(at=[-6, 5.5])
EXTRA = dict(badge="LA CIUDAD DE LA COMUNIDAD", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="Ayer se encendieron nueve ventanas, y con ellas empieza a levantarse algo nuevo en la ciudad.", cap="*9 ventanas* más… y algo *NUEVO* se levanta", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Ya somos doscientas cincuenta y nueve ventanas encendidas, y la meta sigue siendo llegar a mil.", cap="De *250*… | a *259*", hold=.8),
 dict(id="s2", who="nar", cut=True, say="Y desde ahora, cada seguidor pone también una pieza de la noria de la ciudad.", cap="Cada seguidor pone | una pieza de | la *NORIA*", hold=1.0),
 dict(id="s3", who="nar", cut=True, say="Lleva nueve piezas de cincuenta. Cuando encendamos la ventana trescientas, la noria se enciende y empieza a girar.", cap="*9 de 50* piezas. | En la ventana *300*, | la noria *GIRA*", hold=.3),
 dict(id="cta", who="nar", cut=True, say="Para la trescientos faltan cuarenta y una piezas. Sígueme, envíaselo a un amigo, y la siguiente la pones tú.", cap="Faltan *41*: | la siguiente pieza | la pones *TÚ*"),
]
