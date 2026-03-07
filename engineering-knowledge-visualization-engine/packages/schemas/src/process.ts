export type Process = {
  id: string;
  name: string;
  steps: string[];
  inputs?: string[];
  outputs?: string[];
  causalNotes?: string[];
};
