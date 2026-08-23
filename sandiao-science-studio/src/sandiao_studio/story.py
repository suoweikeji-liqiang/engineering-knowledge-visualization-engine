from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .story_migration import CURRENT_SCHEMA_VERSION, StoryMigrationError, migrate_story_data


class StoryError(ValueError):
    pass


@dataclass(frozen=True)
class Character:
    id: str
    name: str
    palette: dict[str, str]
    voice: dict[str, Any]
    renderer: CharacterRenderer


@dataclass(frozen=True)
class AssetRef:
    """A semantic asset reference. IDs are resolved by an asset manifest later."""

    id: str
    variant: str | None
    role: str | None
    parameters: dict[str, Any]


@dataclass(frozen=True)
class CharacterRenderer:
    type: str
    asset_ref: AssetRef | None
    variant: str | None


@dataclass(frozen=True)
class Cue:
    id: str
    intensity: float
    parameters: dict[str, Any]


@dataclass(frozen=True)
class Background:
    id: str
    variant: str | None
    mood: str | None
    asset_ref: AssetRef | None


@dataclass(frozen=True)
class Layout:
    preset: str
    focus: str | None
    safe_area: tuple[float, float, float, float] | None
    zones: dict[str, tuple[float, float, float, float]]


@dataclass(frozen=True)
class Camera:
    framing: str
    movement: str
    target: str | None
    intensity: float


@dataclass(frozen=True)
class Scene:
    id: str
    background: Background | None
    layout: Layout | None
    camera: Camera | None
    asset_refs: tuple[AssetRef, ...]


@dataclass(frozen=True)
class State:
    character: str
    x: float
    y: float
    scale: float
    facing: int
    action: str
    expression: str
    action_cue: Cue
    expression_cue: Cue


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
    scene: Scene | None


@dataclass(frozen=True)
class Story:
    source: Path
    schema_version: str
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


_ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_RENDERER_TYPES = {"procedural", "svg-sprite", "png-pose-pack"}
_ACTION_IDS = {
    "idle", "talk", "point", "shock", "think", "nod", "shake", "celebrate",
    "walk", "run", "angry", "laugh", "cry", "sweat", "whisper",
}
_EXPRESSION_IDS = {
    "neutral", "happy", "confident", "serious", "puzzled", "shocked", "angry",
    "tired", "laugh", "cry", "embarrassed", "determined", "smile",
}
_CAMERA_FRAMINGS = {
    "extreme-wide", "wide", "medium-wide", "medium", "medium-close", "close-up",
    "extreme-close-up",
}
_CAMERA_MOVEMENTS = {"static", "push-in", "pull-out", "pan", "follow", "cut"}


def _object(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise StoryError(f"{where} must be an object")
    return value


def _array(value: Any, where: str) -> list[Any]:
    if not isinstance(value, list):
        raise StoryError(f"{where} must be an array")
    return value


def _id(value: Any, where: str) -> str:
    result = str(value)
    if not _ID_PATTERN.fullmatch(result):
        raise StoryError(f"{where} must be a semantic id")
    return result


def _optional_text(value: Any, where: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise StoryError(f"{where} must be a non-empty string")
    return value


def _unit(value: Any, where: str, default: float = 1.0) -> float:
    try:
        result = float(default if value is None else value)
    except (TypeError, ValueError) as exc:
        raise StoryError(f"{where} must be a number from 0 to 1") from exc
    if not 0 <= result <= 1:
        raise StoryError(f"{where} must be from 0 to 1")
    return result


def _parameters(value: Any, where: str) -> dict[str, Any]:
    if value is None:
        return {}
    return dict(_object(value, where))


def _asset_ref(value: Any, where: str) -> AssetRef:
    item = _object(value, where)
    return AssetRef(
        id=_id(_need(item, "id", where), f"{where}.id"),
        variant=_optional_text(item.get("variant"), f"{where}.variant"),
        role=_optional_text(item.get("role"), f"{where}.role"),
        parameters=_parameters(item.get("parameters"), f"{where}.parameters"),
    )


def _renderer(value: Any, where: str) -> CharacterRenderer:
    item = _object(value, where)
    renderer_type = str(item.get("type", "procedural"))
    if renderer_type not in _RENDERER_TYPES:
        raise StoryError(f"{where}.type must be one of {sorted(_RENDERER_TYPES)}")
    asset = item.get("assetRef")
    asset_ref = _asset_ref(asset, f"{where}.assetRef") if asset is not None else None
    if renderer_type != "procedural" and asset_ref is None:
        raise StoryError(f"{where}.assetRef is required for {renderer_type}")
    return CharacterRenderer(
        type=renderer_type,
        asset_ref=asset_ref,
        variant=_optional_text(item.get("variant"), f"{where}.variant"),
    )


def _cue(value: Any, where: str, default: str, known: set[str]) -> Cue:
    item = _object({"id": default} if value is None else value, where)
    cue_id = _id(_need(item, "id", where), f"{where}.id")
    if cue_id not in known:
        raise StoryError(f"unknown {where.rsplit('.', 1)[-1]} id: {cue_id}")
    return Cue(
        id=cue_id,
        intensity=_unit(item.get("intensity"), f"{where}.intensity"),
        parameters=_parameters(item.get("parameters"), f"{where}.parameters"),
    )


def _background(value: Any, where: str) -> Background:
    item = _object(value, where)
    asset = item.get("assetRef")
    return Background(
        id=_id(_need(item, "id", where), f"{where}.id"),
        variant=_optional_text(item.get("variant"), f"{where}.variant"),
        mood=_optional_text(item.get("mood"), f"{where}.mood"),
        asset_ref=_asset_ref(asset, f"{where}.assetRef") if asset is not None else None,
    )


def _rect(value: Any, where: str) -> tuple[float, float, float, float]:
    values = _array(value, where)
    if len(values) != 4:
        raise StoryError(f"{where} must contain [x, y, width, height]")
    rect = tuple(_unit(v, where) for v in values)
    x, y, width, height = rect
    if width <= 0 or height <= 0 or x + width > 1 or y + height > 1:
        raise StoryError(f"{where} must fit inside normalized canvas")
    return rect


def _layout(value: Any, where: str) -> Layout:
    item = _object(value, where)
    safe_area_raw = item.get("safeArea")
    safe_area = None
    if safe_area_raw is not None:
        values = _array(safe_area_raw, f"{where}.safeArea")
        if len(values) != 4:
            raise StoryError(f"{where}.safeArea must contain [top, right, bottom, left]")
        safe_area = tuple(_unit(v, f"{where}.safeArea") for v in values)
        if safe_area[0] + safe_area[2] >= 1 or safe_area[1] + safe_area[3] >= 1:
            raise StoryError(f"{where}.safeArea leaves no drawable area")
    zones_raw = item.get("zones", {})
    zones_obj = _object(zones_raw, f"{where}.zones")
    zones = {_id(name, f"{where}.zones key"): _rect(rect, f"{where}.zones.{name}") for name, rect in zones_obj.items()}
    return Layout(
        preset=_id(item.get("preset", "auto"), f"{where}.preset"),
        focus=_optional_text(item.get("focus"), f"{where}.focus"),
        safe_area=safe_area,
        zones=zones,
    )


def _camera(value: Any, where: str) -> Camera:
    item = _object(value, where)
    framing = str(item.get("framing", "wide"))
    movement = str(item.get("movement", "static"))
    if framing not in _CAMERA_FRAMINGS:
        raise StoryError(f"{where}.framing must be one of {sorted(_CAMERA_FRAMINGS)}")
    if movement not in _CAMERA_MOVEMENTS:
        raise StoryError(f"{where}.movement must be one of {sorted(_CAMERA_MOVEMENTS)}")
    return Camera(
        framing=framing,
        movement=movement,
        target=_optional_text(item.get("target"), f"{where}.target"),
        intensity=_unit(item.get("intensity"), f"{where}.intensity", default=0.0),
    )


def _scene(value: Any, where: str) -> Scene:
    item = _object(value, where)
    background = item.get("background")
    layout = item.get("layout")
    camera = item.get("camera")
    refs = _array(item.get("assetRefs", []), f"{where}.assetRefs")
    asset_refs = tuple(_asset_ref(ref, f"{where}.assetRefs[{i}]") for i, ref in enumerate(refs))
    if len({ref.id for ref in asset_refs}) != len(asset_refs):
        raise StoryError(f"duplicate asset reference in {where}")
    return Scene(
        id=_id(item.get("id", "scene.default"), f"{where}.id"),
        background=_background(background, f"{where}.background") if background is not None else None,
        layout=_layout(layout, f"{where}.layout") if layout is not None else None,
        camera=_camera(camera, f"{where}.camera") if camera is not None else None,
        asset_refs=asset_refs,
    )


def parse_story(document: Mapping[str, Any], source: str | Path | None = None) -> Story:
    """Migrate and validate an in-memory Story document."""

    try:
        raw = migrate_story_data(document)
    except StoryMigrationError as exc:
        raise StoryError(str(exc)) from exc
    source_path = Path(source).resolve() if source is not None else Path("<memory>")
    meta = _object(_need(raw, "meta", "root"), "root.meta")
    resolution = _need(meta, "resolution", "meta")
    if not isinstance(resolution, list) or len(resolution) != 2:
        raise StoryError("meta.resolution must be [width, height]")
    try:
        width, height = int(resolution[0]), int(resolution[1])
        fps = int(meta.get("fps", 12))
    except (TypeError, ValueError) as exc:
        raise StoryError("meta resolution and fps must be integers") from exc
    if width < 640 or height < 360:
        raise StoryError("minimum resolution is 640x360")
    if not 10 <= fps <= 60:
        raise StoryError("fps must be 10..60")

    chars: dict[str, Character] = {}
    for i, value in enumerate(_array(_need(raw, "characters", "root"), "root.characters")):
        item = _object(value, f"characters[{i}]")
        cid = _id(_need(item, "id", f"characters[{i}]"), f"characters[{i}].id")
        if cid in chars:
            raise StoryError(f"duplicate character: {cid}")
        palette = _object(_need(item, "palette", f"characters[{i}]"), f"characters[{i}].palette")
        if not all(isinstance(key, str) and isinstance(color, str) for key, color in palette.items()):
            raise StoryError(f"characters[{i}].palette must map strings to colors")
        chars[cid] = Character(
            id=cid,
            name=str(_need(item, "name", f"characters[{i}]")),
            palette=dict(palette),
            voice=_parameters(item.get("voice"), f"characters[{i}].voice"),
            renderer=_renderer(item.get("renderer", {"type": "procedural"}), f"characters[{i}].renderer"),
        )

    shots: list[Shot] = []
    ids: set[str] = set()
    for i, value in enumerate(_array(_need(raw, "shots", "root"), "root.shots")):
        item = _object(value, f"shots[{i}]")
        sid = _id(_need(item, "id", f"shots[{i}]"), f"shots[{i}].id")
        if sid in ids:
            raise StoryError(f"duplicate shot: {sid}")
        ids.add(sid)
        try:
            duration = float(_need(item, "duration", f"shots[{i}]"))
        except (TypeError, ValueError) as exc:
            raise StoryError(f"shots[{i}].duration must be a number") from exc
        if duration <= 0.5:
            raise StoryError(f"shot {sid} is too short")
        speaker = item.get("speaker")
        if speaker is not None and not isinstance(speaker, str):
            raise StoryError(f"speaker must be a character id in {sid}")
        if speaker is not None and speaker not in chars:
            raise StoryError(f"unknown speaker {speaker} in {sid}")
        states: list[State] = []
        states_raw = _array(item.get("states", []), f"shots[{i}].states")
        state_characters: set[str] = set()
        for j, state_value in enumerate(states_raw):
            where = f"shots[{i}].states[{j}]"
            state = _object(state_value, where)
            cid = _id(_need(state, "character", where), f"{where}.character")
            if cid not in chars:
                raise StoryError(f"unknown character {cid} in {sid}")
            if cid in state_characters:
                raise StoryError(f"duplicate character state {cid} in {sid}")
            state_characters.add(cid)
            try:
                x = float(_need(state, "x", where))
                y = float(_need(state, "y", where))
                scale = float(state.get("scale", 1.0))
            except (TypeError, ValueError) as exc:
                raise StoryError(f"state coordinates and scale must be numbers in {sid}") from exc
            if not (0 <= x <= 1 and 0 <= y <= 1):
                raise StoryError(f"state coordinates must be normalized in {sid}")
            if scale <= 0:
                raise StoryError(f"state scale must be positive in {sid}")
            try:
                facing = 1 if int(state.get("facing", 1)) >= 0 else -1
            except (TypeError, ValueError) as exc:
                raise StoryError(f"state facing must be a number in {sid}") from exc
            action = _cue(state.get("action"), f"{where}.action", "idle", _ACTION_IDS)
            expression = _cue(state.get("expression"), f"{where}.expression", "neutral", _EXPRESSION_IDS)
            states.append(
                State(
                    character=cid,
                    x=x,
                    y=y,
                    scale=scale,
                    facing=facing,
                    action=action.id,
                    expression=expression.id,
                    action_cue=action,
                    expression_cue=expression,
                )
            )
        scene_raw = item.get("scene")
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
                sfx=tuple(str(v) for v in _array(item.get("sfx", []), f"shots[{i}].sfx")),
                states=tuple(states),
                scene=_scene(scene_raw, f"shots[{i}].scene") if scene_raw is not None else None,
            )
        )

    slug = str(_need(meta, "slug", "meta"))
    return Story(
        source=source_path,
        schema_version=CURRENT_SCHEMA_VERSION,
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


def load_story(path: str | Path) -> Story:
    """Load a v1 or v2 Story JSON file, migrate it in memory, then validate it."""

    source = Path(path).resolve()
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StoryError(f"story not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise StoryError(f"invalid JSON line {exc.lineno}: {exc.msg}") from exc
    if not isinstance(raw, dict):
        raise StoryError("story root must be an object")
    return parse_story(raw, source)
