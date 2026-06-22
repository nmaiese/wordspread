# Stato di avanzamento / Handoff

Ultimo aggiornamento: 2026-06-22

## Dove siamo

MVP **Parla Mente** completo e funzionante (Fase 1, solo fonti ufficiali Camera),
con tre bugfix runtime e ora uno **storico esteso** appena raccolto.

### Fatto e committato (branch `parla-mente` su `nmaiese/wordspread`)
- Backend `parlamente`: modelli pydantic, storage DuckDB, repository, CLI Typer,
  API FastAPI. NLP: stopword IT + rumore parlamentare, keyword TF-IDF n-grammi,
  tassonomia 40 temi/10 macro-aree keyword-based, evidence con citazioni+link.
- Ingestion Camera REALE: deputati via SPARQL (~414, leg. 19) + parser resoconti
  stenografici con attribuzione `idPersona` -> `camera_d<idPersona>_19`.
- Frontend Next.js: Home (ricerca/filtri), Pagina Parlamentare, Confronto A/B.
- Fase 2 predisposta (stub `public_communication`, `source_layer`/`source_type`,
  firme `compare_official_vs_public`/`calculate_*_gap`). Legacy in
  `apps/legacy-wordspread/`. 13 test verdi.
- **Bugfix**: API DuckDB in read-only (lock), date robuste (str|date),
  **connessione/cursore per-richiesta** (thread-safety: i 404/500 intermittenti).

### Storico esteso (questo step)
- Nuova modalità harvest per **range di idSeduta** (`speeches.py` `seduta_ids`,
  data ricavata dall'header del documento; `build_camera_fixtures.py`
  `--from-seduta/--to-seduta`).
- **Raccolta completa legislatura XIX**: 679 sedute, **28.620 interventi**,
  dal **2022-10-13** al **2026-06-19**. Fixtures in `data/fixtures/camera/`
  (~32 MB, committate).

## DA FARE quando si riprende (prossimi passi)

1. **Re-ingest + NLP sullo storico** (il DB locale `data/db/` è gitignored, va
   rigenerato):
   ```bash
   # ferma l'API se attiva (tiene il lock): pkill -f "uvicorn parlamente"
   cd backend && . ../.venv/bin/activate
   parlamente db reset
   parlamente ingest deputies
   parlamente ingest speeches      # ora carica 679 fixtures / 28.620 interventi
   parlamente nlp keywords
   parlamente nlp topics
   parlamente db stats
   # riavvia API:
   python -m uvicorn parlamente.api.main:app --host 127.0.0.1 --port 8000 &
   ```
   Con 28k interventi i profili avranno **molti più temi** e una vera timeline
   (2022 -> 2026). Verificare un paio di profili "ricchi" (es. capigruppo).

2. **Verificare performance** della classificazione topic su 28k interventi
   (regex per intervento: dovrebbe restare veloce; se lento, vettorizzare).

3. **Valutare il peso git** delle fixtures (32 MB): se eccessivo, opzioni:
   - gitignore del bulk + commit di un campione (es. ultime ~60 sedute) e
     rigenerazione via script per il resto; oppure
   - Git LFS per `data/fixtures/camera/*.json`.

4. **Atti** (interrogazioni/mozioni): ancora non popolati — vedi
   `docs/sources-limits.md` (link atto->firmatario SPARQL non risolto).

5. **Timeline UI**: ora che c'è storico reale 2022-2026, valutare un grafico vero
   (al momento la timeline è dati grezzi per macro-area/mese).

## Note operative
- Due ambienti Python: usare sempre il `.venv` del progetto (install editable).
- DuckDB single-writer: fermare l'API prima di `ingest`/`nlp`.
- Server locali (se attivi): API `:8000`, frontend `:3000`.
