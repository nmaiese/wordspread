"""Modelli dati normalizzati di Parla Mente.

Tutti gli oggetti prodotti dagli adapter delle fonti sono normalizzati in queste
strutture: niente DataFrame grezzi sparsi nel codice.
"""

from .enums import Chamber, SourceLayer, SourceType
from .entities import (
    Act,
    Intervention,
    Keyword,
    Politician,
    SourceDocument,
    Topic,
    TopicAssignment,
)
from .evidence import EvidenceItem, TopicEvidence

__all__ = [
    "Chamber",
    "SourceLayer",
    "SourceType",
    "Politician",
    "SourceDocument",
    "Intervention",
    "Act",
    "Topic",
    "TopicAssignment",
    "Keyword",
    "EvidenceItem",
    "TopicEvidence",
]
