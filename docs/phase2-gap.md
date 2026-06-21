# Fase 2 — Official vs Public Communication Gap

> Stato: **non implementata**. Questo documento descrive *come* la Fase 2 si
> aggancia all'architettura della Fase 1, così che aggiungerla sia naturale.

## Idea

La Fase 1 misura di cosa si occupa un parlamentare **nelle sedi ufficiali**
(`source_layer = official_institutional`). La Fase 2 aggiunge ciò che lo stesso
parlamentare **comunica all'esterno** (`source_layer = public_communication`:
social, interviste, comunicati, talk show…). Confrontando i due layer si misura
lo scarto tra *attività istituzionale* e *comunicazione/propaganda*.

## Come l'architettura è già predisposta

1. **Modelli** — `SourceDocument`/`Intervention`/`Act` portano già `source_layer`
   e `source_type` (vedi `models/enums.py`). Nessuna migrazione necessaria.
2. **Adapter** — `sources/public_communication/` contiene già gli stub
   (`facebook`, `instagram`, `interviews`, `press_releases`) che ereditano
   `PublicCommunicationAdapter` (layer fissato a `public_communication`) e
   producono gli **stessi modelli normalizzati**. La pipeline di ingestion non
   cambia.
3. **Storage** — le stesse tabelle (`interventions`, `intervention_topics`,
   `keywords`) ospitano entrambi i layer: basta filtrare per `source_layer`.
4. **Analisi** — `analysis/compare.py` espone già le firme:
   - `compare_official_vs_public(politician_id, period)`
   - `calculate_topic_gap(politician_id, topic_id, period)`
   - `calculate_rhetoric_gap(politician_id, period)`

## Metriche previste

Per un parlamentare e un periodo:

- **Topic gap** per tema *t*:
  `gap(t) = share_public(t) − share_official(t)`
  - `gap > 0` → comunica *t* fuori più di quanto vi lavori in Parlamento
    (es. parla molto di "sicurezza" sui social ma presenta pochi atti);
  - `gap < 0` → lavora *t* nelle sedi ufficiali ma lo comunica poco fuori.

- **Rhetoric gap**: differenza lessicale/di registro tra i due layer
  (es. divergenza tra distribuzioni di keyword TF-IDF dei due layer, o distanza
  coseno tra gli embedding — Livello C, `nlp/embeddings.py`).

- **Communication-vs-action index**: sintesi aggregata dei topic gap, pesata per
  volume, che riassume quanto la comunicazione esterna rispecchia l'attività
  istituzionale.

## Vincoli e cautele (Fase 2)

- Rispetto di ToS/API delle piattaforme; niente scraping aggressivo.
- Attribuzione certa account → parlamentare (account ufficiali verificati).
- Le metriche restano **evidence-based**: ogni punto del gap deve poter elencare
  i contenuti (ufficiali e pubblici) che lo generano, con link.
