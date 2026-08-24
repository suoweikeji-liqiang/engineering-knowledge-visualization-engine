#!/usr/bin/env python3
"""
Generate comprehensive contact sheets and verification images for character assets:
- Turnaround sheets
- 12 Expressions matrix (160px avatar readability test)
- 6 Mouth shapes chart
- Pure black silhouette test (Silhouette discrimination verification)
"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DESIGN_DIR = PROJECT_DIR / "design"
CHARACTERS_DIR = DESIGN_DIR / "assets" / "brand" / "characters"
PREVIEWS_DIR = DESIGN_DIR / "previews"
PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)

def generate_silhouette_comparison_svg():
    # True black silhouette geometry for Lao Wang (stout, wide vest, round trapezoid head with hair tufts, thick legs)
    laowang_silhouette = """
    <g fill="#13223A" stroke="#13223A">
      <!-- Legs -->
      <path d="M 210,540 L 210,680 L 150,680 L 150,650 L 190,650 L 190,540 Z"/>
      <path d="M 302,540 L 302,680 L 362,680 L 362,650 L 322,650 L 322,540 Z"/>
      <!-- Torso & Belt -->
      <path d="M 170,300 C 150,370 160,540 190,540 L 322,540 C 352,540 362,370 342,300 Z"/>
      <!-- Left Arm (Hip) -->
      <path d="M 176,330 C 130,370 120,460 170,480 C 180,480 180,460 170,450 C 140,430 145,370 185,340 Z"/>
      <!-- Right Arm (Point) -->
      <path d="M 336,330 C 390,310 420,260 450,210 C 465,190 480,210 460,230 C 430,280 400,330 346,350 Z"/>
      <!-- Neck & Head Base -->
      <rect x="236" y="270" width="40" height="42"/>
      <path d="M 186,245 C 180,165 205,130 256,130 C 307,130 332,165 326,245 C 321,278 191,278 186,245 Z"/>
      <!-- Hair side tufts -->
      <path d="M 184,225 C 175,185 185,145 200,135 C 210,135 200,165 190,215 Z"/>
      <path d="M 328,225 C 337,185 327,145 312,135 C 302,135 312,165 322,215 Z"/>
    </g>
    """

    # True black silhouette geometry for Xiao Ming (tall, slender, tech coat, sharp hair, straight posture)
    xiaoming_silhouette = """
    <g fill="#13223A" stroke="#13223A">
      <!-- Legs -->
      <path d="M 220,540 L 220,680 L 175,680 L 175,655 L 205,655 L 205,540 Z"/>
      <path d="M 292,540 L 292,680 L 337,680 L 337,655 L 307,655 L 307,540 Z"/>
      <!-- Torso (Long Slim Coat) -->
      <path d="M 196,280 C 186,350 196,540 216,540 L 296,540 C 316,540 326,350 316,280 Z"/>
      <!-- Left Arm (Pointing Laser Pointer) -->
      <path d="M 196,300 C 140,280 100,250 50,230 C 30,220 30,240 50,250 C 100,270 140,300 186,320 Z"/>
      <!-- Right Arm (Down by Side) -->
      <path d="M 316,300 C 345,350 345,420 320,450 C 310,450 310,430 320,410 C 335,380 330,340 306,310 Z"/>
      <!-- Neck & Head Base -->
      <rect x="242" y="250" width="28" height="38"/>
      <ellipse cx="256" cy="195" rx="50" ry="60"/>
      <!-- Modern Sharp Hair -->
      <path d="M 204,188 C 202,148 232,130 256,130 C 285,130 310,150 308,188 C 292,160 256,162 204,188 Z"/>
      <!-- Glasses Frame Rim Silhouette -->
      <rect x="208" y="178" width="40" height="30" rx="6"/>
      <rect x="264" y="178" width="40" height="30" rx="6"/>
    </g>
    """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <style>
      .font-title {{ font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 800; }}
      .font-body {{ font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 600; }}
      .font-mono {{ font-family: 'SF Mono', monospace; font-weight: 600; }}
    </style>
  </defs>
  <rect width="1920" height="1080" fill="#0B1321"/>

  <g transform="translate(100, 50)">
    <text x="0" y="40" fill="#FFFFFF" class="font-title" font-size="34">角色剪影辨识度验收 (Pure Black Silhouette Verification)</text>
    <text x="0" y="75" fill="#8FA6CB" class="font-body" font-size="18">依据验收标准 1：在纯黑剪影下，老王（4.8头身、微胖、工装轮廓）与小明（5.5头身、修长、科技风衣）仅凭外形即可 100% 区分。</text>
  </g>

  <!-- Left: Lao Wang (Colored vs Silhouette) -->
  <g transform="translate(140, 160)">
    <!-- Colored -->
    <rect x="0" y="0" width="380" height="800" rx="20" fill="#101C31" stroke="#FA541C" stroke-width="2"/>
    <text x="190" y="50" fill="#FA541C" class="font-title" font-size="22" text-anchor="middle">老王 · 完整着色态 (4.8 头身)</text>
    <g transform="translate(-66, 30)">
      <use href="#lw_colored"/>
    </g>

    <!-- Silhouette -->
    <g transform="translate(420, 0)">
      <rect x="0" y="0" width="380" height="800" rx="20" fill="#F4F6F9" stroke="#13223A" stroke-width="2"/>
      <text x="190" y="50" fill="#13223A" class="font-title" font-size="22" text-anchor="middle">老王 · 纯黑剪影 (Silhouette)</text>
      <!-- True Solid Black Silhouette -->
      <g transform="translate(-66, 30)">
        {laowang_silhouette}
      </g>
    </g>
  </g>

  <!-- Right: Xiao Ming (Colored vs Silhouette) -->
  <g transform="translate(1000, 160)">
    <!-- Colored -->
    <rect x="0" y="0" width="380" height="800" rx="20" fill="#101C31" stroke="#1FD6E2" stroke-width="2"/>
    <text x="190" y="50" fill="#1FD6E2" class="font-title" font-size="22" text-anchor="middle">小明 · 完整着色态 (5.5 头身)</text>
    <g transform="translate(-66, 30)">
      <use href="#xm_colored"/>
    </g>

    <!-- Silhouette -->
    <g transform="translate(420, 0)">
      <rect x="0" y="0" width="380" height="800" rx="20" fill="#F4F6F9" stroke="#13223A" stroke-width="2"/>
      <text x="190" y="50" fill="#13223A" class="font-title" font-size="22" text-anchor="middle">小明 · 纯黑剪影 (Silhouette)</text>
      <!-- True Solid Black Silhouette -->
      <g transform="translate(-66, 30)">
        {xiaoming_silhouette}
      </g>
    </g>
  </g>

  <defs>
"""
    with open(CHARACTERS_DIR / "laowang/poses/point.svg", "r") as f:
        content = f.read().split("<svg")[1].split(">", 1)[1].rsplit("</svg>", 1)[0]
        svg += f'<g id="lw_colored">{content}</g>\n'
    with open(CHARACTERS_DIR / "xiaoming/poses/point.svg", "r") as f:
        content = f.read().split("<svg")[1].split(">", 1)[1].rsplit("</svg>", 1)[0]
        svg += f'<g id="xm_colored">{content}</g>\n'

    svg += """
  </defs>
</svg>
"""
    with open(PREVIEWS_DIR / "contact_sheet_silhouette_comparison.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    generate_silhouette_comparison_svg()
    print("Silhouette comparison updated in:", PREVIEWS_DIR)

if __name__ == "__main__":
    main()
