export type ControlLoop = {
  schemaVersion: "1.0";
  id: string;
  controlledVariable: string;
  manipulatedVariable: string;
  feedbackSource: string;
  constraints?: string[];
  explanationNotes?: string[];
};
