# 04/11 11:30: reto en curso (1.000 antes del 05/11 02:00). Novedad visible: panel LED con cuenta atrás + fuegos del hito 200 + ventana 200 dorada.
FRESH = [dict(idx=199, color="#ffc23a", nota="ventana 200, 04/11")]
CLOCK = dict(falta=795, secs=14.5 * 3600)
HITO = 200
EXTRA = dict(badge="RETO · QUEDAN 14 H", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="Quedan catorce horas y media, y faltan setecientos noventa y cinco.", cap="Quedan *14 H* y faltan *795*", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Cada ventana es una persona que me sigue. Salimos con ciento noventa y una. Ya somos doscientas cinco.", cap="Salimos con *191*… | ya somos *205*", hold=1.0),
 dict(id="s2", who="nar", cut=True, say="Hemos pasado de doscientas. Esa ventana de oro es la número doscientos, y la ciudad lo celebra.", cap="Pasamos las *200*: | la ventana de *ORO*", hold=1.6),
 dict(id="s3", who="nar", cut=True, say="Te digo la verdad: a este ritmo, no llegamos. Hace falta que esto corra de verdad, antes de las dos de la madrugada.", cap="La verdad: | a este ritmo, *NO LLEGAMOS*. | Hasta las *02:00*", hold=.3),
 dict(id="cta", who="nar", cut=True, say="Sígueme, y mándaselo a un amigo. A ver hasta dónde encendemos la ciudad.", cap="*Sígueme* y mándaselo | a un *amigo*"),
]
