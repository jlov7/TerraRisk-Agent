from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

DEFAULT_COLUMNS = [
    "state",
    "county",
    "county_fips",
    "hazard_type",
    "expected_annual_loss",
    "population",
    "resilience_index",
]


@dataclass
class NRILoader:
    source_path: Path | None = None

    def load(self, columns: Iterable[str] | None = None) -> pd.DataFrame:
        usecols = list(columns) if columns else DEFAULT_COLUMNS
        if not self.source_path:
            # Return empty DataFrame when no source path is provided; offline demos inject fixtures.
            return pd.DataFrame(columns=usecols)
        frame = pd.read_csv(self.source_path, usecols=usecols)
        frame["county_fips"] = frame["county_fips"].astype(str).str.zfill(5)
        frame["hazard_type"] = frame["hazard_type"].str.lower()
        frame = frame.rename(columns={"expected_annual_loss": "eal"})
        return frame

    def hazards_for_county(self, county_fips: str) -> pd.DataFrame:
        frame = self.load()
        return frame[frame["county_fips"] == county_fips]
