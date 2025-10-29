"use client";

import axios from "axios";
import type { AnalysisMode, AnalysisResponse } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function submitAnalysis(
  params: {
    query: string;
    hazards: string[];
    geographyFilter: string[];
    mode: AnalysisMode;
    portfolioReference?: string;
  }
): Promise<AnalysisResponse> {
  const payload = {
    query: params.query,
    hazards: params.hazards,
    geography_filter: params.geographyFilter,
    mode: params.mode,
    portfolio_reference: params.portfolioReference ?? null
  };
  const response = await axios.post<AnalysisResponse>(
    `${API_BASE_URL}/analyze`,
    payload,
    { headers: { "Content-Type": "application/json" } }
  );
  return response.data;
}
