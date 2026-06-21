"""Evidence layer: ogni topic assegnato a un parlamentare deve essere spiegabile
e riconducibile a fonti ufficiali."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    """Un singolo elemento di prova (un documento/intervento rappresentativo)."""

    date: date
    source: str  # es. "Camera dei Deputati"
    document_type: str  # es. "Resoconto Assemblea"
    title: str
    quote: str  # estratto rappresentativo (snippet attorno al match)
    url: str
    entity_type: str = "intervention"  # "intervention" | "act"
    score: float = 0.0


class TopicEvidence(BaseModel):
    """Spiegazione completa di (parlamentare, topic): conta, keyword, evidenze."""

    politician_id: str
    topic: str
    topic_id: str
    macro_area: str
    score: float  # quota del tema sul totale (0..1)
    intervention_count: int = 0
    act_count: int = 0
    keywords: list[str] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
