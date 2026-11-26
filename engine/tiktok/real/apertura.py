"""v37 (26/11): ILUSIÓN DE APERTURA / POSTE DE BARBERÍA por código, reutilizable.
Rayas diagonales que se mueven SIEMPRE en horizontal (vx px/s) vistas a través de una ventana rectangular (w×h) que se puede animar.
Ventana alta y estrecha → se ven subir/bajar; ancha y baja → van de lado; sin ventana → se ve el movimiento real.
Wallach (1935), 'Über visuell wahrgenommene Bewegungsrichtung', Psychologische Forschung 20: 325–380; Guilford (1929) lo notó antes en un
poste de barbería (Wikipedia 'Barberpole illusion': 'A vertically elongated aperture makes vertical motion dominant whereas a horizontally
elongated aperture makes horizontal motion dominant').
`slit_dir(slope, vx)` calcula hacia dónde se desplaza el cruce de una raya con una línea vertical (lo que se ve en una ranura alta)."""
import math
import skia


def stripes(c, cx, cy, win_w, win_h, t, vx=140.0, period=110.0, slope=-1.0, cols=(0xFFE8343F, 0xFFF4F2EC, 0xFF2A5BD8), frame=0xFF1A1A1A, fw=14, marker=None):
    """Dibuja la ventana centrada en (cx,cy). slope = dy/dx de las rayas en pantalla (y hacia abajo): -1 = '/' , +1 = '\\'.
    Las rayas se desplazan vx px/s en horizontal. marker=(k, color): punto pintado sobre la raya k que viaja con ella (prueba del movimiento real)."""
    r = skia.Rect.MakeXYWH(cx - win_w / 2, cy - win_h / 2, win_w, win_h)
    c.save(); c.clipRect(r, skia.ClipOp.kIntersect, True)
    off = (vx * t) % (period * len(cols))
    # una raya = banda entre dos rectas y = slope*(x - x0) + cy ; en el eje x, separación 'period'
    span = win_w + win_h * 2 + period * 6
    n0 = int(-span / period) - len(cols)
    for i in range(n0, int(span / period) + len(cols)):
        x0 = cx + i * period + off
        col = cols[i % len(cols)]
        p = skia.Path()
        H = win_h / 2 + 40
        # recta a la altura y: x = x0 + (y-cy)/slope
        xa = x0 + (-H) / slope; xb = x0 + H / slope
        p.moveTo(xa, cy - H); p.lineTo(xa + period, cy - H); p.lineTo(xb + period, cy + H); p.lineTo(xb, cy + H); p.close()
        c.drawPath(p, skia.Paint(Color=col, AntiAlias=True))
    if marker is not None:
        k, mc = marker
        x0 = cx + k * period + vx * t + period / 2
        c.drawCircle(x0, cy, 26, skia.Paint(Color=mc, AntiAlias=True))
        c.drawCircle(x0, cy, 26, skia.Paint(Color=0xFF101010, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6))
    c.restore()
    c.drawRect(r, skia.Paint(Color=frame, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=fw))


def slit_dir(slope, vx):
    """En una ranura vertical (x fijo) el borde de la raya está en y = cy + slope*(x - x0(t)), x0(t) = x00 + vx t →
    dy/dt = -slope*vx (pantalla, y hacia abajo). Devuelve 'ARRIBA' si dy/dt < 0."""
    dy = -slope * vx
    return "ARRIBA" if dy < 0 else "ABAJO"
