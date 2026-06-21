"""Resoconti Assemblea Senato — STUB (Fase 1.b). Vedi senate/__init__.py."""

from __future__ import annotations

from datetime import date

from ...models import Intervention
from ..base import SourceAdapter


class SenateSpeechesAdapter(SourceAdapter):
    source_name = "Senato della Repubblica — Resoconti Assemblea"

    def fetch_politicians(self, legislature: str):  # type: ignore[override]
        raise NotImplementedError("Usa SenateSenatorsAdapter per i senatori.")

    def fetch_interventions(
        self, since: date | None = None, until: date | None = None
    ) -> list[Intervention]:
        raise NotImplementedError("Adapter resoconti Senato non ancora implementato (Fase 1.b).")
