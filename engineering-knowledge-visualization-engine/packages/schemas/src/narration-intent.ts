export type NarrationIntent = {
  schemaVersion: "1.0";
  id: string;
  goal: string;
  audienceLevel?: "beginner" | "intermediate" | "advanced";
  explanationStyle?: string;
  emphasisPoints?: string[];
};
