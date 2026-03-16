import {
  NarrationIntent,
  RendererTarget,
  Scene,
  SceneType,
  Timing,
  VisualIntent
} from "@repo/schemas";

export type Storyboard = {
  schemaVersion: "1.0";
  id: string;
  outlineId: string;
  topic: string;
  domain: string;
  targetAudience: "beginner" | "intermediate" | "advanced";
  contentType: "equipment-principle" | "system-flow" | "control-algorithm";
  scenes: Scene[];
  narrationIntents: NarrationIntent[];
  visualIntents: VisualIntent[];
  timings: Timing[];
  totalEstimatedDurationSec: number;
};

export type OutlineInput = {
  topic: string;
  domain: string;
  targetAudience: "beginner" | "intermediate" | "advanced";
  contentType: "equipment-principle" | "system-flow" | "control-algorithm";
  sections: Array<{
    id: string;
    title: string;
    learningObjective: string;
    keyPoints: string[];
    estimatedDurationSec: number;
  }>;
};

function slugify(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .replace(/-{2,}/g, "-");
}

function inferSceneType(
  contentType: OutlineInput["contentType"],
  section: OutlineInput["sections"][number],
  index: number,
  totalSections: number
): SceneType {
  const normalizedTitle = section.title.toLowerCase();

  if (normalizedTitle.includes("summary") || index === totalSections - 1) {
    return "summary";
  }

  if (index === 0) {
    return "introduction";
  }

  if (normalizedTitle.includes("component")) {
    return "component-breakdown";
  }

  if (contentType === "system-flow") {
    return "system-flow";
  }

  if (contentType === "control-algorithm") {
    return "control-logic";
  }

  return "principle";
}

function inferTargetRenderer(sceneType: SceneType): RendererTarget {
  if (sceneType === "introduction" || sceneType === "summary") {
    return "remotion";
  }

  return "manim";
}

function inferExplanationStyle(sceneType: SceneType): string {
  switch (sceneType) {
    case "introduction":
      return "purpose-context-first";
    case "component-breakdown":
      return "label-and-function";
    case "system-flow":
      return "chronological-flow-trace";
    case "control-logic":
      return "feedback-first";
    case "summary":
      return "recap-and-transfer";
    case "principle":
    default:
      return "cause-and-effect";
  }
}

function inferVisualPattern(sceneType: SceneType): string {
  switch (sceneType) {
    case "introduction":
      return "chapter-card";
    case "component-breakdown":
      return "component-highlight-sequence";
    case "system-flow":
      return "flow-trace";
    case "control-logic":
      return "signal-and-response";
    case "summary":
      return "key-takeaways";
    case "principle":
    default:
      return "process-reveal";
  }
}

function inferMotionType(sceneType: SceneType): string {
  switch (sceneType) {
    case "introduction":
      return "title-reveal";
    case "component-breakdown":
      return "sequential-highlight";
    case "system-flow":
      return "directional-flow";
    case "control-logic":
      return "signal-propagation";
    case "summary":
      return "bullet-recap";
    case "principle":
    default:
      return "progressive-build";
  }
}

function inferDiagramStyle(sceneType: SceneType, targetRenderer: RendererTarget): string {
  if (targetRenderer === "remotion") {
    return "motion-graphic";
  }

  if (sceneType === "control-logic") {
    return "block-diagram";
  }

  return "technical-schematic";
}

function derivePrimaryObjects(keyPoints: string[]): string[] {
  const candidates = keyPoints.map((keyPoint) => {
    const [label] = keyPoint.split(/\s[-:]\s/);
    return label.trim();
  });

  return Array.from(new Set(candidates)).filter((candidate) => candidate.length > 0);
}

function deriveHighlightTargets(sceneType: SceneType, primaryObjects: string[]): string[] | undefined {
  if (sceneType === "component-breakdown") {
    return primaryObjects.slice(0, 4);
  }

  if (sceneType === "control-logic") {
    return ["setpoint", "error", "controller-output", "feedback"];
  }

  return undefined;
}

function buildBeatPoints(estimatedDurationSec: number): number[] {
  const points = [
    0,
    Math.round(estimatedDurationSec * 0.25),
    Math.round(estimatedDurationSec * 0.5),
    Math.round(estimatedDurationSec * 0.75)
  ].filter((point) => point >= 0 && point < estimatedDurationSec);

  return Array.from(new Set(points)).sort((left, right) => left - right);
}

export function outlineToStoryboard(outline: OutlineInput): Storyboard {
  const scenes: Scene[] = [];
  const narrationIntents: NarrationIntent[] = [];
  const visualIntents: VisualIntent[] = [];
  const timings: Timing[] = [];
  const outlineSlug = slugify(outline.topic);
  const outlineId = `outline-${outlineSlug}`;
  const storyboardId = `storyboard-${outlineSlug}`;

  outline.sections.forEach((section, index) => {
    const sceneOrder = index + 1;
    const sceneSlug = slugify(section.title);
    const sceneId = `scene-${String(sceneOrder).padStart(2, "0")}-${sceneSlug}`;
    const narrationId = `narration-${sceneId}`;
    const visualId = `visual-${sceneId}`;
    const timingId = `timing-${sceneId}`;
    const sceneType = inferSceneType(outline.contentType, section, index, outline.sections.length);
    const targetRenderer = inferTargetRenderer(sceneType);
    const primaryObjects = derivePrimaryObjects(section.keyPoints);

    scenes.push({
      schemaVersion: "1.0",
      id: sceneId,
      order: sceneOrder,
      title: section.title,
      sourceSectionId: section.id,
      sceneType,
      targetRenderer,
      visualIntentId: visualId,
      narrationIntentId: narrationId,
      timingId
    });

    narrationIntents.push({
      schemaVersion: "1.0",
      id: narrationId,
      goal: section.learningObjective,
      audienceLevel: outline.targetAudience,
      explanationStyle: inferExplanationStyle(sceneType),
      emphasisPoints: section.keyPoints
    });

    visualIntents.push({
      schemaVersion: "1.0",
      id: visualId,
      primaryObjects,
      visualPattern: inferVisualPattern(sceneType),
      highlightTargets: deriveHighlightTargets(sceneType, primaryObjects),
      motionType: inferMotionType(sceneType),
      diagramStyle: inferDiagramStyle(sceneType, targetRenderer)
    });

    timings.push({
      schemaVersion: "1.0",
      id: timingId,
      estimatedDurationSec: section.estimatedDurationSec,
      beatPoints: buildBeatPoints(section.estimatedDurationSec),
      syncTargets: [narrationId]
    });
  });

  return {
    schemaVersion: "1.0",
    id: storyboardId,
    outlineId,
    topic: outline.topic,
    domain: outline.domain,
    targetAudience: outline.targetAudience,
    contentType: outline.contentType,
    scenes,
    narrationIntents,
    visualIntents,
    timings,
    totalEstimatedDurationSec: outline.sections.reduce(
      (total, section) => total + section.estimatedDurationSec,
      0
    )
  };
}
