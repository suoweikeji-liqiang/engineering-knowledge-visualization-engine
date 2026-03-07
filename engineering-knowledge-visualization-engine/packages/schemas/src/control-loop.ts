export type ControlLoop = {
  id: string;
  controlledVariable: string;
  manipulatedVariable: string;
  feedbackSource: string;
  constraints?: string[];
  explanationNotes?: string[];
};
