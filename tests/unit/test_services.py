"""Testes da regra de negocio com repositorio fake (sem rede)."""

from __future__ import annotations

from f1.domain.models import Driver, Lap, Meeting, Session
from f1.domain.services import F1Service, build_fastest_laps, continent_for


def test_build_fastest_laps_cruza_piloto_e_formata() -> None:
    laps = [
        Lap(driver_number=1, lap_number=39, lap_duration=92.608),
        Lap(driver_number=16, lap_number=53, lap_duration=93.2),
    ]
    drivers = [
        Driver(driver_number=1, full_name="Max Verstappen", team_name="Red Bull"),
        Driver(driver_number=16, full_name="Charles Leclerc", team_name="Ferrari"),
    ]
    result = build_fastest_laps(laps, drivers, top_n=5)
    assert [lap.position for lap in result] == [1, 2]
    assert result[0].driver_name == "Max Verstappen"
    assert result[0].lap_time_formatted == "1:32.608"


def test_continent_for() -> None:
    assert continent_for("Brazil") == "South America"
    assert continent_for("Italy") == "Europe"
    assert continent_for(None) == "Outros"
    assert continent_for("Narnia") == "Outros"


class FakeRepo:
    """Repositorio fake que simula a OpenF1 sem rede."""

    def meetings(self, year: int) -> list[Meeting]:
        return [
            Meeting(meeting_key=1, meeting_name="Brazil GP", country_name="Brazil", year=year),
            Meeting(meeting_key=2, meeting_name="Italy GP", country_name="Italy", year=year),
        ]

    def sessions(self, year, country_name=None, session_name=None) -> list[Session]:
        return [Session(session_key=99, session_name="Race", country_name=country_name)]

    def laps(self, session_key: int) -> list[Lap]:
        return [
            Lap(driver_number=4, lap_number=33, lap_duration=75.4),
            Lap(driver_number=1, lap_number=10, lap_duration=74.9),
        ]

    def drivers(self, session_key: int) -> list[Driver]:
        return [
            Driver(driver_number=4, full_name="Lando Norris", team_name="McLaren"),
            Driver(driver_number=1, full_name="Max Verstappen", team_name="Red Bull"),
        ]


def _service() -> F1Service:
    return F1Service(repository=FakeRepo())


def test_service_fastest_laps() -> None:
    result = _service().fastest_laps_for_session(99, top_n=5)
    assert result[0].driver_name == "Max Verstappen"  # 74.9 mais rapido
    assert result[1].driver_name == "Lando Norris"


def test_service_continents_e_countries() -> None:
    svc = _service()
    assert svc.continents(2024) == ["Europe", "South America"]
    assert svc.countries(2024, continent="Europe") == ["Italy"]
    assert svc.countries(2024) == ["Brazil", "Italy"]


def test_service_driver_e_team_stats() -> None:
    svc = _service()
    ds = svc.driver_stats_for_session(99)
    ts = svc.team_stats_for_session(99)
    assert {d.driver_name for d in ds} == {"Max Verstappen", "Lando Norris"}
    assert {t.team_name for t in ts} == {"McLaren", "Red Bull"}
