"""Repository: unico punto di accesso allo storage.

Isolare le query qui rende naturale la futura migrazione a PostgreSQL (basta
sostituire la connessione e poche istruzioni di upsert).
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from ..models import (
    Act,
    Intervention,
    Keyword,
    Politician,
    SourceDocument,
    Topic,
    TopicAssignment,
)
from .db import Database


def _dumps(d: dict[str, Any]) -> str:
    return json.dumps(d, ensure_ascii=False, default=str)


class Repositories:
    def __init__(self, db: "Database | object") -> None:
        # Accetta un Database oppure direttamente una connessione/cursore DuckDB.
        # Importante: una connessione DuckDB NON è thread-safe; per l'API si passa
        # un cursore per-richiesta (db.conn.cursor()), così thread concorrenti non
        # condividono lo stesso cursore.
        if hasattr(db, "conn"):
            self.db = db
            self.conn = db.conn
        else:
            self.db = None
            self.conn = db

    # ---------- politicians ----------
    def upsert_politicians(self, items: Iterable[Politician]) -> int:
        rows = [
            (
                p.id,
                p.full_name,
                p.first_name,
                p.last_name,
                p.chamber.value,
                p.group_name,
                p.legislature,
                p.official_url,
                _dumps(p.metadata),
            )
            for p in items
        ]
        if not rows:
            return 0
        self.conn.executemany(
            """INSERT OR REPLACE INTO politicians
               (id, full_name, first_name, last_name, chamber, group_name,
                legislature, official_url, metadata_json)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            rows,
        )
        return len(rows)

    def list_politicians(
        self,
        chamber: str | None = None,
        legislature: str | None = None,
        query: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        sql = "SELECT * FROM politicians WHERE 1=1"
        params: list[Any] = []
        if chamber:
            sql += " AND chamber = ?"
            params.append(chamber)
        if legislature:
            sql += " AND legislature = ?"
            params.append(legislature)
        if query:
            sql += " AND LOWER(full_name) LIKE ?"
            params.append(f"%{query.lower()}%")
        sql += " ORDER BY full_name LIMIT ?"
        params.append(limit)
        return self._fetch_dicts(sql, params)

    def get_politician(self, politician_id: str) -> dict[str, Any] | None:
        rows = self._fetch_dicts("SELECT * FROM politicians WHERE id = ?", [politician_id])
        return rows[0] if rows else None

    # ---------- documents ----------
    def upsert_documents(self, items: Iterable[SourceDocument]) -> int:
        rows = [
            (
                d.id,
                d.source,
                d.chamber.value,
                d.legislature,
                d.source_layer.value,
                d.source_type.value,
                d.document_type,
                d.date,
                d.title,
                d.url,
                d.raw_text,
                _dumps(d.metadata),
            )
            for d in items
        ]
        if not rows:
            return 0
        self.conn.executemany(
            """INSERT OR REPLACE INTO documents
               (id, source, chamber, legislature, source_layer, source_type,
                document_type, date, title, url, raw_text, metadata_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            rows,
        )
        return len(rows)

    # ---------- interventions ----------
    def upsert_interventions(self, items: Iterable[Intervention]) -> int:
        rows = [
            (
                i.id,
                i.politician_id,
                i.politician_name,
                i.document_id,
                i.date,
                i.chamber.value,
                i.source_layer.value,
                i.source_type.value,
                i.context,
                i.text,
                i.source_url,
                _dumps(i.metadata),
            )
            for i in items
        ]
        if not rows:
            return 0
        self.conn.executemany(
            """INSERT OR REPLACE INTO interventions
               (id, politician_id, politician_name, document_id, date, chamber,
                source_layer, source_type, context, text, source_url, metadata_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            rows,
        )
        return len(rows)

    def interventions_for(self, politician_id: str) -> list[dict[str, Any]]:
        return self._fetch_dicts(
            "SELECT * FROM interventions WHERE politician_id = ? ORDER BY date",
            [politician_id],
        )

    def all_interventions(self) -> list[dict[str, Any]]:
        return self._fetch_dicts("SELECT * FROM interventions ORDER BY date", [])

    # ---------- acts ----------
    def upsert_acts(self, items: Iterable[Act]) -> int:
        rows = [
            (
                a.id,
                a.politician_id,
                a.date,
                a.chamber.value,
                a.source_layer.value,
                a.source_type.value,
                a.act_type,
                a.title,
                a.text,
                a.status,
                a.source_url,
                _dumps(a.metadata),
            )
            for a in items
        ]
        if not rows:
            return 0
        self.conn.executemany(
            """INSERT OR REPLACE INTO acts
               (id, politician_id, date, chamber, source_layer, source_type,
                act_type, title, text, status, source_url, metadata_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            rows,
        )
        return len(rows)

    def acts_for(self, politician_id: str) -> list[dict[str, Any]]:
        return self._fetch_dicts(
            "SELECT * FROM acts WHERE politician_id = ? ORDER BY date", [politician_id]
        )

    def all_acts(self) -> list[dict[str, Any]]:
        return self._fetch_dicts("SELECT * FROM acts ORDER BY date", [])

    # ---------- topics ----------
    def upsert_topics(self, items: Iterable[Topic]) -> int:
        rows = [(t.id, t.name, t.macro_area, t.description) for t in items]
        if not rows:
            return 0
        self.conn.executemany(
            "INSERT OR REPLACE INTO topics (id, name, macro_area, description) VALUES (?,?,?,?)",
            rows,
        )
        return len(rows)

    def topics_map(self) -> dict[str, dict[str, Any]]:
        return {r["id"]: r for r in self._fetch_dicts("SELECT * FROM topics", [])}

    # ---------- topic assignments ----------
    def replace_topic_assignments(self, items: Iterable[TopicAssignment]) -> int:
        self.conn.execute("DELETE FROM intervention_topics")
        rows = [(a.entity_type, a.entity_id, a.topic_id, a.score) for a in items]
        if rows:
            self.conn.executemany(
                """INSERT OR REPLACE INTO intervention_topics
                   (entity_type, entity_id, topic_id, score) VALUES (?,?,?,?)""",
                rows,
            )
        return len(rows)

    def assignments_for_entities(
        self, entity_type: str, entity_ids: list[str]
    ) -> list[dict[str, Any]]:
        if not entity_ids:
            return []
        placeholders = ",".join("?" for _ in entity_ids)
        return self._fetch_dicts(
            f"""SELECT * FROM intervention_topics
                WHERE entity_type = ? AND entity_id IN ({placeholders})""",
            [entity_type, *entity_ids],
        )

    # ---------- keywords ----------
    def replace_keywords_for(self, entity_type: str, items: Iterable[Keyword]) -> int:
        self.conn.execute("DELETE FROM keywords WHERE entity_type = ?", [entity_type])
        rows = [
            (k.entity_type, k.entity_id, k.keyword, k.score, k.frequency, k.period)
            for k in items
        ]
        if rows:
            self.conn.executemany(
                """INSERT INTO keywords
                   (entity_type, entity_id, keyword, score, frequency, period)
                   VALUES (?,?,?,?,?,?)""",
                rows,
            )
        return len(rows)

    def keywords_for(
        self, entity_type: str, entity_id: str, limit: int = 50
    ) -> list[dict[str, Any]]:
        return self._fetch_dicts(
            """SELECT keyword, score, frequency, period FROM keywords
               WHERE entity_type = ? AND entity_id = ?
               ORDER BY score DESC LIMIT ?""",
            [entity_type, entity_id, limit],
        )

    # ---------- helpers ----------
    def _fetch_dicts(self, sql: str, params: list[Any]) -> list[dict[str, Any]]:
        cur = self.conn.execute(sql, params)
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
