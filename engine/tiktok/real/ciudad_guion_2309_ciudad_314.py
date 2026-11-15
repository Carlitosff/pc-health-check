# 15/11 11:30: IGEV01 14/11 = 314 (+1 desde 313; 11–13/11 sin crecer: 311, 313, 313). Se dice tal cual: +1, sin celebrarlo como hito.
# Cumple lo prometido el 10/11 ('sígueme hoy y mañana tu ventana también se enciende'): el foco busca la ventana 314 y se enciende.
# Novedad (v26): 314 = cifras de π (3,14) → la ventana 314 se queda ROSA para siempre (ciudad_state.json) y lleva un CARTEL DE NEÓN 'π 3,14'.
# 1.000 sigue como meta sin plazo. Sin sorteo.
CLOCK = dict(falta=686, secs=None)
NORIA = dict(at=[-6, 5.5], seg="s3", fill=.42)
SPOT = True
SIGN = dict(lines=["π", "3,14"], seg="s3", col="#ff3fb0")
FRESH = [dict(idx=313, color="#ff3fb0", nota="ventana 314 = π (3,14), 15/11")]
EXTRA = dict(badge="LA CIUDAD DE LA COMUNIDAD", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="Cuatro días sin ventanas nuevas en esta ciudad, y hoy por fin se enciende una.", cap="4 días a oscuras… | y hoy *SE ENCIENDE*", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Ayer éramos trescientas trece ventanas, y hoy trescientas catorce. Solo una persona más, pero cuenta.", cap="De *313* | a *314*: | *+1*", hold=.5),
 dict(id="s2", who="nar", cut=True, say="Como os prometí, el foco busca la ventana nueva por toda la ciudad, hasta que la encuentra.", cap="El foco busca | *TU VENTANA*", hold=.6),
 dict(id="s3", who="nar", cut=True, say="Y como trescientos catorce son las cifras del número pi, esta ventana se queda rosa, con su propio cartel.", cap="*3,14*… | como el número *π*", hold=1.2),
 dict(id="cta", who="nar", cut=True, say="Faltan seiscientas ochenta y seis para las mil. Sígueme, y la próxima ventana que se enciende es la tuya.", cap="Faltan *686*. | La próxima, *LA TUYA*"),
]
