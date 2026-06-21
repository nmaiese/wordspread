"""Interviste / talk show — STUB Fase 2. source_type=interview. Vedi base.py.

Fonte: trascrizioni di interviste e talk show (testate, YouTube, ecc.).
Richiede attribuzione e, dove serve, trascrizione automatica del parlato.
"""

from __future__ import annotations

from datetime import date

from ...models import Intervention, SourceType
from .base import PublicCommunicationAdapter


class InterviewsAdapter(PublicCommunicationAdapter):
    source_name = "Interviste / Talk show"
    source_type = SourceType.INTERVIEW

    def fetch_interventions(
        self, since: date | None = None, until: date | None = None
    ) -> list[Intervention]:
        raise NotImplementedError("Fase 2 non avviata: nessuna raccolta esterna.")
