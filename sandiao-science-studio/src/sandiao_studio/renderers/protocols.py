"""Structural interfaces for independently replaceable renderer components."""

from __future__ import annotations

from typing import Any, Mapping, Protocol, runtime_checkable

from .types import Layer, RenderContext, RenderResult


RenderSpec = Mapping[str, Any]


class _ComponentRenderer(Protocol):
    renderer_id: str

    def render(
        self,
        context: RenderContext,
        layer: Layer,
        spec: RenderSpec,
    ) -> RenderResult:
        """Render ``spec`` into the optional context surface and return metadata."""


@runtime_checkable
class CharacterRenderer(_ComponentRenderer, Protocol):
    """Renders a character pose, expression, and action description."""


@runtime_checkable
class BackgroundRenderer(_ComponentRenderer, Protocol):
    """Renders an environment or backdrop description."""


@runtime_checkable
class DiagramRenderer(_ComponentRenderer, Protocol):
    """Renders a domain-neutral diagram description."""


@runtime_checkable
class SubtitleRenderer(_ComponentRenderer, Protocol):
    """Renders subtitle text and its presentation description."""
