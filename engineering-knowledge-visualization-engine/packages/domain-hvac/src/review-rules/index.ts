export type ReviewRule = {
  id: string;
  category: "terminology" | "flow" | "causality" | "control" | "simplification";
  rule: string;
  checkFor: string[];
  examples?: { incorrect: string; correct: string }[];
};

export const HVAC_REVIEW_RULES: ReviewRule[] = [
  {
    id: "term-chiller-vs-cooler",
    category: "terminology",
    rule: "Use 'chiller' for refrigeration-based cooling, not 'cooler'",
    checkFor: ["cooler", "cooling machine"],
    examples: [
      {
        incorrect: "The cooler removes heat from water",
        correct: "The chiller removes heat from water"
      }
    ]
  },
  {
    id: "term-refrigerant-vs-coolant",
    category: "terminology",
    rule: "Use 'refrigerant' for the working fluid in refrigeration cycle, 'chilled water' for the secondary fluid",
    checkFor: ["coolant in evaporator", "refrigerant in coils"],
    examples: [
      {
        incorrect: "Coolant evaporates in the evaporator",
        correct: "Refrigerant evaporates in the evaporator"
      }
    ]
  },
  {
    id: "flow-direction-consistency",
    category: "flow",
    rule: "Flow direction must be consistent throughout diagrams and animations",
    checkFor: ["reversed arrows", "contradictory flow paths"],
    examples: [
      {
        incorrect: "Chilled water flows from AHU to chiller",
        correct: "Chilled water flows from chiller to AHU, returns warmed"
      }
    ]
  },
  {
    id: "flow-return-path",
    category: "flow",
    rule: "Always show return path in循环 systems",
    checkFor: ["missing return line", "open-ended flow"],
    examples: [
      {
        incorrect: "Show only supply line from chiller to AHU",
        correct: "Show both supply and return lines forming complete loop"
      }
    ]
  },
  {
    id: "causal-heat-flow",
    category: "causality",
    rule: "Heat flows from high temperature to low temperature",
    checkFor: ["heat flowing uphill", "spontaneous cooling without work input"],
    examples: [
      {
        incorrect: "Chiller cools water without energy input",
        correct: "Chiller uses compressor work to move heat from cold to hot"
      }
    ]
  },
  {
    id: "causal-pressure-flow",
    category: "causality",
    rule: "Fluid flows from high pressure to low pressure",
    checkFor: ["flow against pressure gradient", "pump on wrong side"],
    examples: [
      {
        incorrect: "Water flows without pump or pressure difference",
        correct: "Pump creates pressure difference driving flow"
      }
    ]
  },
  {
    id: "control-feedback-path",
    category: "control",
    rule: "Control loops must show feedback path from sensor to controller",
    checkFor: ["missing sensor", "no feedback connection", "open-loop labeled as closed-loop"],
    examples: [
      {
        incorrect: "Controller adjusts valve without measuring temperature",
        correct: "Sensor measures temperature, controller compares to setpoint, adjusts valve"
      }
    ]
  },
  {
    id: "control-variable-clarity",
    category: "control",
    rule: "Clearly distinguish controlled variable from manipulated variable",
    checkFor: ["confusing what is measured vs what is adjusted"],
    examples: [
      {
        incorrect: "Control the valve position to maintain valve position",
        correct: "Control the temperature by adjusting valve position"
      }
    ]
  },
  {
    id: "simplification-phase-change",
    category: "simplification",
    rule: "When simplifying refrigeration cycle, acknowledge that phase change is critical",
    checkFor: ["omitting evaporation/condensation", "treating as simple heat pump"],
    examples: [
      {
        incorrect: "Refrigerant just moves heat around",
        correct: "Refrigerant absorbs heat during evaporation, rejects heat during condensation"
      }
    ]
  },
  {
    id: "simplification-energy-conservation",
    category: "simplification",
    rule: "Do not imply free cooling or perpetual motion",
    checkFor: ["missing energy input", "efficiency > 100%", "no work required"],
    examples: [
      {
        incorrect: "Chiller produces cooling without energy cost",
        correct: "Chiller requires electrical energy to drive compressor"
      }
    ]
  }
];
