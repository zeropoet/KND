from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "responsive" / "manifest.json"
PAGES = [
    ROOT / "index.html",
    ROOT / "apparel.html",
    ROOT / "kids.html",
    ROOT / "sports.html",
    ROOT / "brand-direction.html",
    ROOT / "shop.html",
]


ATTR_RE = re.compile(r'([a-zA-Z:-]+)(?:="([^"]*)")?')
IMG_RE = re.compile(r'(?P<indent>[ \t]*)<img(?P<attrs>[^>]*\bsrc="assets/[^"]+\.png"[^>]*)>', re.MULTILINE)
PICTURE_RE = re.compile(
    r'(?P<indent>[ \t]*)<picture>\s*.*?<img(?P<attrs>[^>]*\bdata-original-src="assets/[^"]+\.png"[^>]*)>\s*</picture>',
    re.MULTILINE | re.DOTALL,
)
PRELOAD_RE = re.compile(r'<link rel="preload" as="image" href="(?P<src>assets/[^"]+\.(?:png|avif))"(?: type="image/avif")?>')


def parse_attrs(raw: str) -> dict[str, str]:
    return {key: value or "" for key, value in ATTR_RE.findall(raw)}


def attrs_to_html(attrs: dict[str, str]) -> str:
    return " ".join(f'{key}="{value}"' if value else key for key, value in attrs.items())


def srcset(entry: dict[str, object], extension: str) -> str:
    return ", ".join(
        f"{variant['src']} {variant['width']}w"
        for variant in entry["variants"][extension]
    )


def picture_html(indent: str, attrs: dict[str, str], entry: dict[str, object], eager: bool) -> str:
    original_src = attrs.get("data-original-src", attrs["src"])
    attrs["src"] = entry["variants"]["jpg"][-1]["src"]
    attrs["srcset"] = srcset(entry, "jpg")
    attrs["sizes"] = attrs.get("sizes", "100vw")
    attrs["width"] = str(entry["width"])
    attrs["height"] = str(entry["height"])
    attrs.setdefault("decoding", "async")
    attrs["loading"] = "eager" if eager else attrs.get("loading", "lazy")
    attrs["data-original-src"] = original_src
    if eager:
        attrs["fetchpriority"] = "high"
    else:
        attrs.pop("fetchpriority", None)

    return "\n".join(
        [
            f'{indent}<picture>',
            f'{indent}  <source type="image/avif" srcset="{srcset(entry, "avif")}" sizes="{attrs["sizes"]}">',
            f'{indent}  <source type="image/webp" srcset="{srcset(entry, "webp")}" sizes="{attrs["sizes"]}">',
            f'{indent}  <img {attrs_to_html(attrs)}>',
            f'{indent}</picture>',
        ]
    )


def rewrite_page(path: Path, manifest: dict[str, object]) -> None:
    html = path.read_text()
    stem_to_source = {Path(source).stem: source for source in manifest}
    eager_sources = {match.group("src") for match in PRELOAD_RE.finditer(html)}
    first_png_seen = False

    def replace_preload(match: re.Match[str]) -> str:
        src = match.group("src")
        source = src
        if source.endswith(".avif"):
            source_stem = re.sub(r"-\d+$", "", Path(source).stem)
            source = stem_to_source.get(source_stem, source)
        entry = manifest.get(source)
        if not entry:
            return match.group(0)
        avif = entry["variants"]["avif"][-1]["src"]
        return f'<link rel="preload" as="image" href="{avif}" type="image/avif">'

    html = PRELOAD_RE.sub(replace_preload, html)

    def replace_picture(match: re.Match[str]) -> str:
        attrs = parse_attrs(match.group("attrs"))
        src = attrs.get("data-original-src")
        entry = manifest.get(src)
        if not entry:
            return match.group(0)
        eager = attrs.get("loading") == "eager" or attrs.get("fetchpriority") == "high"
        return picture_html(match.group("indent"), attrs, entry, eager)

    html = PICTURE_RE.sub(replace_picture, html)

    def replace_img(match: re.Match[str]) -> str:
        nonlocal first_png_seen
        attrs = parse_attrs(match.group("attrs"))
        src = attrs.get("src")
        entry = manifest.get(src)
        if not entry:
            return match.group(0)
        eager = src in eager_sources or not first_png_seen
        first_png_seen = True
        return picture_html(match.group("indent"), attrs, entry, eager)

    html = IMG_RE.sub(replace_img, html)
    path.write_text(html)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    for page in PAGES:
        rewrite_page(page, manifest)
        print(f"Updated {page.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
