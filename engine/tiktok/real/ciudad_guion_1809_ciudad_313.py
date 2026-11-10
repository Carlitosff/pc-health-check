# 10/11 11:30: IGEV01 09/11 = 313 (+30 desde 283). HITO: se pasa de la ventana 300 → la noria llega a 50/50, se enciende y ARRANCA a girar (v21: arranque con inercia
# en el momento exacto de la pieza 50, destello y cabinas encendidas). Cumple lo prometido el 09/11 ('mañana el foco busca tu ventana'): el foco recorre UNA A UNA
# las 30 ventanas nuevas (SPOT sweep). 1.000 sigue como meta sin plazo. Sin sorteo.
CLOCK = dict(falta=687, secs=None)
NORIA = dict(at=[-6, 5.5], seg="s3", fill=.42)
SPOT = dict(sweep=True, dz=9)
EXTRA = dict(badge="LA CIUDAD DE LA COMUNIDAD", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="Hoy esta ciudad pasó de las trescientas ventanas, y por fin pasa lo que os prometí con la noria.", cap="Pasamos las *300*… | y la *NORIA*…", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Ayer teníamos doscientas ochenta y tres ventanas, y hoy somos trescientas trece, treinta personas nuevas.", cap="De *283*… | a *313*: | *+30*", hold=.5),
 dict(id="s2", who="nar", cut=True, say="Como os dije ayer, el foco busca vuestras ventanas, una a una, hasta llegar a la última.", cap="El foco busca | *TU VENTANA*, | una a una", hold=.6),
 dict(id="s3", who="nar", cut=True, say="Y con la pieza número cincuenta, la noria está completa, se enciende entera y empieza a girar.", cap="Pieza *50 de 50*: | la noria | *GIRA*", hold=1.4),
 dict(id="cta", who="nar", cut=True, say="Ahora vamos a por las mil. Sígueme hoy, y mañana tu ventana también se enciende.", cap="Ahora, a por | las *1.000*. | La próxima, *LA TUYA*"),
]
