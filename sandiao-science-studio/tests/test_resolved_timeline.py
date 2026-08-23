from pathlib import Path

from sandiao_studio.resolved_timeline import ResolvedShot, load_resolved_timeline, save_resolved_timeline
from sandiao_studio.story import load_story


def test_resolved_timeline_round_trip(tmp_path: Path) -> None:
    story = load_story("stories/ac-16c.json")
    shots = [
        ResolvedShot(shot.id, shot.duration, shot.duration + 0.5, shot.duration + 1.0)
        for shot in story.shots
    ]
    audio = tmp_path / "voice.wav"

    artifact = save_resolved_timeline(story, "mimo", shots, audio)
    resolved = load_resolved_timeline(story, audio)

    assert artifact.name == "voice.timeline.json"
    assert resolved is not None
    assert resolved.provider == "mimo"
    assert resolved.duration == story.duration + len(story.shots)
