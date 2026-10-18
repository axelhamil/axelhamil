import math
import random

W, H = 1200, 480


def n(v):
    s = f"{v:.1f}"
    if s.endswith(".0"):
        s = s[:-2]
    return "0" if s == "-0" else s


def pts(points):
    return " ".join(f"{n(x)} {n(y)}" for x, y in points)


def poly(points):
    return f"M{pts(points[:1])}L{pts(points[1:])}Z"


def closed(points, bottom=H):
    return poly([(points[0][0], bottom)] + list(points) + [(points[-1][0], bottom)])


def smooth(points):
    d = f"M{n(points[0][0])} {n(points[0][1])}"
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{n(c1[0])} {n(c1[1])} {n(c2[0])} {n(c2[1])} {n(p2[0])} {n(p2[1])}"
    return d


def smooth_closed(points, bottom=H):
    return smooth(points) + f"L{n(points[-1][0])} {bottom}L{n(points[0][0])} {bottom}Z"


def noise(seed, octaves, f0=0.004, f1=0.012):
    rnd = random.Random(seed)
    waves = [(rnd.uniform(f0, f1) * 2 ** i, rnd.uniform(0, 6.28), 0.55 ** i) for i in range(octaves)]
    return lambda x: sum(a * math.sin(f * x + p) for f, p, a in waves)


def hills(x0, x1, base, amp, seed, step=30, octaves=3, shape=None):
    f = noise(seed, octaves)
    out = []
    for x in range(x0, x1 + step, step):
        y = base - amp * (f(x) + 1.2)
        out.append((x, y + (shape(x) if shape else 0)))
    return out


def at(points, x):
    for (xa, ya), (xb, yb) in zip(points, points[1:]):
        if xa <= x <= xb:
            return ya + (yb - ya) * (x - xa) / (xb - xa)
    return points[-1][1] if x > points[-1][0] else points[0][1]


def smoothstep(a, b, x):
    k = min(1.0, max(0.0, (x - a) / (b - a)))
    return k * k * (3 - 2 * k)
