"""Entry point FastAPI di Parla Mente."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .. import __version__
from .routers import compare, politicians

app = FastAPI(
    title="Parla Mente API",
    version=__version__,
    description=(
        "Capire di cosa parlano davvero deputati e senatori, partendo dalle fonti "
        "ufficiali. Ogni insight è riconducibile a una fonte tracciabile."
    ),
)

# Frontend Next.js in sviluppo locale.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(politicians.router)
app.include_router(compare.router)


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}
