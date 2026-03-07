export type Scene = {
  schemaVersion: "1.0";
  id: string;
  title: string;
  sceneType: string;
  targetRenderer: "manim" | "remotion" | "asset-based";
  visualIntentId?: string;
  narrationIntentId?: string;
  timingId?: string;
};
