import { Scene } from "@repo/schemas";

export type ManimGeneratorConfig = {
  outputDir: string;
  quality: "low" | "medium" | "high";
};

export class ManimGenerator {
  constructor(private config: ManimGeneratorConfig) {}

  async generateScene(scene: Scene): Promise<string> {
    // Stub: returns path to generated Python script
    const scriptPath = `${this.config.outputDir}/${scene.id}.py`;
    return scriptPath;
  }
}
