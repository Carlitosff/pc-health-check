"""Retos de palillos (motor v25, 14/11): dígitos de 7 segmentos y búsqueda exhaustiva de soluciones moviendo UN palillo.
Uso: from palillos import solutions, candidates
  solutions(7, '+', 6, 1) -> {(1,'+',6,7, i_origen, seg_origen, j_destino, seg_destino)}  (0=1er número, 1=signo, 2=2º número, 3=resultado)
  candidates() -> lista de (a, op, b, c, solución) con solución ÚNICA, para elegir el reto del día sin repetir (ver used_topics.md).
Usados: 5+7=2 (13/11, → 9−7=2), 7+6=1 (14/11, → 1+6=7)."""
SEG7 = {0: 'abcdef', 1: 'bc', 2: 'abged', 3: 'abgcd', 4: 'fgbc', 5: 'afgcd', 6: 'afgedc', 7: 'abc', 8: 'abcdefg', 9: 'abcdfg'}
INV = {frozenset(v): k for k, v in SEG7.items()}
USED = {(5, '+', 7, 2), (7, '+', 6, 1)}


def solutions(a, op, b, c_):
    st = [set(SEG7[a]), {'h', 'v'} if op == '+' else {'h'}, set(SEG7[b]), set(SEG7[c_])]
    slots = ['abcdefg', 'hv', 'abcdefg', 'abcdefg']; out = set()
    for i in range(4):
        for s_ in list(st[i]):
            for j in range(4):
                for t_ in slots[j]:
                    n = [set(x) for x in st]; n[i].discard(s_)
                    if t_ in n[j] or (i == j and t_ == s_):
                        continue
                    n[j].add(t_)
                    A, B, C = INV.get(frozenset(n[0])), INV.get(frozenset(n[2])), INV.get(frozenset(n[3]))
                    O = '+' if n[1] == {'h', 'v'} else '-' if n[1] == {'h'} else None
                    if None not in (A, B, C, O) and (A + B if O == '+' else A - B) == C:
                        out.add((A, O, B, C, i, s_, j, t_))
    return out


def candidates(cross=True):
    """Ecuaciones falsas con UNA sola solución. cross=True: solo las que mueven el palillo entre dos números distintos (más difíciles)."""
    res = []
    for a in range(10):
        for b in range(10):
            for c in range(10):
                for op in '+-':
                    if (a + b if op == '+' else a - b) == c or (a, op, b, c) in USED:
                        continue
                    S = solutions(a, op, b, c)
                    if len(S) == 1:
                        s = next(iter(S))
                        if not cross or (s[4] != s[6] and 1 not in (s[4], s[6])):
                            res.append((a, op, b, c, s))
    return res


if __name__ == "__main__":
    cs = candidates()
    print(len(cs), "retos con solución única entre dos números:")
    for x in cs[:40]:
        print(x)
