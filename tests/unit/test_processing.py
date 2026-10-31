"""Testes das funcoes puras de processamento de voltas."""

from __future__ import annotations

import pytest

from f1.domain.models import Driver, Lap
from f1.processing.laps import driver_stats, fastest_laps, team_stats, valid_laps


def _laps() -> list[Lap]:
    return [
        Lap(driver_number=1, lap_number=10, lap_duration=92.6),
        Lap(driver_number=1, lap_number=11, lap_duration=93.0),
        Lap(driver_number=16, lap_number=12, lap_duration=93.1),
        Lap(driver_number=44, lap_number=5, lap_duration=None),  # invalida
        Lap(driver_number=4, lap_number=1, lap_duration=120.0, is_pit_out_lap=True),
        Lap(driver_number=63, lap_number=20, lap_duration=92.9),
        Lap(driver_number=11, lap_number=22, lap_duration=0.0),  # invalida
    ]


def _drivers() -> list[Driver]:
    return [
        Driver(driver_number=1, full_name="Max Verstappen", team_name="Red Bull"),
        Driver(driver_number=16, full_name="Charles Leclerc", team_name="Ferrari"),
        Driver(driver_number=63, full_name="George Russell", team_name="Mercedes"),
    ]


def test_valid_laps_remove_invalidas_e_pit_out() -> None:
    numbers = [lap.driver_number for lap in valid_laps(_laps())]
    assert sorted(set(numbers)) == [1, 16, 63]


def test_fastest_laps_ordena_por_tempo() -> None:
    result = fastest_laps(_laps(), top_n=3)
    tempos = [lap.lap_duration for lap in result]
    assert tempos == sorted(tempos)
    assert result[0].driver_number == 1  # 92.6 e o menor


def test_fastest_laps_respeita_top_n() -> None:
    assert len(fastest_laps(_laps(), top_n=2)) == 2


def test_fastest_laps_top_n_negativo_levanta_erro() -> None:
    with pytest.raises(ValueError):
        fastest_laps(_laps(), top_n=-1)


def test_driver_stats_agrega_por_piloto() -> None:
    stats = driver_stats(_laps(), _drivers())
    by_number = {s.driver_number: s for s in stats}
    assert by_number[1].laps_count == 2
    assert by_number[1].best_lap == 92.6
    assert by_number[1].average_lap == 92.8
    # ordenado pela melhor volta (menor primeiro)
    assert stats[0].best_lap <= stats[-1].best_lap


def test_team_stats_agrega_por_equipe() -> None:
    stats = team_stats(_laps(), _drivers())
    by_team = {s.team_name: s for s in stats}
    assert by_team["Red Bull"].laps_count == 2
    assert by_team["Red Bull"].drivers_count == 1
    assert by_team["Ferrari"].best_lap == 93.1
