"""Testes da regra de negocio (API mockada)."""

from __future__ import annotations

from f1.domain.models import Driver, Lap
from f1.domain.services import FastestLapsService, build_fastest_laps


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
    assert result[0].team_name == "Red Bull"
    assert result[0].lap_time_formatted == "1:32.608"


def test_build_fastest_laps_piloto_desconhecido() -> None:
    laps = [Lap(driver_number=99, lap_number=1, lap_duration=90.0)]
    result = build_fastest_laps(laps, drivers=[], top_n=5)
    assert result[0].driver_name == "#99"
    assert result[0].team_name is None


class _FakeClient:
    """Cliente falso que simula a OpenF1 sem rede."""

    def get_laps(self, session_key: int) -> list[Lap]:
        return [
            Lap(driver_number=4, lap_number=33, lap_duration=75.4),
            Lap(driver_number=1, lap_number=10, lap_duration=74.9),
        ]

    def get_drivers(self, session_key: int) -> list[Driver]:
        return [
            Driver(driver_number=4, full_name="Lando Norris", team_name="McLaren"),
            Driver(driver_number=1, full_name="Max Verstappen", team_name="Red Bull"),
        ]


def test_service_usa_cliente_injetado() -> None:
    service = FastestLapsService(client=_FakeClient())
    result = service.fastest_laps_for_session(session_key=123, top_n=5)

    assert result[0].driver_name == "Max Verstappen"  # 74.9 e o mais rapido
    assert result[1].driver_name == "Lando Norris"
    assert len(result) == 2
