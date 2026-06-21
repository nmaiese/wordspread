"""Pipeline NLP sui dati già normalizzati nello storage.

- run_keywords: estrae le keyword distintive PER PARLAMENTARE (un documento del
  corpus = tutto il testo di quel parlamentare) e le salva in `keywords`.
- run_topics : classifica ogni intervento e ogni atto sui topic della tassonomia
  e salva le assegnazioni in `intervention_topics`. Salva anche i topic stessi.

Entrambe sono riproducibili e idempotenti (riscrivono le rispettive tabelle).
"""

from __future__ import annotations

from collections import defaultdict

from ..logging import get_logger
from ..models import Keyword, TopicAssignment
from ..nlp.keywords import KeywordExtractor
from ..nlp.taxonomy import classify, taxonomy_as_models
from ..storage.repositories import Repositories

logger = get_logger(__name__)


def run_keywords(repo: Repositories, top_n: int = 30) -> int:
    """Una entry del corpus per parlamentare; salva top-N keyword per ciascuno."""
    interventions = repo.all_interventions()
    acts = repo.all_acts()

    texts_by_pol: dict[str, list[str]] = defaultdict(list)
    for row in interventions:
        texts_by_pol[row["politician_id"]].append(row["text"] or "")
    for row in acts:
        texts_by_pol[row["politician_id"]].append(
            f"{row.get('title', '')} {row.get('text', '')}"
        )

    pol_ids = list(texts_by_pol.keys())
    corpus = [" ".join(texts_by_pol[pid]) for pid in pol_ids]
    if not corpus:
        logger.warning("run_keywords: nessun testo da elaborare")
        return 0

    extractor = KeywordExtractor(ngram_range=(1, 3))
    per_doc = extractor.extract_per_document(corpus, top_n=top_n)

    keywords: list[Keyword] = []
    for pid, scores in zip(pol_ids, per_doc):
        for ks in scores:
            keywords.append(
                Keyword(
                    entity_type="politician",
                    entity_id=pid,
                    keyword=ks.keyword,
                    score=ks.score,
                    frequency=ks.frequency,
                )
            )
    n = repo.replace_keywords_for("politician", keywords)
    logger.info("run_keywords: %d keyword salvate per %d parlamentari", n, len(pol_ids))
    return n


def run_topics(repo: Repositories, threshold: float = 1.0) -> int:
    """Classifica interventi e atti; salva topic e assegnazioni."""
    repo.upsert_topics(taxonomy_as_models())

    assignments: list[TopicAssignment] = []
    for row in repo.all_interventions():
        for topic_id, score in classify(row["text"] or "", threshold=threshold):
            assignments.append(
                TopicAssignment(
                    entity_type="intervention",
                    entity_id=row["id"],
                    topic_id=topic_id,
                    score=score,
                )
            )
    for row in repo.all_acts():
        text = f"{row.get('title', '')} {row.get('text', '')}"
        for topic_id, score in classify(text, threshold=threshold):
            assignments.append(
                TopicAssignment(
                    entity_type="act",
                    entity_id=row["id"],
                    topic_id=topic_id,
                    score=score,
                )
            )

    n = repo.replace_topic_assignments(assignments)
    logger.info("run_topics: %d assegnazioni topic salvate", n)
    return n
