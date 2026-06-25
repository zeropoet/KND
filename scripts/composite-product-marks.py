from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
TMP_DIR = Path("/private/tmp")

INK = "#171511"
CREAM = "#f8f6f2"

MARK_FILES = {
    "period": TMP_DIR / "knd-period-mark.svg.png",
    "word": TMP_DIR / "knd-mark.svg.png",
    "kids": TMP_DIR / "knd-kids-period-mark.svg.png",
}


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def mark(name: str, color: str, width: int, opacity: float = 0.9) -> Image.Image:
    source = Image.open(MARK_FILES[name]).convert("RGBA")
    luminance = source.convert("L")
    mask = luminance.point(lambda value: max(0, min(255, round((255 - value) * 1.45))))
    bbox = mask.getbbox()
    source = source.crop(bbox)
    mask = mask.crop(bbox)
    ratio = width / source.width
    source = source.resize((width, max(1, round(source.height * ratio))), Image.Resampling.LANCZOS)
    mask = mask.resize(source.size, Image.Resampling.LANCZOS)
    alpha = mask.point(lambda value: round(value * opacity))
    out = Image.new("RGBA", source.size, hex_to_rgb(color) + (0,))
    out.putalpha(alpha)
    return out


def stamp(
    layer: Image.Image,
    name: str,
    xy: tuple[int, int],
    width: int,
    color: str,
    angle: float = 0,
    opacity: float = 0.9,
) -> None:
    asset = mark(name, color, width, opacity)
    if angle:
        asset = asset.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    layer.alpha_composite(asset, xy)


def composite(path: Path, stamps: list[dict[str, object]]) -> None:
    image = Image.open(path).convert("RGBA")
    for item in stamps:
        stamp(
            image,
            str(item.get("mark", "period")),
            tuple(item["xy"]),  # type: ignore[arg-type]
            int(item["width"]),
            str(item.get("color", INK)),
            float(item.get("angle", 0)),
            float(item.get("opacity", 0.9)),
        )
    image.convert("RGB").filter(ImageFilter.UnsharpMask(radius=0.8, percent=24, threshold=5)).save(path, quality=94, optimize=True)
    print(f"Composited {path.relative_to(ROOT)}")


def main() -> None:
    composites = {
        "knd-shop-bundle-concept.png": [
            {"mark": "period", "xy": (314, 610), "width": 155, "color": INK, "angle": -2, "opacity": 0.78},
            {"mark": "period", "xy": (610, 622), "width": 180, "color": CREAM, "angle": 1, "opacity": 0.72},
            {"mark": "word", "xy": (970, 450), "width": 230, "color": INK, "angle": 7, "opacity": 0.68},
            {"mark": "word", "xy": (1005, 930), "width": 120, "color": CREAM, "angle": -11, "opacity": 0.64},
        ],
        "knd-shop-cap-concept.png": [
            {"mark": "period", "xy": (345, 565), "width": 138, "color": INK, "angle": -5, "opacity": 0.68},
            {"mark": "period", "xy": (930, 610), "width": 142, "color": CREAM, "angle": 2, "opacity": 0.64},
        ],
        "knd-shop-hoodie-concept.png": [
            {"mark": "period", "xy": (405, 690), "width": 145, "color": INK, "angle": -3, "opacity": 0.72},
            {"mark": "period", "xy": (900, 695), "width": 165, "color": CREAM, "angle": 1, "opacity": 0.66},
        ],
        "knd-shop-tee-concept.png": [
            {"mark": "kids", "xy": (375, 665), "width": 140, "color": INK, "angle": -2, "opacity": 0.76},
            {"mark": "kids", "xy": (780, 675), "width": 118, "color": INK, "angle": 0, "opacity": 0.72},
            {"mark": "kids", "xy": (1110, 685), "width": 92, "color": INK, "angle": 2, "opacity": 0.72},
        ],
        "knd-sports-joy.png": [
            {"mark": "period", "xy": (380, 640), "width": 155, "color": INK, "angle": -2, "opacity": 0.74},
            {"mark": "period", "xy": (860, 520), "width": 176, "color": CREAM, "angle": 1, "opacity": 0.64},
            {"mark": "word", "xy": (940, 1032), "width": 114, "color": CREAM, "angle": -4, "opacity": 0.62},
        ],
    }

    aliases = {
        "knd-shop-bundle-concept.png": [
            "knd-apparel-hero-marks.png",
            "knd-apparel-joy.png",
            "knd-apparel-worktable.png",
            "knd-apparel-options-table.png",
            "knd-apparel-team-pack.png",
            "knd-apparel-rack-options.png",
            "knd-brand-table.png",
            "knd-future-colorway.png",
        ],
        "knd-shop-cap-concept.png": [
            "knd-cap-light.png",
            "knd-apparel-cap-spectrum.png",
            "knd-reference-cap-tag.png",
            "knd-reference-sports-cap.png",
        ],
        "knd-shop-hoodie-concept.png": [
            "knd-hoodie.png",
            "knd-product-crew-cream.png",
            "knd-product-sweatpant-charcoal.png",
        ],
        "knd-shop-tee-concept.png": [
            "knd-tee.png",
            "knd-kids-hero.png",
            "knd-kids-flatlay.png",
            "knd-kids-size-range.png",
            "knd-product-youth-tee-sky.png",
        ],
        "knd-sports-joy.png": [
            "knd-sports-color-products.png",
            "knd-sports-product-basketball.png",
            "knd-sports-product-field.png",
            "knd-product-athletic-tee-blue.png",
            "knd-product-warmup-cream.png",
        ],
    }

    for source, targets in aliases.items():
        source_path = ASSET_DIR / source
        for target in targets:
            (ASSET_DIR / target).write_bytes(source_path.read_bytes())

    for filename, stamps in composites.items():
        composite(ASSET_DIR / filename, stamps)
        for target in aliases.get(filename, []):
            (ASSET_DIR / target).write_bytes((ASSET_DIR / filename).read_bytes())


if __name__ == "__main__":
    main()
