"""Configuracao compartilhada dos testes."""

from __future__ import annotations

import pytest

from f1.domain.models import Driver, Lap


@pytest.fixture
def sample_laps() -> list[Lap]:
    return [
        Lap(driver_number=1, lap_number=10, lap_duration=92.6),
        Lap(driver_number=16, lap_number=12, lap_duration=93.1),
    ]


@pytest.fixture
def sample_drivers() -> list[Driver]:
    return [
        Driver(driver_number=1, full_name="Max Verstappen", team_name="Red Bull"),
        Driver(driver_number=16, full_name="Charles Leclerc", team_name="Ferrari"),
    ]
