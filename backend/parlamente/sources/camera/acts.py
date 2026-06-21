"""Adapter degli atti Camera (interrogazioni, interpellanze, mozioni, risoluzioni,
ordini del giorno, proposte di legge).

STATO: scaffold reale + loader di fixtures. Gli atti reali sono disponibili via
dati.camera.it (anche SPARQL) ma con classi e relazioni dedicate; per l'MVP
usiamo fixtures reali. Vedi docs/sources-limits.md.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from ...config import get_settings
from ...logging import get_logger
from ...models import Act, Chamber, Politician, SourceType
from ..base import SourceAdapter

logger = get_logger(__name__)


def _acts_fixtures_dir() -> Path:
    return get_settings().fixtures_dir / "camera"


class CameraActsAdapter(SourceAdapter):
    source_name = "Camera dei Deputati — Atti"

    def __init__(self, use_fixtures: bool = True) -> None:
        self.use_fixtures = use_fixtures

    def fetch_politicians(self, legislature: str) -> list[Politician]:
        raise NotImplementedError("Usa CameraDeputiesAdapter per i deputati.")

    def fetch_acts(
        self, since: date | None = None, until: date | None = None
    ) -> list[Act]:
        if not self.use_fixtures:
            raise NotImplementedError(
                "Parsing reale atti non ancora implementato. Vedi docs/sources-limits.md."
            )
        acts: list[Act] = []
        for path in sorted(_acts_fixtures_dir().glob("acts*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            for raw in data if isinstance(data, list) else [data]:
                acts.append(self._parse_act(raw))
        logger.info("Camera fixtures: %d atti caricati", len(acts))
        return acts

    @staticmethod
    def _parse_act(raw: dict) -> Act:
        return Act(
            id=raw["id"],
            politician_id=raw["politician_id"],
            date=date.fromisoformat(raw["date"]),
            chamber=Chamber(raw.get("chamber", "camera")),
            source_type=SourceType(raw.get("source_type", "parliamentary_question")),
            act_type=raw["act_type"],
            title=raw["title"],
            text=raw.get("text", ""),
            status=raw.get("status"),
            source_url=raw["source_url"],
            metadata=raw.get("metadata", {}),
        )
