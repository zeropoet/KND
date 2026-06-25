from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://zeropoet.github.io/KND"
SITE_NAME = "KND"
THEME_COLOR = "#f8f6f2"

PAGES = {
    "index.html": {
        "title": "KND",
        "description": "KND is a character brand built around kindness as something lived, worn, and shared.",
        "image": "assets/responsive/knd-apparel-joy-1693.jpg",
        "type": "website",
    },
    "apparel.html": {
        "title": "KND Apparel",
        "description": "KND apparel opportunities built around character, joy, and everyday wear.",
        "image": "assets/responsive/knd-apparel-hero-marks-1693.jpg",
        "type": "website",
    },
    "kids.html": {
        "title": "KND Kids",
        "description": "KND Kids apparel for babies, toddlers, and kids: kindness they can wear.",
        "image": "assets/responsive/knd-kids-hero-1600.jpg",
        "type": "website",
    },
    "sports.html": {
        "title": "KND Sports",
        "description": "KND sports partnership opportunities for teams, clubs, events, and community programs.",
        "image": "assets/responsive/knd-sports-joy-1536.jpg",
        "type": "website",
    },
    "brand-direction.html": {
        "title": "KND Brand Direction",
        "description": "KND brand direction, logo system, and visual system.",
        "image": "assets/responsive/knd-brand-table-1600.jpg",
        "type": "website",
    },
    "shop.html": {
        "title": "KND Shop",
        "description": "KND shop concept system for apparel, bundles, product records, attestation, tracking, shipment, and account-ready product architecture.",
        "image": "assets/responsive/knd-shop-bundle-concept-1254.jpg",
        "type": "website",
    },
    "404.html": {
        "title": "KND Page Not Found",
        "description": "The KND page you were looking for could not be found.",
        "image": "assets/responsive/knd-apparel-joy-1693.jpg",
        "type": "website",
    },
}


def url_for(page: str) -> str:
    return SITE_URL + ("/" if page == "index.html" else f"/{page}")


def absolute(path: str) -> str:
    return f"{SITE_URL}/{path}"


def json_ld(page: str, data: dict[str, str]) -> dict[str, object]:
    base = {
        "@context": "https://schema.org",
        "@type": "Brand",
        "name": "KND",
        "url": SITE_URL + "/",
        "logo": absolute("assets/knd-period-mark.svg"),
        "slogan": "Kindness has a smile now.",
    }

    if page == "shop.html":
        catalog = json.loads((ROOT / "data" / "catalog.json").read_text())
        return {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "KND Shop Product Preview",
            "url": url_for(page),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index + 1,
                    "item": {
                        "@type": "Product",
                        "name": product["name"],
                        "sku": product["id"],
                        "description": product["summary"],
                        "brand": {"@type": "Brand", "name": "KND"},
                        "image": absolute(product["image"]["src"]),
                    },
                }
                for index, product in enumerate(catalog["products"])
                if product.get("visibility") == "public"
            ],
        }

    return base


def meta_block(page: str, data: dict[str, str]) -> str:
    canonical = url_for(page)
    image = absolute(data["image"])
    title = data["title"]
    description = data["description"]
    ld = json.dumps(json_ld(page, data), separators=(",", ":"))
    with Image.open(ROOT / data["image"]) as image_file:
      image_width, image_height = image_file.size

    return "\n".join(
        [
            f'    <link rel="canonical" href="{canonical}">',
            '    <link rel="icon" href="assets/knd-period-mark.svg" type="image/svg+xml">',
            '    <link rel="alternate icon" href="favicon.ico">',
            '    <link rel="apple-touch-icon" href="assets/icons/icon-180.png">',
            '    <link rel="manifest" href="site.webmanifest">',
            f'    <meta name="theme-color" content="{THEME_COLOR}">',
            f'    <meta property="og:site_name" content="{SITE_NAME}">',
            f'    <meta property="og:type" content="{data["type"]}">',
            f'    <meta property="og:title" content="{title}">',
            f'    <meta property="og:description" content="{description}">',
            f'    <meta property="og:url" content="{canonical}">',
            f'    <meta property="og:image" content="{image}">',
            f'    <meta property="og:image:width" content="{image_width}">',
            f'    <meta property="og:image:height" content="{image_height}">',
            '    <meta name="twitter:card" content="summary_large_image">',
            f'    <meta name="twitter:title" content="{title}">',
            f'    <meta name="twitter:description" content="{description}">',
            f'    <meta name="twitter:image" content="{image}">',
            f'    <script type="application/ld+json">{ld}</script>',
        ]
    )


def apply_meta(page: str, data: dict[str, str]) -> None:
    path = ROOT / page
    html = path.read_text()
    html = re.sub(r"\n    <link rel=\"canonical\".*?(?=\n    <link rel=\"preload\"|\n    <link rel=\"stylesheet\")", "", html, flags=re.DOTALL)
    html = re.sub(
        r'    <title>.*?</title>\n    <meta name="description" content=".*?">',
        f'    <title>{data["title"]}</title>\n    <meta name="description" content="{data["description"]}">\n{meta_block(page, data)}',
        html,
        count=1,
    )
    path.write_text(html)
    print(f"Updated {page}")


def main() -> None:
    for page, data in PAGES.items():
        if (ROOT / page).exists():
            apply_meta(page, data)


if __name__ == "__main__":
    main()
