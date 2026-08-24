from sandiao_studio.engine import Timeline
from sandiao_studio.story import load_story


def test_timeline() -> None:
    story = load_story("stories/ac-16c.json")
    timeline = Timeline(story)
    assert timeline.locate(0).shot.id == "hook"
    assert timeline.locate(3.7).shot.id == "not-faucet"
    assert timeline.locate(999).shot.id == "end"


def test_programmatic_sfx_is_deterministic() -> None:
    import numpy as np

    from sandiao_studio.engine import _sfx

    assert np.array_equal(_sfx("whoosh"), _sfx("whoosh"))
