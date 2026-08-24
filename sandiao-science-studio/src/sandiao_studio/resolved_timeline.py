from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from .story import Story


@dataclass(frozen=True)
class ResolvedShot:
    id: str
    planned_duration: float
    speech_duration: float
    duration: float


@dataclass(frozen=True)
class ResolvedTimeline:
    story_slug: str
    story_fingerprint: str
    provider: str
    shots: tuple[ResolvedShot, ...]

    @property
    def durations(self) -> tuple[float, ...]:
        return tuple(item.duration for item in self.shots)

    @property
    def duration(self) -> float:
        return sum(self.durations)


def story_fingerprint(story: Story) -> str:
    value = {
        "slug": story.slug,
        "characters": {key: item.voice for key, item in story.characters.items()},
        "shots": [
            {"id": shot.id, "duration": shot.duration, "speaker": shot.speaker, "dialogue": shot.dialogue}
            for shot in story.shots
        ],
    }
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def timeline_path(audio_path: str | Path) -> Path:
    return Path(audio_path).resolve().with_suffix(".timeline.json")


def save_resolved_timeline(story: Story, provider: str, shots: list[ResolvedShot], audio_path: str | Path) -> Path:
    artifact = {
        "schemaVersion": "1.0",
        "storySlug": story.slug,
        "storyFingerprint": story_fingerprint(story),
        "provider": provider,
        "duration": round(sum(item.duration for item in shots), 3),
        "shots": [
            {
                "id": item.id,
                "plannedDuration": round(item.planned_duration, 3),
                "speechDuration": round(item.speech_duration, 3),
                "duration": round(item.duration, 3),
            }
            for item in shots
        ],
    }
    output = timeline_path(audio_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def load_resolved_timeline(story: Story, audio_path: str | Path | None = None) -> ResolvedTimeline | None:
    path = timeline_path(audio_path or story.audio)
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw.get("schemaVersion") != "1.0" or raw.get("storySlug") != story.slug:
            return None
        if raw.get("storyFingerprint") != story_fingerprint(story):
            return None
        rows = raw.get("shots") or []
        if [row.get("id") for row in rows] != [shot.id for shot in story.shots]:
            return None
        shots = tuple(
            ResolvedShot(
                id=str(row["id"]),
                planned_duration=float(row["plannedDuration"]),
                speech_duration=float(row["speechDuration"]),
                duration=float(row["duration"]),
            )
            for row in rows
        )
        return ResolvedTimeline(
            story_slug=story.slug,
            story_fingerprint=str(raw["storyFingerprint"]),
            provider=str(raw.get("provider") or "unknown"),
            shots=shots,
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None
