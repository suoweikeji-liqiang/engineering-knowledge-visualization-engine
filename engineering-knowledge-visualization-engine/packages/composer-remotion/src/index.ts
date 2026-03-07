export type CompositionConfig = {
  outputPath: string;
  fps: number;
  width: number;
  height: number;
};

export class RemotionComposer {
  constructor(private config: CompositionConfig) {}

  async composeVideo(sceneVideos: string[], audioPath?: string): Promise<string> {
    // Stub: returns path to composed video
    return this.config.outputPath;
  }
}
