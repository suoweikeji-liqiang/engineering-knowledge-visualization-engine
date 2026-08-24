#!/usr/bin/env python3
"""
Generator for Engineering Props and Diagram Components:
- HVAC Hardware Props (AC units, compressor, coils, fan, valves, sensors)
- Universal Scientific Icons (water, air, heat, cold, electricity, clock, warning)
- Reusable Diagram Containers & Visualizations (comparison card, tips card, line chart, bar chart, gauges, formula card)
"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
HVAC_PROPS = PROJECT_DIR / "design" / "assets" / "domains" / "hvac" / "props"
SHARED_SYMBOLS = PROJECT_DIR / "design" / "assets" / "shared" / "symbols"
BASE_DIAGRAMS = PROJECT_DIR / "design" / "assets" / "shared" / "diagrams"

HVAC_PROPS.mkdir(parents=True, exist_ok=True)
SHARED_SYMBOLS.mkdir(parents=True, exist_ok=True)
BASE_DIAGRAMS.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. Engineering & HVAC Props
# -------------------------------------------------------------

def generate_props():
    props = {}

    props["hvac-ac-indoor.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 256" width="512" height="256">
  <!-- Indoor AC Unit -->
  <g id="hvac-ac-indoor">
    <rect x="16" y="24" width="480" height="180" rx="24" fill="#FFFFFF" stroke="#13223A" stroke-width="4"/>
    <rect x="36" y="140" width="440" height="36" rx="8" fill="#F0F5FF" stroke="#13223A" stroke-width="2.5"/>
    <!-- Digital Temp Display -->
    <rect x="390" y="44" width="76" height="40" rx="8" fill="#101C31"/>
    <text x="428" y="71" fill="#1FD6E2" font-family="'SF Mono', monospace" font-size="20" font-weight="bold" text-anchor="middle">16℃</text>
    <!-- Brand Asteroid Mark -->
    <circle cx="60" cy="64" r="10" fill="#1F5CFF"/>
    <ellipse cx="60" cy="64" rx="16" ry="6" fill="none" stroke="#1FD6E2" stroke-width="2" transform="rotate(-20 60 64)"/>
  </g>
</svg>"""

    props["hvac-ac-outdoor.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 384" width="512" height="384">
  <!-- Outdoor Condenser Unit -->
  <g id="hvac-ac-outdoor">
    <rect x="24" y="24" width="464" height="336" rx="28" fill="#E6EEF8" stroke="#13223A" stroke-width="4"/>
    <!-- Fan Grille -->
    <circle cx="180" cy="192" r="120" fill="#FFFFFF" stroke="#13223A" stroke-width="3"/>
    <circle cx="180" cy="192" r="80" fill="none" stroke="#8FA6CB" stroke-width="2"/>
    <circle cx="180" cy="192" r="40" fill="none" stroke="#8FA6CB" stroke-width="2"/>
    <!-- Fan Blades -->
    <circle cx="180" cy="192" r="24" fill="#101C31"/>
    <path d="M 180,168 Q 230,130 240,160 Z" fill="#172A46"/>
    <path d="M 180,216 Q 130,254 120,224 Z" fill="#172A46"/>
    <path d="M 204,192 Q 242,242 212,252 Z" fill="#172A46"/>
    <path d="M 156,192 Q 118,142 148,132 Z" fill="#172A46"/>
    <!-- Service Valve Compartment -->
    <rect x="340" y="60" width="110" height="264" rx="14" fill="#D0DEEE" stroke="#13223A" stroke-width="2.5"/>
    <circle cx="395" cy="120" r="16" fill="#FA541C" stroke="#13223A" stroke-width="2"/>
    <circle cx="395" cy="220" r="16" fill="#1890FF" stroke="#13223A" stroke-width="2"/>
  </g>
</svg>"""

    props["hvac-compressor.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="384" height="512">
  <!-- Hermetic Compressor Section -->
  <g id="hvac-compressor">
    <!-- Shell -->
    <path d="M 64,120 C 64,40 320,40 320,120 L 320,380 C 320,460 64,460 64,380 Z" fill="#101C31" stroke="#13223A" stroke-width="4"/>
    <!-- Motor Chamber -->
    <rect x="96" y="160" width="192" height="180" rx="20" fill="#1F385C" stroke="#1FD6E2" stroke-width="2"/>
    <circle cx="192" cy="250" r="48" fill="#1FD6E2" opacity="0.25"/>
    <circle cx="192" cy="250" r="28" fill="#1FD6E2" stroke="#FFFFFF" stroke-width="2"/>
    <!-- Suction & Discharge Ports -->
    <rect x="24" y="160" width="40" height="24" rx="4" fill="#1890FF"/>
    <rect x="320" y="120" width="40" height="24" rx="4" fill="#FA541C"/>
    <!-- Rating Badge -->
    <rect x="110" y="380" width="164" height="32" rx="8" fill="#000000" opacity="0.7"/>
    <text x="192" y="402" fill="#1FD6E2" font-family="'SF Mono', monospace" font-size="14" font-weight="bold" text-anchor="middle">RATED 100%</text>
  </g>
</svg>"""

    props["hvac-heat-exchanger.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="384" height="512">
  <!-- Evaporator S-Coils -->
  <g id="hvac-heat-exchanger">
    <rect x="24" y="24" width="336" height="464" rx="24" fill="#FFFFFF" stroke="#13223A" stroke-width="3.5"/>
    <!-- Fins Background -->
    <g opacity="0.25">
      <line x1="60" y1="60" x2="324" y2="60" stroke="#8FA6CB" stroke-width="2"/>
      <line x1="60" y1="100" x2="324" y2="100" stroke="#8FA6CB" stroke-width="2"/>
      <line x1="60" y1="140" x2="324" y2="140" stroke="#8FA6CB" stroke-width="2"/>
      <line x1="60" y1="180" x2="324" y2="180" stroke="#8FA6CB" stroke-width="2"/>
      <line x1="60" y1="220" x2="324" y2="220" stroke="#8FA6CB" stroke-width="2"/>
      <line x1="60" y1="260" x2="324" y2="260" stroke="#8FA6CB" stroke-width="2"/>
      <line x1="60" y1="300" x2="324" y2="300" stroke="#8FA6CB" stroke-width="2"/>
      <line x1="60" y1="340" x2="324" y2="340" stroke="#8FA6CB" stroke-width="2"/>
      <line x1="60" y1="380" x2="324" y2="380" stroke="#8FA6CB" stroke-width="2"/>
      <line x1="60" y1="420" x2="324" y2="420" stroke="#8FA6CB" stroke-width="2"/>
    </g>
    <!-- Copper Continuous S-Pipe -->
    <path d="M 80,80 L 300,80 A 30,30 0 0,1 300,140 L 80,140 A 30,30 0 0,0 80,200 L 300,200 A 30,30 0 0,1 300,260 L 80,260 A 30,30 0 0,0 80,320 L 300,320 A 30,30 0 0,1 300,380 L 80,380 A 30,30 0 0,0 80,440 L 300,440" fill="none" stroke="#1890FF" stroke-width="16" stroke-linecap="round"/>
    <path d="M 80,80 L 300,80 A 30,30 0 0,1 300,140 L 80,140 A 30,30 0 0,0 80,200 L 300,200 A 30,30 0 0,1 300,260 L 80,260 A 30,30 0 0,0 80,320 L 300,320 A 30,30 0 0,1 300,380 L 80,380 A 30,30 0 0,0 80,440 L 300,440" fill="none" stroke="#13223A" stroke-width="2.5"/>
  </g>
</svg>"""

    props["hvac-fan.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <g id="hvac-fan">
    <circle cx="128" cy="128" r="110" fill="#E6F7FF" stroke="#13223A" stroke-width="4"/>
    <circle cx="128" cy="128" r="28" fill="#101C31"/>
    <!-- 4 Curved Fan Blades -->
    <path d="M 128,100 C 128,40 170,40 180,70 C 190,100 150,110 128,100 Z" fill="#1890FF"/>
    <path d="M 156,128 C 216,128 216,170 186,180 C 156,190 146,150 156,128 Z" fill="#1890FF"/>
    <path d="M 128,156 C 128,216 86,216 76,186 C 66,156 106,146 128,156 Z" fill="#1890FF"/>
    <path d="M 100,128 C 40,128 40,86 70,76 C 100,66 110,106 100,128 Z" fill="#1890FF"/>
  </g>
</svg>"""

    props["hvac-pipes.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 128" width="512" height="128">
  <g id="hvac-pipes">
    <rect x="0" y="32" width="512" height="64" rx="12" fill="#BAE7FF" stroke="#13223A" stroke-width="3.5"/>
    <path d="M 60,64 L 140,64 M 220,64 L 300,64 M 380,64 L 460,64" stroke="#1890FF" stroke-width="8" stroke-linecap="round"/>
    <polygon points="140,54 165,64 140,74" fill="#1890FF"/>
    <polygon points="300,54 325,64 300,74" fill="#1890FF"/>
    <polygon points="460,54 485,64 460,74" fill="#1890FF"/>
  </g>
</svg>"""

    props["hvac-expansion-valve.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <g id="hvac-expansion-valve">
    <polygon points="32,64 128,128 32,192" fill="#FA541C" stroke="#13223A" stroke-width="3"/>
    <polygon points="224,64 128,128 224,192" fill="#1890FF" stroke="#13223A" stroke-width="3"/>
    <line x1="128" y1="40" x2="128" y2="128" stroke="#13223A" stroke-width="4"/>
    <ellipse cx="128" cy="40" rx="36" ry="16" fill="#FAAD14" stroke="#13223A" stroke-width="2.5"/>
  </g>
</svg>"""

    props["hvac-sensor-temp.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 256" width="128" height="256">
  <g id="hvac-sensor-temp">
    <rect x="48" y="16" width="32" height="150" rx="6" fill="#8C8C8C" stroke="#13223A" stroke-width="2"/>
    <circle cx="64" cy="180" r="28" fill="#FA541C" stroke="#13223A" stroke-width="3"/>
    <rect x="58" y="40" width="12" height="120" rx="4" fill="#FA541C"/>
    <text x="64" y="240" fill="#13223A" font-family="'SF Mono', monospace" font-size="14" font-weight="bold" text-anchor="middle">℃ SENSOR</text>
  </g>
</svg>"""

    props["hvac-sensor-pressure.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <g id="hvac-sensor-pressure">
    <circle cx="128" cy="110" r="80" fill="#FFFFFF" stroke="#13223A" stroke-width="4"/>
    <circle cx="128" cy="110" r="10" fill="#101C31"/>
    <line x1="128" y1="110" x2="170" y2="70" stroke="#F04B2F" stroke-width="4" stroke-linecap="round"/>
    <rect x="112" y="190" width="32" height="50" rx="4" fill="#8C8C8C" stroke="#13223A" stroke-width="2.5"/>
    <text x="128" y="150" fill="#13223A" font-family="'SF Mono', monospace" font-size="16" font-weight="bold" text-anchor="middle">MPa</text>
  </g>
</svg>"""

    props["hvac-thermometer.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 384" width="128" height="384">
  <g id="hvac-thermometer">
    <rect x="36" y="20" width="56" height="280" rx="28" fill="#F4F6F9" stroke="#13223A" stroke-width="3.5"/>
    <circle cx="64" cy="320" r="38" fill="#FA541C" stroke="#13223A" stroke-width="3.5"/>
    <rect x="52" y="100" width="24" height="200" rx="8" fill="#FA541C"/>
    <!-- Scale ticks -->
    <line x1="78" y1="60" x2="88" y2="60" stroke="#13223A" stroke-width="2"/>
    <line x1="78" y1="100" x2="92" y2="100" stroke="#13223A" stroke-width="2.5"/>
    <line x1="78" y1="140" x2="88" y2="140" stroke="#13223A" stroke-width="2"/>
    <line x1="78" y1="180" x2="92" y2="180" stroke="#13223A" stroke-width="2.5"/>
    <line x1="78" y1="220" x2="88" y2="220" stroke="#13223A" stroke-width="2"/>
    <line x1="78" y1="260" x2="92" y2="260" stroke="#13223A" stroke-width="2.5"/>
  </g>
</svg>"""

    props["hvac-electric-meter.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 320" width="256" height="320">
  <g id="hvac-electric-meter">
    <rect x="20" y="20" width="216" height="280" rx="20" fill="#FFFFFF" stroke="#13223A" stroke-width="3.5"/>
    <!-- LCD Meter Screen -->
    <rect x="40" y="50" width="176" height="70" rx="8" fill="#101C31"/>
    <text x="128" y="95" fill="#52C41A" font-family="'SF Mono', monospace" font-size="24" font-weight="bold" text-anchor="middle">0342.8 kWh</text>
    <circle cx="60" cy="180" r="16" fill="#1FD6E2"/>
    <circle cx="128" cy="180" r="16" fill="#FAAD14"/>
    <circle cx="196" cy="180" r="16" fill="#FA541C"/>
    <text x="128" y="260" fill="#13223A" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle">ENERGY METER</text>
  </g>
</svg>"""

    # Scientific Symbols
    props["symbol-water-drop.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <path d="M 64,16 C 64,16 24,64 24,88 C 24,110 42,120 64,120 C 86,120 104,110 104,88 C 104,64 64,16 64,16 Z" fill="#1890FF" stroke="#13223A" stroke-width="3"/>
</svg>"""

    props["symbol-airflow.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <path d="M 16,40 L 80,40 C 95,40 104,30 96,16" fill="none" stroke="#1FD6E2" stroke-width="6" stroke-linecap="round"/>
  <path d="M 16,64 L 96,64 C 112,64 120,76 110,90" fill="none" stroke="#1FD6E2" stroke-width="6" stroke-linecap="round"/>
  <path d="M 16,88 L 60,88 C 75,88 84,100 76,112" fill="none" stroke="#1FD6E2" stroke-width="6" stroke-linecap="round"/>
</svg>"""

    props["symbol-heat-flow.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <g transform="translate(64,64) rotate(-45)">
    <path d="M -30,-40 C -10,-20 -50,0 -30,20 C -10,40 -50,60 -30,80" fill="none" stroke="#FA541C" stroke-width="6" stroke-linecap="round"/>
    <path d="M 0,-40 C 20,-20 -20,0 0,20 C 20,40 -20,60 0,80" fill="none" stroke="#F04B2F" stroke-width="6" stroke-linecap="round"/>
    <path d="M 30,-40 C 50,-20 10,0 30,20 C 50,40 10,60 30,80" fill="none" stroke="#FAAD14" stroke-width="6" stroke-linecap="round"/>
  </g>
</svg>"""

    props["symbol-cold-flow.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <g transform="translate(64,64)">
    <line x1="0" y1="-48" x2="0" y2="48" stroke="#1FD6E2" stroke-width="5" stroke-linecap="round"/>
    <line x1="-48" y1="0" x2="48" y2="0" stroke="#1FD6E2" stroke-width="5" stroke-linecap="round"/>
    <line x1="-34" y1="-34" x2="34" y2="34" stroke="#1FD6E2" stroke-width="4" stroke-linecap="round"/>
    <line x1="34" y1="-34" x2="-34" y2="34" stroke="#1FD6E2" stroke-width="4" stroke-linecap="round"/>
  </g>
</svg>"""

    props["symbol-electricity.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <polygon points="72,12 24,70 60,70 48,116 104,56 68,56" fill="#FADB14" stroke="#D48806" stroke-width="3"/>
</svg>"""

    props["symbol-warning.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <polygon points="64,16 116,108 12,108" fill="#FAAD14" stroke="#13223A" stroke-width="3.5"/>
  <line x1="64" y1="46" x2="64" y2="76" stroke="#13223A" stroke-width="6" stroke-linecap="round"/>
  <circle cx="64" cy="94" r="4.5" fill="#13223A"/>
</svg>"""

    props["symbol-success.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <circle cx="64" cy="64" r="52" fill="#52C41A" stroke="#13223A" stroke-width="3"/>
  <path d="M 38,64 L 56,82 L 90,44" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

    props["symbol-error.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <circle cx="64" cy="64" r="52" fill="#F5222D" stroke="#13223A" stroke-width="3"/>
  <path d="M 42,42 L 86,86 M 86,42 L 42,86" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
</svg>"""

    props["symbol-clock.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <circle cx="64" cy="64" r="52" fill="#FFFFFF" stroke="#13223A" stroke-width="3.5"/>
  <line x1="64" y1="64" x2="64" y2="32" stroke="#13223A" stroke-width="4" stroke-linecap="round"/>
  <line x1="64" y1="64" x2="88" y2="64" stroke="#FA541C" stroke-width="4" stroke-linecap="round"/>
  <circle cx="64" cy="64" r="5" fill="#101C31"/>
</svg>"""

    props["symbol-gauge.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <path d="M 20,96 A 52,52 0 1,1 108,96" fill="none" stroke="#13223A" stroke-width="6"/>
  <line x1="64" y1="64" x2="90" y2="40" stroke="#F04B2F" stroke-width="4" stroke-linecap="round"/>
  <circle cx="64" cy="64" r="7" fill="#13223A"/>
</svg>"""

    for name, content in props.items():
        directory = HVAC_PROPS if name.startswith("hvac-") else SHARED_SYMBOLS
        with open(directory / name, "w", encoding="utf-8") as f:
            f.write(content.strip())

# -------------------------------------------------------------
# 2. Diagram Components & Card Widgets
# -------------------------------------------------------------

def generate_diagrams():
    diagrams = {}

    diagrams["diagram-comparison-card.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="1000" height="600">
  <!-- Runtime component: inject all labels and content in the renderer. -->
  <g id="diagram-comparison-card">
    <rect id="card-frame" width="1000" height="600" rx="24" fill="#FFFFFF" stroke="#13223A" stroke-width="3.5"/>
    <g id="left-panel">
      <rect x="36" y="36" width="440" height="528" rx="16" fill="#FFF5F5" stroke="#FFA39E" stroke-width="2"/>
      <rect id="left-badge-slot" x="56" y="56" width="100" height="28" rx="6" fill="#F04B2F"/>
      <rect id="left-title-slot" x="176" y="56" width="260" height="28" rx="6" fill="#FFE1DF"/>
      <rect id="left-content-slot" x="56" y="112" width="400" height="424" rx="12" fill="#FFFFFF" opacity="0.7"/>
    </g>
    <g id="right-panel">
      <rect x="524" y="36" width="440" height="528" rx="16" fill="#E6F9FB" stroke="#87E8DE" stroke-width="2"/>
      <rect id="right-badge-slot" x="544" y="56" width="100" height="28" rx="6" fill="#13C2C2"/>
      <rect id="right-title-slot" x="664" y="56" width="260" height="28" rx="6" fill="#B5F5EC"/>
      <rect id="right-content-slot" x="544" y="112" width="400" height="424" rx="12" fill="#FFFFFF" opacity="0.7"/>
    </g>
  </g>
</svg>"""

    diagrams["diagram-tips-card.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" width="960" height="520">
  <!-- Runtime component: slots stay content-free and addressable. -->
  <g id="diagram-tips-card">
    <rect id="card-frame" width="960" height="520" rx="24" fill="#FFFFFF" stroke="#13223A" stroke-width="3.5"/>
    <rect id="title-slot" x="48" y="28" width="600" height="36" rx="8" fill="#E6EEF8"/>
    <g id="tip-one">
      <rect x="48" y="88" width="864" height="110" rx="14" fill="#F6F8FA" stroke="#D9D9D9" stroke-width="1.5"/>
      <circle id="tip-one-index" cx="98" cy="143" r="24" fill="#1F5CFF"/>
      <rect id="tip-one-title-slot" x="144" y="116" width="560" height="24" rx="6" fill="#D6E4FF"/>
      <rect id="tip-one-body-slot" x="144" y="154" width="700" height="18" rx="5" fill="#E6EEF8"/>
    </g>
    <g id="tip-two">
      <rect x="48" y="222" width="864" height="110" rx="14" fill="#F6F8FA" stroke="#D9D9D9" stroke-width="1.5"/>
      <circle id="tip-two-index" cx="98" cy="277" r="24" fill="#1FD6E2"/>
      <rect id="tip-two-title-slot" x="144" y="250" width="560" height="24" rx="6" fill="#B5F5EC"/>
      <rect id="tip-two-body-slot" x="144" y="288" width="700" height="18" rx="5" fill="#E6EEF8"/>
    </g>
    <g id="tip-three">
      <rect x="48" y="356" width="864" height="110" rx="14" fill="#F6F8FA" stroke="#D9D9D9" stroke-width="1.5"/>
      <circle id="tip-three-index" cx="98" cy="411" r="24" fill="#52C41A"/>
      <rect id="tip-three-title-slot" x="144" y="384" width="560" height="24" rx="6" fill="#D9F7BE"/>
      <rect id="tip-three-body-slot" x="144" y="422" width="700" height="18" rx="5" fill="#E6EEF8"/>
    </g>
  </g>
</svg>"""

    diagrams["diagram-line-chart.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" width="960" height="480">
  <!-- Runtime chart frame: the renderer supplies labels, series and annotations. -->
  <g id="diagram-line-chart">
    <rect id="chart-frame" width="960" height="480" rx="20" fill="#FFFFFF" stroke="#13223A" stroke-width="3"/>
    <rect id="title-slot" x="40" y="24" width="520" height="28" rx="6" fill="#E6EEF8"/>
    <g id="plot-grid" opacity="0.45" stroke="#D0DEEE" stroke-width="1">
      <line x1="80" y1="160" x2="880" y2="160"/><line x1="80" y1="240" x2="880" y2="240"/>
      <line x1="80" y1="320" x2="880" y2="320"/><line x1="280" y1="80" x2="280" y2="400"/>
      <line x1="480" y1="80" x2="480" y2="400"/><line x1="680" y1="80" x2="680" y2="400"/>
    </g>
    <g id="axes" stroke="#13223A" stroke-width="2.5">
      <line x1="80" y1="400" x2="880" y2="400"/><line x1="80" y1="80" x2="80" y2="400"/>
    </g>
    <path id="primary-series" d="M 80,320 C 220,300 280,210 400,220 S 650,150 840,180" fill="none" stroke="#1F5CFF" stroke-width="4"/>
    <path id="secondary-series" d="M 80,350 C 220,340 320,280 440,300 S 680,240 840,260" fill="none" stroke="#FA541C" stroke-width="4" stroke-dasharray="10 7"/>
    <g id="annotation-layer"/>
    <g id="x-label-slot"/><g id="y-label-slot"/><g id="legend-slot"/>
  </g>
</svg>"""

    diagrams["diagram-flow-node.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <!-- Runtime node: ports and text slots are semantic, content is injected later. -->
  <g id="diagram-flow-node">
    <rect id="node-frame" width="320" height="180" rx="16" fill="#101C31" stroke="#1FD6E2" stroke-width="2.5"/>
    <circle id="state-indicator" cx="36" cy="36" r="12" fill="#1FD6E2"/>
    <rect id="title-slot" x="60" y="24" width="220" height="24" rx="6" fill="#1F385C"/>
    <line id="header-divider" x1="20" y1="64" x2="300" y2="64" stroke="#1F385C" stroke-width="1.5"/>
    <rect id="body-slot" x="24" y="84" width="272" height="56" rx="8" fill="#172A46"/>
    <rect id="status-slot" x="24" y="150" width="150" height="12" rx="4" fill="#1FD6E2" opacity="0.65"/>
    <circle id="input-port" cx="0" cy="112" r="8" fill="#1890FF"/>
    <circle id="output-port" cx="320" cy="112" r="8" fill="#FA541C"/>
  </g>
</svg>"""

    for name, content in diagrams.items():
        with open(BASE_DIAGRAMS / name, "w", encoding="utf-8") as f:
            f.write(content.strip())

def main():
    generate_props()
    generate_diagrams()
    print("Props and Diagram assets generated.")

if __name__ == "__main__":
    main()
