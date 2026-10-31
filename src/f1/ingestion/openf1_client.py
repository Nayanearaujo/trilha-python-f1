"""Cliente HTTP para a OpenF1 API.

Responsavel apenas por falar com a API e devolver dados ja validados como
modelos de dominio. Nenhuma regra de negocio aqui.
"""

from __future__ import annotations

from typing import Any

import requests

from f1.domain.models import Driver, Lap, Session
from f1.utils.config import OPENF1_BASE_URL, REQUEST_TIMEOUT
from f1.utils.logger import get_logger

logger = get_logger(__name__)


class OpenF1Client:
    """Cliente simples para os endpoints publicos da OpenF1."""

    def __init__(
        self,
        base_url: str = OPENF1_BASE_URL,
        timeout: int = REQUEST_TIMEOUT,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = session or requests.Session()

    def _get(self, endpoint: str, params: dict[str, Any]) -> list[dict[str, Any]]:
        url = f"{self.base_url}/{endpoint}"
        logger.info("GET %s params=%s", url, params)
        response = self._session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

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
