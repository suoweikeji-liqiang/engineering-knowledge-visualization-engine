"""Minimal deterministic renderers useful in tests and early integration."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from .protocols import RenderSpec
from .types import Layer, RenderContext, RenderResult


@dataclass(frozen=True, slots=True)
class RenderCommand:
    """A backend-neutral command emitted by ``ProceduralTestRenderer``."""

    renderer_id: str
    layer_id: str
    frame_index: int
    progress: float
    spec: RenderSpec


@dataclass(frozen=True, slots=True)
class NoopRenderer:
    """A renderer that reports layer geometry without drawing anything."""

    renderer_id: str = "test.noop"

    def render(
        self,
        context: RenderContext,
        layer: Layer,
        spec: RenderSpec,
    ) -> RenderResult:
        del context, spec
        return RenderResult(
            renderer_id=self.renderer_id,
            layer_id=layer.id,
            bounds=layer.bounds,
            anchors=layer.anchors,
        )


@dataclass(frozen=True, slots=True)
class ProceduralTestRenderer:
    """Emits an immutable command; equal inputs always produce equal output."""

    renderer_id: str = "test.procedural"

    def render(
        self,
        context: RenderContext,
        layer: Layer,
        spec: RenderSpec,
    ) -> RenderResult:
        command = RenderCommand(
            renderer_id=self.renderer_id,
            layer_id=layer.id,
            frame_index=context.frame_index,
            progress=context.progress,
            spec=MappingProxyType(dict(spec)),
        )
        return RenderResult(
            renderer_id=self.renderer_id,
            layer_id=layer.id,
            bounds=layer.bounds,
            anchors=layer.anchors,
            payload=command,
            metadata={"deterministic": True},
        )
