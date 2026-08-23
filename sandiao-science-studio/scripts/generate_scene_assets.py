#!/usr/bin/env python3
"""
Generator script for Scene and Background assets:
5 Scene Types:
1. daily-living (Living room / everyday misconception)
2. science-lab (Observatory science lab / whiteboard deduction)
3. plant-room (Equipment room / chiller / compressor loops)
4. abstract-stage (Modular telemetry stage / formulas / flowcharts)
5. summary-stage (Outro / conclusion desk / 3 actionable tips)

Each scene generates:
- background_16x9.svg
- midground_16x9.svg
- foreground_16x9.svg
- scene_16x9.svg (Full composite)
- scene_9x16.svg (Vertical 3-tier mobile composite)
- scene_night_16x9.svg (Night/Dark telemetry variant)
"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = PROJECT_DIR / "design" / "assets"


def scene_dir(scene: str) -> Path:
    if scene == "plant-room":
        return ASSETS_DIR / "domains" / "hvac" / "backgrounds" / scene
    if scene == "daily-living":
        return ASSETS_DIR / "shared" / "backgrounds" / scene
    return ASSETS_DIR / "brand" / "backgrounds" / scene

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. Daily Living Scene (Living Room)
# -------------------------------------------------------------
def generate_daily_living():
    s_dir = scene_dir("daily-living")
    ensure_dir(s_dir)

    # Layer 1: Background (Wall, Window, Sunlight)
    bg_16x9 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Daily Living: Background Layer -->
  <rect width="1920" height="1080" fill="#F4EDE2"/>
  <!-- Wall subtle panel lines -->
  <line x1="0" y1="200" x2="1920" y2="200" stroke="#E5DAC9" stroke-width="1.5"/>
  <line x1="0" y1="750" x2="1920" y2="750" stroke="#E5DAC9" stroke-width="2"/>
  <!-- Window on Left Wall -->
  <g transform="translate(100, 160)">
    <rect x="0" y="0" width="280" height="420" rx="16" fill="#BAE7FF" stroke="#13223A" stroke-width="3.5"/>
    <line x1="140" y1="0" x2="140" y2="420" stroke="#13223A" stroke-width="3"/>
    <line x1="0" y1="210" x2="280" y2="210" stroke="#13223A" stroke-width="3"/>
    <!-- Sunlight rays -->
    <polygon points="40,0 240,0 280,420 0,420" fill="#FFE58F" opacity="0.25"/>
    <!-- Wall shadow under window -->
    <rect x="-10" y="420" width="300" height="16" rx="4" fill="#D9C9B3"/>
  </g>
  <!-- Floor Wooden Planks -->
  <rect x="0" y="750" width="1920" height="330" fill="#D4B185"/>
  <line x1="0" y1="840" x2="1920" y2="840" stroke="#B89363" stroke-width="2"/>
  <line x1="0" y1="940" x2="1920" y2="940" stroke="#B89363" stroke-width="2"/>
  <line x1="0" y1="1040" x2="1920" y2="1040" stroke="#B89363" stroke-width="2"/>
</svg>"""

    # Layer 2: Midground (Air Conditioner Indoor Unit, Bookshelf, Plant)
    mg_16x9 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Daily Living: Midground Layer -->
  <!-- Indoor AC Unit mounted high on right -->
  <g transform="translate(1420, 120)">
    <rect x="0" y="0" width="380" height="140" rx="18" fill="#FFFFFF" stroke="#13223A" stroke-width="3.5"/>
    <!-- Louver air flap -->
    <rect x="20" y="100" width="340" height="24" rx="6" fill="#F0F5FF" stroke="#13223A" stroke-width="2"/>
    <!-- LED temperature display (16C) -->
    <rect x="300" y="30" width="56" height="32" rx="6" fill="#101C31"/>
    <text x="328" y="53" fill="#1FD6E2" font-family="'SF Mono', monospace" font-size="16" font-weight="bold" text-anchor="middle">16℃</text>
  </g>
  <!-- Modern Bookshelf on far left -->
  <g transform="translate(60, 600)">
    <rect x="0" y="0" width="160" height="240" rx="10" fill="#874D00" stroke="#13223A" stroke-width="3"/>
    <rect x="15" y="20" width="30" height="80" rx="4" fill="#1890FF"/>
    <rect x="50" y="20" width="24" height="80" rx="4" fill="#FA541C"/>
    <rect x="80" y="35" width="28" height="65" rx="4" fill="#52C41A"/>
  </g>
</svg>"""

    # Layer 3: Foreground (Coffee table trim, Character podium anchor)
    fg_16x9 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Daily Living: Foreground Layer -->
  <!-- Reserved Safe Zones: Left Char (x=80..380), Center Stage (x=420..1500), Right Char (x=1540..1840) -->
  <g id="fg_anchors">
    <!-- Baseboard floor trim -->
    <rect x="0" y="740" width="1920" height="14" fill="#874D00"/>
  </g>
</svg>"""

    # Full Composite 16:9
    scene_16x9 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Scene: Daily Living (16:9 Composite) -->
  <g id="layer_background">{bg_16x9.split('<svg')[1].split('>',1)[1].rsplit('</svg>',1)[0]}</g>
  <g id="layer_midground">{mg_16x9.split('<svg')[1].split('>',1)[1].rsplit('</svg>',1)[0]}</g>
  <g id="layer_foreground">{fg_16x9.split('<svg')[1].split('>',1)[1].rsplit('</svg>',1)[0]}</g>
</svg>"""

    # Full Composite 9:16 (Vertical)
    scene_9x16 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <!-- Scene: Daily Living (9:16 Vertical Composite) -->
  <!-- Wall -->
  <rect width="1080" height="1920" fill="#F4EDE2"/>
  <line x1="0" y1="380" x2="1080" y2="380" stroke="#E5DAC9" stroke-width="2"/>
  <!-- Top AC Unit -->
  <g transform="translate(350, 180)">
    <rect x="0" y="0" width="380" height="120" rx="16" fill="#FFFFFF" stroke="#13223A" stroke-width="3"/>
    <rect x="20" y="85" width="340" height="20" rx="5" fill="#F0F5FF" stroke="#13223A" stroke-width="2"/>
    <rect x="290" y="25" width="60" height="30" rx="6" fill="#101C31"/>
    <text x="320" y="47" fill="#1FD6E2" font-family="'SF Mono', monospace" font-size="16" font-weight="bold" text-anchor="middle">16℃</text>
  </g>
  <!-- Window on top left -->
  <g transform="translate(60, 200)">
    <rect x="0" y="0" width="200" height="300" rx="12" fill="#BAE7FF" stroke="#13223A" stroke-width="3"/>
    <line x1="100" y1="0" x2="100" y2="300" stroke="#13223A" stroke-width="2.5"/>
    <line x1="0" y1="150" x2="200" y2="150" stroke="#13223A" stroke-width="2.5"/>
  </g>
  <!-- Floor -->
  <rect x="0" y="1400" width="1080" height="520" fill="#D4B185"/>
  <line x1="0" y1="1400" x2="1080" y2="1400" stroke="#874D00" stroke-width="8"/>
</svg>"""

    # Night Variant 16:9
    scene_night_16x9 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Scene: Daily Living (Night Variant) -->
  <rect width="1920" height="1080" fill="#1A2233"/>
  <g transform="translate(100, 160)">
    <!-- Night Dark Window with Moon & Stars -->
    <rect x="0" y="0" width="280" height="420" rx="16" fill="#080E18" stroke="#1FD6E2" stroke-width="2"/>
    <circle cx="210" cy="80" r="28" fill="#FFFBE6"/>
    <circle cx="80" cy="140" r="2" fill="#FFFFFF"/>
    <circle cx="120" cy="90" r="3" fill="#1FD6E2"/>
    <line x1="140" y1="0" x2="140" y2="420" stroke="#101C31" stroke-width="3"/>
    <line x1="0" y1="210" x2="280" y2="210" stroke="#101C31" stroke-width="3"/>
  </g>
  <!-- Indoor Night Light AC Unit -->
  <g transform="translate(1420, 120)">
    <rect x="0" y="0" width="380" height="140" rx="18" fill="#243048" stroke="#1FD6E2" stroke-width="2"/>
    <rect x="20" y="100" width="340" height="24" rx="6" fill="#172238" stroke="#1FD6E2" stroke-width="1.5"/>
    <rect x="300" y="30" width="56" height="32" rx="6" fill="#080E18"/>
    <text x="328" y="53" fill="#1FD6E2" font-family="'SF Mono', monospace" font-size="16" font-weight="bold" text-anchor="middle">16℃</text>
  </g>
  <rect x="0" y="750" width="1920" height="330" fill="#3D3024"/>
</svg>"""

    with open(s_dir / "background_16x9.svg", "w") as f: f.write(bg_16x9)
    with open(s_dir / "midground_16x9.svg", "w") as f: f.write(mg_16x9)
    with open(s_dir / "foreground_16x9.svg", "w") as f: f.write(fg_16x9)
    with open(s_dir / "scene_16x9.svg", "w") as f: f.write(scene_16x9)
    with open(s_dir / "scene_9x16.svg", "w") as f: f.write(scene_9x16)
    with open(s_dir / "scene_night_16x9.svg", "w") as f: f.write(scene_night_16x9)

# -------------------------------------------------------------
# 2. Science Lab Scene (Observatory Laboratory)
# -------------------------------------------------------------
def generate_science_lab():
    s_dir = scene_dir("science-lab")
    ensure_dir(s_dir)

    scene_16x9 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Science Lab: Observatory Research Stage -->
  <defs>
    <linearGradient id="labBg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0E1726"/>
      <stop offset="60%" stop-color="#142136"/>
      <stop offset="100%" stop-color="#1A2C49"/>
    </linearGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#labBg)"/>
  <!-- Telemetry Grid & Modular Server Racks -->
  <g opacity="0.2">
    <line x1="0" y1="120" x2="1920" y2="120" stroke="#1FD6E2" stroke-width="1.5"/>
    <line x1="0" y1="840" x2="1920" y2="840" stroke="#1FD6E2" stroke-width="1.5"/>
    <line x1="80" y1="0" x2="80" y2="1080" stroke="#1FD6E2" stroke-width="1.5"/>
    <line x1="1840" y1="0" x2="1840" y2="1080" stroke="#1FD6E2" stroke-width="1.5"/>
  </g>
  <!-- Left Telemetry Sensor Column -->
  <g transform="translate(80, 200)">
    <rect x="0" y="0" width="140" height="580" rx="14" fill="#101C31" stroke="#1F5CFF" stroke-width="2"/>
    <circle cx="70" cy="40" r="16" fill="#1FD6E2" opacity="0.3"/>
    <circle cx="70" cy="40" r="8" fill="#1FD6E2"/>
    <line x1="20" y1="80" x2="120" y2="80" stroke="#1F5CFF" stroke-width="2"/>
    <rect x="20" y="100" width="100" height="30" rx="6" fill="#172A46"/>
    <text x="70" y="121" fill="#1FD6E2" font-family="'SF Mono', monospace" font-size="14" text-anchor="middle">SENS-01</text>
  </g>
  <!-- Right Telemetry Sensor Column -->
  <g transform="translate(1700, 200)">
    <rect x="0" y="0" width="140" height="580" rx="14" fill="#101C31" stroke="#1F5CFF" stroke-width="2"/>
    <circle cx="70" cy="40" r="16" fill="#FA541C" opacity="0.3"/>
    <circle cx="70" cy="40" r="8" fill="#FA541C"/>
    <line x1="20" y1="80" x2="120" y2="80" stroke="#1F5CFF" stroke-width="2"/>
    <rect x="20" y="100" width="100" height="30" rx="6" fill="#172A46"/>
    <text x="70" y="121" fill="#FA541C" font-family="'SF Mono', monospace" font-size="14" text-anchor="middle">SENS-02</text>
  </g>
  <!-- Floor Lab Deck -->
  <rect x="0" y="840" width="1920" height="240" fill="#0A0F1A"/>
  <line x1="0" y1="840" x2="1920" y2="840" stroke="#1FD6E2" stroke-width="3"/>
</svg>"""

    scene_9x16 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <!-- Science Lab (9:16 Vertical Composite) -->
  <rect width="1080" height="1920" fill="#0E1726"/>
  <g opacity="0.2">
    <line x1="60" y1="0" x2="60" y2="1920" stroke="#1FD6E2" stroke-width="1.5"/>
    <line x1="1020" y1="0" x2="1020" y2="1920" stroke="#1FD6E2" stroke-width="1.5"/>
  </g>
  <!-- Top Lab Header -->
  <rect x="60" y="80" width="960" height="80" rx="16" fill="#101C31" stroke="#1F5CFF" stroke-width="2"/>
  <text x="120" y="130" fill="#FFFFFF" font-family="sans-serif" font-size="24" font-weight="bold">ASTEROID LAB / 物理机理推导舞台</text>
  <!-- Floor Lab Deck -->
  <rect x="0" y="1540" width="1080" height="380" fill="#0A0F1A"/>
  <line x1="0" y1="1540" x2="1080" y2="1540" stroke="#1FD6E2" stroke-width="3"/>
</svg>"""

    with open(s_dir / "scene_16x9.svg", "w") as f: f.write(scene_16x9)
    with open(s_dir / "scene_9x16.svg", "w") as f: f.write(scene_9x16)
    with open(s_dir / "background_16x9.svg", "w") as f: f.write(scene_16x9)
    with open(s_dir / "midground_16x9.svg", "w") as f: f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"/>')
    with open(s_dir / "foreground_16x9.svg", "w") as f: f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"/>')
    with open(s_dir / "scene_night_16x9.svg", "w") as f: f.write(scene_16x9)

# -------------------------------------------------------------
# 3. Plant Room Scene (HVAC Equipment Room)
# -------------------------------------------------------------
def generate_plant_room():
    s_dir = scene_dir("plant-room")
    ensure_dir(s_dir)

    scene_16x9 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Plant Room: HVAC Machine & Pipe System -->
  <rect width="1920" height="1080" fill="#151E2E"/>
  <!-- Industrial Concrete Wall & Girders -->
  <line x1="0" y1="180" x2="1920" y2="180" stroke="#2B3A52" stroke-width="6"/>
  <line x1="400" y1="0" x2="400" y2="820" stroke="#2B3A52" stroke-width="4"/>
  <line x1="1520" y1="0" x2="1520" y2="820" stroke="#2B3A52" stroke-width="4"/>
  <!-- Overhead Supply & Return Pipes -->
  <!-- Blue Chilled Water Supply Pipe -->
  <path d="M 0,80 L 1920,80" fill="none" stroke="#1890FF" stroke-width="28"/>
  <path d="M 0,80 L 1920,80" fill="none" stroke="#13223A" stroke-width="3"/>
  <text x="960" y="87" fill="#FFFFFF" font-family="'SF Mono', monospace" font-size="14" font-weight="bold" text-anchor="middle">CHW SUPPLY 7℃</text>
  <!-- Orange Hot Return Pipe -->
  <path d="M 0,130 L 1920,130" fill="none" stroke="#FA541C" stroke-width="28"/>
  <path d="M 0,130 L 1920,130" fill="none" stroke="#13223A" stroke-width="3"/>
  <text x="960" y="137" fill="#FFFFFF" font-family="'SF Mono', monospace" font-size="14" font-weight="bold" text-anchor="middle">CONDENSER RETURN 37℃</text>
  <!-- Floor Deck -->
  <rect x="0" y="820" width="1920" height="260" fill="#0C121D"/>
  <line x1="0" y1="820" x2="1920" y2="820" stroke="#FAAD14" stroke-width="4" stroke-dasharray="24 16"/>
</svg>"""

    scene_9x16 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <!-- Plant Room (9:16 Vertical Composite) -->
  <rect width="1080" height="1920" fill="#151E2E"/>
  <path d="M 0,120 L 1080,120" fill="none" stroke="#1890FF" stroke-width="32"/>
  <path d="M 0,180 L 1080,180" fill="none" stroke="#FA541C" stroke-width="32"/>
  <rect x="0" y="1520" width="1080" height="400" fill="#0C121D"/>
  <line x1="0" y1="1520" x2="1080" y2="1520" stroke="#FAAD14" stroke-width="6" stroke-dasharray="30 20"/>
</svg>"""

    with open(s_dir / "scene_16x9.svg", "w") as f: f.write(scene_16x9)
    with open(s_dir / "scene_9x16.svg", "w") as f: f.write(scene_9x16)
    with open(s_dir / "background_16x9.svg", "w") as f: f.write(scene_16x9)
    with open(s_dir / "midground_16x9.svg", "w") as f: f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"/>')
    with open(s_dir / "foreground_16x9.svg", "w") as f: f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"/>')
    with open(s_dir / "scene_night_16x9.svg", "w") as f: f.write(scene_16x9)

# -------------------------------------------------------------
# 4. Abstract Stage Scene (Formulas & Logic Flowcards)
# -------------------------------------------------------------
def generate_abstract_stage():
    s_dir = scene_dir("abstract-stage")
    ensure_dir(s_dir)

    scene_16x9 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Abstract Telemetry Stage -->
  <defs>
    <radialGradient id="abstractGlow" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#172B4D"/>
      <stop offset="100%" stop-color="#080E18"/>
    </radialGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#abstractGlow)"/>
  <!-- Concentric Telemetry Orbit Rings -->
  <g opacity="0.25">
    <circle cx="960" cy="460" r="300" fill="none" stroke="#1FD6E2" stroke-width="1.5" stroke-dasharray="8 6"/>
    <circle cx="960" cy="460" r="500" fill="none" stroke="#1F5CFF" stroke-width="1.5"/>
    <circle cx="960" cy="460" r="700" fill="none" stroke="#1FD6E2" stroke-width="1" stroke-dasharray="4 8"/>
    <line x1="960" y1="0" x2="960" y2="1080" stroke="#1FD6E2" stroke-width="1"/>
    <line x1="0" y1="460" x2="1920" y2="460" stroke="#1FD6E2" stroke-width="1"/>
  </g>
</svg>"""

    scene_9x16 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <!-- Abstract Stage (9:16 Vertical Composite) -->
  <rect width="1080" height="1920" fill="#080E18"/>
  <circle cx="540" cy="800" r="350" fill="none" stroke="#1FD6E2" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.3"/>
  <circle cx="540" cy="800" r="500" fill="none" stroke="#1F5CFF" stroke-width="1.5" opacity="0.3"/>
</svg>"""

    with open(s_dir / "scene_16x9.svg", "w") as f: f.write(scene_16x9)
    with open(s_dir / "scene_9x16.svg", "w") as f: f.write(scene_9x16)
    with open(s_dir / "background_16x9.svg", "w") as f: f.write(scene_16x9)
    with open(s_dir / "midground_16x9.svg", "w") as f: f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"/>')
    with open(s_dir / "foreground_16x9.svg", "w") as f: f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"/>')
    with open(s_dir / "scene_dark_16x9.svg", "w") as f: f.write(scene_16x9)

# -------------------------------------------------------------
# 5. Summary Stage Scene (Outro & Verdict Desk)
# -------------------------------------------------------------
def generate_summary_stage():
    s_dir = scene_dir("summary-stage")
    ensure_dir(s_dir)

    scene_16x9 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Summary & Verdict Stage -->
  <rect width="1920" height="1080" fill="#0B1321"/>
  <!-- Starfield & Asteroid Orbit Backdrop -->
  <g opacity="0.2">
    <ellipse cx="960" cy="200" rx="800" ry="300" fill="none" stroke="#1F5CFF" stroke-width="2" transform="rotate(-10 960 200)"/>
    <circle cx="300" cy="150" r="3" fill="#1FD6E2"/>
    <circle cx="1600" cy="180" r="3" fill="#1FD6E2"/>
    <circle cx="1400" cy="90" r="2" fill="#FFFFFF"/>
  </g>
  <!-- High-Tech Broadcast Desk -->
  <g transform="translate(260, 760)">
    <polygon points="100,0 1300,0 1400,160 0,160" fill="#101C31" stroke="#1FD6E2" stroke-width="2.5"/>
    <line x1="200" y1="40" x2="1200" y2="40" stroke="#1F5CFF" stroke-width="3"/>
    <rect x="620" y="60" width="160" height="40" rx="8" fill="#172A46"/>
    <text x="700" y="86" fill="#1FD6E2" font-family="'SF Mono', monospace" font-size="16" font-weight="bold" text-anchor="middle">CONCLUSION DESK</text>
  </g>
  <rect x="0" y="920" width="1920" height="160" fill="#060A12"/>
</svg>"""

    scene_9x16 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <!-- Summary Stage (9:16 Vertical Composite) -->
  <rect width="1080" height="1920" fill="#0B1321"/>
  <ellipse cx="540" cy="300" rx="450" ry="200" fill="none" stroke="#1F5CFF" stroke-width="2" opacity="0.3"/>
  <polygon points="60,1480 1020,1480 1080,1680 0,1680" fill="#101C31" stroke="#1FD6E2" stroke-width="2.5"/>
  <rect x="0" y="1680" width="1080" height="240" fill="#060A12"/>
</svg>"""

    with open(s_dir / "scene_16x9.svg", "w") as f: f.write(scene_16x9)
    with open(s_dir / "scene_9x16.svg", "w") as f: f.write(scene_9x16)
    with open(s_dir / "background_16x9.svg", "w") as f: f.write(scene_16x9)
    with open(s_dir / "midground_16x9.svg", "w") as f: f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"/>')
    with open(s_dir / "foreground_16x9.svg", "w") as f: f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"/>')
    with open(s_dir / "scene_night_16x9.svg", "w") as f: f.write(scene_16x9)

def main():
    generate_daily_living()
    generate_science_lab()
    generate_plant_room()
    generate_abstract_stage()
    generate_summary_stage()
    print("All 5 scene categories generated by brand/shared/domain package in:", ASSETS_DIR)

if __name__ == "__main__":
    main()
