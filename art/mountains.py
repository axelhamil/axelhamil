import random

from geo import H, closed, n, noise, poly, smoothstep


def profile(x0, x1, base, peaks, seed, step=6, rough=2.0, power=1.1, taper=(0, 0)):
    rnd = random.Random(seed)
    jag = noise(seed + 7, 3, 0.03, 0.07)
    top = max(p[1] for p in peaks)
    out = []
    for x in range(x0, x1 + step, step):
        h = max(ph * max(0.0, 1 - abs(x - px) / pw) ** power for px, ph, pw in peaks)
        h += rough * jag(x) * (0.3 + h / top) + rnd.uniform(-0.4, 0.4) * rough
        y = base - max(h, 0.0)
        if taper[0]:
            y += (H - y) * (1 - smoothstep(x0, x0 + taper[0], x))
        if taper[1]:
            y += (H - y) * smoothstep(x1 - taper[1], x1, x)
        out.append((x, y))
    summits = sorted((px, base - ph) for px, ph, _ in peaks)
    out = [p for p in out if all(abs(p[0] - s[0]) > step * 0.5 for s in summits)] + summits
    return sorted(out), summits


def facets(points, summits, base, seed):
    rnd = random.Random(seed)
    wedges, gullies = [], []
    for i, (sx, sy) in enumerate(summits):
        nx = summits[i + 1][0] if i + 1 < len(summits) else points[-1][0]
        seg = [p for p in points if sx < p[0] <= nx]
        if not seg:
            continue
        valley = seg[-1] if i + 1 == len(summits) else max(seg, key=lambda p: p[1])
        ridge = [p for p in seg if p[0] <= valley[0]]
        foot = (sx + (valley[0] - sx) * rnd.uniform(0.25, 0.45), base + 1)
        spine = [(sx + (foot[0] - sx) * k / 5 + rnd.uniform(-1.6, 1.6) * (k > 0), sy + (foot[1] - sy) * k / 5) for k in range(1, 5)]
        wedges.append(poly([(sx, sy)] + ridge + [foot] + spine[::-1]))
        height = base - sy
        prev = summits[i - 1][0] if i else points[0][0]
        for _ in range(int(height / 14)):
            gx = rnd.uniform(max(prev, sx - height * 0.9), sx - 3)
            gy = min(p[1] for p in points if abs(p[0] - gx) < 7) + 2
            length = (base - gy) * rnd.uniform(0.3, 0.6)
            gullies.append(f"M{n(gx)} {n(gy)}l{n(length * 0.35)} {n(length)}")
    return "".join(wedges), "".join(gullies)


def snowcaps(points, summits, base, frac, minimum, seed):
    rnd = random.Random(seed)
    caps = []
    for sx, sy in summits:
        height = base - sy
        if height < minimum:
            continue
        depth = height * frac * rnd.uniform(0.85, 1.15)
        line = sy + depth
        span = height * 3.2
        edge = []
        x = sx - span
        while x <= sx + span:
            y = line + rnd.uniform(-0.12, 0.12) * depth
            if rnd.random() < 0.16:
                y += rnd.uniform(0.15, 0.4) * depth
            edge.append((x, y))
            x += rnd.uniform(3.5, 6.0)
        caps.append(poly([(sx - span, sy - 10)] + edge + [(sx + span, sy - 10)]))
    return "".join(caps)


def mountain_range(uid, t, x0, x1, base, peaks, seed, lit, shade, snow=None, frac=0.3, minimum=30, step=6, rough=2.0, gully_opacity=0.45, taper=(0, 0)):
    points, summits = profile(x0, x1, base, peaks, seed, step, rough, taper=taper)
    body = closed(points)
    wedges, gullies = facets(points, summits, base, seed + 1)
    defs = ""
    out = (
        f'<path d="{body}" fill="{lit}"/>'
        f'<path d="{wedges}" fill="{shade}"/>'
        f'<path d="{gullies}" stroke="{shade}" stroke-width=".8" opacity="{gully_opacity}" fill="none"/>'
    )
    if snow:
        caps = snowcaps(points, summits, base, frac, minimum, seed + 2)
        defs += f'<clipPath id="{uid}"><path d="{body}"/></clipPath>'
        defs += f'<clipPath id="{uid}s"><path d="{caps}"/></clipPath>'
        out += (
            f'<g clip-path="url(#{uid})"><path d="{caps}" fill="{snow[0]}"/>'
            f'<path d="{wedges}" fill="{snow[1]}" clip-path="url(#{uid}s)"/></g>'
        )
    return defs, out, points
