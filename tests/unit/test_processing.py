"""Testes das funcoes puras de processamento de voltas."""

from __future__ import annotations

import pytest

from f1.domain.models import Lap
from f1.processing.laps import fastest_laps, valid_laps


def _laps() -> list[Lap]:
    return [
        Lap(driver_number=1, lap_number=10, lap_duration=92.6),
        Lap(driver_number=16, lap_number=12, lap_duration=93.1),
        Lap(driver_number=44, lap_number=5, lap_duration=None),  # invalida
        Lap(driver_number=4, lap_number=1, lap_duration=120.0, is_pit_out_lap=True),
        Lap(driver_number=63, lap_number=20, lap_duration=92.9),
        Lap(driver_number=11, lap_number=22, lap_duration=0.0),  # invalida
    ]


def test_valid_laps_remove_invalidas_e_pit_out() -> None:
    result = valid_laps(_laps())
    numbers = {lap.driver_number for lap in result}
    assert numbers == {1, 16, 63}


def test_fastest_laps_ordena_por_tempo() -> None:
    result = fastest_laps(_laps(), top_n=3)
    tempos = [lap.lap_duration for lap in result]
    assert tempos == sorted(tempos)
    assert result[0].driver_number == 1  # menor tempo (92.6)


def test_fastest_laps_respeita_top_n() -> None:
    assert len(fastest_laps(_laps(), top_n=2)) == 2
    assert len(fastest_laps(_laps(), top_n=10)) == 3  # so ha 3 validas


def test_fastest_laps_top_n_negativo_levanta_erro() -> None:
    with pytest.raises(ValueError):
        fastest_laps(_laps(), top_n=-1)
