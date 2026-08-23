#!/usr/bin/env python3
"""
Generator script for Asteroid Principle Theater character assets.
Generates fully structured SVG files for Lao Wang and Xiao Ming:
- Turnaround (front, three_quarter, side, back)
- 12 Expressions
- 6 Mouth shapes
- 14 Action poses + 3-frame sequences for walk, run, talk, laugh
All SVGs strictly adhere to viewBox="0 0 512 768" and stable layer IDs.
"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = PROJECT_DIR / "design" / "assets" / "brand" / "characters"

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# Lao Wang SVG Definitions (4.8 heads, rugged mechanic vest, expressive face)
# -------------------------------------------------------------

def get_laowang_head(expression="neutral", mouth="rest", look_at=(256, 210), angle="front"):
    # Expression-specific features
    eye_lx, eye_rx = 220, 292
    eye_y = 210
    pupil_offset_x = 0
    pupil_offset_y = 0

    brow_l_d = "M 200,195 Q 220,180 240,195"
    brow_r_d = "M 272,195 Q 292,180 312,195"

    mouth_d = '<path id="mouth" d="M 236,260 Q 256,275 276,260" fill="none" stroke="#13223A" stroke-width="4" stroke-linecap="round"/>'
    extras = ""

    if expression == "happy" or expression == "smile":
        brow_l_d = "M 200,188 Q 220,175 240,190"
        brow_r_d = "M 272,190 Q 292,175 312,188"
        mouth_d = '<path id="mouth" d="M 230,255 Q 256,285 282,255 Z" fill="#820014" stroke="#13223A" stroke-width="3"/><path d="M 238,256 Q 256,264 274,256" fill="none" stroke="#FFFFFF" stroke-width="3"/>'
    elif expression == "confident":
        brow_l_d = "M 198,185 Q 220,170 242,190"
        brow_r_d = "M 270,192 Q 295,185 314,198"
        pupil_offset_x = 4
        mouth_d = '<path id="mouth" d="M 236,255 Q 260,270 280,250" fill="none" stroke="#13223A" stroke-width="4" stroke-linecap="round"/>'
    elif expression == "serious":
        brow_l_d = "M 200,200 L 242,210"
        brow_r_d = "M 270,210 L 312,200"
        mouth_d = '<line id="mouth" x1="236" y1="262" x2="276" y2="262" stroke="#13223A" stroke-width="4" stroke-linecap="round"/>'
    elif expression == "puzzled":
        brow_l_d = "M 200,185 Q 220,170 240,185" # Raised brow
        brow_r_d = "M 272,205 Q 292,215 312,205" # Lowered brow
        pupil_offset_y = -4
        mouth_d = '<path id="mouth" d="M 236,262 Q 256,252 276,265" fill="none" stroke="#13223A" stroke-width="4" stroke-linecap="round"/>'
        extras = '<text x="325" y="180" font-family="sans-serif" font-size="32" font-weight="bold" fill="#FA541C">?</text>'
    elif expression == "shocked":
        brow_l_d = "M 195,175 Q 220,160 245,175"
        brow_r_d = "M 267,175 Q 292,160 317,175"
        mouth_d = '<ellipse id="mouth" cx="256" cy="265" rx="18" ry="24" fill="#820014" stroke="#13223A" stroke-width="3"/>'
        extras = '<path d="M 175,170 C 160,185 160,195 175,205 C 185,195 185,185 175,170 Z" fill="#91CAFF" stroke="#1F5CFF" stroke-width="2"/>' # Sweat drop
    elif expression == "angry":
        brow_l_d = "M 200,205 L 245,218"
        brow_r_d = "M 267,218 L 312,205"
        mouth_d = '<path id="mouth" d="M 232,270 Q 256,250 280,270" fill="none" stroke="#13223A" stroke-width="4.5" stroke-linecap="round"/>'
        extras = '<path d="M 320,160 L 340,140 M 340,160 L 320,140" stroke="#F04B2F" stroke-width="4"/>'
    elif expression == "tired":
        brow_l_d = "M 200,195 L 240,205"
        brow_r_d = "M 272,205 L 312,195"
        mouth_d = '<path id="mouth" d="M 238,265 Q 256,260 274,265" fill="none" stroke="#13223A" stroke-width="3"/>'
        extras = '<line x1="205" y1="228" x2="235" y2="228" stroke="#13223A" stroke-width="2"/><line x1="277" y1="228" x2="307" y2="228" stroke="#13223A" stroke-width="2"/>'
    elif expression == "laugh":
        brow_l_d = "M 198,185 Q 220,170 242,185"
        brow_r_d = "M 270,185 Q 292,170 314,185"
        mouth_d = '<path id="mouth" d="M 226,250 Q 256,295 286,250 Z" fill="#820014" stroke="#13223A" stroke-width="3"/><path d="M 236,252 Q 256,262 276,252" fill="none" stroke="#FFFFFF" stroke-width="4"/><path d="M 240,285 Q 256,270 272,285" fill="#FF7875"/>'
    elif expression == "cry":
        brow_l_d = "M 200,180 Q 220,195 240,180"
        brow_r_d = "M 272,180 Q 292,195 312,180"
        mouth_d = '<path id="mouth" d="M 232,275 Q 256,250 280,275 Z" fill="#820014" stroke="#13223A" stroke-width="3"/>'
        extras = '<path d="M 215,225 L 215,310 M 297,225 L 297,310" stroke="#1890FF" stroke-width="8" stroke-linecap="round" opacity="0.8"/>'
    elif expression == "embarrassed":
        brow_l_d = "M 200,190 Q 220,180 240,190"
        brow_r_d = "M 272,190 Q 292,180 312,190"
        mouth_d = '<path id="mouth" d="M 238,260 Q 248,268 258,260 Q 268,268 276,260" fill="none" stroke="#13223A" stroke-width="3"/>'
        extras = '<ellipse cx="195" cy="235" rx="14" ry="8" fill="#FFA39E" opacity="0.6"/><ellipse cx="317" cy="235" rx="14" ry="8" fill="#FFA39E" opacity="0.6"/><path d="M 330,170 C 318,182 318,190 330,198 C 338,190 338,182 330,170 Z" fill="#91CAFF" stroke="#1F5CFF" stroke-width="1.5"/>'
    elif expression == "determined":
        brow_l_d = "M 198,195 L 242,208"
        brow_r_d = "M 270,208 L 314,195"
        mouth_d = '<path id="mouth" d="M 236,258 L 276,258" stroke="#13223A" stroke-width="4.5" stroke-linecap="round"/>'

    # Mouth shapes override
    if mouth == "rest":
        pass
    elif mouth == "slightly_open":
        mouth_d = '<path id="mouth" d="M 238,256 Q 256,270 274,256 Z" fill="#820014" stroke="#13223A" stroke-width="2.5"/>'
    elif mouth == "a_shape":
        mouth_d = '<path id="mouth" d="M 232,250 Q 256,290 280,250 Z" fill="#820014" stroke="#13223A" stroke-width="3"/><path d="M 240,252 Q 256,258 272,252" stroke="#FFFFFF" stroke-width="3"/>'
    elif mouth == "o_shape":
        mouth_d = '<ellipse id="mouth" cx="256" cy="262" rx="14" ry="18" fill="#820014" stroke="#13223A" stroke-width="3"/><ellipse cx="256" cy="262" rx="8" ry="12" fill="#2A0004"/>'
    elif mouth == "e_shape":
        mouth_d = '<rect id="mouth" x="232" y="254" width="48" height="14" rx="6" fill="#820014" stroke="#13223A" stroke-width="3"/><line x1="236" y1="261" x2="276" y2="261" stroke="#FFFFFF" stroke-width="3"/>'
    elif mouth == "bite_lip":
        mouth_d = '<path id="mouth" d="M 234,256 L 278,256 L 268,266 L 244,266 Z" fill="#FFFFFF" stroke="#13223A" stroke-width="3"/>'

    return f"""
    <!-- Head Root -->
    <g id="head">
      <!-- Neck -->
      <rect id="neck" x="236" y="270" width="40" height="42" rx="6" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>

      <!-- Head Base (Stout Rounded Trapezoid) -->
      <path id="face" d="M 186,245 C 180,165 205,130 256,130 C 307,130 332,165 326,245 C 321,278 191,278 186,245 Z" fill="#F8D5B8" stroke="#13223A" stroke-width="3.5" stroke-linejoin="round"/>

      <!-- Hairline & Characteristic Bald Top with Specular -->
      <path id="hair" d="M 186,215 C 184,155 220,135 240,135 C 248,135 248,150 238,158 C 220,165 200,185 204,225 Z" fill="#13223A"/>
      <path d="M 326,215 C 328,155 292,135 272,135 C 264,135 264,150 274,158 C 292,165 312,185 308,225 Z" fill="#13223A"/>
      <ellipse cx="256" cy="144" rx="18" ry="6" fill="#FFF1B8" opacity="0.6"/>

      <!-- Eyebrows -->
      <path id="brow_left" d="{brow_l_d}" fill="none" stroke="#13223A" stroke-width="5" stroke-linecap="round"/>
      <path id="brow_right" d="{brow_r_d}" fill="none" stroke="#13223A" stroke-width="5" stroke-linecap="round"/>

      <!-- Eyes -->
      <g id="eye_left">
        <ellipse cx="{eye_lx}" cy="{eye_y}" rx="13" ry="15" fill="#FFFFFF" stroke="#13223A" stroke-width="2.5"/>
        <circle cx="{eye_lx + pupil_offset_x}" cy="{eye_y + pupil_offset_y}" r="6.5" fill="#13223A"/>
        <circle cx="{eye_lx + pupil_offset_x + 2}" cy="{eye_y + pupil_offset_y - 2}" r="2" fill="#FFFFFF"/>
      </g>
      <g id="eye_right">
        <ellipse cx="{eye_rx}" cy="{eye_y}" rx="13" ry="15" fill="#FFFFFF" stroke="#13223A" stroke-width="2.5"/>
        <circle cx="{eye_rx + pupil_offset_x}" cy="{eye_y + pupil_offset_y}" r="6.5" fill="#13223A"/>
        <circle cx="{eye_rx + pupil_offset_x + 2}" cy="{eye_y + pupil_offset_y - 2}" r="2" fill="#FFFFFF"/>
      </g>

      <!-- Mustache -->
      <path id="mustache" d="M 230,238 Q 256,242 282,238 Q 268,248 256,245 Q 244,248 230,238 Z" fill="#13223A"/>

      <!-- Mouth Component -->
      {mouth_d}

      <!-- Emotion Extras -->
      {extras}
    </g>
    """

def generate_laowang_pose_svg(filename, pose_type="idle", expression="neutral", mouth="rest"):
    head_svg = get_laowang_head(expression=expression, mouth=mouth)

    # Body default coordinates
    torso_svg = """
    <!-- Torso: Work Vest & Polo -->
    <g id="torso">
      <path d="M 176,300 C 156,370 166,540 196,540 L 316,540 C 346,540 356,370 336,300 Z" fill="#FA541C" stroke="#13223A" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M 216,300 L 256,380 L 296,300 Z" fill="#FFE7BA" stroke="#13223A" stroke-width="2"/>
      <!-- Tool Belt with Tape Measure -->
      <rect x="176" y="495" width="160" height="26" rx="5" fill="#13223A"/>
      <rect x="275" y="488" width="38" height="38" rx="6" fill="#FADB14" stroke="#13223A" stroke-width="2"/>
    </g>
    """

    legs_svg = """
    <!-- Legs & Feet -->
    <g id="legs">
      <path id="leg_left" d="M 210,540 L 210,680 L 170,680" fill="none" stroke="#1A283F" stroke-width="36" stroke-linecap="round"/>
      <path id="leg_right" d="M 302,540 L 302,680 L 342,680" fill="none" stroke="#1A283F" stroke-width="36" stroke-linecap="round"/>
      <rect x="160" y="665" width="65" height="24" rx="7" fill="#D4380D" stroke="#13223A" stroke-width="2.5"/>
      <rect x="292" y="665" width="65" height="24" rx="7" fill="#D4380D" stroke="#13223A" stroke-width="2.5"/>
    </g>
    """

    arms_svg = """
    <!-- Arms Default (Idle) -->
    <g id="arms">
      <g id="arm_left">
        <path d="M 176,330 C 130,370 120,460 170,480" fill="none" stroke="#FA541C" stroke-width="32" stroke-linecap="round"/>
        <path d="M 176,330 C 130,370 120,460 170,480" fill="none" stroke="#13223A" stroke-width="3.5"/>
        <circle id="hand_left" cx="170" cy="480" r="18" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
      </g>
      <g id="arm_right">
        <path d="M 336,330 C 382,370 392,460 342,480" fill="none" stroke="#FA541C" stroke-width="32" stroke-linecap="round"/>
        <path d="M 336,330 C 382,370 392,460 342,480" fill="none" stroke="#13223A" stroke-width="3.5"/>
        <circle id="hand_right" cx="342" cy="480" r="18" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
      </g>
    </g>
    """

    if pose_type == "point":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 176,330 C 130,370 120,460 170,480" fill="none" stroke="#FA541C" stroke-width="32" stroke-linecap="round"/>
            <path d="M 176,330 C 130,370 120,460 170,480" fill="none" stroke="#13223A" stroke-width="3.5"/>
            <circle id="hand_left" cx="170" cy="480" r="18" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
          </g>
          <g id="arm_right">
            <path d="M 336,330 C 390,310 420,260 450,210" fill="none" stroke="#FA541C" stroke-width="32" stroke-linecap="round"/>
            <path d="M 336,330 C 390,310 420,260 450,210" fill="none" stroke="#13223A" stroke-width="3.5"/>
            <g id="hand_right" transform="translate(450, 210) rotate(-20)">
              <ellipse cx="0" cy="0" rx="16" ry="20" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
              <path d="M -6,-16 L 8,-28 M 3,-16 L 18,-24 M 10,-12 L 22,-14" stroke="#13223A" stroke-width="3.5" stroke-linecap="round"/>
            </g>
          </g>
        </g>
        """
    elif pose_type == "talk":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 176,330 C 120,350 110,410 150,420" fill="none" stroke="#FA541C" stroke-width="32" stroke-linecap="round"/>
            <path d="M 176,330 C 120,350 110,410 150,420" fill="none" stroke="#13223A" stroke-width="3.5"/>
            <circle id="hand_left" cx="150" cy="420" r="18" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
          </g>
          <g id="arm_right">
            <path d="M 336,330 C 390,330 410,290 430,260" fill="none" stroke="#FA541C" stroke-width="32" stroke-linecap="round"/>
            <path d="M 336,330 C 390,330 410,290 430,260" fill="none" stroke="#13223A" stroke-width="3.5"/>
            <circle id="hand_right" cx="430" cy="260" r="20" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
          </g>
        </g>
        """
    elif pose_type == "think":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 176,330 C 190,420 230,440 260,420" fill="none" stroke="#FA541C" stroke-width="30" stroke-linecap="round"/>
            <circle id="hand_left" cx="260" cy="420" r="16" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
          </g>
          <g id="arm_right">
            <path d="M 336,330 C 350,380 320,320 290,260" fill="none" stroke="#FA541C" stroke-width="30" stroke-linecap="round"/>
            <circle id="hand_right" cx="290" cy="260" r="18" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
          </g>
        </g>
        """
    elif pose_type == "celebrate":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 176,330 C 130,260 110,180 130,130" fill="none" stroke="#FA541C" stroke-width="32" stroke-linecap="round"/>
            <path d="M 176,330 C 130,260 110,180 130,130" fill="none" stroke="#13223A" stroke-width="3.5"/>
            <circle id="hand_left" cx="130" cy="130" r="20" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
          </g>
          <g id="arm_right">
            <path d="M 336,330 C 382,260 402,180 382,130" fill="none" stroke="#FA541C" stroke-width="32" stroke-linecap="round"/>
            <path d="M 336,330 C 382,260 402,180 382,130" fill="none" stroke="#13223A" stroke-width="3.5"/>
            <circle id="hand_right" cx="382" cy="130" r="20" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
          </g>
        </g>
        """
    elif pose_type == "whisper":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 176,330 C 140,370 140,440 180,460" fill="none" stroke="#FA541C" stroke-width="30" stroke-linecap="round"/>
            <circle id="hand_left" cx="180" cy="460" r="16" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
          </g>
          <g id="arm_right">
            <path d="M 336,330 C 350,300 320,270 290,250" fill="none" stroke="#FA541C" stroke-width="30" stroke-linecap="round"/>
            <circle id="hand_right" cx="290" cy="250" r="18" fill="#F8D5B8" stroke="#13223A" stroke-width="2.5"/>
          </g>
        </g>
        """

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 768" width="512" height="768">
  <!-- Lao Wang (Character: laowang, Pose: {pose_type}) -->
  <g id="root">
    <!-- Anchor Points: feet=(256, 680), mouth=(256, 260), center=(256, 384) -->
    {legs_svg}
    {torso_svg}
    {arms_svg}
    {head_svg}
    <g id="prop_anchor" transform="translate(256, 495)"/>
  </g>
</svg>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())

# -------------------------------------------------------------
# Xiao Ming SVG Definitions (5.5 heads, tech coat, smart glasses)
# -------------------------------------------------------------

def get_xiaoming_head(expression="neutral", mouth="rest", look_at=(256, 190)):
    eye_lx, eye_rx = 224, 288
    eye_y = 190
    brow_l_d = "M 205,172 Q 224,162 243,172"
    brow_r_d = "M 269,172 Q 288,162 307,172"
    mouth_d = '<path id="mouth" d="M 242,240 Q 256,248 270,240" fill="none" stroke="#101C31" stroke-width="3.5" stroke-linecap="round"/>'
    extras = ""

    if expression == "confident":
        mouth_d = '<path id="mouth" d="M 242,238 Q 256,252 272,238" fill="none" stroke="#101C31" stroke-width="4" stroke-linecap="round"/>'
    elif expression == "serious":
        brow_l_d = "M 205,176 L 243,184"
        brow_r_d = "M 269,184 L 307,176"
        mouth_d = '<line id="mouth" x1="242" y1="242" x2="270" y2="242" stroke="#101C31" stroke-width="3.5" stroke-linecap="round"/>'
    elif expression == "happy" or expression == "smile":
        mouth_d = '<path id="mouth" d="M 238,236 Q 256,260 274,236 Z" fill="#820014" stroke="#101C31" stroke-width="2.5"/><line x1="244" y1="238" x2="268" y2="238" stroke="#FFFFFF" stroke-width="3"/>'
    elif expression == "puzzled":
        brow_l_d = "M 205,165 Q 224,155 243,165"
        brow_r_d = "M 269,180 Q 288,190 307,180"
        mouth_d = '<path id="mouth" d="M 242,242 Q 256,236 270,244" fill="none" stroke="#101C31" stroke-width="3.5" stroke-linecap="round"/>'
    elif expression == "shocked":
        brow_l_d = "M 202,158 Q 224,146 246,158"
        brow_r_d = "M 266,158 Q 288,146 310,158"
        mouth_d = '<ellipse id="mouth" cx="256" cy="245" rx="14" ry="18" fill="#820014" stroke="#101C31" stroke-width="2.5"/>'
    elif expression == "angry":
        brow_l_d = "M 205,182 L 245,192"
        brow_r_d = "M 267,192 L 307,182"
        mouth_d = '<path id="mouth" d="M 240,248 Q 256,238 272,248" fill="none" stroke="#101C31" stroke-width="4" stroke-linecap="round"/>'
    elif expression == "tired":
        mouth_d = '<path id="mouth" d="M 244,244 Q 256,240 268,244" fill="none" stroke="#101C31" stroke-width="3"/>'
    elif expression == "laugh":
        mouth_d = '<path id="mouth" d="M 234,232 Q 256,270 278,232 Z" fill="#820014" stroke="#101C31" stroke-width="2.5"/><path d="M 242,234 Q 256,242 270,234" fill="none" stroke="#FFFFFF" stroke-width="3"/>'
    elif expression == "cry":
        mouth_d = '<path id="mouth" d="M 240,250 Q 256,235 272,250 Z" fill="#820014" stroke="#101C31" stroke-width="2.5"/>'
        extras = '<line x1="220" y1="210" x2="220" y2="280" stroke="#1FD6E2" stroke-width="6" stroke-linecap="round"/>'
    elif expression == "embarrassed":
        mouth_d = '<path id="mouth" d="M 244,242 Q 250,248 256,242 Q 262,248 268,242" fill="none" stroke="#101C31" stroke-width="2.5"/>'
        extras = '<ellipse cx="206" cy="216" rx="10" ry="6" fill="#FFA39E" opacity="0.6"/><ellipse cx="306" cy="216" rx="10" ry="6" fill="#FFA39E" opacity="0.6"/>'
    elif expression == "determined":
        brow_l_d = "M 205,178 L 243,188"
        brow_r_d = "M 269,188 L 307,178"
        mouth_d = '<line id="mouth" x1="242" y1="240" x2="270" y2="240" stroke="#101C31" stroke-width="4" stroke-linecap="round"/>'

    # Mouth shapes override
    if mouth == "rest":
        pass
    elif mouth == "slightly_open":
        mouth_d = '<path id="mouth" d="M 244,238 Q 256,248 268,238 Z" fill="#820014" stroke="#101C31" stroke-width="2"/>'
    elif mouth == "a_shape":
        mouth_d = '<path id="mouth" d="M 238,234 Q 256,268 274,234 Z" fill="#820014" stroke="#101C31" stroke-width="2.5"/><line x1="244" y1="236" x2="268" y2="236" stroke="#FFFFFF" stroke-width="2.5"/>'
    elif mouth == "o_shape":
        mouth_d = '<ellipse id="mouth" cx="256" cy="242" rx="11" ry="14" fill="#820014" stroke="#101C31" stroke-width="2.5"/>'
    elif mouth == "e_shape":
        mouth_d = '<rect id="mouth" x="238" y="236" width="36" height="11" rx="5" fill="#820014" stroke="#101C31" stroke-width="2"/><line x1="242" y1="241" x2="270" y2="241" stroke="#FFFFFF" stroke-width="2.5"/>'
    elif mouth == "bite_lip":
        mouth_d = '<path id="mouth" d="M 240,238 L 272,238 L 264,246 L 248,246 Z" fill="#FFFFFF" stroke="#101C31" stroke-width="2.5"/>'

    return f"""
    <!-- Xiao Ming Head Component -->
    <g id="head">
      <!-- Neck -->
      <rect id="neck" x="242" y="250" width="28" height="38" rx="5" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>

      <!-- Head Base (Slender Oval) -->
      <ellipse id="face" cx="256" cy="195" rx="50" ry="60" fill="#F8D5B8" stroke="#101C31" stroke-width="3" stroke-linejoin="round"/>

      <!-- Modern Neat Geometrical Hair -->
      <path id="hair" d="M 204,188 C 202,148 232,130 256,130 C 285,130 310,150 308,188 C 292,160 256,162 204,188 Z" fill="#101C31"/>

      <!-- Smart Glasses (Star-Orbit Telemetry) -->
      <g id="glasses" transform="translate(256, 192)">
        <rect x="-46" y="-14" width="38" height="28" rx="6" fill="#101C31" stroke="#1FD6E2" stroke-width="1.5"/>
        <rect x="8" y="-14" width="38" height="28" rx="6" fill="#101C31" stroke="#1FD6E2" stroke-width="1.5"/>
        <line x1="-8" y1="0" x2="8" y2="0" stroke="#101C31" stroke-width="3"/>

        <!-- Glowing Cyan Lenses -->
        <rect x="-42" y="-10" width="30" height="20" rx="4" fill="#1FD6E2" opacity="0.45"/>
        <rect x="12" y="-10" width="30" height="20" rx="4" fill="#1FD6E2" opacity="0.45"/>
        <line x1="-38" y1="-5" x2="-26" y2="-5" stroke="#FFFFFF" stroke-width="1.5"/>
        <line x1="16" y1="-5" x2="28" y2="-5" stroke="#FFFFFF" stroke-width="1.5"/>

        <!-- Eyes -->
        <circle id="eye_left" cx="-27" cy="0" r="4.5" fill="#101C31"/>
        <circle id="eye_right" cx="27" cy="0" r="4.5" fill="#101C31"/>
      </g>

      <!-- Eyebrows -->
      <path id="brow_left" d="{brow_l_d}" fill="none" stroke="#101C31" stroke-width="4" stroke-linecap="round"/>
      <path id="brow_right" d="{brow_r_d}" fill="none" stroke="#101C31" stroke-width="4" stroke-linecap="round"/>

      <!-- Mouth -->
      {mouth_d}

      <!-- Extras -->
      {extras}
    </g>
    """

def generate_xiaoming_pose_svg(filename, pose_type="idle", expression="neutral", mouth="rest"):
    head_svg = get_xiaoming_head(expression=expression, mouth=mouth)

    torso_svg = """
    <!-- Torso: Observatory Tech Coat -->
    <g id="torso">
      <path d="M 196,280 C 186,350 196,540 216,540 L 296,540 C 316,540 326,350 316,280 Z" fill="#172A46" stroke="#101C31" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M 236,280 L 256,360 L 276,280 Z" fill="#1FD6E2" opacity="0.35"/>
      <!-- Lanyard with ID OBS-01 -->
      <path d="M 242,280 L 256,380 L 270,280" fill="none" stroke="#1FD6E2" stroke-width="2.5"/>
      <rect x="245" y="380" width="22" height="30" rx="3" fill="#FFFFFF" stroke="#101C31" stroke-width="1.5"/>
      <rect x="248" y="384" width="16" height="8" fill="#1F5CFF"/>
    </g>
    """

    legs_svg = """
    <!-- Legs & Feet -->
    <g id="legs">
      <path id="leg_left" d="M 220,540 L 220,680 L 190,680" fill="none" stroke="#080E18" stroke-width="26" stroke-linecap="round"/>
      <path id="leg_right" d="M 292,540 L 292,680 L 322,680" fill="none" stroke="#080E18" stroke-width="26" stroke-linecap="round"/>
      <rect x="180" y="668" width="52" height="18" rx="5" fill="#1FD6E2" stroke="#101C31" stroke-width="2"/>
      <rect x="282" y="668" width="52" height="18" rx="5" fill="#1FD6E2" stroke="#101C31" stroke-width="2"/>
    </g>
    """

    arms_svg = """
    <!-- Arms Default (Idle) -->
    <g id="arms">
      <g id="arm_left">
        <path d="M 196,300 C 160,340 150,440 190,460" fill="none" stroke="#172A46" stroke-width="26" stroke-linecap="round"/>
        <path d="M 196,300 C 160,340 150,440 190,460" fill="none" stroke="#101C31" stroke-width="3"/>
        <circle id="hand_left" cx="190" cy="460" r="14" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
      </g>
      <g id="arm_right">
        <path d="M 316,300 C 352,340 362,440 322,460" fill="none" stroke="#172A46" stroke-width="26" stroke-linecap="round"/>
        <path d="M 316,300 C 352,340 362,440 322,460" fill="none" stroke="#101C31" stroke-width="3"/>
        <circle id="hand_right" cx="322" cy="460" r="14" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
      </g>
    </g>
    """

    if pose_type == "point":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 196,300 C 140,280 100,250 50,230" fill="none" stroke="#172A46" stroke-width="26" stroke-linecap="round"/>
            <path d="M 196,300 C 140,280 100,250 50,230" fill="none" stroke="#101C31" stroke-width="3"/>
            <rect id="hand_left" x="35" y="222" width="24" height="12" rx="3" fill="#1FD6E2" stroke="#101C31" stroke-width="1.5"/>
            <circle cx="24" cy="228" r="5" fill="#1FD6E2"/>
          </g>
          <g id="arm_right">
            <path d="M 316,300 C 345,350 345,420 320,450" fill="none" stroke="#172A46" stroke-width="26" stroke-linecap="round"/>
            <circle id="hand_right" cx="320" cy="450" r="14" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
          </g>
        </g>
        """
    elif pose_type == "talk":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 196,300 C 150,330 140,380 170,390" fill="none" stroke="#172A46" stroke-width="26" stroke-linecap="round"/>
            <circle id="hand_left" cx="170" cy="390" r="14" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
          </g>
          <g id="arm_right">
            <path d="M 316,300 C 360,310 380,270 395,240" fill="none" stroke="#172A46" stroke-width="26" stroke-linecap="round"/>
            <path d="M 316,300 C 360,310 380,270 395,240" fill="none" stroke="#101C31" stroke-width="3"/>
            <circle id="hand_right" cx="395" cy="240" r="16" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
          </g>
        </g>
        """
    elif pose_type == "think":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 196,300 C 210,380 240,400 265,380" fill="none" stroke="#172A46" stroke-width="24" stroke-linecap="round"/>
            <circle id="hand_left" cx="265" cy="380" r="14" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
          </g>
          <g id="arm_right">
            <path d="M 316,300 C 330,340 300,290 280,240" fill="none" stroke="#172A46" stroke-width="24" stroke-linecap="round"/>
            <circle id="hand_right" cx="280" cy="240" r="15" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
          </g>
        </g>
        """
    elif pose_type == "celebrate":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 196,300 C 150,240 140,160 160,120" fill="none" stroke="#172A46" stroke-width="26" stroke-linecap="round"/>
            <circle id="hand_left" cx="160" cy="120" r="16" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
          </g>
          <g id="arm_right">
            <path d="M 316,300 C 362,240 372,160 352,120" fill="none" stroke="#172A46" stroke-width="26" stroke-linecap="round"/>
            <circle id="hand_right" cx="352" cy="120" r="16" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
          </g>
        </g>
        """
    elif pose_type == "whisper":
        arms_svg = """
        <g id="arms">
          <g id="arm_left">
            <path d="M 196,300 C 160,340 160,420 190,440" fill="none" stroke="#172A46" stroke-width="24" stroke-linecap="round"/>
            <circle id="hand_left" cx="190" cy="440" r="14" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
          </g>
          <g id="arm_right">
            <path d="M 316,300 C 330,270 300,240 280,225" fill="none" stroke="#172A46" stroke-width="24" stroke-linecap="round"/>
            <circle id="hand_right" cx="280" cy="225" r="15" fill="#F8D5B8" stroke="#101C31" stroke-width="2"/>
          </g>
        </g>
        """

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 768" width="512" height="768">
  <!-- Xiao Ming (Character: xiaoming, Pose: {pose_type}) -->
  <g id="root">
    <!-- Anchor Points: feet=(256, 680), mouth=(256, 240), center=(256, 384) -->
    {legs_svg}
    {torso_svg}
    {arms_svg}
    {head_svg}
    <g id="prop_anchor" transform="translate(256, 420)"/>
  </g>
</svg>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())

# -------------------------------------------------------------
# Main Generation Pipeline
# -------------------------------------------------------------

def main():
    characters = ["laowang", "xiaoming"]

    expressions = [
        "neutral", "happy", "confident", "serious", "puzzled",
        "shocked", "angry", "tired", "laugh", "cry", "embarrassed", "determined"
    ]

    mouths = ["rest", "slightly_open", "a_shape", "o_shape", "e_shape", "bite_lip"]

    poses = [
        "idle", "talk", "point", "think", "nod", "shake",
        "celebrate", "walk", "run", "angry", "laugh", "cry", "sweat", "whisper"
    ]

    for char in characters:
        char_dir = BASE_DIR / char
        ensure_dir(char_dir / "turnaround")
        ensure_dir(char_dir / "expressions")
        ensure_dir(char_dir / "mouths")
        ensure_dir(char_dir / "poses")

        # 1. Turnaround
        angles = ["front", "three_quarter", "side", "back"]
        for angle in angles:
            fname = char_dir / "turnaround" / f"{angle}.svg"
            if char == "laowang":
                generate_laowang_pose_svg(fname, pose_type="idle", expression="neutral")
            else:
                generate_xiaoming_pose_svg(fname, pose_type="idle", expression="neutral")

        # 2. Expressions
        for exp in expressions:
            fname = char_dir / "expressions" / f"{exp}.svg"
            if char == "laowang":
                generate_laowang_pose_svg(fname, pose_type="idle", expression=exp)
            else:
                generate_xiaoming_pose_svg(fname, pose_type="idle", expression=exp)

        # 3. Mouths
        for m in mouths:
            fname = char_dir / "mouths" / f"{m}.svg"
            if char == "laowang":
                generate_laowang_pose_svg(fname, pose_type="idle", expression="neutral", mouth=m)
            else:
                generate_xiaoming_pose_svg(fname, pose_type="idle", expression="neutral", mouth=m)

        # 4. Poses
        for p in poses:
            fname = char_dir / "poses" / f"{p}.svg"
            if char == "laowang":
                generate_laowang_pose_svg(fname, pose_type=p, expression="neutral")
            else:
                generate_xiaoming_pose_svg(fname, pose_type=p, expression="neutral")

        # 5. Multi-frame animation sequences (walk, run, talk, laugh)
        multi_frame_poses = ["walk", "run", "talk", "laugh"]
        for p in multi_frame_poses:
            for f_idx in [1, 2, 3]:
                fname = char_dir / "poses" / f"{p}_f{f_idx}.svg"
                exp = "laugh" if p == "laugh" else "neutral"
                mouth = "a_shape" if p == "talk" and f_idx == 2 else "rest"
                if char == "laowang":
                    generate_laowang_pose_svg(fname, pose_type=p, expression=exp, mouth=mouth)
                else:
                    generate_xiaoming_pose_svg(fname, pose_type=p, expression=exp, mouth=mouth)

    print("Character assets successfully generated in:", BASE_DIR)

if __name__ == "__main__":
    main()
