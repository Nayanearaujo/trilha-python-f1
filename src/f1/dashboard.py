"""Dashboard Streamlit: 5 voltas mais rapidas por circuito (OpenF1).

Camada de apresentacao: apenas orquestra servicos e exibe os dados.
Rode com:  poetry run streamlit run src/f1/dashboard.py
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from f1.domain.services import FastestLapsService
from f1.ingestion.openf1_client import OpenF1Client
from f1.utils.config import TOP_N_LAPS


@st.cache_data(show_spinner=False)
def _load_sessions(year: int, country: str) -> list[dict]:
    client = OpenF1Client()
    sessions = client.get_sessions(year=year, country_name=country or None, session_name="Race")
    return [s.model_dump() for s in sessions]


def main() -> None:
    st.set_page_config(page_title="F1 - Voltas mais rapidas", page_icon="🏎️")
    st.title("🏎️ Formula 1 - Voltas mais rapidas por circuito")
    st.caption("Dados em tempo real da OpenF1 API")

    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Ano", min_value=2023, max_value=2026, value=2024, step=1)
    with col2:
        country = st.text_input("Pais (circuito)", value="Brazil")

    top_n = st.slider("Quantidade de voltas", 1, 10, TOP_N_LAPS)

    if not st.button("Buscar voltas mais rapidas"):
        st.info("Escolha ano e pais e clique em buscar.")
        return

    try:
        sessions = _load_sessions(int(year), country)
    except Exception as exc:  # noqa: BLE001 - erro amigavel na UI
        st.error(f"Falha ao consultar a API: {exc}")
        return

    if not sessions:
        st.warning("Nenhuma sessao de corrida encontrada para esse ano/pais.")
        return

    session = sessions[0]
    st.subheader(
        f"{session.get('circuit_short_name') or country} "
        f"- {session.get('session_name')} {session.get('year')}"
    )

    service = FastestLapsService()
    try:
        laps = service.fastest_laps_for_session(session["session_key"], top_n=top_n)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Falha ao carregar as voltas: {exc}")
        return

    if not laps:
        st.warning("Nenhuma volta valida encontrada para essa sessao.")
        return

    df = pd.DataFrame(
        {
            "Posicao": lap.position,
            "Piloto": lap.driver_name,
            "Equipe": lap.team_name,
            "Volta": lap.lap_number,
            "Tempo": lap.lap_time_formatted,
            "Segundos": round(lap.lap_duration, 3),
        }
        for lap in laps
    )

    st.dataframe(df.drop(columns=["Segundos"]), hide_index=True, use_container_width=True)

    fig = px.bar(
        df,
        x="Piloto",
        y="Segundos",
        color="Equipe",
        text="Tempo",
        title="Tempo das voltas mais rapidas (segundos)",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_title="Duracao (s)", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
