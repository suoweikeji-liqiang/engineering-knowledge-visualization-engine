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
  transitionIn?: string;
  transitionOut?: string;
  accumulationKey: string;
};
