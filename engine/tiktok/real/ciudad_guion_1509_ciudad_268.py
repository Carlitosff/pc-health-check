# 07/11 11:30: IGEV01 06/11 = 268 (+9). Novedad visible: hoy se cuelgan 2 cabinas nuevas en la noria (la 2ª y la 3ª, en las piezas 12 y 18) con rótulo 18/50 en la base. Gancho con 'tú': una de estas ventanas es tuya. 1.000 sigue como meta sin plazo.
CLOCK = dict(falta=732, secs=None)
NORIA = dict(at=[-6, 5.5])
EXTRA = dict(badge="LA CIUDAD DE LA COMUNIDAD", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="Si me sigues, una de estas ventanas es tuya, y ayer se encendieron otras nueve.", cap="Si me sigues, una de estas ventanas es *TUYA*", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Ya somos doscientas sesenta y ocho ventanas encendidas, y la meta sigue siendo llegar a mil.", cap="De *259*… | a *268* ventanas", hold=.8),
 dict(id="s2", who="nar", cut=True, say="Y con las piezas nuevas, hoy se cuelgan dos cabinas más en la noria.", cap="Hoy se cuelgan | *2 cabinas* más | en la *NORIA*", hold=1.0),
 dict(id="s3", who="nar", cut=True, say="Lleva dieciocho piezas de cincuenta. En la ventana trescientos, se enciende y empieza a girar.", cap="*18 de 50* piezas. | En la *300*, | la noria *GIRA*", hold=.3),
 dict(id="cta", who="nar", cut=True, say="Faltan treinta y dos piezas. Sígueme, y envíaselo a un amigo para que ponga la suya.", cap="Faltan *32*: | que tu amigo | ponga *la suya*"),
]
