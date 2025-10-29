"use client";

import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { MapPreview } from "../components/MapPreview";
import { submitAnalysis } from "../lib/api";
import type { AnalysisMode, AnalysisResponse } from "../lib/types";

const hazardOptions = [
  { label: "Hurricane", value: "hurricane" },
  { label: "Flood", value: "flood" },
  { label: "Wildfire", value: "wildfire" }
];

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

  return (
    <main style={{ padding: "2rem", display: "grid", gap: "2rem" }}>
      <section style={{ background: "#ffffff", borderRadius: "16px", padding: "1.5rem" }}>
        <h1 style={{ marginTop: 0 }}>TerraRisk Agent</h1>
        <p style={{ color: "#4b5563" }}>
          Personal passion R&D build that pairs synthetic Google Earth AI plans with NRI and BigQuery templates.
        </p>
        <form onSubmit={handleSubmit} style={{ display: "grid", gap: "1rem" }}>
          <label>
            Query
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              rows={3}
              style={{ width: "100%", marginTop: "0.5rem" }}
            />
          </label>
          <fieldset style={{ border: "1px solid #e5e7eb", borderRadius: "12px", padding: "1rem" }}>
            <legend>Hazards</legend>
            <div style={{ display: "flex", gap: "1rem" }}>
              {hazardOptions.map((option) => (
                <label key={option.value} style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                  <input
                    type="checkbox"
                    checked={hazards.includes(option.value)}
                    onChange={() => toggleHazard(option.value)}
                  />
                  {option.label}
                </label>
              ))}
            </div>
          </fieldset>
          <label>
            Mode
            <select
              value={mode}
              onChange={(event) => setMode(event.target.value as AnalysisMode)}
              style={{ marginLeft: "0.75rem" }}
            >
              <option value="cloud">Cloud (Earth AI + BigQuery)</option>
              <option value="byo_bigquery">BYO GCP BigQuery</option>
              <option value="offline">Offline demo</option>
            </select>
          </label>
          <button
            type="submit"
            disabled={mutation.isPending}
            style={{
              width: "fit-content",
              background: "#1b4d89",
              color: "white",
              padding: "0.75rem 1.5rem",
              borderRadius: "999px",
              border: "none"
            }}
          >
            {mutation.isPending ? "Running..." : "Run analysis"}
          </button>
        </form>
        {mutation.isError && (
          <p style={{ color: "#dc2626" }}>Unable to reach the backend right now.</p>
        )}
      </section>
      <section style={{ display: "grid", gap: "1.5rem" }}>
        <div style={{ background: "#ffffff", borderRadius: "16px", padding: "1.5rem" }}>
          <h2 style={{ marginTop: 0 }}>Geospatial view</h2>
          <MapPreview geojsonUrl={latestResponse?.artifacts.find((artifact) => artifact.type === "application/geo+json")?.uri} />
        </div>
        <div style={{ background: "#ffffff", borderRadius: "16px", padding: "1.5rem" }}>
          <h2 style={{ marginTop: 0 }}>Generated deliverables</h2>
          {latestResponse ? (
            <ul>
              {latestResponse.artifacts.map((artifact) => (
                <li key={artifact.uri}>
                  <code>{artifact.type}</code> — {artifact.uri}
                </li>
              ))}
            </ul>
          ) : (
            <p>No analysis run yet. Offline fixtures mirror the backend demo.</p>
          )}
        </div>
      </section>
    </main>
  );
}
