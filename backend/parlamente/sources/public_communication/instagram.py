"""Instagram — STUB Fase 2. source_type=instagram_post. Vedi base.py."""

from __future__ import annotations

from datetime import date

from ...models import Intervention, SourceType
from .base import PublicCommunicationAdapter


class InstagramAdapter(PublicCommunicationAdapter):
    source_name = "Instagram"
    source_type = SourceType.INSTAGRAM_POST

    def fetch_interventions(
        self, since: date | None = None, until: date | None = None
    ) -> list[Intervention]:
        raise NotImplementedError("Fase 2 non avviata: nessuna raccolta social.")
