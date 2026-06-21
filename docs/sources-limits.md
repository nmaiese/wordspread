# Note tecniche sui limiti delle fonti ufficiali (Fase 1)

Documentazione onesta dei limiti incontrati e delle scelte fatte. Aggiornare man
mano che gli adapter reali vengono completati.

## Camera dei Deputati — SPARQL (dati.camera.it)

- **Endpoint**: `https://dati.camera.it/sparql` — vivo, risponde JSON SPARQL.
- **Deputati (REALE, funzionante)**: classe `ocd:deputato`, legislatura via
  `ocd:rif_leg` → `.../legislatura.rdf/repubblica_19`, nome via
  `foaf:surname`/`foaf:firstName`, gruppo via `ocd:aderisce` → `rdfs:label`.
  L'adapter `sources/camera/deputies.py` estrae ~414 deputati della XIX
  legislatura con nome e gruppo corrente.
- **Limite — timeout su aggregazioni**: query con `GROUP BY`/`COUNT` su grandi
  insiemi restituiscono **HTTP 504**. Per questo il client
  (`sources/camera/sparql.py`) usa **SELECT mirate con paginazione**
  (`__LIMIT__`/`__OFFSET__`) e **cache su disco**, evitando le aggregazioni.
- **Limite — gruppo "corrente"**: un deputato ha più adesioni nel tempo; si
  sceglie quella con data di inizio più recente (parsing della data
  nell'etichetta del gruppo). Euristica, non perfetta.
- **Atti via SPARQL — non risolto**: la classe `ocd:atto` copre tutte le
  legislature (anche storiche) e nel grafo **titolo e firmatario stanno su
  risorse diverse** (`?atto dc:title ?t ; ocd:rif_firmatario ?f` restituisce 0
  righe). Il path ontologico corretto per legare atto→primo firmatario nella
  legislatura corrente non è stato individuato in tempi ragionevoli e
  `dct:isReferencedBy` sul deputato risulta vuoto. → **Atti rimandati**: adapter
  `sources/camera/acts.py` predisposto (legge fixtures `acts*.json`), parsing
  reale da completare.

## Camera dei Deputati — Resoconti stenografici (REALE, funzionante)

- **Fonte**: indice `https://www.camera.it/leg19/207`; documento per seduta via
  `documenti.camera.it/.../getDocumento.ashx?...&tipoDoc=stenografico&idSeduta=NNNN`.
- **robots.txt**: `User-agent: *` senza `Disallow` → consultazione consentita.
  Manteniamo comunque User-Agent dedicato, rate-limit e cache.
- **Attribuzione (chiave)**: ogni `<p class="intervento">` contiene un link alla
  scheda con `idPersona=NNNNNN`. Mapping verificato:
  `idPersona NNNNNN` → deputato `camera_dNNNNNN_19`. Questo lega in modo
  affidabile l'intervento al deputato.
- **Filtri**: si tengono gli interventi con testo ≥ 200 caratteri (si escludono i
  meri richiami procedurali). Molti interventi d'Assemblea restano procedurali:
  è normale che alcuni deputati mostrino pochi temi sostanziali.
- **Fixtures**: `scripts/build_camera_fixtures.py` esegue il parser live su poche
  sedute recenti e salva l'output **reale** in `data/fixtures/camera/`
  (documenti veri, URL e date veri). Le fixtures **non contengono dati inventati**.

## Commissioni / Senato

- **Commissioni** (`sources/camera/committees.py`): stub. Struttura analoga ai
  resoconti d'Assemblea, con `context` = nome Commissione e
  `source_type = committee_speech`.
- **Senato** (`sources/senate/*`): stub. Endpoint open data dedicato
  (`dati.senato.it/sparql`) con ontologia diversa; gli adapter replicano i
  contratti della Camera per un'estensione a basso attrito.

## Principio di integrità

Nessun dato è inventato. Ogni intervento mostrato in UI è ricondotto al resoconto
ufficiale (URL + data + seduta) e al deputato (idPersona). Dove una fonte non è
ancora parsabile in modo affidabile (atti), lo dichiariamo e lasciamo l'adapter
predisposto, senza riempire i vuoti con contenuti sintetici.
