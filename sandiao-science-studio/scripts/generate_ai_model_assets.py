#!/usr/bin/env python3
"""Generate the domain.ai-models visual asset pack.

The SVGs intentionally avoid lesson-specific copy. Stable layer ids expose the
semantic parts that a renderer may animate, tint, or annotate at runtime.
"""

from __future__ import annotations

from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR / "design" / "assets" / "domains" / "ai-models"
COMPONENTS = ROOT / "components"
DIAGRAMS = ROOT / "diagrams"
BACKGROUNDS = ROOT / "backgrounds" / "model-observatory"

INK = "#13223A"
NAVY = "#101C31"
BLUE = "#1F5CFF"
CYAN = "#1FD6E2"
VIOLET = "#8B5CF6"
GREEN = "#22C55E"
AMBER = "#F59E0B"
CORAL = "#F04B2F"
PAPER = "#F6F8FC"
MUTED = "#8FA6CB"


def svg(body: str, *, view_box: str = "0 0 512 512", defs: str = "") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}">
  <defs>{defs}</defs>
{body}
</svg>\n'''


def arrow(x1: int, y1: int, x2: int, y2: int, color: str = CYAN, ident: str = "flow") -> str:
    tip = 14
    return f'''  <g id="{ident}">
    <path d="M{x1} {y1} L{x2 - tip} {y2}" fill="none" stroke="{color}" stroke-width="8" stroke-linecap="round"/>
    <path d="M{x2 - tip} {y2 - 10} L{x2} {y2} L{x2 - tip} {y2 + 10}" fill="none" stroke="{color}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  </g>'''


def node(x: int, y: int, color: str, ident: str, radius: int = 22) -> str:
    return f'''  <g id="{ident}">
    <circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" fill-opacity=".18" stroke="{color}" stroke-width="4"/>
    <circle cx="{x}" cy="{y}" r="7" fill="{color}"/>
  </g>'''


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def components() -> dict[str, str]:
    token = svg(f'''  <g id="ai-token">
    <rect id="token-shell" x="54" y="122" width="404" height="268" rx="54" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>
    <rect id="token-field" x="88" y="156" width="336" height="200" rx="34" fill="{CYAN}" fill-opacity=".12" stroke="{CYAN}" stroke-width="4" stroke-dasharray="12 10"/>
    <path id="token-mark" d="M202 202h108M256 202v108M218 310h76" fill="none" stroke="{BLUE}" stroke-width="18" stroke-linecap="round"/>
    <circle id="token-index" cx="414" cy="132" r="28" fill="{VIOLET}" stroke="#FFFFFF" stroke-width="6"/>
  </g>''')

    bars = "\n".join(
        f'    <rect id="dimension-{i + 1}" x="{74 + i * 46}" y="{316 - h}" width="26" height="{h}" rx="13" fill="{VIOLET if i % 2 else CYAN}" opacity="{0.58 + i * 0.04:.2f}"/>'
        for i, h in enumerate((90, 150, 62, 210, 118, 178, 74, 132))
    )
    embedding = svg(f'''  <g id="ai-embedding-vector">
    <rect x="30" y="76" width="452" height="360" rx="36" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>
    <path id="axis" d="M64 350H448" stroke="{MUTED}" stroke-width="4" stroke-linecap="round"/>
{bars}
    <path id="vector-flow" d="M74 382 C170 420 318 350 438 398" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round" stroke-dasharray="12 12"/>
  </g>''')

    connections = []
    for y1 in (126, 256, 386):
        for y2 in (106, 206, 306, 406):
            connections.append(f'    <path d="M134 {y1} L378 {y2}" stroke="{VIOLET}" stroke-opacity=".22" stroke-width="4"/>')
    neurons = [node(112, y, CYAN, f"input-{i + 1}", 18) for i, y in enumerate((126, 256, 386))]
    neurons += [node(400, y, VIOLET, f"output-{i + 1}", 18) for i, y in enumerate((106, 206, 306, 406))]
    neural = svg('''  <g id="ai-neural-layer">\n''' + "\n".join(connections + neurons) + '''
    <path id="layer-boundary" d="M256 54V458" stroke="#8FA6CB" stroke-width="3" stroke-dasharray="10 12"/>
  </g>''')

    attention = svg(f'''  <g id="ai-attention-head">
    <circle id="attention-ring" cx="256" cy="256" r="188" fill="{VIOLET}" fill-opacity=".08" stroke="{VIOLET}" stroke-width="7"/>
    <g id="query">{node(256, 118, CYAN, "query-node", 28)}</g>
    <g id="key-left">{node(138, 330, VIOLET, "key-left-node", 26)}</g>
    <g id="key-right">{node(374, 330, VIOLET, "key-right-node", 26)}</g>
    <path id="score-left" d="M242 144L154 304" stroke="{CYAN}" stroke-width="12" stroke-linecap="round" opacity=".9"/>
    <path id="score-right" d="M270 144L358 304" stroke="{CYAN}" stroke-width="5" stroke-linecap="round" opacity=".45"/>
    <path id="mix" d="M166 350 Q256 426 346 350" fill="none" stroke="{BLUE}" stroke-width="8" stroke-linecap="round"/>
  </g>''')

    transformer = svg(f'''  <g id="ai-transformer-block">
    <rect id="block-shell" x="70" y="36" width="372" height="440" rx="42" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>
    <rect id="attention-slot" x="106" y="82" width="300" height="112" rx="24" fill="{VIOLET}" fill-opacity=".15" stroke="{VIOLET}" stroke-width="4"/>
    <path id="residual-one" d="M118 216 C58 216 58 62 118 62" fill="none" stroke="{CYAN}" stroke-width="7" stroke-linecap="round"/>
    <rect id="normalization-slot" x="140" y="224" width="232" height="58" rx="18" fill="{BLUE}" fill-opacity=".14" stroke="{BLUE}" stroke-width="4"/>
    <rect id="feed-forward-slot" x="106" y="312" width="300" height="112" rx="24" fill="{CYAN}" fill-opacity=".14" stroke="{CYAN}" stroke-width="4"/>
    <path id="residual-two" d="M394 446 C454 446 454 292 394 292" fill="none" stroke="{VIOLET}" stroke-width="7" stroke-linecap="round"/>
    <circle id="merge-one" cx="256" cy="209" r="13" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>
    <circle id="merge-two" cx="256" cy="439" r="13" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>
  </g>''')

    model_core = svg(f'''  <g id="ai-model-core">
    <circle id="outer-orbit" cx="256" cy="256" r="206" fill="{NAVY}" stroke="{BLUE}" stroke-width="6"/>
    <ellipse id="orbit-one" cx="256" cy="256" rx="174" ry="76" fill="none" stroke="{CYAN}" stroke-width="5" transform="rotate(-24 256 256)"/>
    <ellipse id="orbit-two" cx="256" cy="256" rx="174" ry="76" fill="none" stroke="{VIOLET}" stroke-width="5" transform="rotate(42 256 256)"/>
    <circle id="parameter-field" cx="256" cy="256" r="104" fill="{VIOLET}" fill-opacity=".28" stroke="{VIOLET}" stroke-width="5"/>
    <path id="model-glyph" d="M196 278V224l60-34 60 34v68l-60 34-60-34zM256 190v136M196 224l120 68M316 224l-120 68" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>
    <circle id="active-parameter" cx="390" cy="126" r="18" fill="{CYAN}"/>
  </g>''')

    gpu = svg(f'''  <g id="ai-gpu-cluster">
    <rect id="rack" x="54" y="42" width="404" height="428" rx="32" fill="{NAVY}" stroke="{INK}" stroke-width="8"/>
    <g id="gpu-one"><rect x="88" y="82" width="336" height="94" rx="18" fill="#172A46" stroke="{BLUE}" stroke-width="4"/><circle cx="354" cy="129" r="27" fill="none" stroke="{CYAN}" stroke-width="5"/><path d="M354 102v54M327 129h54" stroke="{CYAN}" stroke-width="4"/></g>
    <g id="gpu-two"><rect x="88" y="210" width="336" height="94" rx="18" fill="#172A46" stroke="{VIOLET}" stroke-width="4"/><circle cx="354" cy="257" r="27" fill="none" stroke="{VIOLET}" stroke-width="5"/><path d="M354 230v54M327 257h54" stroke="{VIOLET}" stroke-width="4"/></g>
    <g id="gpu-three"><rect x="88" y="338" width="336" height="94" rx="18" fill="#172A46" stroke="{CYAN}" stroke-width="4"/><circle cx="354" cy="385" r="27" fill="none" stroke="{BLUE}" stroke-width="5"/><path d="M354 358v54M327 385h54" stroke="{BLUE}" stroke-width="4"/></g>
    <g id="compute-indicators"><circle cx="120" cy="129" r="9" fill="{GREEN}"/><circle cx="120" cy="257" r="9" fill="{GREEN}"/><circle cx="120" cy="385" r="9" fill="{AMBER}"/></g>
  </g>''')

    dataset = svg(f'''  <g id="ai-dataset-stack">
    <path id="sheet-back" d="M116 82h286v298H116z" fill="{MUTED}" fill-opacity=".22" stroke="{MUTED}" stroke-width="5" transform="translate(34 -28)"/>
    <path id="sheet-mid" d="M92 106h286v298H92z" fill="{BLUE}" fill-opacity=".12" stroke="{BLUE}" stroke-width="5" transform="translate(18 -12)"/>
    <rect id="sheet-front" x="68" y="118" width="304" height="310" rx="22" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>
    <g id="data-rows" stroke-linecap="round"><path d="M112 184h212" stroke="{CYAN}" stroke-width="14"/><path d="M112 242h156" stroke="{VIOLET}" stroke-width="14"/><path d="M112 300h226" stroke="{BLUE}" stroke-width="14"/><path d="M112 358h180" stroke="{CYAN}" stroke-width="14"/></g>
    <circle id="quality-badge" cx="382" cy="392" r="54" fill="{GREEN}" stroke="#FFFFFF" stroke-width="8"/><path d="M354 392l18 18 38-42" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  </g>''')

    vector_db = svg(f'''  <g id="ai-vector-database">
    <path id="database-shell" d="M78 126v260c0 52 356 52 356 0V126" fill="{GREEN}" fill-opacity=".10" stroke="{INK}" stroke-width="7"/>
    <ellipse id="database-top" cx="256" cy="126" rx="178" ry="70" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>
    <path id="database-band" d="M78 246c0 52 356 52 356 0M78 346c0 52 356 52 356 0" fill="none" stroke="{MUTED}" stroke-width="4"/>
    <g id="vector-points" fill="{GREEN}"><circle cx="174" cy="116" r="12"/><circle cx="240" cy="98" r="12"/><circle cx="302" cy="138" r="12"/><circle cx="346" cy="102" r="12"/></g>
    <path id="nearest-neighbor" d="M174 116l66-18 62 40 44-36" fill="none" stroke="{CYAN}" stroke-width="6" stroke-linecap="round"/>
  </g>''')

    tool = svg(f'''  <g id="ai-tool-connector">
    <path id="connector-line" d="M76 256h104M332 256h104" stroke="{GREEN}" stroke-width="20" stroke-linecap="round"/>
    <rect id="tool-port" x="170" y="170" width="172" height="172" rx="44" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>
    <path id="tool-gear" d="M256 206l14 20 24-4 5 25 22 11-12 22 12 22-22 11-5 25-24-4-14 20-14-20-24 4-5-25-22-11 12-22-12-22 22-11 5-25 24 4z" fill="{GREEN}" fill-opacity=".18" stroke="{GREEN}" stroke-width="5" stroke-linejoin="round"/>
    <circle id="tool-center" cx="256" cy="280" r="30" fill="{GREEN}"/>
  </g>''')

    return {
        "ai-token.svg": token,
        "ai-embedding-vector.svg": embedding,
        "ai-neural-layer.svg": neural,
        "ai-attention-head.svg": attention,
        "ai-transformer-block.svg": transformer,
        "ai-model-core.svg": model_core,
        "ai-gpu-cluster.svg": gpu,
        "ai-dataset-stack.svg": dataset,
        "ai-vector-database.svg": vector_db,
        "ai-tool-connector.svg": tool,
    }


def diagrams() -> dict[str, str]:
    def shell(inner: str, ident: str) -> str:
        return svg(f'''  <g id="{ident}">
    <rect id="canvas" x="18" y="42" width="988" height="492" rx="34" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>
{inner}
  </g>''', view_box="0 0 1024 576")

    training = shell(f'''    <g id="dataset-stage"><path d="M82 210h130v162H82z" fill="{CYAN}" fill-opacity=".13" stroke="{CYAN}" stroke-width="5"/><path d="M104 250h86M104 292h70M104 334h92" stroke="{CYAN}" stroke-width="10" stroke-linecap="round"/></g>
{arrow(222, 291, 336, 291, CYAN, "data-flow")}
    <g id="forward-stage"><rect x="348" y="180" width="166" height="222" rx="28" fill="{VIOLET}" fill-opacity=".13" stroke="{VIOLET}" stroke-width="5"/><path d="M384 242h94M384 292h94M384 342h94" stroke="{VIOLET}" stroke-width="11" stroke-linecap="round"/></g>
{arrow(526, 291, 640, 291, VIOLET, "prediction-flow")}
    <g id="loss-stage"><circle cx="708" cy="291" r="66" fill="{CORAL}" fill-opacity=".13" stroke="{CORAL}" stroke-width="5"/><path d="M678 270l60 42M738 270l-60 42" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/></g>
    <path id="backprop-flow" d="M708 214 C708 92 430 92 430 164" fill="none" stroke="{AMBER}" stroke-width="8" stroke-linecap="round" stroke-dasharray="14 12"/>
    <g id="optimizer-stage"><rect x="820" y="228" width="124" height="126" rx="28" fill="{BLUE}" fill-opacity=".12" stroke="{BLUE}" stroke-width="5"/><circle cx="882" cy="291" r="32" fill="none" stroke="{BLUE}" stroke-width="8"/><path d="M882 259v64M850 291h64" stroke="{BLUE}" stroke-width="6"/></g>''', "ai-training-pipeline")

    inference = shell(f'''    <g id="prompt-slot"><rect x="74" y="214" width="164" height="154" rx="28" fill="{CYAN}" fill-opacity=".12" stroke="{CYAN}" stroke-width="5"/><circle cx="122" cy="260" r="15" fill="{CYAN}"/><path d="M154 260h48M104 312h104" stroke="{CYAN}" stroke-width="10" stroke-linecap="round"/></g>
{arrow(250, 291, 354, 291, CYAN, "prompt-flow")}
    <g id="model-stage"><circle cx="480" cy="291" r="106" fill="{VIOLET}" fill-opacity=".14" stroke="{VIOLET}" stroke-width="6"/><path d="M430 310v-58l50-29 50 29v58l-50 29zM480 223v116" fill="none" stroke="{VIOLET}" stroke-width="8"/></g>
{arrow(598, 291, 702, 291, VIOLET, "generation-flow")}
    <g id="token-stream"><rect x="716" y="224" width="74" height="74" rx="18" fill="{BLUE}" fill-opacity=".16" stroke="{BLUE}" stroke-width="5"/><rect x="804" y="252" width="74" height="74" rx="18" fill="{CYAN}" fill-opacity=".16" stroke="{CYAN}" stroke-width="5"/><rect x="892" y="280" width="74" height="74" rx="18" fill="{GREEN}" fill-opacity=".16" stroke="{GREEN}" stroke-width="5"/></g>
    <path id="kv-cache" d="M390 422h180" stroke="{AMBER}" stroke-width="12" stroke-linecap="round" stroke-dasharray="18 12"/>''', "ai-inference-pipeline")

    grid = []
    for row in range(5):
        for col in range(6):
            opacity = max(.08, .92 - abs(row - (col * 0.62)) * .25)
            grid.append(f'    <rect id="attention-{row + 1}-{col + 1}" x="{328 + col * 72}" y="{100 + row * 72}" width="56" height="56" rx="12" fill="{VIOLET}" opacity="{opacity:.2f}"/>')
    attention_map = shell(f'''    <g id="query-tokens">{''.join(f'<rect x="92" y="{100+i*72}" width="174" height="56" rx="14" fill="{CYAN}" opacity="{.25+i*.10:.2f}"/>' for i in range(5))}</g>
    <g id="attention-grid">{''.join(grid)}</g>
    <path id="focus-vector" d="M266 272H760" stroke="{CORAL}" stroke-width="5" stroke-dasharray="12 10"/>
    <g id="head-selector"><circle cx="870" cy="188" r="42" fill="{BLUE}" fill-opacity=".16" stroke="{BLUE}" stroke-width="5"/><circle cx="870" cy="291" r="42" fill="{VIOLET}" stroke="{VIOLET}" stroke-width="5"/><circle cx="870" cy="394" r="42" fill="{CYAN}" fill-opacity=".16" stroke="{CYAN}" stroke-width="5"/></g>''', "ai-attention-map")

    rag = shell(f'''    <g id="question-stage">{node(116, 291, CYAN, "question-node", 46)}</g>
{arrow(174, 291, 286, 291, CYAN, "embedding-flow")}
    <g id="retrieval-stage"><path d="M302 226v130c0 36 176 36 176 0V226" fill="{GREEN}" fill-opacity=".12" stroke="{GREEN}" stroke-width="5"/><ellipse cx="390" cy="226" rx="88" ry="35" fill="#FFFFFF" stroke="{GREEN}" stroke-width="5"/><circle cx="360" cy="222" r="8" fill="{GREEN}"/><circle cx="398" cy="210" r="8" fill="{GREEN}"/><circle cx="425" cy="235" r="8" fill="{GREEN}"/></g>
{arrow(490, 291, 604, 291, GREEN, "context-flow")}
    <g id="context-stage"><path d="M620 210h136v162H620z" fill="{AMBER}" fill-opacity=".12" stroke="{AMBER}" stroke-width="5"/><path d="M648 252h80M648 292h62M648 332h86" stroke="{AMBER}" stroke-width="9" stroke-linecap="round"/></g>
{arrow(768, 291, 838, 291, AMBER, "grounded-flow")}
    <g id="answer-stage">{node(902, 291, VIOLET, "answer-node", 46)}</g>
    <path id="citation-link" d="M390 388 C520 486 698 462 688 384" fill="none" stroke="{GREEN}" stroke-width="6" stroke-dasharray="12 10"/>''', "ai-rag-pipeline")

    agent = shell(f'''    <g id="model-stage">{node(512, 160, VIOLET, "model-node", 62)}</g>
    <g id="plan-stage">{node(272, 291, BLUE, "plan-node", 54)}</g>
    <g id="tool-stage">{node(512, 420, GREEN, "tool-node", 54)}</g>
    <g id="observation-stage">{node(752, 291, CYAN, "observation-node", 54)}</g>
    <path id="plan-flow" d="M466 200L316 258" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/>
    <path id="action-flow" d="M310 330L468 398" stroke="{GREEN}" stroke-width="9" stroke-linecap="round"/>
    <path id="observation-flow" d="M556 398L714 330" stroke="{CYAN}" stroke-width="9" stroke-linecap="round"/>
    <path id="reasoning-flow" d="M708 252L558 198" stroke="{VIOLET}" stroke-width="9" stroke-linecap="round"/>
    <circle id="stop-condition" cx="512" cy="291" r="34" fill="{CORAL}" fill-opacity=".15" stroke="{CORAL}" stroke-width="5"/>''', "ai-agent-loop")

    expert_nodes = "\n".join(node(640 + (i % 3) * 116, 194 + (i // 3) * 186, VIOLET if i != 4 else GREEN, f"expert-{i + 1}", 38) for i in range(6))
    expert_paths = "\n".join(f'    <path id="route-{i + 1}" d="M300 291 L{640 + (i % 3) * 116} {194 + (i // 3) * 186}" stroke="{GREEN if i in (1, 4) else MUTED}" stroke-width="{10 if i in (1, 4) else 4}" opacity="{1 if i in (1, 4) else .3}"/>' for i in range(6))
    moe = shell(f'''    <g id="router"><path d="M100 210h200l72 81-72 81H100z" fill="{BLUE}" fill-opacity=".12" stroke="{BLUE}" stroke-width="6"/><circle cx="230" cy="291" r="42" fill="{BLUE}"/></g>
    <g id="routes">{expert_paths}</g>
    <g id="experts">{expert_nodes}</g>
    <path id="merge" d="M920 194v186" stroke="{CYAN}" stroke-width="10" stroke-linecap="round"/>''', "ai-moe-routing")

    slots = "\n".join(f'    <rect id="context-slot-{i + 1}" x="{72 + i * 104}" y="238" width="84" height="114" rx="18" fill="{CYAN if i < 3 else VIOLET if i < 7 else MUTED}" opacity="{.28 if i < 7 else .14}" stroke="{CYAN if i < 3 else VIOLET if i < 7 else MUTED}" stroke-width="4"/>' for i in range(9))
    context = shell(f'''    <g id="context-slots">{slots}</g>
    <path id="window-bracket" d="M176 394v30h416v-30" fill="none" stroke="{VIOLET}" stroke-width="7" stroke-linecap="round"/>
    <path id="overflow" d="M800 196v198" stroke="{CORAL}" stroke-width="7" stroke-dasharray="12 12"/>
    <g id="memory-compression"><circle cx="512" cy="142" r="42" fill="{AMBER}" fill-opacity=".15" stroke="{AMBER}" stroke-width="5"/><path d="M486 142h52M512 116v52" stroke="{AMBER}" stroke-width="7"/></g>''', "ai-context-window")

    safety = shell(f'''    <g id="input-stage">{node(116, 291, CYAN, "input-node", 46)}</g>
{arrow(174, 291, 306, 291, CYAN, "input-flow")}
    <g id="policy-gate"><path d="M330 160h176v262H330z" fill="{AMBER}" fill-opacity=".13" stroke="{AMBER}" stroke-width="6"/><path d="M418 198l54 24v54c0 52-54 82-54 82s-54-30-54-82v-54z" fill="{AMBER}" fill-opacity=".22" stroke="{AMBER}" stroke-width="6"/></g>
{arrow(518, 245, 662, 245, GREEN, "safe-flow")}
    <g id="safe-output">{node(730, 245, GREEN, "safe-node", 46)}</g>
    <path id="blocked-flow" d="M518 338H662" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/>
    <g id="blocked-output"><circle cx="730" cy="338" r="46" fill="{CORAL}" fill-opacity=".13" stroke="{CORAL}" stroke-width="5"/><path d="M708 316l44 44M752 316l-44 44" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/></g>
    <g id="audit-trail"><path d="M830 188h104v206H830z" fill="#FFFFFF" stroke="{MUTED}" stroke-width="5"/><path d="M852 230h60M852 276h60M852 322h60M852 368h42" stroke="{MUTED}" stroke-width="8" stroke-linecap="round"/></g>''', "ai-safety-gate")

    cells = []
    colors = (GREEN, CYAN, AMBER, VIOLET)
    for row in range(4):
        for col in range(5):
            value = .18 + ((row * 3 + col * 2) % 7) * .1
            cells.append(f'    <rect id="metric-{row + 1}-{col + 1}" x="{260 + col * 124}" y="{112 + row * 92}" width="102" height="70" rx="14" fill="{colors[row]}" opacity="{value:.2f}"/>')
    evaluation = shell(f'''    <g id="metric-label-slots">{''.join(f'<rect x="74" y="{112+i*92}" width="142" height="70" rx="14" fill="{colors[i]}" opacity=".16"/>' for i in range(4))}</g>
    <g id="score-grid">{''.join(cells)}</g>
    <path id="threshold" d="M246 346H900" stroke="{CORAL}" stroke-width="6" stroke-dasharray="14 10"/>
    <g id="overall-score"><circle cx="920" cy="130" r="44" fill="#FFFFFF" stroke="{BLUE}" stroke-width="7"/><path d="M896 132l16 16 34-38" fill="none" stroke="{GREEN}" stroke-width="8" stroke-linecap="round"/></g>''', "ai-evaluation-matrix")

    return {
        "ai-training-pipeline.svg": training,
        "ai-inference-pipeline.svg": inference,
        "ai-attention-map.svg": attention_map,
        "ai-rag-pipeline.svg": rag,
        "ai-agent-loop.svg": agent,
        "ai-moe-routing.svg": moe,
        "ai-context-window.svg": context,
        "ai-safety-gate.svg": safety,
        "ai-evaluation-matrix.svg": evaluation,
    }


def backgrounds() -> dict[str, str]:
    def scene(night: bool) -> str:
        sky = NAVY if night else "#EAF2FF"
        panel = "#172A46" if night else "#FFFFFF"
        line = "#31517A" if night else "#C9D8EC"
        stars = "".join(
            f'<circle cx="{90 + i * 137}" cy="{82 + (i % 3) * 66}" r="{3 + i % 4}" fill="{CYAN}" opacity=".{3 + i % 6}"/>'
            for i in range(13)
        )
        return svg(f'''  <g id="ai-model-observatory">
    <rect id="background" width="1920" height="1080" fill="{sky}"/>
    <g id="constellation-field">{stars}<path d="M90 82l274 132 274-66 274 132 274-198 274 132" fill="none" stroke="{CYAN}" stroke-width="3" opacity=".20"/></g>
    <path id="rear-wall" d="M0 356L960 210l960 146v724H0z" fill="{panel}" stroke="{line}" stroke-width="6"/>
    <g id="compute-racks">
      <rect x="90" y="410" width="260" height="440" rx="28" fill="{NAVY}" stroke="{BLUE}" stroke-width="5"/>
      <rect x="1570" y="410" width="260" height="440" rx="28" fill="{NAVY}" stroke="{VIOLET}" stroke-width="5"/>
      <g stroke="{line}" stroke-width="4"><path d="M125 500h190M125 595h190M125 690h190M125 785h190M1605 500h190M1605 595h190M1605 690h190M1605 785h190"/></g>
      <g fill="{GREEN}"><circle cx="150" cy="465" r="8"/><circle cx="1640" cy="465" r="8"/></g>
    </g>
    <g id="model-hologram">
      <circle cx="960" cy="510" r="180" fill="{VIOLET}" fill-opacity=".10" stroke="{VIOLET}" stroke-width="6"/>
      <ellipse cx="960" cy="510" rx="270" ry="92" fill="none" stroke="{CYAN}" stroke-width="5" transform="rotate(-12 960 510)"/>
      <path d="M894 548v-76l66-38 66 38v76l-66 38zM960 434v152" fill="none" stroke="{CYAN}" stroke-width="10"/>
    </g>
    <path id="floor" d="M0 860h1920v220H0z" fill="{NAVY}"/>
    <path id="floor-grid" d="M0 940h1920M260 860L90 1080M620 860l-70 220M960 860v220M1300 860l70 220M1660 860l170 220" stroke="{BLUE}" stroke-width="4" opacity=".24"/>
    <g id="presenter-zone"><ellipse cx="960" cy="890" rx="330" ry="56" fill="{CYAN}" opacity=".10"/><path d="M650 890h620" stroke="{CYAN}" stroke-width="4" stroke-dasharray="18 14"/></g>
  </g>''', view_box="0 0 1920 1080")

    return {"scene_16x9.svg": scene(False), "scene_night_16x9.svg": scene(True)}


def main() -> None:
    for name, content in components().items():
        write(COMPONENTS / name, content)
    for name, content in diagrams().items():
        write(DIAGRAMS / name, content)
    for name, content in backgrounds().items():
        write(BACKGROUNDS / name, content)
    total = len(components()) + len(diagrams()) + len(backgrounds())
    print(f"Generated {total} AI model assets under {ROOT}")


if __name__ == "__main__":
    main()
