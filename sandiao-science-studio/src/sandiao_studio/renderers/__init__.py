"""Public renderer component contracts."""

from .protocols import (
    BackgroundRenderer,
    CharacterRenderer,
    DiagramRenderer,
    RenderSpec,
    SubtitleRenderer,
)
from .registry import (
    DuplicateRendererError,
    RendererRegistry,
    RendererRegistryError,
    UnknownRendererError,
)
from .svg_asset import SvgAssetRenderer, SvgRasterizationError, SvgRasterizer
from .types import Anchors, Bounds, Layer, Point, RenderContext, RenderResult

__all__ = [
    "Anchors",
    "BackgroundRenderer",
    "Bounds",
    "CharacterRenderer",
    "DiagramRenderer",
    "DuplicateRendererError",
    "Layer",
    "Point",
    "RendererRegistry",
    "RendererRegistryError",
    "RenderContext",
    "RenderResult",
    "RenderSpec",
    "SubtitleRenderer",
    "SvgAssetRenderer",
    "SvgRasterizationError",
    "SvgRasterizer",
    "UnknownRendererError",
]
