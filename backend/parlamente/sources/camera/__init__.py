"""Adapter per la Camera dei Deputati.

- `deputies`  : REALE, via endpoint SPARQL dati.camera.it.
- `speeches`  : adapter reale scaffolded + loader di fixtures (documenti reali
                scaricati una volta in data/fixtures/camera/).
- `acts`      : come speeches.
- `committees`: come speeches.
"""

from .deputies import CameraDeputiesAdapter

__all__ = ["CameraDeputiesAdapter"]
