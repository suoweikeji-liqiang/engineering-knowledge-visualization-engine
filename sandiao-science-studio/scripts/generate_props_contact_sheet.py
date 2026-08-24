#!/usr/bin/env python3
"""
Generate contact sheets for Engineering Props and Diagrams.
"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DESIGN_DIR = PROJECT_DIR / "design"
HVAC_PROPS = DESIGN_DIR / "assets" / "domains" / "hvac" / "props"
SHARED_SYMBOLS = DESIGN_DIR / "assets" / "shared" / "symbols"
PREVIEWS_DIR = DESIGN_DIR / "previews"

def generate_props_contact_sheet():
    props_list = [
        ("hvac-ac-indoor.svg", "室内空调机挂机"),
        ("hvac-ac-outdoor.svg", "室外冷凝器风机机组"),
        ("hvac-compressor.svg", "封闭式定频压缩机剖面"),
        ("hvac-heat-exchanger.svg", "蒸发器 S 型换热盘管"),
        ("hvac-fan.svg", "离心风机叶轮"),
        ("hvac-pipes.svg", "冷媒流动双管系统"),
        ("hvac-expansion-valve.svg", "热力膨胀阀节流阀"),
        ("hvac-sensor-temp.svg", "RTD 温度传感器探头"),
        ("hvac-sensor-pressure.svg", "压阻式压力传感器表"),
        ("hvac-thermometer.svg", "环境水银刻度温度计"),
        ("hvac-electric-meter.svg", "数字有功电能表"),
        ("symbol-water-drop.svg", "冷凝水滴符号"),
        ("symbol-airflow.svg", "空气对流气流矢量"),
        ("symbol-heat-flow.svg", "高温排热热流波纹"),
        ("symbol-cold-flow.svg", "低温制冷冷量雪花"),
        ("symbol-electricity.svg", "电能动力脉冲闪电"),
        ("symbol-warning.svg", "过载警示三角"),
        ("symbol-success.svg", "物理事实验证对勾"),
        ("symbol-error.svg", "直觉误区否定红叉"),
        ("symbol-clock.svg", "超长运行时间时钟"),
        ("symbol-gauge.svg", "满载压力仪表盘")
    ]

    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <style>
      .font-title { font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 800; }
      .font-body { font-family: system-ui, -apple-system, 'PingFang SC', sans-serif; font-weight: 600; }
      .font-mono { font-family: 'SF Mono', monospace; font-weight: 600; }
    </style>
    <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0B1321"/>
      <stop offset="100%" stop-color="#14233C"/>
    </linearGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#bg)"/>

  <g transform="translate(80, 45)">
    <text x="0" y="36" fill="#FFFFFF" class="font-title" font-size="32">HVAC 工程道具与通用科学图例组件库 (Props &amp; Icons Contact Sheet)</text>
    <text x="0" y="70" fill="#8FA6CB" class="font-body" font-size="16">高精度矢量标准件 · 统一 2.5px/3.5px 描边与母品牌语义色标</text>
  </g>

  <!-- Grid: 7 columns x 3 rows -->
  <g transform="translate(80, 140)">
"""
    for idx, (p_file, p_title) in enumerate(props_list):
        col = idx % 7
        row = idx // 7
        x = col * 250
        y = row * 290

        svg += f"""
    <!-- Prop {idx}: {p_file} -->
    <g transform="translate({x}, {y})">
      <rect x="0" y="0" width="235" height="265" rx="14" fill="#101C31" stroke="#1F5CFF" stroke-width="1.5"/>
      <rect x="15" y="15" width="205" height="175" rx="10" fill="#F4F6F9"/>
      <g transform="translate(20, 20) scale(0.38)">
        <use href="#prop_{idx}"/>
      </g>
      <rect x="15" y="200" width="205" height="50" rx="8" fill="#172A46"/>
      <text x="117" y="222" fill="#1FD6E2" class="font-body" font-size="12" text-anchor="middle">{p_title}</text>
      <text x="117" y="240" fill="#8FA6CB" class="font-mono" font-size="10" text-anchor="middle">{p_file}</text>
    </g>
"""

    svg += """
  </g>
  <defs>
"""
    for idx, (p_file, _) in enumerate(props_list):
        fpath = (HVAC_PROPS if p_file.startswith("hvac-") else SHARED_SYMBOLS) / p_file
        with open(fpath, "r") as f:
            content = f.read().split("<svg")[1].split(">", 1)[1].rsplit("</svg>", 1)[0]
            svg += f'<g id="prop_{idx}">{content}</g>\n'

    svg += """
  </defs>
</svg>
"""
    with open(PREVIEWS_DIR / "contact_sheet_props.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    generate_props_contact_sheet()
    print("Props contact sheet created.")

if __name__ == "__main__":
    main()
