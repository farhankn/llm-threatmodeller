"""LLM provider abstraction and concrete client implementations."""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from typing import Any, Callable

import requests

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class LLMError(RuntimeError):
    """Base error raised by LLM clients."""


class LLMHTTPError(LLMError):
    """Error raised for provider HTTP failures."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class LLMClient(ABC):
    """Common interface for all providers."""

    @abstractmethod
    def generate(self, prompt: dict[str, str], temperature: float = 0.1) -> str:
        """Generate a response string from provider."""

    def validate(self) -> None:
        """Validate provider readiness."""


def get_llm_client(provider: str, **kwargs: Any) -> LLMClient:
    """Factory for provider-specific clients."""
    normalized = provider.strip().lower()

    if normalized == "openai":
        return OpenAIClient(**kwargs)
    if normalized == "ollama":
        return OllamaClient(**kwargs)

    raise LLMError(f"Unsupported provider '{provider}'. Expected one of: openai, ollama")


class OpenAIClient(LLMClient):
    """OpenAI chat completion client."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        timeout: float = 60.0,
        max_retries: int = 3,
        base_delay: float = 1.0,
        openai_client: Any | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay

        if not self.api_key:
            raise LLMError("OPENAI_API_KEY is not set")

        self._client = openai_client or self._build_openai_client()

    def validate(self) -> None:
        if not self.api_key:
            raise LLMError("OPENAI_API_KEY is not set")

    def generate(self, prompt: dict[str, str], temperature: float = 0.1) -> str:
        messages = [
            {"role": "system", "content": prompt.get("system", "")},
            {"role": "user", "content": prompt.get("user", "")},
        ]

        def _call() -> str:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                timeout=self.timeout,
            )
            content = response.choices[0].message.content if response.choices else None
            if not content:
                raise LLMError("OpenAI response did not include message content")
            return content

        return _retry_with_backoff(_call, max_retries=self.max_retries, base_delay=self.base_delay)

    def _build_openai_client(self) -> Any:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - dependency expected in runtime env
            raise LLMError("openai package is not installed") from exc

        return OpenAI(api_key=self.api_key)


class OllamaClient(LLMClient):
    """Ollama chat REST client."""

    def __init__(
        self,
        *,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.1",
        timeout: float = 60.0,
        max_retries: int = 3,
        base_delay: float = 1.0,
        session: requests.Session | Any | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self._session = session or requests.Session()

    def validate(self) -> None:
        try:
            response = self._session.get(f"{self.base_url}/api/tags", timeout=self.timeout)
        except requests.RequestException as exc:
            raise LLMError(f"Unable to reach Ollama at {self.base_url}: {exc}") from exc

        if response.status_code != 200:
            raise LLMHTTPError(
                f"Ollama health check failed with status {response.status_code}",
                status_code=response.status_code,
            )

    def generate(self, prompt: dict[str, str], temperature: float = 0.1) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": prompt.get("system", "")},
                {"role": "user", "content": prompt.get("user", "")},
            ],
            "options": {"temperature": temperature},
        }

        def _call() -> str:
            try:
                response = self._session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                raise LLMError(f"Ollama request failed: {exc}") from exc

            if response.status_code != 200:
                raise LLMHTTPError(
                    f"Ollama returned status {response.status_code}",
                    status_code=response.status_code,
                )

            data = response.json()
            content = data.get("message", {}).get("content")
            if not content:
                raise LLMError("Ollama response did not include message.content")

            return content

        return _retry_with_backoff(_call, max_retries=self.max_retries, base_delay=self.base_delay)


def _retry_with_backoff(
    fn: Callable[[], str],
    *,
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> str:
    """Run a call with exponential retry for 429/5xx and transient transport errors."""
    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - provider SDK errors vary by type
            last_error = exc
            if not _is_retryable_error(exc) or attempt == max_retries - 1:
                break
            delay = base_delay * (backoff_factor**attempt)
            time.sleep(delay)

    message = f"LLM request failed after {max_retries} attempts"
    if last_error is not None:
        raise LLMError(f"{message}: {last_error}") from last_error
    raise LLMError(message)


def _is_retryable_error(error: Exception) -> bool:
    status = _extract_status_code(error)
    if status in RETRYABLE_STATUS_CODES:
        return True

    if isinstance(error, requests.RequestException):
        return True

    return False


def _extract_status_code(error: Exception) -> int | None:
    status_code = getattr(error, "status_code", None)
    if isinstance(status_code, int):
        return status_code

    response = getattr(error, "response", None)
    if response is not None:
        response_status = getattr(response, "status_code", None)
        if isinstance(response_status, int):
            return response_status

    return None
