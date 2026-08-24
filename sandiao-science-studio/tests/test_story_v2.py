from __future__ import annotations

from copy import deepcopy

import pytest

from sandiao_studio.story import StoryError, parse_story
from sandiao_studio.story_migration import migrate_story_data


def _v2_story() -> dict:
    return {
        "schemaVersion": "2.0",
        "meta": {"title": "测试", "slug": "test-story", "resolution": [960, 540], "fps": 15},
        "characters": [
            {
                "id": "observer",
                "name": "观察员",
                "palette": {"accent": "#38D8E8"},
                "renderer": {
                    "type": "svg-sprite",
                    "variant": "default",
                    "assetRef": {"id": "character.observer", "variant": "default"},
                },
            }
        ],
        "shots": [
            {
                "id": "explain",
                "duration": 2.5,
                "speaker": "observer",
                "dialogue": "先观察，再验证。",
                "states": [
                    {
                        "character": "observer",
                        "x": 0.25,
                        "y": 0.65,
                        "action": {"id": "point", "intensity": 0.7, "parameters": {"hand": "right"}},
                        "expression": {"id": "determined", "intensity": 0.8},
                    }
                ],
                "scene": {
                    "id": "scene.observation",
                    "background": {
                        "id": "background.observatory",
                        "variant": "day",
                        "mood": "focused",
                        "assetRef": {"id": "background.observatory", "variant": "day"},
                    },
                    "layout": {
                        "preset": "dialogue-diagram",
                        "focus": "diagram",
                        "safeArea": [0.05, 0.05, 0.15, 0.05],
                        "zones": {"character-left": [0.05, 0.1, 0.3, 0.7], "diagram": [0.4, 0.1, 0.55, 0.65]},
                    },
                    "camera": {
                        "framing": "medium-wide",
                        "movement": "push-in",
                        "target": "diagram",
                        "intensity": 0.25,
                    },
                    "assetRefs": [
                        {"id": "prop.thermometer", "role": "prop", "parameters": {"state": "cold"}}
                    ],
                },
            }
        ],
    }


def test_v1_sample_is_loaded_as_v2() -> None:
    from sandiao_studio.story import load_story

    story = load_story("stories/ac-16c.json")
    assert story.schema_version == "2.0"
    assert story.duration == 32.0
    assert story.characters["laowang"].renderer.type == "procedural"
    assert story.shots[0].scene is not None
    assert story.shots[0].states[0].action == "talk"
    assert story.shots[0].states[0].action_cue.id == "talk"


def test_v1_migration_is_deterministic_and_non_mutating() -> None:
    legacy = {
        "meta": {"title": "T", "slug": "t", "resolution": [640, 360]},
        "characters": [{"id": "host", "name": "H", "palette": {}}],
        "shots": [
            {
                "id": "intro",
                "duration": 1,
                "states": [{"character": "host", "x": 0.5, "y": 0.5, "action": "talk"}],
            }
        ],
    }
    original = deepcopy(legacy)

    first = migrate_story_data(legacy)
    second = migrate_story_data(legacy)

    assert legacy == original
    assert first == second
    assert first["schemaVersion"] == "2.0"
    assert first["characters"][0]["renderer"] == {"type": "procedural"}
    assert first["shots"][0]["states"][0]["action"] == {"id": "talk"}
    assert first["shots"][0]["states"][0]["expression"] == {"id": "neutral"}


def test_v2_semantic_visual_fields_are_parsed() -> None:
    story = parse_story(_v2_story())
    character = story.characters["observer"]
    state = story.shots[0].states[0]
    scene = story.shots[0].scene

    assert character.renderer.type == "svg-sprite"
    assert character.renderer.asset_ref is not None
    assert character.renderer.asset_ref.id == "character.observer"
    assert state.action == "point"
    assert state.action_cue.intensity == 0.7
    assert state.action_cue.parameters == {"hand": "right"}
    assert state.expression == "determined"
    assert scene is not None and scene.background is not None
    assert scene.background.id == "background.observatory"
    assert scene.layout is not None
    assert scene.layout.zones["diagram"] == (0.4, 0.1, 0.55, 0.65)
    assert scene.camera is not None and scene.camera.movement == "push-in"
    assert scene.asset_refs[0].id == "prop.thermometer"


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda raw: raw["shots"][0]["states"][0].update(action={"id": "moonwalk"}), "unknown action id"),
        (lambda raw: raw["shots"][0]["scene"]["layout"].update(zones={"bad": [0.8, 0.1, 0.3, 0.2]}), "normalized canvas"),
        (lambda raw: raw["characters"][0]["renderer"].pop("assetRef"), "assetRef is required"),
    ],
)
def test_v2_rejects_invalid_visual_contract(mutate, message: str) -> None:
    raw = _v2_story()
    mutate(raw)
    with pytest.raises(StoryError, match=message):
        parse_story(raw)


def test_unknown_schema_version_is_rejected() -> None:
    raw = _v2_story()
    raw["schemaVersion"] = "3.0"
    with pytest.raises(StoryError, match="unsupported story schemaVersion"):
        parse_story(raw)
