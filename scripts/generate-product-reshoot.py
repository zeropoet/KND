from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
TMP_DIR = Path("/private/tmp")

WIDTH = 1800
HEIGHT = 1200
SQUARE = 1400

INK = "#171511"
CHARCOAL = "#242321"
CREAM = "#f6efe1"
PAPER = "#fbf8ef"
SKY = "#8ec9ee"
SUN = "#ffd35a"
CORAL = "#ff7f62"
LEAF = "#86bd68"
BLUE = "#327de5"
ROSE = "#f2a4b5"
LILAC = "#bba7ff"


MARK_FILES = {
    "period": TMP_DIR / "knd-period-mark.svg.png",
    "word": TMP_DIR / "knd-mark.svg.png",
    "smile": TMP_DIR / "knd-lockup-smile.svg.png",
    "wins": TMP_DIR / "knd-kindness-wins-smile.svg.png",
    "kids": TMP_DIR / "knd-kids-period-mark.svg.png",
}


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def soften(color: str, amount: float = 0.72) -> tuple[int, int, int]:
    r, g, b = hex_to_rgb(color)
    pr, pg, pb = hex_to_rgb(PAPER)
    return (
        round(r * (1 - amount) + pr * amount),
        round(g * (1 - amount) + pg * amount),
        round(b * (1 - amount) + pb * amount),
    )


def canvas(size: tuple[int, int] = (WIDTH, HEIGHT), wash: str = SKY) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, PAPER)
    draw = ImageDraw.Draw(image)
    wash_rgb = soften(wash, 0.42)
    paper_rgb = hex_to_rgb(PAPER)
    for y in range(height):
        mix = y / height
        color = tuple(round(wash_rgb[i] * (1 - mix) + paper_rgb[i] * mix) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)
    draw.ellipse((-180, -260, 720, 520), fill=soften(SUN, 0.35))
    draw.rectangle((0, height * 0.58, width, height), fill=soften(CREAM, 0.35))
    return image


def shadow(layer: Image.Image, bbox: tuple[int, int, int, int], radius: int = 40, alpha: int = 58) -> None:
    shade = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shade)
    draw.ellipse(bbox, fill=(0, 0, 0, alpha))
    shade = shade.filter(ImageFilter.GaussianBlur(radius))
    layer.alpha_composite(shade)


def mark(name: str = "period", color: str = INK, width: int = 220) -> Image.Image:
    source = Image.open(MARK_FILES[name]).convert("RGBA")
    bbox = source.getbbox()
    source = source.crop(bbox)
    ratio = width / source.width
    source = source.resize((width, max(1, round(source.height * ratio))), Image.Resampling.LANCZOS)
    alpha = source.getchannel("A")
    colored = Image.new("RGBA", source.size, hex_to_rgb(color) + (0,))
    colored.putalpha(alpha)
    return colored


def paste_mark(layer: Image.Image, name: str, xy: tuple[int, int], width: int, color: str = INK, angle: float = 0) -> None:
    asset = mark(name, color, width)
    if angle:
        asset = asset.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    layer.alpha_composite(asset, xy)


def rounded(layer: Image.Image, box: tuple[int, int, int, int], fill: str, radius: int = 34, outline: str | None = None) -> None:
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=3 if outline else 1)


def tee(layer: Image.Image, x: int, y: int, color: str, scale: float = 1, mark_name: str = "period") -> None:
    w = round(520 * scale)
    h = round(620 * scale)
    draw = ImageDraw.Draw(layer)
    shadow(layer, (x - 30, y + h - 30, x + w + 30, y + h + 90), 36, 45)
    points = [
        (x + w * 0.24, y + h * 0.04),
        (x + w * 0.03, y + h * 0.18),
        (x + w * 0.13, y + h * 0.36),
        (x + w * 0.27, y + h * 0.30),
        (x + w * 0.27, y + h * 0.96),
        (x + w * 0.73, y + h * 0.96),
        (x + w * 0.73, y + h * 0.30),
        (x + w * 0.87, y + h * 0.36),
        (x + w * 0.97, y + h * 0.18),
        (x + w * 0.76, y + h * 0.04),
    ]
    draw.polygon(points, fill=color)
    draw.arc((x + w * 0.37, y + h * 0.01, x + w * 0.63, y + h * 0.17), 0, 180, fill=soften(color, 0.55), width=8)
    paste_mark(layer, mark_name, (round(x + w * 0.43), round(y + h * 0.34)), round(w * 0.22), CREAM if color == CHARCOAL else INK)


def hoodie(layer: Image.Image, x: int, y: int, color: str, scale: float = 1, mark_name: str = "period") -> None:
    w = round(570 * scale)
    h = round(660 * scale)
    draw = ImageDraw.Draw(layer)
    shadow(layer, (x - 25, y + h - 40, x + w + 35, y + h + 92), 42, 54)
    draw.rounded_rectangle((x + w * 0.18, y + h * 0.22, x + w * 0.82, y + h * 0.97), radius=70, fill=color)
    draw.pieslice((x + w * 0.26, y, x + w * 0.74, y + h * 0.45), 180, 360, fill=color)
    draw.rounded_rectangle((x + w * 0.02, y + h * 0.25, x + w * 0.28, y + h * 0.87), radius=72, fill=color)
    draw.rounded_rectangle((x + w * 0.72, y + h * 0.25, x + w * 0.98, y + h * 0.87), radius=72, fill=color)
    draw.arc((x + w * 0.38, y + h * 0.18, x + w * 0.62, y + h * 0.36), 0, 180, fill=soften(color, 0.54), width=8)
    draw.rounded_rectangle((x + w * 0.38, y + h * 0.58, x + w * 0.62, y + h * 0.78), radius=34, fill=soften(color, 0.32))
    paste_mark(layer, mark_name, (round(x + w * 0.44), round(y + h * 0.42)), round(w * 0.2), CREAM if color == CHARCOAL else INK)


def cap(layer: Image.Image, x: int, y: int, color: str, scale: float = 1, mark_name: str = "period") -> None:
    w = round(560 * scale)
    h = round(310 * scale)
    draw = ImageDraw.Draw(layer)
    shadow(layer, (x - 24, y + h * 0.64, x + w + 34, y + h + 80), 36, 54)
    draw.pieslice((x + w * 0.12, y, x + w * 0.88, y + h * 1.35), 180, 360, fill=color)
    draw.rounded_rectangle((x + w * 0.45, y + h * 0.49, x + w * 1.02, y + h * 0.73), radius=58, fill=color)
    draw.arc((x + w * 0.24, y + h * 0.1, x + w * 0.76, y + h * 1.04), 195, 345, fill=soften(color, 0.35), width=5)
    paste_mark(layer, mark_name, (round(x + w * 0.42), round(y + h * 0.34)), round(w * 0.19), CREAM if color == CHARCOAL else INK)


def tote(layer: Image.Image, x: int, y: int, color: str = CREAM, scale: float = 1, mark_name: str = "period") -> None:
    w = round(470 * scale)
    h = round(610 * scale)
    draw = ImageDraw.Draw(layer)
    shadow(layer, (x - 20, y + h - 38, x + w + 20, y + h + 70), 36, 42)
    draw.rounded_rectangle((x, y + h * 0.18, x + w, y + h), radius=22, fill=color)
    draw.arc((x + w * 0.28, y, x + w * 0.72, y + h * 0.35), 180, 360, fill=INK, width=12)
    paste_mark(layer, mark_name, (round(x + w * 0.25), round(y + h * 0.48)), round(w * 0.5), INK)


def socks(layer: Image.Image, x: int, y: int, color: str, scale: float = 1, mark_name: str = "word") -> None:
    w = round(160 * scale)
    h = round(520 * scale)
    draw = ImageDraw.Draw(layer)
    for offset in (0, round(w * 0.55)):
        draw.rounded_rectangle((x + offset, y, x + offset + w, y + h * 0.78), radius=34, fill=color)
        draw.rounded_rectangle((x + offset, y + h * 0.68, x + offset + w * 1.55, y + h), radius=36, fill=color)
        paste_mark(layer, mark_name, (round(x + offset + w * 0.24), round(y + h * 0.18)), round(w * 0.48), CREAM if color == CHARCOAL else INK)
    shadow(layer, (x - 10, y + h - 22, x + w * 2 + 34, y + h + 50), 28, 34)


def bottle(layer: Image.Image, x: int, y: int, color: str, scale: float = 1, mark_name: str = "period") -> None:
    w = round(190 * scale)
    h = round(620 * scale)
    draw = ImageDraw.Draw(layer)
    shadow(layer, (x - 18, y + h - 20, x + w + 18, y + h + 60), 28, 42)
    draw.rounded_rectangle((x + w * 0.22, y, x + w * 0.78, y + h * 0.12), radius=18, fill=INK)
    draw.rounded_rectangle((x, y + h * 0.1, x + w, y + h), radius=68, fill=color)
    paste_mark(layer, mark_name, (round(x + w * 0.24), round(y + h * 0.48)), round(w * 0.54), CREAM if color == CHARCOAL else INK, angle=-90)


def patch(layer: Image.Image, x: int, y: int, color: str, scale: float = 1, mark_name: str = "period") -> None:
    w = round(310 * scale)
    h = round(190 * scale)
    shadow(layer, (x - 12, y + h - 8, x + w + 12, y + h + 40), 22, 38)
    rounded(layer, (x, y, x + w, y + h), color, 28, INK)
    paste_mark(layer, mark_name, (round(x + w * 0.2), round(y + h * 0.36)), round(w * 0.6), CREAM if color == CHARCOAL else INK)


def card_scene(filename: str, subject: str, colors: list[str], square: bool = False, mark_name: str = "period") -> None:
    size = (SQUARE, SQUARE) if square else (WIDTH, HEIGHT)
    image = canvas(size, random.choice([SKY, SUN, CORAL, LEAF]))
    layer = image.convert("RGBA")
    if subject == "cap":
        cap(layer, 390, 430, colors[0], 1.55, mark_name)
        patch(layer, 970, 705, colors[1], 0.78, "word")
    elif subject == "hoodie":
        hoodie(layer, 330, 270, colors[0], 1.2, mark_name)
        cap(layer, 1040, 640, colors[1], 0.82, "word")
    elif subject == "tee":
        tee(layer, 370, 260, colors[0], 1.2, mark_name)
        socks(layer, 1040, 520, colors[1], 0.72, "word")
    elif subject == "tote":
        tote(layer, 370, 250, colors[0], 1.15, mark_name)
        bottle(layer, 1040, 370, colors[1], 0.82, "word")
    elif subject == "bundle":
        tee(layer, 130, 260, colors[0], 0.92, mark_name)
        hoodie(layer, 620, 210, colors[1], 0.86, "word")
        cap(layer, 1120, 610, colors[2], 0.72, mark_name)
        socks(layer, 1180, 160, colors[3], 0.55, "word")
        patch(layer, 880, 850, colors[4], 0.78, mark_name)
    elif subject == "sports":
        tee(layer, 220, 260, colors[0], 1.08, mark_name)
        cap(layer, 920, 530, colors[1], 1.0, "word")
        bottle(layer, 1280, 300, colors[2], 0.82, "period")
    else:
        hoodie(layer, 250, 260, colors[0], 1, mark_name)
        tee(layer, 890, 300, colors[1], 0.9, "word")
        patch(layer, 1180, 820, colors[2], 0.8, "period")

    final = layer.convert("RGB").filter(ImageFilter.UnsharpMask(radius=1.1, percent=38, threshold=4))
    final.save(ASSET_DIR / filename, quality=95, optimize=True)
    print(f"Wrote assets/{filename}")


def main() -> None:
    random.seed(42)
    scenes = {
        "knd-shop-cap-concept.png": ("cap", [CHARCOAL, SUN], True, "period"),
        "knd-shop-hoodie-concept.png": ("hoodie", [CHARCOAL, CREAM], True, "period"),
        "knd-shop-tee-concept.png": ("tee", [CREAM, CHARCOAL], True, "period"),
        "knd-shop-bundle-concept.png": ("bundle", [CREAM, CHARCOAL, BLUE, CORAL, SUN], True, "period"),
        "knd-cap-light.png": ("cap", [CREAM, SKY], False, "period"),
        "knd-hoodie.png": ("hoodie", [CHARCOAL, CORAL], False, "period"),
        "knd-tee.png": ("tee", [CREAM, BLUE], False, "period"),
        "knd-apparel-hero-marks.png": ("bundle", [CREAM, CHARCOAL, SKY, CORAL, LEAF], False, "period"),
        "knd-apparel-joy.png": ("bundle", [CORAL, CREAM, BLUE, SUN, LEAF], False, "period"),
        "knd-apparel-worktable.png": ("bundle", [CREAM, CHARCOAL, CORAL, SKY, SUN], False, "wins"),
        "knd-apparel-lunch.png": ("assorted", [CREAM, BLUE, SUN], False, "period"),
        "knd-apparel-details.png": ("assorted", [CHARCOAL, CREAM, CORAL], False, "word"),
        "knd-apparel-options-table.png": ("bundle", [CREAM, CHARCOAL, BLUE, CORAL, LILAC], False, "period"),
        "knd-apparel-team-pack.png": ("bundle", [BLUE, CHARCOAL, CREAM, SUN, CORAL], False, "period"),
        "knd-apparel-cap-spectrum.png": ("cap", [BLUE, SUN], False, "period"),
        "knd-apparel-daily-carry.png": ("tote", [CREAM, BLUE], False, "period"),
        "knd-apparel-group-options.png": ("assorted", [CORAL, CREAM, LEAF], False, "period"),
        "knd-apparel-rack-options.png": ("bundle", [CREAM, CHARCOAL, LEAF, BLUE, SUN], False, "period"),
        "knd-brand-table.png": ("assorted", [CREAM, CHARCOAL, SUN], False, "smile"),
        "knd-future-colorway.png": ("bundle", [LILAC, CREAM, BLUE, CORAL, SUN], False, "period"),
        "knd-reference-cap-tag.png": ("cap", [CHARCOAL, CREAM], True, "period"),
        "knd-reference-sports-cap.png": ("cap", [BLUE, CREAM], True, "period"),
        "knd-sports-joy.png": ("sports", [CREAM, BLUE, CORAL], False, "period"),
        "knd-sports-color-products.png": ("bundle", [BLUE, CREAM, CORAL, SUN, LEAF], False, "period"),
        "knd-sports-product-basketball.png": ("sports", [CORAL, CHARCOAL, BLUE], False, "period"),
        "knd-sports-product-field.png": ("sports", [LEAF, CREAM, BLUE], False, "period"),
        "knd-kids-hero.png": ("bundle", [CREAM, SKY, CORAL, SUN, LILAC], False, "kids"),
        "knd-kids-flatlay.png": ("tee", [SKY, CORAL], False, "kids"),
        "knd-kids-size-range.png": ("bundle", [CREAM, CORAL, SKY, SUN, LILAC], False, "kids"),
        "knd-product-crew-cream.png": ("hoodie", [CREAM, SUN], True, "period"),
        "knd-product-sweatpant-charcoal.png": ("assorted", [CHARCOAL, CREAM, SKY], True, "word"),
        "knd-product-tote-cream.png": ("tote", [CREAM, CORAL], True, "period"),
        "knd-product-socks-sun.png": ("assorted", [SUN, CHARCOAL, CREAM], True, "word"),
        "knd-product-bottle-blue.png": ("tote", [CREAM, BLUE], True, "period"),
        "knd-product-youth-tee-sky.png": ("tee", [SKY, CORAL], True, "kids"),
        "knd-product-athletic-tee-blue.png": ("sports", [BLUE, CREAM, SUN], True, "period"),
        "knd-product-warmup-cream.png": ("sports", [CREAM, CHARCOAL, CORAL], True, "word"),
        "knd-product-patch-pack.png": ("assorted", [SUN, CORAL, BLUE], True, "period"),
    }
    for filename, (subject, colors, square, mark_name) in scenes.items():
        card_scene(filename, subject, colors, square, mark_name)


if __name__ == "__main__":
    main()
