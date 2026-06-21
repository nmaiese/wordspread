"""Configurazione centralizzata via variabili d'ambiente / file .env.

Nessun segreto è hardcoded: tutto passa da .env (vedi .env.example).
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Radice del repo (…/parlamente), tre livelli sopra questo file:
# backend/parlamente/config.py -> backend/parlamente -> backend -> repo root
REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PARLAMENTE_",
        env_file=(REPO_ROOT / ".env"),
        extra="ignore",
    )

    # Storage
    db_path: Path = Field(default=Path("data/db/parlamente.duckdb"))
    data_dir: Path = Field(default=Path("data"))

    # Camera dei Deputati
    camera_sparql_endpoint: str = "https://dati.camera.it/sparql"
    camera_base_url: str = "https://www.camera.it"

    # HTTP politeness
    http_timeout: float = 60.0
    http_rate_limit_seconds: float = 1.0
    user_agent: str = "ParlaMente/0.1 (civic-tech)"

    # Logging
    log_level: str = "INFO"

    def resolve(self, path: Path) -> Path:
        """Risolve un path relativo rispetto alla radice del repo."""
        return path if path.is_absolute() else (REPO_ROOT / path)

    @property
    def db_file(self) -> Path:
        return self.resolve(self.db_path)

    @property
    def raw_dir(self) -> Path:
        return self.resolve(self.data_dir) / "raw"

    @property
    def fixtures_dir(self) -> Path:
        return self.resolve(self.data_dir) / "fixtures"


@lru_cache
def get_settings() -> Settings:
    return Settings()
