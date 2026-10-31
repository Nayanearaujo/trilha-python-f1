"""Cliente HTTP generico, reutilizavel.

Isola o uso do `requests` do resto do projeto. Faz retry simples e
tratamento de erros, sem conhecer nada sobre a OpenF1.
"""

from __future__ import annotations

import time
from typing import Any

import requests

from f1.utils.logger import get_logger

logger = get_logger(__name__)


class HttpError(RuntimeError):
    """Erro de alto nivel para falhas HTTP."""


class HttpClient:
    """Wrapper fino sobre requests.Session com retry e timeout."""

    def __init__(
        self,
        timeout: int = 10,
        max_retries: int = 2,
        backoff: float = 0.5,
        session: requests.Session | None = None,
    ) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff
        self._session = session or requests.Session()

    def get_json(self, url: str, params: dict[str, Any] | None = None) -> Any:
        """Faz GET e devolve o JSON, com algumas tentativas em caso de falha."""
        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                logger.info("GET %s params=%s (tentativa %d)", url, params, attempt + 1)
                response = self._session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    time.sleep(self.backoff * (attempt + 1))
        raise HttpError(f"Falha ao consultar {url}: {last_exc}") from last_exc
