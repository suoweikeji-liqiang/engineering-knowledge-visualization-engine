export type VisualIntent = {
  schemaVersion: "1.0";
  id: string;
  primaryObjects: string[];
  visualPattern?: string;
  highlightTargets?: string[];
  motionType?: string;
  diagramStyle?: string;
};
