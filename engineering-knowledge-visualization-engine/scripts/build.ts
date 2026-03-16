const { spawnSync } = require("node:child_process");

const command = process.platform === "win32" ? "pnpm.cmd" : "pnpm";
const result = spawnSync(command, ["typecheck"], { stdio: "inherit" });

if (result.status !== 0) {
  process.exit(result.status ?? 1);
}
