from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import ImageDraw, ImageFont

from .story import Shot, Story

C = {
    "ink": "#172238", "paper": "#F4EBD8", "paper2": "#E7DBC3",
    "blue": "#2A6FBB", "blue2": "#8AC6E8", "red": "#E14B3B",
    "yellow": "#F2C14E", "green": "#4C956C", "white": "#FFFDF7",
    "floor": "#C99B69",
}
RATE = 44_100


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def ease(t: float) -> float:
    return 1 - (1 - clamp(t)) ** 3


@dataclass(frozen=True)
class Point:
    shot: Shot
    start: float
    local: float
    progress: float


class Timeline:
    def __init__(self, story: Story):
        self.story = story
        self.starts: list[float] = []
        cursor = 0.0
        for shot in story.shots:
            self.starts.append(cursor)
            cursor += shot.duration
        self.duration = cursor

    def locate(self, t: float) -> Point:
        t = clamp(t, 0, max(self.duration - 1e-6, 0))
        for i in range(len(self.story.shots) - 1, -1, -1):
            if t >= self.starts[i]:
                shot = self.story.shots[i]
                local = t - self.starts[i]
                return Point(shot, self.starts[i], local, clamp(local / shot.duration))
        return Point(self.story.shots[0], 0, 0, 0)


class Fonts:
    def __init__(self):
        regular = [
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "/usr/share/fonts/truetype/arphic-gbsn00lp/gbsn00lp.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        bold = [
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "C:/Windows/Fonts/msyhbd.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        self.regular = next((p for p in regular if Path(p).exists()), regular[-1])
        self.bold = next((p for p in bold if Path(p).exists()), bold[-1])
        self.cache: dict[tuple[int, bool], ImageFont.FreeTypeFont] = {}

    def get(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        key = (max(8, size), bold)
        if key not in self.cache:
            self.cache[key] = ImageFont.truetype(self.bold if bold else self.regular, key[0])
        return self.cache[key]
