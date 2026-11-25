"""Genera los iconos del logo DAZ y los añade a todas las páginas (web, Google y redes).

Se ejecuta desde GitHub Actions (workflow brand.yml). Es seguro repetirlo:
no duplica nada si ya está aplicado.
"""
import glob
import html
import json
import os
import re
import urllib.request
from datetime import date

from PIL import Image

SITE = "https://dazperformance.com"
LOGO_URL = "https://dazpremiumfit.com/cdn/shop/files/Gemini_Generated_Image_8w4gk78w4gk78w4g.png"
NAME = "DAZ Premium Fit Performance"
MARK_START = "<!-- DAZ-BRAND:START -->"
MARK_END = "<!-- DAZ-BRAND:END -->"
SAME_AS = [
    "https://dazpremiumfit.com",
    "https://t.me/DPFPerformance_bot",
]


def build_images() -> None:
    os.makedirs("assets", exist_ok=True)
    src_path = "assets/logo-original.png"
    if not os.path.exists(src_path):
        req = urllib.request.Request(LOGO_URL, headers={"User-Agent": "Mozilla/5.0 (DAZ Brand Bot)"})
        with urllib.request.urlopen(req, timeout=60) as resp, open(src_path, "wb") as out:
            out.write(resp.read())
    logo = Image.open(src_path).convert("RGB")
    side = min(logo.size)
    left = (logo.width - side) // 2
    top = (logo.height - side) // 2
    logo = logo.crop((left, top, left + side, top + side))

    def save(size: int, path: str, fmt: str = "PNG") -> None:
        img = logo.resize((size, size), Image.LANCZOS)
        if fmt == "JPEG":
            img.save(path, fmt, quality=90, optimize=True)
        else:
            img.save(path, fmt, optimize=True)

    save(512, "assets/logo-512.png")
    save(192, "assets/logo-192.png")
    save(180, "apple-touch-icon.png")
    save(48, "favicon-48.png")
    save(640, "assets/telegram-photo.jpg", "JPEG")
    logo.resize((256, 256), Image.LANCZOS).save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    # Imagen para compartir (Google, WhatsApp, Telegram, redes): 1200x630
    bg_color = logo.getpixel((5, 5))
    og = Image.new("RGB", (1200, 630), bg_color)
    mark = logo.resize((630, 630), Image.LANCZOS)
    og.paste(mark, ((1200 - 630) // 2, 0))
    og.save("assets/og-image.jpg", "JPEG", quality=88, optimize=True)

    manifest = {
        "name": NAME,
        "short_name": "DAZ Performance",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0b0b0b",
        "theme_color": "#0b0b0b",
        "icons": [
            {"src": "/assets/logo-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/logo-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    with open("site.webmanifest", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def head_block(page: str, title: str, description: str) -> str:
    url = f"{SITE}/" if page == "index.html" else f"{SITE}/{page}"
    t = html.escape(title, quote=True)
    d = html.escape(description, quote=True)
    lines = [
        MARK_START,
        '  <link rel="icon" href="/favicon.ico" sizes="any" />',
        '  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png" />',
        '  <link rel="icon" type="image/png" sizes="192x192" href="/assets/logo-192.png" />',
        '  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />',
        '  <link rel="manifest" href="/site.webmanifest" />',
        '  <meta name="theme-color" content="#0b0b0b" />',
        f'  <link rel="canonical" href="{url}" />',
        '  <meta property="og:type" content="website" />',
        f'  <meta property="og:site_name" content="{NAME}" />',
        f'  <meta property="og:title" content="{t}" />',
        f'  <meta property="og:description" content="{d}" />',
        f'  <meta property="og:url" content="{url}" />',
        f'  <meta property="og:image" content="{SITE}/assets/og-image.jpg" />',
        '  <meta property="og:image:width" content="1200" />',
        '  <meta property="og:image:height" content="630" />',
        '  <meta name="twitter:card" content="summary_large_image" />',
        f'  <meta name="twitter:title" content="{t}" />',
        f'  <meta name="twitter:description" content="{d}" />',
        f'  <meta name="twitter:image" content="{SITE}/assets/og-image.jpg" />',
    ]
    if page == "index.html":
        data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Organization",
                    "@id": f"{SITE}/#organization",
                    "name": NAME,
                    "url": f"{SITE}/",
                    "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/logo-512.png", "width": 512, "height": 512},
                    "image": f"{SITE}/assets/og-image.jpg",
                    "parentOrganization": {"@type": "Organization", "name": "Community16 LLC"},
                    "sameAs": SAME_AS,
                },
                {
                    "@type": "WebSite",
                    "@id": f"{SITE}/#website",
                    "name": NAME,
                    "url": f"{SITE}/",
                    "inLanguage": ["es", "en"],
                    "publisher": {"@id": f"{SITE}/#organization"},
                },
            ],
        }
        lines.append('  <script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>")
    lines.append(MARK_END)
    return "\n".join(lines) + "\n"


def patch_pages() -> list[str]:
    pages = sorted(p for p in glob.glob("*.html") if not p.startswith("google"))
    for page in pages:
        with open(page, encoding="utf-8") as f:
            content = f.read()
        content = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END) + r"\n?", "", content, flags=re.S)
        title_m = re.search(r"<title>(.*?)</title>", content, re.S | re.I)
        title = html.unescape(title_m.group(1).strip()) if title_m else NAME
        desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content, re.I)
        if desc_m:
            description = html.unescape(desc_m.group(1))
        else:
            description = (
                "DAZ Premium Fit Performance: entrenamientos por objetivos, nutrición, macros, "
                "suplementación y planificación atlética con datos científicos."
            )
            content = re.sub(
                r"(</head>)",
                f'  <meta name="description" content="{html.escape(description, quote=True)}" />\n\\1',
                content, count=1, flags=re.I,
            )
        content = re.sub(r"(</head>)", head_block(page, title, description).replace("\\", "\\\\") + r"\1",
                         content, count=1, flags=re.I)
        with open(page, "w", encoding="utf-8") as f:
            f.write(content)
    return pages


def patch_nav_logo() -> None:
    path = "nav.js"
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        js = f.read()
    if "daz-brand-logo" in js:
        return
    js = js.replace(
        '<a href="index.html" class="daz-brand">',
        '<a href="index.html" class="daz-brand"><img class="daz-brand-logo" src="assets/logo-192.png" alt="DAZ Premium Fit" width="38" height="38" />',
        1,
    )
    js = js.replace(
        "    .daz-brand span.gold {",
        "    .daz-brand { display: inline-flex; align-items: center; gap: 10px; }\n"
        "    .daz-brand-logo { width: 38px; height: 38px; border-radius: 8px; object-fit: cover; }\n"
        "    .daz-brand span.gold {",
        1,
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(js)


def write_sitemap(pages: list[str]) -> None:
    today = date.today().isoformat()
    order = ["index.html"] + [p for p in pages if p != "index.html"]
    urls = []
    for p in order:
        loc = f"{SITE}/" if p == "index.html" else f"{SITE}/{p}"
        prio = "1.0" if p == "index.html" else "0.8"
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>{prio}</priority></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    build_images()
    pages = patch_pages()
    patch_nav_logo()
    write_sitemap(pages)
    print("[BRAND] Listo:", ", ".join(pages))
