export type Timing = {
  schemaVersion: "1.0";
  id: string;
  estimatedDurationSec: number;
  beatPoints?: number[];
  syncTargets?: string[];
};
