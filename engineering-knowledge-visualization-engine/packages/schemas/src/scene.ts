export type Scene = {
  id: string;
  title: string;
  sceneType: string;
  targetRenderer: "manim" | "remotion" | "asset-based";
  visualIntentId?: string;
  narrationIntentId?: string;
  timingId?: string;
};
