"""Confronto tra parlamentari (Fase 1) + firme predisposte per la Fase 2.

Fase 1: temi comuni / distintivi, keyword caratteristiche, volumi per sede
(Aula vs Commissione vs Atti), fonti collegate.

Fase 2 (STUB): l'architettura prevede già la metrica chiave
"Official vs Public Communication Gap". Le funzioni esistono come contratto, ma
sollevano NotImplementedError finché non saranno presenti dati
`public_communication` (vedi docs/phase2-gap.md).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from ..models import SourceType
from ..storage.repositories import Repositories
from .evidence import build_topic_evidence


def _topic_shares(repo: Repositories, politician_id: str) -> dict[str, dict[str, Any]]:
    return {
        te.topic_id: {
            "topic": te.topic,
            "macro_area": te.macro_area,
            "share": te.score,
            "intervention_count": te.intervention_count,
            "act_count": te.act_count,
        }
        for te in build_topic_evidence(repo, politician_id)
    }


def _venue_volumes(repo: Repositories, politician_id: str) -> dict[str, int]:
    """Conta interventi in Aula vs Commissione vs Atti."""
    vols: dict[str, int] = defaultdict(int)
    for r in repo.interventions_for(politician_id):
        if r["source_type"] == SourceType.COMMITTEE_SPEECH.value:
            vols["commissione"] += 1
        else:
            vols["aula"] += 1
    vols["atti"] = len(repo.acts_for(politician_id))
    return dict(vols)


def compare_politicians(repo: Repositories, id_a: str, id_b: str) -> dict[str, Any] | None:
    pa = repo.get_politician(id_a)
    pb = repo.get_politician(id_b)
    if not pa or not pb:
        return None

    shares_a = _topic_shares(repo, id_a)
    shares_b = _topic_shares(repo, id_b)
    topics_a, topics_b = set(shares_a), set(shares_b)

    common = sorted(
        (
            {
                "topic_id": tid,
                "topic": shares_a[tid]["topic"],
                "share_a": shares_a[tid]["share"],
                "share_b": shares_b[tid]["share"],
            }
            for tid in topics_a & topics_b
        ),
        key=lambda x: x["share_a"] + x["share_b"],
        reverse=True,
    )
    distinctive_a = sorted(
        (shares_a[tid] | {"topic_id": tid} for tid in topics_a - topics_b),
        key=lambda x: x["share"],
        reverse=True,
    )
    distinctive_b = sorted(
        (shares_b[tid] | {"topic_id": tid} for tid in topics_b - topics_a),
        key=lambda x: x["share"],
        reverse=True,
    )

    kw_a = {k["keyword"] for k in repo.keywords_for("politician", id_a, limit=40)}
    kw_b = {k["keyword"] for k in repo.keywords_for("politician", id_b, limit=40)}

    def _summary(p: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": p["id"],
            "full_name": p["full_name"],
            "chamber": p["chamber"],
            "group_name": p["group_name"],
        }

    return {
        "a": _summary(pa),
        "b": _summary(pb),
        "common_topics": common,
        "distinctive_a": distinctive_a,
        "distinctive_b": distinctive_b,
        "distinctive_keywords_a": sorted(kw_a - kw_b)[:25],
        "distinctive_keywords_b": sorted(kw_b - kw_a)[:25],
        "venues": {"a": _venue_volumes(repo, id_a), "b": _venue_volumes(repo, id_b)},
    }


# ---------------------------------------------------------------------------
# Fase 2 — STUB. Vedi docs/phase2-gap.md per la definizione delle metriche.
# ---------------------------------------------------------------------------
def compare_official_vs_public(politician_id: str, period: str | None = None) -> dict[str, Any]:
    raise NotImplementedError(
        "Fase 2 non avviata: richiede dati con source_layer=public_communication."
    )


def calculate_topic_gap(politician_id: str, topic_id: str, period: str | None = None) -> float:
    """Gap = quota del topic nella comunicazione pubblica − quota nell'attività ufficiale."""
    raise NotImplementedError("Fase 2 non avviata. Vedi docs/phase2-gap.md.")


def calculate_rhetoric_gap(politician_id: str, period: str | None = None) -> dict[str, Any]:
    """Differenza di lessico/toni tra sede istituzionale e comunicazione pubblica."""
    raise NotImplementedError("Fase 2 non avviata. Vedi docs/phase2-gap.md.")
