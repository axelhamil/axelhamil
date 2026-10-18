import argparse
import functools
import http.server
import shutil
import subprocess
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".preview"
CSS = "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-{theme}.min.css"
PAGE_COLORS = {"light": ("#ffffff", "#d0d7de"), "dark": ("#0d1117", "#30363d")}
RELOAD = """<script>let v;setInterval(async()=>{try{const t=await (await fetch("version.txt",{cache:"no-store"})).text();if(v&&t!==v)location.reload();v=t}catch{}},1000)</script>"""


def github_html():
    readme = (ROOT / "README.md").read_text()
    result = subprocess.run(
        ["gh", "api", "markdown", "-f", f"text={readme}", "-f", "mode=gfm", "-f", "context=axelhamil/axelhamil"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def themed(body, theme):
    if theme == "dark":
        return body.replace("-light.svg", "-dark.svg")

    return "\n".join(line for line in body.splitlines() if "<source media" not in line)


def page(body, theme):
    background, border = PAGE_COLORS[theme]
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>README {theme}</title>
<link rel="stylesheet" href="{CSS.format(theme=theme)}">
<style>body{{margin:0;background:{background}}}.markdown-body{{box-sizing:border-box;max-width:880px;margin:32px auto;padding:24px;border:1px solid {border};border-radius:6px}}</style></head>
<body>{RELOAD}<article class="markdown-body">{themed(body, theme)}</article></body></html>
"""


def render():
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
    body = github_html()
    for theme in PAGE_COLORS:
        (OUT / f"{theme}.html").write_text(page(body, theme))
    (OUT / "version.txt").write_text(str(time.time_ns()))


def stamp():
    files = [ROOT / "README.md", *(ROOT / "assets").rglob("*.svg")]
    return max(f.stat().st_mtime for f in files)


def watch():
    last = stamp()
    while True:
        time.sleep(1)
        now = stamp()
        if now == last:
            continue

        last = now
        try:
            render()
        except subprocess.CalledProcessError as error:
            print(f"render failed, keeping the last page: {error.stderr.strip()}", flush=True)
            continue

        print(f"rebuilt {time.strftime('%H:%M:%S')}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Render README.md like GitHub and serve it with live reload.")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    OUT.mkdir(exist_ok=True)
    render()
    threading.Thread(target=watch, daemon=True).start()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=OUT)
    print(f"http://localhost:{args.port}/light.html  http://localhost:{args.port}/dark.html", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler).serve_forever()


if __name__ == "__main__":
    main()
