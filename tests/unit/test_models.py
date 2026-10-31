"""Testes dos modelos de dominio."""

from __future__ import annotations

from f1.domain.models import DriverStats, FastestLap, TeamStats


def test_fastest_lap_format() -> None:
    lap = FastestLap(position=1, driver_number=1, driver_name="Max", lap_duration=92.608)
    assert lap.lap_time_formatted == "1:32.608"


def test_driver_stats_format() -> None:
    stats = DriverStats(driver_number=1, driver_name="Max", laps_count=10, best_lap=75.4)
    assert stats.best_lap_formatted == "1:15.400"
    sem = DriverStats(driver_number=2, driver_name="X", laps_count=0, best_lap=None)
    assert sem.best_lap_formatted == "-"


def test_team_stats_format() -> None:
    stats = TeamStats(team_name="Red Bull", drivers_count=2, laps_count=20, best_lap=74.9)
    assert stats.best_lap_formatted == "1:14.900"
