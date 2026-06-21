"""Livello B — Classificazione su tassonomia controllata.

Classificatore keyword-based, trasparente e verificabile: ogni assegnazione di
topic deriva da match espliciti di trigger (vedi topics.yaml), non da una scatola
nera. Questo è coerente col principio del progetto: niente sintesi inventate.

Il punteggio di un (documento, topic) è il numero di occorrenze dei trigger del
topic nel testo, pesato per la specificità del trigger (le locuzioni multi-parola
pesano più delle parole singole).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

from ..models import Topic

_TOPICS_FILE = Path(__file__).with_name("topics.yaml")


@dataclass
class TopicDef:
    id: str
    name: str
    macro_area: str
    triggers: list[str] = field(default_factory=list)
    # regex precompilata per ciascun trigger (match su confine di parola)
    _patterns: list[tuple[re.Pattern[str], float]] = field(default_factory=list)

    def compile(self) -> None:
        self._patterns = []
        for trig in self.triggers:
            trig = trig.strip().lower()
            if not trig:
                continue
            weight = 1.0 + 0.5 * (trig.count(" "))  # locuzioni pesano di più
            pattern = re.compile(r"\b" + re.escape(trig).replace(r"\ ", r"\s+") + r"\b")
            self._patterns.append((pattern, weight))

    def score(self, text: str) -> float:
        total = 0.0
        for pattern, weight in self._patterns:
            total += weight * len(pattern.findall(text))
        return total


@lru_cache
def load_taxonomy() -> list[TopicDef]:
    data = yaml.safe_load(_TOPICS_FILE.read_text(encoding="utf-8"))
    topics: list[TopicDef] = []
    for macro in data.get("macro_areas", []):
        macro_name = macro["name"]
        for t in macro.get("topics", []):
            td = TopicDef(
                id=t["id"],
                name=t["name"],
                macro_area=macro_name,
                triggers=t.get("triggers", []),
            )
            td.compile()
            topics.append(td)
    return topics


def taxonomy_as_models() -> list[Topic]:
    return [
        Topic(id=t.id, name=t.name, macro_area=t.macro_area, description=", ".join(t.triggers[:5]))
        for t in load_taxonomy()
    ]


def classify(text: str, threshold: float = 1.0) -> list[tuple[str, float]]:
    """Restituisce [(topic_id, score)] per i topic con score >= threshold,
    ordinati per score decrescente."""
    text = (text or "").lower()
    hits = [(t.id, t.score(text)) for t in load_taxonomy()]
    return sorted([(tid, s) for tid, s in hits if s >= threshold], key=lambda x: x[1], reverse=True)
