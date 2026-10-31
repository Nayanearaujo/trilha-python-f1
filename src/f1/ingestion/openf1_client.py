"""Cliente especifico da OpenF1 API.

Conhece os endpoints da OpenF1 e devolve dados ja validados como modelos de
dominio. Delega o transporte HTTP ao HttpClient (separacao de responsabilidades).
"""

from __future__ import annotations

from typing import Any

from f1.domain.models import Driver, Lap, Meeting, Session
from f1.ingestion.http_client import HttpClient
from f1.utils.config import OPENF1_BASE_URL, REQUEST_TIMEOUT
from f1.utils.logger import get_logger

logger = get_logger(__name__)


class OpenF1Client:
    """Acesso aos endpoints publicos da OpenF1."""

    def __init__(
        self,
        base_url: str = OPENF1_BASE_URL,
        http: HttpClient | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._http = http or HttpClient(timeout=REQUEST_TIMEOUT)

    def _get(self, endpoint: str, params: dict[str, Any]) -> list[dict[str, Any]]:
        url = f"{self.base_url}/{endpoint}"
        data = self._http.get_json(url, params=params)
        return data if isinstance(data, list) else []

    def get_meetings(self, year: int) -> list[Meeting]:
        """Lista os GPs (meetings) de um ano."""
        data = self._get("meetings", {"year": year})
        return [Meeting(**item) for item in data]

    def get_sessions(
        self,
        year: int,
        country_name: str | None = None,
        session_name: str | None = None,
    ) -> list[Session]:
        """Lista sessoes para um ano (e, opcionalmente, pais/sessao)."""
        params: dict[str, Any] = {"year": year}
        if country_name:
            params["country_name"] = country_name
        if session_name:
            params["session_name"] = session_name
        data = self._get("sessions", params)
        return [Session(**item) for item in data]

    def get_laps(self, session_key: int) -> list[Lap]:
        """Retorna as voltas de uma sessao."""
        data = self._get("laps", {"session_key": session_key})
        return [Lap(**item) for item in data]

    def get_drivers(self, session_key: int) -> list[Driver]:
        """Retorna os pilotos de uma sessao."""
        data = self._get("drivers", {"session_key": session_key})
        return [Driver(**item) for item in data]
