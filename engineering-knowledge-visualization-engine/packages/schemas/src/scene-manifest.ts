import type { NarrationIntent } from "./narration-intent";
import type { SceneType, RendererTarget } from "./scene";
import type { Timing } from "./timing";
import type { VisualIntent } from "./visual-intent";

export type SceneManifestNarration = Omit<NarrationIntent, "schemaVersion" | "id">;
export type SceneManifestVisual = Omit<VisualIntent, "schemaVersion" | "id">;
export type SceneManifestTiming = Omit<Timing, "schemaVersion" | "id">;

export type SceneManifest = {
  schemaVersion: "1.0";
  id: string;
  fileName: string;
  order: number;
  slug: string;
  title: string;
  topic: string;
  domain: string;
  targetAudience: "beginner" | "intermediate" | "advanced";
  contentType: "equipment-principle" | "system-flow" | "control-algorithm";
  sceneType: SceneType;
  targetRenderer: RendererTarget;
  source: {
    outlineId: string;
    storyboardId: string;
    sectionId: string;
  };
  narration: SceneManifestNarration;
  visual: SceneManifestVisual;
  timing: SceneManifestTiming;
};
