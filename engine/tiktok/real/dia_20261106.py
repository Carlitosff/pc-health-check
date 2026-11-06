"""Producción 06/11/2026 (1401–1402, motor actual; 1403 mito_gorro.py y 1404 serie_salto.py en 3D, 1409 ciudad3d).
  1401 PRUEBA CON TU CUERPO: ilusión del dedo dormido (numbness illusion): Dieguez, Mercier, Newby, Blanke, 'Feeling numbness for someone else's finger', 2009 (EPFL, Current Biology); procedimiento y explicación: Gustavus Psychological Science blog, 02/05/2022.
  1402 RETO: ¿qué vaso se llena primero? Agua simulada por el grafo de tubos (assert: se llena el 6; el 3 y el 4 quedan secos)."""
import math, sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/tiktok/real")
import core as K, hc
from core import W, H, WHITE, INK, clamp, lerp, ease_out, with_alpha, fill, stroke, draw_text
OUT = "/home/claude/tiktok/outdaily"
GOLD = 0xFFFFC23A; RED = 0xFFFF2D3F; CYAN = 0xFF4DE3FF; GREEN = 0xFF4ADE80; BLUE = 0xFF8FB8FF


def seg(P, t):
    sg = K.seg_at(P, t)
    return sg["id"], t - sg["a"], sg["b"] - sg["a"]


# ============================ 1401 dedo dormido
SK1 = (0xFFF0C09A, 0xFFC98A62, 0xFFA8693F)   # tu mano
SK2 = (0xFFB98058, 0xFF8E5A3A, 0xFF6C4026)   # la del amigo
NUMB = (0xFFBFC8DC, 0xFF8D97B4, 0xFF6C7596)


def mix(a, b, k):
    return tuple(
        (0xFF << 24) | sum(int(lerp((x >> s) & 255, (y >> s) & 255, k)) << s for s in (16, 8, 0))
        for x, y in zip(a, b))


def finger(c, bx, by, L, w, ang, skin, nail_side=-1):
    """dedo vertical desde (bx,by) hacia arriba, girado ang grados."""
    c.save(); c.translate(bx, by); c.rotate(ang)
    r = skia.Rect.MakeXYWH(-w / 2, -L, w, L + 40)
    shd = skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(-w / 2, 0), skia.Point(w / 2, 0)], [skin[2], skin[0], skin[0], skin[1]], [0, .32, .62, 1]), AntiAlias=True)
    rr = skia.RRect.MakeRectXY(r, w / 2, w / 2)
    c.drawRRect(rr, shd); c.drawRRect(rr, stroke(with_alpha(0xFF2A1408, .35), 3))
    # pliegues
    for f in (.34, .62):
        y = -L * f
        for dy in (-7, 5):
            c.drawLine(-w * .32, y + dy, w * .32, y + dy, stroke(with_alpha(skin[2], .55), 3))
    # uña en el lado exterior
    nx = nail_side * w * .30
    n = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(nx - w * .17, -L + 12, w * .34, L * .17), 14, 14)
    c.drawRRect(n, fill(with_alpha(0xFFFFE9E0, .85))); c.drawRRect(n, stroke(with_alpha(skin[2], .6), 2))
    c.restore()


def hand(c, x, y, dirx, gap_k, skin, numb=0.0):
    """mano de perfil: dirx=-1 izquierda (TÚ), 1 derecha (AMIGO). gap_k: 0 palmas pegadas, 1 solo los índices."""
    gap = 8 + 92 * gap_k
    px = x + dirx * (gap + 88)
    # muñeca y antebrazo hacia el borde
    arm = skia.Path(); arm.moveTo(px - 62, y + 170); arm.lineTo(px + 62, y + 170); arm.lineTo(px + 110 * dirx + 92, H + 20); arm.lineTo(px + 110 * dirx - 92, H + 20); arm.close()
    c.drawPath(arm, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(px - 90, 0), skia.Point(px + 90, 0)], [skin[2], skin[0], skin[1]]), AntiAlias=True))
    # dedos de atrás
    for k, (L, dx) in enumerate(((300, 44), (332, 22), (268, 66))):
        finger(c, px + dirx * dx, y - 52, L, 66, dirx * 5 * gap_k, skin, nail_side=dirx)
    # palma
    pr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(px - 92, y - 120, 184, 300), 62, 62)
    c.drawRRect(pr, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(px - 92, 0), skia.Point(px + 92, 0)], [skin[2], skin[0], skin[1]]), AntiAlias=True))
    # índice: inclinado para seguir tocando al otro en la línea central
    bx = px - dirx * 58; by = y - 70
    tipx = x + dirx * 34
    L = 360
    ang = math.degrees(math.atan2(tipx - bx, L))
    sk = mix(skin, NUMB, numb)
    finger(c, bx, by, L, 74, ang, sk, nail_side=dirx)
    return bx, by, ang


def pinch(c, x, y, skin, pulse, lt):
    """tu otra mano: pulgar por la izquierda, índice por la derecha, sobre los dos dedos."""
    # sombra
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 120, y + 60, 240, 150), 66, 66), fill(with_alpha(0xFF000000, .28)))
    # brazo desde abajo
    arm = skia.Path(); arm.moveTo(x - 78, y + 140); arm.lineTo(x + 78, y + 140); arm.lineTo(x + 120, H + 20); arm.lineTo(x - 120, H + 20); arm.close()
    c.drawPath(arm, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(x - 120, 0), skia.Point(x + 120, 0)], [skin[2], skin[0], skin[1]]), AntiAlias=True))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 112, y + 46, 224, 170), 74, 74), skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(x - 112, 0), skia.Point(x + 112, 0)], [skin[2], skin[0], skin[1]]), AntiAlias=True))
    finger(c, x - 96, y + 110, 166, 66, 8, skin, nail_side=-1)   # pulgar
    finger(c, x + 96, y + 110, 190, 62, -8, skin, nail_side=1)  # índice
    for sx in (-1, 1):
        r = 44 + 34 * pulse
        c.drawCircle(x + sx * 78, y - 22, r, stroke(with_alpha(GREEN if sx < 0 else CYAN, .75 * (1 - pulse)), 7))


def s_dedo(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.clear(0xFF17121F)
    # fondo: luz cálida que respira + motas
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1120), 900 + 40 * math.sin(t * .9), [0xFF4A2C54, 0xFF241A36, 0xFF120E1C], [0, .55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    rs = np.random.RandomState(9)
    for i in range(46):
        x = (rs.rand() * W + t * (6 + 22 * rs.rand())) % W; y = (rs.rand() * H - t * (14 + 40 * rs.rand())) % H
        c.drawCircle(x, y, 2 + 6 * rs.rand(), fill(with_alpha(0xFFFFD9B0, .05 + .14 * rs.rand())))
    tl = P["tl"]
    CX, CY = W / 2, 1270
    # coreografía de las manos
    if sid == "h":
        gk, rub, numb = 1.0, 1.0, .25 + .55 * K.smooth(lt / d)
    elif sid == "s1":
        gk = K.smooth((lt - 1.8) / 2.2); rub = 0.0; numb = 0.0
    elif sid == "s2":
        gk, rub, numb = 1.0, K.smooth((lt - .6) / .8), 0.0
    elif sid == "s3":
        gk, rub, numb = 1.0, 1.0, K.smooth(lt / 3.0) * .95
    elif sid == "s4":
        gk, rub, numb = 1.0, 1.0 - K.smooth(lt / .5), .95
    else:
        gk, rub, numb = 1.0, 1.0, .95
    z = 1.0 + .02 * math.sin(t * .8)
    c.save(); c.translate(W / 2, 1200); c.scale(z, z); c.translate(-W / 2, -1200)
    if sid == "s1":
        # plano general: las manos enteras enseñan la postura
        spread = 340 * (1 - K.smooth(lt / 1.2))
        c.save(); c.translate(-spread, 0); hand(c, CX, CY, -1, gk, SK1, numb=numb); c.restore()
        c.save(); c.translate(spread, 0); hand(c, CX, CY, 1, gk, SK2); c.restore()
    else:
        # primer plano: solo los dos índices y la pinza de tu otra mano
        if sid == "s4":
            c.saveLayerAlpha(None, int(255 * (1 - .72 * K.smooth(lt / .5))))
        FW_ = 158; FL = 1120; BY = 1900
        finger(c, W / 2 - FW_ / 2 + 2, BY, FL, FW_, 0, mix(SK1, NUMB, numb), nail_side=-1)
        finger(c, W / 2 + FW_ / 2 - 2, BY, FL, FW_, 0, SK2, nail_side=1)
        if rub > 0:
            yy = 1190 + 105 * math.sin(t * 1.25 * math.pi) + (1 - rub) * 900
            # brazo y palma por delante
            arm = skia.Path(); arm.moveTo(W / 2 - 200, yy + 330); arm.lineTo(W / 2 + 200, yy + 330); arm.lineTo(W / 2 + 300, H + 40); arm.lineTo(W / 2 - 300, H + 40); arm.close()
            c.drawPath(arm, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(W / 2 - 300, 0), skia.Point(W / 2 + 300, 0)], [SK1[2], SK1[0], SK1[1]]), AntiAlias=True))
            pal = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - 300, yy + 110, 600, 300), 120, 120)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(W / 2 - 300, yy + 96, 600, 40), 20, 20), fill(with_alpha(0xFF000000, .3)))
            c.drawRRect(pal, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(W / 2 - 300, 0), skia.Point(W / 2 + 300, 0)], [SK1[2], SK1[0], SK1[1]]), AntiAlias=True))
            finger(c, W / 2 - 262, yy + 210, 360, 128, 14, SK1, nail_side=-1)   # pulgar
            finger(c, W / 2 + 262, yy + 210, 370, 118, -14, SK1, nail_side=1)   # índice
            pulse = (t * 1.5) % 1
            for sx, col in ((-1, GREEN), (1, CYAN)):
                c.drawCircle(W / 2 + sx * 165, yy - 95, 48 + 60 * pulse, stroke(with_alpha(col, .8 * (1 - pulse)), 8))
        if sid == "s4":
            c.restore()
    c.restore()
    if sid == "s1":
        K.tag(c, 250, 1570, "TÚ", lt - .6, accent=GOLD, size=52)
        K.tag(c, 830, 1570, "TU AMIGO", lt - .6, accent=CYAN, size=52)
    if sid == "s2":
        K.tag(c, 250, 830, "EL TUYO", lt - .3, accent=GOLD, size=46)
        K.tag(c, 830, 830, "EL SUYO", lt - .3, accent=CYAN, size=46)
    if sid in ("h", "s3") and numb > .3:
        for i in range(3):
            u = (t * .5 + i / 3) % 1
            draw_text(c, "z", 300 - 26 * i + 60 * u, 900 - 150 * u, 54 + 26 * u, with_alpha(0xFFC6D4FF, (1 - u) * numb), shadow=False)
    if sid == "s4":
        # corte visto desde arriba: lo que cada dedo siente
        cy = 1180; k = K.smooth(lt / .6); r = 118 * ease_out(clamp(lt / .5))
        c.drawCircle(W / 2 - r, cy, r, fill(mix(SK1, NUMB, .9)[0])); c.drawCircle(W / 2 + r, cy, r, fill(SK2[0]))
        c.drawCircle(W / 2 - r, cy, r, stroke(WHITE, 5)); c.drawCircle(W / 2 + r, cy, r, stroke(WHITE, 5))
        rr = 48 * k
        c.drawCircle(W / 2 - 2 * r - rr, cy, rr, fill(SK1[0])); c.drawCircle(W / 2 + 2 * r + rr, cy, rr, fill(SK1[0]))
        if lt > .5:
            K.tag(c, W / 2 - r, cy + 190, "TU DEDO", lt - .5, accent=GOLD, size=44)
            K.tag(c, W / 2 + r, cy + 190, "EL SUYO", lt - .5, accent=CYAN, size=44)
        if lt > 1.5:
            p = 40 + 22 * math.sin(t * 7)
            c.drawCircle(W / 2 - 2 * r, cy, p, stroke(GREEN, 9))
            K.tag(c, W / 2, cy + 300, "TU DEDO SOLO SIENTE UN LADO", lt - 1.5, accent=RED, size=50)
    K.vignette(c, .4)


V1401 = dict(slug="1401_dedo_dormido", accent=GOLD, drone=0.015, scene=s_dedo, mood="misterio", send="ENVÍASELO A QUIEN TENGAS AL LADO",
             rehook=("s3", "ESPERA… NO DEJES DE FROTAR"), reveal=("s4", "EL PORQUÉ"), segs=[
    dict(id="h", who="nar", say="Busca a alguien, junta tu dedo con el suyo, y vas a notar el tuyo como dormido.", cap="Junta tu dedo con el de alguien: *SE TE DUERME*", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="Poneos frente a frente, palma con palma, y separad las manos dejando juntos solo los índices.", cap="*Palma con palma*… | y juntos solo | los *ÍNDICES*", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Con tu mano libre, coge los dos dedos con el pulgar y el índice, y frota arriba y abajo.", cap="Con tu otra mano: | *frota los dos dedos* | arriba y abajo", hold=0.5),
    dict(id="s3", who="nar", cut=True, say="Sigue frotando despacio. Lo notarás raro, como si uno de los dedos estuviera anestesiado.", cap="Se nota *RARO*: | como *anestesiado*", hold=0.5),
    dict(id="s4", who="nar", cut=True, say="Tus yemas tocan dos lados, pero tu dedo solo siente uno, porque tu cerebro no cuenta con el dedo de la otra persona.", cap="Tu cerebro *no cuenta* | con el dedo del otro", hold=0.5),
    dict(id="cta", who="nar", cut=True, say="Envíaselo a quien tengas al lado, y comenta si se te ha dormido: sí o no.", cap="¿Se te ha dormido? | Comenta *SÍ* o *NO*"),
])

# ============================ 1402 vasos y tubos
CW_, CH_ = 170, 170
CUP = {1: (540, 780), 2: (250, 1010), 3: (830, 1010), 4: (150, 1340), 5: (540, 1340), 6: (930, 1560)}  # (centro x, borde y)
# tubo: desde vaso, lado, nivel de salida (0 fondo, 1 borde), hasta vaso, x de caída, tapón
PIPES = [(1, -1, .25, 2, 250, False), (1, 1, .70, 3, 830, False),
         (2, -1, .28, 4, 110, True), (2, 1, .65, 5, 490, False),
         (3, -1, .30, 5, 590, False), (3, 1, .70, 6, 930, False),
         (5, 1, .30, 6, 930, False)]


def cup_y(n, f):
    x, r = CUP[n]
    return r + (1 - f) * CH_


def simulate():
    """Vierte en el 1: el agua sube hasta el tubo abierto más bajo; si no hay, se llena. Devuelve eventos (tipo, id, a, b, dur)."""
    ev = []; cur = 1; lvl = {k: 0.0 for k in CUP}; seen = []
    while True:
        seen.append(cur)
        outs = sorted([p for p in PIPES if p[0] == cur], key=lambda p: p[2])
        blocked = [p for p in outs if p[5]]
        openp = [p for p in outs if not p[5]]
        if not openp:
            ev.append(("fill", cur, lvl[cur], 1.0, 2.6)); return ev, cur, seen
        p = openp[0]
        ev.append(("fill", cur, lvl[cur], p[2], .55 + 1.1 * p[2]))
        ev.append(("pipe", PIPES.index(p), 0, 1, .7))
        cur = p[3]


EV, WINNER, ROUTE = simulate()
assert WINNER == 6 and ROUTE == [1, 2, 5, 6]
assert 3 not in ROUTE and 4 not in ROUTE
T_FLOW = sum(e[4] for e in EV)


def flow_state(u):
    lv = {k: 0.0 for k in CUP}; pf = {}; left = u
    for e in EV:
        k = clamp(left / e[4])
        if e[0] == "fill":
            lv[e[1]] = lerp(e[2], e[3], k)
        else:
            pf[e[1]] = k
        left -= e[4]
        if left <= 0:
            break
    return lv, pf


def pipe_path(p):
    a, sd, f, b, xd, _ = p
    x, r = CUP[a]; y = cup_y(a, f)
    x0 = x + sd * CW_ / 2; rb = CUP[b][1]
    return [(x0, y), (xd, y), (xd, rb - 4)]


def poly_len(pts):
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))


def draw_poly(c, pts, paint, f=1.0):
    L = poly_len(pts) * f; path = skia.Path(); path.moveTo(*pts[0])
    for i in range(len(pts) - 1):
        d = math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        if L >= d:
            path.lineTo(*pts[i + 1]); L -= d
        else:
            k = L / max(d, 1); path.lineTo(lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)); break
    c.drawPath(path, paint)


def s_vasos(c, t, P, V):
    sid, lt, d = seg(P, t)
    c.clear(0xFF0B1A2B)
    g = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, 1200), 1000, [0xFF16405C, 0xFF0D2338, 0xFF081422], [0, .6, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    rs = np.random.RandomState(4)
    for i in range(40):
        x = (rs.rand() * W + math.sin(t * .6 + i) * 18) % W; y = (rs.rand() * H - t * (22 + 50 * rs.rand())) % H; r_ = 3 + 8 * rs.rand()
        c.drawCircle(x, y, r_, stroke(with_alpha(0xFFBFE9FF, .08 + .14 * rs.rand()), 2))
    tl = P["tl"]
    a3 = tl["s3"][0]; aC = tl["cta"][0]
    u = 0.0
    if t >= a3:
        span = max(.1, aC - a3 - .15)
        u = clamp((t - a3) / span) * T_FLOW
    lv, pf = flow_state(u)
    # tubos
    for i, p in enumerate(PIPES):
        pts = pipe_path(p)
        pw = stroke(0xFF55657E, 30); pw.setStrokeCap(skia.Paint.kRound_Cap); pw.setStrokeJoin(skia.Paint.kRound_Join)
        draw_poly(c, pts, pw)
        pw2 = stroke(0xFF94A7C2, 20); pw2.setStrokeJoin(skia.Paint.kRound_Join); draw_poly(c, pts, pw2)
        pw3 = stroke(0xFF1B2636, 12); pw3.setStrokeJoin(skia.Paint.kRound_Join); draw_poly(c, pts, pw3)
        if i in pf and pf[i] > 0:
            w = stroke(CYAN, 12); w.setStrokeJoin(skia.Paint.kRound_Join); draw_poly(c, pts, w, pf[i])
            # el caudal sigue cayendo una vez lleno el tramo
            if pf[i] >= 1:
                L = poly_len(pts); ph = (t * 2.4) % 1
                x, y = pts[-1]; c.drawCircle(x, y - (1 - ph) * 60, 7, fill(WHITE))
        if p[5]:
            # tapón rojo
            x0, y0 = pts[0]; xm = (x0 + pts[1][0]) / 2 - 8
            pul = 1 + .08 * math.sin(t * 5)
            r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(xm - 15, y0 - 24 * pul, 30, 48 * pul), 8, 8)
            c.drawRRect(r, fill(RED)); c.drawRRect(r, stroke(WHITE, 4))
    # vasos
    for n, (x, r) in CUP.items():
        l = x - CW_ / 2; b = r + CH_
        rect = skia.Rect.MakeLTRB(l, r, l + CW_, b)
        c.drawRRect(skia.RRect.MakeRectXY(rect, 14, 14), fill(with_alpha(0xFFD8F2FF, .10)))
        f = lv[n]
        if f > 0:
            ytop = b - f * CH_
            wave = skia.Path(); wave.moveTo(l + 5, b - 5); wave.lineTo(l + 5, ytop)
            for k in range(11):
                xx = l + 5 + (CW_ - 10) * k / 10
                wave.lineTo(xx, ytop + 3.5 * math.sin(k * .9 + t * 9))
            wave.lineTo(l + CW_ - 5, b - 5); wave.close()
            c.drawPath(wave, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, ytop), skia.Point(0, b)], [0xFF7BEBFF, 0xFF1787D8]), AntiAlias=True))
        c.drawRRect(skia.RRect.MakeRectXY(rect, 14, 14), stroke(with_alpha(WHITE, .85), 6))
        c.drawRect(skia.Rect.MakeXYWH(l + 20, r + 16, 12, CH_ - 40), fill(with_alpha(WHITE, .18)))
        # número
        win = sid == "cta" and n == WINNER
        rad = 42 * (1 + (.14 * math.sin(t * 7) if win else 0))
        c.drawCircle(x, r + CH_ / 2 + 4, rad, fill(GOLD if win else 0xFF10131F))
        c.drawCircle(x, r + CH_ / 2 + 4, rad, stroke(WHITE, 5))
        draw_text(c, str(n), x, r + CH_ / 2 + 26, 62, 0xFF10131F if win else WHITE, shadow=False)
    # grifo
    tx, ty = CUP[1][0], CUP[1][1]
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(tx - 100, ty - 92, 120, 36), 12, 12), fill(0xFFA9B6C8))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(tx - 16, ty - 92, 36, 68), 10, 10), fill(0xFF8797AE))
    wh = t * 2 if u > 0 else 0
    c.save(); c.translate(tx + 2, ty - 104); c.rotate(math.degrees(wh)); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-40, -9, 80, 18), 8, 8), fill(RED)); c.restore()
    if u > 0:
        c.drawRect(skia.Rect.MakeXYWH(tx - 7, ty - 26, 14, CH_ + 20 - (lv[1] * CH_)), fill(with_alpha(CYAN, .9)))
    else:
        ph = (t * .9) % 1; c.drawCircle(tx + 2, ty - 18 + ph * 80, 8, fill(with_alpha(CYAN, 1 - ph * .6)))
    if sid == "s1" and lt > 1:
        x0, y0 = pipe_path(PIPES[2])[0]
        K.tag(c, 190, 1275, "TAPÓN: NO PASA", lt - 1, accent=RED, size=40)
    if sid == "cta":
        s = ease_out(clamp(lt / .35))
        c.save(); c.translate(W / 2, 1000); c.rotate(-4); c.scale(s, s)
        r_ = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-340, -76, 680, 142), 18, 18); c.drawRRect(r_, fill(GOLD)); c.drawRRect(r_, stroke(WHITE, 8))
        draw_text(c, "EL VASO 6", 0, 32, 96, 0xFF10131F, shadow=False); c.restore()
    K.vignette(c, .35)


V1402 = dict(slug="1402_que_vaso_se_llena", accent=CYAN, drone=0.02, scene=s_vasos, mood="epico", send="RETA A UN AMIGO: ¿QUÉ VASO?",
             rehook=("s3", "HAY DOS TRAMPAS"), reveal=("s4", "LA SOLUCIÓN"), segs=[
    dict(id="h", who="nar", say="Abro el grifo. ¿Qué vaso se llena primero? Di el número.", cap="¿Qué vaso se llena *PRIMERO*?", hold=0.2),
    dict(id="s1", who="nar", cut=True, say="El agua sale siempre por el tubo más bajo que esté abierto, y por el tapón rojo no pasa.", cap="Sale por el tubo *más bajo*. | Por el *tapón* no pasa", hold=0.3),
    dict(id="s2", who="nar", cut=True, say="Tienes cinco segundos, mira bien todos los tubos.", cap="*5 segundos*: | ¿qué vaso?", hold=4.0),
    dict(id="s3", who="nar", cut=True, say="El uno se vacía por la izquierda hacia el dos. Y el dos parece que baja al cuatro, pero ahí está el tapón.", cap="El *2* parece que baja | al *4*… | ¡pero hay *TAPÓN*!", hold=0.3),
    dict(id="s4", who="nar", cut=True, say="Así que sube hasta el otro tubo y cae en el cinco, y el cinco se vacía entero en el seis.", cap="Cae en el *5*… | y el *5* se vacía | en el *6*", hold=0.6),
    dict(id="cta", who="nar", cut=True, say="Se llena el seis. ¿Cuál habías dicho tú? Comenta tu número, y reta a un amigo.", cap="¿Cuál dijiste? | Comenta tu *NÚMERO*"),
])
VIDEOS = [V1401, V1402]


def make_scene(V):
    def scene(c, t, P):
        V["scene"](c, t, P, V)
    return scene


if __name__ == "__main__":
    arg = sys.argv[1]
    idxs = range(len(VIDEOS)) if arg == "all" else [int(x) for x in arg.split(",")]
    pv = "auto" if len(sys.argv) > 2 else None
    for i in idxs:
        K.run(VIDEOS[i], make_scene(VIDEOS[i]), OUT, preview=pv)
