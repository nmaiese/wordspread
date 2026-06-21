"""Source adapter: ogni fonte restituisce oggetti normalizzati (models.*),
mai DataFrame grezzi."""

from .base import SourceAdapter

__all__ = ["SourceAdapter"]
