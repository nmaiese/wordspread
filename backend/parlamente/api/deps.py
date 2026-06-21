"""Dipendenze condivise dell'API."""

from __future__ import annotations

from functools import lru_cache

from ..storage.db import get_db
from ..storage.repositories import Repositories


@lru_cache
def _shared_db():
    return get_db()


def get_repositories() -> Repositories:
    # Una sola connessione DuckDB condivisa (read-mostly) per il processo API.
    return Repositories(_shared_db())
