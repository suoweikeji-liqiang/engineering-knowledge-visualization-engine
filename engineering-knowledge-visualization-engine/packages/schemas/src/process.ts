export type Process = {
  schemaVersion: "1.0";
  id: string;
  name: string;
  steps: string[];
  inputs?: string[];
  outputs?: string[];
  causalNotes?: string[];
};
