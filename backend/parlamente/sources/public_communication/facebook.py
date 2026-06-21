"""Facebook — STUB Fase 2.

Fonte: post pubblici di pagine ufficiali dei parlamentari.
Vincoli: Graph API + ToS Meta; nessuno scraping aggressivo. source_type=facebook_post.
"""

from __future__ import annotations

from datetime import date

from ...models import Intervention, SourceType
from .base import PublicCommunicationAdapter


class FacebookAdapter(PublicCommunicationAdapter):
    source_name = "Facebook"
    source_type = SourceType.FACEBOOK_POST

    def fetch_interventions(
        self, since: date | None = None, until: date | None = None
    ) -> list[Intervention]:
        raise NotImplementedError("Fase 2 non avviata: nessuna raccolta social.")
