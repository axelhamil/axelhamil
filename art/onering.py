import math

from geo import n


def arc(r, a0, a1):
    x0, y0 = r * math.cos(math.radians(a0)), r * math.sin(math.radians(a0))
    x1, y1 = r * math.cos(math.radians(a1)), r * math.sin(math.radians(a1))
    return f"M{n(x0)} {n(y0)}A{r} {r} 0 0 1 {n(x1)} {n(y1)}"


def circle_d(r, cy=0):
    return f"M{-r} {cy}A{r} {r} 0 1 1 {r} {cy}A{r} {r} 0 1 1 {-r} {cy}Z"


def reveal(i):
    return 2.2 + i * 0.3


def one_ring(t, inscription, cx, cy, r, band, k=0.58, tilt=-9, depth=22):
    ro, ri = r + band / 2, r - band / 2
    g = t["gold"]
    hull = f"M{-ro} 0A{ro} {ro} 0 0 1 {ro} 0V{depth}A{ro} {ro} 0 0 1 {-ro} {depth}Z"
    face = circle_d(ro) + circle_d(ri)
    xi = math.sqrt(ri * ri - (depth / 2) ** 2)
    lens = f"M{n(-xi)} {depth / 2}A{ri} {ri} 0 0 1 {n(xi)} {depth / 2}A{ri} {ri} 0 0 1 {n(-xi)} {depth / 2}Z"
    length = 2 * math.pi * r
    defs = (
        f'<linearGradient id="goldface" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{g[1]}"/><stop offset=".2" stop-color="{g[3]}"/><stop offset=".3" stop-color="{g[4]}"/>'
        f'<stop offset=".45" stop-color="{g[2]}"/><stop offset=".64" stop-color="{g[3]}"/><stop offset=".82" stop-color="{g[1]}"/><stop offset="1" stop-color="{g[0]}"/></linearGradient>'
        f'<linearGradient id="goldside" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{g[0]}"/><stop offset=".14" stop-color="{g[1]}"/><stop offset=".34" stop-color="{g[3]}"/><stop offset=".42" stop-color="{g[4]}"/>'
        f'<stop offset=".56" stop-color="{g[2]}"/><stop offset=".84" stop-color="{g[1]}"/><stop offset="1" stop-color="{g[0]}"/></linearGradient>'
        f'<linearGradient id="goldinner" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g[0]}"/><stop offset=".5" stop-color="{g[1]}"/><stop offset="1" stop-color="{g[2]}"/></linearGradient>'
        f'<linearGradient id="firelight" x1="0" y1="0" x2=".6" y2="1"><stop offset=".55" stop-color="{t["brand"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity=".4"/></linearGradient>'
        f'<radialGradient id="ringhalo"><stop offset=".55" stop-color="{t["glow"]}" stop-opacity="{t["halo"]}"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="ringheat"><stop offset=".6" stop-color="{t["brand"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["brand"]}" stop-opacity=".12"/></radialGradient>'
        f'<path id="verse" d="M0 {-r}A{r} {r} 0 1 1 -.01 {-r}"/>'
    )
    spec = arc(ro - 2.5, 196, 248) + arc(ri + 2, 300, 335)
    words = inscription.split("᛫")
    spans = "".join(
        f'<tspan class="rw" style="animation-delay:{reveal(i):.2f}s">{w}{"᛫" if i < len(words) - 1 else ""}</tspan>' for i, w in enumerate(words)
    )
    runes = f'<textPath href="#verse" textLength="{length - 6:.0f}" lengthAdjust="spacing">{spans}</textPath>'
    markup = (
        f'<ellipse class="glow" cx="{cx}" cy="{cy + 8}" rx="{n(ro * 1.45)}" ry="{n(ro * 1.0)}" fill="url(#ringhalo)"/>'
        f'<g transform="translate({cx} {cy}) rotate({tilt}) scale(1 {k})">'
        f'<path d="{hull}{lens}" fill="url(#goldside)" fill-rule="evenodd"/>'
        f'<path class="heat" d="{hull}{lens}" fill="url(#firelight)" fill-rule="evenodd"/>'
        f'<path d="{circle_d(ri)}{lens}" fill="url(#goldinner)" fill-rule="evenodd"/>'
        f'<path d="{face}" fill="url(#goldface)" fill-rule="evenodd"/>'
        f'<path class="heat" d="{face}" fill="url(#ringheat)" fill-rule="evenodd"/>'
        f'<path d="{spec}" fill="none" stroke="{g[4]}" stroke-width="2.4" stroke-linecap="round" opacity=".85"/>'
        f'<path d="{circle_d(ro)}{circle_d(ri)}" fill="none" stroke="{g[0]}" stroke-width="1" vector-effect="non-scaling-stroke"/>'
        f'<path d="M{-ro} 0V{depth}A{ro} {ro} 0 0 0 {ro} {depth}V0" fill="none" stroke="{g[0]}" stroke-width="1" vector-effect="non-scaling-stroke"/>'
        f'<g class="spin"><g class="words">'
        f'<text font-family="Runes,serif" font-size="17" fill="none" stroke="{t["brand"]}" stroke-width="3.2" stroke-linejoin="round" opacity=".7" dominant-baseline="central">{runes}</text>'
        f'<text font-family="Runes,serif" font-size="17" fill="{t["glyph"]}" dominant-baseline="central">{runes}</text>'
        f'</g></g></g>'
        f'<g transform="translate({cx - 107} {cy - 33})"><path class="glint" d="M0 -8L1 -1.2L8 0L1 1.2L0 8L-1 1.2L-8 0L-1 -1.2Z" fill="{g[4]}"/></g>'
    )
    return defs, markup
