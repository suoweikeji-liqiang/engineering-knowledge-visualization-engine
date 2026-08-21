from __future__ import annotations

import math
from PIL import Image, ImageDraw

from .core import C, Point, ease


class IconStudioMixin:
    """Replace emoji-dependent diagrams with deterministic vector primitives."""

    def diagram(self, image: Image.Image, point: Point) -> None:
        if point.shot.diagram not in {"not-faucet", "no-super", "tips"}:
            return super().diagram(image, point)
        draw = ImageDraw.Draw(image, "RGBA")
        enter = ease(point.progress / .18)
        x1, y1 = self.s(260 + (1-enter)*250), self.s(68)
        x2, y2 = self.s(625 + (1-enter)*250), self.s(274)
        self.panel(draw, (x1, y1, x2, y2))
        cx, cy, w = (x1+x2)/2, (y1+y2)/2, x2-x1

        if point.shot.diagram == "not-faucet":
            fx, fy = x1+w*.27, cy-self.s(8)
            draw.rounded_rectangle((fx-self.s(34), fy-self.s(10), fx+self.s(22), fy+self.s(10)),
                                   radius=self.s(5), fill=C["blue2"], outline=C["ink"], width=self.s(2))
            draw.line((fx+self.s(20), fy, fx+self.s(20), fy+self.s(30)),
                      fill=C["ink"], width=self.s(5))
            draw.arc((fx-self.s(8), fy-self.s(34), fx+self.s(24), fy-self.s(5)),
                     180, 355, fill=C["ink"], width=self.s(4))
            draw.polygon([(fx+self.s(20), fy+self.s(35)), (fx+self.s(13), fy+self.s(47)),
                          (fx+self.s(27), fy+self.s(47))], fill=C["blue"], outline=C["ink"])
            self.center(draw, (fx, y2-self.s(30)), "水龙头", 13, C["ink"], True)

            ax, ay = x1+w*.73, cy-self.s(5)
            draw.rounded_rectangle((ax-self.s(48), ay-self.s(23), ax+self.s(48), ay+self.s(23)),
                                   radius=self.s(8), fill=C["paper2"], outline=C["ink"], width=self.s(2))
            draw.line((ax-self.s(34), ay+self.s(11), ax+self.s(34), ay+self.s(11)),
                      fill=C["blue"], width=self.s(3))
            for off in (-24, 0, 24):
                draw.arc((ax+self.s(off-8), ay+self.s(20), ax+self.s(off+8), ay+self.s(47)),
                         0, 180, fill=C["blue2"], width=self.s(2))
            self.center(draw, (ax, y2-self.s(30)), "空调", 13, C["ink"], True)
            draw.line((cx-self.s(20), cy-self.s(20), cx+self.s(20), cy+self.s(20)),
                      fill=C["red"], width=self.s(7))
            draw.line((cx+self.s(20), cy-self.s(20), cx-self.s(20), cy+self.s(20)),
                      fill=C["red"], width=self.s(7))
            self.center(draw, (cx, y2-self.s(18)), "设定温度不是冷量旋钮", 14, C["ink"], True)
            return

        if point.shot.diagram == "no-super":
            bolt = [(cx-self.s(18), cy-self.s(58)), (cx+self.s(8), cy-self.s(58)),
                    (cx-self.s(3), cy-self.s(13)), (cx+self.s(28), cy-self.s(13)),
                    (cx-self.s(20), cy+self.s(58)), (cx-self.s(5), cy+self.s(7)),
                    (cx-self.s(32), cy+self.s(7))]
            draw.polygon(bolt, fill=C["yellow"], outline=C["ink"])
            draw.ellipse((cx-self.s(63), cy-self.s(63), cx+self.s(63), cy+self.s(63)),
                         outline=C["red"], width=self.s(7))
            draw.line((cx-self.s(45), cy-self.s(45), cx+self.s(45), cy+self.s(45)),
                      fill=C["red"], width=self.s(7))
            self.center(draw, (cx, y2-self.s(22)), "没有隐藏的超级功率档", 16, C["ink"], True)
            return

        tips = [("温度合理", C["green"]), ("门窗密闭", C["blue2"]),
                ("遮阳+风量", C["yellow"])]
        for i, (label, color) in enumerate(tips):
            bx = x1+self.s(12)+i*self.s(117)
            mid = bx+self.s(52)
            draw.rounded_rectangle((bx, y1+self.s(38), bx+self.s(105), y2-self.s(24)),
                                   radius=self.s(9), fill=color, outline=C["ink"], width=self.s(2))
            iy = y1+self.s(82)
            if i == 0:
                draw.ellipse((mid-self.s(25), iy-self.s(25), mid+self.s(25), iy+self.s(25)),
                             fill=C["white"], outline=C["ink"], width=self.s(2))
                self.center(draw, (mid, iy), "26°", 18, C["red"], True)
            elif i == 1:
                draw.rectangle((mid-self.s(23), iy-self.s(27), mid+self.s(23), iy+self.s(27)),
                               fill=C["white"], outline=C["ink"], width=self.s(2))
                draw.line((mid, iy-self.s(27), mid, iy+self.s(27)), fill=C["ink"], width=self.s(2))
                draw.line((mid-self.s(23), iy, mid+self.s(23), iy), fill=C["ink"], width=self.s(2))
            else:
                draw.ellipse((mid-self.s(25), iy-self.s(25), mid+self.s(25), iy+self.s(25)),
                             fill=C["white"], outline=C["ink"], width=self.s(2))
                for angle in (0, 120, 240):
                    rad = math.radians(angle + point.local*45)
                    ex = mid + math.cos(rad)*self.s(14)
                    ey = iy + math.sin(rad)*self.s(14)
                    draw.ellipse((ex-self.s(7), ey-self.s(7), ex+self.s(7), ey+self.s(7)),
                                 fill=C["blue2"], outline=C["ink"])
            self.center(draw, (mid, y2-self.s(37)), label, 13, C["ink"], True)
