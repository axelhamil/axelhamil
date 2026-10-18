import random

from geo import n

STYLE = """
.flap{animation:flap 2.8s ease-in-out infinite}
@keyframes flap{0%,36%,100%{transform:scaleY(.45)}3%,11%,19%,27%{transform:scaleY(1.7)}7%,15%,23%,31%{transform:scaleY(-1.3)}}
.bob{animation:bob 4s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translate(0,0) rotate(0)}30%{transform:translate(2px,-2.6px) rotate(-6deg)}65%{transform:translate(-1.5px,1.8px) rotate(5deg)}}
.migrate{animation:migrate 64s cubic-bezier(.35,.1,.65,.9) 4s infinite}
@keyframes migrate{0%{transform:translate(0,0)}22%{transform:translate(-300px,10px)}45%{transform:translate(-640px,-6px)}70%{transform:translate(-1010px,12px)}100%{transform:translate(-1480px,0)}}
.eflap{animation:eflap 12s ease-in-out infinite}
@keyframes eflap{0%,22%,100%{transform:scale(1,1)}4%,12%{transform:scale(.88,-.75)}8%,16%{transform:scale(1,1.25)}}
.soar{animation:soar 28s ease-in-out infinite}
@keyframes soar{0%,100%{transform:translate(0,0) rotate(0)}24%{transform:translate(-20px,5px) rotate(-9deg)}46%{transform:translate(-5px,10px) rotate(3deg)}74%{transform:translate(17px,3px) rotate(10deg)}}
.bflap{animation:bflap 9s ease-in-out infinite}
@keyframes bflap{0%,40%,100%{transform:scaleY(1)}10%,30%{transform:scaleY(-.55)}20%{transform:scaleY(1.08)}}
.heave{animation:heave 9s ease-in-out infinite}
@keyframes heave{0%,40%,100%{transform:translateY(0)}10%,30%{transform:translateY(-1.6px)}20%{transform:translateY(.8px)}}
.circle{animation:circle 40s ease-in-out infinite}
@keyframes circle{0%,100%{transform:translate(0,0) rotate(0)}20%{transform:translate(-30px,4px) rotate(-7deg)}38%{transform:translate(-40px,9px) rotate(-2deg)}55%{transform:translate(-10px,13px) rotate(6deg)}78%{transform:translate(24px,5px) rotate(9deg)}}
"""

ANIMATED = ".flap,.bob,.migrate,.eflap,.soar,.bflap,.heave,.circle"


def timing(duration, delay):
    return f'style="animation-duration:{duration:.2f}s;animation-delay:{delay:.2f}s"'


def flock(color, x, y, birds, seed, width=0.9):
    rnd = random.Random(seed)
    v = "M-3 -1.2Q-1.4 -1.6 0 0Q1.4 -1.6 3 -1.2"
    out = []
    for dx, dy, s in birds:
        bob = timing(rnd.uniform(3.2, 5.2), -rnd.uniform(0, 5))
        flap = timing(rnd.uniform(2.4, 3.4), -rnd.uniform(0, 3))
        out.append(
            f'<g transform="translate({n(dx)} {n(dy)}) scale({n(s)})"><g class="bob" {bob}>'
            f'<path class="flap" {flap} d="{v}" vector-effect="non-scaling-stroke"/></g></g>'
        )
    return (
        f'<g transform="translate({x} {y})"><g class="migrate" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round">'
        + "".join(out) + "</g></g>"
    )


def eagle(t, x, y, s, soar, flap):
    wings = (
        "M0 0C-4 -2.2 -9 -3.2 -15 -1.4L-13.4 -.4L-15 .5L-12.6 .7L-13.6 1.8L-9.4 1.4C-5.6 1.7 -3 1.6 0 1.6"
        "C3 1.6 5.6 1.7 9.4 1.4L13.6 1.8L12.6 .7L15 .5L13.4 -.4L15 -1.4C9 -3.2 4 -2.2 0 0Z"
    )
    body = "M0 -1.6C1 -1.6 1.4 -.4 1.3 1.4L1.8 4.4L0 6L-1.8 4.4L-1.3 1.4C-1.4 -.4 -1 -1.6 0 -1.6Z"
    return (
        f'<g transform="translate({x} {y})"><g class="soar" {timing(*soar)}><g transform="scale({s})" fill="{t["eagle"]}">'
        f'<path class="eflap" {timing(*flap)} d="{wings}"/><path d="{body}"/></g></g></g>'
    )


def fell_beast(t, x, y, s):
    wing_far = "M2 0C3 -4 6 -8 10 -9L9 -6.5L11 -5.5L8.5 -4L9.5 -2.5L6 -1.5C5 -.8 3.5 0 2 0Z"
    wing_near = "M0 0C-3 -5 -9 -11 -16 -12L-13.5 -8.5L-16 -7L-12 -5.5L-13.5 -3.2L-8.5 -2.6L-9 -.8L-4 -.4C-2.5 .1 -1 .2 0 0Z"
    body = "M-8 .5Q-11 -.6 -13 1.2L-12.6 1.8Q-11 .6 -8 1.6Q-3 2.2 2 1.6Q7 1.8 12 3.4Q8 1 3 -.2Q-2 -.6 -8 .5Z"
    rider = "M-1.2 -.2L-.6 -4.4L.3 -4.8L.9 -.2Z"
    return (
        f'<g transform="translate({x} {y})"><g class="circle"><g transform="scale({s})" fill="{t["beast"]}"><g class="heave">'
        f'<g transform="translate(0 -1)"><path class="bflap" style="animation-delay:-.35s" d="{wing_far}" opacity=".8"/></g>'
        f'<path d="{body}"/><path d="{rider}"/>'
        f'<g transform="translate(-1 -1)"><path class="bflap" d="{wing_near}"/></g>'
        "</g></g></g></g>"
    )
