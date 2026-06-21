"""Endpoint sui parlamentari."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from ...analysis.evidence import build_topic_evidence
from ...analysis.profile import build_profile
from ...storage.repositories import Repositories
from ..deps import get_repositories

router = APIRouter(prefix="/politicians", tags=["politicians"])


@router.get("")
def list_politicians(
    chamber: str | None = Query(None, description="camera | senato"),
    legislature: str | None = Query(None),
    q: str | None = Query(None, description="Ricerca per nome"),
    limit: int = Query(100, le=500),
    repo: Repositories = Depends(get_repositories),
) -> list[dict]:
    rows = repo.list_politicians(chamber=chamber, legislature=legislature, query=q, limit=limit)
    return [
        {
            "id": r["id"],
            "full_name": r["full_name"],
            "chamber": r["chamber"],
            "group_name": r["group_name"],
            "legislature": r["legislature"],
        }
        for r in rows
    ]


@router.get("/{politician_id}")
def get_politician(
    politician_id: str,
    repo: Repositories = Depends(get_repositories),
) -> dict:
    profile = build_profile(repo, politician_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Parlamentare non trovato")
    return profile


@router.get("/{politician_id}/topics/{topic_id}/evidence")
def get_topic_evidence(
    politician_id: str,
    topic_id: str,
    repo: Repositories = Depends(get_repositories),
) -> dict:
    for te in build_topic_evidence(repo, politician_id, max_items=20):
        if te.topic_id == topic_id:
            return te.model_dump(mode="json")
    raise HTTPException(status_code=404, detail="Topic non trovato per questo parlamentare")
