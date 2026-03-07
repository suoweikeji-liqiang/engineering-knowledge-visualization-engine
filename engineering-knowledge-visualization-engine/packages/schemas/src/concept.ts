export type Concept = {
  schemaVersion: "1.0";
  id: string;
  name: string;
  description?: string;
  prerequisites?: string[];
  relatedConcepts?: string[];
};
