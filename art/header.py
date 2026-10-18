from datetime import date
from pathlib import Path

from fonts import COURIER, FRAUNCES_BOLD, FRAUNCES_ITALIC, FRAUNCES_MEDIUM, RUNES, face, runes
from land import scene
from onering import one_ring, reveal
from themes import THEMES

VERSE = "ONE TYPE TO RULE THEM ALL, ONE BUILD TO SHIP THEM, ONE REPO TO BRING THEM ALL AND IN CLEAN CODE BIND THEM"

NAME = "Axel Hamilcaro"
STATUS = "OPEN TO FREELANCE · TOURS, FRANCE · REMOTE"
HEAD_ACCENT = "Fullstack"
HEAD_REST = " developer"
LINE = "ship fast, keep it clean, don't let it rot"
STACK = "React · Next.js · TypeScript · Node"
CAPTION_LINES = ("One type to rule them all, one build to ship them,", "One repo to bring them all, and in clean code bind them.")
CAPTION = " ".join(CAPTION_LINES)

W, H = 1200, 480
CX, CY, R, BAND = 975, 150, 120, 30
CAPTION_Y = 282


def caption_spans():
    out, i = [], 0
    for line, dy in zip(CAPTION_LINES, ("0", "19")):
        for j, word in enumerate(line.split(" ")):
            lead = f' x="{CX}" dy="{dy}"' if j == 0 else ""
            out.append(f'<tspan{lead} class="cw" style="animation-delay:{reveal(i):.2f}s">{word}{" " if j < len(line.split(" ")) - 1 else ""}</tspan>')
            i += 1
    return "".join(out)


def svg(t, inscription, fonts_dir, day):
    faces = (
        face(fonts_dir, FRAUNCES_BOLD, HEAD_ACCENT + HEAD_REST)
        + face(fonts_dir, FRAUNCES_MEDIUM, NAME)
        + face(fonts_dir, FRAUNCES_ITALIC, CAPTION)
        + face(fonts_dir, COURIER, STATUS + LINE + STACK)
        + face(fonts_dir, RUNES, inscription)
    )
    defs, land = scene(t, day)
    ring_defs, ring = one_ring(t, inscription, CX, CY, R, BAND)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">{NAME}, fullstack developer. Open to freelance work.</title>
<defs>
{defs}
{ring_defs}
</defs>
<style>
{faces}
.serif{{font-family:Fraunces,Georgia,serif;}}
.mono{{font-family:Courier,'Courier New',monospace;}}
.heat{{opacity:0;animation:heat 2.4s ease-in 0.6s forwards;}}
.glow{{opacity:0;animation:glow 2.4s ease-in 0.6s forwards;}}
.rw{{animation:rw 1.4s ease-out both;}}
.cw{{animation:cw 2.4s ease-out both;}}
@keyframes rw{{0%{{fill-opacity:0;stroke-opacity:0}}100%{{fill-opacity:1;stroke-opacity:1}}}}
@keyframes cw{{0%{{fill-opacity:0;fill:{t["brand"]}}}35%{{fill-opacity:1;fill:{t["brand"]}}}100%{{fill-opacity:1;fill:{t["muted"]}}}}}
.caption{{font-family:FrauncesItalic,Georgia,serif;font-style:normal;}}
.mist{{animation:drift 28s ease-in-out infinite alternate;}}

@keyframes drift{{to{{transform:translateX(-60px)}}}}
.spin{{transform-origin:0 0;animation:spin 120s linear infinite;}}
.dot{{animation:pulse 2s ease-in-out infinite;}}
@keyframes heat{{to{{opacity:1}}}}
.glint{{opacity:0;transform-box:fill-box;transform-origin:center;animation:glint 11s ease-in-out 4s infinite;}}
@keyframes glint{{0%{{opacity:0;transform:scale(.2) rotate(0)}}4%{{opacity:1;transform:scale(1) rotate(45deg)}}9%,100%{{opacity:0;transform:scale(.2) rotate(90deg)}}}}
@keyframes glow{{60%{{opacity:.7}}to{{opacity:.35}}}}
@keyframes spin{{to{{transform:rotate(-360deg)}}}}
@keyframes pulse{{50%{{opacity:.35}}}}
@media (prefers-reduced-motion:reduce){{.rw,.cw{{animation:none}}.heat{{animation:none;opacity:1}}.glow{{animation:none;opacity:.35}}.spin,.dot,.mist,.glint{{animation:none}}}}
</style>
{land}

<rect x="72" y="62" width="{len(STATUS) * 9.0 + 52:.0f}" height="34" rx="6" fill="none" stroke="{t["border"]}"/>
<circle class="dot" cx="92" cy="79" r="4.5" fill="{t["ok"]}"/>
<text class="mono" x="106" y="84" font-size="15" letter-spacing="0" fill="{t["muted"]}">{STATUS}</text>
<text class="serif" x="72" y="152" font-size="28" font-weight="500" fill="{t["muted"]}">{NAME}</text>
<text class="serif" x="68" y="232" font-size="70" font-weight="700" letter-spacing="-1.2" fill="{t["ink"]}"><tspan fill="{t["brand"]}">{HEAD_ACCENT}</tspan>{HEAD_REST}</text>
<text class="mono" x="72" y="290" font-size="20" fill="{t["ink"]}">{LINE}</text>
<text class="mono" x="72" y="326" font-size="17" fill="{t["muted"]}">{STACK}</text>

{ring}
<text class="caption" x="{CX}" y="{CAPTION_Y}" text-anchor="middle" font-size="14.5" fill="{t["muted"]}">{caption_spans()}</text>
</svg>
"""


def build(fonts_dir, out_dir, day=None):
    day = day or date.today()
    inscription = runes(VERSE)
    for name, theme in THEMES.items():
        (Path(out_dir) / f"header-{name}.svg").write_text(svg(theme, inscription, fonts_dir, day))
