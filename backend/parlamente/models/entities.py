"""Entità normalizzate.

Ogni entità che genera un insight è tracciabile a una fonte ufficiale via
`source_url` / `url`. Questo è il vincolo non negoziabile del progetto.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field

from .enums import Chamber, SourceLayer, SourceType


class Politician(BaseModel):
    """Parlamentare normalizzato."""

    id: str  # es. "camera_d309220_19"
    full_name: str
    first_name: str | None = None
    last_name: str | None = None
    chamber: Chamber
    group_name: str | None = None
    legislature: str  # es. "19"
    official_url: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceDocument(BaseModel):
    """Documento ufficiale grezzo normalizzato (un resoconto, un atto, una scheda…)."""

    id: str
    source: str  # es. "Camera dei Deputati"
    chamber: Chamber
    legislature: str
    source_layer: SourceLayer = SourceLayer.OFFICIAL_INSTITUTIONAL
    source_type: SourceType
    document_type: str  # etichetta human-readable, es. "Resoconto Assemblea"
    date: date
    title: str
    url: str
    raw_text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Intervention(BaseModel):
    """Un singolo intervento attribuito a un parlamentare dentro un documento."""

    id: str
    politician_id: str
    politician_name: str
    document_id: str
    date: date
    chamber: Chamber
    source_layer: SourceLayer = SourceLayer.OFFICIAL_INSTITUTIONAL
    source_type: SourceType = SourceType.CHAMBER_SPEECH
    context: str  # es. "Assemblea", "Commissione Affari Sociali"
    text: str
    source_url: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Act(BaseModel):
    """Atto parlamentare (interrogazione, mozione, proposta di legge…)."""

    id: str
    politician_id: str
    date: date
    chamber: Chamber
    source_layer: SourceLayer = SourceLayer.OFFICIAL_INSTITUTIONAL
    source_type: SourceType = SourceType.PARLIAMENTARY_QUESTION
    act_type: str  # human-readable
    title: str
    text: str
    status: str | None = None
    source_url: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Topic(BaseModel):
    """Tema della tassonomia controllata."""

    id: str  # slug, es. "sanita_liste_attesa"
    name: str
    macro_area: str
    description: str | None = None


class TopicAssignment(BaseModel):
    """Associazione intervento/atto -> topic con punteggio (tabella intervention_topics)."""

    entity_type: str  # "intervention" | "act"
    entity_id: str
    topic_id: str
    score: float


class Keyword(BaseModel):
    """Keyword caratteristica estratta (TF-IDF / frequenza)."""

    entity_type: str  # "politician" | "topic" | "intervention"
    entity_id: str
    keyword: str
    score: float
    frequency: int = 0
    period: str | None = None  # es. "2025-05" o None per l'aggregato
