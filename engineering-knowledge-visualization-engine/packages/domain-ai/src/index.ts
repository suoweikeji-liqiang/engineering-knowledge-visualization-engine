import type {CharacterPerformanceAsset, CharacterRigAsset, CharacterStageActor, CinematicSceneAsset, CinematicSoundCue, HostNarrativeTemplate, TopologySceneGrammar} from "@repo/schemas";

export const AI_HOST_NARRATIVE_TEMPLATES: HostNarrativeTemplate[] = [
  {
    schemaVersion: "1.0",
    id: "xiaolan-hosted-case-study-v1",
    characterId: "xiaolan",
    narrativeCaseRequired: true,
    presenceTarget: {min: 0.45, max: 0.65},
    demonstrationTarget: {min: 0.25},
    primaryEvidenceTarget: {min: 2},
    maxSecondsWithoutVisualChange: 5,
    rules: [
      "先让主持人遇到或观察到具体事件，再提出抽象概念",
      "主持人每次出场必须执行 notice、question、investigate、bridge、warn、resolve 中的一种叙事动作",
      "真实演示必须保留设备、结果和前后状态，不能只作为模糊背景",
      "技术图解应从主持人的手势、道具或上一镜结果中生长出来",
      "结尾回到开场案例，用可验证结果收束观点"
    ],
    beats: [
      {id: "event", role: "notice", mode: "host-cold-open", hostOnScreen: true, focus: "现实事件与人物反应", hostAction: "注意到异常信号", transitionHook: "notification-card"},
      {id: "proof", role: "investigate", mode: "host-demo", hostOnScreen: false, focus: "真实操作与状态变化", evidenceRef: "official-demo", transitionHook: "device-frame"},
      {id: "model", role: "bridge", mode: "host-diagram", hostOnScreen: true, focus: "从案例抽出系统结构", hostAction: "沿执行路径指向关键节点", transitionHook: "signal-path"},
      {id: "source", role: "warn", mode: "host-evidence", hostOnScreen: true, focus: "一手来源、能力边界和限制", hostAction: "标记证据而非代替证据", evidenceRef: "primary-source", transitionHook: "marker-stroke"},
      {id: "return", role: "resolve", mode: "host-synthesis", hostOnScreen: true, focus: "案例结果与主持人判断", hostAction: "回到观众并给出适用边界", transitionHook: "callback-object"}
    ],
    accumulationKey: "ai/narrative/hosted-case-study/v1"
  }
];

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

export const AI_CHARACTER_PERFORMANCE_ASSETS: CharacterPerformanceAsset[] = [
  {
    schemaVersion: "1.0",
    id: "xiaolan-evidence-bridge",
    characterId: "xiaolan",
    narrativeRole: "investigate",
    performanceState: "investigate",
    emotion: "focused",
    gesture: "annotate",
    motionProfile: "scan-and-mark",
    focusTarget: "evidence gap",
    beats: [
      {id: "notice-gap", cueIndex: 0, pose: "close-up-think", gaze: "object", gesture: "chin-touch", expression: "curious", assetRef: "ai/character/xiaolan/pose/thinking", transition: "cut-in"},
      {id: "mark-gap", cueIndex: 2, pose: "standing-point", gaze: "path", gesture: "point", expression: "focused", assetRef: "ai/character/xiaolan/pose/pointing", transition: "match-cut"},
      {id: "state-proof", cueIndex: 4, pose: "present-sign", gaze: "viewer", gesture: "hold-proof", expression: "resolved", assetRef: "ai/character/xiaolan/pose/sign", transition: "reaction-pop"}
    ],
    action: "从来源文档中提取关键句，并把荧光标记延展成技术图解",
    gaze: "object",
    assetRef: "ai/character/xiaolan/evidence-bridge",
    compatibleSceneModes: ["evidence-to-abstraction", "character-metaphor"],
    transitionHooks: ["highlight-stroke", "document-edge"],
    parallaxLayers: ["foreground-notes", "character", "evidence-board", "observatory-background"],
    accumulationKey: "ai/character/xiaolan/performance/evidence-bridge"
  },
  {
    schemaVersion: "1.0",
    id: "xiaolan-connect-modules",
    characterId: "xiaolan",
    narrativeRole: "connect",
    performanceState: "synthesize",
    emotion: "confident",
    gesture: "present",
    motionProfile: "assemble-and-present",
    focusTarget: "artifact stack",
    beats: [
      {id: "review-artifacts", cueIndex: 0, pose: "desk-review", gaze: "object", gesture: "review", expression: "attentive", assetRef: "ai/character/xiaolan/pose/desk", transition: "cut-in"},
      {id: "connect-proof", cueIndex: 2, pose: "standing-point", gaze: "path", gesture: "point", expression: "confident", assetRef: "ai/character/xiaolan/pose/pointing", transition: "match-cut"},
      {id: "close-episode", cueIndex: 4, pose: "host-wave", gaze: "viewer", gesture: "wave", expression: "warm", assetRef: "ai/character/xiaolan/pose/outro", transition: "reaction-pop"}
    ],
    action: "把分散模块接入同一条信号路径，建立系统关系",
    gaze: "path",
    assetRef: "ai/character/xiaolan/connect-modules",
    compatibleSceneModes: ["diagram-explainer", "character-metaphor"],
    transitionHooks: ["signal-cable", "module-node"],
    parallaxLayers: ["foreground-tools", "character", "modules", "observatory-background"],
    accumulationKey: "ai/character/xiaolan/performance/connect-modules"
  },
  {
    schemaVersion: "1.0",
    id: "xiaolan-recover-path",
    characterId: "xiaolan",
    narrativeRole: "recover",
    performanceState: "recover",
    emotion: "determined",
    gesture: "reroute",
    motionProfile: "error-to-success",
    focusTarget: "checkpoint path",
    beats: [
      {id: "notice-error", cueIndex: 0, pose: "desk-alert", gaze: "object", gesture: "brace", expression: "surprised", assetRef: "ai/character/xiaolan/pose/surprised", transition: "reaction-pop"},
      {id: "find-checkpoint", cueIndex: 2, pose: "close-up-think", gaze: "path", gesture: "chin-touch", expression: "determined", assetRef: "ai/character/xiaolan/pose/thinking", transition: "match-cut"},
      {id: "confirm-recovery", cueIndex: 4, pose: "present-sign", gaze: "viewer", gesture: "hold-proof", expression: "relieved", assetRef: "ai/character/xiaolan/pose/sign", transition: "cut-in"}
    ],
    action: "面对失败分支重新规划路径，并把错误状态转回可执行流程",
    gaze: "path",
    assetRef: "ai/character/xiaolan/recover-path",
    compatibleSceneModes: ["technical-trace", "character-synthesis"],
    transitionHooks: ["red-error-path", "green-recovery-path"],
    parallaxLayers: ["foreground-alert", "character", "route-board", "observatory-background"],
    accumulationKey: "ai/character/xiaolan/performance/recover-path"
  }
];

export const AI_CHARACTER_STAGE_ASSETS: CharacterStageActor[] = [
  {schemaVersion: "1.0", id: "xiaolan-stage-pointing", characterId: "xiaolan", assetRef: "ai/character/xiaolan/stage/pointing", intrinsicSize: {width: 1367, height: 1151}, pose: "pointing", gaze: "target", gesture: "point", interactionAnchor: {kind: "fingertip", normalizedX: 0.864, normalizedY: 0.372}, targetAnchor: "nearest-edge", interactionSfx: "character-point", compatibleVisualKinds: ["topology", "code", "bars", "curve"], targetBinding: "semantic-id", alphaRequired: true, accumulationKey: "ai/character/xiaolan/stage/pointing"},
  {schemaVersion: "1.0", id: "xiaolan-stage-thinking", characterId: "xiaolan", assetRef: "ai/character/xiaolan/stage/thinking", intrinsicSize: {width: 1369, height: 1149}, pose: "thinking", gaze: "target", gesture: "chin-touch", interactionAnchor: {kind: "gaze", normalizedX: 0.43, normalizedY: 0.3}, targetAnchor: "nearest-edge", interactionSfx: "character-think", compatibleVisualKinds: ["topology", "code", "bars", "curve"], targetBinding: "semantic-id", alphaRequired: true, accumulationKey: "ai/character/xiaolan/stage/thinking"},
  {schemaVersion: "1.0", id: "xiaolan-stage-presenting", characterId: "xiaolan", assetRef: "ai/character/xiaolan/stage/presenting", intrinsicSize: {width: 1448, height: 1086}, pose: "presenting", gaze: "viewer", gesture: "open-palm", interactionAnchor: {kind: "open-palm", normalizedX: 0.18, normalizedY: 0.5}, targetAnchor: "nearest-edge", interactionSfx: "character-present", compatibleVisualKinds: ["topology", "code", "bars", "curve"], targetBinding: "semantic-id", alphaRequired: true, accumulationKey: "ai/character/xiaolan/stage/presenting"}
];

export const AI_CHARACTER_RIGS: CharacterRigAsset[] = [
  {
    schemaVersion: "1.0",
    id: "xiaolan-rig-v1",
    characterId: "xiaolan",
    system: "xiaolan-rig-v1",
    technique: "two-part-cutout",
    bones: [
      {id: "root", pivot: {normalizedX: 0.5, normalizedY: 1}, maxTranslation: {x: 16, y: 18}},
      {id: "torso", parent: "root", pivot: {normalizedX: 0.5, normalizedY: 0.72}, maxRotationDegrees: 2},
      {id: "head", parent: "torso", pivot: {normalizedX: 0.5, normalizedY: 0.54}, maxRotationDegrees: 4, maxTranslation: {x: 5, y: 7}},
      {id: "gaze", parent: "head", pivot: {normalizedX: 0.5, normalizedY: 0.29}, maxTranslation: {x: 3, y: 2}},
      {id: "mouth", parent: "head", pivot: {normalizedX: 0.5, normalizedY: 0.39}, maxTranslation: {x: 0, y: 4}},
      {id: "gesture", parent: "torso", pivot: {normalizedX: 0.86, normalizedY: 0.37}, maxRotationDegrees: 6}
    ],
    actions: [
      {id: "idle-talk", durationHintSeconds: 4, loop: true, activeBones: ["root", "torso", "head", "gaze", "mouth"], audioDriven: "voice-rms", narrativeRoles: ["notice", "question", "investigate", "bridge", "warn", "resolve"]},
      {id: "react-surprise", durationHintSeconds: 1.1, loop: false, activeBones: ["root", "head", "gaze", "mouth"], audioDriven: "voice-rms", narrativeRoles: ["notice", "question"]},
      {id: "point-emphasis", durationHintSeconds: 1.4, loop: false, activeBones: ["torso", "head", "gaze", "mouth", "gesture"], audioDriven: "voice-rms", narrativeRoles: ["bridge", "warn"]},
      {id: "think-focus", durationHintSeconds: 3.2, loop: true, activeBones: ["root", "head", "gaze", "mouth"], audioDriven: "voice-rms", narrativeRoles: ["investigate", "warn"]},
      {id: "explain-open", durationHintSeconds: 2.2, loop: true, activeBones: ["root", "torso", "head", "gaze", "mouth", "gesture"], audioDriven: "voice-rms", narrativeRoles: ["bridge"]},
      {id: "resolve-wave", durationHintSeconds: 2.4, loop: false, activeBones: ["root", "torso", "head", "gaze", "mouth", "gesture"], audioDriven: "voice-rms", narrativeRoles: ["resolve"]}
    ],
    sourcePoseAssets: [
      {pose: "pointing", assetRef: "ai/character/xiaolan/stage/pointing", intrinsicSize: {width: 1367, height: 1151}, upperBodyCut: 0.54, faceAnchors: {leftEye: {normalizedX: 0.446, normalizedY: 0.278}, rightEye: {normalizedX: 0.556, normalizedY: 0.278}, mouth: {normalizedX: 0.47, normalizedY: 0.365}}},
      {pose: "thinking", assetRef: "ai/character/xiaolan/stage/thinking", intrinsicSize: {width: 1369, height: 1149}, upperBodyCut: 0.55, faceAnchors: {leftEye: {normalizedX: 0.417, normalizedY: 0.24}, rightEye: {normalizedX: 0.519, normalizedY: 0.24}, mouth: {normalizedX: 0.447, normalizedY: 0.387}}},
      {pose: "presenting", assetRef: "ai/character/xiaolan/stage/presenting", intrinsicSize: {width: 1448, height: 1086}, upperBodyCut: 0.56, faceAnchors: {leftEye: {normalizedX: 0.479, normalizedY: 0.267}, rightEye: {normalizedX: 0.573, normalizedY: 0.267}, mouth: {normalizedX: 0.535, normalizedY: 0.364}}}
    ],
    blinkIntervalSeconds: {min: 2.8, max: 5.2},
    lipSync: "voice-rms-envelope",
    accumulationKey: "ai/character/xiaolan/rig/v1"
  }
];

export const AI_TOPOLOGY_SCENE_GRAMMARS: TopologySceneGrammar[] = [
  {
    schemaVersion: "1.0",
    id: "ai-topology-orbit",
    composition: "orbit",
    relationship: "system-parts",
    narrativePurpose: "表达多个能力共同围绕一个系统核心工作",
    recommendedFor: ["agent components", "runtime capabilities", "shared services"],
    motionBeats: ["establish core", "reveal orbiting parts", "connect into system"],
    accumulationKey: "ai/explanation/topology/orbit"
  },
  {
    schemaVersion: "1.0",
    id: "ai-topology-branch",
    composition: "branch",
    relationship: "state-exits",
    narrativePurpose: "从一个运行态明确分叉到多个互斥出口",
    recommendedFor: ["stop reasons", "error routes", "approval outcomes"],
    motionBeats: ["establish active state", "draw directed exits", "land on terminal states"],
    accumulationKey: "ai/explanation/topology/branch"
  },
  {
    schemaVersion: "1.0",
    id: "ai-topology-quadrants",
    composition: "quadrants",
    relationship: "typed-memory",
    narrativePurpose: "把容易混淆的四类状态或存储对象分区对照",
    recommendedFor: ["state versus memory", "artifact types", "context layers"],
    motionBeats: ["establish shared session", "reveal typed quadrants", "contrast responsibilities"],
    accumulationKey: "ai/explanation/topology/quadrants"
  },
  {
    schemaVersion: "1.0",
    id: "ai-topology-constellation",
    composition: "constellation",
    relationship: "delegation",
    narrativePurpose: "用不对称空间距离表达角色分工、委派与回传",
    recommendedFor: ["multi-agent", "manager and handoff", "distributed tools"],
    motionBeats: ["establish coordinator", "dispatch work", "return structured results"],
    accumulationKey: "ai/explanation/topology/constellation"
  },
  {
    schemaVersion: "1.0",
    id: "ai-topology-dashboard",
    composition: "dashboard",
    relationship: "evaluation",
    narrativePurpose: "把多种确定性检查聚合为一个评测核心",
    recommendedFor: ["evals", "quality gates", "artifact verification"],
    motionBeats: ["establish artifact", "attach checks", "resolve executable constraints"],
    accumulationKey: "ai/explanation/topology/dashboard"
  },
  {
    schemaVersion: "1.0",
    id: "ai-topology-hero-map",
    composition: "hero-map",
    relationship: "synthesis",
    narrativePurpose: "在收束镜头中把多个概念沿同一基线汇入核心判断",
    recommendedFor: ["chapter synthesis", "system recap", "final thesis"],
    motionBeats: ["state thesis", "assemble supporting roles", "hold final system map"],
    accumulationKey: "ai/explanation/topology/hero-map"
  }
];

export const AI_SOUND_CUES: CinematicSoundCue[] = [
  {id: "paper-settle", semanticRole: "enter", family: "paper", durationHintMs: 420, mixPriority: "support"},
  {id: "document-settle", semanticRole: "enter", family: "paper", durationHintMs: 520, mixPriority: "support"},
  {id: "marker-draw", semanticRole: "draw", family: "writing", durationHintMs: 520, mixPriority: "foreground"},
  {id: "connector-draw", semanticRole: "connect", family: "diagram", durationHintMs: 460, mixPriority: "foreground"},
  {id: "data-pulse", semanticRole: "connect", family: "signal", durationHintMs: 220, mixPriority: "support"},
  {id: "data-rise", semanticRole: "draw", family: "chart", durationHintMs: 680, mixPriority: "support"},
  {id: "curve-draw", semanticRole: "draw", family: "chart", durationHintMs: 900, mixPriority: "support"},
  {id: "code-focus", semanticRole: "draw", family: "code", durationHintMs: 180, mixPriority: "support"},
  {id: "editor-open", semanticRole: "enter", family: "code", durationHintMs: 360, mixPriority: "support"},
  {id: "terminal-success", semanticRole: "confirm", family: "result", durationHintMs: 280, mixPriority: "foreground"},
  {id: "result-stamp", semanticRole: "resolve", family: "result", durationHintMs: 360, mixPriority: "foreground"},
  {id: "scene-whoosh", semanticRole: "enter", family: "transition", durationHintMs: 620, mixPriority: "ambient"},
  {id: "soft-step", semanticRole: "enter", family: "foley", durationHintMs: 240, mixPriority: "ambient"},
  {id: "task-inject", semanticRole: "enter", family: "signal", durationHintMs: 380, mixPriority: "support"},
  {id: "soft-tick", semanticRole: "confirm", family: "ui", durationHintMs: 140, mixPriority: "ambient"},
  {id: "character-return", semanticRole: "resolve", family: "character", durationHintMs: 540, mixPriority: "support"},
  {id: "character-think", semanticRole: "connect", family: "character", durationHintMs: 420, mixPriority: "support"},
  {id: "character-point", semanticRole: "connect", family: "character", durationHintMs: 360, mixPriority: "foreground"},
  {id: "character-present", semanticRole: "resolve", family: "character", durationHintMs: 460, mixPriority: "support"}
];

export const AI_REVIEW_RULES = [
  "不要把一次模型回答描述为已完成的 Agent 任务",
  "展示工具调用时必须同时说明输入、结果与失败路径",
  "角色隐喻之后必须回到技术结构，不能只保留情绪画面",
  "证据画面必须保留来源、页码或可追溯标识",
  "技术 Trace 必须呈现状态变化，而不是只展示终端装饰"
] as const;
