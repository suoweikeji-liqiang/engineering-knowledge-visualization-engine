"""Backend-neutral value objects shared by renderer components.

The objects in this module deliberately describe composition semantics rather
than drawing primitives.  A renderer may put a Pillow image, an SVG document,
or a backend-specific command buffer in ``RenderContext.surface`` and
``RenderResult.payload`` without changing the orchestration contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from typing import Any, Mapping, TypeAlias


Point: TypeAlias = tuple[float, float]


def _frozen_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return a shallow, read-only copy so callers cannot mutate context state."""

    return MappingProxyType(dict(value))


@dataclass(frozen=True, slots=True)
class Bounds:
    """An axis-aligned rectangle in the context's coordinate space."""

    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        values = (self.x, self.y, self.width, self.height)
        if not all(isfinite(value) for value in values):
            raise ValueError("bounds values must be finite")
        if self.width < 0 or self.height < 0:
            raise ValueError("bounds width and height must be non-negative")

    @property
    def left(self) -> float:
        return self.x

    @property
    def top(self) -> float:
        return self.y

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center(self) -> Point:
        return (self.x + self.width / 2, self.y + self.height / 2)


@dataclass(frozen=True, slots=True)
class Anchors:
    """Named attachment points expressed in the same space as ``Bounds``."""

    points: Mapping[str, Point] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized: dict[str, Point] = {}
        for name, point in self.points.items():
            if not name or not name.strip():
                raise ValueError("anchor names must be non-empty")
            if len(point) != 2 or not all(isfinite(value) for value in point):
                raise ValueError(f"anchor {name!r} must contain two finite values")
            normalized[name] = (float(point[0]), float(point[1]))
        object.__setattr__(self, "points", MappingProxyType(normalized))

    def resolve(self, name: str) -> Point:
        try:
            return self.points[name]
        except KeyError as exc:
            raise KeyError(f"unknown anchor: {name!r}") from exc

    @classmethod
    def from_bounds(cls, bounds: Bounds) -> Anchors:
        """Create the common nine-point anchors for a rectangle."""

        center_x, center_y = bounds.center
        return cls(
            {
                "top_left": (bounds.left, bounds.top),
                "top": (center_x, bounds.top),
                "top_right": (bounds.right, bounds.top),
                "left": (bounds.left, center_y),
                "center": (center_x, center_y),
                "right": (bounds.right, center_y),
                "bottom_left": (bounds.left, bounds.bottom),
                "bottom": (center_x, bounds.bottom),
                "bottom_right": (bounds.right, bounds.bottom),
            }
        )


@dataclass(frozen=True, slots=True)
class Layer:
    """A compositing layer allocated to one renderer component."""

    id: str
    bounds: Bounds
    z_index: int = 0
    opacity: float = 1.0
    anchors: Anchors | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise ValueError("layer id must be non-empty")
        if not isfinite(self.opacity) or not 0 <= self.opacity <= 1:
            raise ValueError("layer opacity must be between 0 and 1")
        if self.anchors is None:
            object.__setattr__(self, "anchors", Anchors.from_bounds(self.bounds))
        object.__setattr__(self, "metadata", _frozen_mapping(self.metadata))


@dataclass(frozen=True, slots=True)
class RenderContext:
    """Frame-level state supplied to every renderer.

    ``surface`` is intentionally typed as ``object``.  Pillow users can pass an
    ``Image`` or ``ImageDraw`` instance; non-Pillow backends can pass their own
    canvas or command buffer.
    """

    width: int
    height: int
    time_seconds: float = 0.0
    duration_seconds: float = 0.0
    frame_index: int = 0
    fps: float = 30.0
    scene_id: str = ""
    locale: str = "zh-CN"
    seed: int = 0
    surface: object | None = None
    variables: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("render dimensions must be positive")
        if not isfinite(self.time_seconds) or self.time_seconds < 0:
            raise ValueError("time_seconds must be finite and non-negative")
        if not isfinite(self.duration_seconds) or self.duration_seconds < 0:
            raise ValueError("duration_seconds must be finite and non-negative")
        if not isfinite(self.fps) or self.fps <= 0:
            raise ValueError("fps must be finite and positive")
        if self.frame_index < 0:
            raise ValueError("frame_index must be non-negative")
        object.__setattr__(self, "variables", _frozen_mapping(self.variables))

    @property
    def frame_bounds(self) -> Bounds:
        return Bounds(0, 0, float(self.width), float(self.height))

    @property
    def progress(self) -> float:
        if self.duration_seconds == 0:
            return 0.0
        return min(1.0, self.time_seconds / self.duration_seconds)


@dataclass(frozen=True, slots=True)
class RenderResult:
    """Observable output of rendering one layer."""

    renderer_id: str
    layer_id: str
    bounds: Bounds
    anchors: Anchors | None = None
    payload: object | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.renderer_id or not self.renderer_id.strip():
            raise ValueError("renderer_id must be non-empty")
        if not self.layer_id or not self.layer_id.strip():
            raise ValueError("layer_id must be non-empty")
        if self.anchors is None:
            object.__setattr__(self, "anchors", Anchors.from_bounds(self.bounds))
        object.__setattr__(self, "metadata", _frozen_mapping(self.metadata))
        object.__setattr__(self, "warnings", tuple(self.warnings))
