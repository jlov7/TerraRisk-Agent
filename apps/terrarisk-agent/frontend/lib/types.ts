export type AnalysisMode = "cloud" | "byo_bigquery" | "offline";

export interface Artifact {
  uri: string;
  type: string;
  hash?: string | null;
  metadata?: Record<string, unknown>;
}

export interface PlannerStep {
  id: string;
  description: string;
  source: string;
  inputs: string[];
}

export interface ActionCredential {
  id: string;
  action: {
    type: string;
    inputs: string[];
    outputs: string[];
    source: { system: string; reference: string; mode?: string | null };
  };
  timestamp: string;
}

export interface AnalysisResponse {
  run_id: string;
  steps: PlannerStep[];
  artifacts: Artifact[];
  action_credentials: ActionCredential[];
}
