"""Adapter dei resoconti stenografici dell'Assemblea (Camera).

STATO: parser REALE + loader di fixtures.

Il parser reale (`_parse_live`) scarica i resoconti stenografici pubblicati dalla
Camera e attribuisce ogni intervento al deputato corretto sfruttando l'`idPersona`
presente nel link alla scheda del deputato: idPersona=NNNNNN -> camera_dNNNNNN_<leg>.

Per l'MVP `use_fixtures=True` legge i resoconti già scaricati (fixtures reali,
committate); con `use_fixtures=False` l'adapter scarica e parsa dal vivo.

Fonti:
- indice resoconti Assemblea L19: https://www.camera.it/leg19/207
- documento stenografico per seduta (servizio getDocumento.ashx)
"""

from __future__ import annotations

import re
from datetime import date

from bs4 import BeautifulSoup

from ...config import get_settings
from ...logging import get_logger
from ...models import Chamber, Intervention, Politician, SourceDocument, SourceType
import httpx

from ..base import SourceAdapter
from . import fixtures

logger = get_logger(__name__)

_INDEX_URL = "https://www.camera.it/leg{leg}/207"
_STENO_URL = (
    "https://documenti.camera.it/apps/commonServices/getDocumento.ashx"
    "?idLegislatura={leg}&sezione=assemblea&tipoDoc=stenografico&idSeduta={seduta:04d}"
)
_ID_PERSONA_RE = re.compile(r"idPersona=(\d+)")
_SLDATE_RE = re.compile(r"slAnnoMese=(\d{6})&(?:amp;)?slGiorno=(\d{1,2})&(?:amp;)?idSeduta=(\d+)")
_MIN_TEXT_LEN = 200  # focus sugli interventi sostanziali, non sui meri richiami procedurali

_MONTHS = {
    "gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6,
    "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12,
}
# Header del resoconto: "... venerdì 23 gennaio 2026 ..." (primo match nel documento).
_DOC_DATE_RE = re.compile(
    r"(?:luned|marted|mercoled|gioved|venerd|sabato|domenica)\w*\s+"
    r"(\d{1,2})\s+(" + "|".join(_MONTHS) + r")\s+(20\d{2})",
    re.IGNORECASE,
)


def _extract_seduta_date(text: str) -> date | None:
    m = _DOC_DATE_RE.search(text)
    if not m:
        return None
    try:
        return date(int(m.group(3)), _MONTHS[m.group(2).lower()], int(m.group(1)))
    except (ValueError, KeyError):
        return None


class CameraSpeechesAdapter(SourceAdapter):
    source_name = "Camera dei Deputati — Resoconti Assemblea"

    def __init__(
        self,
        use_fixtures: bool = True,
        legislature: str = "19",
        max_sedute: int = 4,
        seduta_ids: list[int] | None = None,
    ):
        self.use_fixtures = use_fixtures
        self.legislature = legislature
        self.max_sedute = max_sedute
        # Se valorizzato, scarica esattamente queste sedute (storico esteso),
        # ricavando la data dal documento; altrimenti usa l'indice (ultime sedute).
        self.seduta_ids = seduta_ids
        self._cache: tuple[list[SourceDocument], list[Intervention]] | None = None
        settings = get_settings()
        self._rate_limit = settings.http_rate_limit_seconds
        self._last_request = 0.0
        self._http = httpx.Client(
            timeout=settings.http_timeout,
            headers={"User-Agent": settings.user_agent},
            follow_redirects=True,
        )

    def fetch_politicians(self, legislature: str) -> list[Politician]:
        raise NotImplementedError("Usa CameraDeputiesAdapter per i deputati.")

    def fetch_documents(self, since=None, until=None) -> list[SourceDocument]:
        if self.use_fixtures:
            return fixtures.load_fixture_documents()
        return self._parse_live()[0]

    def fetch_interventions(self, since=None, until=None) -> list[Intervention]:
        if self.use_fixtures:
            return fixtures.load_fixture_interventions()
        return self._parse_live()[1]

    # ------------------------------------------------------------------
    # Parser reale
    # ------------------------------------------------------------------
    def _parse_live(self) -> tuple[list[SourceDocument], list[Intervention]]:
        if self._cache is not None:
            return self._cache
        if self.seduta_ids is not None:
            # Storico esteso: id espliciti, data ricavata dal documento.
            sedute: list[tuple[int, date | None]] = [(sid, None) for sid in self.seduta_ids]
        else:
            sedute = self._list_sedute()[: self.max_sedute]
        docs: list[SourceDocument] = []
        interventions: list[Intervention] = []
        for seduta_id, seduta_date in sedute:
            doc, ints = self._fetch_seduta(seduta_id, seduta_date)
            if doc and ints:
                docs.append(doc)
                interventions.extend(ints)
        logger.info("Camera live: %d sedute, %d interventi", len(docs), len(interventions))
        self._cache = (docs, interventions)
        return self._cache

    def _list_sedute(self) -> list[tuple[int, date]]:
        """Estrae (idSeduta, data) dall'indice dei resoconti, ordinati per data desc."""
        url = _INDEX_URL.format(leg=self.legislature)
        html = self._get(url)
        found: dict[int, date] = {}
        for m in _SLDATE_RE.finditer(html):
            ym, day, seduta = m.group(1), int(m.group(2)), int(m.group(3))
            year, month = int(ym[:4]), int(ym[4:6])
            try:
                found.setdefault(seduta, date(year, month, day))
            except ValueError:
                continue
        sedute = sorted(found.items(), key=lambda kv: kv[1], reverse=True)
        logger.info("Camera: trovate %d sedute nell'indice", len(sedute))
        return sedute

    def _fetch_seduta(
        self, seduta_id: int, seduta_date: date | None = None
    ) -> tuple[SourceDocument | None, list[Intervention]]:
        url = _STENO_URL.format(leg=self.legislature, seduta=seduta_id)
        try:
            html = self._get(url)
        except httpx.HTTPError as exc:
            logger.warning("Seduta %s non scaricata: %s", seduta_id, exc)
            return None, []

        soup = BeautifulSoup(html, "html.parser")
        if seduta_date is None:
            seduta_date = _extract_seduta_date(soup.get_text(" ", strip=True))
            if seduta_date is None:
                logger.warning("Seduta %s: data non trovata, salto.", seduta_id)
                return None, []
        doc_id = f"camera_sten_{self.legislature}_sed{seduta_id:04d}"
        document = SourceDocument(
            id=doc_id,
            source="Camera dei Deputati",
            chamber=Chamber.CAMERA,
            legislature=str(self.legislature),
            source_type=SourceType.CHAMBER_SPEECH,
            document_type="Resoconto stenografico dell'Assemblea",
            date=seduta_date,
            title=f"Assemblea — Seduta n. {seduta_id} del {seduta_date.isoformat()}",
            url=url,
            raw_text="",  # il testo vive negli interventi attribuiti
            metadata={"seduta": seduta_id},
        )

        interventions: list[Intervention] = []
        for idx, p in enumerate(soup.find_all("p", class_="intervento")):
            link = p.find("a", href=True)
            if not link:
                continue
            mp = _ID_PERSONA_RE.search(link["href"])
            if not mp:
                continue
            id_persona = mp.group(1)
            speaker = _speaker_name(link)
            # testo = testo del paragrafo meno l'etichetta dell'oratore
            text = p.get_text(" ", strip=True)
            label = link.get_text(strip=True)
            if text.startswith(label):
                text = text[len(label):].lstrip(" .—-").strip()
            if len(text) < _MIN_TEXT_LEN:
                continue
            interventions.append(
                Intervention(
                    id=f"{doc_id}_int{idx:04d}",
                    politician_id=f"camera_d{id_persona}_{self.legislature}",
                    politician_name=speaker,
                    document_id=doc_id,
                    date=seduta_date,
                    chamber=Chamber.CAMERA,
                    source_type=SourceType.CHAMBER_SPEECH,
                    context="Assemblea",
                    text=text,
                    source_url=url,
                    metadata={"id_persona": id_persona, "seduta": seduta_id},
                )
            )
        return document, interventions

    def _get(self, url: str) -> str:
        # Rispetto del rate-limit verso le fonti ufficiali.
        import time

        elapsed = time.monotonic() - self._last_request
        if elapsed < self._rate_limit:
            time.sleep(self._rate_limit - elapsed)
        self._last_request = time.monotonic()
        resp = self._http.get(url)
        resp.raise_for_status()
        return resp.text


def _speaker_name(link) -> str:
    """Preferisce il nome reale dal title 'Vai alla scheda personale: COGNOME Nome'."""
    title = link.get("title", "")
    if ":" in title:
        raw = title.split(":", 1)[1].strip()
        return raw.title() if raw.isupper() else raw
    return link.get_text(strip=True).title()
