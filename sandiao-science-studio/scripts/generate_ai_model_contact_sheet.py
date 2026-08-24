#!/usr/bin/env python3
"""Render a review sheet for the domain.ai-models asset package."""

from __future__ import annotations

import io
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR / "design" / "assets" / "domains" / "ai-models"
OUTPUT = PROJECT_DIR / "design" / "previews" / "contact_sheet_ai_models.png"

INK = "#13223A"
NAVY = "#101C31"
BLUE = "#1F5CFF"
CYAN = "#1FD6E2"
VIOLET = "#8B5CF6"
GREEN = "#22C55E"
AMBER = "#F59E0B"
CORAL = "#F04B2F"


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def raster(path: Path, width: int, height: int) -> Image.Image:
    try:
        import cairosvg
    except ImportError:
        cairosvg = None
    if cairosvg is not None:
        raw = cairosvg.svg2png(url=str(path), output_width=width, output_height=height)
        return Image.open(io.BytesIO(raw)).convert("RGBA")
    sips = shutil.which("sips")
    if not sips:
        raise RuntimeError("contact sheet generation requires CairoSVG or macOS sips")
    with tempfile.TemporaryDirectory(prefix="sandiao-ai-assets-") as directory:
        output = Path(directory) / "asset.png"
        process = subprocess.run(
            [sips, "-s", "format", "png", str(path), "--out", str(output)],
            capture_output=True,
            text=True,
            check=False,
        )
        if process.returncode != 0:
            raise RuntimeError(process.stderr.strip() or process.stdout.strip())
        image = Image.open(output).convert("RGBA")
        image.load()
        return image


def fit(image: Image.Image, width: int, height: int) -> Image.Image:
    scale = min(width / image.width, height / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
    return canvas


def card(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    path: Path,
    label: str,
    box: tuple[int, int, int, int],
    *,
    diagram: bool = False,
) -> None:
    x, y, w, h = box
    draw.rounded_rectangle((x, y, x + w, y + h), radius=24, fill="#FFFFFF", outline="#D6E0EF", width=3)
    title_height = 54
    draw.rounded_rectangle((x + 2, y + 2, x + w - 2, y + title_height), radius=22, fill="#F2F6FC")
    draw.text((x + 20, y + 15), label, fill=INK, font=font(22, bold=True))
    source = raster(path, 900 if diagram else 520, 520)
    visual = fit(source, w - 36, h - title_height - 28)
    canvas.alpha_composite(visual, (x + 18, y + title_height + 12))


def main() -> None:
    width, height = 2400, 2220
    canvas = Image.new("RGBA", (width, height), "#EAF0F8")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((48, 42, 2352, 158), radius=32, fill=NAVY)
    draw.text((86, 67), "DOMAIN.AI-MODELS / ASSET SYSTEM 01", fill="#FFFFFF", font=font(44, bold=True))
    draw.text((1680, 80), "DATA  MODEL  COMPUTE  RETRIEVAL  RISK", fill=CYAN, font=font(20, bold=True))
    colors = (CYAN, VIOLET, BLUE, GREEN, AMBER, CORAL)
    for index, color in enumerate(colors):
        draw.rounded_rectangle((86 + index * 76, 132, 146 + index * 76, 142), radius=5, fill=color)

    backgrounds = [
        (ROOT / "backgrounds/model-observatory/scene_16x9.svg", "MODEL OBSERVATORY / DAY"),
        (ROOT / "backgrounds/model-observatory/scene_night_16x9.svg", "MODEL OBSERVATORY / NIGHT"),
    ]
    for index, (path, label) in enumerate(backgrounds):
        card(canvas, draw, path, label, (48 + index * 1164, 188, 1140, 440), diagram=True)

    draw.text((48, 668), "CORE COMPONENTS", fill=INK, font=font(30, bold=True))
    component_paths = sorted((ROOT / "components").glob("*.svg"))
    for index, path in enumerate(component_paths):
        col, row = index % 5, index // 5
        card(canvas, draw, path, path.stem.removeprefix("ai-").upper(), (48 + col * 464, 716 + row * 334, 440, 306))

    draw.text((48, 1406), "TEACHING DIAGRAMS", fill=INK, font=font(30, bold=True))
    diagram_paths = sorted((ROOT / "diagrams").glob("*.svg"))
    for index, path in enumerate(diagram_paths):
        col, row = index % 3, index // 3
        card(canvas, draw, path, path.stem.removeprefix("ai-").upper(), (48 + col * 776, 1454 + row * 236, 752, 212), diagram=True)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, quality=94)
    print(OUTPUT)


if __name__ == "__main__":
    main()
