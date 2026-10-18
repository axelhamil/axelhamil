import random

from geo import at, n, poly

FIRS = [6, 9, 12, 16, 21, 28, 36]
OAKS = [5, 7, 10]


def fir_shape(h):
    w = h * 0.3
    if h < 8:
        return poly([(0, -h), (w, 0), (-w, 0)]), poly([(0, -h), (w, 0), (0, 0)])
    tiers = 3 if h < 15 else 4
    left = [(0, -h)]
    for k in range(1, tiers + 1):
        frac = k / tiers
        ty = -h + h * 0.9 * frac
        left.append((-w * frac, ty))
        if k < tiers:
            left.append((-w * frac * 0.42, ty - h * 0.05))
    trunk = max(0.6, h * 0.035)
    ty = left[-1][1]
    left += [(-trunk, ty), (-trunk, 0.5)]
    right = [(-x, y) for x, y in left[1:]][::-1]
    return poly(left + right), poly([(0, -h)] + [(-x, y) for x, y in left[1:-2]] + [(0, ty)])


def symbols(t):
    out = []
    for h in FIRS:
        body, shade = fir_shape(h)
        out.append(f'<g id="f{h}"><path d="{body}"/><path d="{shade}" fill="#000" opacity="{t["leaf_shade"]}"/></g>')
    for r in OAKS:
        crown = (
            f'<circle cx="0" cy="{n(-r * 1.25)}" r="{r}"/><circle cx="{n(-r * 0.75)}" cy="{n(-r * 0.85)}" r="{n(r * 0.7)}"/>'
            f'<circle cx="{n(r * 0.75)}" cy="{n(-r * 0.8)}" r="{n(r * 0.72)}"/><rect x="-.6" y="{n(-r * 0.6)}" width="1.2" height="{n(r * 0.6 + 0.5)}"/>'
        )
        lights = f'<circle cx="{n(-r * 0.35)}" cy="{n(-r * 1.55)}" r="{n(r * 0.5)}" fill="#fff" opacity="{t["leaf_light"]}"/>'
        darks = f'<circle cx="{n(r * 0.75)}" cy="{n(-r * 0.7)}" r="{n(r * 0.5)}" fill="#000" opacity="{t["leaf_shade"]}"/>'
        out.append(f'<g id="o{r}">{crown}{lights}{darks}</g>')
    return "".join(out)


def forest(ground, x0, x1, seed, sizes, density=1.0, oak_share=0.0, oaks=OAKS, sink=2.0, gap=None):
    rnd = random.Random(seed)
    trees = []
    x = x0
    while x < x1:
        if gap and gap[0] < x < gap[1]:
            x = gap[1]
            continue
        y = at(ground, x) + sink + rnd.uniform(0, 2)
        if rnd.random() < oak_share:
            r = rnd.choice(oaks)
            trees.append((y, f'<use href="#o{r}" x="{n(x)}" y="{n(y)}"/>'))
            x += r * rnd.uniform(1.0, 1.6) / density
            continue
        h = rnd.choice(sizes)
        trees.append((y, f'<use href="#f{h}" x="{n(x)}" y="{n(y)}"/>'))
        x += h * rnd.uniform(0.18, 0.5) / density
    return "".join(s for _, s in sorted(trees))
