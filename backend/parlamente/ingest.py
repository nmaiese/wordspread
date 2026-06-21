"""Servizio di ingestion: collega i source adapter allo storage.

Mantiene la pipeline disaccoppiata: gli adapter producono modelli normalizzati,
qui li si persiste. Cambiare fonte (Camera -> Senato, o aggiungere Fase 2) non
tocca questo livello oltre alla scelta dell'adapter.
"""

from __future__ import annotations

from datetime import date

from .logging import get_logger
from .sources.camera.acts import CameraActsAdapter
from .sources.camera.deputies import CameraDeputiesAdapter
from .sources.camera.speeches import CameraSpeechesAdapter
from .storage.repositories import Repositories

logger = get_logger(__name__)


def ingest_deputies(repo: Repositories, legislature: str = "19") -> int:
    adapter = CameraDeputiesAdapter()
    politicians = adapter.fetch_politicians(legislature)
    n = repo.upsert_politicians(politicians)
    logger.info("Ingestion deputati: %d salvati", n)
    return n


def ingest_speeches(
    repo: Repositories,
    since: date | None = None,
    until: date | None = None,
    use_fixtures: bool = True,
) -> tuple[int, int]:
    adapter = CameraSpeechesAdapter(use_fixtures=use_fixtures)
    docs = adapter.fetch_documents(since, until)
    interventions = adapter.fetch_interventions(since, until)
    nd = repo.upsert_documents(docs)
    ni = repo.upsert_interventions(interventions)
    logger.info("Ingestion resoconti: %d documenti, %d interventi", nd, ni)
    return nd, ni


def ingest_acts(
    repo: Repositories,
    since: date | None = None,
    until: date | None = None,
    use_fixtures: bool = True,
) -> int:
    adapter = CameraActsAdapter(use_fixtures=use_fixtures)
    acts = adapter.fetch_acts(since, until)
    n = repo.upsert_acts(acts)
    logger.info("Ingestion atti: %d salvati", n)
    return n
