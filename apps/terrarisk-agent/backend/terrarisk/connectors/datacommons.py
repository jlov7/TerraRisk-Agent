from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class DataCommonsClient:
    base_url: str = "https://api.datacommons.org"

    async def fetch_population(self, place_dcid: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/stat/series",
                params={"stat_var": "Count_Person", "place": place_dcid},
            )
            response.raise_for_status()
            payload = response.json()
            return payload
