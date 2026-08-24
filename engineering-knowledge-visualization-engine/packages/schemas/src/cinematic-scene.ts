export type CinematicSceneMode =
  | "host-home-base"
  | "character-metaphor"
  | "evidence-to-abstraction"
  | "diagram-explainer"
  | "technical-trace"
  | "code-perspective"
  | "character-synthesis";

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
  action: string;
  gaze: "viewer" | "object" | "path" | "offscreen";
  assetRef: string;
  compatibleSceneModes: CinematicSceneMode[];
  transitionHooks?: string[];
  parallaxLayers?: string[];
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
