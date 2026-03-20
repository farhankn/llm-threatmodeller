import os
from types import SimpleNamespace

import pytest

from threatcli.llm_client import (
    LLMError,
    LLMHTTPError,
    OllamaClient,
    OpenAIClient,
    _retry_with_backoff,
    get_llm_client,
)


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict | None = None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self) -> dict:
        return self._payload


class _FakeSession:
    def __init__(self, responses: list[_FakeResponse]):
        self._responses = responses
        self.post_calls = 0
        self.get_calls = 0

    def post(self, *_args, **_kwargs) -> _FakeResponse:
        response = self._responses[min(self.post_calls, len(self._responses) - 1)]
        self.post_calls += 1
        return response

    def get(self, *_args, **_kwargs) -> _FakeResponse:
        response = self._responses[min(self.get_calls, len(self._responses) - 1)]
        self.get_calls += 1
        return response


def test_get_llm_client_rejects_unknown_provider() -> None:
    with pytest.raises(LLMError):
        get_llm_client("unknown")


def test_openai_client_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(LLMError):
        OpenAIClient(openai_client=object())


def test_retry_with_backoff_retries_retryable_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = {"count": 0}
    delays: list[float] = []

    def _fake_sleep(delay: float) -> None:
        delays.append(delay)

    monkeypatch.setattr("threatcli.llm_client.time.sleep", _fake_sleep)

    def _fn() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise LLMHTTPError("rate limited", status_code=429)
        return "ok"

    value = _retry_with_backoff(_fn, max_retries=3, base_delay=1.0)

    assert value == "ok"
    assert attempts["count"] == 3
    assert delays == [1.0, 2.0]


def test_retry_with_backoff_stops_on_non_retryable_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("threatcli.llm_client.time.sleep", lambda _delay: None)

    def _fn() -> str:
        raise LLMHTTPError("bad request", status_code=400)

    with pytest.raises(LLMError) as exc:
        _retry_with_backoff(_fn, max_retries=3, base_delay=1.0)

    assert "after 3 attempts" in str(exc.value)


def test_openai_generate_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    fake_message = SimpleNamespace(content="threat output")
    fake_choice = SimpleNamespace(message=fake_message)
    fake_response = SimpleNamespace(choices=[fake_choice])

    class _FakeCompletions:
        def create(self, **_kwargs):
            return fake_response

    fake_chat = SimpleNamespace(completions=_FakeCompletions())
    fake_client = SimpleNamespace(chat=fake_chat)

    client = OpenAIClient(openai_client=fake_client)
    output = client.generate({"system": "sys", "user": "usr"}, temperature=0.2)

    assert output == "threat output"


def test_ollama_generate_retries_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    delays: list[float] = []
    monkeypatch.setattr("threatcli.llm_client.time.sleep", lambda delay: delays.append(delay))

    session = _FakeSession(
        [
            _FakeResponse(500, {}),
            _FakeResponse(200, {"message": {"content": "ok"}}),
        ]
    )

    client = OllamaClient(session=session)
    output = client.generate({"system": "sys", "user": "usr"})

    assert output == "ok"
    assert session.post_calls == 2
    assert delays == [1.0]


def test_ollama_validate_checks_health() -> None:
    session = _FakeSession([_FakeResponse(200, {"models": []})])
    client = OllamaClient(session=session)

    client.validate()
    assert session.get_calls == 1


def test_get_llm_client_builds_ollama_instance() -> None:
    client = get_llm_client("ollama", session=_FakeSession([_FakeResponse(200, {"models": []})]))
    assert isinstance(client, OllamaClient)


def test_get_llm_client_builds_openai_instance(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "key")

    fake_message = SimpleNamespace(content="ok")
    fake_choice = SimpleNamespace(message=fake_message)
    fake_response = SimpleNamespace(choices=[fake_choice])

    class _FakeCompletions:
        def create(self, **_kwargs):
            return fake_response

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=_FakeCompletions()))
    client = get_llm_client("openai", openai_client=fake_client)

    assert isinstance(client, OpenAIClient)


def test_openai_client_reads_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")

    fake_message = SimpleNamespace(content="ok")
    fake_choice = SimpleNamespace(message=fake_message)
    fake_response = SimpleNamespace(choices=[fake_choice])

    class _FakeCompletions:
        def create(self, **_kwargs):
            return fake_response

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=_FakeCompletions()))

    client = OpenAIClient(openai_client=fake_client)
    assert client.api_key == "env-key"


def test_openai_generate_raises_when_content_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    fake_response = SimpleNamespace(choices=[])

    class _FakeCompletions:
        def create(self, **_kwargs):
            return fake_response

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=_FakeCompletions()))

    client = OpenAIClient(openai_client=fake_client)

    with pytest.raises(LLMError):
        client.generate({"system": "sys", "user": "usr"})


@pytest.mark.skipif(not hasattr(os, "environ"), reason="environment support required")
def test_ollama_generate_raises_on_non_retryable_status(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("threatcli.llm_client.time.sleep", lambda _delay: None)

    session = _FakeSession([_FakeResponse(400, {})])
    client = OllamaClient(session=session)

    with pytest.raises(LLMError):
        client.generate({"system": "sys", "user": "usr"})
