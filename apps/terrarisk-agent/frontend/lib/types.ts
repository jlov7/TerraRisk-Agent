export type AnalysisMode = "cloud" | "byo_bigquery" | "offline";

export interface ArtifactMetadata {
  filename?: string;
  size_bytes?: number;
  download_url?: string;
  [key: string]: unknown;
}

export interface Artifact {
  uri: string;
  type: string;
  hash?: string | null;
  metadata?: ArtifactMetadata;
}

export interface PlannerStep {
  id: string;
  description: string;
  source: string;
  inputs: string[];
  parameters?: Record<string, unknown>;
}

export interface ActionCredential {
  id: string;
  version?: string;
  timestamp: string;
  actor?: Record<string, unknown>;
  action: {
    type: string;
    inputs: string[];
    outputs: string[];
    source: { system: string; reference: string; mode?: string | null };
  };
  artifacts?: Artifact[];
  claims?: { name?: string; value?: string }[];
  signatures?: Record<string, unknown>[];
  trace?: Record<string, unknown> | null;
}

export interface AnalysisResponse {
  run_id: string;
  steps: PlannerStep[];
  artifacts: Artifact[];
  action_credentials: ActionCredential[];
  highlights?: string[];
  sources?: string[];
}
