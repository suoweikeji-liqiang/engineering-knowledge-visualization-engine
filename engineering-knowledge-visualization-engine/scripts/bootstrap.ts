const { existsSync } = require("node:fs");
const { join } = require("node:path");

const workspaceDirs = [
  "apps/cli",
  "apps/studio",
  "packages/schemas",
  "packages/core",
  "packages/domain-hvac",
  "packages/generator-manim",
  "packages/composer-remotion",
  "packages/voice",
  "packages/utils"
];

const missingManifests = workspaceDirs.filter((dir) => {
  return !existsSync(join(process.cwd(), dir, "package.json"));
});

if (missingManifests.length > 0) {
  console.error("Workspace manifest check failed.");
  missingManifests.forEach((dir) => {
    console.error(`- Missing package.json in ${dir}`);
  });
  process.exit(1);
}

console.log("Workspace manifest check passed.");
console.log("Run `pnpm install` to install dependencies, then `pnpm typecheck` to verify the baseline.");
