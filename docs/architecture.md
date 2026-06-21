# Architettura — Parla Mente

```
┌─────────────┐   adapters    ┌──────────────┐   pipeline    ┌────────────┐
│  Fonti      │ ────────────▶ │  Modelli     │ ────────────▶ │  Storage   │
│  ufficiali  │  (normalizz.) │  normalizzati│  (NLP)        │  DuckDB    │
│  (SPARQL,   │               │  pydantic    │               │            │
│  resoconti) │               └──────────────┘               └─────┬──────┘
└─────────────┘                                                     │
                                                                    ▼
                                              ┌──────────────┐  ┌────────────┐
                                              │  FastAPI     │◀─│  analysis  │
                                              │  (REST)      │  │ profile/   │
                                              └──────┬───────┘  │ evidence/  │
                                                     │          │ compare    │
                                                     ▼          └────────────┘
                                              ┌──────────────┐
                                              │  Next.js     │
                                              │  (UI)        │
                                              └──────────────┘
```

## Separazione dei livelli

- **ingestion** (`sources/`) — un adapter per fonte; restituisce **solo** modelli
  normalizzati (`models/`). Nessun DataFrame grezzo fuori da qui.
- **processing** (`nlp/`, `analysis/`) — keyword (TF-IDF + n-grammi), tassonomia
  controllata keyword-based, evidence, profili, confronti.
- **storage** (`storage/`) — DuckDB dietro un repository; schema con tipi standard
  per migrare a PostgreSQL senza riscrivere le query.
- **api** (`api/`) — FastAPI; risposte già con i campi-fonte per la tracciabilità.
- **ui** (`frontend/`) — Next.js; il centro è la **mappa tematica verificabile**,
  la word cloud è un elemento identitario secondario.

## Separazione dei layer di fonte (Fase 1 vs 2)

`SourceLayer ∈ {official_institutional, public_communication}` è presente nei
modelli e nello storage fin dall'inizio. La Fase 1 popola **solo**
`official_institutional`. La Fase 2 (stub in `sources/public_communication/`)
aggiungerà `public_communication` riusando la stessa pipeline. Vedi
[phase2-gap.md](phase2-gap.md).

## NLP a tre livelli

- **A — Keyword** (`nlp/keywords.py`): TF-IDF + frequenze, n-grammi 1..3,
  stopword IT + rumore parlamentare.
- **B — Tassonomia** (`nlp/taxonomy.py` + `topics.yaml`): 40 temi su 10 macro-aree,
  classificazione keyword-based **trasparente** (ogni assegnazione deriva da match
  espliciti, non da una scatola nera).
- **C — Embeddings** (`nlp/embeddings.py`): stub multilingua per ricerca
  semantica/similarità (fase successiva, extra `nlp`).
