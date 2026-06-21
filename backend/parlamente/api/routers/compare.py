"""Endpoint di confronto tra parlamentari."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from ...analysis.compare import compare_politicians
from ...storage.repositories import Repositories
from ..deps import get_repositories

router = APIRouter(prefix="/compare", tags=["compare"])


@router.get("")
def compare(
    a: str = Query(..., description="ID parlamentare A"),
    b: str = Query(..., description="ID parlamentare B"),
    repo: Repositories = Depends(get_repositories),
) -> dict:
    result = compare_politicians(repo, a, b)
    if result is None:
        raise HTTPException(status_code=404, detail="Uno dei due parlamentari non esiste")
    return result
