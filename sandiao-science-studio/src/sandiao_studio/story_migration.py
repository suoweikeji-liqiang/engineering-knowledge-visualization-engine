from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


LEGACY_SCHEMA_VERSION = "1.0"
CURRENT_SCHEMA_VERSION = "2.0"


class StoryMigrationError(ValueError):
    """Raised when a Story document cannot be migrated safely."""


def detect_story_version(document: Mapping[str, Any]) -> str:
    """Return the declared Story version, treating an absent version as v1."""

    value = document.get("schemaVersion", LEGACY_SCHEMA_VERSION)
    if not isinstance(value, str) or not value:
        raise StoryMigrationError("root.schemaVersion must be a non-empty string")
    return value


def migrate_story_data(
    document: Mapping[str, Any], target_version: str = CURRENT_SCHEMA_VERSION
) -> dict[str, Any]:
    """Return a migrated deep copy without mutating *document*.

    The function is deliberately independent of files and the command-line layer so
    authoring tools can migrate an in-memory JSON document before validating it.
    """

    if not isinstance(document, Mapping):
        raise StoryMigrationError("story root must be an object")
    if target_version != CURRENT_SCHEMA_VERSION:
        raise StoryMigrationError(f"unsupported migration target: {target_version}")

    version = detect_story_version(document)
    if version == CURRENT_SCHEMA_VERSION:
        return deepcopy(dict(document))
    if version != LEGACY_SCHEMA_VERSION:
        raise StoryMigrationError(f"unsupported story schemaVersion: {version}")
    return migrate_v1_to_v2(document)


def migrate_v1_to_v2(document: Mapping[str, Any]) -> dict[str, Any]:
    """Apply the one supported migration step and return a deep copy."""

    if detect_story_version(document) != LEGACY_SCHEMA_VERSION:
        raise StoryMigrationError("migrate_v1_to_v2 requires a v1 Story document")
    migrated = deepcopy(dict(document))
    migrated["schemaVersion"] = CURRENT_SCHEMA_VERSION

    characters = migrated.get("characters")
    if isinstance(characters, list):
        for character in characters:
            if isinstance(character, dict):
                character.setdefault("renderer", {"type": "procedural"})

    shots = migrated.get("shots")
    if isinstance(shots, list):
        for shot in shots:
            if not isinstance(shot, dict):
                continue
            shot.setdefault(
                "scene",
                {
                    "id": "scene.default",
                    "background": {"id": "background.default", "variant": "default"},
                    "layout": {"preset": "legacy-normalized"},
                    "camera": {"framing": "wide", "movement": "static"},
                },
            )
            states = shot.get("states")
            if not isinstance(states, list):
                continue
            for state in states:
                if not isinstance(state, dict):
                    continue
                action = state.get("action", "idle")
                if isinstance(action, str):
                    state["action"] = {"id": action}
                expression = state.get("expression", "neutral")
                if isinstance(expression, str):
                    state["expression"] = {"id": expression}

    return migrated
