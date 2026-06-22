"""Dipendenze condivise dell'API.

L'API è read-mostly: apre DuckDB in **read-only** così non prende il lock
esclusivo in scrittura e può coesistere con altri lettori / istanze. La scrittura
(ingestion, NLP) avviene solo via CLI.
"""

from __future__ import annotations

from functools import lru_cache

import duckdb
from fastapi import HTTPException

from ..config import get_settings
from ..storage.db import get_db
from ..storage.repositories import Repositories


@lru_cache
def _shared_db():
    settings = get_settings()
    if not settings.db_file.exists():
        raise HTTPException(
            status_code=503,
            detail=(
                "Database non inizializzato. Esegui prima la pipeline: "
                "`parlamente ingest deputies` && `parlamente ingest speeches` && "
                "`parlamente nlp keywords` && `parlamente nlp topics`."
            ),
        )
    try:
        # Una sola connessione DuckDB read-only condivisa per il processo API.
        return get_db(read_only=True)
    except duckdb.IOException as exc:
        # Lock in scrittura tenuto da un'altra istanza (es. ingestion in corso o
        # una vecchia API con codice non-read-only ancora attiva).
        raise HTTPException(
            status_code=503,
            detail=(
                "Database temporaneamente bloccato da un altro processo in scrittura. "
                "Chiudi eventuali ingestion in corso o istanze API duplicate e riprova."
            ),
        ) from exc


def get_repositories() -> Repositories:
    # Cursore per-richiesta sulla connessione read-only condivisa: ogni richiesta
    # (eseguita in un thread del threadpool di FastAPI) ha il proprio cursore,
    # evitando la corruzione da accesso concorrente a una connessione DuckDB.
    base = _shared_db()
    return Repositories(base.conn.cursor())
