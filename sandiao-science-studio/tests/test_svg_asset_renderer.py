from __future__ import annotations

from pathlib import Path

from PIL import Image

from sandiao_studio.assets import load_asset_manifest
from sandiao_studio.renderers import Bounds, Layer, RenderContext, SvgAssetRenderer


FIXTURE = Path(__file__).parent / "fixtures/assets/manifests/design-assets.json"


class SolidRasterizer:
    def __init__(self) -> None:
        self.calls: list[tuple[Path, int, int]] = []

    def rasterize(self, path: Path, width: int, height: int) -> Image.Image:
        self.calls.append((path, width, height))
        return Image.new("RGBA", (width, height), (240, 75, 47, 255))


def test_svg_asset_renderer_composites_and_resolves_manifest_anchors() -> None:
    manifest = load_asset_manifest(FIXTURE)
    rasterizer = SolidRasterizer()
    renderer = SvgAssetRenderer(manifest, rasterizer=rasterizer)
    surface = Image.new("RGBA", (200, 160), (0, 0, 0, 0))
    context = RenderContext(width=200, height=160, surface=surface)
    layer = Layer("thermometer", Bounds(20, 20, 80, 120))

    result = renderer.render(
        context,
        layer,
        {"assetId": "prop.thermometer.default", "fit": "contain"},
    )

    assert rasterizer.calls[0][1:] == (80, 120)
    assert surface.getpixel((60, 80))[3] == 255
    assert result.anchors is not None
    assert result.anchors.resolve("center") == (60, 80)
    assert result.metadata["assetId"] == "prop.thermometer.default"


def test_svg_asset_renderer_flips_anchor_within_layer() -> None:
    manifest = load_asset_manifest(FIXTURE)
    renderer = SvgAssetRenderer(manifest, rasterizer=SolidRasterizer())
    layer = Layer("thermometer", Bounds(10, 10, 160, 120))

    result = renderer.render(
        RenderContext(width=200, height=160),
        layer,
        {"assetId": "prop.thermometer.default", "fit": "contain", "flipX": True},
    )

    assert result.anchors is not None
    # The 2:3 asset is centered in a 4:3 layer, leaving 40px on either side.
    assert result.anchors.resolve("center") == (90, 70)
    assert result.anchors.resolve("label") == (90, 10)
