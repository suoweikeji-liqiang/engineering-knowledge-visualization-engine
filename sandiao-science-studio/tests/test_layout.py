import pytest

from sandiao_studio.layout import LayoutEngine, LayoutError, LayoutRequest, Orientation


@pytest.mark.parametrize("size", [(960, 540), (1920, 1080), (1080, 1920)])
@pytest.mark.parametrize("characters", [0, 1, 2])
@pytest.mark.parametrize("diagram", [False, True])
def test_default_layouts_stay_inside_safe_area_and_do_not_overlap(size, characters, diagram) -> None:
    plan = LayoutEngine().plan(LayoutRequest(*size, character_count=characters, has_diagram=diagram))
    assert plan.safe_area.width > 0
    assert len(plan.characters) == characters
    assert (plan.diagram is not None) is diagram


def test_portrait_is_reflowed_instead_of_cropped() -> None:
    plan = LayoutEngine().plan(LayoutRequest(1080, 1920, character_count=2, has_diagram=True))
    assert LayoutRequest(1080, 1920).orientation is Orientation.PORTRAIT
    assert plan.diagram is not None
    assert plan.diagram.bottom < plan.characters[0].y


def test_landscape_places_characters_around_diagram() -> None:
    plan = LayoutEngine().plan(LayoutRequest(1920, 1080, character_count=2, has_diagram=True))
    assert plan.diagram is not None
    assert plan.characters[0].right < plan.diagram.x
    assert plan.diagram.right < plan.characters[1].x


def test_rejects_unsupported_character_count() -> None:
    with pytest.raises(LayoutError, match="zero, one, or two"):
        LayoutEngine().plan(LayoutRequest(960, 540, character_count=3))
