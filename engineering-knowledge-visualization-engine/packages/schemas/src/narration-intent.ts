export type NarrationIntent = {
  id: string;
  goal: string;
  audienceLevel?: "beginner" | "intermediate" | "advanced";
  explanationStyle?: string;
  emphasisPoints?: string[];
};
