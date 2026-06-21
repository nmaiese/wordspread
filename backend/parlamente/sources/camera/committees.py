"""Adapter dei resoconti delle Commissioni (Camera).

STATO: stub documentato. Struttura identica a `speeches` ma con `context` =
nome Commissione e `source_type = committee_speech`. Da completare in Fase 1.b;
nell'MVP gli interventi di Commissione, se presenti nelle fixtures, sono già
caricati da `speeches`/`fixtures` con il proprio source_type.
"""

from __future__ import annotations

from datetime import date

from ...models import Intervention, Politician
from ..base import SourceAdapter


class CameraCommitteesAdapter(SourceAdapter):
    source_name = "Camera dei Deputati — Commissioni"

    def fetch_politicians(self, legislature: str) -> list[Politician]:
        raise NotImplementedError("Usa CameraDeputiesAdapter per i deputati.")

    def fetch_interventions(
        self, since: date | None = None, until: date | None = None
    ) -> list[Intervention]:
        raise NotImplementedError(
            "Parsing reale resoconti Commissione non ancora implementato. "
            "Vedi docs/sources-limits.md."
        )
