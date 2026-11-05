# 05/11 11:30: el reto de 1.000 en 24 h terminó sin llegar (05/11 02:00). Último IGEV01 = 250 (04/11). Sin prórroga: 1.000 queda como meta sin plazo.
# Novedad visible: rascacielos terminado (torre de 2×19 que cierra en la ventana 250, corona y antena), fuegos del hito, grúa en el edificio siguiente, panel sin reloj.
FRESH = [dict(idx=249, color="#ffc23a", nota="ventana 250, remate del primer rascacielos, 05/11")]
CLOCK = dict(falta=750, secs=None)
HITO = 250
EXTRA = dict(badge="EL RETO HA TERMINADO", send="ENVÍASELO A UN AMIGO")
SEGS = [
 dict(id="h", who="nar", say="Se acabó el reto de los mil seguidores en veinticuatro horas. Y no llegamos.", cap="Reto de *1.000* en 24 h: *NO LLEGAMOS*", hold=.1),
 dict(id="s1", who="nar", cut=True, say="Empezamos con ciento noventa y una ventanas, y el último dato que tengo es de doscientas cincuenta.", cap="De *191*… | a *250*", hold=1.0),
 dict(id="s2", who="nar", cut=True, say="Pero esa ventana de oro, la número doscientos cincuenta, termina el primer rascacielos de la ciudad.", cap="La ventana *250* | termina el primer *RASCACIELOS*", hold=2.0),
 dict(id="s3", who="nar", cut=True, say="Te digo la verdad: faltan setecientas cincuenta. Los mil siguen siendo la meta, pero ya sin reloj.", cap="Faltan *750*. | La meta sigue, | *sin reloj*", hold=.3),
 dict(id="cta", who="nar", cut=True, say="Sígueme, y la siguiente ventana, en el edificio nuevo, es la tuya.", cap="La siguiente | ventana | es la *TUYA*"),
]
