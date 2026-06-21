"""Adapter per il Senato della Repubblica — STUB documentati (Fase 1.b).

Il Senato pubblica open data (dati.senato.it, anch'esso con endpoint SPARQL) con
un'ontologia diversa da quella della Camera. Gli adapter qui replicano i contratti
della Camera così che l'estensione sia un semplice riempimento, senza toccare
pipeline, storage o UI.
"""

from .senators import SenateSenatorsAdapter

__all__ = ["SenateSenatorsAdapter"]
