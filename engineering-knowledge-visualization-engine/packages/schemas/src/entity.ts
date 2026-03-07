export type Entity = {
  schemaVersion: "1.0";
  id: string;
  name: string;
  type: string;
  attributes?: Record<string, unknown>;
  components?: string[];
  domainTags?: string[];
};
