"""Adapter REALE dei deputati via SPARQL dati.camera.it.

Schema OCD verificato sull'endpoint:
- classe        : ocd:deputato
- legislatura   : ocd:rif_leg -> .../legislatura.rdf/repubblica_<N>
- cognome/nome  : foaf:surname / foaf:firstName
- gruppo        : ocd:aderisce -> nodo con rdfs:label "<GRUPPO> (<date>)"

Un deputato può avere più adesioni a gruppo nel tempo: scegliamo l'adesione più
recente (etichetta con data di inizio più alta) come gruppo "corrente".
"""

from __future__ import annotations

import re
from datetime import date as date_type

from ...logging import get_logger
from ...models import Chamber, Politician
from ..base import SourceAdapter
from .sparql import SparqlClient

logger = get_logger(__name__)

def _deputies_query(leg: str) -> str:
    """Query paginabile: i token __LIMIT__/__OFFSET__ sono sostituiti da select_paginated."""
    return f"""
PREFIX ocd: <http://dati.camera.it/ocd/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?dep ?cognome ?nome ?gruppo WHERE {{
  ?dep a ocd:deputato ;
       ocd:rif_leg <http://dati.camera.it/ocd/legislatura.rdf/repubblica_{leg}> ;
       foaf:surname ?cognome ;
       foaf:firstName ?nome .
  OPTIONAL {{ ?dep ocd:aderisce ?ad . ?ad rdfs:label ?gruppo }}
}}
ORDER BY ?dep
LIMIT __LIMIT__ OFFSET __OFFSET__
"""

_DATE_IN_LABEL = re.compile(r"\((\d{2})\.(\d{2})\.(\d{4})")


def _group_start_date(label: str) -> date_type:
    """Estrae la data di inizio dall'etichetta del gruppo, per ordinare le adesioni."""
    m = _DATE_IN_LABEL.search(label or "")
    if not m:
        return date_type.min
    day, month, year = (int(x) for x in m.groups())
    try:
        return date_type(year, month, day)
    except ValueError:
        return date_type.min


def _deputy_local_id(dep_uri: str) -> str:
    # http://dati.camera.it/ocd/deputato.rdf/d309220_19 -> d309220_19
    return dep_uri.rstrip("/").split("/")[-1]


class CameraDeputiesAdapter(SourceAdapter):
    source_name = "Camera dei Deputati"

    def __init__(self, client: SparqlClient | None = None) -> None:
        self.client = client or SparqlClient()

    def fetch_politicians(self, legislature: str) -> list[Politician]:
        query = _deputies_query(legislature)
        rows = self.client.select_paginated(query, page_size=500)
        logger.info("Camera: %d righe deputato/gruppo (legislatura %s)", len(rows), legislature)

        # Raggruppa per deputato e scegli l'adesione di gruppo più recente.
        by_dep: dict[str, dict] = {}
        for r in rows:
            dep_uri = r.get("dep")
            if not dep_uri:
                continue
            local_id = _deputy_local_id(dep_uri)
            entry = by_dep.setdefault(
                local_id,
                {
                    "dep_uri": dep_uri,
                    "cognome": r.get("cognome", ""),
                    "nome": r.get("nome", ""),
                    "group": None,
                    "group_date": date_type.min,
                },
            )
            gruppo = r.get("gruppo")
            if gruppo:
                start = _group_start_date(gruppo)
                if start >= entry["group_date"]:
                    entry["group"] = gruppo
                    entry["group_date"] = start

        politicians: list[Politician] = []
        for local_id, e in by_dep.items():
            cognome = (e["cognome"] or "").strip()
            nome = (e["nome"] or "").strip()
            full_name = f"{nome} {cognome}".strip().title()
            politicians.append(
                Politician(
                    id=f"camera_{local_id}",
                    full_name=full_name,
                    first_name=nome.title() or None,
                    last_name=cognome.title() or None,
                    chamber=Chamber.CAMERA,
                    group_name=e["group"],
                    legislature=str(legislature),
                    official_url=e["dep_uri"],
                    metadata={"ocd_uri": e["dep_uri"]},
                )
            )
        politicians.sort(key=lambda p: p.full_name)
        logger.info("Camera: %d deputati normalizzati", len(politicians))
        return politicians
