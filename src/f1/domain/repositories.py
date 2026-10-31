"""Camada de repositorio.

Abstrai a origem dos dados. O resto do dominio depende desta interface, nao
do cliente HTTP concreto. Isso facilita testes (basta um repositorio fake) e
troca de fonte de dados no futuro.
"""

from __future__ import annotations

from typing import Protocol

from f1.domain.models import Driver, Lap, Meeting, Session
from f1.ingestion.openf1_client import OpenF1Client


class F1Repository(Protocol):
    """Contrato de acesso aos dados de F1."""

    def meetings(self, year: int) -> list[Meeting]: ...

    def sessions(
        self, year: int, country_name: str | None = None, session_name: str | None = None
    ) -> list[Session]: ...

    def laps(self, session_key: int) -> list[Lap]: ...

    def drivers(self, session_key: int) -> list[Driver]: ...


class OpenF1Repository:
    """Implementacao do repositorio baseada na OpenF1 API."""

    def __init__(self, client: OpenF1Client | None = None) -> None:
        self._client = client or OpenF1Client()

    def meetings(self, year: int) -> list[Meeting]:
        return self._client.get_meetings(year)

    def sessions(
        self, year: int, country_name: str | None = None, session_name: str | None = None
    ) -> list[Session]:
        return self._client.get_sessions(
            year=year, country_name=country_name, session_name=session_name
        )

    def laps(self, session_key: int) -> list[Lap]:
        return self._client.get_laps(session_key)

    def drivers(self, session_key: int) -> list[Driver]:
        return self._client.get_drivers(session_key)
