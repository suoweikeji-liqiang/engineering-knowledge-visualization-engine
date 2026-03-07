export type TeachingPattern = {
  id: string;
  name: string;
  contentType: "equipment-principle" | "system-flow" | "control-algorithm";
  structure: string[];
  visualApproach: string;
  narrationApproach: string;
  commonPitfalls?: string[];
};

export const HVAC_TEACHING_PATTERNS: TeachingPattern[] = [
  {
    id: "equipment-principle-pattern",
    name: "Equipment Principle Explanation",
    contentType: "equipment-principle",
    structure: [
      "State the purpose and context",
      "Show the main components",
      "Explain the working principle",
      "Demonstrate the cycle or process",
      "Highlight key relationships"
    ],
    visualApproach: "Start with complete equipment, then isolate and highlight components sequentially, animate the process flow",
    narrationApproach: "Begin with why it matters, use simple analogies, build from familiar to technical",
    commonPitfalls: [
      "Showing all components at once without context",
      "Starting with technical details before establishing purpose",
      "Skipping the 'why' to jump to 'how'"
    ]
  },
  {
    id: "system-flow-pattern",
    name: "System Flow Explanation",
    contentType: "system-flow",
    structure: [
      "Show the complete system overview",
      "Identify the main flow path",
      "Trace the flow step by step",
      "Explain energy or mass transfer at each stage",
      "Show return path and cycle completion"
    ],
    visualApproach: "Use flow animation with directional indicators, highlight active components as flow passes through, show state changes",
    narrationApproach: "Follow the flow chronologically, explain what happens at each stage, emphasize cause and effect",
    commonPitfalls: [
      "Showing bidirectional flows simultaneously causing confusion",
      "Not clearly indicating flow direction",
      "Skipping the return path in循环 systems"
    ]
  },
  {
    id: "control-algorithm-pattern",
    name: "Control Algorithm Explanation",
    contentType: "control-algorithm",
    structure: [
      "Define the control objective",
      "Identify controlled and manipulated variables",
      "Show the feedback mechanism",
      "Explain the control logic",
      "Demonstrate response to disturbances"
    ],
    visualApproach: "Use block diagrams, show signal flow, animate controller response, plot variables over time",
    narrationApproach: "Start with the goal, explain the problem being solved, build intuition before equations, show behavior patterns",
    commonPitfalls: [
      "Introducing equations before intuition",
      "Not showing what happens without control",
      "Skipping the feedback path visualization"
    ]
  }
];
