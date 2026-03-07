export type Entity = {
  id: string;
  name: string;
  type: string;
  attributes?: Record<string, unknown>;
  components?: string[];
  domainTags?: string[];
};
