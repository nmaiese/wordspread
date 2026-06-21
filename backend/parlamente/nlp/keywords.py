"""Livello A — Keyword extraction.

Versione moderna della vecchia pipeline TF-IDF di Wordspread:
- scikit-learn moderno (`get_feature_names_out`, niente API deprecate);
- TF-IDF per le parole/locuzioni distintive + frequenze grezze (CountVectorizer);
- n-grammi 1..3 -> cattura "liste d'attesa", "medicina territoriale",
  "salario minimo", "autonomia differenziata", ecc.;
- stopword italiane + rumore parlamentare.
"""

from __future__ import annotations

from dataclasses import dataclass

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from ..logging import get_logger
from .stopwords_it import get_italian_stopwords

logger = get_logger(__name__)


@dataclass
class KeywordScore:
    keyword: str
    score: float
    frequency: int


class KeywordExtractor:
    """Estrae keyword distintive da un corpus di documenti (un doc = un parlamentare,
    oppure un doc = un intervento, a seconda dell'uso)."""

    def __init__(
        self,
        ngram_range: tuple[int, int] = (1, 3),
        min_df: int = 1,
        max_df: float = 0.9,
        stopwords: list[str] | None = None,
    ) -> None:
        self.stopwords = stopwords or get_italian_stopwords()
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df

    def _build_vectorizers(self, n_docs: int) -> tuple[TfidfVectorizer, CountVectorizer]:
        # Su corpora piccoli max_df in frazione può scendere sotto min_df: disattivalo.
        max_df = 1.0 if int(self.max_df * n_docs) < self.min_df else self.max_df
        common = dict(
            analyzer="word",
            ngram_range=self.ngram_range,
            strip_accents="ascii",
            stop_words=self.stopwords,
            min_df=self.min_df,
            max_df=max_df,
            token_pattern=r"(?u)\b[a-zàèéìòù][a-zàèéìòù'\-]{2,}\b",
        )
        tfidf = TfidfVectorizer(use_idf=True, sublinear_tf=True, **common)
        count = CountVectorizer(**common)
        return tfidf, count

    def extract_per_document(
        self, documents: list[str], top_n: int = 30
    ) -> list[list[KeywordScore]]:
        """Per ogni documento del corpus, restituisce le top-N keyword TF-IDF
        con la relativa frequenza grezza."""
        if not documents:
            return []
        tfidf, count = self._build_vectorizers(len(documents))
        try:
            tfidf_matrix = tfidf.fit_transform(documents)
            count_matrix = count.fit_transform(documents)
        except ValueError as exc:
            # corpus troppo piccolo / solo stopword
            logger.warning("KeywordExtractor: vocabolario vuoto (%s)", exc)
            return [[] for _ in documents]

        tfidf_names = tfidf.get_feature_names_out()
        count_names = count.get_feature_names_out()
        count_index = {name: i for i, name in enumerate(count_names)}

        results: list[list[KeywordScore]] = []
        count_dense = count_matrix.toarray()
        for row_idx in range(tfidf_matrix.shape[0]):
            row = tfidf_matrix.getrow(row_idx)
            pairs = sorted(
                zip(row.indices, row.data), key=lambda p: p[1], reverse=True
            )[:top_n]
            scored: list[KeywordScore] = []
            for col, score in pairs:
                term = tfidf_names[col]
                freq = 0
                ci = count_index.get(term)
                if ci is not None:
                    freq = int(count_dense[row_idx, ci])
                scored.append(KeywordScore(keyword=term, score=float(score), frequency=freq))
            results.append(scored)
        return results
