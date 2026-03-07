import { Scene, NarrationIntent, VisualIntent, Timing } from "@repo/schemas";

export type Storyboard = {
  schemaVersion: "1.0";
  outlineId: string;
  scenes: Scene[];
  narrationIntents: NarrationIntent[];
  visualIntents: VisualIntent[];
  timings: Timing[];
};

export type OutlineInput = {
  topic: string;
  sections: Array<{
    id: string;
    title: string;
    learningObjective: string;
    keyPoints: string[];
  }>;
};

export function outlineToStoryboard(outline: OutlineInput): Storyboard {
  const scenes: Scene[] = [];
  const narrationIntents: NarrationIntent[] = [];
  const visualIntents: VisualIntent[] = [];
  const timings: Timing[] = [];

  outline.sections.forEach((section, index) => {
    const sceneId = `scene-${String(index + 1).padStart(2, "0")}`;
    const narrationId = `narration-${sceneId}`;
    const visualId = `visual-${sceneId}`;
    const timingId = `timing-${sceneId}`;

    scenes.push({
      schemaVersion: "1.0",
      id: sceneId,
      title: section.title,
      sceneType: "explanation",
      targetRenderer: "manim",
      visualIntentId: visualId,
      narrationIntentId: narrationId,
      timingId: timingId
    });

    narrationIntents.push({
      schemaVersion: "1.0",
      id: narrationId,
      goal: section.learningObjective,
      audienceLevel: "beginner",
      emphasisPoints: section.keyPoints
    });

    visualIntents.push({
      schemaVersion: "1.0",
      id: visualId,
      primaryObjects: section.keyPoints,
      visualPattern: "sequential-reveal"
    });

    timings.push({
      schemaVersion: "1.0",
      id: timingId,
      estimatedDurationSec: 30
    });
  });

  return {
    schemaVersion: "1.0",
    outlineId: outline.topic,
    scenes,
    narrationIntents,
    visualIntents,
    timings
  };
}
