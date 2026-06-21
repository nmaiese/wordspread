from datetime import date

from parlamente.models import (
    Chamber,
    Intervention,
    Politician,
    SourceLayer,
    SourceType,
)


def test_politician_minimal():
    p = Politician(
        id="camera_d1_19",
        full_name="Mario Rossi",
        chamber=Chamber.CAMERA,
        legislature="19",
    )
    assert p.chamber == Chamber.CAMERA
    assert p.metadata == {}


def test_intervention_default_layer_is_official():
    i = Intervention(
        id="x",
        politician_id="camera_d1_19",
        politician_name="Mario Rossi",
        document_id="doc1",
        date=date(2025, 5, 18),
        chamber=Chamber.CAMERA,
        context="Assemblea",
        text="liste d'attesa e medicina territoriale",
        source_url="https://example.org",
    )
    assert i.source_layer == SourceLayer.OFFICIAL_INSTITUTIONAL
    assert i.source_type == SourceType.CHAMBER_SPEECH


def test_source_type_layer_mapping():
    assert SourceType.FACEBOOK_POST.layer == SourceLayer.PUBLIC_COMMUNICATION
    assert SourceType.CHAMBER_SPEECH.layer == SourceLayer.OFFICIAL_INSTITUTIONAL
