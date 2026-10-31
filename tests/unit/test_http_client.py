"""Testes do HttpClient generico (requests mockado)."""

from __future__ import annotations

import pytest
import requests

from f1.ingestion.http_client import HttpClient, HttpError


class _FakeResponse:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status = status

    def raise_for_status(self):
        if self.status >= 400:
            raise requests.HTTPError(f"status {self.status}")

    def json(self):
        return self._payload


class _FakeSession:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0

    def get(self, url, params=None, timeout=None):
        self.calls += 1
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def test_get_json_sucesso() -> None:
    session = _FakeSession([_FakeResponse([{"a": 1}])])
    client = HttpClient(session=session)
    assert client.get_json("http://x/y") == [{"a": 1}]
    assert session.calls == 1


def test_get_json_retry_e_sucesso() -> None:
    session = _FakeSession([requests.ConnectionError("boom"), _FakeResponse([{"ok": True}])])
    client = HttpClient(session=session, max_retries=2, backoff=0)
    assert client.get_json("http://x/y") == [{"ok": True}]
    assert session.calls == 2


def test_get_json_falha_apos_retries() -> None:
    session = _FakeSession([requests.ConnectionError("1"), requests.ConnectionError("2")])
    client = HttpClient(session=session, max_retries=1, backoff=0)
    with pytest.raises(HttpError):
        client.get_json("http://x/y")
