"""CLI di Parla Mente (Typer).

Esempi:
    parlamente ingest deputies --source camera --legislature 19
    parlamente ingest speeches  --source camera
    parlamente ingest acts      --source camera
    parlamente nlp keywords
    parlamente nlp topics
    parlamente db reset
    parlamente api
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from .analysis.pipeline import run_keywords, run_topics
from .ingest import ingest_acts, ingest_deputies, ingest_speeches
from .logging import setup_logging
from .storage.db import get_db
from .storage.repositories import Repositories

app = typer.Typer(help="Parla Mente — fonti ufficiali del Parlamento italiano.", no_args_is_help=True)
ingest_app = typer.Typer(help="Ingestion dalle fonti ufficiali.")
nlp_app = typer.Typer(help="Pipeline NLP (keyword, topic).")
db_app = typer.Typer(help="Gestione database.")
app.add_typer(ingest_app, name="ingest")
app.add_typer(nlp_app, name="nlp")
app.add_typer(db_app, name="db")

console = Console()


def _repo() -> Repositories:
    setup_logging()
    return Repositories(get_db())


def _check_camera(source: str) -> None:
    if source != "camera":
        raise typer.BadParameter("Solo 'camera' è disponibile in Fase 1 MVP (Senato: stub).")


@ingest_app.command("deputies")
def cmd_deputies(
    source: str = typer.Option("camera", help="Fonte ufficiale."),
    legislature: str = typer.Option("19", help="Legislatura."),
) -> None:
    """Scarica l'anagrafica deputati via SPARQL (REALE)."""
    _check_camera(source)
    n = ingest_deputies(_repo(), legislature)
    console.print(f"[green]OK[/] {n} deputati salvati (legislatura {legislature}).")


@ingest_app.command("speeches")
def cmd_speeches(
    source: str = typer.Option("camera"),
    live: bool = typer.Option(False, help="Tenta il parsing reale invece delle fixtures."),
) -> None:
    """Carica resoconti/interventi (fixtures reali nell'MVP)."""
    _check_camera(source)
    nd, ni = ingest_speeches(_repo(), use_fixtures=not live)
    console.print(f"[green]OK[/] {nd} documenti, {ni} interventi.")


@ingest_app.command("acts")
def cmd_acts(
    source: str = typer.Option("camera"),
    live: bool = typer.Option(False, help="Tenta il parsing reale invece delle fixtures."),
) -> None:
    """Carica atti (fixtures reali nell'MVP)."""
    _check_camera(source)
    n = ingest_acts(_repo(), use_fixtures=not live)
    console.print(f"[green]OK[/] {n} atti salvati.")


@nlp_app.command("keywords")
def cmd_keywords(top_n: int = typer.Option(30, help="Keyword per parlamentare.")) -> None:
    """Estrae le keyword distintive (TF-IDF + n-grammi)."""
    n = run_keywords(_repo(), top_n=top_n)
    console.print(f"[green]OK[/] {n} keyword salvate.")


@nlp_app.command("topics")
def cmd_topics(threshold: float = typer.Option(1.0, help="Soglia minima di score.")) -> None:
    """Classifica interventi e atti sulla tassonomia controllata."""
    n = run_topics(_repo(), threshold=threshold)
    console.print(f"[green]OK[/] {n} assegnazioni topic salvate.")


@db_app.command("reset")
def cmd_reset() -> None:
    """Azzera e ricrea lo schema."""
    get_db().reset()
    console.print("[yellow]Database azzerato e schema ricreato.[/]")


@db_app.command("stats")
def cmd_stats() -> None:
    """Mostra il conteggio delle tabelle principali."""
    repo = _repo()
    table = Table("Tabella", "Righe")
    for name in ("politicians", "documents", "interventions", "acts", "topics",
                 "intervention_topics", "keywords"):
        count = repo.conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        table.add_row(name, str(count))
    console.print(table)


@app.command("api")
def cmd_api(
    host: str = typer.Option("127.0.0.1"),
    port: int = typer.Option(8000),
    reload: bool = typer.Option(False),
) -> None:
    """Avvia l'API FastAPI (uvicorn)."""
    import uvicorn

    uvicorn.run("parlamente.api.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    app()
