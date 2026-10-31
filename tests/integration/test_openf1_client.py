"""Teste de integracao real contra a OpenF1 (opt-in).

So roda quando a env RUN_INTEGRATION=1 estiver definida, para nao depender de
rede no CI nem nos testes unitarios do dia a dia.
"""

from __future__ import annotations

import os

import pytest

from f1.ingestion.openf1_client import OpenF1Client

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="defina RUN_INTEGRATION=1 para rodar testes de integracao",
)


def test_get_sessions_real() -> None:
    client = OpenF1Client()
    sessions = client.get_sessions(year=2024, country_name="Brazil", session_name="Race")
    assert sessions
    assert sessions[0].session_key > 0
