import type {CinematicSceneAsset} from "@repo/schemas";

export const AI_CINEMATIC_SCENES: CinematicSceneAsset[] = [
  {
    schemaVersion: "1.0",
    id: "ai-host-home-base",
    mode: "host-home-base",
    narrativePurpose: "让固定主持人在稳定世界观中提出本期问题",
    requiredInputs: ["characterAsset", "locationAsset", "question"],
    optionalInputs: ["propAssets", "ambientSound"],
    beats: [
      {id: "establish", role: "establish", durationHintSeconds: 1.2, focus: "地点与人物", motionHint: "slow push-in"},
      {id: "question", role: "question", durationHintSeconds: 2.2, focus: "本期核心问题", motionHint: "character look or gesture"}
    ],
    transitionOut: "match prop or handwritten mark into the next scene",
    accumulationKey: "ai/host-home-base"
  },
  {
    schemaVersion: "1.0",
    id: "ai-character-metaphor",
    mode: "character-metaphor",
    narrativePurpose: "先用角色动作建立直觉，再把动作翻译成技术结构",
    requiredInputs: ["characterAsset", "metaphorWorld", "conceptMappings"],
    optionalInputs: ["propAssets", "foleyCues"],
    beats: [
      {id: "metaphor", role: "demonstrate", durationHintSeconds: 2.4, focus: "角色在隐喻世界中的连续动作", motionHint: "parallax and camera follow"},
      {id: "translate", role: "translate", durationHintSeconds: 1.2, focus: "动作与技术概念的对应", motionHint: "semantic morph"},
      {id: "diagram", role: "reveal", durationHintSeconds: 2.4, focus: "技术图解", motionHint: "trace the same path"}
    ],
    transitionIn: "enter through a familiar object or host gesture",
    transitionOut: "preserve spatial positions into the technical diagram",
    accumulationKey: "ai/character-metaphor"
  },
  {
    schemaVersion: "1.0",
    id: "ai-evidence-to-abstraction",
    mode: "evidence-to-abstraction",
    narrativePurpose: "把一手证据中的关键句变成可理解的结构图",
    requiredInputs: ["evidenceAsset", "sourceMeta", "claims", "diagramNodes"],
    optionalInputs: ["highlightRegions", "pageNumber"],
    beats: [
      {id: "source", role: "establish", durationHintSeconds: 1.0, focus: "可追溯的一手来源", motionHint: "document settle"},
      {id: "extract", role: "reveal", durationHintSeconds: 1.6, focus: "关键句与证据区域", motionHint: "marker highlight"},
      {id: "abstract", role: "translate", durationHintSeconds: 2.2, focus: "从证据抽出的技术结构", motionHint: "highlight becomes connector"}
    ],
    transitionOut: "highlight stroke becomes a diagram edge",
    accumulationKey: "ai/evidence-to-abstraction"
  },
  {
    schemaVersion: "1.0",
    id: "ai-technical-trace",
    mode: "technical-trace",
    narrativePurpose: "用一次具体执行把抽象架构变成可观察的因果链",
    requiredInputs: ["task", "traceSteps", "result"],
    optionalInputs: ["terminalLines", "latency", "errorBranch"],
    beats: [
      {id: "task", role: "question", durationHintSeconds: 0.8, focus: "输入任务", motionHint: "task card enters"},
      {id: "trace", role: "demonstrate", durationHintSeconds: 3.2, focus: "逐步执行与状态变化", motionHint: "moving pulse"},
      {id: "result", role: "resolve", durationHintSeconds: 1.2, focus: "成功或失败的可验证结果", motionHint: "terminal scan and outcome stamp"}
    ],
    accumulationKey: "ai/technical-trace"
  },
  {
    schemaVersion: "1.0",
    id: "ai-metric-progression",
    mode: "diagram-explainer",
    narrativePurpose: "让对比数据从共同基线依次增长，并在最后落到一个可解释差异",
    requiredInputs: ["series", "values", "unit", "source"],
    optionalInputs: ["baseline", "annotations", "highlightIndex"],
    beats: [
      {id: "baseline", role: "establish", durationHintSeconds: 0.6, focus: "共同基线与单位", motionHint: "draw axis"},
      {id: "grow", role: "demonstrate", durationHintSeconds: 2.2, focus: "柱形依次增长", motionHint: "staggered scale from baseline"},
      {id: "compare", role: "resolve", durationHintSeconds: 1.2, focus: "差异与结论", motionHint: "value count and marker note"}
    ],
    accumulationKey: "ai/explanation/chart/bars"
  },
  {
    schemaVersion: "1.0",
    id: "ai-trend-explanation",
    mode: "diagram-explainer",
    narrativePurpose: "用曲线表达趋势、阶段或阈值，并把节点与因果事件对应",
    requiredInputs: ["points", "unit", "source"],
    optionalInputs: ["phases", "threshold", "comparisonSeries"],
    beats: [
      {id: "axis", role: "establish", durationHintSeconds: 0.5, focus: "坐标含义", motionHint: "axis reveal"},
      {id: "trace", role: "demonstrate", durationHintSeconds: 2.0, focus: "曲线与节点", motionHint: "path draw"},
      {id: "phases", role: "translate", durationHintSeconds: 1.6, focus: "阶段与原因", motionHint: "node-to-callout"}
    ],
    accumulationKey: "ai/explanation/chart/curve"
  },
  {
    schemaVersion: "1.0",
    id: "ai-code-walkthrough",
    mode: "code-perspective",
    narrativePurpose: "把真实关键代码、调用栈和运行结果组织成一条可跟随的执行路径",
    requiredInputs: ["sourceRef", "codeLines", "focusSteps", "output"],
    optionalInputs: ["callStack", "diff", "errorBranch"],
    beats: [
      {id: "file", role: "establish", durationHintSeconds: 0.6, focus: "文件与代码位置", motionHint: "editor settle"},
      {id: "walk", role: "demonstrate", durationHintSeconds: 2.8, focus: "逐行执行与调用栈", motionHint: "focus line and advance stack"},
      {id: "output", role: "resolve", durationHintSeconds: 1.1, focus: "可复现的运行结果", motionHint: "terminal scan and result stamp"}
    ],
    transitionOut: "focused symbol or output value becomes the next diagram label",
    accumulationKey: "ai/explanation/code/walkthrough"
  },
  {
    schemaVersion: "1.0",
    id: "ai-character-synthesis",
    mode: "character-synthesis",
    narrativePurpose: "由主持人把多个技术事实收束成带立场的个人判断",
    requiredInputs: ["characterAsset", "thesis", "supportingPoints"],
    optionalInputs: ["nextQuestion", "callbackProp"],
    beats: [
      {id: "return", role: "establish", durationHintSeconds: 0.8, focus: "主持人回到画面", motionHint: "match cut to home base"},
      {id: "synthesis", role: "resolve", durationHintSeconds: 2.6, focus: "个人判断与适用边界", motionHint: "gesture plus handwritten summary"}
    ],
    accumulationKey: "ai/character-synthesis"
  }
];

export const AI_VISUAL_METAPHORS = [
  {concept: "agent-loop", world: "跨越连续踏脚石", mapping: ["目标=远处旗帜", "规划=路线草图", "工具调用=落脚", "观察=回望结果", "完成=抵达"]},
  {concept: "context-window", world: "观测站工作台", mapping: ["上下文=桌面可见区", "检索=抽屉取档", "压缩=整理成索引卡"]},
  {concept: "tool-router", world: "空间站转接台", mapping: ["工具=接口舱", "权限=舱门", "返回值=信号回流"]},
  {concept: "model-vs-runtime", world: "领航员与飞船", mapping: ["模型=判断航向", "运行时=持续执行", "护栏=航行规则"]}
] as const;

export const AI_REVIEW_RULES = [
  "不要把一次模型回答描述为已完成的 Agent 任务",
  "展示工具调用时必须同时说明输入、结果与失败路径",
  "角色隐喻之后必须回到技术结构，不能只保留情绪画面",
  "证据画面必须保留来源、页码或可追溯标识",
  "技术 Trace 必须呈现状态变化，而不是只展示终端装饰"
] as const;
