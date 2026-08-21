from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .engine import Studio, build_audio
from .story import StoryError, load_story


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="sandiao")
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("validate", "audio", "poster", "render", "build"):
        cmd = sub.add_parser(name)
        cmd.add_argument("story", type=Path)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
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
    studio = Studio(story)
    if args.command == "audio":
        print(build_audio(story))
    elif args.command == "poster":
        print(studio.poster())
    elif args.command == "render":
        print(studio.render())
    else:
        audio = build_audio(story)
        poster = studio.poster()
        video = studio.render(audio=audio)
        print(f"audio: {audio}")
        print(f"poster: {poster}")
        print(f"video: {video}")
    return 0
