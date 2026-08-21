from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from .core import C, Fonts, Point, Timeline, ease
from .story import Character, State, Story

class Studio:
    def __init__(self, story: Story):
        self.story = story
        self.timeline = Timeline(story)
        self.fonts = Fonts()
        self.k = min(story.width / 640, story.height / 360)

    def s(self, value: float) -> int:
        return max(1, round(value * self.k))

    def center(self, draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str,
               size: int, fill: str, bold: bool = False, stroke: int = 0) -> None:
        font = self.fonts.get(self.s(size), bold)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=self.s(stroke))
        draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2),
                  text, font=font, fill=fill, stroke_width=self.s(stroke),
                  stroke_fill=C["ink"] if stroke else None)

    def panel(self, draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
        o = self.s(5)
        draw.rounded_rectangle((box[0] + o, box[1] + o, box[2] + o, box[3] + o),
                               radius=self.s(15), fill=(70, 60, 50, 55))
        draw.rounded_rectangle(box, radius=self.s(15), fill=C["white"],
                               outline=C["ink"], width=self.s(3))

    def background(self, image: Image.Image, point: Point) -> None:
        draw = ImageDraw.Draw(image, "RGBA")
        w, h = image.size
        floor = int(h * .72)
        draw.rectangle((0, 0, w, h), fill=C["paper"])
        draw.rectangle((0, floor, w, h), fill=C["floor"])
        for y in range(floor + self.s(12), h, self.s(14)):
            draw.line((0, y, w, y), fill="#9C6F4638", width=self.s(1))
        wx1, wy1, wx2, wy2 = self.s(18), self.s(55), self.s(178), self.s(210)
        draw.rounded_rectangle((wx1, wy1, wx2, wy2), radius=self.s(8),
                               fill=C["blue2"], outline=C["ink"], width=self.s(3))
        draw.line(((wx1 + wx2) / 2, wy1, (wx1 + wx2) / 2, wy2), fill=C["ink"], width=self.s(2))
        draw.line((wx1, (wy1 + wy2) / 2, wx2, (wy1 + wy2) / 2), fill=C["ink"], width=self.s(2))
        draw.ellipse((wx1 + self.s(18), wy1 + self.s(18), wx1 + self.s(45), wy1 + self.s(45)),
                     fill=C["yellow"], outline=C["ink"], width=self.s(2))
        draw.polygon([(wx1 - self.s(8), wy1 - self.s(8)), (wx1 + self.s(34), wy1 - self.s(8)),
                      (wx1 + self.s(23), wy2 + self.s(8)), (wx1 - self.s(14), wy2 + self.s(8))],
                     fill=C["red"], outline=C["ink"])
        acx, acy = int(w * .55), self.s(40)
        draw.rounded_rectangle((acx - self.s(80), acy - self.s(22), acx + self.s(80), acy + self.s(22)),
                               radius=self.s(10), fill=C["white"], outline=C["ink"], width=self.s(3))
        draw.line((acx - self.s(58), acy + self.s(11), acx + self.s(58), acy + self.s(11)),
                  fill=C["blue"], width=self.s(3))
        for i in range(5):
            x = acx - self.s(50) + i * self.s(25)
            y = acy + self.s(26) + math.sin(point.local * 2 + i) * self.s(3)
            draw.arc((x - self.s(8), y, x + self.s(8), y + self.s(28)), 0, 180,
                     fill="#5CBCE199", width=self.s(2))
        badge = (self.s(18), self.s(14), self.s(181), self.s(42))
        draw.rounded_rectangle(badge, radius=self.s(9), fill=C["ink"],
                               outline=C["yellow"], width=self.s(2))
        draw.text((badge[0] + self.s(9), badge[1] + self.s(4)),
                  f"沙雕科普实验室 · {self.story.episode}",
                  font=self.fonts.get(self.s(12), True), fill=C["white"])

    def character(self, image: Image.Image, spec: Character, state: State, point: Point) -> None:
        draw = ImageDraw.Draw(image, "RGBA")
        x, y = state.x * image.width, state.y * image.height
        k = state.scale * self.k
        talking = point.shot.speaker == state.character and bool(point.shot.dialogue)
        if state.action == "nod": y += math.sin(point.local * 7) * 3 * k
        elif state.action == "shake": x += math.sin(point.local * 22) * 5 * k
        elif state.action == "celebrate": y -= abs(math.sin(point.local * 5)) * 8 * k
        else: y += math.sin(point.local * 7) * 1.3 * k
        cx, cy = int(x), int(y)
        skin = spec.palette.get("skin", "#F2C9A5")
        shirt = spec.palette.get("shirt", C["blue"])
        hair = spec.palette.get("hair", "#202630")
        accent = spec.palette.get("accent", C["yellow"])
        ink = C["ink"]
        draw.ellipse((cx - 40*k, cy + 58*k, cx + 40*k, cy + 72*k), fill=(20, 25, 35, 35))
        draw.rounded_rectangle((cx - 39*k, cy + 15*k, cx + 39*k, cy + 67*k), radius=15*k,
                               fill=shirt, outline=ink, width=max(1, int(3*k)))
        draw.rectangle((cx - 11*k, cy + 4*k, cx + 11*k, cy + 22*k), fill=skin)
        if state.action == "point":
            hx, hy = cx + state.facing * 72*k, cy + 15*k
            draw.line((cx + state.facing*28*k, cy + 34*k, hx, hy), fill=shirt, width=max(4, int(13*k)))
            draw.ellipse((hx - 6*k, hy - 6*k, hx + 6*k, hy + 6*k), fill=skin, outline=ink)
            draw.line((hx, hy, hx + state.facing*16*k, hy - 7*k), fill=ink, width=max(1, int(3*k)))
        else:
            wave = math.sin(point.local * 8) * 8*k if talking else 0
            for side in (-1, 1):
                hx, hy = cx + side*43*k, cy + 55*k + (wave if side == state.facing else 0)
                draw.line((cx + side*27*k, cy + 34*k, hx, hy), fill=shirt, width=max(4, int(12*k)))
        draw.ellipse((cx - 39*k, cy - 54*k, cx + 39*k, cy + 18*k), fill=skin,
                     outline=ink, width=max(1, int(3*k)))
        draw.pieslice((cx - 40*k, cy - 60*k, cx + 40*k, cy + 5*k), 184, 356, fill=hair)
        if spec.id == "laowang":
            draw.ellipse((cx - 8*k, cy - 60*k, cx + 22*k, cy - 47*k), fill=skin)
        else:
            draw.polygon([(cx - 34*k, cy - 37*k), (cx - 10*k, cy - 55*k), (cx, cy - 38*k),
                          (cx + 18*k, cy - 55*k), (cx + 35*k, cy - 34*k)], fill=hair)
        ey = cy - 20*k
        if state.expression in {"shocked", "puzzled"}:
            for dx in (-15, 15):
                draw.ellipse((cx + (dx-5)*k, ey-5*k, cx + (dx+5)*k, ey+5*k),
                             fill=C["white"], outline=ink, width=max(1, int(2*k)))
                draw.ellipse((cx + (dx-2)*k, ey-2*k, cx + (dx+2)*k, ey+2*k), fill=ink)
        else:
            for dx in (-16, 16):
                draw.ellipse((cx + (dx-3)*k, ey-3*k, cx + (dx+3)*k, ey+3*k), fill=ink)
        if spec.id == "xiaoming":
            for dx in (-15, 15):
                draw.rounded_rectangle((cx + (dx-11)*k, ey-9*k, cx + (dx+11)*k, ey+9*k),
                                       radius=4*k, outline=ink, width=max(1, int(2*k)))
            draw.line((cx - 4*k, ey, cx + 4*k, ey), fill=ink, width=max(1, int(2*k)))
        my = cy + k
        if state.expression == "shocked":
            draw.ellipse((cx - 7*k, my - 4*k, cx + 7*k, my + 10*k), fill="#8D3636", outline=ink)
        elif talking and math.sin(point.local * 18) > -.15:
            draw.ellipse((cx - 9*k, my - 2*k, cx + 9*k, my + 9*k), fill="#8D3636", outline=ink)
        elif state.expression in {"smile", "confident"}:
            draw.arc((cx - 11*k, my - 6*k, cx + 11*k, my + 8*k), 10, 170, fill=ink, width=max(1, int(3*k)))
        else:
            draw.line((cx - 7*k, my + 3*k, cx + 7*k, my + 3*k), fill=ink, width=max(1, int(2*k)))
        if state.action == "think" or state.expression == "shocked":
            mark = "?" if state.action == "think" else "!"
            draw.text((cx + 38*k, cy - 58*k), mark, font=self.fonts.get(max(8, int(18*k)), True),
                      fill=accent if mark == "?" else C["red"], stroke_width=1, stroke_fill=ink)
        draw.rounded_rectangle((cx - 25*k, cy + 43*k, cx + 25*k, cy + 57*k), radius=5*k,
                               fill=accent, outline=ink)
        self.center(draw, (cx, cy + 50*k), spec.name, max(8, int(9*k/self.k)), ink, True)

    def diagram(self, image: Image.Image, point: Point) -> None:
        if not point.shot.diagram: return
        draw = ImageDraw.Draw(image, "RGBA")
        enter = ease(point.progress / .18)
        x1, y1, x2, y2 = self.s(260 + (1-enter)*250), self.s(68), self.s(625 + (1-enter)*250), self.s(274)
        self.panel(draw, (x1, y1, x2, y2))
        cx, cy, w, h = (x1+x2)/2, (y1+y2)/2, x2-x1, y2-y1
        d = point.shot.diagram
        if d == "myth":
            self.center(draw, (cx, y1+h*.34), "16℃", 56, C["blue"], True, 1)
            self.center(draw, (cx, y1+h*.66), "= 更快 + 更省电？", 20, C["ink"], True)
        elif d == "not-faucet":
            self.center(draw, (x1+w*.28, cy), "🚰", 48, C["blue"], True)
            self.center(draw, (x1+w*.73, cy), "❄", 52, C["blue"], True)
            draw.line((cx-self.s(20), cy-self.s(20), cx+self.s(20), cy+self.s(20)), fill=C["red"], width=self.s(7))
            draw.line((cx+self.s(20), cy-self.s(20), cx-self.s(20), cy+self.s(20)), fill=C["red"], width=self.s(7))
            self.center(draw, (cx, y2-self.s(22)), "空调不是水龙头", 17, C["ink"], True)
        elif d == "compressor":
            self.center(draw, (cx, y1+self.s(27)), "定频空调的典型逻辑", 17, C["ink"], True)
            cards = [("启动", C["red"]), ("额定能力", C["yellow"]), ("满足条件停机", C["green"])]
            for i, (label, color) in enumerate(cards):
                bx = x1+self.s(27)+i*self.s(91)
                draw.rounded_rectangle((bx, y1+self.s(61), bx+self.s(78), y1+self.s(123)),
                                       radius=self.s(9), fill=color, outline=C["ink"], width=self.s(2))
                self.center(draw, (bx+self.s(39), y1+self.s(92)), label, 12, C["ink"], True)
        elif d == "no-super":
            self.center(draw, (cx, cy-self.s(12)), "⚡", 72, C["yellow"], True, 1)
            draw.ellipse((cx-self.s(63), cy-self.s(63), cx+self.s(63), cy+self.s(63)),
                         outline=C["red"], width=self.s(7))
            draw.line((cx-self.s(45), cy-self.s(45), cx+self.s(45), cy+self.s(45)),
                      fill=C["red"], width=self.s(7))
            self.center(draw, (cx, y2-self.s(22)), "没有隐藏的超级功率档", 16, C["ink"], True)
        elif d == "runtime":
            self.center(draw, (cx, y1+self.s(26)), "主要改变的是：运行多久", 17, C["ink"], True)
            for i, (label, ratio, color) in enumerate([("26℃", .52, C["green"]), ("16℃", .92, C["red"])]):
                yy, start, maxw = y1+self.s(72+i*58), x1+self.s(86), w-self.s(112)
                self.center(draw, (x1+self.s(42), yy), label, 18, C["ink"], True)
                draw.rounded_rectangle((start, yy-self.s(12), start+maxw, yy+self.s(12)),
                                       radius=self.s(7), fill=C["paper2"], outline=C["ink"])
                draw.rounded_rectangle((start, yy-self.s(10), start+maxw*ratio*ease(point.progress/.55), yy+self.s(10)),
                                       radius=self.s(6), fill=color)
        elif d == "never":
            tx, top, bottom = x1+self.s(78), y1+self.s(42), y2-self.s(42)
            draw.rounded_rectangle((tx-self.s(9), top, tx+self.s(9), bottom), radius=self.s(6),
                                   fill=C["white"], outline=C["ink"], width=self.s(2))
            draw.ellipse((tx-self.s(20), bottom-self.s(7), tx+self.s(20), bottom+self.s(31)),
                         fill=C["red"], outline=C["ink"])
            self.center(draw, (x1+w*.7, cy-self.s(12)), "压缩机", 17, C["ink"], True)
            self.center(draw, (x1+w*.7, cy+self.s(20)), "持续运行…", 20, C["red"], True)
            self.center(draw, (cx, y2-self.s(20)), "目标到不了，停机条件可能一直不成立", 13, C["ink"], True)
        elif d == "tips":
            tips = [("26°", "温度合理", C["green"]), ("▣", "门窗密闭", C["blue2"]), ("◉", "遮阳+风量", C["yellow"])]
            for i, (icon, label, color) in enumerate(tips):
                bx = x1+self.s(12)+i*self.s(117)
                draw.rounded_rectangle((bx, y1+self.s(38), bx+self.s(105), y2-self.s(24)),
                                       radius=self.s(9), fill=color, outline=C["ink"], width=self.s(2))
                self.center(draw, (bx+self.s(52), y1+self.s(82)), icon, 25, C["white"], True, 1)
                self.center(draw, (bx+self.s(52), y2-self.s(37)), label, 13, C["ink"], True)
        elif d == "end":
            self.center(draw, (cx, cy-self.s(28)), "16℃不是省电键", 25, C["blue"], True)
            self.center(draw, (cx, cy+self.s(12)), "更像压缩机的“加班键”", 18, C["ink"], True)
            self.center(draw, (cx, y2-self.s(22)), "舒适优先，温度合理", 14, C["green"], True)

    def headline(self, image: Image.Image, point: Point) -> None:
        if not point.shot.headline: return
        draw = ImageDraw.Draw(image, "RGBA")
        font = self.fonts.get(self.s(19), True)
        box = draw.textbbox((0, 0), point.shot.headline, font=font)
        tw, th = box[2]-box[0], box[3]-box[1]
        y, x = -self.s(25)+ease(point.progress/.18)*self.s(78), image.width/2-tw/2
        draw.rounded_rectangle((x-self.s(12), y-self.s(6), x+tw+self.s(12), y+th+self.s(6)),
                               radius=self.s(9), fill=C["yellow"], outline=C["ink"], width=self.s(2))
        draw.text((x, y), point.shot.headline, font=font, fill=C["ink"])

    def subtitle(self, image: Image.Image, point: Point) -> None:
        if not point.shot.dialogue: return
        draw = ImageDraw.Draw(image, "RGBA")
        box = (self.s(28), self.s(285), image.width-self.s(28), image.height-self.s(12))
        draw.rounded_rectangle(box, radius=self.s(12), fill=(18, 25, 37, 235),
                               outline=C["yellow"], width=self.s(2))
        char = self.story.characters[point.shot.speaker] if point.shot.speaker else None
        name = char.name if char else "旁白"
        accent = char.palette.get("accent", C["yellow"]) if char else C["yellow"]
        name_font, text_font = self.fonts.get(self.s(13), True), self.fonts.get(self.s(17), True)
        nb = draw.textbbox((0, 0), name, font=name_font)
        nw, nh, nx, ny = nb[2]-nb[0], nb[3]-nb[1], box[0]+self.s(13), box[1]+self.s(12)
        draw.rounded_rectangle((nx, ny, nx+nw+self.s(16), ny+nh+self.s(8)), radius=self.s(7),
                               fill=accent, outline=C["ink"])
        draw.text((nx+self.s(8), ny+self.s(2)), name, font=name_font, fill=C["ink"])
        tx, maxw = nx+nw+self.s(31), box[2]-(nx+nw+self.s(31))-self.s(14)
        lines, current = [], ""
        for ch in point.shot.dialogue:
            if draw.textbbox((0, 0), current+ch, font=text_font)[2] <= maxw or not current:
                current += ch
            else:
                lines.append(current); current = ch
        if current: lines.append(current)
        y = (box[1]+box[3]-len(lines[:2])*self.s(23))/2
        for i, line in enumerate(lines[:2]):
            draw.text((tx, y+i*self.s(23)), line, font=text_font, fill=C["white"],
                      stroke_width=self.s(1), stroke_fill=C["ink"])
        p = (point.start+point.local)/self.timeline.duration
        draw.rounded_rectangle((box[0]+self.s(6), box[3]-self.s(5),
                                box[0]+self.s(6)+(box[2]-box[0]-self.s(12))*p, box[3]-self.s(2)),
                               radius=self.s(2), fill=C["yellow"])

    def frame(self, t: float) -> Image.Image:
        point = self.timeline.locate(t)
        image = Image.new("RGB", (self.story.width, self.story.height), C["paper"])
        self.background(image, point)
        self.diagram(image, point)
        self.headline(image, point)
        for state in point.shot.states:
            self.character(image, self.story.characters[state.character], state, point)
        self.subtitle(image, point)
        if point.local < .16:
            overlay = Image.new("RGBA", image.size, (244, 235, 216, int(180*(1-point.local/.16))))
            image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
        return image

    def poster(self, output: Path | None = None) -> Path:
        out = (output or self.story.poster).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        image = self.frame(1).convert("RGBA")
        draw = ImageDraw.Draw(image, "RGBA")
        draw.rounded_rectangle((self.s(28), self.s(48), self.s(420), self.s(137)), radius=self.s(14),
                               fill=(23, 34, 56, 240), outline=C["yellow"], width=self.s(3))
        draw.text((self.s(47), self.s(61)), "空调开到16℃", font=self.fonts.get(self.s(30), True), fill=C["white"])
        draw.text((self.s(47), self.s(101)), "真的更省电吗？", font=self.fonts.get(self.s(17), True), fill=C["yellow"])
        image.convert("RGB").save(out, quality=94)
        return out

    def render(self, output: Path | None = None, audio: Path | None = None) -> Path:
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg: raise RuntimeError("ffmpeg not found")
        out, audio_path = (output or self.story.video).resolve(), (audio or self.story.audio).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [ffmpeg, "-y", "-loglevel", "warning", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{self.story.width}x{self.story.height}", "-r", str(self.story.fps), "-i", "-"]
        if audio_path.exists(): cmd += ["-i", str(audio_path)]
        cmd += ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "19", "-pix_fmt", "yuv420p"]
        if audio_path.exists(): cmd += ["-c:a", "aac", "-b:a", "144k", "-shortest"]
        cmd += ["-movflags", "+faststart", str(out)]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        assert process.stdin is not None
        count = math.ceil(self.timeline.duration*self.story.fps)
        try:
            for i in range(count):
                process.stdin.write(self.frame(i/self.story.fps).tobytes())
                if i % max(1, self.story.fps*4) == 0: print(f"render {100*i/count:5.1f}%", flush=True)
        finally:
            process.stdin.close()
        if process.wait(): raise RuntimeError("ffmpeg render failed")
        return out
