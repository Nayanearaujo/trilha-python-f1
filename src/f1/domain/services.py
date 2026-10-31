"""Regra de negocio: montar as voltas mais rapidas de um circuito."""

from __future__ import annotations

from f1.domain.models import Driver, FastestLap, Lap
from f1.ingestion.openf1_client import OpenF1Client
from f1.processing.laps import fastest_laps
from f1.utils.config import TOP_N_LAPS
from f1.utils.logger import get_logger

logger = get_logger(__name__)


def build_fastest_laps(
    laps: list[Lap],
    drivers: list[Driver],
    top_n: int = TOP_N_LAPS,
) -> list[FastestLap]:
    """Converte voltas + pilotos nas `top_n` voltas mais rapidas prontas para UI.

    Funcao pura (sem rede): recebe os dados ja carregados.
    """
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


class FastestLapsService:
    """Orquestra o cliente OpenF1 para entregar as voltas mais rapidas."""

    def __init__(self, client: OpenF1Client | None = None) -> None:
        self.client = client or OpenF1Client()

    def fastest_laps_for_session(
        self, session_key: int, top_n: int = TOP_N_LAPS
    ) -> list[FastestLap]:
        """Busca voltas e pilotos de uma sessao e devolve as mais rapidas."""
        laps = self.client.get_laps(session_key)
        drivers = self.client.get_drivers(session_key)
        return build_fastest_laps(laps, drivers, top_n=top_n)
