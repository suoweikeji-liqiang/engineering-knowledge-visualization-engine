#!/usr/bin/env python3
"""Generate the design-system motion board for the first ten seconds."""

from __future__ import annotations

from html import escape
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
PREVIEWS_DIR = PROJECT_DIR / "design" / "previews"

BEATS = (
    ("00.0–00.8", "HOOK / 推近", "老王自信开讲", "红底问题卡弹入", "scan + voice in", "#FA541C", "hook"),
    ("00.8–02.0", "HOOK / 保持", "老王挥手，小明待机", "水龙头隐喻启动", "talk + water", "#FAAD14", "faucet"),
    ("02.0–03.6", "HOOK / 收束", "老王 settle，小明严肃", "INVALID 印章回弹", "impact + 0.3s gap", "#F5222D", "stamp"),
    ("03.6–04.5", "NOT FAUCET / 横移", "小明指向核心图解", "水龙头打叉，空调展开", "boing + speech", "#1FD6E2", "cross"),
    ("04.5–07.4", "NOT FAUCET / 解释", "小明稳定讲解，老王托腮", "旋钮到底，流量仍 100%", "steady narration", "#1F5CFF", "flow"),
    ("07.4–10.0", "COMPRESSOR / 切场", "小明点解，老王凑近", "压缩机与冷媒回路点亮", "motor + rated 100%", "#52C41A", "compressor"),
)


def _mini_visual(kind: str, color: str) -> str:
    common = """
      <g transform="translate(34 72)">
        <circle cx="34" cy="24" r="18" fill="#F8D5B8" stroke="#13223A" stroke-width="2"/>
        <path d="M16 48 Q34 38 52 48 L58 102 L10 102 Z" fill="#FA541C" stroke="#13223A" stroke-width="2"/>
      </g>
      <g transform="translate(296 70)">
        <circle cx="34" cy="24" r="17" fill="#F8D5B8" stroke="#13223A" stroke-width="2"/>
        <path d="M14 48 Q34 38 54 48 L60 104 L8 104 Z" fill="#1FD6E2" stroke="#13223A" stroke-width="2"/>
        <path d="M18 23 H50" stroke="#13223A" stroke-width="3"/>
      </g>
    """
    visuals = {
        "hook": f"""<rect x="100" y="54" width="190" height="78" rx="12" fill="{color}"/>
          <path d="M132 93 H258" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round"/>
          <path d="M150 112 H240" stroke="#FFE58F" stroke-width="7" stroke-linecap="round"/>""",
        "faucet": f"""<path d="M126 80 H214 Q242 80 242 108 V124" fill="none" stroke="{color}" stroke-width="14" stroke-linecap="round"/>
          <path d="M242 135 Q226 155 242 171 Q258 155 242 135" fill="#1890FF"/>
          <path d="M118 60 H174 M146 44 V76" stroke="#13223A" stroke-width="8" stroke-linecap="round"/>""",
        "stamp": f"""<g transform="rotate(-8 205 110)"><rect x="112" y="68" width="186" height="82" rx="10" fill="none" stroke="{color}" stroke-width="10"/>
          <path d="M140 92 H270 M140 123 H246" stroke="{color}" stroke-width="10" stroke-linecap="round"/></g>""",
        "cross": f"""<path d="M106 82 H176 Q198 82 198 104 V128" fill="none" stroke="#8FA6CB" stroke-width="12"/>
          <path d="M110 68 L202 158 M202 68 L110 158" stroke="{color}" stroke-width="12" stroke-linecap="round"/>
          <rect x="234" y="68" width="74" height="80" rx="12" fill="#FFFFFF" stroke="#13223A" stroke-width="4"/>""",
        "flow": f"""<circle cx="148" cy="108" r="48" fill="#101C31" stroke="{color}" stroke-width="5"/>
          <path d="M148 82 L171 108 L148 134 L125 108 Z" fill="{color}"/>
          <path d="M202 108 H294" stroke="#1FD6E2" stroke-width="9" stroke-dasharray="16 8"/>
          <circle cx="314" cy="108" r="20" fill="#52C41A"/>""",
        "compressor": f"""<path d="M126 70 Q126 48 168 48 Q210 48 210 70 V148 Q210 170 168 170 Q126 170 126 148 Z" fill="#101C31" stroke="{color}" stroke-width="5"/>
          <circle cx="168" cy="108" r="28" fill="{color}" opacity="0.65"/>
          <path d="M210 82 H296 V150 H238" fill="none" stroke="#1FD6E2" stroke-width="9" stroke-linecap="round"/>
          <path d="M240 150 H306" stroke="#FA541C" stroke-width="9" stroke-linecap="round"/>""",
    }
    return common + visuals[kind]


def generate_motion_board() -> Path:
    PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    cards: list[str] = []
    for index, (timecode, shot, acting, visual, audio, color, kind) in enumerate(BEATS):
        x = (index % 3) * 580
        y = (index // 3) * 405
        cards.append(
            f"""
    <g id="beat-{index + 1}" transform="translate({x} {y})">
      <rect width="550" height="375" rx="20" fill="#101C31" stroke="{color}" stroke-width="2.5"/>
      <rect x="20" y="18" width="510" height="42" rx="9" fill="#172A46"/>
      <text x="36" y="46" fill="{color}" class="mono" font-size="17">{escape(timecode)}</text>
      <text x="510" y="46" fill="#FFFFFF" class="title" font-size="17" text-anchor="end">{escape(shot)}</text>
      <g transform="translate(70 70)">
        <rect width="410" height="200" rx="14" fill="#E6EEF8"/>
        {_mini_visual(kind, color)}
      </g>
      <circle cx="35" cy="300" r="7" fill="{color}"/><text x="54" y="306" fill="#FFFFFF" class="body" font-size="15">角色：{escape(acting)}</text>
      <circle cx="35" cy="329" r="7" fill="#1FD6E2"/><text x="54" y="335" fill="#D6E4FF" class="body" font-size="15">画面：{escape(visual)}</text>
      <circle cx="35" cy="356" r="7" fill="#8FA6CB"/><text x="54" y="362" fill="#8FA6CB" class="mono" font-size="13">声音：{escape(audio)}</text>
    </g>"""
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <style>
      .title {{ font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 800; }}
      .body {{ font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 600; }}
      .mono {{ font-family: 'SF Mono', monospace; font-weight: 650; }}
    </style>
    <linearGradient id="board-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#080E18"/><stop offset="1" stop-color="#14233C"/>
    </linearGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#board-bg)"/>
  <g transform="translate(90 48)">
    <text x="0" y="36" fill="#FFFFFF" class="title" font-size="34">前 10 秒核心动态板 · AC-16C</text>
    <text x="0" y="70" fill="#8FA6CB" class="body" font-size="17">Shot 01 → Shot 02 → Shot 03 前半段 · 角色、图解与声音同轨验收</text>
  </g>
  <g transform="translate(90 160)">{''.join(cards)}
  </g>
  <g transform="translate(90 1012)">
    <line x1="0" y1="0" x2="1740" y2="0" stroke="#1F385C" stroke-width="3"/>
    <circle cx="0" cy="0" r="8" fill="#FA541C"/><circle cx="626" cy="0" r="8" fill="#1FD6E2"/><circle cx="1288" cy="0" r="8" fill="#52C41A"/>
    <text x="0" y="30" fill="#8FA6CB" class="mono" font-size="14">0.0s</text><text x="626" y="30" fill="#8FA6CB" class="mono" font-size="14">3.6s</text>
    <text x="1288" y="30" fill="#8FA6CB" class="mono" font-size="14">7.4s</text><text x="1740" y="30" fill="#8FA6CB" class="mono" font-size="14" text-anchor="end">10.0s</text>
  </g>
</svg>
"""
    output = PREVIEWS_DIR / "motion_board_10s.svg"
    output.write_text(svg, encoding="utf-8")
    return output


if __name__ == "__main__":
    print(f"Motion board generated: {generate_motion_board()}")
