"""Regra de negocio: orquestra repositorio + processamento."""

from __future__ import annotations

from f1.domain.models import (
    Driver,
    DriverStats,
    FastestLap,
    Lap,
    Meeting,
    Session,
    TeamStats,
)
from f1.domain.repositories import F1Repository, OpenF1Repository
from f1.processing.laps import driver_stats, fastest_laps, team_stats
from f1.utils.config import TOP_N_LAPS
from f1.utils.logger import get_logger

logger = get_logger(__name__)

# Mapa simples de pais -> continente, para o filtro encadeado do dashboard.
COUNTRY_TO_CONTINENT: dict[str, str] = {
    "Bahrain": "Asia",
    "Saudi Arabia": "Asia",
    "Australia": "Oceania",
    "Japan": "Asia",
    "China": "Asia",
    "Singapore": "Asia",
    "Qatar": "Asia",
    "United Arab Emirates": "Asia",
    "Azerbaijan": "Asia",
    "Italy": "Europe",
    "Monaco": "Europe",
    "Spain": "Europe",
    "Austria": "Europe",
    "United Kingdom": "Europe",
    "Great Britain": "Europe",
    "Hungary": "Europe",
    "Belgium": "Europe",
    "Netherlands": "Europe",
    "United States": "North America",
    "USA": "North America",
    "Mexico": "North America",
    "Canada": "North America",
    "Brazil": "South America",
}


def continent_for(country: str | None) -> str:
    """Retorna o continente de um pais (ou 'Outros')."""
    if not country:
        return "Outros"
    return COUNTRY_TO_CONTINENT.get(country, "Outros")


def build_fastest_laps(
    laps: list[Lap],
    drivers: list[Driver],
    top_n: int = TOP_N_LAPS,
) -> list[FastestLap]:
    """Converte voltas + pilotos nas `top_n` voltas mais rapidas prontas para UI."""
    drivers_by_number = {d.driver_number: d for d in drivers}
    result: list[FastestLap] = []
    for position, lap in enumerate(fastest_laps(laps, top_n=top_n), start=1):
        driver = drivers_by_number.get(lap.driver_number)
        driver_name = (
            driver.full_name or driver.name_acronym if driver else f"#{lap.driver_number}"
        ) or f"#{lap.driver_number}"
        result.append(
            FastestLap(
                position=position,
                driver_number=lap.driver_number,
                driver_name=driver_name,
                team_name=driver.team_name if driver else None,
                lap_number=lap.lap_number,
                lap_duration=lap.lap_duration or 0.0,
            )
        )
    return result


class F1Service:
    """Servico principal: expoe dados prontos para o dashboard."""

    def __init__(self, repository: F1Repository | None = None) -> None:
        self.repo: F1Repository = repository or OpenF1Repository()

    # --- filtros / navegacao ------------------------------------------------
    def meetings(self, year: int) -> list[Meeting]:
        return self.repo.meetings(year)

    def continents(self, year: int) -> list[str]:
        found = {continent_for(m.country_name) for m in self.repo.meetings(year)}
        return sorted(found)

    def countries(self, year: int, continent: str | None = None) -> list[str]:
        result = []
        for m in self.repo.meetings(year):
            if not m.country_name:
                continue
            if continent and continent_for(m.country_name) != continent:
                continue
            result.append(m.country_name)
        return sorted(set(result))

    def race_sessions(self, year: int, country_name: str) -> list[Session]:
        return self.repo.sessions(year=year, country_name=country_name, session_name="Race")

    # --- dados / analises ---------------------------------------------------
    def _laps_and_drivers(self, session_key: int) -> tuple[list[Lap], list[Driver]]:
        return self.repo.laps(session_key), self.repo.drivers(session_key)

    def fastest_laps_for_session(
        self, session_key: int, top_n: int = TOP_N_LAPS
    ) -> list[FastestLap]:
        laps, drivers = self._laps_and_drivers(session_key)
        return build_fastest_laps(laps, drivers, top_n=top_n)

    def driver_stats_for_session(self, session_key: int) -> list[DriverStats]:
        laps, drivers = self._laps_and_drivers(session_key)
        return driver_stats(laps, drivers)

    def team_stats_for_session(self, session_key: int) -> list[TeamStats]:
        laps, drivers = self._laps_and_drivers(session_key)
        return team_stats(laps, drivers)


# Alias compatibilidade com a versao anterior do projeto.
FastestLapsService = F1Service
