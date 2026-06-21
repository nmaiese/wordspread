"""Client SPARQL per dati.camera.it.

LIMITI NOTI (verificati, vedi docs/sources-limits.md):
- Le query di aggregazione (GROUP BY / COUNT su grandi insiemi) restituiscono
  504 Gateway Time-out. Per questo il client incoraggia SELECT mirate con
  LIMIT/OFFSET e paginazione, e mette in cache i risultati su disco.
- Rispettiamo un rate-limit configurabile tra le richieste.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import httpx

from ...config import get_settings
from ...logging import get_logger

logger = get_logger(__name__)


class SparqlClient:
    def __init__(self, endpoint: str | None = None, cache_dir: Path | None = None) -> None:
        settings = get_settings()
        self.endpoint = endpoint or settings.camera_sparql_endpoint
        self.cache_dir = cache_dir or (settings.raw_dir / "camera" / "sparql_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.rate_limit = settings.http_rate_limit_seconds
        self._client = httpx.Client(
            timeout=settings.http_timeout,
            headers={"User-Agent": settings.user_agent},
            follow_redirects=True,
        )
        self._last_request = 0.0

    def _cache_path(self, query: str) -> Path:
        digest = hashlib.sha256(query.encode("utf-8")).hexdigest()[:16]
        return self.cache_dir / f"{digest}.json"

    def select(self, query: str, use_cache: bool = True) -> list[dict[str, Any]]:
        """Esegue una SELECT e restituisce le binding come lista di dict {var: value}."""
        cache_path = self._cache_path(query)
        if use_cache and cache_path.exists():
            logger.debug("SPARQL cache hit %s", cache_path.name)
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            return self._parse_bindings(data)

        self._respect_rate_limit()
        logger.info("SPARQL query (%d chars) -> %s", len(query), self.endpoint)
        try:
            resp = self._client.get(
                self.endpoint,
                params={"query": query, "format": "json"},
                headers={"Accept": "application/sparql-results+json"},
            )
            resp.raise_for_status()
        except httpx.HTTPError as exc:  # rete / 5xx / timeout
            logger.error("SPARQL request fallita: %s", exc)
            raise
        data = resp.json()
        cache_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return self._parse_bindings(data)

    def select_paginated(
        self, query_template: str, page_size: int = 500, max_pages: int = 50
    ) -> list[dict[str, Any]]:
        """Pagina una query che contiene i token __LIMIT__ e __OFFSET__.

        Usa la sostituzione di token (non str.format) perché il corpo SPARQL
        contiene parentesi graffe letterali. Evita inoltre le aggregazioni
        pesanti che mandano in timeout l'endpoint.
        """
        out: list[dict[str, Any]] = []
        for page in range(max_pages):
            offset = page * page_size
            q = query_template.replace("__LIMIT__", str(page_size)).replace(
                "__OFFSET__", str(offset)
            )
            rows = self.select(q)
            if not rows:
                break
            out.extend(rows)
            if len(rows) < page_size:
                break
        return out

    def _respect_rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self._last_request = time.monotonic()

    @staticmethod
    def _parse_bindings(data: dict[str, Any]) -> list[dict[str, Any]]:
        bindings = data.get("results", {}).get("bindings", [])
        return [{k: v.get("value") for k, v in row.items()} for row in bindings]

    def close(self) -> None:
        self._client.close()
