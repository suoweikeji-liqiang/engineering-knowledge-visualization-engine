"""Pillow-backed renderer for validated SVG design assets."""

from __future__ import annotations

import io
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from PIL import Image

from ..assets import AssetManifest, DesignAsset
from .protocols import RenderSpec
from .types import Anchors, Bounds, Layer, RenderContext, RenderResult


class SvgRasterizationError(RuntimeError):
    """Raised when no local SVG rasterization backend can render an asset."""


class Rasterizer(Protocol):
    def rasterize(self, path: Path, width: int, height: int) -> Image.Image: ...


@dataclass
class SvgRasterizer:
    """Rasterize SVGs deterministically, caching immutable source results.

    CairoSVG is the portable production backend. macOS ``sips`` is retained as
    a local fallback so design review remains possible before dependencies are
    bootstrapped.
    """

    _sources: dict[Path, Image.Image] = field(default_factory=dict)
    _scaled: dict[tuple[Path, int, int], Image.Image] = field(default_factory=dict)

    def _source(self, path: Path) -> Image.Image:
        path = path.resolve()
        cached = self._sources.get(path)
        if cached is not None:
            return cached
        try:
            import cairosvg  # type: ignore[import-not-found]
        except ImportError:
            cairosvg = None
        if cairosvg is not None:
            raw = cairosvg.svg2png(url=str(path))
            image = Image.open(io.BytesIO(raw)).convert("RGBA")
        else:
            sips = shutil.which("sips")
            if not sips:
                raise SvgRasterizationError(
                    "SVG rendering requires CairoSVG; install project dependencies"
                )
            with tempfile.TemporaryDirectory(prefix="sandiao-svg-") as directory:
                output = Path(directory) / "asset.png"
                process = subprocess.run(
                    [sips, "-s", "format", "png", str(path), "--out", str(output)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if process.returncode != 0 or not output.is_file():
                    detail = process.stderr.strip() or process.stdout.strip()
                    raise SvgRasterizationError(f"failed to rasterize {path}: {detail}")
                image = Image.open(output).convert("RGBA")
        image.load()
        self._sources[path] = image
        return image

    def rasterize(self, path: Path, width: int, height: int) -> Image.Image:
        if width <= 0 or height <= 0:
            raise ValueError("SVG raster dimensions must be positive")
        key = (path.resolve(), width, height)
        cached = self._scaled.get(key)
        if cached is None:
            cached = self._source(path).resize((width, height), Image.Resampling.LANCZOS)
            self._scaled[key] = cached
        return cached.copy()


@dataclass
class SvgAssetRenderer:
    """Render a manifest asset into a Pillow frame using the shared protocol."""

    manifest: AssetManifest
    rasterizer: Rasterizer = field(default_factory=SvgRasterizer)
    renderer_id: str = "asset.svg"

    def render(
        self,
        context: RenderContext,
        layer: Layer,
        spec: RenderSpec,
    ) -> RenderResult:
        asset_id = spec.get("assetId")
        if not isinstance(asset_id, str) or not asset_id:
            raise ValueError("SVG render spec requires assetId")
        asset = self.manifest.get(asset_id)
        fit = spec.get("fit", "contain")
        if fit not in {"contain", "cover", "stretch"}:
            raise ValueError("SVG render fit must be contain, cover, or stretch")
        target_width = max(1, round(layer.bounds.width))
        target_height = max(1, round(layer.bounds.height))
        rendered, offset_x, offset_y, scale_x, scale_y = self._fit(
            asset, target_width, target_height, str(fit)
        )
        if spec.get("flipX"):
            rendered = rendered.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        opacity = layer.opacity
        if opacity < 1:
            alpha = rendered.getchannel("A").point(lambda value: round(value * opacity))
            rendered.putalpha(alpha)

        surface = context.surface
        if surface is not None:
            if not isinstance(surface, Image.Image):
                raise TypeError("SvgAssetRenderer requires a Pillow Image surface")
            surface.paste(
                rendered,
                (round(layer.bounds.x), round(layer.bounds.y)),
                rendered,
            )

        anchors = self._anchors(
            asset,
            layer.bounds,
            offset_x,
            offset_y,
            scale_x,
            scale_y,
            bool(spec.get("flipX")),
        )
        return RenderResult(
            renderer_id=self.renderer_id,
            layer_id=layer.id,
            bounds=layer.bounds,
            anchors=anchors,
            payload=rendered,
            metadata={"assetId": asset.id, "fit": fit},
        )

    def _fit(
        self, asset: DesignAsset, target_width: int, target_height: int, fit: str
    ) -> tuple[Image.Image, float, float, float, float]:
        _, _, source_width, source_height = asset.view_box
        if fit == "stretch":
            width, height = target_width, target_height
            scale_x, scale_y = width / source_width, height / source_height
        else:
            scales = (target_width / source_width, target_height / source_height)
            scale = max(scales) if fit == "cover" else min(scales)
            width, height = max(1, round(source_width * scale)), max(1, round(source_height * scale))
            scale_x = scale_y = scale
        scaled = self.rasterizer.rasterize(asset.path, width, height)
        offset_x = (target_width - width) / 2
        offset_y = (target_height - height) / 2
        image = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        image.paste(scaled, (round(offset_x), round(offset_y)), scaled)
        return image, offset_x, offset_y, scale_x, scale_y

    @staticmethod
    def _anchors(
        asset: DesignAsset,
        bounds: Bounds,
        offset_x: float,
        offset_y: float,
        scale_x: float,
        scale_y: float,
        flip_x: bool,
    ) -> Anchors:
        min_x, min_y, _, _ = asset.view_box
        points: dict[str, tuple[float, float]] = {}
        for name, (x, y) in asset.anchors.items():
            local_x = offset_x + (x - min_x) * scale_x
            if flip_x:
                local_x = bounds.width - local_x
            points[name] = (
                bounds.x + local_x,
                bounds.y + offset_y + (y - min_y) * scale_y,
            )
        return Anchors(points)
