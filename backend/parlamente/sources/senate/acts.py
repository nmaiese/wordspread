"""Atti e disegni di legge Senato — STUB (Fase 1.b). Vedi senate/__init__.py."""

from __future__ import annotations

from datetime import date

from ...models import Act
from ..base import SourceAdapter


class SenateActsAdapter(SourceAdapter):
    source_name = "Senato della Repubblica — Atti"

    def fetch_politicians(self, legislature: str):  # type: ignore[override]
        raise NotImplementedError("Usa SenateSenatorsAdapter per i senatori.")

    def fetch_acts(
        self, since: date | None = None, until: date | None = None
    ) -> list[Act]:
        raise NotImplementedError("Adapter atti Senato non ancora implementato (Fase 1.b).")
