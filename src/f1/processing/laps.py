"""Funcoes puras para filtrar e ordenar voltas.

Sem dependencia de rede nem de IO: faceis de testar.
"""

from __future__ import annotations

from f1.domain.models import Lap


def valid_laps(laps: list[Lap]) -> list[Lap]:
    """Mantem apenas voltas com duracao valida e que nao sejam de pit out."""
    return [
        lap
        for lap in laps
        if lap.lap_duration is not None and lap.lap_duration > 0 and not lap.is_pit_out_lap
    ]


def fastest_laps(laps: list[Lap], top_n: int = 5) -> list[Lap]:
    """Retorna as `top_n` voltas mais rapidas, ja filtradas e ordenadas.

    A ordenacao e por `lap_duration` crescente (menor tempo primeiro).
    """
    if top_n < 0:
        raise ValueError("top_n deve ser >= 0")
    ordered = sorted(valid_laps(laps), key=lambda lap: lap.lap_duration or float("inf"))
    return ordered[:top_n]
