"""Evidence layer: rende ogni topic di un parlamentare spiegabile e verificabile.

Per ogni (parlamentare, topic) raccoglie n. interventi/atti, keyword rilevanti e
documenti rappresentativi con estratto (snippet attorno al trigger) e URL fonte.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from ..models import EvidenceItem, TopicEvidence
from ..nlp.taxonomy import load_taxonomy
from ..storage.repositories import Repositories

_SNIPPET_RADIUS = 160


def _topic_triggers() -> dict[str, list[str]]:
    return {t.id: t.triggers for t in load_taxonomy()}


def _make_quote(text: str, triggers: list[str]) -> str:
    """Estrae uno snippet attorno al primo trigger trovato; altrimenti l'incipit."""
    low = (text or "").lower()
    for trig in triggers:
        pattern = re.compile(r"\b" + re.escape(trig.lower()).replace(r"\ ", r"\s+") + r"\b")
        m = pattern.search(low)
        if m:
            start = max(0, m.start() - _SNIPPET_RADIUS)
            end = min(len(text), m.end() + _SNIPPET_RADIUS)
            prefix = "…" if start > 0 else ""
            suffix = "…" if end < len(text) else ""
            return f"{prefix}{text[start:end].strip()}{suffix}"
    return (text or "")[: 2 * _SNIPPET_RADIUS].strip()


def build_topic_evidence(
    repo: Repositories, politician_id: str, max_items: int = 5
) -> list[TopicEvidence]:
    """Costruisce la lista di TopicEvidence per un parlamentare, ordinata per peso."""
    interventions = {r["id"]: r for r in repo.interventions_for(politician_id)}
    acts = {r["id"]: r for r in repo.acts_for(politician_id)}
    topics_map = repo.topics_map()
    triggers = _topic_triggers()

    int_assign = repo.assignments_for_entities("intervention", list(interventions))
    act_assign = repo.assignments_for_entities("act", list(acts))

    # Aggrega per topic
    per_topic_score: dict[str, float] = defaultdict(float)
    per_topic_int: dict[str, int] = defaultdict(int)
    per_topic_act: dict[str, int] = defaultdict(int)
    per_topic_items: dict[str, list[EvidenceItem]] = defaultdict(list)

    for a in int_assign:
        tid = a["topic_id"]
        row = interventions[a["entity_id"]]
        per_topic_score[tid] += a["score"]
        per_topic_int[tid] += 1
        per_topic_items[tid].append(
            EvidenceItem(
                date=row["date"],
                source="Camera dei Deputati",
                document_type=row.get("context") or "Intervento",
                title=row.get("context") or "Intervento in Assemblea",
                quote=_make_quote(row["text"], triggers.get(tid, [])),
                url=row["source_url"],
                entity_type="intervention",
                score=a["score"],
            )
        )
    for a in act_assign:
        tid = a["topic_id"]
        row = acts[a["entity_id"]]
        per_topic_score[tid] += a["score"]
        per_topic_act[tid] += 1
        per_topic_items[tid].append(
            EvidenceItem(
                date=row["date"],
                source="Camera dei Deputati",
                document_type=row.get("act_type") or "Atto",
                title=row.get("title") or "Atto parlamentare",
                quote=_make_quote(
                    f"{row.get('title', '')}. {row.get('text', '')}", triggers.get(tid, [])
                ),
                url=row["source_url"],
                entity_type="act",
                score=a["score"],
            )
        )

    total = sum(per_topic_score.values()) or 1.0
    result: list[TopicEvidence] = []
    for tid, score in per_topic_score.items():
        meta = topics_map.get(tid, {})
        items = sorted(per_topic_items[tid], key=lambda e: e.score, reverse=True)[:max_items]
        result.append(
            TopicEvidence(
                politician_id=politician_id,
                topic=meta.get("name", tid),
                topic_id=tid,
                macro_area=meta.get("macro_area", ""),
                score=round(score / total, 4),
                intervention_count=per_topic_int[tid],
                act_count=per_topic_act[tid],
                keywords=_topic_keywords(triggers.get(tid, []), interventions, acts),
                evidence=items,
            )
        )
    result.sort(key=lambda te: te.score, reverse=True)
    return result


def _topic_keywords(
    triggers: list[str],
    interventions: dict[str, Any],
    acts: dict[str, Any],
) -> list[str]:
    """Tra i trigger del topic, restituisce quelli effettivamente presenti nei testi
    del parlamentare (così le keyword mostrate sono verificabili, non teoriche)."""
    corpus = " ".join(
        [r["text"] or "" for r in interventions.values()]
        + [f"{r.get('title', '')} {r.get('text', '')}" for r in acts.values()]
    ).lower()
    present = []
    for trig in triggers:
        pattern = re.compile(r"\b" + re.escape(trig.lower()).replace(r"\ ", r"\s+") + r"\b")
        if pattern.search(corpus):
            present.append(trig)
    return present[:8]
