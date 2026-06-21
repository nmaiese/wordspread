"""Senatori — STUB. Endpoint open data: https://dati.senato.it/sparql

TODO Fase 1.b: mappare l'ontologia del Senato (osr:) su `Politician`, analogamente
a CameraDeputiesAdapter. La forma di output normalizzata è identica.
"""

from __future__ import annotations

from ...models import Politician
from ..base import SourceAdapter


class SenateSenatorsAdapter(SourceAdapter):
    source_name = "Senato della Repubblica"

    def fetch_politicians(self, legislature: str) -> list[Politician]:
        raise NotImplementedError(
            "Adapter Senato non ancora implementato (Fase 1.b). "
            "Endpoint: https://dati.senato.it/sparql"
        )
