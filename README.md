# Parla Mente

**Capire di cosa parlano davvero deputati e senatori, partendo dalle fonti ufficiali.**

Parla Mente è l'evoluzione di [Wordspread](https://github.com/nmaiese/wordspread):
da esperimento statico di word cloud sui post social di due politici, a
piattaforma **data-driven, verificabile e trasparente** che mostra **di quali
temi si occupano davvero i parlamentari italiani**, sulla base di **fonti
parlamentari ufficiali**.

> Ogni insight mostrato nell'interfaccia è ricondotto a una **fonte ufficiale
> tracciabile** (URL, data, organo, tipo documento, parlamentare). Nessuna sintesi
> inventata: dove una fonte non è ancora parsabile in modo affidabile, lo
> dichiariamo (vedi [docs/sources-limits.md](docs/sources-limits.md)).

## Da Wordspread a Parla Mente

| | Wordspread (legacy) | Parla Mente |
|---|---|---|
| Fonte | post Facebook/Twitter | resoconti e atti ufficiali della Camera |
| Soggetti | 2 politici hardcoded (Salvini/Di Maio) | tutti i deputati (modello dati generico) |
| Output | word cloud + tabella | **mappa tematica verificabile** + evidence + fonti |
| Stack | pandas/gensim, D3 v3, JSON statici | pydantic/DuckDB/scikit-learn, FastAPI, Next.js |

La word cloud resta come **elemento identitario**, ma non è il centro dell'app:
il centro è la mappa tematica con evidence verificabile.

## Le due fasi

- **Fase 1 — Official Institutional Layer** (questo MVP): **solo** fonti ufficiali
  istituzionali (Camera dei Deputati; Senato predisposto come stub).
- **Fase 2 — Public Communication / Propaganda Layer** (predisposta, non attiva):
  social, interviste, comunicati, talk show… per misurare lo scarto tra ciò che un
  parlamentare *fa nelle sedi ufficiali* e ciò che *comunica all'esterno*
  (**Official vs Public Communication Gap**). Vedi
  [docs/phase2-gap.md](docs/phase2-gap.md).

`source_layer` e `source_type` sono già nei modelli e nello storage: la Fase 2 si
aggancia senza migrazioni.

## Struttura

```
parlamente/
  apps/legacy-wordspread/   # archivio storico di Wordspread (non eseguito)
  backend/                  # package python "parlamente": ingestion, NLP, storage, API, CLI
  frontend/                 # Next.js (Home, Parlamentare, Confronto)
  data/                     # raw/processed/db (gitignored) + fixtures reali (tracked)
  docs/                     # architettura, limiti fonti, gap Fase 2
```

Dettagli architetturali in [docs/architecture.md](docs/architecture.md).

## Fonti ufficiali (Fase 1)

- **Deputati** — endpoint SPARQL `dati.camera.it/sparql` (REALE): ~414 deputati
  della XIX legislatura con nome e gruppo.
- **Resoconti stenografici dell'Assemblea** — parser REALE dei resoconti pubblicati
  dalla Camera, con attribuzione di ogni intervento al deputato corretto
  (`idPersona`). Per l'MVP si leggono fixtures **reali** già scaricate.
- **Atti** (interrogazioni, mozioni, proposte di legge) — adapter predisposto;
  parsing reale da completare (vedi limiti).
- **Senato**, **Commissioni** — stub documentati.

## Installazione

Requisiti: Python ≥ 3.11, Node ≥ 18.

```bash
git clone <questo-repo> && cd parlamente
cp .env.example .env

# Backend
python -m venv .venv && source .venv/bin/activate
pip install -e backend

# Frontend
cd frontend && cp .env.local.example .env.local && npm install && cd ..
```

## Esecuzione (pipeline)

```bash
# 1) anagrafica deputati (SPARQL reale)
parlamente ingest deputies --source camera --legislature 19
# 2) resoconti/interventi (fixtures reali; --live per parsare dal vivo)
parlamente ingest speeches --source camera
# 3) NLP
parlamente nlp keywords
parlamente nlp topics
# stato
parlamente db stats
```

(Ri)generare le fixtures reali dai resoconti pubblicati:

```bash
cd backend && python scripts/build_camera_fixtures.py --sedute 4
```

## Avvio dell'app

```bash
# terminale 1 — API
parlamente api          # http://127.0.0.1:8000  (/docs per OpenAPI)
# terminale 2 — UI
cd frontend && npm run dev   # http://localhost:3000
```

UI: **Home** (ricerca + filtri) → **Pagina Parlamentare** (KPI, top temi, evidence
con citazioni e link fonte, word cloud, tabella interventi) → **Confronto** A vs B.

## Esempio di output (logico)

```
Parlamentare: Fabio Rampelli — Camera dei Deputati — FRATELLI D'ITALIA
Periodo: 2026-06-16 → 2026-06-19 · 13 interventi analizzati

Top temi:
  Università — 100%   (medicina/ricerca/reclutamento)

Evidence (Università):
  «…del disegno di legge n. 2735: Revisione delle modalità di accesso,
   valutazione e reclutamento del personale ricercatore…»
  → Resoconto stenografico dell'Assemblea, 2026-06-19 [link fonte ufficiale]
```

## Test

```bash
cd backend && pytest        # 13 test, nessuna rete
```

## Limiti noti

- **Atti** non ancora popolati (attribuzione atto→firmatario via SPARQL non
  risolta; adapter predisposto). Dettagli in
  [docs/sources-limits.md](docs/sources-limits.md).
- Molti interventi d'Assemblea sono procedurali: alcuni deputati mostrano pochi
  temi sostanziali. Le aggregazioni SPARQL pesanti vanno in timeout (504): il
  client usa SELECT paginate + cache.
- Senato, embeddings (Livello C) e Fase 2 (social) sono stub.

## Roadmap

1. **Fase 1.b** — atti Camera, resoconti di Commissione, Senato.
2. **Livello C** — embeddings multilingua: ricerca semantica, similarità tra
   parlamentari/interventi, clustering di temi emergenti.
3. **Fase 2** — `public_communication` + metrica *Official vs Public Communication
   Gap* (vedi [docs/phase2-gap.md](docs/phase2-gap.md)).

## Vincoli etici e tecnici

Niente dati inventati · rispetto di robots.txt e rate-limit · caching locale ·
logging dei download · gestione errori HTTP · nessuna chiave/segreto o dato
pesante nel repository.

## Licenza

MIT. Pensato per evolvere in un progetto pubblico di data journalism / civic tech.
