"""Pulizia del testo italiano.

Riprende i concetti del legacy (`text_process.clean_text`): rimozione URL,
lowercase, tokenizzazione, filtro stopword — ma senza dipendere da NLTK
(usa una regex di tokenizzazione stabile, niente download di corpora).
"""

from __future__ import annotations

import re

_URL_RE = re.compile(r"http\S+|www\.\S+")
_WS_RE = re.compile(r"\s+")
# token = sequenza di lettere (incluse accentate) e apostrofo/trattino interni
_TOKEN_RE = re.compile(r"[a-zàáèéìíòóùúA-ZÀÁÈÉÌÍÒÓÙÚ][a-zàáèéìíòóùúA-ZÀÁÈÉÌÍÒÓÙÚ'\-]+")


def remove_urls(text: str) -> str:
    return _URL_RE.sub(" ", text)


def normalize_whitespace(text: str) -> str:
    return _WS_RE.sub(" ", text).strip()


def clean_text(text: str) -> str:
    """Restituisce testo lowercase, senza URL, normalizzato — pronto per il vectorizer."""
    text = remove_urls(text or "")
    return normalize_whitespace(text.lower())


def tokenize(text: str, stopwords: set[str] | None = None, min_len: int = 3) -> list[str]:
    """Tokenizza in parole significative, filtrando stopword e token corti."""
    stopwords = stopwords or set()
    tokens = _TOKEN_RE.findall((text or "").lower())
    return [t for t in tokens if len(t) >= min_len and t not in stopwords]
