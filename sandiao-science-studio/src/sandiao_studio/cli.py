from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .assets import AssetManifestError, load_asset_source
from .doctor import run_doctor
from .design_studio import DesignStudio
from .engine import Studio, build_audio
from .mimo import MimoClient, MimoError
from .story import StoryError, load_story, parse_story
from .story_migration import StoryMigrationError, migrate_story_data


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="sandiao")
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("validate", "audio", "poster", "render", "build"):
        cmd = sub.add_parser(name)
        cmd.add_argument("story", type=Path)
        if name in {"audio", "build"}:
            cmd.add_argument("--tts-provider", choices=["auto", "mimo", "espeak", "silent"], default="auto")
        if name in {"poster", "render", "build"}:
            cmd.add_argument("--assets", type=Path, help="use a validated design asset manifest or catalog")
        if name in {"render", "build"}:
            cmd.add_argument("--duration", type=float, help="render only the first N seconds")
        if name == "render":
            cmd.add_argument("--output", type=Path, help="override the video output path")
    tts = sub.add_parser("mimo-tts", help="synthesize speech with MiMo")
    tts.add_argument("text")
    tts.add_argument("output", type=Path)
    tts.add_argument("--voice")
    tts.add_argument("--style", default="")
    asr = sub.add_parser("mimo-asr", help="transcribe a local audio file with MiMo")
    asr.add_argument("audio", type=Path)
    asr.add_argument("--prompt")
    video = sub.add_parser("mimo-video", help="understand a local video or HTTPS URL with MiMo")
    video.add_argument("video")
    video.add_argument("--prompt")
    video.add_argument("--fps", type=float, default=1.0)
    doctor = sub.add_parser("doctor", help="check runtime, TTS, Story, and optional design assets")
    doctor.add_argument("--story", type=Path)
    doctor.add_argument("--assets", type=Path)
    doctor.add_argument("--json", action="store_true", dest="json_output")
    assets = sub.add_parser("validate-assets", help="strictly validate a design asset manifest or catalog")
    assets.add_argument("manifest", type=Path, help="path to a package manifest or top-level catalog")
    assets.add_argument("--asset-root", type=Path)
    migrate = sub.add_parser("migrate-story", help="write a validated Story v2 document")
    migrate.add_argument("story", type=Path)
    migrate.add_argument("output", type=Path, nargs="?")
    migrate.add_argument("--force", action="store_true")
    return root


def _migrate_story_file(source: Path, output: Path | None, force: bool) -> Path:
    source = source.resolve()
    destination = (output or source.with_name(f"{source.stem}.v2.json")).resolve()
    if destination.exists() and not force:
        raise RuntimeError(f"output already exists: {destination}; pass --force to replace it")
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StoryMigrationError(f"story not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise StoryMigrationError(f"invalid JSON line {exc.lineno}: {exc.msg}") from exc
    if not isinstance(raw, dict):
        raise StoryMigrationError("story root must be an object")
    migrated = migrate_story_data(raw)
    parse_story(migrated, source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(migrated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return destination


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "doctor":
        report = run_doctor(args.story, args.assets)
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2) if args.json_output else report.render_text())
        return report.exit_code
    if args.command == "validate-assets":
        try:
            manifest = load_asset_source(args.manifest, asset_root=args.asset_root)
        except AssetManifestError as exc:
            print(f"asset error: {exc}", file=sys.stderr)
            return 4
        print(f"asset source {manifest.schema_version} | {len(manifest.assets)} assets | {manifest.source}")
        return 0
    if args.command == "migrate-story":
        try:
            print(_migrate_story_file(args.story, args.output, args.force))
            return 0
        except (StoryMigrationError, StoryError, RuntimeError) as exc:
            print(f"migration error: {exc}", file=sys.stderr)
            return 5
    if args.command.startswith("mimo-"):
        try:
            client = MimoClient()
            if args.command == "mimo-tts":
                print(client.synthesize(args.text, args.output, voice=args.voice, style=args.style))
            elif args.command == "mimo-asr":
                kwargs = {"prompt": args.prompt} if args.prompt else {}
                print(client.transcribe(args.audio, **kwargs))
            else:
                kwargs = {"fps": args.fps}
                if args.prompt:
                    kwargs["prompt"] = args.prompt
                print(client.understand_video(args.video, **kwargs))
            return 0
        except (MimoError, RuntimeError) as exc:
            print(f"mimo error: {exc}", file=sys.stderr)
            return 3
    try:
        story = load_story(args.story)
    except StoryError as exc:
        print(f"story error: {exc}", file=sys.stderr)
        return 2
    print(
        f"{story.title} | {len(story.shots)} shots | {story.duration:.1f}s | "
        f"{story.width}x{story.height}@{story.fps}fps"
    )
    if args.command == "validate":
        return 0
    if args.command == "audio":
        print(build_audio(story, provider=args.tts_provider))
    elif args.command == "poster":
        studio = DesignStudio(story, args.assets) if args.assets else Studio(story)
        print(studio.poster())
    elif args.command == "render":
        studio = DesignStudio(story, args.assets) if args.assets else Studio(story)
        print(studio.render(output=args.output, duration=args.duration))
    else:
        audio = build_audio(story, provider=args.tts_provider)
        studio = DesignStudio(story, args.assets) if args.assets else Studio(story)
        poster = studio.poster()
        video = studio.render(audio=audio, duration=args.duration)
        print(f"audio: {audio}")
        print(f"poster: {poster}")
        print(f"video: {video}")
    return 0
