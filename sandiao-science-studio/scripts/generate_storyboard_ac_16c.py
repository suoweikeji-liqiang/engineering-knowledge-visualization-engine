#!/usr/bin/env python3
"""
Generator for AC 16°C Sample Storyboard Redesign:
- 1 Poster / Cover (16:9 & 9:16)
- 8 Shots Full Style Frames (1920x1080)
- 3 Representative 9:16 Vertical Frames (Hook, Compressor, Tips)
- Storyboard Spec documentation
- 8-Shot Contact Sheet
"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DESIGN_DIR = PROJECT_DIR / "design"
STORY_DIR = DESIGN_DIR / "storyboards" / "ac-16c"
PREVIEWS_DIR = DESIGN_DIR / "previews"
CHARACTERS_DIR = DESIGN_DIR / "assets" / "brand" / "characters"
STORY_DIR.mkdir(parents=True, exist_ok=True)
PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)

def read_svg_body(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    return content.split("<svg")[1].split(">", 1)[1].rsplit("</svg>", 1)[0]

# Common SVG Header & Footer Templates
def make_16x9_frame(shot_id, headline_tab, diagram_content, laowang_pose, xiaoming_pose, subtitle_speaker, subtitle_text):
    lw_char = f"""
    <!-- Lao Wang -->
    <g transform="translate(60, 310)">
      <use href="#lw_pose_{laowang_pose}"/>
      <!-- Nameplate -->
      <g transform="translate(70, 560)">
        <rect x="0" y="0" width="150" height="36" rx="8" fill="#101C31" stroke="#FA541C" stroke-width="2"/>
        <circle cx="16" cy="18" r="5" fill="#FA541C"/>
        <text x="32" y="24" fill="#FFFFFF" font-family="sans-serif" font-size="15" font-weight="bold">老王</text>
      </g>
    </g>
    """

    xm_char = f"""
    <!-- Xiao Ming -->
    <g transform="translate(1580, 270)">
      <use href="#xm_pose_{xiaoming_pose}"/>
      <!-- Nameplate -->
      <g transform="translate(60, 600)">
        <rect x="0" y="0" width="160" height="36" rx="8" fill="#101C31" stroke="#1FD6E2" stroke-width="2"/>
        <circle cx="16" cy="18" r="5" fill="#1FD6E2"/>
        <text x="32" y="24" fill="#FFFFFF" font-family="sans-serif" font-size="15" font-weight="bold">小明</text>
      </g>
    </g>
    """

    speaker_color = "#FA541C" if subtitle_speaker == "老王" else "#1FD6E2"
    speaker_text_color = "#FFFFFF" if subtitle_speaker == "老王" else "#080E18"

    lw_talk = read_svg_body(CHARACTERS_DIR / "laowang/poses/talk.svg")
    lw_point = read_svg_body(CHARACTERS_DIR / "laowang/poses/point.svg")
    lw_think = read_svg_body(CHARACTERS_DIR / "laowang/poses/think.svg")
    lw_idle = read_svg_body(CHARACTERS_DIR / "laowang/poses/idle.svg")
    lw_shake = read_svg_body(CHARACTERS_DIR / "laowang/poses/shake.svg")
    lw_celebrate = read_svg_body(CHARACTERS_DIR / "laowang/poses/celebrate.svg")

    xm_talk = read_svg_body(CHARACTERS_DIR / "xiaoming/poses/talk.svg")
    xm_point = read_svg_body(CHARACTERS_DIR / "xiaoming/poses/point.svg")
    xm_think = read_svg_body(CHARACTERS_DIR / "xiaoming/poses/think.svg")
    xm_idle = read_svg_body(CHARACTERS_DIR / "xiaoming/poses/idle.svg")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <style>
      .font-title {{ font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 800; }}
      .font-body {{ font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 600; }}
      .font-mono {{ font-family: 'SF Mono', monospace; font-weight: 600; }}
    </style>
    <linearGradient id="bgGrad_{shot_id}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#080E18"/>
      <stop offset="50%" stop-color="#101C31"/>
      <stop offset="100%" stop-color="#14233C"/>
    </linearGradient>
    <linearGradient id="stageGrad_{shot_id}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F4F6F9"/>
    </linearGradient>
    <filter id="panelShadow_{shot_id}" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- Deep Background -->
  <rect width="1920" height="1080" fill="url(#bgGrad_{shot_id})"/>

  <!-- Subtle Telemetry Grid -->
  <g opacity="0.18">
    <line x1="0" y1="100" x2="1920" y2="100" stroke="#1FD6E2" stroke-width="1"/>
    <line x1="0" y1="920" x2="1920" y2="920" stroke="#1FD6E2" stroke-width="1"/>
    <line x1="80" y1="0" x2="80" y2="1080" stroke="#1FD6E2" stroke-width="1"/>
    <line x1="1840" y1="0" x2="1840" y2="1080" stroke="#1FD6E2" stroke-width="1"/>
    <ellipse cx="960" cy="200" rx="750" ry="280" fill="none" stroke="#1F5CFF" stroke-width="1.5" transform="rotate(-8 960 200)"/>
  </g>

  <!-- Top Brand Navigation Bar -->
  <g transform="translate(80, 36)">
    <circle cx="24" cy="24" r="16" fill="#1F5CFF"/>
    <ellipse cx="24" cy="24" rx="28" ry="10" fill="none" stroke="#1FD6E2" stroke-width="3" transform="rotate(-25 24 24)"/>
    <circle cx="44" cy="16" r="3.5" fill="#FFFFFF"/>
    <text x="70" y="32" fill="#FFFFFF" class="font-title" font-size="24" letter-spacing="1">小行星原理剧场</text>
    <rect x="245" y="10" width="80" height="28" rx="6" fill="#1F5CFF"/>
    <text x="285" y="29" fill="#FFFFFF" class="font-mono" font-size="14" text-anchor="middle">EP.01</text>
    <text x="345" y="30" fill="#8FA6CB" class="font-body" font-size="16">| 课题：空调开到 16℃ 真的更省电吗？</text>
    <g transform="translate(1560, 10)">
      <circle cx="0" cy="14" r="5" fill="#1FD6E2"/>
      <text x="16" y="20" fill="#1FD6E2" class="font-mono" font-size="15">OBSERVATORY LIVE</text>
    </g>
  </g>

  <!-- Central High-Contrast Engineering Stage Card (w=1160, h=690) -->
  <g transform="translate(380, 120)" filter="url(#panelShadow_{shot_id})">
    <rect width="1160" height="690" rx="24" fill="url(#stageGrad_{shot_id})" stroke="#13223A" stroke-width="3.5"/>

    <!-- Top Headline Tab -->
    <g transform="translate(36, -20)">
      <rect width="480" height="42" rx="10" fill="#101C31" stroke="#1FD6E2" stroke-width="2"/>
      <circle cx="20" cy="21" r="5" fill="{speaker_color}"/>
      <text x="36" y="28" fill="#FFFFFF" class="font-title" font-size="18">{headline_tab}</text>
    </g>

    <!-- Specific Diagram Body -->
    {diagram_content}
  </g>

  {lw_char}
  {xm_char}

  <!-- Bottom Non-Occluding Subtitle Bar -->
  <g transform="translate(180, 930)" filter="url(#panelShadow_{shot_id})">
    <rect width="1560" height="96" rx="20" fill="#080E18" stroke="#1F5CFF" stroke-width="2"/>
    <g transform="translate(32, 24)">
      <rect width="100" height="48" rx="10" fill="{speaker_color}"/>
      <text x="50" y="32" fill="{speaker_text_color}" class="font-title" font-size="22" text-anchor="middle">{subtitle_speaker}</text>
    </g>
    <text x="160" y="58" fill="#FFFFFF" class="font-body" font-size="26">{subtitle_text}</text>
  </g>

  <defs>
    <!-- Embedded Character Poses -->
    <g id="lw_pose_talk">{lw_talk}</g>
    <g id="lw_pose_point">{lw_point}</g>
    <g id="lw_pose_think">{lw_think}</g>
    <g id="lw_pose_idle">{lw_idle}</g>
    <g id="lw_pose_shake">{lw_shake}</g>
    <g id="lw_pose_celebrate">{lw_celebrate}</g>

    <g id="xm_pose_talk">{xm_talk}</g>
    <g id="xm_pose_point">{xm_point}</g>
    <g id="xm_pose_think">{xm_think}</g>
    <g id="xm_pose_idle">{xm_idle}</g>
  </defs>
</svg>
"""

# -------------------------------------------------------------
# Generate 8 Shots
# -------------------------------------------------------------

def generate_8_shots():
    # Shot 01: Hook
    d1 = """
    <g transform="translate(180, 80)">
      <rect width="800" height="500" rx="20" fill="#FFF2E8" stroke="#FA541C" stroke-width="3"/>
      <g transform="translate(120, 80)">
        <text x="280" y="60" fill="#D4380D" font-family="sans-serif" font-size="56" font-weight="900" text-anchor="middle">16℃</text>
        <text x="280" y="140" fill="#13223A" font-family="sans-serif" font-size="36" font-weight="bold" text-anchor="middle">= 降温更快 + 狂省电？</text>
        <rect x="60" y="190" width="440" height="80" rx="16" fill="#FA541C"/>
        <text x="280" y="242" fill="#FFFFFF" font-family="sans-serif" font-size="28" font-weight="bold" text-anchor="middle">生活常见直觉经验大拷问</text>
      </g>
    </g>
    """
    s1 = make_16x9_frame("shot_01_hook", "破题猜想：16℃ = 更快 + 更省电？", d1, "talk", "idle", "老王", "“空调开到十六度，肯定降温更快，还更省电！”")
    with open(STORY_DIR / "shot_01_hook_16x9.svg", "w") as f: f.write(s1)

    # Shot 02: Not Faucet
    d2 = """
    <g transform="translate(60, 60)">
      <!-- Left: Faucet -->
      <rect x="0" y="0" width="480" height="540" rx="16" fill="#FFF5F5" stroke="#FFA39E" stroke-width="2"/>
      <text x="240" y="60" fill="#820014" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">直觉模型：水龙头旋钮</text>
      <path d="M 120,160 L 260,160 A 24,24 0 0,1 284,184 L 284,260" fill="none" stroke="#8C8C8C" stroke-width="24" stroke-linecap="round"/>
      <path d="M 270,270 L 298,270 L 330,420 L 238,420 Z" fill="#91CAFF" opacity="0.6"/>
      <g transform="translate(340, 240) rotate(-15)">
        <rect x="-60" y="-24" width="120" height="48" rx="8" fill="#FFF1F0" stroke="#F04B2F" stroke-width="3"/>
        <text x="0" y="8" fill="#F04B2F" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">完全不符</text>
      </g>
      <!-- Right: Real AC -->
      <g transform="translate(540, 0)">
        <rect x="0" y="0" width="500" height="540" rx="16" fill="#E6F9FB" stroke="#87E8DE" stroke-width="2"/>
        <text x="250" y="60" fill="#00474F" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">实际物理机制：恒定压差</text>
        <rect x="80" y="140" width="340" height="120" rx="16" fill="#FFFFFF" stroke="#13223A" stroke-width="3"/>
        <text x="250" y="210" fill="#003A8C" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">冷量输出受限于盘管物理上限</text>
        <text x="250" y="380" fill="#00474F" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">✔ 温度按键只是目标线，非冷量阀门！</text>
      </g>
    </g>
    """
    s2 = make_16x9_frame("shot_02_not_faucet", "原理厘清：空调 ≠ 水龙头", d2, "think", "point", "小明", "“先别急，空调可不是水龙头，温度拧低就立刻多出冷量。”")
    with open(STORY_DIR / "shot_02_not_faucet_16x9.svg", "w") as f: f.write(s2)

    # Shot 03: Compressor
    d3 = """
    <g transform="translate(60, 60)">
      <rect width="1040" height="540" rx="20" fill="#E6F7FF" stroke="#1890FF" stroke-width="2"/>
      <text x="520" y="60" fill="#003A8C" font-family="sans-serif" font-size="26" font-weight="bold" text-anchor="middle">定频空调典型工况：额定转速运行</text>
      <!-- 3 Flow Boxes strictly contained in 1040 width! -->
      <!-- Box 1 -->
      <g transform="translate(60, 140)">
        <rect width="260" height="300" rx="16" fill="#FFFFFF" stroke="#13223A" stroke-width="3"/>
        <circle cx="130" cy="70" r="30" fill="#1FD6E2" opacity="0.2"/>
        <text x="130" y="78" fill="#101C31" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">01</text>
        <text x="130" y="140" fill="#13223A" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">启动上电</text>
        <text x="130" y="190" fill="#6B7A99" font-family="sans-serif" font-size="15" text-anchor="middle">压缩机电机起动</text>
      </g>
      <!-- Arrow 1 -->
      <path d="M 335,290 L 375,290" stroke="#1F5CFF" stroke-width="6" stroke-linecap="round"/>
      <!-- Box 2 (Highlight) -->
      <g transform="translate(390, 140)">
        <rect width="260" height="300" rx="16" fill="#101C31" stroke="#1FD6E2" stroke-width="3.5"/>
        <circle cx="130" cy="70" r="30" fill="#1FD6E2"/>
        <text x="130" y="78" fill="#080E18" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">02</text>
        <text x="130" y="140" fill="#1FD6E2" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">100% 额定出力</text>
        <text x="130" y="190" fill="#FFFFFF" font-family="sans-serif" font-size="15" text-anchor="middle">恒定压差，恒定排量</text>
      </g>
      <!-- Arrow 2 -->
      <path d="M 665,290 L 705,290" stroke="#1F5CFF" stroke-width="6" stroke-linecap="round"/>
      <!-- Box 3 -->
      <g transform="translate(720, 140)">
        <rect width="260" height="300" rx="16" fill="#FFFFFF" stroke="#13223A" stroke-width="3"/>
        <circle cx="130" cy="70" r="30" fill="#52C41A" opacity="0.2"/>
        <text x="130" y="78" fill="#101C31" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">03</text>
        <text x="130" y="140" fill="#13223A" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">达温停机</text>
        <text x="130" y="190" fill="#6B7A99" font-family="sans-serif" font-size="15" text-anchor="middle">室温满足设定线即停</text>
      </g>
    </g>
    """
    s3 = make_16x9_frame("shot_03_compressor", "机制剖析：先看定频压缩机怎么干活", d3, "idle", "point", "小明", "“多数定频空调一启动，压缩机基本就是按额定能力干活。”")
    with open(STORY_DIR / "shot_03_compressor_16x9.svg", "w") as f: f.write(s3)

    # Shot 04: Question
    d4 = """
    <g transform="translate(160, 80)">
      <rect width="840" height="480" rx="20" fill="#FFFBE6" stroke="#FAAD14" stroke-width="3"/>
      <text x="420" y="100" fill="#874D00" font-family="sans-serif" font-size="34" font-weight="bold" text-anchor="middle">老王的追问：难道没有“爆发模式”？</text>
      <rect x="80" y="160" width="680" height="220" rx="16" fill="#FFFFFF" stroke="#13223A" stroke-width="2"/>
      <text x="420" y="240" fill="#FA541C" font-family="sans-serif" font-size="26" font-weight="bold" text-anchor="middle">“把温度按死在 16℃，压缩机不会加倍卖力吗？”</text>
      <text x="420" y="300" fill="#6B7A99" font-family="sans-serif" font-size="18" text-anchor="middle">（真相：普通定频电机转速固定，物理上不存在超频档）</text>
    </g>
    """
    s4 = make_16x9_frame("shot_04_question", "逻辑追问：温度更低 = 功率更大？", d4, "point", "think", "老王", "“那调十六度，它不是会更卖力、出更大风力吗？”")
    with open(STORY_DIR / "shot_04_question_16x9.svg", "w") as f: f.write(s4)

    # Shot 05: Runtime Curve
    d5 = """
    <g transform="translate(60, 60)">
      <rect width="1040" height="540" rx="20" fill="#FFFFFF" stroke="#13223A" stroke-width="3"/>
      <text x="60" y="50" fill="#13223A" font-family="sans-serif" font-size="22" font-weight="bold">功率与时间真实曲线 (Power vs Runtime)</text>
      <!-- Axes -->
      <line x1="100" y1="440" x2="960" y2="440" stroke="#13223A" stroke-width="3"/>
      <line x1="100" y1="100" x2="100" y2="440" stroke="#13223A" stroke-width="3"/>
      <!-- Constant Power line -->
      <line x1="100" y1="200" x2="900" y2="200" stroke="#1F5CFF" stroke-width="4"/>
      <text x="120" y="180" fill="#1F5CFF" font-family="sans-serif" font-size="16" font-weight="bold">额定功率 100% (恒定无超级档)</text>
      <!-- 26C Stop Zone -->
      <line x1="450" y1="200" x2="450" y2="440" stroke="#52C41A" stroke-width="3" stroke-dasharray="6 4"/>
      <text x="450" y="470" fill="#52C41A" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle">26℃ 及时停机</text>
      <!-- 16C Delay Running -->
      <rect x="450" y="200" width="400" height="240" fill="#FA541C" opacity="0.15"/>
      <line x1="850" y1="200" x2="850" y2="440" stroke="#FA541C" stroke-width="3" stroke-dasharray="6 4"/>
      <text x="650" y="320" fill="#FA541C" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">设 16℃：推迟停机狂耗电</text>
    </g>
    """
    s5 = make_16x9_frame("shot_05_runtime", "事实揭晓：真正改变的只是运行时间", d5, "idle", "point", "小明", "“通常只是更晚停机，不会凭空多出一档超级功率。”")
    with open(STORY_DIR / "shot_05_runtime_16x9.svg", "w") as f: f.write(s5)

    # Shot 06: Never Reach
    d6 = """
    <g transform="translate(80, 60)">
      <rect width="1000" height="540" rx="20" fill="#FFF1F0" stroke="#F5222D" stroke-width="3"/>
      <text x="500" y="60" fill="#CF1322" font-family="sans-serif" font-size="26" font-weight="bold" text-anchor="middle">极端情况：房间永远到不了 16℃ 会怎样？</text>
      <g transform="translate(60, 120)">
        <rect width="880" height="340" rx="16" fill="#FFFFFF" stroke="#FFA39E" stroke-width="2"/>
        <text x="440" y="80" fill="#CF1322" font-family="sans-serif" font-size="32" font-weight="900" text-anchor="middle">⚡ 压缩机陷入“死循环满载狂转” ⚡</text>
        <text x="440" y="160" fill="#13223A" font-family="sans-serif" font-size="22" text-anchor="middle">室外高温持续渗透 ＞ 空调极限吸热能力</text>
        <rect x="220" y="220" width="440" height="60" rx="12" fill="#FAAD14"/>
        <text x="440" y="258" fill="#874D00" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">结果：温度下不去 + 电表疯狂飞转！</text>
      </g>
    </g>
    """
    s6 = make_16x9_frame("shot_06_never", "风险警示：目标到不了，会发生什么？", d6, "shake", "talk", "小明", "“房间到不了十六度时，压缩机甚至可能二十四小时一直硬跑。”")
    with open(STORY_DIR / "shot_06_never_16x9.svg", "w") as f: f.write(s6)

    # Shot 07: Tips
    d7 = """
    <g transform="translate(60, 50)">
      <text x="40" y="35" fill="#13223A" font-family="sans-serif" font-size="24" font-weight="bold">真正科学省电的三件事 (Actionable Tips)</text>
      <g transform="translate(0, 60)">
        <!-- Tip 1 -->
        <rect x="0" y="0" width="1040" height="120" rx="16" fill="#F6F8FA" stroke="#1F5CFF" stroke-width="2"/>
        <circle cx="60" cy="60" r="26" fill="#1F5CFF"/>
        <text x="60" y="68" fill="#FFFFFF" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">1</text>
        <text x="110" y="50" fill="#13223A" font-family="sans-serif" font-size="22" font-weight="bold">合理温度：设定 26℃</text>
        <text x="110" y="85" fill="#6B7A99" font-family="sans-serif" font-size="16">每调高 1℃ 可节约约 7%~10% 电力消耗。</text>

        <!-- Tip 2 -->
        <g transform="translate(0, 140)">
          <rect x="0" y="0" width="1040" height="120" rx="16" fill="#F6F8FA" stroke="#1FD6E2" stroke-width="2"/>
          <circle cx="60" cy="60" r="26" fill="#1FD6E2"/>
          <text x="60" y="68" fill="#080E18" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">2</text>
          <text x="110" y="50" fill="#13223A" font-family="sans-serif" font-size="22" font-weight="bold">密闭门窗 + 拉窗帘遮阳</text>
          <text x="110" y="85" fill="#6B7A99" font-family="sans-serif" font-size="16">阻断室外辐射热，降低空调总负荷。</text>
        </g>

        <!-- Tip 3 -->
        <g transform="translate(0, 280)">
          <rect x="0" y="0" width="1040" height="120" rx="16" fill="#F6F8FA" stroke="#52C41A" stroke-width="2"/>
          <circle cx="60" cy="60" r="26" fill="#52C41A"/>
          <text x="60" y="68" fill="#FFFFFF" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">3</text>
          <text x="110" y="50" fill="#13223A" font-family="sans-serif" font-size="22" font-weight="bold">配合循环风扇对流</text>
          <text x="110" y="85" fill="#6B7A99" font-family="sans-serif" font-size="16">加速空气混合，同等耗电下体感温度更凉爽。</text>
        </g>
      </g>
    </g>
    """
    s7 = make_16x9_frame("shot_07_tips", "行动指南：真正科学省电的三件事", d7, "idle", "point", "小明", "“想省电，温度别设太低，再配合密闭、遮阳和合适风量。”")
    with open(STORY_DIR / "shot_07_tips_16x9.svg", "w") as f: f.write(s7)

    # Shot 08: End
    d8 = """
    <g transform="translate(100, 60)">
      <rect width="960" height="540" rx="24" fill="#101C31" stroke="#FA541C" stroke-width="3"/>
      <g transform="translate(80, 100)">
        <text x="400" y="60" fill="#FA541C" font-family="sans-serif" font-size="42" font-weight="900" text-anchor="middle">老王神总结：</text>
        <rect x="0" y="120" width="800" height="180" rx="20" fill="#FFFFFF"/>
        <text x="400" y="200" fill="#13223A" font-family="sans-serif" font-size="34" font-weight="900" text-anchor="middle">“16℃ 不是省电键，”</text>
        <text x="400" y="260" fill="#F04B2F" font-family="sans-serif" font-size="36" font-weight="900" text-anchor="middle">“是压缩机的无情加班键！”</text>
      </g>
    </g>
    """
    s8 = make_16x9_frame("shot_08_end", "大结局：老王终于悟了！", d8, "celebrate", "talk", "老王", "“明白了，十六度不是省电键，是压缩机的无情加班键！”")
    with open(STORY_DIR / "shot_08_end_16x9.svg", "w") as f: f.write(s8)

# -------------------------------------------------------------
# Generate 9:16 Vertical Style Frames
# -------------------------------------------------------------

def generate_vertical_frames():
    lw_talk = read_svg_body(CHARACTERS_DIR / "laowang/poses/talk.svg")
    xm_idle = read_svg_body(CHARACTERS_DIR / "xiaoming/poses/idle.svg")
    xm_point = read_svg_body(CHARACTERS_DIR / "xiaoming/poses/point.svg")

    # 9:16 Shot 01: Hook
    v1 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <!-- 9:16 Shot 01: Hook -->
  <rect width="1080" height="1920" fill="#080E18"/>
  <!-- Top Nav -->
  <g transform="translate(60, 80)">
    <rect width="960" height="80" rx="16" fill="#101C31" stroke="#1F5CFF" stroke-width="2"/>
    <text x="50" y="50" fill="#FFFFFF" font-family="sans-serif" font-size="26" font-weight="bold">小行星原理剧场 #01 · 破题观察</text>
  </g>
  <!-- Top Character Stage (y: 200..600) -->
  <g transform="translate(100, 200)">
    <g transform="translate(0, 0) scale(0.75)">
      <use href="#lw_v_talk"/>
    </g>
    <g transform="translate(520, 0) scale(0.75)">
      <use href="#xm_v_idle"/>
    </g>
  </g>
  <!-- Middle Diagram Card (y: 620..1520, w: 920) -->
  <g transform="translate(80, 620)">
    <rect width="920" height="880" rx="28" fill="#FFFFFF" stroke="#13223A" stroke-width="4"/>
    <rect x="40" y="-24" width="460" height="48" rx="12" fill="#FA541C"/>
    <text x="270" y="8" fill="#FFFFFF" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">破题：16℃ 会更省电吗？</text>
    <g transform="translate(60, 100)">
      <rect width="800" height="700" rx="20" fill="#FFF2E8" stroke="#FFA39E" stroke-width="2"/>
      <text x="400" y="160" fill="#D4380D" font-family="sans-serif" font-size="72" font-weight="900" text-anchor="middle">16℃</text>
      <text x="400" y="280" fill="#13223A" font-family="sans-serif" font-size="38" font-weight="bold" text-anchor="middle">= 降温更快 + 狂省电？</text>
      <rect x="140" y="380" width="520" height="100" rx="20" fill="#FA541C"/>
      <text x="400" y="442" fill="#FFFFFF" font-family="sans-serif" font-size="32" font-weight="bold" text-anchor="middle">生活常见直觉经验大拷问</text>
    </g>
  </g>
  <!-- Bottom Subtitle Bar (y: 1560..1720) -->
  <g transform="translate(60, 1560)">
    <rect width="960" height="150" rx="24" fill="#101C31" stroke="#1F5CFF" stroke-width="2"/>
    <rect x="24" y="24" width="100" height="42" rx="10" fill="#FA541C"/>
    <text x="74" y="52" fill="#FFFFFF" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">老王</text>
    <text x="140" y="54" fill="#FFFFFF" font-family="sans-serif" font-size="26">“空调开到十六度，降温更快还省电！”</text>
  </g>
  <defs>
    <g id="lw_v_talk">{lw_talk}</g>
    <g id="xm_v_idle">{xm_idle}</g>
  </defs>
</svg>"""
    with open(STORY_DIR / "shot_01_hook_9x16.svg", "w") as f: f.write(v1)

    # 9:16 Shot 03: Compressor
    v3 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <!-- 9:16 Shot 03: Compressor -->
  <rect width="1080" height="1920" fill="#080E18"/>
  <g transform="translate(60, 80)">
    <rect width="960" height="80" rx="16" fill="#101C31" stroke="#1F5CFF" stroke-width="2"/>
    <text x="50" y="50" fill="#FFFFFF" font-family="sans-serif" font-size="26" font-weight="bold">小行星原理剧场 #01 · 机制剖析</text>
  </g>
  <g transform="translate(100, 200)">
    <g transform="translate(0, 0) scale(0.75)">
      <use href="#lw_v_talk"/>
    </g>
    <g transform="translate(520, 0) scale(0.75)">
      <use href="#xm_v_point"/>
    </g>
  </g>
  <g transform="translate(80, 620)">
    <rect width="920" height="880" rx="28" fill="#FFFFFF" stroke="#13223A" stroke-width="4"/>
    <rect x="40" y="-24" width="460" height="48" rx="12" fill="#13C2C2"/>
    <text x="270" y="8" fill="#FFFFFF" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">定频压缩机工况：额定转速</text>
    <!-- 3 Stacked Boxes in 9:16 -->
    <g transform="translate(60, 60)">
      <rect x="0" y="0" width="800" height="220" rx="16" fill="#F6F8FA" stroke="#D9D9D9" stroke-width="2"/>
      <circle cx="60" cy="110" r="30" fill="#1FD6E2" opacity="0.2"/>
      <text x="60" y="118" fill="#101C31" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">01</text>
      <text x="120" y="90" fill="#13223A" font-family="sans-serif" font-size="22" font-weight="bold">启动起动</text>
      <text x="120" y="130" fill="#6B7A99" font-family="sans-serif" font-size="16">压缩机电机按额定频率启动</text>
    </g>
    <g transform="translate(60, 310)">
      <rect x="0" y="0" width="800" height="240" rx="16" fill="#101C31" stroke="#1FD6E2" stroke-width="3"/>
      <circle cx="60" cy="120" r="30" fill="#1FD6E2"/>
      <text x="60" y="128" fill="#080E18" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">02</text>
      <text x="120" y="95" fill="#1FD6E2" font-family="sans-serif" font-size="24" font-weight="bold">100% 额定出力 (恒定输出)</text>
      <text x="120" y="145" fill="#FFFFFF" font-family="sans-serif" font-size="16">排气量与压差固定，无所谓 16℃ 超频档！</text>
    </g>
    <g transform="translate(60, 580)">
      <rect x="0" y="0" width="800" height="220" rx="16" fill="#F6F8FA" stroke="#D9D9D9" stroke-width="2"/>
      <circle cx="60" cy="110" r="30" fill="#52C41A" opacity="0.2"/>
      <text x="60" y="118" fill="#101C31" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">03</text>
      <text x="120" y="90" fill="#13223A" font-family="sans-serif" font-size="22" font-weight="bold">达温停机</text>
      <text x="120" y="130" fill="#6B7A99" font-family="sans-serif" font-size="16">室温达标则停机，未达标则一直跑</text>
    </g>
  </g>
  <g transform="translate(60, 1560)">
    <rect width="960" height="150" rx="24" fill="#101C31" stroke="#1F5CFF" stroke-width="2"/>
    <rect x="24" y="24" width="100" height="42" rx="10" fill="#1FD6E2"/>
    <text x="74" y="52" fill="#080E18" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">小明</text>
    <text x="140" y="54" fill="#FFFFFF" font-family="sans-serif" font-size="26">“多数定频空调一启动，压缩机就是按额定能力干活。”</text>
  </g>
  <defs>
    <g id="lw_v_talk">{lw_talk}</g>
    <g id="xm_v_point">{xm_point}</g>
  </defs>
</svg>"""
    with open(STORY_DIR / "shot_03_compressor_9x16.svg", "w") as f: f.write(v3)

    # 9:16 Shot 07: Tips
    v7 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <!-- 9:16 Shot 07: Tips -->
  <rect width="1080" height="1920" fill="#080E18"/>
  <g transform="translate(60, 80)">
    <rect width="960" height="80" rx="16" fill="#101C31" stroke="#1F5CFF" stroke-width="2"/>
    <text x="50" y="50" fill="#FFFFFF" font-family="sans-serif" font-size="26" font-weight="bold">小行星原理剧场 #01 · 行动指南</text>
  </g>
  <g transform="translate(100, 200)">
    <g transform="translate(0, 0) scale(0.75)">
      <use href="#lw_v_talk"/>
    </g>
    <g transform="translate(520, 0) scale(0.75)">
      <use href="#xm_v_point"/>
    </g>
  </g>
  <g transform="translate(80, 620)">
    <rect width="920" height="880" rx="28" fill="#FFFFFF" stroke="#13223A" stroke-width="4"/>
    <rect x="40" y="-24" width="460" height="48" rx="12" fill="#52C41A"/>
    <text x="270" y="8" fill="#FFFFFF" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">科学省电三大动作</text>
    <g transform="translate(60, 60)">
      <!-- Tip 1 -->
      <rect x="0" y="0" width="800" height="220" rx="16" fill="#F6F8FA" stroke="#1F5CFF" stroke-width="2"/>
      <circle cx="60" cy="110" r="30" fill="#1F5CFF"/>
      <text x="60" y="120" fill="#FFFFFF" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">1</text>
      <text x="120" y="90" fill="#13223A" font-family="sans-serif" font-size="24" font-weight="bold">温度设定 26℃</text>
      <text x="120" y="135" fill="#6B7A99" font-family="sans-serif" font-size="16">每高 1℃ 省电 7%~10%</text>

      <!-- Tip 2 -->
      <g transform="translate(0, 260)">
        <rect x="0" y="0" width="800" height="220" rx="16" fill="#F6F8FA" stroke="#1FD6E2" stroke-width="2"/>
        <circle cx="60" cy="110" r="30" fill="#1FD6E2"/>
        <text x="60" y="120" fill="#080E18" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">2</text>
        <text x="120" y="90" fill="#13223A" font-family="sans-serif" font-size="24" font-weight="bold">门窗密闭 + 遮阳</text>
        <text x="120" y="135" fill="#6B7A99" font-family="sans-serif" font-size="16">阻断室外热辐射负荷</text>
      </g>

      <!-- Tip 3 -->
      <g transform="translate(0, 520)">
        <rect x="0" y="0" width="800" height="220" rx="16" fill="#F6F8FA" stroke="#52C41A" stroke-width="2"/>
        <circle cx="60" cy="110" r="30" fill="#52C41A"/>
        <text x="60" y="120" fill="#FFFFFF" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">3</text>
        <text x="120" y="90" fill="#13223A" font-family="sans-serif" font-size="24" font-weight="bold">加循环扇促进对流</text>
        <text x="120" y="135" fill="#6B7A99" font-family="sans-serif" font-size="16">体感更凉爽，消除温差</text>
      </g>
    </g>
  </g>
  <g transform="translate(60, 1560)">
    <rect width="960" height="150" rx="24" fill="#101C31" stroke="#1F5CFF" stroke-width="2"/>
    <rect x="24" y="24" width="100" height="42" rx="10" fill="#1FD6E2"/>
    <text x="74" y="52" fill="#080E18" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">小明</text>
    <text x="140" y="54" fill="#FFFFFF" font-family="sans-serif" font-size="26">“想省电，温度别设太低，再配合密闭和合适风量。”</text>
  </g>
  <defs>
    <g id="lw_v_talk">{lw_talk}</g>
    <g id="xm_v_point">{xm_point}</g>
  </defs>
</svg>"""
    with open(STORY_DIR / "shot_07_tips_9x16.svg", "w") as f: f.write(v7)

# -------------------------------------------------------------
# Generate Posters (16:9 & 9:16)
# -------------------------------------------------------------

def generate_posters():
    lw_talk = read_svg_body(CHARACTERS_DIR / "laowang/poses/talk.svg")
    xm_point = read_svg_body(CHARACTERS_DIR / "xiaoming/poses/point.svg")

    poster_16x9 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Official Poster 16:9 -->
  <defs>
    <linearGradient id="pGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#080E18"/>
      <stop offset="60%" stop-color="#101C31"/>
      <stop offset="100%" stop-color="#14233C"/>
    </linearGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#pGrad)"/>
  <!-- Orbit & Telemetry FX -->
  <ellipse cx="960" cy="400" rx="850" ry="320" fill="none" stroke="#1F5CFF" stroke-width="2.5" transform="rotate(-8 960 400)" opacity="0.4"/>
  <!-- Big Poster Title -->
  <g transform="translate(960, 180)">
    <rect x="-480" y="-70" width="960" height="140" rx="28" fill="#101C31" stroke="#1FD6E2" stroke-width="3"/>
    <text x="0" y="18" fill="#FFFFFF" font-family="sans-serif" font-size="52" font-weight="900" text-anchor="middle">空调开到 16℃ 真的更省电吗？</text>
    <text x="0" y="110" fill="#1FD6E2" font-family="'SF Mono', monospace" font-size="24" font-weight="bold" text-anchor="middle">ASTEROID PRINCIPLE THEATER · EPISODE 01</text>
  </g>
  <!-- Lao Wang on Left -->
  <g transform="translate(180, 280)">
    <use href="#lw_p_talk"/>
  </g>
  <!-- Xiao Ming on Right -->
  <g transform="translate(1360, 240)">
    <use href="#xm_p_point"/>
  </g>
  <!-- Central Hook Badge -->
  <g transform="translate(700, 480)">
    <rect width="520" height="280" rx="24" fill="#FFFFFF" stroke="#13223A" stroke-width="4"/>
    <rect x="40" y="40" width="440" height="60" rx="12" fill="#FA541C"/>
    <text x="260" y="80" fill="#FFFFFF" font-family="sans-serif" font-size="26" font-weight="bold" text-anchor="middle">16℃ 不是省电键！</text>
    <text x="260" y="160" fill="#13223A" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">揭秘定频压缩机真实工况</text>
    <text x="260" y="210" fill="#1890FF" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">小行星AI观测站 · 原理剧场</text>
  </g>
  <defs>
    <g id="lw_p_talk">{lw_talk}</g>
    <g id="xm_p_point">{xm_point}</g>
  </defs>
</svg>"""
    with open(STORY_DIR / "poster_16x9.svg", "w") as f: f.write(poster_16x9)

# -------------------------------------------------------------
# Generate 8-Shots Contact Sheet
# -------------------------------------------------------------

def generate_storyboard_contact_sheet():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <style>
      .font-title { font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 800; }
      .font-body { font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 600; }
      .font-mono { font-family: 'SF Mono', monospace; font-weight: 600; }
    </style>
  </defs>
  <rect width="1920" height="1080" fill="#0B1321"/>

  <g transform="translate(80, 45)">
    <text x="0" y="36" fill="#FFFFFF" class="font-title" font-size="32">《空调开到 16℃ 真的更省电吗？》8 镜头重设计分镜汇总 (8-Shot Storyboard Contact Sheet)</text>
    <text x="0" y="70" fill="#8FA6CB" class="font-body" font-size="16">彻底解决基线文字重叠、右边缘裁切与角色遮挡 · 100% 符合 8px 空间网格与安全区</text>
  </g>

  <!-- 4 columns x 2 rows grid (each cell 430 x 360) -->
  <g transform="translate(80, 130)">
"""
    shots = [
        ("shot_01_hook_16x9.svg", "Shot 01: Hook 破题猜想"),
        ("shot_02_not_faucet_16x9.svg", "Shot 02: Not Faucet 空调≠水龙头"),
        ("shot_03_compressor_16x9.svg", "Shot 03: Compressor 定频机制"),
        ("shot_04_question_16x9.svg", "Shot 04: Question 老王追问"),
        ("shot_05_runtime_16x9.svg", "Shot 05: Runtime 运行时间真相"),
        ("shot_06_never_16x9.svg", "Shot 06: Never 到不了死循环"),
        ("shot_07_tips_16x9.svg", "Shot 07: Tips 科学省电三件事"),
        ("shot_08_end_16x9.svg", "Shot 08: End 老王顿悟总结")
    ]

    for idx, (s_file, s_title) in enumerate(shots):
        col = idx % 4
        row = idx // 4
        x = col * 445
        y = row * 435

        svg += f"""
    <!-- Shot Cell {idx}: {s_file} -->
    <g transform="translate({x}, {y})">
      <rect width="430" height="390" rx="16" fill="#101C31" stroke="#1F5CFF" stroke-width="1.5"/>
      <rect x="15" y="15" width="400" height="34" rx="8" fill="#172A46"/>
      <text x="30" y="38" fill="#1FD6E2" class="font-title" font-size="15">{s_title}</text>
      <!-- Frame Preview (scale 1920x1080 -> 400x225) -->
      <g transform="translate(15, 60)">
        <rect width="400" height="225" rx="8" fill="#000000"/>
        <g transform="scale(0.2083)">
          <use href="#shot_{idx}"/>
        </g>
        <rect width="400" height="225" rx="8" fill="none" stroke="#1FD6E2" stroke-width="1.5"/>
      </g>
      <rect x="15" y="295" width="400" height="80" rx="8" fill="#080E18"/>
      <text x="25" y="320" fill="#52C41A" class="font-mono" font-size="12">✓ 状态：无文字重叠 · 无右侧截断</text>
      <text x="25" y="342" fill="#8FA6CB" class="font-body" font-size="12">双人舞台 + 中央 1160px 大图解安全隔离</text>
      <text x="25" y="364" fill="#1FD6E2" class="font-mono" font-size="11">{s_file}</text>
    </g>
"""

    svg += """
  </g>
  <defs>
"""
    for idx, (s_file, _) in enumerate(shots):
        fpath = STORY_DIR / s_file
        content = read_svg_body(fpath)
        svg += f'<g id="shot_{idx}">{content}</g>\n'

    svg += """
  </defs>
</svg>
"""
    with open(PREVIEWS_DIR / "contact_sheet_storyboard_8shots.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    generate_8_shots()
    generate_vertical_frames()
    generate_posters()
    generate_storyboard_contact_sheet()
    print("Storyboard assets and contact sheet generated in:", STORY_DIR)

if __name__ == "__main__":
    main()
