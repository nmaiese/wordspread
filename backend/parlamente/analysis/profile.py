"""Assembla il payload della pagina Parlamentare a partire dallo storage.

Tutto ciò che esce di qui è già tracciabile a fonti ufficiali (ogni evidence
porta il proprio URL)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from ..storage.repositories import Repositories
from .evidence import build_topic_evidence


def _iso(d: Any) -> str | None:
    """ISO 'YYYY-MM-DD' robusto: accetta date, datetime o stringa (a seconda di
    come il driver DuckDB restituisce le colonne DATE)."""
    if not d:
        return None
    if isinstance(d, str):
        return d
    return d.isoformat()


def _month(d: Any) -> str:
    iso = _iso(d)
    return iso[:7] if iso else ""


def build_profile(repo: Repositories, politician_id: str) -> dict[str, Any] | None:
    pol = repo.get_politician(politician_id)
    if not pol:
        return None

    interventions = repo.interventions_for(politician_id)
    acts = repo.acts_for(politician_id)
    topic_evidence = build_topic_evidence(repo, politician_id)
    keywords = repo.keywords_for("politician", politician_id, limit=40)

    # KPI / periodo coperto (ISO ordina lessicograficamente come cronologicamente)
    isos = sorted(i for i in (_iso(r["date"]) for r in interventions + acts) if i)
    period = {
        "from": isos[0] if isos else None,
        "to": isos[-1] if isos else None,
    }

    # Top temi (quota%) e timeline per macro-aggregato del topic principale per mese
    top_topics = [
        {
            "topic_id": te.topic_id,
            "topic": te.topic,
            "macro_area": te.macro_area,
            "share": te.score,
            "intervention_count": te.intervention_count,
            "act_count": te.act_count,
            "keywords": te.keywords,
        }
        for te in topic_evidence
    ]

    timeline = _build_topic_timeline(repo, interventions, acts)

    return {
        "politician": {
            "id": pol["id"],
            "full_name": pol["full_name"],
            "chamber": pol["chamber"],
            "group_name": pol["group_name"],
            "legislature": pol["legislature"],
            "official_url": pol["official_url"],
        },
        "kpi": {
            "intervention_count": len(interventions),
            "act_count": len(acts),
            "topic_count": len(top_topics),
            "period": period,
        },
        "top_topics": top_topics,
        "timeline": timeline,
        "keywords": [
            {"keyword": k["keyword"], "score": k["score"], "frequency": k["frequency"]}
            for k in keywords
        ],
        "evidence": [te.model_dump(mode="json") for te in topic_evidence],
        "interventions": [
            {
                "id": r["id"],
                "date": _iso(r["date"]),
                "context": r["context"],
                "text": (r["text"] or "")[:400],
                "source_url": r["source_url"],
            }
            for r in interventions
        ],
        "acts": [
            {
                "id": r["id"],
                "date": _iso(r["date"]),
                "act_type": r["act_type"],
                "title": r["title"],
                "status": r["status"],
                "source_url": r["source_url"],
            }
            for r in acts
        ],
    }


def _build_topic_timeline(
    repo: Repositories, interventions: list[dict], acts: list[dict]
) -> list[dict[str, Any]]:
    """Evoluzione dei temi nel tempo: per ogni mese, score per macro_area."""
    topics_map = repo.topics_map()
    int_assign = repo.assignments_for_entities("intervention", [r["id"] for r in interventions])
    act_assign = repo.assignments_for_entities("act", [r["id"] for r in acts])
    int_date = {r["id"]: r["date"] for r in interventions}
    act_date = {r["id"]: r["date"] for r in acts}

    # (month, macro_area) -> score
    grid: dict[tuple[str, str], float] = defaultdict(float)
    for a in int_assign:
        macro = topics_map.get(a["topic_id"], {}).get("macro_area", "Altro")
        grid[(_month(int_date.get(a["entity_id"])), macro)] += a["score"]
    for a in act_assign:
        macro = topics_map.get(a["topic_id"], {}).get("macro_area", "Altro")
        grid[(_month(act_date.get(a["entity_id"])), macro)] += a["score"]

    months = sorted({m for (m, _) in grid if m})
    out: list[dict[str, Any]] = []
    for m in months:
        entry: dict[str, Any] = {"month": m}
        for (mm, macro), score in grid.items():
            if mm == m:
                entry[macro] = round(entry.get(macro, 0.0) + score, 3)
        out.append(entry)
    return out
