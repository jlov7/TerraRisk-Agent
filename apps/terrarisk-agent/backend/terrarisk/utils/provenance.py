from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from ..config import get_settings
from ..models.domain import ActionCredential, Artifact


def load_schema() -> dict[str, Any]:
    settings = get_settings()
    schema_path = Path(settings.action_credential_schema_path)
    if schema_path.exists():
        return json.loads(schema_path.read_text())
    return {}


def create_action_credential(
    *,
    action_type: str,
    inputs: Sequence[str],
    outputs: Sequence[str],
    source: str,
    artifacts: Sequence[Artifact],
    claims: Sequence[dict[str, Any]] | None = None,
    mode: str | None = None,
) -> ActionCredential:
    claims = claims or []
    credential = ActionCredential(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
        actor={"name": "TerraRisk Agent", "role": "system"},
        action={
            "type": action_type,
            "inputs": list(inputs),
            "outputs": list(outputs),
            "source": {"system": source, "reference": source, "mode": mode},
        },
        artifacts=list(artifacts),
        claims=claims,
        signatures=[],
        trace=None,
    )
    return credential
