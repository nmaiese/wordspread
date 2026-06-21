"""Comunicati stampa / newsletter — STUB Fase 2. source_type=press_release. Vedi base.py."""

from __future__ import annotations

from datetime import date

from ...models import Intervention, SourceType
from .base import PublicCommunicationAdapter


class PressReleasesAdapter(PublicCommunicationAdapter):
    source_name = "Comunicati stampa / Newsletter"
    source_type = SourceType.PRESS_RELEASE

    def fetch_interventions(
        self, since: date | None = None, until: date | None = None
    ) -> list[Intervention]:
        raise NotImplementedError("Fase 2 non avviata: nessuna raccolta esterna.")
