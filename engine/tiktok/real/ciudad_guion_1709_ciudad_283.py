# 09/11 11:30: IGEV01 08/11 = 283 (+1 desde 282). Día flojo y se dice tal cual. Novedad visible: FOCO BUSCADOR (ciudad.js v20, J.spot) que barre la
# ciudad y se clava en la ventana 283; noria 33/50 (sin cabina nueva: tocan en 37). 1.000 sigue como meta sin plazo. Sin sorteo.
CLOCK = dict(falta=717, secs=None)
NORIA = dict(at=[-6, 5.5])
SPOT = True
EXTRA = dict(badge="LA CIUDAD DE LA COMUNIDAD", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="Ayer, en esta ciudad, solo se encendió una ventana, y hoy te enseño cuál es.", cap="Ayer solo se encendió *UNA* ventana", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Teníamos doscientas ochenta y dos ventanas, y ahora somos doscientas ochenta y tres.", cap="De *282*… | a *283*", hold=.6),
 dict(id="s2", who="nar", cut=True, say="El foco la busca entre todas, y aquí está, la ventana de la última persona que me siguió.", cap="El foco la busca… | y *aquí está*: | la *283*", hold=1.0),
 dict(id="s3", who="nar", cut=True, say="Con ella, la noria ya tiene treinta y tres piezas, y le faltan diecisiete para encenderse y girar.", cap="Noria: *33 de 50*. | Faltan *17* | para que *GIRE*", hold=.4),
 dict(id="cta", who="nar", cut=True, say="Si me sigues hoy, mañana el foco busca tu ventana. Envíaselo a un amigo para que ponga la suya.", cap="Mañana el foco | busca *LA TUYA*"),
]
