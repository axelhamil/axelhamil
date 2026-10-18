import math
import random
from datetime import date

from geo import n, poly
from mountains import mountain_range

TOWER_HALF = [
    (12.5, -151), (12, -143), (9.5, -137), (11, -135), (11, -131), (13, -130), (13, -126), (10, -124),
    (10.5, -104), (13.5, -102), (13.5, -98), (12.5, -97), (14.5, -74), (17.5, -72), (17.5, -68), (16.5, -67),
    (19, -48), (22, -46), (23, -42), (33, -51), (27, -34), (30, -26), (44, -33), (34, -16), (38, -8), (48, -11), (41, 0),
]
HORN_INNER = [(0, -140), (4, -142), (6, -146), (8.5, -152), (11, -160)]


def barad_dur(t, x, base, s):
    right = HORN_INNER + TOWER_HALF
    left = [(-px, py) for px, py in right][::-1]
    outline = poly(right + left[:-1])
    shade = poly([(0, -140)] + right[1:] + [(0, 0)])
    ribs = "".join(f"M{n(rx)} -122V{n(y1)}" for rx, y1 in [(-5, -20), (0, -30), (4.5, -18), (-9.5, -60), (9, -64)])
    rim = "M-11 -160L-12.5 -151L-12 -143L-9.5 -137L-11 -135L-11 -131L-13 -130L-13 -126L-10 -124L-10.5 -104L-13.5 -102L-13.5 -98L-12.5 -97L-14.5 -74L-17.5 -72L-17.5 -68L-16.5 -67L-19 -48"
    tower = (
        f'<g transform="translate({n(x)} {n(base)}) scale({s})">'
        f'<path d="{outline}" fill="{t["tower"]}"/>'
        f'<path d="{shade}" fill="#000" opacity=".22"/>'
        f'<path d="{ribs}" stroke="{t["tower_edge"]}" stroke-width=".9" opacity=".7"/>'
        f'<path class="heat" d="{rim}" fill="none" stroke="{t["brand"]}" stroke-width="1.3" opacity=".55"/>'
        "</g>"
    )
    ex, ey = x, base - 150 * s
    eye = (
        f'<g class="heat"><circle class="eye" cx="{n(ex)}" cy="{n(ey)}" r="{n(26 * s)}" fill="url(#eyehalo)"/>'
        f'<path d="M{n(ex - 6.5 * s)} {n(ey)}Q{n(ex)} {n(ey - 3.6 * s)} {n(ex + 6.5 * s)} {n(ey)}Q{n(ex)} {n(ey + 3.6 * s)} {n(ex - 6.5 * s)} {n(ey)}Z" fill="url(#eyeball)"/>'
        f'<path d="M{n(ex)} {n(ey - 3 * s)}Q{n(ex + 1 * s)} {n(ey)} {n(ex)} {n(ey + 3 * s)}Q{n(ex - 1 * s)} {n(ey)} {n(ex)} {n(ey - 3 * s)}Z" fill="#1A0602" class="pupil"/></g>'
    )
    return tower + eye


def eye_defs(t):
    return (
        f'<radialGradient id="eyehalo"><stop offset="0" stop-color="{t["window"]}" stop-opacity=".95"/>'
        f'<stop offset=".25" stop-color="{t["brand"]}" stop-opacity=".55"/><stop offset="1" stop-color="{t["brand"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="eyeball"><stop offset="0" stop-color="{t["glyph"]}"/><stop offset=".45" stop-color="{t["window"]}"/>'
        f'<stop offset="1" stop-color="{t["brand"]}"/></radialGradient>'
    )


def doom(t, dx, top, base):
    outline = (
        f"M{dx - 140} {base}C{dx - 95} {base - 8} {dx - 62} {base - 22} {dx - 44} {base - 34}"
        f"C{dx - 30} {base - 45} {dx - 20} {top + 22} {dx - 14} {top}"
        f"L{dx - 8} {top - 2}L{dx - 3} {top + 2}L{dx + 4} {top + 1}L{dx + 9} {top - 1}L{dx + 14} {top + 1}"
        f"C{dx + 20} {top + 24} {dx + 32} {base - 42} {dx + 48} {base - 31}"
        f"C{dx + 72} {base - 14} {dx + 102} {base - 6} {dx + 140} {base}Z"
    )
    wedge = poly([(dx + 3, top - 4), (dx + 8, top + 20), (dx + 16, top + 44), (dx + 26, base - 20), (dx + 30, base + 4), (dx + 160, base + 4), (dx + 160, top - 4)])
    shoulder = poly([(dx - 44, base - 34), (dx - 52, base - 22), (dx - 70, base - 10), (dx - 100, base), (dx - 40, base), (dx - 36, base - 18)])
    road = f"M{dx - 70} {base - 6}L{dx - 30} {base - 22}L{dx - 46} {base - 30}L{dx - 22} {top + 44}L{dx - 6} {top + 30}L{dx + 9} {top + 18}"
    lava = (
        f"M{dx - 6} {top + 1}C{dx - 12} {top + 20} {dx - 3} {top + 36} {dx - 16} {top + 60}"
        f"M{dx - 11} {top + 2}C{dx - 18} {top + 16} {dx - 22} {top + 30} {dx - 32} {top + 44}"
        f"M{dx + 2} {top + 2}C{dx + 4} {top + 14} {dx} {top + 22} {dx + 4} {top + 34}"
    )
    defs = (
        f'<clipPath id="doomclip"><path d="{outline}"/></clipPath>'
        f'<radialGradient id="ember"><stop offset="0" stop-color="{t["window"]}"/><stop offset=".35" stop-color="{t["brand"]}" stop-opacity=".8"/>'
        f'<stop offset="1" stop-color="{t["brand"]}" stop-opacity="0"/></radialGradient>'
    )
    out = (
        f'<path d="{outline}" fill="{t["doom"]}"/>'
        f'<g clip-path="url(#doomclip)"><path d="{wedge}" fill="{t["doom_shade"]}"/><path d="{shoulder}" fill="#000" opacity=".12"/>'
        f'<path d="{road}" fill="none" stroke="{t["doom_road"]}" stroke-width=".8" opacity=".7"/></g>'
        f'<g class="heat"><g class="flick"><path d="{lava}" fill="none" stroke="{t["brand"]}" stroke-width="4" opacity=".25" stroke-linecap="round"/>'
        f'<path d="{lava}" fill="none" stroke="{t["brand"]}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<path d="{lava}" fill="none" stroke="{t["window"]}" stroke-width=".5" stroke-linecap="round"/></g>'
        f'<ellipse cx="{dx}" cy="{top + 1}" rx="30" ry="13" fill="url(#ember)"/>'
        f'<rect x="{dx + 9.5}" y="{top + 17}" width="2.2" height="2" fill="{t["window"]}"/></g>'
    )
    return defs, out


def plume(t, dx, top):
    puffs = [(-4, 9, 0), (6, 12, 3), (0, 8, 6), (10, 10, 9)]
    return "".join(
        f'<circle class="ash" cx="{dx + ox}" cy="{top - 8}" r="{r}" fill="url(#puff)" style="animation-delay:{d}s"/>'
        for ox, r, d in puffs
    )


def minas_tirith(t, x, base):
    defs, mount, _ = mountain_range("mdl", t, x - 96, x + 84, base + 2, [(x - 20, 92, 84), (x + 26, 58, 66), (x - 62, 40, 40)], 23,
                                    t["mindolluin"], t["mindolluin_shade"], (t["snow"], t["snow_shade"]), 0.22, 50, step=4, rough=1.6, taper=(30, 30))
    slabs, lights = [], []
    rnd = random.Random(17)
    for k in range(6, -1, -1):
        hw, wall, step = 31 - 3.2 * k, 2.8, 4.3
        ry = hw * 0.13
        c = base - 31 * 0.13 - wall - step * k
        terrace = f"M{n(x - hw)} {n(c)}A{n(hw)} {n(ry)} 0 0 0 {n(x + hw)} {n(c)}V{n(c - step + wall)}A{n(hw)} {n(ry)} 0 0 1 {n(x - hw)} {n(c - step + wall)}Z"
        face = f"M{n(x - hw)} {n(c)}A{n(hw)} {n(ry)} 0 0 0 {n(x + hw)} {n(c)}V{n(c + wall)}A{n(hw)} {n(ry)} 0 0 1 {n(x - hw)} {n(c + wall)}Z"
        lip = f"M{n(x - hw)} {n(c)}A{n(hw)} {n(ry)} 0 0 0 {n(x + hw)} {n(c)}"
        slabs.append(
            f'<path d="{terrace}" fill="{t["city_roof"]}"/><path d="{face}" fill="url(#cityg)"/>'
            f'<path d="{lip}" fill="none" stroke="{t["city_shade"]}" stroke-width=".45" stroke-dasharray=".5 .7"/>'
        )
        for frac in sorted(rnd.sample([-0.75, -0.5, -0.25, 0.25, 0.5, 0.75], 2)):
            dx = hw * frac
            sag = ry * (1 - frac * frac) ** 0.5
            lights.append(f'<rect x="{n(x + dx - 0.25)}" y="{n(c + sag + wall * 0.35)}" width=".5" height=".8"/>')
    top = base - 31 * 0.13 - 2.8 - 4.3 * 6
    prow = f"M{x - 2.4} {top + 0.6}L{x + 2.4} {top + 0.6}L{x + 0.9} {base - 9}L{x} {base - 7.4}L{x - 0.9} {base - 9}Z"
    prow_shade = f"M{x} {top + 0.6}L{x + 2.4} {top + 0.6}L{x + 0.9} {base - 9}L{x} {base - 7.4}Z"
    tower = poly([(x - 1.3, top + 1), (x - 0.9, top - 12), (x - 1.3, top - 12.5), (x - 0.5, top - 13.6), (x, top - 17), (x + 0.5, top - 13.6),
                  (x + 1.3, top - 12.5), (x + 0.9, top - 12), (x + 1.3, top + 1)])
    pelennor = f"M{x - 90} {base + 6}C{x - 60} {base} {x - 40} {base} {x} {base}C{x + 40} {base} {x + 60} {base} {x + 90} {base + 6}Z"
    return (
        defs + f'<linearGradient id="cityg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["city"]}"/><stop offset=".55" stop-color="{t["city"]}"/>'
        f'<stop offset="1" stop-color="{t["city_shade"]}"/></linearGradient>'
        f'<radialGradient id="beaconglow"><stop offset="0" stop-color="{t["glow"]}" stop-opacity=".6"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>',
        mount + "".join(slabs)
        + f'<path d="M{x - 1.2} {base - 0.4}V{base - 1.8}a1.2 1.2 0 0 1 2.4 0V{base - 0.4}Z" fill="#000" opacity=".4"/>'
        f'<path d="{prow}" fill="{t["city"]}"/><path d="{prow_shade}" fill="{t["city_shade"]}"/>'
        f'<path d="{tower}" fill="url(#cityg)"/><path d="M{x} {top - 17}v-3.2" stroke="{t["city_shade"]}" stroke-width=".35"/>'
        f'<g transform="translate({x} {top - 20.1})"><path class="pennant" d="M0 0L4.6 .6L0 1.3Z" fill="{t["city"]}" stroke="{t["city_shade"]}" stroke-width=".2"/></g>'
        f'<g fill="{t["window"]}" opacity="{t["city_lights"]}">{"".join(lights)}</g>'
        f'<path d="{pelennor}" fill="{t["far2"]}"/>',
    )


def beacon(t, x, y):
    return (
        f'<g class="heat"><circle cx="{x}" cy="{y}" r="7" fill="url(#beaconglow)"/>'
        f'<path class="beacon" d="M{x - 1.1} {y + 0.6}Q{x - 0.8} {y - 1.4} {x} {y - 2.6}Q{x + 0.8} {y - 1.4} {x + 1.1} {y + 0.6}Z" fill="{t["brand"]}"/></g>'
    )


def orthanc(t, x, base):
    left = [(-5.2, 0), (-4.1, -2.6), (-3.3, -7), (-3, -27), (-3.3, -29.5), (-4.7, -38), (-2.2, -31.2), (-1.1, -36), (-0.5, -31.6)]
    tower = poly(left + [(-px, py) for px, py in left[::-1]])
    shade = poly([(0, -31.6), (0.5, -31.6), (1.1, -36), (2.2, -31.2), (4.7, -38), (3.3, -29.5), (3, -27), (3.3, -7), (4.1, -2.6), (5.2, 0), (0, 0)])
    ribs = "".join(f"M{dx} -3.5V-28" for dx in (-1.6, 0, 1.6))
    knoll = "M-10 2.5C-7 -1.2 -4 -.8 0 -.8C4 -.8 7 -1.2 10 2.5Z"
    ox, oy, ix, iy = 30, 6.4, 28, 5.4
    wall_top = f"M{-ox} 0A{ox} {oy} 0 1 1 {ox} 0A{ox} {oy} 0 1 1 {-ox} 0Z"
    plain = f"M{-ix} 0A{ix} {iy} 0 1 1 {ix} 0A{ix} {iy} 0 1 1 {-ix} 0Z"
    face = f"M{-ox} 0A{ox} {oy} 0 0 0 {ox} 0V3.4A{ox} {oy} 0 0 1 {-ox} 3.4Z"
    inner_face = f"M{-ix} 0A{ix} {iy} 0 0 1 {ix} 0V1.8A{ix} {iy - 0.6} 0 0 0 {-ix} 1.8Z"
    pits = "".join(f'<ellipse cx="{dx}" cy="{dy}" rx="{rx}" ry="{n(rx * 0.4)}"/>' for dx, dy, rx in [(-17, 1, 1.6), (-12, -2.6, 1.2), (13, -2.2, 1.4), (17, 1.4, 1.8), (-7, 3, 1.1), (8, 3.2, 1.3), (-20, -1.2, 0.9)])
    forges = [(-15, 1.6), (12, -1.6), (18, 1.8)]
    glows = "".join(f'<circle cx="{dx}" cy="{dy}" r="3.2" fill="url(#forge)"/><circle cx="{dx}" cy="{dy}" r=".5" fill="{t["brand"]}"/>' for dx, dy in forges)
    smoke = "".join(f'<circle class="puff" cx="{dx + 0.5}" cy="{dy - 3}" r="1.6" fill="url(#puff)" style="animation-delay:{d}s;animation-duration:{u}s"/>'
                    for (dx, dy), d, u in zip(forges * 2, [0, 2.4, 4.1, 5.3, 1.2, 6.6], [7, 8.5, 7.6, 9, 8, 7.2]))
    return (
        f'<radialGradient id="forge"><stop offset="0" stop-color="{t["brand"]}" stop-opacity=".55"/><stop offset="1" stop-color="{t["brand"]}" stop-opacity="0"/></radialGradient>',
        f'<g transform="translate({x} {base})">'
        f'<path d="{wall_top}" fill="{t["isen_wall"]}"/><path d="{plain}" fill="{t["isen_plain"]}"/><path d="{inner_face}" fill="{t["isen_face"]}" opacity=".8"/>'
        f'<g fill="#000" opacity=".22">{pits}</g><g class="heat">{glows}</g>{smoke}'
        f'<path d="{knoll}" fill="{t["isen_wall"]}"/>'
        f'<path d="{tower}" fill="{t["orthanc"]}"/><path d="{shade}" fill="#000" opacity=".28"/>'
        f'<path d="{ribs}" stroke="{t["isen_rib"]}" stroke-width=".4" opacity=".7"/>'
        f'<circle class="tw" cx="0" cy="-32.6" r=".7" fill="{t["spark"]}" style="animation-duration:4.5s"/>'
        f'<path d="{face}" fill="{t["isen_face"]}"/></g>',
    )


def black_gate(t, x, base):
    cliff = poly([(-40, 1), (-33, -8), (-30, -17), (-27, -21), (-24, -22.5), (-20.5, -21), (-18.5, -15), (-17, -6), (-16.5, 1)])
    cliff_r = poly([(16.5, 1), (17.2, -7), (18.6, -16), (21, -21.5), (24.5, -23), (27.5, -21), (30, -16), (34, -9), (42, 1)])
    merlons = [(k + dx, -12 - up) for k in range(-17, 17, 2) for dx, up in [(0, 1.1), (1, 1.1), (1, 0), (2, 0)]]
    wall = poly([(-17.5, 1), (-17.5, -12)] + merlons + [(17.5, -12), (17.5, 1)])
    doors = "".join(f"M{dx} 0V-6.2A4 4.2 0 0 1 {dx + 8} -6.2V0Z" for dx in (-9, 1))
    bars = "".join(f"M{dx + k * 1.6} 0V-8" for dx in (-9, 1) for k in range(1, 5))
    spikes = "".join(f"M{k} -12.6V-14.4" for k in range(-16, 17, 4))
    tower = poly([(-2.8, 0), (-2.2, -15), (-2.9, -16), (-1.9, -17), (-2.3, -20.5), (-1, -18.6), (0, -23.5), (1, -18.6), (2.3, -20.5), (1.9, -17), (2.9, -16), (2.2, -15), (2.8, 0)])
    towers = "".join(f'<path transform="translate({tx} {ty})" d="{tower}"/>' for tx, ty in [(-23.5, -21.5), (24.5, -22)])
    slits = "".join(f'<rect x="{tx - 0.35}" y="{ty - 13}" width=".7" height="1.6"/>' for tx, ty in [(-23.5, -21.5), (24.5, -22)])
    return (
        f'<g transform="translate({x} {base})">'
        f'<path d="{cliff}{cliff_r}" fill="{t["mordor_near_shade"]}"/>'
        f'<g fill="{t["gate"]}"><path d="{wall}"/>{towers}</g>'
        f'<path d="{spikes}" stroke="{t["gate"]}" stroke-width=".4"/>'
        f'<path d="{doors}" fill="#000" opacity=".5"/><path d="{bars}" stroke="{t["tower_edge"]}" stroke-width=".35" opacity=".8"/>'
        f'<path d="M-1 0V-8.6M1 0V-8.6" stroke="{t["gate"]}" stroke-width="1"/>'
        f'<g class="heat" fill="{t["window"]}">{slits}</g></g>'
    )


def gollum(t, x, base):
    rock = "M-11 1.6C-9.6 -1.4 -5.6 -1.8 -1 -1.6C4 -1.6 8 -1.2 10 1.6Z"
    spine = "M5 -3.6C5.6 -8.8 1.2 -10 -1.6 -7.8C-2.8 -6.8 -3.4 -6 -4.2 -5.4"
    head = "M-3.4 -5.8C-3.6 -8.4 -6.6 -9.4 -8.6 -7.8C-10.2 -6.6 -9.8 -4 -8.2 -3.4C-7 -3 -6 -3.6 -5.2 -4C-4.2 -4.4 -3.3 -4.6 -3.4 -5.8Z"
    ears = "M-3.8 -6.6L-2.9 -6.9L-3.6 -6.1"
    hair = "M-6.4 -9C-5.2 -9.2 -4 -8.4 -3.4 -6.6M-5.4 -9C-4.4 -8.8 -3.8 -8 -3.7 -7.4M-7.4 -8.8C-7.8 -9.4 -8.4 -9.4 -8.8 -9"
    hind = "M4.4 -4C6.2 -7.6 6.8 -9.6 6.4 -10.2C7.4 -6.4 7.8 -2.8 7.4 -1.6L9.6 -1.6"
    arm = "M-2.2 -5.6C-2.4 -7.8 -3.2 -9.4 -3.6 -9.4C-4.6 -6.6 -6.8 -3.4 -8.4 -1.8L-10 -1.6"
    arm_far = "M0 -5.4C.2 -7.8 -.6 -8.8 -1 -8.8C-2 -6 -3.6 -3.2 -4.8 -1.8L-6 -1.6"
    hind_far = "M3 -4.4C4.2 -7.2 4.8 -8.6 4.4 -9.2C5.6 -6 5.8 -3.2 5.4 -1.7L7 -1.6"
    fish = "M-10.4 -2.2C-11.4 -3.4 -12.8 -3.4 -13.6 -2.6L-14.6 -3.4L-14.4 -1.8L-13.6 -2C-12.8 -1.2 -11.4 -1.2 -10.4 -2.2Z"
    eye = 'class="blink" r=".78"'
    return (
        f'<g transform="translate({x} {base}) scale(1.3)">'
        f'<g class="rip" fill="none" stroke="{t["ripple"]}" stroke-width=".35"><ellipse cx="-17" cy="2.6" rx="4" ry=".9"/><ellipse cx="-17" cy="2.6" rx="7" ry="1.5" style="animation-delay:-2.2s"/></g>'
        f'<path d="{rock}" fill="{t["rock"]}"/>'
        f'<g fill="none" stroke="{t["gollum"]}" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="{arm_far}{hind_far}" stroke-width=".5" opacity=".75"/>'
        f'<path d="{spine}" stroke-width="1.7"/>'
        f'<path d="{hind}{arm}" stroke-width=".62"/><path d="{hair}" stroke-width=".25"/><path d="{ears}" stroke-width=".4"/></g>'
        f'<path d="{head}" fill="{t["gollum"]}"/><path d="{fish}" fill="{t["fish"]}"/>'
        f'<circle {eye} cx="-8" cy="-5.6" fill="{t["gollum_eye"]}"/><circle {eye} cx="-5.8" cy="-5.8" fill="{t["gollum_eye"]}"/>'
        f'<g class="blink" fill="#fff"><circle cx="-8.25" cy="-5.85" r=".22"/><circle cx="-6.05" cy="-6.05" r=".22"/></g>'
        "</g>"
    )


def hole_symbol(t):
    planks = "M-3.6 -6.2V6.2M0 -7.2V7.2M3.6 -6.2V6.2"
    return (
        f'<g id="hole"><circle r="9" fill="{t["stone"]}"/><circle r="7.4" fill="{t["door"]}"/>'
        f'<path d="{planks}" stroke="#000" stroke-width=".5" opacity=".25"/>'
        f'<circle r="1" fill="{t["window"]}"/><path d="M-9 7.4h18v1.8h-18Z" fill="{t["stone"]}"/></g>'
        f'<g id="win"><circle r="3.6" fill="{t["stone"]}"/><circle r="2.7" fill="{t["window"]}"/>'
        f'<path d="M-2.7 0h5.4M0 -2.7v5.4" stroke="{t["stone"]}" stroke-width=".6"/></g>'
    )


def cart(t, x, y):
    return (
        f'<g transform="translate({x} {y})">'
        f'<path d="M-24 -3.5l3.5-1.5l4 -.2l1.5-4l1.2 0l-.6 4.2l3 .8l1 3.4h-1.2l-.6-2.6l-2.2 -.4v2.8h-1.2v-2.8l-5.6.2v2.6h-1.2v-2.6l-1.6-.4Z" fill="{t["horse"]}"/>'
        f'<path d="M-11 -3h-1.2" stroke="{t["horse"]}" stroke-width=".8"/>'
        f'<path d="M-12 -5.8h13v4.2h-13Z" fill="{t["cart"]}"/>'
        f'<circle cx="-8.5" cy="-1.2" r="2.5" fill="none" stroke="{t["cart"]}" stroke-width=".9"/><circle cx="-2" cy="-1.2" r="2.5" fill="none" stroke="{t["cart"]}" stroke-width=".9"/>'
        f'<path d="M-9 -5.8l1.4-4.6l2.6 0l1 4.6Z" fill="{t["gandalf"]}"/>'
        f'<path d="M-9.4 -10.2h6l-2.4-1.2l-1.2-4.8Z" fill="{t["gandalf"]}"/>'
        f'<path d="M-4 -5.8l1-2.2 2 .4l.4 1.8Z" fill="{t["window"]}" opacity=".9"/></g>'
    )


def firework(t, x, y):
    rays = "".join(
        f"M{n(math.cos(a) * 3)} {n(math.sin(a) * 3)}L{n(math.cos(a) * 9)} {n(math.sin(a) * 9)}"
        for a in [k * math.pi / 6 for k in range(12)]
    )
    sparks = "".join(f'<circle cx="{n(math.cos(a) * 11)}" cy="{n(math.sin(a) * 11)}" r=".7"/>' for a in [k * math.pi / 6 + 0.26 for k in range(12)])
    return (
        f'<g transform="translate({x} {y})"><g class="fw">'
        f'<path d="{rays}" stroke="{t["window"]}" stroke-width=".8" stroke-linecap="round"/>'
        f'<g fill="{t["glyph"]}">{sparks}</g><circle r="1.4" fill="{t["glyph"]}"/></g></g>'
        f'<path d="M{x} {y + 12}q-1 12 -3 26" fill="none" stroke="{t["muted"]}" stroke-width=".6" opacity=".35" stroke-dasharray="1.5 2"/>'
    )


def sting(t, x, y):
    return (
        f'<g transform="translate({x} {y}) rotate(8)">'
        f'<circle class="sting" cy="-7" r="9" fill="url(#stingglow)"/>'
        f'<path d="M-.7 -1V-13L0 -15L.7 -13V-1Z" fill="{t["sting"]}"/>'
        f'<path d="M-3 -1.2h6v1h-6Z" fill="{t["stone"]}"/><path d="M-.5 0h1v3h-1Z" fill="{t["stone"]}"/></g>'
    )


def stars(t, seed):
    rnd = random.Random(seed)
    out, twinkle = [], []
    tries = 0
    while len(out) + len(twinkle) < 90 and tries < 4000:
        tries += 1
        x, y = rnd.uniform(4, 1196), rnd.uniform(4, 300)
        behind_text = 60 < x < 720 and 40 < y < 345
        near_ring = (x - 975) ** 2 + ((y - 160) / 0.75) ** 2 < 175 ** 2
        caption = 850 < x < 1100 and 270 < y < 335
        if near_ring or caption:
            continue
        if behind_text and rnd.random() < 0.85:
            continue
        o = rnd.uniform(0.12, 0.3) if behind_text else rnd.uniform(0.25, 0.75) * (1 - y / 420)
        r = rnd.choice([0.5, 0.6, 0.7, 0.9]) if not behind_text else 0.5
        dot = f'<circle cx="{n(x)}" cy="{n(y)}" r="{r}" opacity="{o:.2f}"/>'
        if not behind_text and len(twinkle) < 7 and r >= 0.7:
            twinkle.append(f'<circle class="tw" cx="{n(x)}" cy="{n(y)}" r="{r + 0.2}" opacity="{o:.2f}" style="animation-delay:{rnd.uniform(0, 5):.1f}s"/>')
        else:
            out.append(dot)
    return f'<g fill="{t["star"]}">{"".join(out)}{"".join(twinkle)}</g>'


def moon_phase(day):
    synodic = 29.530588853
    return ((day - date(2000, 1, 6)).days - 0.76) / synodic % 1


def moon(t, x, y, r, day):
    phase = moon_phase(day)
    lit = (1 - math.cos(2 * math.pi * phase)) / 2
    if lit < 0.03:
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{t["star"]}" stroke-width=".5" opacity=".25"/>'
    if lit > 0.97:
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["star"]}" opacity=".7"/>'
    waxing = phase < 0.5
    rx = n(r * abs(1 - 2 * lit))
    limb = 1 if waxing else 0
    term = (0 if lit < 0.5 else 1) if waxing else (1 if lit < 0.5 else 0)
    d = f"M{x} {y - r}A{r} {r} 0 0 {limb} {x} {y + r}A{rx} {r} 0 0 {term} {x} {y - r}Z"
    return f'<path d="{d}" fill="{t["star"]}" opacity=".7"/>'

def eye_beam(t, ex, ey):
    cone = poly([(ex, ey), (ex - 300, ey + 64), (ex - 300, ey + 122)])
    return (
        f'<linearGradient id="beamg" gradientUnits="userSpaceOnUse" x1="{n(ex)}" y1="{n(ey)}" x2="{n(ex - 300)}" y2="{n(ey + 90)}">'
        f'<stop offset="0" stop-color="{t["window"]}" stop-opacity="{t["beam"]}"/><stop offset="1" stop-color="{t["window"]}" stop-opacity="0"/></linearGradient>',
        f'<g class="heat"><path class="beam" style="transform-origin:{n(ex)}px {n(ey)}px" d="{cone}" fill="url(#beamg)"/></g>',
    )


def fireflies(t, seed, area, count):
    rnd = random.Random(seed)
    return "".join(
        f'<circle class="ff" cx="{n(rnd.uniform(area[0], area[2]))}" cy="{n(rnd.uniform(area[1], area[3]))}" r=".9" fill="{t["firefly"]}" '
        f'style="animation-delay:{rnd.uniform(0, 8):.1f}s;animation-duration:{rnd.uniform(5, 9):.1f}s"/>'
        for _ in range(count)
    )


def clouds(t, seed, boxes):
    rnd = random.Random(seed)
    return "".join(
        f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="{n(rnd.uniform(60, 110))}" ry="{n(rnd.uniform(3, 6))}"/>' for x, y in boxes
    )
