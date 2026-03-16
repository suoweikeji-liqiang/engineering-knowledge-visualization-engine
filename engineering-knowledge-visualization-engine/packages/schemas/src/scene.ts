export type RendererTarget = "manim" | "remotion" | "asset-based";

export type SceneType =
  | "introduction"
  | "component-breakdown"
  | "principle"
  | "system-flow"
  | "control-logic"
  | "summary";

export type Scene = {
  schemaVersion: "1.0";
  id: string;
  order: number;
  title: string;
  sourceSectionId: string;
  sceneType: SceneType;
  targetRenderer: RendererTarget;
  visualIntentId?: string;
  narrationIntentId?: string;
  timingId?: string;
};
