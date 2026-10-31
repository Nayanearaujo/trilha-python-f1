"""Dashboard Streamlit - Analise de dados da Formula 1 (OpenF1).

Camada de apresentacao: orquestra o F1Service e exibe os dados em abas
(Corridas, Equipes, Pilotos, Voltas, Resumo Geral), com filtros encadeados
(continente -> pais -> sessao) e graficos interativos em Plotly.

Rode com:  poetry run streamlit run src/f1/dashboard.py
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from f1.domain.services import F1Service, continent_for
from f1.utils.config import TOP_N_LAPS

st.set_page_config(
    page_title="F1 Analytics",
    page_icon="🏎️",
    layout="wide",
)

PLOTLY_TEMPLATE = "plotly_dark"


@st.cache_resource
def get_service() -> F1Service:
    return F1Service()


@st.cache_data(show_spinner="Carregando GPs...")
def load_meetings(year: int) -> pd.DataFrame:
    service = get_service()
    meetings = service.meetings(year)
    return pd.DataFrame(
        {
            "GP": m.meeting_name,
            "Pais": m.country_name,
            "Continente": continent_for(m.country_name),
            "Circuito": m.circuit_short_name,
        }
        for m in meetings
    )


@st.cache_data(show_spinner="Carregando sessao...")
def load_session_key(year: int, country: str) -> int | None:
    service = get_service()
    sessions = service.race_sessions(year, country)
    return sessions[0].session_key if sessions else None


@st.cache_data(show_spinner="Analisando voltas...")
def load_fastest(session_key: int, top_n: int) -> pd.DataFrame:
    laps = get_service().fastest_laps_for_session(session_key, top_n=top_n)
    return pd.DataFrame(
        {
            "Posicao": lap.position,
            "Rotulo": f"P{lap.position} {lap.driver_name}",
            "Piloto": lap.driver_name,
            "Equipe": lap.team_name or "Desconhecida",
            "Volta": lap.lap_number,
            "Tempo": lap.lap_time_formatted,
            "Segundos": round(lap.lap_duration, 3),
        }
        for lap in laps
    )


def _axis_range(values: list[float], pad_ratio: float = 0.15) -> list[float]:
    """Calcula um range de eixo com zoom no intervalo real dos dados.

    Em vez de comecar em zero (o que esconde diferencas pequenas entre tempos
    de volta), foca no intervalo [min, max] com uma folga proporcional.
    """
    clean = [v for v in values if v is not None]
    if not clean:
        return [0, 1]
    low, high = min(clean), max(clean)
    span = high - low or 1.0
    pad = span * pad_ratio
    return [low - pad, high + pad]


@st.cache_data(show_spinner="Analisando pilotos...")
def load_driver_stats(session_key: int) -> pd.DataFrame:
    stats = get_service().driver_stats_for_session(session_key)
    return pd.DataFrame(
        {
            "Piloto": s.driver_name,
            "Equipe": s.team_name or "Desconhecida",
            "Voltas": s.laps_count,
            "Melhor volta": s.best_lap_formatted,
            "Melhor (s)": round(s.best_lap, 3) if s.best_lap else None,
            "Media (s)": s.average_lap,
        }
        for s in stats
    )


@st.cache_data(show_spinner="Analisando equipes...")
def load_team_stats(session_key: int) -> pd.DataFrame:
    stats = get_service().team_stats_for_session(session_key)
    return pd.DataFrame(
        {
            "Equipe": s.team_name,
            "Pilotos": s.drivers_count,
            "Voltas": s.laps_count,
            "Melhor volta": s.best_lap_formatted,
            "Melhor (s)": round(s.best_lap, 3) if s.best_lap else None,
        }
        for s in stats
    )


def _sidebar_filters() -> tuple[int, str | None, str | None, int]:
    st.sidebar.header("🔎 Filtros")
    year = st.sidebar.selectbox("Temporada", [2024, 2025, 2023], index=0)

    meetings = load_meetings(year)
    continent = None
    country = None
    if not meetings.empty:
        continents = ["Todos", *sorted(meetings["Continente"].dropna().unique())]
        continent = st.sidebar.selectbox("Continente", continents)
        filtered = meetings
        if continent and continent != "Todos":
            filtered = meetings[meetings["Continente"] == continent]
        countries = sorted(filtered["Pais"].dropna().unique())
        country = st.sidebar.selectbox("Pais / Circuito", countries) if countries else None
    else:
        st.sidebar.warning("Nao foi possivel carregar os GPs.")

    top_n = st.sidebar.slider("Top N voltas", 3, 10, TOP_N_LAPS)
    return year, (continent if continent != "Todos" else None), country, top_n


def _kpis(fastest: pd.DataFrame, drivers: pd.DataFrame, teams: pd.DataFrame) -> None:
    c1, c2, c3, c4 = st.columns(4)
    best = fastest.iloc[0] if not fastest.empty else None
    c1.metric("Volta mais rapida", best["Tempo"] if best is not None else "-")
    c2.metric("Piloto", best["Piloto"] if best is not None else "-")
    c3.metric("Pilotos na sessao", len(drivers))
    c4.metric("Equipes na sessao", len(teams))


def _tab_corridas(year: int, meetings: pd.DataFrame, country: str | None) -> None:
    st.subheader("🏁 Corridas da temporada")
    if meetings.empty:
        st.info("Sem dados de GPs.")
        return
    st.dataframe(meetings, hide_index=True, use_container_width=True)
    counts = meetings.groupby("Continente").size().reset_index(name="GPs")
    fig = px.pie(
        counts,
        names="Continente",
        values="GPs",
        title=f"Distribuicao de GPs por continente - {year}",
        template=PLOTLY_TEMPLATE,
        hole=0.4,
    )
    st.plotly_chart(fig, use_container_width=True)


def _tab_voltas(fastest: pd.DataFrame) -> None:
    st.subheader("⏱️ Voltas mais rapidas")
    if fastest.empty:
        st.info("Sem voltas validas nessa sessao.")
        return
    table = fastest.drop(columns=["Segundos", "Rotulo"])
    st.dataframe(table, hide_index=True, use_container_width=True)
    fig = px.bar(
        fastest,
        x="Rotulo",
        y="Segundos",
        color="Equipe",
        text="Tempo",
        title="Tempo das voltas mais rapidas (menor = melhor)",
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        yaxis_title="Duracao (s)",
        xaxis_title="",
        yaxis_range=_axis_range(list(fastest["Segundos"])),
        xaxis={"categoryorder": "array", "categoryarray": list(fastest["Rotulo"])},
    )
    st.plotly_chart(fig, use_container_width=True)


def _tab_pilotos(drivers: pd.DataFrame) -> None:
    st.subheader("👤 Pilotos")
    if drivers.empty:
        st.info("Sem dados de pilotos.")
        return
    st.dataframe(drivers, hide_index=True, use_container_width=True)
    plot_df = drivers.dropna(subset=["Melhor (s)"])
    if not plot_df.empty:
        fig = px.bar(
            plot_df,
            x="Melhor (s)",
            y="Piloto",
            color="Equipe",
            orientation="h",
            text="Melhor volta",
            title="Melhor volta por piloto (menor = melhor)",
            template=PLOTLY_TEMPLATE,
        )
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            xaxis_range=_axis_range(list(plot_df["Melhor (s)"])),
        )
        st.plotly_chart(fig, use_container_width=True)


def _tab_equipes(teams: pd.DataFrame) -> None:
    st.subheader("👥 Equipes")
    if teams.empty:
        st.info("Sem dados de equipes.")
        return
    st.dataframe(teams, hide_index=True, use_container_width=True)
    plot_df = teams.dropna(subset=["Melhor (s)"])
    if not plot_df.empty:
        fig = px.bar(
            plot_df,
            x="Equipe",
            y="Melhor (s)",
            color="Equipe",
            text="Melhor volta",
            title="Melhor volta por equipe (menor = melhor)",
            template=PLOTLY_TEMPLATE,
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            yaxis_range=_axis_range(list(plot_df["Melhor (s)"])),
            xaxis={"categoryorder": "total ascending"},
        )
        st.plotly_chart(fig, use_container_width=True)


def _tab_resumo(drivers: pd.DataFrame) -> None:
    st.subheader("📊 Resumo geral")
    if drivers.empty:
        st.info("Sem dados para o resumo.")
        return
    plot_df = drivers.dropna(subset=["Melhor (s)", "Media (s)"])
    if plot_df.empty:
        st.info("Sem metricas suficientes.")
        return
    fig = px.scatter(
        plot_df,
        x="Media (s)",
        y="Melhor (s)",
        color="Equipe",
        size="Voltas",
        hover_name="Piloto",
        title="Consistencia x velocidade (quanto mais embaixo/esquerda, melhor)",
        template=PLOTLY_TEMPLATE,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Eixo X = media das voltas (consistencia), Eixo Y = melhor volta "
        "(velocidade de pico), tamanho = numero de voltas."
    )


def main() -> None:
    st.title("🏎️ F1 Analytics - Dados da Formula 1")
    st.caption("Dados em tempo real da OpenF1 API | Trilha Python F1")

    year, continent, country, top_n = _sidebar_filters()
    meetings = load_meetings(year)

    if not country:
        st.info("Escolha um pais/circuito no menu lateral para carregar a analise.")
        _tab_corridas(year, meetings, country)
        return

    session_key = load_session_key(year, country)
    if session_key is None:
        st.warning(f"Nenhuma corrida encontrada para {country} em {year}.")
        _tab_corridas(year, meetings, country)
        return

    fastest = load_fastest(session_key, top_n)
    drivers = load_driver_stats(session_key)
    teams = load_team_stats(session_key)

    st.markdown(f"### {country} - {year}")
    _kpis(fastest, drivers, teams)

    tabs = st.tabs(["🏁 Corridas", "⏱️ Voltas", "👤 Pilotos", "👥 Equipes", "📊 Resumo"])
    with tabs[0]:
        _tab_corridas(year, meetings, country)
    with tabs[1]:
        _tab_voltas(fastest)
    with tabs[2]:
        _tab_pilotos(drivers)
    with tabs[3]:
        _tab_equipes(teams)
    with tabs[4]:
        _tab_resumo(drivers)


if __name__ == "__main__":
    main()
