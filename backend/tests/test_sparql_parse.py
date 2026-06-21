"""Test del parsing SPARQL su una risposta fixture salvata — nessuna rete."""

from parlamente.sources.camera.deputies import _deputy_local_id, _group_start_date
from parlamente.sources.camera.sparql import SparqlClient

# Forma reale di una risposta SPARQL JSON dell'endpoint dati.camera.it.
SAMPLE = {
    "head": {"vars": ["dep", "cognome", "nome", "gruppo"]},
    "results": {
        "bindings": [
            {
                "dep": {"type": "uri", "value": "http://dati.camera.it/ocd/deputato.rdf/d301531_19"},
                "cognome": {"type": "literal", "value": "CARFAGNA"},
                "nome": {"type": "literal", "value": "MARIA ROSARIA"},
                "gruppo": {"type": "literal", "value": "MISTO (24.09.2024-30.10.2024)"},
            }
        ]
    },
}


def test_parse_bindings_flattens_values():
    rows = SparqlClient._parse_bindings(SAMPLE)
    assert rows == [
        {
            "dep": "http://dati.camera.it/ocd/deputato.rdf/d301531_19",
            "cognome": "CARFAGNA",
            "nome": "MARIA ROSARIA",
            "gruppo": "MISTO (24.09.2024-30.10.2024)",
        }
    ]


def test_deputy_local_id():
    assert _deputy_local_id("http://dati.camera.it/ocd/deputato.rdf/d301531_19") == "d301531_19"


def test_group_start_date_picks_label_date():
    d1 = _group_start_date("PARTITO X (07.01.2025)")
    d2 = _group_start_date("MISTO (24.09.2024-30.10.2024)")
    assert d1.year == 2025 and d1.month == 1 and d1.day == 7
    assert d2.year == 2024 and d2.month == 9
    assert d1 > d2  # la label più recente vince come gruppo corrente
