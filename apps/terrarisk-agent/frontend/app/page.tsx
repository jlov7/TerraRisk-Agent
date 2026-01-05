"use client";

import { useMutation } from "@tanstack/react-query";
import { useMemo, useState, type CSSProperties } from "react";
import { MapPreview } from "../components/MapPreview";
import { resolveApiUrl, submitAnalysis } from "../lib/api";
import type { AnalysisMode, AnalysisResponse, Artifact } from "../lib/types";

const hazardOptions = [
  { label: "Hurricane", value: "hurricane", color: "#f97316" },
  { label: "Flood", value: "flood", color: "#2563eb" },
  { label: "Wildfire", value: "wildfire", color: "#dc2626" }
];

const modeOptions: Array<{
  value: AnalysisMode;
  label: string;
  description: string;
}> = [
  {
    value: "offline",
    label: "Offline demo",
    description: "Synthetic fixtures, zero cloud credentials."
  },
  {
    value: "byo_bigquery",
    label: "BYO BigQuery",
    description: "Use your own dataset with stubbed Earth AI."
  },
  {
    value: "cloud",
    label: "Cloud mode",
    description: "Earth AI + BigQuery live (access required)."
  }
];

const promptPresets = [
  {
    title: "Gulf Coast underwriting watch",
    description: "Rank hurricane + flood exposure across Gulf Coast ZIPs.",
    query: "Rank Gulf Coast ZIPs by hurricane and flood risk for Q3 underwriting.",
    hazards: ["hurricane", "flood"] as string[],
    mode: "offline" as AnalysisMode
  },
  {
    title: "Wildfire mitigation sprint",
    description: "Prioritize wildfire action plans for the Central Valley.",
    query: "Which Central Valley counties need immediate wildfire mitigation this quarter?",
    hazards: ["wildfire"] as string[],
    mode: "offline" as AnalysisMode
  },
  {
    title: "Portfolio flood stress test",
    description: "Stress a demo portfolio against Midwest flood exposure.",
    query: "Stress test demo-portfolio for Midwest flood exposure and resilience gaps.",
    hazards: ["flood"] as string[],
    mode: "offline" as AnalysisMode
  }
];

const governanceHighlights = [
  {
    title: "Policy guardrails",
    description: "OPA bundles enforce deny-by-default, budget caps, and approval gates."
  },
  {
    title: "Audit-grade provenance",
    description: "Every step emits Action Credentials ready for Sigstore signing."
  },
  {
    title: "PII safety",
    description: "County-level geographies only, with opt-in PII expansion."
  },
  {
    title: "Reproducible outputs",
    description: "Artifacts are hashed, stored, and accessible through the API."
  }
];

const artifactLabels: Record<string, string> = {
  "application/pdf": "Mitigation brief",
  "application/geo+json": "GeoJSON layers",
  "text/csv": "Portfolio extracts"
};

function formatTimestamp(timestamp?: string) {
  if (!timestamp) return "Awaiting run";
  const parsed = new Date(timestamp);
  if (Number.isNaN(parsed.getTime())) return timestamp;
  return parsed.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
}

function artifactName(artifact: Artifact) {
  if (artifact.metadata?.filename) return artifact.metadata.filename;
  const segments = artifact.uri.split(/[/\\]/);
  return segments[segments.length - 1] ?? artifact.uri;
}

function artifactUrl(artifact: Artifact) {
  if (artifact.metadata?.download_url) {
    return resolveApiUrl(artifact.metadata.download_url);
  }
  if (artifact.uri.startsWith("http")) {
    return artifact.uri;
  }
  return null;
}

function formatHash(hash?: string | null) {
  if (!hash) return null;
  return `${hash.slice(0, 10)}...${hash.slice(-6)}`;
}

export default function Home() {
  const [query, setQuery] = useState(
    "Which Gulf Coast ZIPs show elevated hurricane and flood risk?"
  );
  const [mode, setMode] = useState<AnalysisMode>("offline");
  const [hazards, setHazards] = useState<string[]>(["hurricane", "flood"]);
  const [latestResponse, setLatestResponse] = useState<AnalysisResponse | null>(null);

  const mutation = useMutation({
    mutationFn: submitAnalysis,
    onSuccess: (data) => {
      setLatestResponse(data);
    }
  });

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    mutation.mutate({
      query,
      hazards,
      geographyFilter: [],
      mode,
      portfolioReference: "demo-portfolio"
    });
  };

  const toggleHazard = (value: string) => {
    setHazards((prev) =>
      prev.includes(value) ? prev.filter((item) => item !== value) : [...prev, value]
    );
  };

  const applyPreset = (preset: (typeof promptPresets)[number]) => {
    setQuery(preset.query);
    setHazards(preset.hazards);
    setMode(preset.mode);
  };

  const hazardSummary = useMemo(() => {
    if (!hazards.length) return "None selected";
    return hazards
      .map((value) => hazardOptions.find((option) => option.value === value)?.label ?? value)
      .join(", ");
  }, [hazards]);

  const runTimestamp = formatTimestamp(
    latestResponse?.action_credentials?.[latestResponse.action_credentials.length - 1]?.timestamp
  );

  const geojsonArtifact = latestResponse?.artifacts.find(
    (artifact) => artifact.type === "application/geo+json"
  );
  const geojsonUrl = geojsonArtifact ? artifactUrl(geojsonArtifact) ?? undefined : undefined;

  return (
    <main className="page">
      <section className="hero">
        <div className="hero__intro fade-rise">
          <div className="hero__badge">TerraRisk Agent</div>
          <h1 className="hero__title">Governance-first geospatial intelligence for climate risk.</h1>
          <p className="hero__subtitle">
            A personal R&amp;D platform that blends Earth AI planning, FEMA NRI data, and
            provenance-first reporting. Every decision is traceable, every artifact is verifiable.
          </p>
          <div className="hero__chips">
            <span className="chip">OPA policy enforcement</span>
            <span className="chip">Action Credentials</span>
            <span className="chip">Signed artifacts</span>
            <span className="chip">Multi-source fusion</span>
          </div>
          <div className="summary-card">
            <div>
              <strong>Latest run</strong>
              <div className="muted">
                {latestResponse ? `Run ${latestResponse.run_id}` : "No analysis run yet"}
              </div>
            </div>
            <div className="summary-grid">
              <div className="summary-item">
                <span>{latestResponse?.steps.length ?? "--"}</span>
                <span>Planner steps</span>
              </div>
              <div className="summary-item">
                <span>{latestResponse?.artifacts.length ?? "--"}</span>
                <span>Artifacts</span>
              </div>
              <div className="summary-item">
                <span>{latestResponse?.action_credentials.length ?? "--"}</span>
                <span>Credentials</span>
              </div>
              <div className="summary-item">
                <span>{hazardSummary}</span>
                <span>Active hazards</span>
              </div>
            </div>
            <div className="muted">Last updated: {runTimestamp}</div>
          </div>
        </div>

        <div className="card fade-rise delay-1">
          <h2 className="card__title">Run a risk analysis</h2>
          <form onSubmit={handleSubmit} className="analysis-form">
            <div className="field">
              <label htmlFor="query">Analysis question</label>
              <textarea
                id="query"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                rows={4}
              />
            </div>
            <div className="field">
              <label>Hazards</label>
              <div className="hazard-grid">
                {hazardOptions.map((option) => (
                  <label
                    key={option.value}
                    className={`hazard-chip ${hazards.includes(option.value) ? "active" : ""}`}
                    style={{ "--chip-color": option.color } as CSSProperties}
                  >
                    <input
                      type="checkbox"
                      checked={hazards.includes(option.value)}
                      onChange={() => toggleHazard(option.value)}
                    />
                    {option.label}
                  </label>
                ))}
              </div>
            </div>
            <div className="field">
              <label>Mode</label>
              <div className="mode-grid">
                {modeOptions.map((option) => (
                  <button
                    type="button"
                    key={option.value}
                    className={`mode-option ${mode === option.value ? "active" : ""}`}
                    onClick={() => setMode(option.value)}
                    aria-pressed={mode === option.value}
                  >
                    <strong>{option.label}</strong>
                    <span>{option.description}</span>
                  </button>
                ))}
              </div>
            </div>
            <button type="submit" disabled={mutation.isPending} className="primary-button">
              {mutation.isPending ? "Running analysis..." : "Run analysis"}
            </button>
            {mutation.isError && (
              <p className="muted">Unable to reach the backend right now.</p>
            )}
          </form>
          <div className="field">
            <label>Quick prompts</label>
            <div className="prompt-grid">
              {promptPresets.map((preset) => (
                <button
                  key={preset.title}
                  type="button"
                  className="prompt-button"
                  onClick={() => applyPreset(preset)}
                >
                  <strong>{preset.title}</strong>
                  <span>{preset.description}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="content-grid">
        <article className="card map-card fade-rise delay-1">
          <h2 className="card__title">Geospatial view</h2>
          <MapPreview geojsonUrl={geojsonUrl} className="map-canvas" />
          <div className="legend">
            {hazardOptions.map((option) => (
              <span key={option.value} style={{ "--chip-color": option.color } as CSSProperties}>
                {option.label}
              </span>
            ))}
          </div>
        </article>

        <article className="card deliverables-card fade-rise delay-2">
          <h2 className="card__title">Deliverables</h2>
          {latestResponse ? (
            <>
              {latestResponse.highlights?.length ? (
                <div className="insight-block">
                  <div className="insight-title">Highlights</div>
                  <ul className="insight-list">
                    {latestResponse.highlights.slice(0, 4).map((highlight) => (
                      <li key={highlight}>{highlight}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
              {latestResponse.sources?.length ? (
                <div className="insight-block">
                  <div className="insight-title">Sources</div>
                  <div className="source-chips">
                    {latestResponse.sources.map((source) => (
                      <span key={source} className="source-chip">
                        {source}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
              <ul className="artifact-list">
                {latestResponse.artifacts.map((artifact) => {
                  const url = artifactUrl(artifact);
                  const displayName = artifactName(artifact);
                  return (
                    <li key={artifact.uri} className="artifact-item">
                      <div className="artifact-item__row">
                        <span className="badge">{artifactLabels[artifact.type] ?? artifact.type}</span>
                        {url ? (
                          <a href={url} className="muted" target="_blank" rel="noreferrer">
                            Download
                          </a>
                        ) : (
                          <span className="muted">Local artifact</span>
                        )}
                      </div>
                      <div>{displayName}</div>
                      <div className="muted">
                        Hash: {formatHash(artifact.hash) ?? "pending"}
                      </div>
                    </li>
                  );
                })}
              </ul>
            </>
          ) : (
            <p className="muted">Run an analysis to generate signed reports and data artifacts.</p>
          )}
        </article>

        <article className="card steps-card fade-rise delay-1">
          <h2 className="card__title">Planner sequence</h2>
          {latestResponse ? (
            <ul className="step-list">
              {latestResponse.steps.map((step) => (
                <li key={step.id} className="step-item">
                  <div className="action-row">
                    <span className="badge">{step.source}</span>
                    <span className="muted">{step.inputs.length} inputs</span>
                  </div>
                  <div>{step.description}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">Planner steps will appear after your first run.</p>
          )}
        </article>

        <article className="card provenance-card fade-rise delay-2">
          <h2 className="card__title">Provenance chain</h2>
          {latestResponse ? (
            <ul className="credential-list">
              {latestResponse.action_credentials.map((credential) => (
                <li key={credential.id} className="credential-item">
                  <div className="action-row">
                    <span className="badge">{credential.action.type}</span>
                    <span className="muted">{credential.action.source.system}</span>
                  </div>
                  <div className="muted">
                    Outputs: {credential.action.outputs.length} | Artifacts:{" "}
                    {credential.artifacts?.length ?? 0}
                  </div>
                  <div className="muted">
                    {formatTimestamp(credential.timestamp)}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">Action Credentials will appear after the analysis completes.</p>
          )}
        </article>
      </section>

      <section className="card card--soft fade-rise delay-2">
        <h2 className="card__title">Governance posture</h2>
        <div className="governance-grid">
          {governanceHighlights.map((item) => (
            <div key={item.title} className="governance-item">
              <h4>{item.title}</h4>
              <p>{item.description}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
