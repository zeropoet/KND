from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"

BRIGHT_DAY = {
    "brightness": 1.13,
    "contrast": 1.06,
    "color": 1.18,
    "warmth": 1.05,
    "blue": 0.965,
    "shadow_lift": 20,
    "highlight_threshold": 202,
    "highlight_strength": 0.5,
}

PRODUCT_DAY = {
    "brightness": 1.04,
    "contrast": 1.04,
    "color": 1.1,
    "warmth": 1.035,
    "blue": 0.98,
    "shadow_lift": 10,
    "highlight_threshold": 210,
    "highlight_strength": 0.62,
}

KIDS_LIGHT_TOUCH = {
    "brightness": 1.03,
    "contrast": 1.03,
    "color": 1.06,
    "warmth": 1.015,
    "blue": 0.995,
    "shadow_lift": 4,
    "highlight_threshold": 214,
    "highlight_strength": 0.7,
}

REFERENCE_DAY = {
    "brightness": 1.08,
    "contrast": 1.06,
    "color": 1.13,
    "warmth": 1.04,
    "blue": 0.97,
    "shadow_lift": 12,
    "highlight_threshold": 206,
    "highlight_strength": 0.58,
}


PROFILE_BY_NAME = {
    "knd-kids-flatlay.png": KIDS_LIGHT_TOUCH,
    "knd-kids-hero.png": KIDS_LIGHT_TOUCH,
    "knd-kids-size-range.png": KIDS_LIGHT_TOUCH,
    "knd-cap-light.png": PRODUCT_DAY,
    "knd-hoodie.png": PRODUCT_DAY,
    "knd-tee.png": PRODUCT_DAY,
    "knd-shop-bundle-concept.png": PRODUCT_DAY,
    "knd-shop-cap-concept.png": PRODUCT_DAY,
    "knd-shop-hoodie-concept.png": PRODUCT_DAY,
    "knd-shop-tee-concept.png": PRODUCT_DAY,
    "knd-reference-cap-tag.png": REFERENCE_DAY,
    "knd-reference-sports-cap.png": REFERENCE_DAY,
}


def profile_for(path: Path) -> dict[str, float]:
    return PROFILE_BY_NAME.get(path.name, BRIGHT_DAY)


def clamp(value: float) -> int:
    return max(0, min(255, round(value)))


def lift_shadows(image: Image.Image, amount: float) -> Image.Image:
    pixels = []
    for r, g, b in image.getdata():
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        factor = max(0, 1 - luminance / 190)
        lift = amount * factor
        pixels.append((clamp(r + lift), clamp(g + lift), clamp(b + lift)))
    out = Image.new("RGB", image.size)
    out.putdata(pixels)
    return out


def warm_image(image: Image.Image, warmth: float, blue: float) -> Image.Image:
    r, g, b = image.split()
    r = r.point(lambda value: clamp(value * warmth + 3))
    g = g.point(lambda value: clamp(value * 1.015 + 1))
    b = b.point(lambda value: clamp(value * blue))
    return Image.merge("RGB", (r, g, b))


def compress_highlights(image: Image.Image, threshold: float, strength: float) -> Image.Image:
    pixels = []
    for r, g, b in image.getdata():
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        if luminance <= threshold:
            pixels.append((r, g, b))
            continue

        excess = luminance - threshold
        target_luminance = threshold + excess * strength
        scale = target_luminance / luminance
        pixels.append((clamp(r * scale), clamp(g * scale), clamp(b * scale)))

    out = Image.new("RGB", image.size)
    out.putdata(pixels)
    return out


def tune(path: Path) -> None:
    settings = profile_for(path)
    image = Image.open(path).convert("RGB")
    image = lift_shadows(image, settings["shadow_lift"])
    image = ImageEnhance.Brightness(image).enhance(settings["brightness"])
    image = ImageEnhance.Color(image).enhance(settings["color"])
    image = warm_image(image, settings["warmth"], settings["blue"])
    image = compress_highlights(
        image,
        settings["highlight_threshold"],
        settings["highlight_strength"],
    )
    image = ImageEnhance.Contrast(image).enhance(settings["contrast"])
    image.save(path, optimize=True)
    print(f"Tuned {path.relative_to(ROOT)}")


def main() -> None:
    for path in sorted(ASSET_DIR.glob("*.png")):
        tune(path)


if __name__ == "__main__":
    main()
