import argparse
from datetime import date
from pathlib import Path

import footer
import header
import titles

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="Render the profile header, footer and section titles, light and dark.")
    parser.add_argument("--fonts", type=Path, default=ROOT / "fonts", help="directory holding the source TTF files")
    parser.add_argument("--out", type=Path, default=ROOT / "assets", help="output directory")
    parser.add_argument("--date", type=date.fromisoformat, default=date.today(), help="scene date, drives the moon phase (YYYY-MM-DD)")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    header.build(args.fonts, args.out, args.date)
    footer.build(args.fonts, args.out, args.date)
    titles.build(args.fonts, args.out)


if __name__ == "__main__":
    main()
