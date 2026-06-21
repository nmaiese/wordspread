"""Test end-to-end della pipeline su DB temporaneo, senza rete."""

from datetime import date

import pytest

from parlamente.analysis.pipeline import run_keywords, run_topics
from parlamente.analysis.profile import build_profile
from parlamente.models import Chamber, Intervention, Politician
from parlamente.storage.db import Database
from parlamente.storage.repositories import Repositories


@pytest.fixture
def repo(tmp_path):
    db = Database(tmp_path / "test.duckdb")
    db.init_schema()
    return Repositories(db)


def _seed(repo: Repositories):
    repo.upsert_politicians(
        [
            Politician(
                id="camera_d1_19",
                full_name="Mario Rossi",
                chamber=Chamber.CAMERA,
                group_name="Gruppo X",
                legislature="19",
            )
        ]
    )
    repo.upsert_interventions(
        [
            Intervention(
                id="i1",
                politician_id="camera_d1_19",
                politician_name="Mario Rossi",
                document_id="doc1",
                date=date(2025, 5, 18),
                chamber=Chamber.CAMERA,
                context="Assemblea",
                text="Le liste d'attesa nella sanità sono inaccettabili, serve medicina territoriale.",
                source_url="https://documenti.camera.it/x",
            ),
            Intervention(
                id="i2",
                politician_id="camera_d1_19",
                politician_name="Mario Rossi",
                document_id="doc1",
                date=date(2025, 6, 2),
                chamber=Chamber.CAMERA,
                context="Assemblea",
                text="Il salario minimo è una priorità per l'occupazione e i lavoratori.",
                source_url="https://documenti.camera.it/y",
            ),
        ]
    )


def test_pipeline_and_profile(repo):
    _seed(repo)
    assert run_keywords(repo) > 0
    assert run_topics(repo) > 0

    profile = build_profile(repo, "camera_d1_19")
    assert profile is not None
    assert profile["kpi"]["intervention_count"] == 2

    topics = {t["topic_id"] for t in profile["top_topics"]}
    assert "san_liste_attesa" in topics or "lav_salario_minimo" in topics

    # ogni evidence deve avere un URL fonte (tracciabilità)
    for te in profile["evidence"]:
        for item in te["evidence"]:
            assert item["url"].startswith("http")


def test_profile_missing_politician(repo):
    assert build_profile(repo, "inesistente") is None
