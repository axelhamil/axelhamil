import math
import random

from flora import forest, symbols
from geo import H, W, at, hills, n, poly, smooth_closed, smoothstep
from landmarks import (
    barad_dur, beacon, black_gate, cart, doom, eye_defs, firework, gollum, hole_symbol, minas_tirith,
    moon, orthanc, plume, stars, sting, eye_beam, fireflies, clouds,
)
from fauna import ANIMATED, STYLE as FAUNA_STYLE, eagle, fell_beast, flock
from mountains import mountain_range

DOOM_X, DOOM_TOP, DOOM_BASE = 1092, 348, 438
TOWER_X, TOWER_BASE, TOWER_SCALE = 1162, 436, 0.78

STYLE = """<style>
.eye{transform-box:fill-box;transform-origin:center;animation:eye 6s ease-in-out infinite}
@keyframes eye{50%{transform:scale(1.3);opacity:.6}}
.tw{animation:tw 6s ease-in-out infinite}
@keyframes tw{50%{opacity:.08}}
.ash{opacity:0;transform-box:fill-box;transform-origin:center;animation:ash 12s ease-out 2s infinite}
@keyframes ash{0%{opacity:0;transform:translate(0,0) scale(.6)}20%{opacity:.85}100%{opacity:0;transform:translate(46px,-64px) scale(2.4)}}
.fw{opacity:0;transform-box:fill-box;transform-origin:center;animation:fw 9s ease-out 5s infinite}
@keyframes fw{0%{opacity:0;transform:scale(.2)}4%{opacity:1}14%{opacity:0;transform:scale(1.15)}100%{opacity:0;transform:scale(1.15)}}
.sting{animation:sting 5s ease-in-out infinite}
@keyframes sting{50%{opacity:.45}}
.pupil{transform-box:fill-box;transform-origin:center;animation:pupil 14s ease-in-out infinite}
@keyframes pupil{0%,100%{transform:translateX(-1.2px)}45%,55%{transform:translateX(1.2px)}}
.beam{animation:beam 14s ease-in-out infinite}
@keyframes beam{0%,100%{transform:rotate(-7deg)}50%{transform:rotate(9deg)}}
.flick{animation:flick 3.7s steps(1) infinite}
@keyframes flick{0%{opacity:1}23%{opacity:.75}31%{opacity:1}58%{opacity:.85}64%{opacity:.6}70%{opacity:1}}
.cloud{animation:cloud 60s ease-in-out infinite alternate}
@keyframes cloud{to{transform:translateX(-50px)}}
.blink{transform-box:fill-box;transform-origin:center;animation:blink 7s infinite}
@keyframes blink{0%,93%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}
.rip ellipse{transform-box:fill-box;transform-origin:center;animation:rip 5s ease-out infinite}
@keyframes rip{0%{transform:scale(.4);opacity:0}30%{opacity:.8}100%{transform:scale(1.2);opacity:0}}
.pennant{animation:pennant 3.2s ease-in-out infinite}
@keyframes pennant{50%{transform:scale(.8,1.25) skewY(8deg)}}
.beacon{transform-box:fill-box;transform-origin:50% 100%;animation:beacon 1.6s steps(4) infinite}
@keyframes beacon{25%{transform:scale(1.1,.85);opacity:.8}50%{transform:scale(.9,1.2)}75%{transform:scale(1.05,.9);opacity:.9}}
.ff{opacity:0;animation:ff 7s ease-in-out infinite}
@keyframes ff{30%{opacity:.9;transform:translate(2px,-3px)}60%{opacity:0;transform:translate(5px,-1px)}}
@media (prefers-reduced-motion:reduce){.eye,.tw,.sting,.pupil,.beam,.flick,.cloud,.pennant,.beacon,.blink,.rip,.rip ellipse,@ANIM@{animation:none}.ash{animation:none;opacity:.5}.fw{animation:none;opacity:0}.ff{animation:none;opacity:.5}}
</style>"""
SHIRE_STYLE = """
.puff{opacity:0;transform-box:fill-box;transform-origin:center;animation:puff 8s ease-out infinite}
@keyframes puff{0%{opacity:0;transform:translate(0,0) scale(.5)}25%{opacity:.75}100%{opacity:0;transform:translate(10px,-24px) scale(2)}}
.flicker{animation:flicker 7s steps(1) 3s infinite}
@keyframes flicker{0%{opacity:1}40%{opacity:.55}44%{opacity:1}71%{opacity:.7}74%{opacity:1}}
"""
def puff_defs(t):
    return f'<radialGradient id="puff"><stop offset="0" stop-color="{t["smoke"]}" stop-opacity=".8"/><stop offset="1" stop-color="{t["smoke"]}" stop-opacity="0"/></radialGradient>'


SHIRE_REDUCED = ".flicker{animation:none}.puff{animation:none;opacity:.5}"
STYLE = STYLE.replace("@ANIM@", ANIMATED).replace("<style>", "<style>" + FAUNA_STYLE + SHIRE_STYLE).replace("{animation:none}.ash", "{animation:none}" + SHIRE_REDUCED + ".ash")


def mist_band(t, y, seed, count, duration):
    rnd = random.Random(seed)
    blobs = "".join(
        f'<ellipse cx="{n(rnd.uniform(-80, 1280))}" cy="{n(y + rnd.uniform(-3, 3))}" rx="{n(rnd.uniform(90, 170))}" ry="{n(rnd.uniform(9, 15))}"/>'
        for _ in range(count)
    )
    return f'<g class="mist" fill="url(#mistg)" style="animation-duration:{duration}s">{blobs}</g>'


def river(t):
    left, right, centre = [], [], []
    for i in range(19):
        k = i / 18
        y = 415 + k * 65
        x = 878 - 46 * k + math.sin(k * 7.2 + 0.4) * (2.5 + 22 * k)
        w = 0.6 + 26 * k ** 1.8
        centre.append((x, y, w))
        left.append((x - w / 2, y))
        right.append((x + w / 2, y))
    body = poly(left + right[::-1])
    rnd = random.Random(61)
    lights, darks = [], []
    for x, y, w in centre[2:]:
        for _ in range(2):
            length = w * rnd.uniform(0.2, 0.55)
            ox = rnd.uniform(-w / 2 + length / 2, w / 2 - length / 2) if w > length else 0
            target = lights if rnd.random() < 0.6 else darks
            target.append(f"M{n(x + ox - length / 2)} {n(y + rnd.uniform(-1.5, 1.5))}h{n(length)}")
    banks = poly(left[2:] + [(left[-1][0] - 3, 480)]) + poly(right[2:] + [(right[-1][0] + 3, 480)])
    out = (
        f'<path d="{body}" fill="url(#riverg)"/>'
        f'<path d="{"".join(lights)}" stroke="{t["ripple"]}" stroke-width=".7" stroke-linecap="round" opacity=".8"/>'
        f'<path d="{"".join(darks)}" stroke="{t["ripple_dark"]}" stroke-width=".7" stroke-linecap="round" opacity=".7"/>'
        f'<path d="{"".join("M" + n(a[0]) + " " + n(a[1]) + "L" + n(b[0]) + " " + n(b[1]) for a, b in zip(left[3:], left[4:]))}" stroke="{t["near_shade"]}" stroke-width=".7" opacity=".6"/>'
    )
    return out, centre


def shire(t, back):
    rnd = random.Random(71)
    strips, hedges = [], []
    tops = [-40 + k * 34 + rnd.uniform(-6, 6) for k in range(19)]
    colours = [t["field_a"], t["field_b"], t["field_c"]]
    for i, (a, b) in enumerate(zip(tops, tops[1:])):
        fan = lambda x: x * 1.35 - 80
        strips.append(f'<path d="{poly([(a, 395), (b, 395), (fan(b), 482), (fan(a), 482)])}" fill="{colours[i % 3]}"/>')
        hedges.append(f"M{n(a)} 395L{n(fan(a))} 482")
    contours = "".join(
        "M" + "L".join(f"{n(x)} {n(at(back, x) + off)}" for x in range(0, 600, 20))
        for off in (7, 17)
    )
    lone = "".join(
        f'<use href="#o{rnd.choice([5, 7])}" x="{n(x)}" y="{n(at(back, x) + rnd.uniform(3, 14))}"/>'
        for x in [rnd.uniform(10, 470) for _ in range(9)]
    )
    flock_xy = [(x, at(back, x) + rnd.uniform(6, 20)) for x in [rnd.uniform(380, 520) for _ in range(7)] + [rnd.uniform(20, 110) for _ in range(4)]]
    sheep = "".join(f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="1.7" ry="1.1"/>' for x, y in flock_xy)
    heads = "".join(f"M{n(x - 1.5)} {n(y - 0.4)}h-.9" for x, y in flock_xy)
    stacks = "".join(f'<path d="M{n(x - 3)} {n(y)}Q{n(x)} {n(y - 6)} {n(x + 3)} {n(y)}Z"/>' for x, y in [(x, at(back, x) + 12) for x in (300, 318, 470, 140)])
    party_x = 372
    party_y = at(back, party_x) + 6
    fields = (
        f'<path d="{smooth_closed(back)}" fill="{t["field_b"]}"/>'
        f'<g clip-path="url(#shireclip)">{"".join(strips)}'
        f'<path d="{"".join(hedges)}{contours}" fill="none" stroke="{t["hedge"]}" stroke-width="2" stroke-dasharray="0 2.6" stroke-linecap="round"/></g>'
        f'<g fill="{t["path"]}">{stacks}</g><g fill="{t["sheep"]}">{sheep}</g><path d="{heads}" stroke="{t["front"]}" stroke-width="1.1"/>'
        f'<g fill="{t["near"]}">{lone}<use href="#o10" transform="translate({party_x} {n(party_y)}) scale(1.7)"/></g>'
        f'<g fill="{t["glyph"]}" opacity=".6">{"".join(f"<circle cx=\"{n(party_x + dx)}\" cy=\"{n(party_y - dy)}\" r=\".55\"/>" for dx, dy in [(-12, 14), (-6, 20), (2, 23), (9, 19), (14, 13), (-14, 8), (15, 6)])}</g>'
    )
    bag_end = "M78 478C108 432 160 413 214 412C268 411 314 430 356 478Z"
    small = "M360 480C380 455 410 446 440 448C470 450 494 464 512 480Z"
    west = "M-10 478C14 452 48 444 80 448C102 451 114 464 122 478Z"
    homes = (
        f'<path d="{west}" fill="url(#hillg)"/><path d="{small}" fill="url(#hillg)"/><path d="{bag_end}" fill="url(#hillg)"/>'
        f'<path d="M244.6 404h3.4v13h-3.4Z" fill="{t["stone"]}"/><path d="M244 403.4h4.6v1.4h-4.6Z" fill="{t["stone"]}"/>'
        f'<use href="#hole" x="214" y="447"/><use class="flicker" href="#win" x="241" y="444"/><use href="#win" x="187" y="446"/><use href="#win" x="262" y="452"/>'
        f'<use href="#hole" transform="translate(432 463) scale(.7)"/><use href="#win" transform="translate(452 461) scale(.8)"/>'
        f'<use href="#hole" transform="translate(52 461) scale(.65)"/><use href="#win" transform="translate(72 459) scale(.75)"/>'
        f'<path d="M150 466v-5M157 466v-5M164 466v-5M171 466v-5M178 466v-5M250 466v-5M257 466v-5M264 466v-5M271 466v-5M278 466v-5M285 466v-5M148 462.5h32M248 462.5h39" stroke="{t["fence"]}" stroke-width=".9"/>'
        f'<path d="M214 457C222 464 252 465 290 467C330 469 380 472 430 480" fill="none" stroke="{t["path"]}" stroke-width="3" stroke-linecap="round"/>'
        f'<g fill="{t["window"]}" opacity=".85"><circle cx="198" cy="458" r=".8"/><circle cx="231" cy="458" r=".8"/><circle cx="226" cy="455" r=".7"/><circle cx="202" cy="455" r=".7"/></g>'
        f'<g fill="{t["glyph"]}" opacity=".8"><circle cx="200" cy="457" r=".7"/><circle cx="228" cy="457.5" r=".7"/></g>'
        + "".join(f'<circle class="puff" cx="246" cy="398" r="{r}" fill="url(#puff)" style="animation-delay:{d}s"/>' for r, d in [(4, 0), (5, 2.7), (4.5, 5.4)])
    )
    return fields, homes


def shire_layer(t):
    back = hills(-20, 620, 446, 6, 53, step=30, shape=lambda x: smoothstep(430, 600, x) * 40)
    defs = (
        f'<clipPath id="shireclip"><path d="{smooth_closed(back)}"/></clipPath>'
        f'<linearGradient id="hillg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["near_lit"]}"/><stop offset=".55" stop-color="{t["near"]}"/><stop offset="1" stop-color="{t["near_shade"]}"/></linearGradient>'
    )
    fields, homes = shire(t, back)
    return defs, fields, homes


def scene(t, day):
    dark = t["star"] is not None
    defs = [
        f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["paper"]}"/><stop offset=".55" stop-color="{t["paper"]}"/>'
        f'<stop offset="1" stop-color="{t["horizon"]}"/></linearGradient>'
        f'<radialGradient id="doomsky" cx="{DOOM_X}" cy="{DOOM_TOP}" r="300" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{t["brand"]}" stop-opacity="{t["doomsky"]}"/><stop offset="1" stop-color="{t["brand"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="mistg"><stop offset="0" stop-color="{t["mist"]}" stop-opacity="{t["mist_op"]}"/><stop offset="1" stop-color="{t["mist"]}" stop-opacity="0"/></radialGradient>'
        + puff_defs(t)
        + f'<radialGradient id="stingglow"><stop offset="0" stop-color="{t["sting"]}" stop-opacity="{t["sting_op"]}"/><stop offset="1" stop-color="{t["sting"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="riverg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["horizon"]}"/><stop offset="1" stop-color="{t["river"]}"/></linearGradient>'
        + eye_defs(t)
        + symbols(t)
        + hole_symbol(t)
    ]

    out = [STYLE, f'<rect width="{W}" height="{H}" fill="url(#sky)"/>', f'<rect class="heat" width="{W}" height="{H}" fill="url(#doomsky)"/>']
    if dark:
        out.append(stars(t, 13) + moon(t, 1152, 50, 9, day))
    out.append(eagle(t, 762, 98, 1.15, (28, -3), (12, -1)) + eagle(t, 795, 121, 0.8, (33, -17), (10.5, -6.5)) + eagle(t, 742, 130, 0.6, (24, -9), (13.5, -9.8)))
    out.append(flock(t["eagle"], 1250, 34, [(0, 0, 1), (9, 4, 0.9), (17, 1, 1.05), (-7, 6, 0.85), (25, 6, 0.8), (13, -4, 0.9)], 41))

    misty = [(40, 14, 60), (130, 22, 80), (230, 18, 70), (330, 28, 90), (420, 40, 90), (500, 54, 100), (575, 66, 110),
             (645, 60, 95), (715, 96, 125), (782, 82, 110), (850, 56, 95), (905, 34, 70)]
    d, m, _ = mountain_range("mm", t, 0, 1000, 402, misty, 3, t["far"], t["far_shade"], (t["snow"], t["snow_shade"]), 0.32, 30, taper=(0, 50))
    defs.append(d)
    out.append(m)
    od, om = orthanc(t, 714, 405)
    defs.append(od)
    out.append(om)
    fangorn = [(x, 418 + ((x - 714) / 40) ** 2 * 2) for x in range(660, 772, 4)]
    out.append(f'<g fill="{t["fangorn"]}">{forest(fangorn, 668, 764, 31, [6, 9], 1.3, 0.4, [5], sink=1)}</g>')
    out.append(firework(t, 396, 368))
    out.append(f'<g class="cloud" fill="url(#mistg)">{clouds(t, 5, [(640, 352), (760, 338), (980, 346), (1120, 336), (860, 362)])}</g>')

    white = [(790, 26, 60), (848, 42, 70), (906, 54, 78), (962, 38, 70), (1004, 22, 55)]
    d, m, _ = mountain_range("wm", t, 720, 1060, 410, white, 11, t["far2"], t["far2_shade"], (t["snow"], t["snow_shade"]), 0.3, 30, taper=(40, 40))
    defs.append(d)
    out.append(m)
    cd, cm = minas_tirith(t, 893, 407)
    defs.append(cd)
    out.append(cm + beacon(t, 962, 371))

    lithui = [(940, 16, 45), (985, 26, 50), (1030, 32, 55), (1075, 24, 45), (1140, 44, 60), (1195, 34, 55)]
    d, m, _ = mountain_range("el", t, 850, 1200, 414, lithui, 19, t["mordor_far"], t["mordor_far_shade"], step=4, rough=2.6, gully_opacity=0.3, taper=(70, 0))
    defs.append(d)
    out.append(m)
    out.append(barad_dur(t, TOWER_X, TOWER_BASE, TOWER_SCALE))
    out.append(fell_beast(t, 1090, 244, 0.95))
    dd, dm = doom(t, DOOM_X, DOOM_TOP, DOOM_BASE)
    defs.append(dd)
    out.append(dm + plume(t, DOOM_X, DOOM_TOP))
    bd, bm = eye_beam(t, TOWER_X, TOWER_BASE - 150 * TOWER_SCALE)
    defs.append(bd)
    out.append(bm)
    out.append(mist_band(t, 404, 31, 8, 30))

    plain = hills(0, 1230, 428, 5, 17, step=30)
    out.append(f'<path d="{smooth_closed(plain)}" fill="{t["mid"]}"/>')
    flow, centre = river(t)
    out.append(flow)
    rx = [c[0] for c in centre]
    out.append(f'<g fill="{t["fir_far"]}">{forest([(x, y - 5) for x, y in plain], 470, 850, 23, [6, 9], 1.5, 0.15, [5], gap=(min(rx) - 8, max(rx) + 6))}</g>')
    out.append(f'<g fill="{t["fir_mid"]}">{forest(plain, 500, 835, 29, [9, 12, 16], 1.0, 0.3, [5, 7], gap=(820, 900))}</g>')

    ephel = [(918, 12, 26), (948, 26, 24), (1002, 24, 24), (1034, 30, 36), (1078, 18, 28), (1122, 26, 38), (1168, 20, 32), (1210, 28, 40)]
    d, m, _ = mountain_range("ed", t, 830, 1200, 452, ephel, 41, t["mordor_near"], t["mordor_near_shade"], step=3, rough=1.8, gully_opacity=0.35, taper=(80, 0))
    defs.append(d)
    out.append(m)
    out.append(black_gate(t, 975, 449))

    shire_defs, fields, homes = shire_layer(t)
    defs.append(shire_defs)
    out.append(fields)
    out.append(mist_band(t, 440, 37, 6, 42))
    out.append(homes)
    out.append(cart(t, 336, 469))
    if dark:
        out.append(fireflies(t, 3, (120, 420, 520, 470), 12))

    near = hills(440, 1230, 470, 4, 83, step=30, shape=lambda x: -smoothstep(560, 760, x) * 6 * (1 - smoothstep(820, 900, x)))
    gx = [c for c in centre if 455 < c[1] < 466][0]
    out.append(gollum(t, n(gx[0] + gx[2] / 2 + 12), n(gx[1] + 1)))
    out.append(f'<g fill="{t["fir_near"]}">{forest(near, 560, 980, 47, [16, 21, 28, 36], 0.55, 0.25, [7, 10], sink=4, gap=(800, 905))}</g>')

    front = hills(-20, 1230, 478, 3, 29, step=30)
    rnd = random.Random(91)
    tufts = "".join(
        f"M{n(x)} {n(at(front, x) + 2)}l{n(rnd.uniform(-1.5, -0.4))} {n(-rnd.uniform(3, 6))}m{n(rnd.uniform(1, 2))} {n(rnd.uniform(1, 3))}l{n(rnd.uniform(0.3, 1.5))} {n(-rnd.uniform(3, 5))}"
        for x in [rnd.uniform(0, 1200) for _ in range(110)]
    )
    out.append(f'<path d="{smooth_closed(front)}" fill="{t["front"]}"/><path d="{tufts}" stroke="{t["front"]}" stroke-width=".9" fill="none" stroke-linecap="round"/>')
    out.append(sting(t, 612, 476))
    return "".join(defs), "\n".join(out)
