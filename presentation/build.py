#!/usr/bin/env python3
"""Build the presentation into one self-contained HTML file.

Inlines every font, image and the LinkedIn QR code, so the result runs
offline from a USB stick with no internet.

    python3 build.py                 # -> dist/Mohamed-Ismail-Presentation.html
    python3 build.py --fragment OUT  # also writes a body-only copy (for web hosting)
"""
import base64, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "dist" / "Mohamed-Ismail-Presentation.html"
MIME = {".woff2": "font/woff2", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def data_uri(rel):
    p = SRC / rel
    return f"data:{MIME[p.suffix.lower()]};base64," + base64.b64encode(p.read_bytes()).decode()


def build():
    html = (SRC / "deck.html").read_text(encoding="utf-8")
    html = re.sub(r"url\((fonts/[^)]+)\)", lambda m: f"url({data_uri(m.group(1))})", html)
    html = re.sub(r'src="(assets/[^"]+)"', lambda m: f'src="{data_uri(m.group(1))}"', html)
    qr = (SRC / "qr-linkedin.svg").read_text(encoding="utf-8").strip()
    qr = qr.replace("<svg ", '<svg role="img" aria-label="QR code linking to Mohamed Ismail on LinkedIn" ', 1)
    html = html.replace("%%QR%%", qr)
    missing = re.findall(r'(?:src="|url\()(?:assets|fonts)/', html)
    if missing:
        sys.exit(f"unresolved asset references: {len(missing)}")
    return html


def main():
    frag = build()
    head, body = frag.split("<!--BODY-->", 1)
    doc = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
           + head.strip() + "\n</head>\n<body>\n" + body.strip() + "\n</body>\n</html>\n")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}  {OUT.stat().st_size / 1e6:.1f} MB")
    if "--fragment" in sys.argv:
        dest = pathlib.Path(sys.argv[sys.argv.index("--fragment") + 1])
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(frag, encoding="utf-8")
        print(f"{dest}  {dest.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
