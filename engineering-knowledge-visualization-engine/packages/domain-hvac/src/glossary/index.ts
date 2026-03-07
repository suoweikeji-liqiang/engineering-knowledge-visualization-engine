export type GlossaryEntry = {
  term: string;
  definition: string;
  category: string;
  relatedTerms?: string[];
  notes?: string;
};

export const HVAC_GLOSSARY: GlossaryEntry[] = [
  {
    term: "Chiller",
    definition: "A refrigeration machine that removes heat from a liquid (typically water) via a vapor-compression or absorption cycle",
    category: "equipment",
    relatedTerms: ["evaporator", "compressor", "condenser", "refrigerant"],
    notes: "Central equipment in chilled water systems"
  },
  {
    term: "Evaporator",
    definition: "Heat exchanger where refrigerant absorbs heat from chilled water, causing the refrigerant to evaporate",
    category: "component",
    relatedTerms: ["chiller", "refrigerant", "heat-exchanger"]
  },
  {
    term: "Compressor",
    definition: "Device that increases refrigerant pressure and temperature, enabling heat rejection at the condenser",
    category: "component",
    relatedTerms: ["chiller", "refrigerant", "condenser"]
  },
  {
    term: "Condenser",
    definition: "Heat exchanger where high-pressure refrigerant rejects heat to cooling water or air, causing condensation",
    category: "component",
    relatedTerms: ["chiller", "refrigerant", "cooling-tower"]
  },
  {
    term: "Expansion Valve",
    definition: "Device that reduces refrigerant pressure, enabling evaporation at low temperature",
    category: "component",
    relatedTerms: ["chiller", "refrigerant", "evaporator"]
  },
  {
    term: "Refrigerant",
    definition: "Working fluid in refrigeration cycle that absorbs and rejects heat through phase changes",
    category: "substance",
    relatedTerms: ["chiller", "evaporator", "condenser"]
  },
  {
    term: "Chilled Water Loop",
    definition: "Closed piping system that circulates chilled water from chiller to cooling loads and back",
    category: "system",
    relatedTerms: ["chiller", "pump", "ahu", "cooling-coil"]
  },
  {
    term: "AHU",
    definition: "Air Handling Unit - equipment that conditions and circulates air, often using chilled water cooling coils",
    category: "equipment",
    relatedTerms: ["chilled-water-loop", "cooling-coil", "fan"]
  },
  {
    term: "Cooling Coil",
    definition: "Heat exchanger in AHU where chilled water absorbs heat from air",
    category: "component",
    relatedTerms: ["ahu", "chilled-water-loop", "heat-exchanger"]
  },
  {
    term: "Primary Pump",
    definition: "Pump that circulates chilled water through the primary loop between chiller and distribution system",
    category: "component",
    relatedTerms: ["chilled-water-loop", "chiller", "secondary-pump"]
  },
  {
    term: "PID Controller",
    definition: "Proportional-Integral-Derivative controller that adjusts control output based on error, error accumulation, and error rate of change",
    category: "control",
    relatedTerms: ["control-loop", "setpoint", "feedback"]
  },
  {
    term: "Setpoint",
    definition: "Target value for a controlled variable that the control system attempts to maintain",
    category: "control",
    relatedTerms: ["pid-controller", "control-loop", "error"]
  },
  {
    term: "Controlled Variable",
    definition: "Process variable that the control system measures and regulates (e.g., temperature, pressure)",
    category: "control",
    relatedTerms: ["control-loop", "setpoint", "sensor"]
  },
  {
    term: "Manipulated Variable",
    definition: "Control output that is adjusted to influence the controlled variable (e.g., valve position, motor speed)",
    category: "control",
    relatedTerms: ["control-loop", "actuator", "pid-controller"]
  },
  {
    term: "Proportional Gain",
    definition: "PID parameter that determines control response proportional to current error",
    category: "control",
    relatedTerms: ["pid-controller", "integral-gain", "derivative-gain"]
  },
  {
    term: "Integral Gain",
    definition: "PID parameter that eliminates steady-state error by accumulating error over time",
    category: "control",
    relatedTerms: ["pid-controller", "proportional-gain", "derivative-gain"]
  },
  {
    term: "Derivative Gain",
    definition: "PID parameter that dampens oscillations by responding to rate of error change",
    category: "control",
    relatedTerms: ["pid-controller", "proportional-gain", "integral-gain"]
  }
];
