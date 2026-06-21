"""Fase 2 — Public Communication / Propaganda Layer (STUB, non attivo).

Questi adapter producono gli stessi modelli normalizzati (Intervention/Document)
ma con `source_layer = PUBLIC_COMMUNICATION` e `source_type` social/media.
Restano deliberatamente vuoti: la Fase 1 usa SOLO fonti ufficiali istituzionali.

Quando popolati, abiliteranno la metrica chiave "Official vs Public Communication
Gap" (vedi docs/phase2-gap.md e analysis/compare.py).
"""

from .base import PublicCommunicationAdapter

__all__ = ["PublicCommunicationAdapter"]
