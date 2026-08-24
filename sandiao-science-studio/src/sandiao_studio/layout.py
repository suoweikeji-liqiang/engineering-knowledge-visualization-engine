from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LayoutError(ValueError):
    pass


class Orientation(str, Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def inset(self, horizontal: float, vertical: float | None = None) -> "Rect":
        vertical = horizontal if vertical is None else vertical
        width = self.width - horizontal * 2
        height = self.height - vertical * 2
        if width <= 0 or height <= 0:
            raise LayoutError("inset leaves no usable rectangle")
        return Rect(self.x + horizontal, self.y + vertical, width, height)

    def contains(self, other: "Rect", tolerance: float = 1e-6) -> bool:
        return (
            other.x >= self.x - tolerance
            and other.y >= self.y - tolerance
            and other.right <= self.right + tolerance
            and other.bottom <= self.bottom + tolerance
        )

    def overlaps(self, other: "Rect", gap: float = 0.0) -> bool:
        return not (
            self.right + gap <= other.x
            or other.right + gap <= self.x
            or self.bottom + gap <= other.y
            or other.bottom + gap <= self.y
        )

    def normalized(self, width: float, height: float) -> "Rect":
        if width <= 0 or height <= 0:
            raise LayoutError("canvas dimensions must be positive")
        return Rect(self.x / width, self.y / height, self.width / width, self.height / height)


@dataclass(frozen=True)
class LayoutRequest:
    width: int
    height: int
    character_count: int = 2
    has_diagram: bool = True
    has_headline: bool = True
    subtitle_lines: int = 2

    @property
    def orientation(self) -> Orientation:
        return Orientation.LANDSCAPE if self.width >= self.height else Orientation.PORTRAIT


@dataclass(frozen=True)
class LayoutPlan:
    canvas: Rect
    safe_area: Rect
    headline: Rect | None
    stage: Rect
    diagram: Rect | None
    characters: tuple[Rect, ...]
    subtitle: Rect | None

    def regions(self) -> dict[str, Rect]:
        regions = {"safe_area": self.safe_area, "stage": self.stage}
        if self.headline:
            regions["headline"] = self.headline
        if self.diagram:
            regions["diagram"] = self.diagram
        if self.subtitle:
            regions["subtitle"] = self.subtitle
        regions.update({f"character_{index + 1}": item for index, item in enumerate(self.characters)})
        return regions


class LayoutEngine:
    """Deterministic default slots; a future design manifest may override ratios."""

    def plan(self, request: LayoutRequest) -> LayoutPlan:
        self._validate_request(request)
        if request.orientation is Orientation.LANDSCAPE:
            plan = self._landscape(request)
        else:
            plan = self._portrait(request)
        self.validate(plan)
        return plan

    def _validate_request(self, request: LayoutRequest) -> None:
        if request.width < 320 or request.height < 320:
            raise LayoutError("minimum canvas dimension is 320px")
        if not 0 <= request.character_count <= 2:
            raise LayoutError("default layouts support zero, one, or two characters")
        if not 0 <= request.subtitle_lines <= 3:
            raise LayoutError("subtitle_lines must be 0..3")

    def _landscape(self, request: LayoutRequest) -> LayoutPlan:
        width, height = float(request.width), float(request.height)
        canvas = Rect(0, 0, width, height)
        safe = Rect(width * .035, height * .035, width * .93, height * .93)
        gap = height * .025
        headline_h = height * .12 if request.has_headline else 0
        subtitle_h = height * (.12 + .035 * max(request.subtitle_lines - 1, 0)) if request.subtitle_lines else 0
        headline = Rect(safe.x, safe.y, safe.width, headline_h) if headline_h else None
        subtitle = Rect(safe.x, safe.bottom - subtitle_h, safe.width, subtitle_h) if subtitle_h else None
        stage_top = headline.bottom + gap if headline else safe.y
        stage_bottom = subtitle.y - gap if subtitle else safe.bottom
        stage = Rect(safe.x, stage_top, safe.width, stage_bottom - stage_top)

        diagram: Rect | None = None
        characters: tuple[Rect, ...] = ()
        if request.has_diagram and request.character_count == 2:
            char_w = stage.width * .205
            diagram_gap = stage.width * .025
            diagram_x = stage.x + char_w + diagram_gap
            diagram_w = stage.width - 2 * (char_w + diagram_gap)
            characters = (
                Rect(stage.x, stage.y, char_w, stage.height),
                Rect(stage.right - char_w, stage.y, char_w, stage.height),
            )
            diagram = Rect(diagram_x, stage.y, diagram_w, stage.height)
        elif request.has_diagram and request.character_count == 1:
            char_w = stage.width * .28
            split_gap = stage.width * .035
            characters = (Rect(stage.x, stage.y, char_w, stage.height),)
            diagram = Rect(stage.x + char_w + split_gap, stage.y, stage.width - char_w - split_gap, stage.height)
        elif request.has_diagram:
            diagram = stage
        elif request.character_count:
            gap_w = stage.width * .04
            total_w = stage.width * (.38 if request.character_count == 1 else .72)
            slot_w = (total_w - gap_w * (request.character_count - 1)) / request.character_count
            start_x = stage.x + (stage.width - total_w) / 2
            characters = tuple(
                Rect(start_x + index * (slot_w + gap_w), stage.y, slot_w, stage.height)
                for index in range(request.character_count)
            )
        return LayoutPlan(canvas, safe, headline, stage, diagram, characters, subtitle)

    def _portrait(self, request: LayoutRequest) -> LayoutPlan:
        width, height = float(request.width), float(request.height)
        canvas = Rect(0, 0, width, height)
        safe = Rect(width * .055, height * .025, width * .89, height * .95)
        gap = height * .018
        headline_h = height * .095 if request.has_headline else 0
        subtitle_h = height * (.085 + .026 * max(request.subtitle_lines - 1, 0)) if request.subtitle_lines else 0
        headline = Rect(safe.x, safe.y, safe.width, headline_h) if headline_h else None
        subtitle = Rect(safe.x, safe.bottom - subtitle_h, safe.width, subtitle_h) if subtitle_h else None
        stage_top = headline.bottom + gap if headline else safe.y
        stage_bottom = subtitle.y - gap if subtitle else safe.bottom
        stage = Rect(safe.x, stage_top, safe.width, stage_bottom - stage_top)

        diagram: Rect | None = None
        characters: tuple[Rect, ...] = ()
        if request.has_diagram and request.character_count:
            diagram_h = stage.height * .55
            split_gap = stage.height * .025
            diagram = Rect(stage.x, stage.y, stage.width, diagram_h)
            character_stage = Rect(stage.x, stage.y + diagram_h + split_gap, stage.width, stage.height - diagram_h - split_gap)
            gap_w = character_stage.width * .04
            slot_w = (character_stage.width - gap_w * (request.character_count - 1)) / request.character_count
            characters = tuple(
                Rect(character_stage.x + index * (slot_w + gap_w), character_stage.y, slot_w, character_stage.height)
                for index in range(request.character_count)
            )
        elif request.has_diagram:
            diagram = stage
        elif request.character_count:
            gap_w = stage.width * .04
            slot_w = (stage.width - gap_w * (request.character_count - 1)) / request.character_count
            characters = tuple(
                Rect(stage.x + index * (slot_w + gap_w), stage.y, slot_w, stage.height)
                for index in range(request.character_count)
            )
        return LayoutPlan(canvas, safe, headline, stage, diagram, characters, subtitle)

    def validate(self, plan: LayoutPlan) -> None:
        for name, region in plan.regions().items():
            if region.width <= 0 or region.height <= 0:
                raise LayoutError(f"{name} has no usable area")
            container = plan.canvas if name == "safe_area" else plan.safe_area
            if not container.contains(region):
                raise LayoutError(f"{name} escapes its safe container")

        exclusive: list[tuple[str, Rect]] = []
        if plan.headline:
            exclusive.append(("headline", plan.headline))
        if plan.diagram:
            exclusive.append(("diagram", plan.diagram))
        exclusive.extend((f"character_{index + 1}", item) for index, item in enumerate(plan.characters))
        if plan.subtitle:
            exclusive.append(("subtitle", plan.subtitle))
        for index, (left_name, left) in enumerate(exclusive):
            for right_name, right in exclusive[index + 1:]:
                if left.overlaps(right):
                    raise LayoutError(f"{left_name} overlaps {right_name}")
