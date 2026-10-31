"""Modelos de dominio (Pydantic v2)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Meeting(BaseModel):
    """Um GP (meeting) de uma temporada."""

    meeting_key: int
    meeting_name: str | None = None
    country_name: str | None = None
    circuit_short_name: str | None = None
    year: int | None = None


class Session(BaseModel):
    """Uma sessao de F1 (corrida, qualifying, treino)."""

    session_key: int
    session_name: str | None = None
    country_name: str | None = None
    circuit_short_name: str | None = None
    year: int | None = None


class Driver(BaseModel):
    """Um piloto dentro de uma sessao."""

    driver_number: int
    full_name: str | None = None
    name_acronym: str | None = None
    team_name: str | None = None
    team_colour: str | None = None


class Lap(BaseModel):
    """Uma volta individual."""

    driver_number: int
    lap_number: int | None = None
    lap_duration: float | None = None
    is_pit_out_lap: bool = False


class FastestLap(BaseModel):
    """Resultado final: uma das voltas mais rapidas, pronta para exibir."""

    position: int = Field(..., ge=1)
    driver_number: int
    driver_name: str
    team_name: str | None = None
    lap_number: int | None = None
    lap_duration: float

    @property
    def lap_time_formatted(self) -> str:
        """Formata a duracao em m:ss.mmm (ex.: 1:32.608)."""
        minutes = int(self.lap_duration // 60)
        seconds = self.lap_duration - minutes * 60
        return f"{minutes}:{seconds:06.3f}"


class DriverStats(BaseModel):
    """Estatisticas agregadas de um piloto numa sessao."""

    driver_number: int
    driver_name: str
    team_name: str | None = None
    laps_count: int
    best_lap: float | None = None
    average_lap: float | None = None

    @property
    def best_lap_formatted(self) -> str:
        if self.best_lap is None:
            return "-"
        minutes = int(self.best_lap // 60)
        seconds = self.best_lap - minutes * 60
        return f"{minutes}:{seconds:06.3f}"


class TeamStats(BaseModel):
    """Estatisticas agregadas de uma equipe numa sessao."""

    team_name: str
    drivers_count: int
    laps_count: int
    best_lap: float | None = None

    @property
    def best_lap_formatted(self) -> str:
        if self.best_lap is None:
            return "-"
        minutes = int(self.best_lap // 60)
        seconds = self.best_lap - minutes * 60
        return f"{minutes}:{seconds:06.3f}"
