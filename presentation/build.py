#!/usr/bin/env python3
"""Build the presentation into self-contained HTML files, one per theme.

Inlines every font, image and the LinkedIn QR code, so each result runs
offline from a USB stick with no internet.

    python3 build.py                     # -> dist/Mohamed-Ismail-Presentation-<Theme>.html
    python3 build.py --fragment-dir DIR  # also writes body-only copies (for web hosting)
"""
import base64, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
MIME = {".woff2": "font/woff2", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}

# name -> (page title, extra stylesheet layered on deck.css, QR module colour)
THEMES = {
    "Blueprint": ("Mohamed Ismail Portfolio", None, "#0c2b52"),
    "Light": ("Mohamed Ismail Portfolio Light", "theme-light.css", "#171717"),
}


def data_uri(rel):
    p = SRC / rel
    return f"data:{MIME[p.suffix.lower()]};base64," + base64.b64encode(p.read_bytes()).decode()


def build(theme):
    title, css, qr_colour = THEMES[theme]
    html = (SRC / "deck.html").read_text(encoding="utf-8")
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1)
    if css:  # append inside the deck stylesheet so the presenter window gets it too
        extra = (SRC / css).read_text(encoding="utf-8")
        html = html.replace("</style>", extra + "\n</style>", 1)
    html = re.sub(r"url\((fonts/[^)]+)\)", lambda m: f"url({data_uri(m.group(1))})", html)
    html = re.sub(r'src="(assets/[^"]+)"', lambda m: f'src="{data_uri(m.group(1))}"', html)
    qr = (SRC / "qr-linkedin.svg").read_text(encoding="utf-8").strip().replace("#0c2b52", qr_colour)
    qr = qr.replace("<svg ", '<svg role="img" aria-label="QR code linking to Mohamed Ismail on LinkedIn" ', 1)
    html = html.replace("%%QR%%", qr)
    if re.findall(r'(?:src="|url\()(?:assets|fonts)/', html):
        sys.exit(f"{theme}: unresolved asset references")
    return html


def main():
    DIST.mkdir(exist_ok=True)
    frag_dir = pathlib.Path(sys.argv[sys.argv.index("--fragment-dir") + 1]) if "--fragment-dir" in sys.argv else None
    for theme in THEMES:
        frag = build(theme)
        head, body = frag.split("<!--BODY-->", 1)
        doc = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
               "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
               + head.strip() + "\n</head>\n<body>\n" + body.strip() + "\n</body>\n</html>\n")
        out = DIST / f"Mohamed-Ismail-Presentation-{theme}.html"
        out.write_text(doc, encoding="utf-8")
        print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1e6:.1f} MB")
        if frag_dir:
            frag_dir.mkdir(parents=True, exist_ok=True)
            dest = frag_dir / f"mohamed-ismail-portfolio{'' if theme == 'Blueprint' else '-' + theme.lower()}.html"
            dest.write_text(frag, encoding="utf-8")
            print(f"{dest}  {dest.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
