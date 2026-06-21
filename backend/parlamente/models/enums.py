"""Enum condivisi.

`SourceLayer` è il cuore della separazione Fase 1 / Fase 2:
ogni documento, intervento e atto porta il proprio layer fin da subito, così
la Fase 2 (comunicazione pubblica / propaganda) si aggancia senza migrazioni.
"""

from __future__ import annotations

from enum import Enum


class SourceLayer(str, Enum):
    """Da dove proviene il contenuto."""

    OFFICIAL_INSTITUTIONAL = "official_institutional"
    PUBLIC_COMMUNICATION = "public_communication"


class SourceType(str, Enum):
    """Tipo specifico di fonte. `source_layer / source_type` identifica la fonte.

    L'enum è volutamente aperto all'estensione: i valori Fase 2 esistono già come
    documentazione del modello, ma non sono ancora popolati da nessun adapter.
    """

    # --- official_institutional ---
    CHAMBER_SPEECH = "chamber_speech"  # resoconto stenografico Assemblea
    COMMITTEE_SPEECH = "committee_speech"  # resoconto Commissione
    PARLIAMENTARY_QUESTION = "parliamentary_question"  # interrogazione/interpellanza
    MOTION = "motion"  # mozione
    RESOLUTION = "resolution"  # risoluzione
    AGENDA_ITEM = "agenda_item"  # ordine del giorno
    BILL = "bill"  # proposta / disegno di legge
    DEPUTY_PROFILE = "deputy_profile"  # scheda deputato/senatore

    # --- public_communication (Fase 2, non ancora popolati) ---
    FACEBOOK_POST = "facebook_post"
    INSTAGRAM_POST = "instagram_post"
    X_POST = "x_post"
    TIKTOK_POST = "tiktok_post"
    YOUTUBE_VIDEO = "youtube_video"
    INTERVIEW = "interview"
    PRESS_RELEASE = "press_release"
    NEWSLETTER = "newsletter"
    TALK_SHOW = "talk_show"

    @property
    def layer(self) -> SourceLayer:
        return (
            SourceLayer.PUBLIC_COMMUNICATION
            if self in _PUBLIC_TYPES
            else SourceLayer.OFFICIAL_INSTITUTIONAL
        )


_PUBLIC_TYPES = {
    SourceType.FACEBOOK_POST,
    SourceType.INSTAGRAM_POST,
    SourceType.X_POST,
    SourceType.TIKTOK_POST,
    SourceType.YOUTUBE_VIDEO,
    SourceType.INTERVIEW,
    SourceType.PRESS_RELEASE,
    SourceType.NEWSLETTER,
    SourceType.TALK_SHOW,
}


class Chamber(str, Enum):
    CAMERA = "camera"
    SENATO = "senato"
