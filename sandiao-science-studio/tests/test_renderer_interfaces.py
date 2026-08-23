from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from sandiao_studio.renderers import (
    Anchors,
    BackgroundRenderer,
    Bounds,
    CharacterRenderer,
    DiagramRenderer,
    DuplicateRendererError,
    Layer,
    RendererRegistry,
    RenderContext,
    SubtitleRenderer,
    UnknownRendererError,
)
from sandiao_studio.renderers.testing import NoopRenderer, ProceduralTestRenderer


def test_bounds_and_default_anchors_are_derived_from_layer() -> None:
    bounds = Bounds(x=10, y=20, width=100, height=60)
    layer = Layer(id="speaker", bounds=bounds)

    assert bounds.right == 110
    assert bounds.bottom == 80
    assert bounds.center == (60, 50)
    assert layer.anchors is not None
    assert layer.anchors.resolve("center") == (60, 50)
    assert layer.anchors.resolve("bottom_right") == (110, 80)


def test_context_progress_is_clamped_and_metadata_is_read_only() -> None:
    context = RenderContext(
        width=1920,
        height=1080,
        time_seconds=6,
        duration_seconds=4,
        variables={"palette": "brand"},
    )

    assert context.progress == 1.0
    assert context.frame_bounds == Bounds(0, 0, 1920, 1080)
    with pytest.raises(TypeError):
        context.variables["palette"] = "other"  # type: ignore[index]


@pytest.mark.parametrize(
    "factory",
    [
        lambda: Bounds(0, 0, -1, 1),
        lambda: Anchors({"bad": (float("inf"), 0)}),
        lambda: Layer("layer", Bounds(0, 0, 1, 1), opacity=1.1),
        lambda: RenderContext(width=0, height=1080),
    ],
)
def test_value_objects_reject_invalid_geometry(factory) -> None:
    with pytest.raises(ValueError):
        factory()


def test_registry_resolves_components_and_has_stable_id_order() -> None:
    registry: RendererRegistry[NoopRenderer] = RendererRegistry()
    second = NoopRenderer("z.component")
    first = NoopRenderer("a.component")

    registry.register_component(second)
    registry.register("a.component", first)

    assert registry.resolve("a.component") is first
    assert registry.ids() == ("a.component", "z.component")
    assert tuple(registry) == registry.ids()


def test_registry_reports_duplicate_and_unknown_ids_explicitly() -> None:
    registry: RendererRegistry[NoopRenderer] = RendererRegistry()
    registry.register_component(NoopRenderer("only.renderer"))

    with pytest.raises(DuplicateRendererError, match="already registered"):
        registry.register_component(NoopRenderer("only.renderer"))

    with pytest.raises(UnknownRendererError, match="missing.renderer") as error:
        registry.resolve("missing.renderer")
    assert "only.renderer" in str(error.value)


def test_component_contracts_accept_backend_neutral_renderer() -> None:
    renderer = ProceduralTestRenderer()

    assert isinstance(renderer, CharacterRenderer)
    assert isinstance(renderer, BackgroundRenderer)
    assert isinstance(renderer, DiagramRenderer)
    assert isinstance(renderer, SubtitleRenderer)


def test_procedural_renderer_is_deterministic() -> None:
    renderer = ProceduralTestRenderer("test.lines")
    context = RenderContext(
        width=1080,
        height=1920,
        time_seconds=1,
        duration_seconds=4,
        frame_index=30,
        surface=object(),
    )
    layer = Layer("diagram", Bounds(100, 200, 880, 700), z_index=3)
    spec = {"kind": "line", "points": ((0, 0), (1, 1))}

    first = renderer.render(context, layer, spec)
    second = renderer.render(context, layer, spec)

    assert first == second
    assert first.payload.progress == 0.25
    assert first.metadata["deterministic"] is True
    with pytest.raises(TypeError):
        first.payload.spec["kind"] = "circle"  # type: ignore[index,union-attr]


def test_frozen_layer_cannot_be_reassigned() -> None:
    layer = Layer("fixed", Bounds(0, 0, 10, 10))
    with pytest.raises(FrozenInstanceError):
        layer.opacity = 0.5  # type: ignore[misc]
