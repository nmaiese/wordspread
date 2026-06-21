"""Contratto base degli adapter di comunicazione pubblica (Fase 2, STUB)."""

from __future__ import annotations

import abc
from datetime import date

from ...models import Intervention, Politician, SourceLayer
from ..base import SourceAdapter


class PublicCommunicationAdapter(SourceAdapter):
    """Tutti gli adapter Fase 2 ereditano questo: layer fissato a public_communication.

    NB: nessuno scraping è implementato. Le sottoclassi documentano la fonte e i
    vincoli (ToS, API, robots) ma sollevano NotImplementedError finché la Fase 2
    non sarà avviata esplicitamente.
    """

    source_layer = SourceLayer.PUBLIC_COMMUNICATION

    def fetch_politicians(self, legislature: str) -> list[Politician]:
        raise NotImplementedError("Le fonti Fase 2 non forniscono l'anagrafica parlamentari.")

    @abc.abstractmethod
    def fetch_interventions(
        self, since: date | None = None, until: date | None = None
    ) -> list[Intervention]:
        ...
