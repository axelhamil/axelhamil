import random
from datetime import date
from pathlib import Path

from fauna import ANIMATED, STYLE as FAUNA_STYLE, flock
from flora import forest, symbols
from fonts import COURIER, FRAUNCES_MEDIUM, RUNES, face, runes
from geo import at, n, poly, smooth, smooth_closed
from land import SHIRE_REDUCED, SHIRE_STYLE, puff_defs, shire_layer
from landmarks import cart, hole_symbol, moon
from themes import THEMES

W, H = 1200, 240
SEA = 148
SUN_X = 816
LINE = "The road goes ever on."
SIGNATURE = "axel hamilcaro · tours, france"
RUNIC = "THE ROAD GOES EVER ON AND ON"

STYLE = """
.serif{font-family:Fraunces,Georgia,serif}
.mono{font-family:Courier,'Courier New',monospace}
.rune{font-family:Runes,serif}
.tw{animation:tw 6s ease-in-out infinite}
@keyframes tw{50%{opacity:.15}}
.earendil{transform-box:fill-box;transform-origin:center;animation:earendil 5s ease-in-out infinite}
@keyframes earendil{50%{transform:scale(.7) rotate(20deg);opacity:.6}}
.road{animation:road 9s ease-in-out infinite}
@keyframes road{50%{opacity:.55}}
.drift{animation:drift 140s ease-in-out infinite alternate}
@keyframes drift{to{transform:translateX(-36px)}}
.drift2{animation:drift 90s ease-in-out infinite alternate-reverse}
.glitter{animation:glitter 3.4s ease-in-out infinite}
@keyframes glitter{50%{opacity:.12}}
.wave{animation:wave 12s ease-in-out infinite alternate}
@keyframes wave{to{transform:translateX(-22px)}}
.swell{animation:swell 7s ease-in-out infinite alternate}
@keyframes swell{to{transform:translate(14px,1px)}}
.depart{animation:depart 150s linear -24s infinite}
@keyframes depart{0%{transform:translate(0,0) scale(1);opacity:0}4%{opacity:1}88%{opacity:1}100%{transform:translate(-26px,-46px) scale(.42);opacity:0}}
.rock{transform-box:fill-box;transform-origin:50% 100%;animation:rock 6s ease-in-out infinite}
@keyframes rock{0%,100%{transform:rotate(-1.4deg) translateY(0)}50%{transform:rotate(1.4deg) translateY(.8px)}}
.moor{transform-box:fill-box;transform-origin:50% 100%;animation:moor 8s ease-in-out infinite}
@keyframes moor{0%,100%{transform:rotate(-.8deg)}50%{transform:rotate(.8deg) translateY(.5px)}}
.oar{transform-box:fill-box;transform-origin:50% 0;animation:oar 2.4s ease-in-out infinite}
@keyframes oar{0%,100%{transform:skewX(28deg)}50%{transform:skewX(-22deg)}}
.lantern{animation:lantern 2.6s steps(3) infinite}
@keyframes lantern{33%{opacity:.6}66%{opacity:.9}}
.lit{animation:lit 9s ease-in-out infinite}
@keyframes lit{50%{opacity:.5}}
.ring{opacity:0;transform-box:fill-box;transform-origin:center;animation:ring 7s ease-out infinite}
@keyframes ring{0%{opacity:0;transform:translate(0,0) scale(.4)}15%{opacity:.8}100%{opacity:0;transform:translate(8px,-24px) scale(1.9)}}
"""

MOVING = ".tw,.earendil,.road,.drift,.drift2,.glitter,.wave,.swell,.depart,.rock,.moor,.oar,.lantern,.lit"
REDUCED = "@media (prefers-reduced-motion:reduce){" + MOVING + "," + ANIMATED + "{animation:none}.ring{animation:none;opacity:0}" + SHIRE_REDUCED + "}"


def delay(rnd, period):
    return f'style="animation-delay:{-rnd.uniform(0, period):.1f}s"'


def sky(t, dark):
    defs = (
        f'<linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["paper"]}"/><stop offset=".4" stop-color="{t["paper"]}"/>'
        f'<stop offset="1" stop-color="{t["horizon"]}"/></linearGradient>'
        f'<radialGradient id="dusk" cx="{SUN_X}" cy="{SEA}" r="460" gradientTransform="translate(0 {SEA}) scale(1 .42) translate(0 {-SEA})" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{t["gold"][3]}" stop-opacity="{".6" if not dark else ".24"}"/><stop offset=".38" stop-color="{t["glow"]}" stop-opacity="{".13" if not dark else ".1"}"/>'
        f'<stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="sun"><stop offset="0" stop-color="{t["gold"][4]}"/><stop offset=".7" stop-color="{t["gold"][3]}"/><stop offset="1" stop-color="{t["gold"][3]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="pillar"><stop offset="0" stop-color="{t["road_glow"]}" stop-opacity="{".7" if not dark else ".35"}"/><stop offset="1" stop-color="{t["road_glow"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="straight" x1="0" x2="1"><stop offset="0" stop-color="{t["road_glow"]}" stop-opacity="0"/><stop offset=".5" stop-color="{t["road_glow"]}"/><stop offset="1" stop-color="{t["road_glow"]}" stop-opacity="0"/></linearGradient>'
    )
    out = [f'<rect width="{W}" height="{H}" fill="url(#fsky)"/>', f'<rect width="{W}" height="{SEA + 2}" fill="url(#dusk)"/>']
    if dark:
        rnd = random.Random(5)
        dots = []
        for k in range(70):
            x, y = rnd.uniform(4, 1196), rnd.uniform(4, 130)
            if x < 540 and y < 160:
                continue
            o = rnd.uniform(0.2, 0.7) * (1 - y / 170)
            cls = ' class="tw"' if k % 8 == 0 else ""
            dots.append(f'<circle{cls} cx="{n(x)}" cy="{n(y)}" r="{rnd.choice([0.5, 0.6, 0.8])}" opacity="{o:.2f}" style="animation-delay:{rnd.uniform(0, 6):.1f}s"/>')
        out.append(f'<g fill="{t["star"]}">{"".join(dots)}</g>')
    out.append(f'<ellipse class="road" cx="{SUN_X}" cy="{SEA}" rx="18" ry="{110 if not dark else 96}" fill="url(#pillar)"/>')
    if dark:
        star = "M0 -7L1 -1L7 0L1 1L0 7L-1 1L-7 0L-1 -1Z"
        out.append(f'<g transform="translate({SUN_X} 44)"><circle r="7" fill="url(#sun)" opacity=".5"/><path class="earendil" d="{star}" fill="{t["spark"]}"/></g>')
    else:
        out.append(f'<circle cx="{SUN_X}" cy="{SEA + 1}" r="17" fill="url(#sun)"/>')
    return defs, out


def clouds(t):
    rnd = random.Random(23)
    bands = [
        (560, 1200, 128, 12, 2.2, 5), (600, 1180, 112, 9, 2.6, 6), (640, 1200, 92, 7, 2.2, 7),
        (600, 1160, 54, 6, 1.4, 3.4), (700, 1200, 34, 5, 1.2, 3),
    ]
    layers = []
    for x0, x1, y, count, ry0, ry1 in bands:
        lit, body = [], []
        for _ in range(count):
            cx = rnd.uniform(x0, x1)
            rx, ry = rnd.uniform(26, 80), rnd.uniform(ry0, ry1)
            cy = y + rnd.uniform(-5, 5)
            near_sun = max(0.0, 1 - abs(cx - SUN_X) / 360)
            lit.append(f'<ellipse cx="{n(cx)}" cy="{n(cy + ry * 0.45)}" rx="{n(rx * 0.92)}" ry="{n(ry)}" opacity="{0.35 + 0.65 * near_sun:.2f}"/>')
            body.append(f'<ellipse cx="{n(cx + rx * 0.06)}" cy="{n(cy - ry * 0.2)}" rx="{n(rx)}" ry="{n(ry)}"/>')
        cls = "drift" if y > 80 else "drift2"
        layers.append(
            f'<g class="{cls}" opacity="{t["cloud_op"]}"><g fill="{t["cloud_lit"]}">{"".join(lit)}</g><g fill="{t["cloud"]}">{"".join(body)}</g></g>'
        )
    return f'<g clip-path="url(#skyclip)">{"".join(layers)}</g>'


def white_tower(t, x, y, h, w=2.6, lamp=False):
    body = f"M{n(x - w)} {n(y)}L{n(x - w * 0.72)} {n(y - h + 6)}L{n(x - w * 1.05)} {n(y - h + 5)}L{n(x)} {n(y - h)}L{n(x + w * 1.05)} {n(y - h + 5)}L{n(x + w * 0.72)} {n(y - h + 6)}L{n(x + w)} {n(y)}Z"
    shade = f"M{n(x)} {n(y - h + 1)}L{n(x + w * 0.72)} {n(y - h + 6)}L{n(x + w)} {n(y)}L{n(x + w * 0.35)} {n(y)}Z"
    out = f'<path d="{body}" fill="{t["haven"]}" stroke="{t["quay_shade"]}" stroke-width=".35"/><path d="{shade}" fill="{t["quay_shade"]}" opacity=".7"/>'
    if lamp:
        out += f'<rect class="lantern" x="{n(x - 0.6)}" y="{n(y - h + 7)}" width="1.2" height="2" fill="{t["window"]}"/>'
    return out


def gulf(t, dark):
    far_r = [(900, SEA + 1), (930, SEA - 8), (960, SEA - 12), (990, SEA - 6), (1010, SEA + 1)]
    downs = [(-10, SEA + 6), (60, SEA - 4), (140, SEA + 2), (230, SEA - 8), (330, SEA - 2), (420, SEA - 10), (500, SEA - 4), (580, SEA + 2), (640, SEA + 30)]
    beraid = [(440, SEA + 40), (490, SEA + 12), (540, SEA - 2), (576, 130), (610, 120), (646, 116), (690, 120), (740, 132), (772, SEA - 6), (786, SEA + 6)]
    face = f"M760 {SEA - 9}C772 {SEA - 6} 782 {SEA - 1} 786 {SEA + 6}L768 {SEA + 6}C768 {SEA} 765 {SEA - 5} 760 {SEA - 9}Z"
    towers = "".join(white_tower(t, x, at(beraid, x) + 2, h, w, lamp=lamp) for x, h, w, lamp in [(616, 32, 2.6, False), (646, 52, 3.3, dark), (676, 30, 2.5, False)])
    return (
        f'<path d="{smooth_closed(far_r, SEA + 2)}" fill="{t["far"]}"/>'
        f'<path d="{smooth_closed(downs, SEA + 40)}" fill="{t["far2"]}"/>'
        f'<g fill="{t["fir_far"]}">{forest(beraid, 548, 760, 13, [6, 9], 0.5, 0.5, [5], sink=3, gap=(600, 692))}</g>'
        f'<path d="{smooth_closed(beraid, SEA + 40)}" fill="{t["mid"]}"/><path d="{face}" fill="{t["lune_shade"]}"/>'
        f'{towers}'
    )


def sea(t, dark):
    defs = f'<linearGradient id="fsea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["sea"]}"/><stop offset="1" stop-color="{t["sea_deep"]}"/></linearGradient>'
    rnd = random.Random(11)
    glints = []
    for k in range(32):
        y = SEA + 2 + k * 2.8 + rnd.uniform(-0.4, 0.4)
        half = (2 + k * 0.55) * rnd.uniform(0.4, 1.1)
        x = SUN_X + rnd.uniform(-0.35, 0.35) * (k + 4) - k * 0.25
        glints.append(f'<path class="glitter" d="M{n(x - half)} {n(y)}h{n(half * 2)}" {delay(rnd, 3.4)}/>')
    waves = "".join(f"M{n(x)} {n(y)}q3 -1.1 6 0" for x, y in [(rnd.uniform(560, 1190), rnd.uniform(SEA + 5, H - 4)) for _ in range(80)])
    swell = "".join(f"M{n(x)} {n(y)}q8 -1.6 16 0" for x, y in [(rnd.uniform(620, 1180), rnd.uniform(SEA + 30, H - 6)) for _ in range(26)])
    out = [
        f'<rect y="{SEA}" width="{W}" height="{H - SEA}" fill="url(#fsea)"/>',
        f'<path class="road" d="M{SUN_X - 120} {SEA}h240" stroke="url(#straight)" stroke-width="1.6"/>',
        f'<g class="wave"><path d="{waves}" fill="none" stroke="{t["ripple"]}" stroke-width=".6" opacity=".55"/></g>',
        f'<g class="swell"><path d="{swell}" fill="none" stroke="{t["ripple_dark"]}" stroke-width=".7" opacity=".6"/></g>',
        f'<g stroke="{t["gold"][4] if not dark else t["road_glow"]}" stroke-width="1" stroke-linecap="round" opacity="{".95" if not dark else ".5"}">{"".join(glints)}</g>',
    ]
    return defs, out


SWAN = (
    "M24 -2C25.5 -5 27.5 -8 27 -12C29.5 -9 29.6 -4 27 0C22 5 -6 6 -14 1C-17 -1 -19 -3 -20 -6"
    "C-23.5 -9 -23.4 -15 -21 -19C-19.6 -21.4 -16.6 -22.2 -15.6 -20.4L-14.2 -19.6L-17.4 -19C-19.2 -16.6 -19.4 -12.4 -17 -8.6"
    "C-15 -5.4 -12 -3.4 -8 -2.6Z"
)


def swan_ship(t, x, y, s, sail, cls, rowing=False, fill=None):
    fill = fill or t["ship_hull"]
    rnd = random.Random(int(x))
    mast = f'<path d="M2 -3V-40" stroke="{fill}" stroke-width="1"/>'
    if sail:
        canvas = "M-11 -37C-3 -39.5 7 -39.5 15 -37C17.4 -27 17 -16 14.6 -7C6 -5.6 -3 -5.6 -10.4 -7C-8.6 -17 -8.8 -27 -11 -37Z"
        rig = f'<path d="M-12 -37.4h28M-11 -6.8h26" stroke="{fill}" stroke-width=".7"/>'
        sails = f'<path d="{canvas}" fill="{t["sail"]}" stroke="{fill}" stroke-width=".45"/><path d="M2 -38C5 -28 5 -16 2 -6.4" fill="none" stroke="{t["quay_shade"]}" stroke-width=".6" opacity=".7"/>{rig}'
    else:
        sails = f'<path d="M-9 -34h22" stroke="{fill}" stroke-width=".9"/><path d="M-8 -34.8h20v1.8h-20Z" fill="{t["sail"]}" opacity=".85"/>'
    oars = ""
    if rowing:
        oars = "".join(f'<path class="oar" style="animation-delay:{-k * 0.08:.2f}s" d="M{x0} 1.5l0 8" stroke="{fill}" stroke-width=".55"/>' for k, x0 in enumerate(range(-8, 22, 4)))
    stripe = f'<path d="M-12 -1.2C-2 2 14 2 25 -2.4" fill="none" stroke="{t["haven"]}" stroke-width=".6" opacity=".7"/>'
    body = f'{oars}{mast}{sails}<path d="{SWAN}" fill="{fill}"/>{stripe}<circle cx="-17.6" cy="-17.6" r=".55" fill="{t["paper"]}"/>'
    timing = f'style="animation-delay:{-rnd.uniform(0, 8):.1f}s"'
    return f'<g transform="translate({x} {y}) scale({s})"><g class="{cls}" {timing}>{body}</g></g>'


def departing(t):
    wake = (
        f'<path class="glitter" d="M28 1L70 6M28 1L66 -1M40 3.4L84 8" fill="none" stroke="{t["ripple"]}" stroke-width=".8" stroke-linecap="round" opacity=".85"/>'
        f'<path d="M-14 3.6C-2 6.4 16 6.4 28 2" fill="none" stroke="{t["ripple"]}" stroke-width=".9" opacity=".7"/>'
    )
    return (
        f'<g transform="translate(842 200)"><g class="depart">{wake}'
        f'{swan_ship(t, 0, 0, 1.25, True, "rock", rowing=True)}</g></g>'
    )


def building(t, rnd, x, base, kind):
    shade, arch = t["quay_shade"], t["arch"]
    if kind == "spire":
        h, w = rnd.uniform(24, 34), rnd.uniform(2, 2.8)
        return white_tower(t, x + w, base, h, w), 2 * w + rnd.uniform(1, 3)
    if kind == "hall":
        w, h = rnd.uniform(16, 24), rnd.uniform(9, 12)
        roof = f"M{n(x - 1)} {n(base - h)}Q{n(x + w * 0.3)} {n(base - h - 1)} {n(x + w / 2)} {n(base - h - 7)}Q{n(x + w * 0.7)} {n(base - h - 1)} {n(x + w + 1)} {n(base - h)}Z"
        arches = "".join(f"M{n(wx)} {n(base - 1.5)}v-{n(h * 0.45)}a1 1 0 0 1 2 0v{n(h * 0.45)}Z" for wx in [x + 2 + k * 3.6 for k in range(int((w - 3) // 3.6))])
        return (
            f'<path d="M{n(x)} {n(base)}V{n(base - h)}H{n(x + w)}V{n(base)}Z" fill="{t["haven"]}" stroke="{shade}" stroke-width=".35"/>'
            f'<path d="{roof}" fill="{t["haven"]}" stroke="{shade}" stroke-width=".35"/><path d="{arches}" fill="{arch}" class="lit" {delay(rnd, 9)}/>'
        ), w + rnd.uniform(1, 4)
    w, h = rnd.uniform(7, 12), rnd.uniform(6, 10)
    peak = rnd.uniform(4, 7)
    roof = f"M{n(x - 0.8)} {n(base - h)}Q{n(x + w * 0.35)} {n(base - h - 0.6)} {n(x + w / 2)} {n(base - h - peak)}Q{n(x + w * 0.65)} {n(base - h - 0.6)} {n(x + w + 0.8)} {n(base - h)}Z"
    door = f"M{n(x + w / 2 - 1)} {n(base)}v-2.6a1 1 0 0 1 2 0v2.6Z"
    return (
        f'<path d="M{n(x)} {n(base)}V{n(base - h)}H{n(x + w)}V{n(base)}Z" fill="{t["haven"]}" stroke="{shade}" stroke-width=".35"/>'
        f'<path d="{roof}" fill="{t["haven"]}" stroke="{shade}" stroke-width=".35"/><path d="{door}" fill="{arch}" class="lit" {delay(rnd, 9)}/>'
    ), w + rnd.uniform(0.5, 5)


def figures(t, x, y):
    gandalf = "M0 0L1.2 -7.2L.7 -7.6L2.2 -12.6L3.4 -7.6L3 -7.2L4.4 0Z"
    staff = "M5.6 0V-10.4"
    hobbit = lambda dx, s: f'<g transform="translate({n(dx)} 0) scale({s})"><path d="M-1.4 0C-1.6 -2.4 -1.2 -4.4 0 -4.6C1.2 -4.4 1.6 -2.4 1.4 0Z"/><circle cy="-5.6" r="1.05"/></g>'
    return (
        f'<g transform="translate({x} {y})" fill="{t["front"]}">{hobbit(-8, 1)}{hobbit(-4.4, 0.95)}{hobbit(-1.2, 0.9)}'
        f'<g transform="translate(1.2 0)"><path d="{gandalf}" fill="{t["gandalf"]}"/><path d="{staff}" stroke="{t["gandalf"]}" stroke-width=".55"/></g></g>'
    )


def havens(t, dark):
    back = [(940, SEA), (990, 96), (1040, 74), (1090, 62), (1130, 44), (1170, 50), (1200, 46)]
    hill = [(900, SEA + 30), (926, SEA - 4), (950, 134), (975, 124), (1000, 110), (1030, 100), (1060, 86), (1095, 80), (1130, 68), (1165, 70), (1200, 62)]
    ridge = [(1010, 118), (1060, 100), (1110, 92), (1200, 88)]
    levels = [(1096, 112, 124), (1046, 132, 146), (994, 152, 166), (936, 170, 179)]
    rnd = random.Random(8)
    out = [
        f'<path d="{smooth_closed(back, SEA + 40)}" fill="{t["lune"]}"/>',
        f'<path d="{smooth_closed(hill, SEA + 40)}" fill="{t["lune_high"]}"/>',
        f'<path d="{smooth(ridge)}" fill="none" stroke="{t["lune_high_shade"]}" stroke-width="1.2" opacity=".7"/>',
    ]
    plan = ["house", "spire", "hall", "house", "house", "spire", "hall", "house", "spire", "house", "house"]
    for i, (x0, top, bottom) in enumerate(levels):
        wall = f"M{x0 - 4} {bottom}L{x0} {top}H{W}V{bottom}Z"
        stair = "".join(f"M{n(x0 - 3 + k * 1.1)} {n(top + 2 + k * 2.4)}h3" for k in range(int((bottom - top - 2) / 2.4)))
        out.append(f'<path d="{wall}" fill="{t["haven"]}" stroke="{t["quay_shade"]}" stroke-width=".4"/><path d="{stair}" stroke="{t["quay_shade"]}" stroke-width=".5"/>')
        if bottom - top > 8:
            arcade = "".join(f"M{n(ax)} {bottom - 1.5}v-{n((bottom - top) * 0.45)}a1.6 1.6 0 0 1 3.2 0v{n((bottom - top) * 0.45)}Z" for ax in range(x0 + 6, W, 9))
            out.append(f'<path d="{arcade}" fill="{t["arch"]}" opacity=".8"/>')
        x = x0 + rnd.uniform(4, 10)
        k = i * 3
        while x < W - 4 and i < 3:
            kind = plan[k % len(plan)] if rnd.random() < 0.75 else rnd.choice(["house", "hall", "spire"])
            svg, step = building(t, rnd, x, top, kind)
            out.append(svg)
            x += step + rnd.uniform(0, 6)
            k += 1
    pier_top = 172
    piles = "".join(f"M{px} 181Q{px + 4} {pier_top + 3} {px + 8} 181" for px in range(882, 936, 8))
    out.append(
        f'<path d="M878 {pier_top}H938V{pier_top + 3}H878Z" fill="{t["haven"]}" stroke="{t["quay_shade"]}" stroke-width=".4"/>'
        f'<path d="{piles}" fill="none" stroke="{t["haven"]}" stroke-width="1.2"/><path d="{piles}" fill="none" stroke="{t["quay_shade"]}" stroke-width=".4" transform="translate(0 .8)"/>'
        f'<path d="M878 181H938" stroke="{t["haven"]}" stroke-width="1" opacity=".35"/>'
    )
    tower_x, tower_h = 884, 50
    out.append(white_tower(t, tower_x, pier_top, tower_h, 3.2))
    lamp_y = pier_top - tower_h + 8
    out.append(
        f'<circle cx="{tower_x}" cy="{lamp_y}" r="9" fill="url(#lanternglow)"/>'
        f'<path class="lantern" d="M{tower_x - 1.1} {lamp_y - 1.6}h2.2v3.4h-2.2Z" fill="{t["window"]}"/>'
    )
    out.append(figures(t, 906, pier_top))
    out.append(f'<rect class="glitter" x="936" y="181" width="264" height="6" fill="{t["haven"]}" opacity=".18"/>')
    for x, y, s in [(970, 187, 0.62), (1046, 188, 0.68), (1126, 187, 0.64)]:
        out.append(swan_ship(t, x, y, s, False, "moor", fill=t["hull"]))
    windows = "".join(f'<circle class="lit" cx="{n(x)}" cy="{n(y)}" r=".7" {delay(rnd, 9)}/>' for x, y in [(1000, 162), (1050, 141), (1092, 160), (1130, 122), (1172, 140), (1010, 140), (1150, 162)])
    out.append(f'<g fill="{t["window"]}" opacity="{t["haven_lights"]}">{windows}</g>')
    return "".join(out)


def shire(t):
    shire_defs, fields, homes = shire_layer(t)
    smoker = (
        '<g transform="translate(232 456.6)" fill="' + t["front"] + '">'
        '<path d="M-3 0h6v.6h-6Z"/><path d="M-2 0C-2 -2.3 -1.4 -3.8 .1 -4C1.5 -3.8 2 -2.3 1.8 0Z"/><circle cx=".1" cy="-5.1" r="1.25"/>'
        '<path d="M1.2 -4.6L3.6 -4L3.8 -4.8" fill="none" stroke="' + t["front"] + '" stroke-width=".4"/></g>'
    )
    rings = "".join(
        f'<ellipse class="ring" cx="237" cy="449" rx="1.3" ry=".8" fill="none" stroke="{t["smoke"]}" stroke-width=".45" style="animation-delay:{d}s"/>'
        for d in (0, 2.3, 4.6)
    )
    lane = f'<path d="M214 457C196 462 160 468 120 470C80 472 40 474 -14 476" fill="none" stroke="{t["path"]}" stroke-width="2.4" stroke-linecap="round"/>'
    sign = (
        f'<g transform="translate(178 466)" fill="{t["fence"]}">'
        '<path d="M-.4 0V-10h.8V0Z"/><path d="M.4 -9.5h5.6l1.2 1-1.2 1h-5.6Z"/><path d="M-.4 -6.8h-5l-1.2 .9 1.2 .9h5Z"/></g>'
    )
    layer = fields + homes + lane + sign + smoker + rings + cart(t, 336, 469)
    return shire_defs, f'<g transform="translate(-6 -296) scale(1.12)">{layer}</g>'


def shore(t):
    rnd = random.Random(31)
    coast = [(600, H + 6), (636, 228), (680, 214), (726, 212), (764, 220), (800, 232), (816, H + 6)]
    tufts = "".join(f"M{n(x)} {n(at(coast, x) + 2)}l{n(rnd.uniform(-1.5, -0.4))} -{n(rnd.uniform(3, 6))}" for x in [rnd.uniform(630, 800) for _ in range(40)])
    rocks = []
    for x, y, w, h in [(1092, 236, 26, 10), (1120, 232, 34, 16), (1160, 230, 44, 20), (1060, 240, 18, 6), (806, 236, 20, 8), (822, 238, 14, 6)]:
        rocks.append(poly([(x - w / 2, y + 4), (x - w * 0.4, y - h * 0.6), (x - w * 0.1, y - h), (x + w * 0.3, y - h * 0.8), (x + w / 2, y + 4)]))
    grass = "".join(f"M{n(x)} {n(y)}l{n(rnd.uniform(-2, 2))} -{n(rnd.uniform(4, 9))}" for x, y in [(rnd.uniform(1130, 1200), rnd.uniform(214, 222)) for _ in range(40)])
    foam = "".join(f"M{x} {y}q4 -1.4 8 0" for x, y in [(1070, 233), (1100, 226), (1140, 221), (798, 233), (826, 235)])
    return (
        f'<path d="{smooth_closed(coast, H + 6)}" fill="{t["near"]}"/><path d="{tufts}" stroke="{t["near"]}" stroke-width=".9" stroke-linecap="round"/>'
        f'<path d="{"".join(rocks)}" fill="{t["rock"]}"/>'
        f'<path d="{grass}" stroke="{t["grass"]}" stroke-width="1" stroke-linecap="round"/>'
        f'<g class="glitter"><path d="{foam}" fill="none" stroke="{t["ripple"]}" stroke-width=".8"/></g>'
    )


def scene(t, day):
    dark = t["star"] is not None
    defs, out = sky(t, dark)
    sea_defs, sea_out = sea(t, dark)
    defs += sea_defs + symbols(t) + hole_symbol(t) + (
        f'<clipPath id="skyclip"><rect x="540" width="{W - 540}" height="{SEA}"/></clipPath>'
        + puff_defs(t)
        + f'<radialGradient id="lanternglow"><stop offset="0" stop-color="{t["window"]}" stop-opacity=".55"/><stop offset="1" stop-color="{t["window"]}" stop-opacity="0"/></radialGradient>'
    )
    if dark:
        out.append(moon(t, 1150, 30, 7, day))
    out.append(clouds(t))
    out += sea_out
    out.append(gulf(t, dark))
    out.append(havens(t, dark))
    out.append(departing(t))
    out.append(flock(t["gull"], 1240, 54, [(0, 0, 0.9), (12, 6, 0.8), (22, -3, 0.85)], 77, 0.8))
    out.append(flock(t["gull"], 1290, 104, [(0, 0, 0.75), (9, 4, 0.7)], 78, 0.8).replace('class="migrate"', 'class="migrate" style="animation-delay:-30s;animation-duration:80s"'))
    shire_defs, shire_out = shire(t)
    defs += shire_defs
    out.append(shire_out)
    out.append(shore(t))
    return defs, out


def svg(t, fonts_dir, day):
    faces = face(fonts_dir, FRAUNCES_MEDIUM, LINE) + face(fonts_dir, COURIER, SIGNATURE) + face(fonts_dir, RUNES, runes(RUNIC))
    defs, out = scene(t, day)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ft">
<title id="ft">{LINE} The Grey Havens at sunset, Emyn Beraid and the Shire road. Axel Hamilcaro, Tours, France.</title>
<defs>{defs}</defs>
<style>{faces}{STYLE}{SHIRE_STYLE}{FAUNA_STYLE}{REDUCED}</style>
{"".join(out)}
<text class="serif" x="72" y="74" font-size="34" font-weight="500" fill="{t["ink"]}">{LINE}</text>
<text class="mono" x="74" y="104" font-size="14" fill="{t["muted"]}">{SIGNATURE}</text>
<text class="rune" x="74" y="130" font-size="13" letter-spacing="2" fill="{t["brand"]}" opacity=".75">{runes(RUNIC)}</text>
</svg>
"""


def build(fonts_dir, out_dir, day=None):
    day = day or date.today()
    for name, theme in THEMES.items():
        (Path(out_dir) / f"footer-{name}.svg").write_text(svg(theme, fonts_dir, day))
