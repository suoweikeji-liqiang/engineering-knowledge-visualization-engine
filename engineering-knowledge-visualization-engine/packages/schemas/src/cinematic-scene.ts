export type CinematicSceneMode =
  | "host-home-base"
  | "character-metaphor"
  | "evidence-to-abstraction"
  | "diagram-explainer"
  | "technical-trace"
  | "code-perspective"
  | "character-synthesis";

export type HostNarrativeSceneMode =
  | "host-cold-open"
  | "host-demo"
  | "host-diagram"
  | "host-evidence"
  | "host-synthesis";

export type HostNarrativeRole =
  | "notice"
  | "question"
  | "investigate"
  | "bridge"
  | "warn"
  | "resolve";

export type HostNarrativeBeat = {
  id: string;
  role: HostNarrativeRole;
  mode: HostNarrativeSceneMode;
  hostOnScreen: boolean;
  focus: string;
  hostAction?: string;
  evidenceRef?: string;
  transitionHook: string;
};

/**
 * A reusable episode-level grammar for presenter-led explainers. It keeps the
 * host, a continuous real-world case, demonstrations, and primary evidence in
 * one narrative instead of treating character shots as decoration.
 */
export type HostNarrativeTemplate = {
  schemaVersion: "1.0";
  id: string;
  characterId: string;
  narrativeCaseRequired: true;
  presenceTarget: {min: number; max: number};
  demonstrationTarget: {min: number};
  primaryEvidenceTarget: {min: number};
  maxSecondsWithoutVisualChange: number;
  rules: string[];
  beats: HostNarrativeBeat[];
  accumulationKey: string;
};

export type CinematicBeatRole =
  | "establish"
  | "question"
  | "reveal"
  | "translate"
  | "demonstrate"
  | "resolve";

export type CinematicSceneBeat = {
  id: string;
  role: CinematicBeatRole;
  durationHintSeconds: number;
  focus: string;
  motionHint?: string;
  soundCue?: string;
};

export type CinematicContinuityToken = {
  key: string;
  label: string;
  detail?: string;
  tone?: "teal" | "red" | "purple" | "gold";
  shape?: "token" | "label" | "path" | "object";
};

export type CinematicSoundCue = {
  id: string;
  semanticRole: "enter" | "draw" | "connect" | "confirm" | "warn" | "resolve";
  family:
    | "paper"
    | "writing"
    | "diagram"
    | "signal"
    | "chart"
    | "code"
    | "result"
    | "transition"
    | "foley"
    | "ui"
    | "character";
  durationHintMs: number;
  mixPriority: "foreground" | "support" | "ambient";
  assetRef?: string;
};

export type CharacterPerformanceState = "investigate" | "recover" | "synthesize";
export type CharacterMotionProfile = "scan-and-mark" | "error-to-success" | "assemble-and-present";

export type CharacterPerformanceBeat = {
  id: string;
  cueIndex: number;
  pose: string;
  gaze: "viewer" | "object" | "path" | "offscreen";
  gesture: string;
  expression: string;
  assetRef: string;
  transition: "cut-in" | "match-cut" | "reaction-pop";
};

export type CharacterPerformanceAsset = {
  schemaVersion: "1.0";
  id: string;
  characterId: string;
  narrativeRole: "introduce" | "investigate" | "connect" | "demonstrate" | "recover" | "synthesize";
  performanceState: CharacterPerformanceState;
  emotion: string;
  gesture: string;
  motionProfile: CharacterMotionProfile;
  focusTarget: string;
  beats: CharacterPerformanceBeat[];
  action: string;
  gaze: "viewer" | "object" | "path" | "offscreen";
  assetRef: string;
  compatibleSceneModes: CinematicSceneMode[];
  transitionHooks?: string[];
  parallaxLayers?: string[];
  accumulationKey: string;
};

export type CharacterStageActor = {
  schemaVersion: "1.0";
  id: string;
  characterId: string;
  assetRef: string;
  intrinsicSize: {width: number; height: number};
  pose: "pointing" | "thinking" | "presenting";
  gaze: "viewer" | "target";
  gesture: "point" | "chin-touch" | "open-palm";
  interactionAnchor: {
    kind: "fingertip" | "gaze" | "open-palm";
    normalizedX: number;
    normalizedY: number;
  };
  targetAnchor: "nearest-edge";
  interactionSfx: "character-think" | "character-point" | "character-present";
  compatibleVisualKinds: Array<"topology" | "code" | "bars" | "curve">;
  targetBinding: "semantic-id";
  alphaRequired: true;
  accumulationKey: string;
};

export type CharacterRigBoneName =
  | "root"
  | "torso"
  | "head"
  | "gaze"
  | "mouth"
  | "gesture";

export type CharacterRigBone = {
  id: CharacterRigBoneName;
  parent?: CharacterRigBoneName;
  pivot: {normalizedX: number; normalizedY: number};
  maxRotationDegrees?: number;
  maxTranslation?: {x: number; y: number};
};

export type CharacterRigAction = {
  id: "idle-talk" | "react-surprise" | "point-emphasis" | "think-focus" | "explain-open" | "resolve-wave";
  durationHintSeconds: number;
  loop: boolean;
  activeBones: CharacterRigBoneName[];
  audioDriven?: "voice-rms";
  narrativeRoles: HostNarrativeRole[];
};

export type CharacterRigAsset = {
  schemaVersion: "1.0";
  id: string;
  characterId: string;
  system: "xiaolan-rig-v1";
  technique: "two-part-cutout";
  bones: CharacterRigBone[];
  actions: CharacterRigAction[];
  sourcePoseAssets: Array<{
    pose: "pointing" | "thinking" | "presenting";
    assetRef: string;
    intrinsicSize: {width: number; height: number};
    upperBodyCut: number;
    faceAnchors: {
      leftEye: {normalizedX: number; normalizedY: number};
      rightEye: {normalizedX: number; normalizedY: number};
      mouth: {normalizedX: number; normalizedY: number};
    };
  }>;
  blinkIntervalSeconds: {min: number; max: number};
  lipSync: "voice-rms-envelope";
  accumulationKey: string;
};

export type LayeredCharacterRigBoneName =
  | "root"
  | "torso"
  | "head"
  | "leftUpperArm"
  | "leftForearm"
  | "leftHand"
  | "rightUpperArm"
  | "rightForearm"
  | "rightHand"
  | "eyes"
  | "mouth";

export type LayeredCharacterRigBone = {
  id: LayeredCharacterRigBoneName;
  parent?: LayeredCharacterRigBoneName;
  partRef?: string;
  pivot: {normalizedX: number; normalizedY: number};
  maxRotationDegrees?: number;
  audioDriven?: "voice-rms";
};

export type LayeredCharacterRigAction = {
  id: "point-emphasis" | "think-focus" | "explain-open" | "resolve-wave";
  durationHintSeconds: number;
  loop: boolean;
  activeBones: LayeredCharacterRigBoneName[];
  narrativeRoles: HostNarrativeRole[];
};

/**
 * A real cutout rig: limbs and face states are independent transparent assets.
 * Unlike CharacterRigAsset V1, motion must rotate child bones around joints and
 * must never be simulated by translating a complete character illustration.
 */
export type LayeredCharacterRigAsset = {
  schemaVersion: "1.0";
  id: string;
  characterId: string;
  system: "xiaolan-rig-v2";
  technique: "layered-cutout-skeleton";
  partsManifestRef: string;
  bones: LayeredCharacterRigBone[];
  actions: LayeredCharacterRigAction[];
  face: {
    blinkSprites: [string, string];
    mouthSprites: [string, string, string];
    lipSync: "voice-rms-sprite-selection";
  };
  sourceAssetCount: number;
  alphaRequired: true;
  accumulationKey: string;
};

export type TopologyComposition =
  | "orbit"
  | "branch"
  | "quadrants"
  | "constellation"
  | "dashboard"
  | "hero-map";

export type TopologySceneGrammar = {
  schemaVersion: "1.0";
  id: string;
  composition: TopologyComposition;
  relationship: "system-parts" | "state-exits" | "typed-memory" | "delegation" | "evaluation" | "synthesis";
  narrativePurpose: string;
  recommendedFor: string[];
  motionBeats: string[];
  accumulationKey: string;
};

/**
 * A reusable scene grammar, not an episode-specific shot.
 * Domain packs provide catalog entries; episodes bind copy and media assets.
 */
export type CinematicSceneAsset = {
  schemaVersion: "1.0";
  id: string;
  mode: CinematicSceneMode;
  narrativePurpose: string;
  requiredInputs: string[];
  optionalInputs?: string[];
  beats: CinematicSceneBeat[];
  continuityIn?: CinematicContinuityToken;
  continuityOut?: CinematicContinuityToken;
  transitionIn?: string;
  transitionOut?: string;
  accumulationKey: string;
};
