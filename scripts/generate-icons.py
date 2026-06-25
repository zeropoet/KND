from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons"
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
SIZES = (32, 180, 192, 512)
PAPER = (248, 246, 242, 255)
INK = (23, 21, 17, 255)


def draw_icon(size: int) -> Image.Image:
    image = Image.new("RGBA", (size, size), PAPER)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT, round(size * 0.29), index=1)
    text = "KND"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    period_size = max(3, round(size * 0.055))
    gap = round(size * 0.025)
    total_width = text_width + gap + period_size
    x = round((size - total_width) / 2)
    y = round((size - text_height) / 2 - size * 0.02)
    draw.text((x, y - bbox[1]), text, font=font, fill=INK)
    draw.rectangle(
        [
            x + text_width + gap,
            y + text_height - period_size,
            x + text_width + gap + period_size,
            y + text_height,
        ],
        fill=INK,
    )
    return image


def main() -> None:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    icons = []
    for size in SIZES:
        icon = draw_icon(size)
        path = ICON_DIR / f"icon-{size}.png"
        icon.save(path, optimize=True)
        icons.append(icon)

    favicon_sizes = [(16, 16), (32, 32), (48, 48)]
    favicon = [draw_icon(size[0]).resize(size, Image.Resampling.LANCZOS) for size in favicon_sizes]
    favicon[0].save(ROOT / "favicon.ico", sizes=favicon_sizes, append_images=favicon[1:])
    print(f"Wrote icons to {ICON_DIR.relative_to(ROOT)} and favicon.ico")


if __name__ == "__main__":
    main()
