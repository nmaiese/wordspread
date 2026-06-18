# Wordspread

Wordspread is a static data visualization experiment for comparing the language
used in public political Facebook posts. It uses TF-IDF scores, word clouds,
timelines and searchable tables to inspect how relevant words change over time.

The included dataset focuses on Italian political communication from the
original analysis period.

## Features

- Compare significant words between two public pages.
- Explore monthly word relevance through interactive word clouds.
- Filter posts by selected terms.
- Generate TF-IDF datasets from exported Facebook/Twitter text data.

## Stack

- Python
- pandas
- scikit-learn
- gensim
- D3.js
- DataTables
- Bootstrap

## Run Locally

The visualization can be opened from `index.html` when served by a local static
server:

```bash
python -m http.server 8000
```

Then open:

```text
http://127.0.0.1:8000
```

The Python scripts are used to regenerate processed datasets. Dependencies are
pinned to the original development period and may require an older Python
environment.

## Project Status

This repository is kept public as a portfolio/archive project. It is not
actively maintained, and the dataset reflects the original analysis period.
