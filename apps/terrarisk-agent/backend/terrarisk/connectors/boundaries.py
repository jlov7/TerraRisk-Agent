from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import geojson


@dataclass
class BoundaryProvider:
    """Simple in-memory boundary provider for offline demos."""

    def county_feature(self, county_fips: str) -> dict[str, Any]:
        # Placeholder geometry (point) for offline usage.
        feature = geojson.Feature(
            geometry=geojson.Point((-95.7129, 37.0902)),
            properties={"county_fips": county_fips, "name": "Synthetic County"},
        )
        return feature.__geo_interface__  # type: ignore[attr-defined]
