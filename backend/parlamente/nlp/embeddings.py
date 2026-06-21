"""Livello C — Semantica / embeddings (STUB, predisposizione architetturale).

Obiettivi futuri (vedi README, roadmap):
- ricerca semantica su interventi/atti;
- similarità tra parlamentari e tra interventi;
- confronto tra ciò che si dice in Parlamento e ciò che si comunica fuori (Fase 2);
- clustering di temi emergenti (es. via BERTopic).

Modello suggerito: un sentence-transformer multilingua leggero
(es. "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2").
L'interfaccia è già definita; l'implementazione è opzionale (extra `nlp`).
"""

from __future__ import annotations

from typing import Protocol

DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class Embedder(Protocol):
    def encode(self, texts: list[str]) -> list[list[float]]:
        ...


class SentenceTransformerEmbedder:
    """Wrapper lazy: importa sentence-transformers solo all'uso, così il pacchetto
    base resta leggero."""

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self.model_name = model_name
        self._model = None

    def _ensure_model(self) -> None:
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:  # pragma: no cover - dipendenza opzionale
                raise ImportError(
                    "Livello C non disponibile: installa gli extra NLP "
                    "(`pip install -e 'backend[nlp]'`)."
                ) from exc
            self._model = SentenceTransformer(self.model_name)

    def encode(self, texts: list[str]) -> list[list[float]]:
        self._ensure_model()
        assert self._model is not None
        return self._model.encode(texts, normalize_embeddings=True).tolist()
