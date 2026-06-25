from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
OUTPUT_DIR = ASSET_DIR / "responsive"
MANIFEST = OUTPUT_DIR / "manifest.json"
WIDTHS = (640, 960, 1280, 1600)
FORMATS = {
    "avif": {"quality": 48},
    "webp": {"quality": 72},
    "jpg": {"quality": 78, "progressive": True, "optimize": True},
}


def variant_widths(original_width: int) -> list[int]:
    widths = [width for width in WIDTHS if width < original_width]
    if not widths or original_width - widths[-1] > 80:
        widths.append(original_width)
    return sorted(set(widths))


def save_variant(image: Image.Image, output: Path, width: int, options: dict[str, object]) -> None:
    ratio = width / image.width
    height = round(image.height * ratio)
    resized = image.resize((width, height), Image.Resampling.LANCZOS)
    output.parent.mkdir(parents=True, exist_ok=True)
    resized.save(output, **options)


def main() -> None:
    manifest: dict[str, object] = {}

    for source in sorted(ASSET_DIR.glob("*.png")):
        with Image.open(source) as raw:
            image = raw.convert("RGB")
            widths = variant_widths(image.width)
            entry = {
                "width": image.width,
                "height": image.height,
                "variants": {extension: [] for extension in FORMATS},
            }

            for width in widths:
                for extension, options in FORMATS.items():
                    output = OUTPUT_DIR / f"{source.stem}-{width}.{extension}"
                    save_variant(image, output, width, options)
                    entry["variants"][extension].append(
                        {
                            "width": width,
                            "src": f"assets/responsive/{output.name}",
                        }
                    )

            manifest[f"assets/{source.name}"] = entry

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {MANIFEST.relative_to(ROOT)} with {len(manifest)} images")


if __name__ == "__main__":
    main()
