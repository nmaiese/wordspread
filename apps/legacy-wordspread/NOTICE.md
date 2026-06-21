# Legacy Wordspread — archivio di riferimento

Questa cartella conserva la versione **storica** di Wordspread (≈2018), mantenuta
come riferimento e archivio. **Non è eseguita** dalla nuova applicazione *Parla
Mente* e non va modificata.

## Cosa c'è
- `main.py`, `text_process.py`, `topic_modeling.py`, `twitter_api.py` — pipeline
  Python originale (CSV Facebook/Twitter → TF-IDF → JSON statici).
- `custom_stopword_tokens.py` — lista di stopword italiane (riusata, in forma
  modernizzata, in `backend/parlamente/nlp/stopwords_it.py`).
- `index.html`, `wordcloud.html`, `assets/js/word-cloud.js`,
  `assets/js/d3linechart.js`, `assets/js/graph.js` — frontend statico originale e
  la **word cloud** (elemento identitario, riproposto nella nuova UI in forma
  alleggerita).

## Cosa NON è stato vendored (di proposito)
- I dataset pesanti `data/*.json`, `data/*.csv`, i modelli gensim `*.npy`/`*.lda`/
  `*.lsi` — hardcoded su singoli politici (Salvini/Di Maio/Renzi), fuori scopo per
  la nuova piattaforma e troppo pesanti per il repository.
- Le librerie di terze parti (Bootstrap, jQuery, D3, DataTables) sotto `assets/`.

Il sorgente completo storico resta disponibile su GitHub:
<https://github.com/nmaiese/wordspread>.

## Perché è qui
La nuova app riusa due cose dal legacy: la **lista di stopword italiane** e il
**concetto di word cloud / TF-IDF**. Tutto il resto è stato riscritto: vedi il
README principale per il razionale della trasformazione da Wordspread (social,
2 politici hardcoded) a Parla Mente (fonti ufficiali, modello dati generico).
