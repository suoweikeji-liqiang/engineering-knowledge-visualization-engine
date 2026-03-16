import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";

import { outlineToStoryboard } from "../pipelines/outline-to-storyboard/index";
import {
  storyboardToSceneManifests,
  writeSceneManifests
} from "../pipelines/storyboard-to-scenes/index";

const EXAMPLE_IDS = [
  "hvac-chiller-basics",
  "hvac-chilled-water-loop",
  "hvac-pid-intro"
] as const;

async function generateArtifactsForExample(exampleId: string): Promise<void> {
  const exampleDir = join(process.cwd(), "examples", exampleId);
  const outlinePath = join(exampleDir, "outline", "outline.json");
  const storyboardDir = join(exampleDir, "storyboard");
  const scenesDir = join(exampleDir, "scenes");

  const outline = JSON.parse(await readFile(outlinePath, "utf8"));
  const storyboard = outlineToStoryboard(outline);
  const sceneManifests = storyboardToSceneManifests(storyboard);

  await mkdir(storyboardDir, { recursive: true });
  await writeFile(
    join(storyboardDir, "storyboard.json"),
    `${JSON.stringify(storyboard, null, 2)}\n`,
    "utf8"
  );
  await writeSceneManifests(sceneManifests, scenesDir);

  console.log(`Generated ${sceneManifests.length} scene manifests for ${exampleId}`);
}

async function main(): Promise<void> {
  for (const exampleId of EXAMPLE_IDS) {
    await generateArtifactsForExample(exampleId);
  }
}

main().catch((error) => {
  console.error("Failed to generate example artifacts.");
  console.error(error);
  process.exit(1);
});
