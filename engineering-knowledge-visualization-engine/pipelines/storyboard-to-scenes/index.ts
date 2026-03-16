import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

import { NarrationIntent, Scene, SceneManifest, Timing, VisualIntent } from "@repo/schemas";

import type { Storyboard } from "../outline-to-storyboard/index";

function slugify(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .replace(/-{2,}/g, "-");
}

function indexById<T extends { id: string }>(items: T[]): Map<string, T> {
  return new Map(items.map((item) => [item.id, item]));
}

function requireReference<T extends { id: string }>(
  map: Map<string, T>,
  id: string | undefined,
  sceneId: string,
  label: string
): T {
  if (!id) {
    throw new Error(`Scene '${sceneId}' is missing ${label} reference`);
  }

  const value = map.get(id);
  if (!value) {
    throw new Error(`Scene '${sceneId}' references missing ${label} '${id}'`);
  }

  return value;
}

function extractSceneSlug(scene: Scene): string {
  const prefix = `scene-${String(scene.order).padStart(2, "0")}-`;
  if (scene.id.startsWith(prefix)) {
    return scene.id.slice(prefix.length);
  }

  return slugify(scene.title);
}

export function storyboardToSceneManifests(storyboard: Storyboard): SceneManifest[] {
  const narrationById = indexById<NarrationIntent>(storyboard.narrationIntents);
  const visualById = indexById<VisualIntent>(storyboard.visualIntents);
  const timingById = indexById<Timing>(storyboard.timings);

  return [...storyboard.scenes]
    .sort((left, right) => left.order - right.order)
    .map((scene) => {
      const narration = requireReference(
        narrationById,
        scene.narrationIntentId,
        scene.id,
        "narrationIntentId"
      );
      const visual = requireReference(visualById, scene.visualIntentId, scene.id, "visualIntentId");
      const timing = requireReference(timingById, scene.timingId, scene.id, "timingId");
      const slug = extractSceneSlug(scene);

      return {
        schemaVersion: "1.0",
        id: scene.id,
        fileName: `${scene.id}.json`,
        order: scene.order,
        slug,
        title: scene.title,
        topic: storyboard.topic,
        domain: storyboard.domain,
        targetAudience: storyboard.targetAudience,
        contentType: storyboard.contentType,
        sceneType: scene.sceneType,
        targetRenderer: scene.targetRenderer,
        source: {
          outlineId: storyboard.outlineId,
          storyboardId: storyboard.id,
          sectionId: scene.sourceSectionId
        },
        narration: {
          goal: narration.goal,
          audienceLevel: narration.audienceLevel,
          explanationStyle: narration.explanationStyle,
          emphasisPoints: narration.emphasisPoints
        },
        visual: {
          primaryObjects: visual.primaryObjects,
          visualPattern: visual.visualPattern,
          highlightTargets: visual.highlightTargets,
          motionType: visual.motionType,
          diagramStyle: visual.diagramStyle
        },
        timing: {
          estimatedDurationSec: timing.estimatedDurationSec,
          beatPoints: timing.beatPoints,
          syncTargets: timing.syncTargets
        }
      };
    });
}

export async function writeSceneManifests(
  sceneManifests: SceneManifest[],
  outputDir: string
): Promise<string[]> {
  await mkdir(outputDir, { recursive: true });

  const filePaths = sceneManifests.map((sceneManifest) => join(outputDir, sceneManifest.fileName));

  await Promise.all(
    sceneManifests.map((sceneManifest, index) => {
      const payload = `${JSON.stringify(sceneManifest, null, 2)}\n`;
      return writeFile(filePaths[index], payload, "utf8");
    })
  );

  return filePaths;
}
