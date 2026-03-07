export type TopicInput = {
  title: string;
  domain: string;
  targetAudience: "beginner" | "intermediate" | "advanced";
  contentType: "equipment-principle" | "system-flow" | "control-algorithm";
};

export type OutlineSection = {
  id: string;
  title: string;
  learningObjective: string;
  keyPoints: string[];
  estimatedDurationSec: number;
};

export type Outline = {
  schemaVersion: "1.0";
  topic: string;
  domain: string;
  targetAudience: string;
  contentType: string;
  sections: OutlineSection[];
  totalEstimatedDurationSec: number;
};

export function topicToOutline(input: TopicInput): Outline {
  // Stub implementation - returns structured outline
  return {
    schemaVersion: "1.0",
    topic: input.title,
    domain: input.domain,
    targetAudience: input.targetAudience,
    contentType: input.contentType,
    sections: [
      {
        id: "section-01",
        title: "Introduction",
        learningObjective: `Understand what ${input.title} is and why it matters`,
        keyPoints: ["Definition", "Purpose", "Context"],
        estimatedDurationSec: 30
      },
      {
        id: "section-02",
        title: "Core Concept",
        learningObjective: `Learn the fundamental principle of ${input.title}`,
        keyPoints: ["Main components", "Working principle", "Key relationships"],
        estimatedDurationSec: 60
      },
      {
        id: "section-03",
        title: "Summary",
        learningObjective: "Recap key takeaways",
        keyPoints: ["Main points review", "Practical implications"],
        estimatedDurationSec: 20
      }
    ],
    totalEstimatedDurationSec: 110
  };
}
