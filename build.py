"""Crea index.html (pagina completa per GitHub Pages) a partire da app.html."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
body = (root / "app.html").read_text(encoding="utf-8")
head = ('<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="theme-color" content="#1D5C96">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-title" content="Presenze">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="icon" href="icon.svg" type="image/svg+xml">\n'
        '<link rel="apple-touch-icon" href="icon-180.png">\n'
        '<style>body{margin:0}:root{padding-top:env(safe-area-inset-top,0px)}img{max-width:100%}[hidden]{display:none!important}</style>\n'
        '</head>\n<body>\n')
(root / "index.html").write_text(head + body + "\n</body>\n</html>\n", encoding="utf-8")
print("index.html creato")
