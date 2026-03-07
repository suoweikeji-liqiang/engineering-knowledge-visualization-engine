export type Concept = {
  id: string;
  name: string;
  description?: string;
  prerequisites?: string[];
  relatedConcepts?: string[];
};
