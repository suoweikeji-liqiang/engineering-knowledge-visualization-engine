import { Entity } from "@repo/schemas";

export const HVAC_ENTITIES: Entity[] = [
  {
    schemaVersion: "1.0",
    id: "chiller-centrifugal",
    name: "Centrifugal Chiller",
    type: "equipment",
    attributes: {
      principle: "vapor-compression",
      compressorType: "centrifugal",
      typicalCapacity: "200-2000 tons"
    },
    components: ["evaporator", "compressor", "condenser", "expansion-valve"],
    domainTags: ["hvac", "cooling", "chiller"]
  },
  {
    schemaVersion: "1.0",
    id: "evaporator",
    name: "Evaporator",
    type: "component",
    attributes: {
      function: "heat-absorption",
      phaseChange: "liquid-to-vapor"
    },
    domainTags: ["hvac", "heat-exchanger", "refrigeration"]
  },
  {
    schemaVersion: "1.0",
    id: "compressor",
    name: "Compressor",
    type: "component",
    attributes: {
      function: "pressure-increase",
      energyInput: "electrical"
    },
    domainTags: ["hvac", "refrigeration", "mechanical"]
  },
  {
    schemaVersion: "1.0",
    id: "condenser",
    name: "Condenser",
    type: "component",
    attributes: {
      function: "heat-rejection",
      phaseChange: "vapor-to-liquid"
    },
    domainTags: ["hvac", "heat-exchanger", "refrigeration"]
  },
  {
    schemaVersion: "1.0",
    id: "expansion-valve",
    name: "Expansion Valve",
    type: "component",
    attributes: {
      function: "pressure-reduction",
      controlType: "thermostatic or electronic"
    },
    domainTags: ["hvac", "refrigeration", "control"]
  },
  {
    schemaVersion: "1.0",
    id: "chilled-water-pump",
    name: "Chilled Water Pump",
    type: "component",
    attributes: {
      function: "fluid-circulation",
      driveType: "variable-speed or constant-speed"
    },
    domainTags: ["hvac", "hydronic", "mechanical"]
  },
  {
    schemaVersion: "1.0",
    id: "ahu",
    name: "Air Handling Unit",
    type: "equipment",
    attributes: {
      function: "air-conditioning",
      typicalComponents: ["fan", "cooling-coil", "heating-coil", "filter"]
    },
    components: ["fan", "cooling-coil", "filter"],
    domainTags: ["hvac", "air-side", "terminal"]
  },
  {
    schemaVersion: "1.0",
    id: "cooling-coil",
    name: "Cooling Coil",
    type: "component",
    attributes: {
      function: "air-cooling",
      heatTransferMedium: "chilled-water"
    },
    domainTags: ["hvac", "heat-exchanger", "air-side"]
  },
  {
    schemaVersion: "1.0",
    id: "temperature-sensor",
    name: "Temperature Sensor",
    type: "component",
    attributes: {
      function: "measurement",
      outputType: "analog or digital signal"
    },
    domainTags: ["hvac", "control", "sensor"]
  },
  {
    schemaVersion: "1.0",
    id: "control-valve",
    name: "Control Valve",
    type: "component",
    attributes: {
      function: "flow-modulation",
      actuatorType: "electric or pneumatic"
    },
    domainTags: ["hvac", "control", "actuator"]
  }
];
