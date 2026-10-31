"""Funcoes puras para filtrar, ordenar e agregar voltas.

Sem dependencia de rede nem de IO: faceis de testar.
"""

from __future__ import annotations

from statistics import mean

from f1.domain.models import Driver, DriverStats, Lap, TeamStats


def valid_laps(laps: list[Lap]) -> list[Lap]:
    """Mantem apenas voltas com duracao valida e que nao sejam de pit out."""
    return [
        lap
        for lap in laps
        if lap.lap_duration is not None and lap.lap_duration > 0 and not lap.is_pit_out_lap
    ]


def fastest_laps(laps: list[Lap], top_n: int = 5) -> list[Lap]:
    """Retorna as `top_n` voltas mais rapidas, ja filtradas e ordenadas."""
    if top_n < 0:
        raise ValueError("top_n deve ser >= 0")
    ordered = sorted(valid_laps(laps), key=lambda lap: lap.lap_duration or float("inf"))
    return ordered[:top_n]


def driver_stats(laps: list[Lap], drivers: list[Driver]) -> list[DriverStats]:
    """Agrega estatisticas por piloto (contagem, melhor e media de voltas)."""
    drivers_by_number = {d.driver_number: d for d in drivers}
    valid = valid_laps(laps)
    laps_by_driver: dict[int, list[float]] = {}
    for lap in valid:
        laps_by_driver.setdefault(lap.driver_number, []).append(lap.lap_duration or 0.0)

    stats: list[DriverStats] = []
    for number, durations in laps_by_driver.items():
        driver = drivers_by_number.get(number)
        name = (driver.full_name or driver.name_acronym if driver else None) or f"#{number}"
        stats.append(
            DriverStats(
                driver_number=number,
                driver_name=name,
                team_name=driver.team_name if driver else None,
                laps_count=len(durations),
                best_lap=min(durations) if durations else None,
                average_lap=round(mean(durations), 3) if durations else None,
            )
        )
    stats.sort(key=lambda s: s.best_lap if s.best_lap is not None else float("inf"))
    return stats


def team_stats(laps: list[Lap], drivers: list[Driver]) -> list[TeamStats]:
    """Agrega estatisticas por equipe."""
    drivers_by_number = {d.driver_number: d for d in drivers}
    valid = valid_laps(laps)

    teams: dict[str, dict] = {}
    for lap in valid:
        driver = drivers_by_number.get(lap.driver_number)
        team = (driver.team_name if driver else None) or "Desconhecida"
        bucket = teams.setdefault(team, {"drivers": set(), "durations": []})
        bucket["drivers"].add(lap.driver_number)
        bucket["durations"].append(lap.lap_duration or 0.0)

    stats: list[TeamStats] = []
    for team, bucket in teams.items():
        durations = bucket["durations"]
        stats.append(
            TeamStats(
                team_name=team,
                drivers_count=len(bucket["drivers"]),
                laps_count=len(durations),
                best_lap=min(durations) if durations else None,
            )
        )
    stats.sort(key=lambda s: s.best_lap if s.best_lap is not None else float("inf"))
    return stats
