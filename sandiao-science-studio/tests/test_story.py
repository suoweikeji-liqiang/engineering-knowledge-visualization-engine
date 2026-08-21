from sandiao_studio.story import load_story


def test_sample_story() -> None:
    story = load_story("stories/ac-16c.json")
    assert story.slug == "ac-16c"
    assert len(story.shots) == 8
    assert story.duration == 32.0
    assert set(story.characters) == {"laowang", "xiaoming"}
