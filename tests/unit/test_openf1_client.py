"""Testes do OpenF1Client e do OpenF1Repository com HttpClient fake."""

from __future__ import annotations

from f1.domain.repositories import OpenF1Repository
from f1.ingestion.openf1_client import OpenF1Client


class _FakeHttp:
    """HttpClient falso: devolve payloads fixos por endpoint."""

    def __init__(self) -> None:
        self.urls: list[str] = []

    def get_json(self, url, params=None):
        self.urls.append(url)
        if url.endswith("/meetings"):
            return [{"meeting_key": 1, "country_name": "Brazil"}]
        if url.endswith("/sessions"):
            return [{"session_key": 99, "session_name": "Race"}]
        if url.endswith("/laps"):
            return [{"driver_number": 1, "lap_number": 10, "lap_duration": 92.6}]
        if url.endswith("/drivers"):
            return [{"driver_number": 1, "full_name": "Max", "team_name": "RBR"}]
        return []


def _client() -> OpenF1Client:
    return OpenF1Client(base_url="https://api.test/v1", http=_FakeHttp())


def test_client_meetings() -> None:
    meetings = _client().get_meetings(2024)
    assert meetings[0].country_name == "Brazil"


def test_client_sessions_com_filtros() -> None:
    sessions = _client().get_sessions(2024, country_name="Brazil", session_name="Race")
    assert sessions[0].session_key == 99


def test_client_laps_e_drivers() -> None:
    client = _client()
    assert client.get_laps(99)[0].lap_duration == 92.6
    assert client.get_drivers(99)[0].full_name == "Max"


def test_repository_delegates_to_client() -> None:
    repo = OpenF1Repository(client=_client())
    assert repo.meetings(2024)[0].country_name == "Brazil"
    assert repo.sessions(2024, country_name="Brazil")[0].session_key == 99
    assert repo.laps(99)[0].lap_duration == 92.6
    assert repo.drivers(99)[0].team_name == "RBR"
