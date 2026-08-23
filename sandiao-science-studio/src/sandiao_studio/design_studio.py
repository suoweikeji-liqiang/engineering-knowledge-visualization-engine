"""Design-system composition built from validated SVG runtime assets."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

from .assets import AssetManifest, load_asset_source
from .core import Point, ease
from .layout import LayoutEngine, LayoutRequest, Rect
from .renderers import Bounds, Layer, RenderContext, SvgAssetRenderer
from .story import Character, State, Story
from .studio import Studio


INK = "#080E18"
PANEL = "#101C31"
PANEL_2 = "#172A46"
CYAN = "#1FD6E2"
BLUE = "#1F5CFF"
ORANGE = "#FA541C"
GREEN = "#52C41A"
MUTED = "#8FA6CB"
WHITE = "#FFFFFF"


class DesignStudio(Studio):
    """Render the observatory visual system through the normal video pipeline."""

    def __init__(self, story: Story, manifest: str | Path | AssetManifest):
        super().__init__(story)
        self.manifest = (
            manifest if isinstance(manifest, AssetManifest) else load_asset_source(manifest)
        )
        self.assets = SvgAssetRenderer(self.manifest)
        self.asset_ids = {asset.id for asset in self.manifest.assets}
        self.layouts = LayoutEngine()

    def _context(self, image: Image.Image, point: Point) -> RenderContext:
        return RenderContext(
            width=image.width,
            height=image.height,
            time_seconds=point.local,
            duration_seconds=self.timeline.durations[self.story.shots.index(point.shot)],
            frame_index=round((point.start + point.local) * self.story.fps),
            fps=self.story.fps,
            scene_id=point.shot.scene.id if point.shot.scene else point.shot.id,
            surface=image,
        )

    def _render_asset(
        self,
        image: Image.Image,
        point: Point,
        asset_id: str,
        rect: Rect,
        *,
        fit: str = "contain",
        flip_x: bool = False,
        opacity: float = 1.0,
        layer_id: str | None = None,
    ) -> None:
        if asset_id not in self.asset_ids:
            return
        self.assets.render(
            self._context(image, point),
            Layer(
                layer_id or asset_id,
                Bounds(rect.x, rect.y, rect.width, rect.height),
                opacity=opacity,
            ),
            {"assetId": asset_id, "fit": fit, "flipX": flip_x},
        )

    def background(self, image: Image.Image, point: Point) -> None:
        explicit = None
        if point.shot.scene and point.shot.scene.background:
            ref = point.shot.scene.background.asset_ref
            explicit = ref.id if ref and ref.id in self.asset_ids else None
        fallback = {
            "hook": "brand.background.science-lab.scene-night16x9",
            "not-faucet": "brand.background.science-lab.scene-night16x9",
            "compressor": "domain.hvac.background.plant-room.scene-night16x9",
            "question": "brand.background.abstract-stage.scene-dark16x9",
            "runtime": "brand.background.abstract-stage.scene-dark16x9",
            "never": "domain.hvac.background.plant-room.scene-night16x9",
            "tips": "brand.background.summary-stage.scene-night16x9",
            "end": "brand.background.summary-stage.scene-night16x9",
        }.get(point.shot.id, "brand.background.science-lab.scene-night16x9")
        self._render_asset(
            image,
            point,
            explicit or fallback,
            Rect(0, 0, image.width, image.height),
            fit="cover",
            layer_id="background",
        )
        shade = Image.new("RGBA", image.size, (8, 14, 24, 54))
        image.alpha_composite(shade)

    def _brand_bar(self, image: Image.Image, point: Point, headline: Rect) -> None:
        draw = ImageDraw.Draw(image, "RGBA")
        draw.rectangle((0, 0, image.width, self.s(41)), fill=(8, 14, 24, 226))
        draw.line((0, self.s(40), image.width, self.s(40)), fill="#1F385C", width=self.s(1))
        icon_x, icon_y = self.s(25), self.s(20)
        draw.ellipse(
            (icon_x - self.s(10), icon_y - self.s(10), icon_x + self.s(10), icon_y + self.s(10)),
            fill=BLUE,
        )
        draw.ellipse(
            (icon_x - self.s(17), icon_y - self.s(6), icon_x + self.s(17), icon_y + self.s(6)),
            outline=CYAN,
            width=self.s(2),
        )
        draw.text(
            (icon_x + self.s(22), self.s(9)),
            "小行星原理剧场",
            font=self.fonts.get(self.s(14), True),
            fill=WHITE,
        )
        episode = f"EP.{self.story.episode}  ·  OBSERVATORY LIVE"
        right_font = self.fonts.get(self.s(9), True)
        box = draw.textbbox((0, 0), episode, font=right_font)
        draw.text(
            (image.width - self.s(20) - (box[2] - box[0]), self.s(13)),
            episode,
            font=right_font,
            fill=CYAN,
        )
        title_font = self.fonts.get(self.s(17), True)
        title_box = draw.textbbox((0, 0), point.shot.headline, font=title_font)
        title_width = title_box[2] - title_box[0]
        x = image.width / 2 - title_width / 2
        y = headline.y + headline.height - self.s(26)
        draw.rounded_rectangle(
            (x - self.s(14), y - self.s(6), x + title_width + self.s(14), y + self.s(24)),
            radius=self.s(9),
            fill=(16, 28, 49, 235),
            outline=CYAN,
            width=self.s(1),
        )
        draw.text((x, y), point.shot.headline, font=title_font, fill=WHITE)

    def _panel(self, draw: ImageDraw.ImageDraw, rect: Rect, accent: str = CYAN) -> None:
        shadow = self.s(7)
        draw.rounded_rectangle(
            (rect.x + shadow, rect.y + shadow, rect.right + shadow, rect.bottom + shadow),
            radius=self.s(17),
            fill=(0, 0, 0, 90),
        )
        draw.rounded_rectangle(
            (rect.x, rect.y, rect.right, rect.bottom),
            radius=self.s(17),
            fill=(16, 28, 49, 244),
            outline=accent,
            width=self.s(2),
        )

    def diagram(self, image: Image.Image, point: Point, rect: Rect) -> None:
        draw = ImageDraw.Draw(image, "RGBA")
        enter = ease(point.progress / 0.18)
        rect = Rect(rect.x + (1 - enter) * rect.width * 0.18, rect.y, rect.width, rect.height)
        accent = ORANGE if point.shot.id == "hook" else CYAN
        self._panel(draw, rect, accent)
        d = point.shot.diagram
        cx, cy = rect.x + rect.width / 2, rect.y + rect.height / 2

        if d == "myth":
            card_w, card_h = rect.width * 0.62, rect.height * 0.46
            pulse = 1 + 0.025 * math.sin(point.local * 7)
            card = Rect(cx - card_w * pulse / 2, cy - card_h * pulse / 2, card_w * pulse, card_h * pulse)
            draw.rounded_rectangle(
                (card.x, card.y, card.right, card.bottom),
                radius=self.s(15),
                fill=ORANGE,
            )
            self.center(draw, (cx, cy - self.s(20)), "16℃", 43, WHITE, True)
            self.center(draw, (cx, cy + self.s(27)), "降温更快，还更省电？", 16, WHITE, True)
            if point.local >= 2.0:
                stamp = ease((point.local - 2.0) / 0.28)
                width = self.s(150) * stamp
                draw.rounded_rectangle(
                    (cx - width / 2, cy + self.s(67), cx + width / 2, cy + self.s(105)),
                    radius=self.s(7),
                    outline="#FF4D4F",
                    width=self.s(5),
                )
                self.center(draw, (cx, cy + self.s(86)), "直觉待验证", 15, "#FF7875", True)
        elif d == "not-faucet":
            split = cx
            draw.line((split, rect.y + self.s(28), split, rect.bottom - self.s(28)), fill="#1F385C", width=self.s(2))
            faucet_x, faucet_y = rect.x + rect.width * 0.25, rect.y + rect.height * 0.42
            draw.line(
                (faucet_x - self.s(55), faucet_y, faucet_x + self.s(20), faucet_y),
                fill=MUTED,
                width=self.s(13),
            )
            draw.arc(
                (faucet_x - self.s(5), faucet_y - self.s(3), faucet_x + self.s(65), faucet_y + self.s(67)),
                270,
                360,
                fill=MUTED,
                width=self.s(13),
            )
            cross = self.s(34) * ease(point.progress / 0.3)
            draw.line((faucet_x - cross, faucet_y - cross, faucet_x + cross, faucet_y + cross), fill="#FF4D4F", width=self.s(7))
            draw.line((faucet_x + cross, faucet_y - cross, faucet_x - cross, faucet_y + cross), fill="#FF4D4F", width=self.s(7))
            ac_rect = Rect(rect.x + rect.width * 0.57, rect.y + rect.height * 0.25, rect.width * 0.36, rect.height * 0.38)
            self._render_asset(image, point, "domain.hvac.prop.ac-indoor", ac_rect, layer_id="diagram-ac")
            self.center(draw, (faucet_x, rect.bottom - self.s(42)), "水龙头旋钮", 13, "#FF7875", True)
            self.center(draw, (rect.x + rect.width * 0.75, rect.bottom - self.s(42)), "温度只是目标线", 13, CYAN, True)
        elif d == "compressor":
            compressor = Rect(rect.x + rect.width * 0.10, rect.y + rect.height * 0.18, rect.width * 0.26, rect.height * 0.64)
            exchanger = Rect(rect.x + rect.width * 0.64, rect.y + rect.height * 0.18, rect.width * 0.22, rect.height * 0.64)
            self._render_asset(image, point, "domain.hvac.prop.compressor", compressor, layer_id="diagram-compressor")
            self._render_asset(image, point, "domain.hvac.prop.heat-exchanger", exchanger, layer_id="diagram-exchanger")
            flow = ease(point.progress / 0.5)
            line_start, line_end = rect.x + rect.width * 0.36, rect.x + rect.width * (0.36 + 0.28 * flow)
            draw.line((line_start, cy, line_end, cy), fill=CYAN, width=self.s(7))
            if line_end > line_start + self.s(20):
                draw.polygon(
                    [(line_end, cy), (line_end - self.s(12), cy - self.s(8)), (line_end - self.s(12), cy + self.s(8))],
                    fill=CYAN,
                )
            self.center(draw, (cx, rect.y + self.s(30)), "启动后按额定能力运行", 16, WHITE, True)
            badge = Rect(cx - self.s(58), rect.bottom - self.s(53), self.s(116), self.s(31))
            draw.rounded_rectangle((badge.x, badge.y, badge.right, badge.bottom), radius=self.s(8), fill=GREEN)
            self.center(draw, (cx, badge.y + badge.height / 2), "RATED 100%", 11, INK, True)
        else:
            # Downstream shots still use the improved visual shell while their
            # dedicated SVG components are integrated incrementally.
            self.center(draw, (cx, cy), point.shot.headline, 21, WHITE, True)

    def _character_asset_id(self, spec: Character, state: State, point: Point) -> str:
        action = state.action
        if action == "talk" and point.shot.speaker == state.character:
            frame = int(point.local * 7) % 3 + 1
            candidate = f"brand.character.{spec.id}.pose.talk-f{frame}"
            if candidate in self.asset_ids:
                return candidate
        candidate = f"brand.character.{spec.id}.pose.{action}"
        if candidate in self.asset_ids:
            return candidate
        expression = "happy" if state.expression == "smile" else state.expression
        candidate = f"brand.character.{spec.id}.expression.{expression}"
        if candidate in self.asset_ids:
            return candidate
        return f"brand.character.{spec.id}.pose.idle"

    def character(
        self,
        image: Image.Image,
        spec: Character,
        state: State,
        point: Point,
        rect: Rect,
    ) -> None:
        bob = math.sin(point.local * 6.5) * self.s(2)
        if state.action == "celebrate":
            bob -= abs(math.sin(point.local * 5)) * self.s(8)
        elif state.action == "shake":
            rect = Rect(rect.x + math.sin(point.local * 22) * self.s(4), rect.y, rect.width, rect.height)
        rect = Rect(rect.x, rect.y + bob, rect.width, rect.height)
        self._render_asset(
            image,
            point,
            self._character_asset_id(spec, state, point),
            rect,
            flip_x=state.facing < 0,
            layer_id=f"character-{state.character}",
        )

    def subtitle(self, image: Image.Image, point: Point, rect: Rect) -> None:
        if not point.shot.dialogue:
            return
        draw = ImageDraw.Draw(image, "RGBA")
        draw.rounded_rectangle(
            (rect.x, rect.y, rect.right, rect.bottom),
            radius=self.s(13),
            fill=(8, 14, 24, 238),
            outline=BLUE,
            width=self.s(2),
        )
        character = self.story.characters.get(point.shot.speaker or "")
        name = character.name if character else "旁白"
        accent = ORANGE if point.shot.speaker == "laowang" else CYAN
        label = Rect(rect.x + self.s(12), rect.y + self.s(12), self.s(70), rect.height - self.s(24))
        draw.rounded_rectangle((label.x, label.y, label.right, label.bottom), radius=self.s(8), fill=accent)
        self.center(draw, (label.x + label.width / 2, label.y + label.height / 2), name, 13, INK, True)
        font = self.fonts.get(self.s(16), True)
        text_x = label.right + self.s(16)
        max_width = rect.right - text_x - self.s(24)
        lines: list[str] = []
        current = ""
        for char in point.shot.dialogue:
            if not current or draw.textbbox((0, 0), current + char, font=font)[2] <= max_width:
                current += char
            else:
                lines.append(current)
                current = char
        if current:
            lines.append(current)
        line_height = self.s(22)
        y = rect.y + (rect.height - line_height * min(2, len(lines))) / 2
        for index, line in enumerate(lines[:2]):
            draw.text((text_x, y + index * line_height), line, font=font, fill=WHITE)
        progress = (point.start + point.local) / self.timeline.duration
        draw.rounded_rectangle(
            (rect.x + self.s(7), rect.bottom - self.s(5), rect.x + self.s(7) + (rect.width - self.s(14)) * progress, rect.bottom - self.s(2)),
            radius=self.s(2),
            fill=accent,
        )

    def frame(self, t: float) -> Image.Image:
        point = self.timeline.locate(t)
        image = Image.new("RGBA", (self.story.width, self.story.height), INK)
        self.background(image, point)
        plan = self.layouts.plan(
            LayoutRequest(
                self.story.width,
                self.story.height,
                character_count=min(2, len(point.shot.states)),
                has_diagram=bool(point.shot.diagram),
                has_headline=bool(point.shot.headline),
                subtitle_lines=2 if point.shot.dialogue else 0,
            )
        )
        if plan.headline:
            self._brand_bar(image, point, plan.headline)
        if plan.diagram:
            self.diagram(image, point, plan.diagram)
        for state, rect in zip(point.shot.states, plan.characters):
            self.character(image, self.story.characters[state.character], state, point, rect)
        if plan.subtitle:
            self.subtitle(image, point, plan.subtitle)
        if point.local < 0.14:
            alpha = round(190 * (1 - point.local / 0.14))
            image.alpha_composite(Image.new("RGBA", image.size, (8, 14, 24, alpha)))
        return image.convert("RGB")

    def poster(self, output: Path | None = None) -> Path:
        """Use the composed observatory frame without the legacy title overlay."""
        destination = (output or self.story.poster).resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        self.frame(1.0).save(destination, quality=94)
        return destination
