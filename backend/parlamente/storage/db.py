"""Storage su DuckDB.

Lo schema usa solo tipi standard (TEXT/DATE/DOUBLE/JSON-as-TEXT) per restare
banalmente migrabile a PostgreSQL: le query del repository non usano funzioni
DuckDB-specifiche.
"""

from __future__ import annotations

from pathlib import Path

import duckdb

from ..config import get_settings
from ..logging import get_logger

logger = get_logger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS politicians (
    id            TEXT PRIMARY KEY,
    full_name     TEXT NOT NULL,
    first_name    TEXT,
    last_name     TEXT,
    chamber       TEXT NOT NULL,
    group_name    TEXT,
    legislature   TEXT NOT NULL,
    official_url  TEXT,
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS documents (
    id            TEXT PRIMARY KEY,
    source        TEXT NOT NULL,
    chamber       TEXT NOT NULL,
    legislature   TEXT NOT NULL,
    source_layer  TEXT NOT NULL,
    source_type   TEXT NOT NULL,
    document_type TEXT NOT NULL,
    date          DATE NOT NULL,
    title         TEXT NOT NULL,
    url           TEXT NOT NULL,
    raw_text      TEXT NOT NULL,
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS interventions (
    id            TEXT PRIMARY KEY,
    politician_id TEXT NOT NULL,
    politician_name TEXT,
    document_id   TEXT,
    date          DATE NOT NULL,
    chamber       TEXT NOT NULL,
    source_layer  TEXT NOT NULL,
    source_type   TEXT NOT NULL,
    context       TEXT,
    text          TEXT NOT NULL,
    source_url    TEXT NOT NULL,
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS acts (
    id            TEXT PRIMARY KEY,
    politician_id TEXT NOT NULL,
    date          DATE NOT NULL,
    chamber       TEXT NOT NULL,
    source_layer  TEXT NOT NULL,
    source_type   TEXT NOT NULL,
    act_type      TEXT NOT NULL,
    title         TEXT NOT NULL,
    text          TEXT NOT NULL,
    status        TEXT,
    source_url    TEXT NOT NULL,
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS topics (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    macro_area  TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS intervention_topics (
    entity_type TEXT NOT NULL,   -- 'intervention' | 'act'
    entity_id   TEXT NOT NULL,
    topic_id    TEXT NOT NULL,
    score       DOUBLE NOT NULL,
    PRIMARY KEY (entity_type, entity_id, topic_id)
);

CREATE TABLE IF NOT EXISTS keywords (
    entity_type TEXT NOT NULL,   -- 'politician' | 'topic' | 'intervention'
    entity_id   TEXT NOT NULL,
    keyword     TEXT NOT NULL,
    score       DOUBLE NOT NULL,
    frequency   INTEGER DEFAULT 0,
    period      TEXT
);
"""


class Database:
    """Wrapper sottile attorno a una connessione DuckDB."""

    def __init__(self, path: Path | str | None = None, read_only: bool = False) -> None:
        settings = get_settings()
        self.path = Path(path) if path else settings.db_file
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.read_only = read_only
        # In read-only più processi/lettori possono aprire lo stesso file senza
        # conflitti di lock (utile per l'API mentre gira altro). La scrittura
        # (ingestion/NLP) usa read_only=False.
        self.conn = duckdb.connect(str(self.path), read_only=read_only)

    def init_schema(self) -> None:
        self.conn.execute(SCHEMA)
        logger.info("Schema inizializzato su %s", self.path)

    def reset(self) -> None:
        for table in (
            "keywords",
            "intervention_topics",
            "topics",
            "acts",
            "interventions",
            "documents",
            "politicians",
        ):
            self.conn.execute(f"DROP TABLE IF EXISTS {table}")
        self.init_schema()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def get_db(path: Path | str | None = None, read_only: bool = False) -> Database:
    db = Database(path, read_only=read_only)
    if not read_only:
        db.init_schema()
    return db
