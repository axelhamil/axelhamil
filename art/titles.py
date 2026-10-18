from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

from fonts import COURIER, FRAUNCES_TITLE, RUNES, face
from themes import THEMES

TITLES = {
    "quests": ("Quests", "experience"),
    "forge": ("The Forge", "private projects, real code"),
    "artifacts": ("Artifacts", "open source libraries and starters"),
    "palantiri": ("Palantíri", "Claude Code tooling"),
    "shire": ("The Shire", "home setup"),
}

W, H = 640, 60
SIZE = 34


def title_width(fonts_dir, text):
    _, file, axes, _ = FRAUNCES_TITLE
    font = instancer.instantiateVariableFont(TTFont(Path(fonts_dir) / file), axes)
    cmap, hmtx, upm = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
    return sum(hmtx[cmap[ord(c)]][0] for c in text) / upm * SIZE


def svg(t, fonts_dir, title, label):
    faces = face(fonts_dir, FRAUNCES_TITLE, title) + face(fonts_dir, COURIER, label) + face(fonts_dir, RUNES, "᛭")
    label_x = 34 + title_width(fonts_dir, title) + 18
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}: {label}">
<style>{faces}</style>
<text x="0" y="40" font-family="Runes,serif" font-size="22" fill="{t["brand"]}">᛭</text>
<text x="32" y="40" font-family="Fraunces,Georgia,serif" font-weight="700" font-size="{SIZE}" fill="{t["ink"]}">{title}</text>
<text x="{label_x:.0f}" y="39" font-family="Courier,monospace" font-size="16" fill="{t["muted"]}">{label}</text>
<line x1="0" y1="56" x2="{W}" y2="56" stroke="{t["border"]}" stroke-width="1.5"/>
</svg>
"""


def build(fonts_dir, out_dir):
    out = Path(out_dir) / "titles"
    out.mkdir(parents=True, exist_ok=True)
    for slug, (title, label) in TITLES.items():
        for name, theme in THEMES.items():
            (out / f"{slug}-{name}.svg").write_text(svg(theme, fonts_dir, title, label))
