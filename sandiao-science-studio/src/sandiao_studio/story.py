from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class StoryError(ValueError):
    pass


@dataclass(frozen=True)
class Character:
    id: str
    name: str
    palette: dict[str, str]
    voice: dict[str, Any]


@dataclass(frozen=True)
class State:
    character: str
    x: float
    y: float
    scale: float
    facing: int
    action: str
    expression: str


@dataclass(frozen=True)
class Shot:
    id: str
    duration: float
    speaker: str | None
    dialogue: str
    headline: str
    diagram: str
    effect: str
    transition: str
    sfx: tuple[str, ...]
    states: tuple[State, ...]


@dataclass(frozen=True)
class Story:
    source: Path
    title: str
    slug: str
    episode: str
    width: int
    height: int
    fps: int
    video: Path
    audio: Path
    poster: Path
    characters: dict[str, Character]
    shots: tuple[Shot, ...]

    @property
    def duration(self) -> float:
        return sum(s.duration for s in self.shots)


def _need(data: dict[str, Any], key: str, where: str) -> Any:
    if key not in data:
        raise StoryError(f"missing {where}.{key}")
    return data[key]


def load_story(path: str | Path) -> Story:
    source = Path(path).resolve()
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StoryError(f"story not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise StoryError(f"invalid JSON line {exc.lineno}: {exc.msg}") from exc

    meta = _need(raw, "meta", "root")
    resolution = _need(meta, "resolution", "meta")
    if not isinstance(resolution, list) or len(resolution) != 2:
        raise StoryError("meta.resolution must be [width, height]")
    width, height = int(resolution[0]), int(resolution[1])
    fps = int(meta.get("fps", 12))
    if width < 640 or height < 360:
        raise StoryError("minimum resolution is 640x360")
    if not 10 <= fps <= 60:
        raise StoryError("fps must be 10..60")

    chars: dict[str, Character] = {}
    for i, item in enumerate(_need(raw, "characters", "root")):
        cid = str(_need(item, "id", f"characters[{i}]"))
        if cid in chars:
            raise StoryError(f"duplicate character: {cid}")
        chars[cid] = Character(
            id=cid,
            name=str(_need(item, "name", f"characters[{i}]")),
            palette=dict(_need(item, "palette", f"characters[{i}]")),
            voice=dict(item.get("voice", {})),
        )

    shots: list[Shot] = []
    ids: set[str] = set()
    for i, item in enumerate(_need(raw, "shots", "root")):
        sid = str(_need(item, "id", f"shots[{i}]"))
        if sid in ids:
            raise StoryError(f"duplicate shot: {sid}")
        ids.add(sid)
        duration = float(_need(item, "duration", f"shots[{i}]"))
        if duration <= 0.5:
            raise StoryError(f"shot {sid} is too short")
        speaker = item.get("speaker")
        if speaker is not None and speaker not in chars:
            raise StoryError(f"unknown speaker {speaker} in {sid}")
        states: list[State] = []
        for j, state in enumerate(item.get("states", [])):
            cid = str(_need(state, "character", f"shots[{i}].states[{j}]"))
            if cid not in chars:
                raise StoryError(f"unknown character {cid} in {sid}")
            x, y = float(state["x"]), float(state["y"])
            if not (0 <= x <= 1 and 0 <= y <= 1):
                raise StoryError(f"state coordinates must be normalized in {sid}")
            states.append(
                State(
                    character=cid,
                    x=x,
                    y=y,
                    scale=float(state.get("scale", 1.0)),
                    facing=1 if int(state.get("facing", 1)) >= 0 else -1,
                    action=str(state.get("action", "idle")),
                    expression=str(state.get("expression", "neutral")),
                )
            )
        shots.append(
            Shot(
                id=sid,
                duration=duration,
                speaker=str(speaker) if speaker is not None else None,
                dialogue=str(item.get("dialogue", "")),
                headline=str(item.get("headline", "")),
                diagram=str(item.get("diagram", "")),
                effect=str(item.get("effect", "")),
                transition=str(item.get("transition", "fade")),
                sfx=tuple(str(v) for v in item.get("sfx", [])),
                states=tuple(states),
            )
        )

    slug = str(_need(meta, "slug", "meta"))
    return Story(
        source=source,
        title=str(_need(meta, "title", "meta")),
        slug=slug,
        episode=str(meta.get("episode", "01")),
        width=width,
        height=height,
        fps=fps,
        video=Path(meta.get("video", f"output/{slug}.mp4")),
        audio=Path(meta.get("audio", f"output/{slug}.wav")),
        poster=Path(meta.get("poster", f"output/{slug}-poster.png")),
        characters=chars,
        shots=tuple(shots),
    )
