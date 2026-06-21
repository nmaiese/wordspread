"""Loader delle fixtures Camera.

IMPORTANTE — integrità dei dati:
Le fixtures NON sono dati inventati. Sono documenti ufficiali REALI scaricati una
sola volta dal sito della Camera / dall'open data e salvati in
`data/fixtures/camera/` con URL e data reali. Servono a far girare la pipeline
NLP + UI end-to-end senza martellare le fonti ufficiali a ogni esecuzione.

Formato fixture (JSON), una lista di oggetti:
{
  "document": { ...campi SourceDocument... },
  "interventions": [ { ...campi Intervention senza id/document_id... }, ... ]
}
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from ...config import get_settings
from ...logging import get_logger
from ...models import Chamber, Intervention, SourceDocument, SourceType

logger = get_logger(__name__)


def _fixtures_dir() -> Path:
    return get_settings().fixtures_dir / "camera"


def _slug(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")[:60]


def load_fixture_documents() -> list[SourceDocument]:
    docs: list[SourceDocument] = []
    for fixture in _iter_fixture_records():
        docs.append(_parse_document(fixture["document"]))
    logger.info("Camera fixtures: %d documenti caricati", len(docs))
    return docs


def load_fixture_interventions() -> list[Intervention]:
    interventions: list[Intervention] = []
    for fixture in _iter_fixture_records():
        doc = fixture["document"]
        doc_id = doc["id"]
        for idx, raw in enumerate(fixture.get("interventions", [])):
            interventions.append(_parse_intervention(raw, doc, doc_id, idx))
    logger.info("Camera fixtures: %d interventi caricati", len(interventions))
    return interventions


def _iter_fixture_records():
    directory = _fixtures_dir()
    if not directory.exists():
        logger.warning("Cartella fixtures assente: %s", directory)
        return
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        records = data if isinstance(data, list) else [data]
        for record in records:
            yield record


def _parse_document(d: dict) -> SourceDocument:
    return SourceDocument(
        id=d["id"],
        source=d.get("source", "Camera dei Deputati"),
        chamber=Chamber(d.get("chamber", "camera")),
        legislature=str(d.get("legislature", "19")),
        source_type=SourceType(d.get("source_type", "chamber_speech")),
        document_type=d["document_type"],
        date=date.fromisoformat(d["date"]),
        title=d["title"],
        url=d["url"],
        raw_text=d.get("raw_text", ""),
        metadata=d.get("metadata", {}),
    )


def _parse_intervention(raw: dict, doc: dict, doc_id: str, idx: int) -> Intervention:
    politician_id = raw["politician_id"]
    inter_id = raw.get("id") or f"{doc_id}_int_{idx}_{_slug(politician_id)}"
    return Intervention(
        id=inter_id,
        politician_id=politician_id,
        politician_name=raw["politician_name"],
        document_id=doc_id,
        date=date.fromisoformat(raw.get("date", doc["date"])),
        chamber=Chamber(raw.get("chamber", doc.get("chamber", "camera"))),
        source_type=SourceType(raw.get("source_type", doc.get("source_type", "chamber_speech"))),
        context=raw.get("context", doc.get("document_type", "Assemblea")),
        text=raw["text"],
        source_url=raw.get("source_url", doc["url"]),
        metadata=raw.get("metadata", {}),
    )
