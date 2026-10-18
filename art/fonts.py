import base64
import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FUTHORC = {
    "TH": "ᚦ", "A": "ᚪ", "B": "ᛒ", "C": "ᚳ", "D": "ᛞ", "E": "ᛖ", "G": "ᚷ", "H": "ᚻ", "I": "ᛁ",
    "L": "ᛚ", "M": "ᛗ", "N": "ᚾ", "O": "ᚩ", "P": "ᛈ", "R": "ᚱ", "S": "ᛋ", "T": "ᛏ", "U": "ᚢ", "Y": "ᚣ",
}

FRAUNCES_BOLD = ("Fraunces", "fraunces.ttf", {"wght": 700, "opsz": 144, "WONK": 1, "SOFT": 0}, 700)
FRAUNCES_MEDIUM = ("Fraunces", "fraunces.ttf", {"wght": 500, "opsz": 36, "WONK": 1, "SOFT": 0}, 500)
FRAUNCES_TITLE = ("Fraunces", "fraunces.ttf", {"wght": 700, "opsz": 72, "WONK": 1, "SOFT": 0}, 700)
FRAUNCES_ITALIC = ("FrauncesItalic", "fraunces-italic.ttf", {"wght": 400, "opsz": 24, "WONK": 1, "SOFT": 0}, 400)
COURIER = ("Courier", "courier.ttf", None, 400)
RUNES = ("Runes", "runic.ttf", None, 400)


def runes(text):
    out, i = [], 0
    while i < len(text):
        if text[i:i + 2] == "TH":
            out.append(FUTHORC["TH"])
            i += 2
            continue
        ch = text[i]
        out.append(FUTHORC.get(ch, "᛫" if ch == " " else ""))
        i += 1
    return "".join(out).replace("᛫᛫", "᛫") + "᛭"


def face(fonts_dir, spec, text):
    family, file, axes, weight = spec
    font = TTFont(Path(fonts_dir) / file, recalcTimestamp=False)
    if axes:
        font = instancer.instantiateVariableFont(font, axes)
    options = subset.Options()
    options.flavor = "woff"
    options.layout_features = ["kern", "liga"]
    sub = subset.Subsetter(options)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff"
    font.save(buf)
    data = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:{family};font-weight:{weight};src:url(data:font/woff;base64,{data}) format('woff');}}"
