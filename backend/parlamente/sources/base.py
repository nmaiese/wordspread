"""Contratto astratto per tutti i source adapter (Camera, Senato, Fase 2)."""

from __future__ import annotations

import abc
from datetime import date

from ..models import Act, Intervention, Politician, SourceDocument


class SourceAdapter(abc.ABC):
    """Interfaccia comune a tutte le fonti.

    Gli adapter Fase 1 implementano i metodi che hanno senso per la propria fonte
    e sollevano `NotImplementedError` per gli altri. Gli adapter Fase 2
    (public_communication) ereditano lo stesso contratto, così la pipeline di
    ingestion è identica indipendentemente dal layer.
    """

    #: etichetta human-readable, es. "Camera dei Deputati"
    source_name: str = "unknown"

    @abc.abstractmethod
    def fetch_politicians(self, legislature: str) -> list[Politician]:
        ...

    def fetch_documents(
        self, since: date | None = None, until: date | None = None
    ) -> list[SourceDocument]:
        raise NotImplementedError(f"{self.source_name}: fetch_documents non implementato")

    def fetch_interventions(
        self, since: date | None = None, until: date | None = None
    ) -> list[Intervention]:
        raise NotImplementedError(f"{self.source_name}: fetch_interventions non implementato")

    def fetch_acts(
        self, since: date | None = None, until: date | None = None
    ) -> list[Act]:
        raise NotImplementedError(f"{self.source_name}: fetch_acts non implementato")
