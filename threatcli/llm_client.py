"""LLM provider abstraction and concrete client implementations."""

from __future__ import annotations

import os
import sys
import time
from abc import ABC, abstractmethod
from pathlib import Path
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
    if normalized == "gemini":
        return GeminiClient(**kwargs)
    if normalized == "ollama":
        return OllamaClient(**kwargs)

    raise LLMError(f"Unsupported provider '{provider}'. Expected one of: openai, gemini, ollama")


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
        self.api_key = api_key or _resolve_api_key("OPENAI_API_KEY")
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


class GeminiClient(LLMClient):
    """Google Gemini REST client using the Generative Language API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str = "gemini-2.5-pro",
        base_url: str | None = None,
        api_version: str | None = None,
        api_mode: str | None = None,
        timeout: float = 60.0,
        max_retries: int = 3,
        base_delay: float = 1.0,
        session: requests.Session | Any | None = None,
    ) -> None:
        self.api_key = api_key or _resolve_api_key("GEMINI_API_KEY", "GOOGLE_API_KEY")
        self.model = model
        self.api_mode = (api_mode or os.getenv("GEMINI_API_MODE", "generative")).strip().lower()
        default_base_url = (
            "https://aiplatform.googleapis.com"
            if self.api_mode == "vertex"
            else "https://generativelanguage.googleapis.com"
        )
        default_api_version = "v1" if self.api_mode == "vertex" else "v1beta"
        resolved_base_url = base_url or os.getenv("GEMINI_BASE_URL") or default_base_url
        resolved_api_version = api_version or os.getenv("GEMINI_API_VERSION") or default_api_version
        self.base_url = resolved_base_url.rstrip("/")
        self.api_version = resolved_api_version
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self._session = session or requests.Session()

        if not self.api_key:
            raise LLMError("GEMINI_API_KEY or GOOGLE_API_KEY is not set")

    def validate(self) -> None:
        if not self.api_key:
            raise LLMError("GEMINI_API_KEY or GOOGLE_API_KEY is not set")
        if self.api_mode == "vertex":
            return

        try:
            response = self._session.get(
                f"{self.base_url}/{self.api_version}/models",
                params={"key": self.api_key},
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise LLMError(f"Unable to reach Gemini API at {self.base_url}: {exc}") from exc

        if response.status_code != 200:
            raise LLMHTTPError(
                f"Gemini health check failed with status {response.status_code}",
                status_code=response.status_code,
            )

    def generate(self, prompt: dict[str, str], temperature: float = 0.1) -> str:
        payload = _build_gemini_payload(prompt, temperature, api_mode=self.api_mode)

        def _call() -> str:
            try:
                endpoint = _build_gemini_endpoint(
                    base_url=self.base_url,
                    api_version=self.api_version,
                    model=self.model,
                    api_mode=self.api_mode,
                )
                response = self._session.post(
                    endpoint,
                    params={"key": self.api_key},
                    json=payload,
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                raise LLMError(f"Gemini request failed: {exc}") from exc

            if response.status_code != 200:
                raise LLMHTTPError(
                    f"Gemini returned status {response.status_code}",
                    status_code=response.status_code,
                )

            return _extract_gemini_text(response.json())

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
    debug_enabled = _llm_debug_enabled()

    for attempt in range(max_retries):
        attempt_number = attempt + 1
        try:
            if debug_enabled:
                _llm_debug(f"attempt {attempt_number}/{max_retries}: sending request")
            return fn()
        except Exception as exc:  # noqa: BLE001 - provider SDK errors vary by type
            last_error = exc
            retryable = _is_retryable_error(exc)
            if debug_enabled:
                status = _extract_status_code(exc)
                _llm_debug(
                    "attempt "
                    f"{attempt_number}/{max_retries}: {exc.__class__.__name__} "
                    f"(status={status}, retryable={retryable}) {_truncate_debug(str(exc))}"
                )
            if not retryable or attempt == max_retries - 1:
                break
            delay = base_delay * (backoff_factor**attempt)
            if debug_enabled:
                _llm_debug(f"attempt {attempt_number}/{max_retries}: retrying in {delay:.2f}s")
            time.sleep(delay)

    message = f"LLM request failed after {max_retries} attempts"
    if last_error is not None:
        if debug_enabled:
            _llm_debug(f"all attempts failed: {_truncate_debug(str(last_error))}")
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


def _extract_gemini_text(data: dict[str, Any]) -> str:
    candidates = data.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        raise LLMError("Gemini response did not include candidates")

    first = candidates[0]
    if not isinstance(first, dict):
        raise LLMError("Gemini response candidate is malformed")

    content = first.get("content", {})
    if not isinstance(content, dict):
        raise LLMError("Gemini response content is malformed")

    parts = content.get("parts", [])
    if not isinstance(parts, list):
        raise LLMError("Gemini response content.parts is malformed")

    text_parts = []
    for part in parts:
        if isinstance(part, dict):
            text = part.get("text")
            if isinstance(text, str) and text.strip():
                text_parts.append(text)

    if not text_parts:
        raise LLMError("Gemini response did not include text content")

    return "\n".join(text_parts)


def _build_gemini_endpoint(*, base_url: str, api_version: str, model: str, api_mode: str) -> str:
    if api_mode == "vertex":
        return f"{base_url}/{api_version}/publishers/google/models/{model}:generateContent"
    return f"{base_url}/{api_version}/models/{model}:generateContent"


def _build_gemini_payload(prompt: dict[str, str], temperature: float, *, api_mode: str) -> dict[str, Any]:
    if api_mode == "vertex":
        combined_text = f"{prompt.get('system', '').strip()}\n\n{prompt.get('user', '').strip()}".strip()
        return {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": combined_text}],
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "responseMimeType": "application/json",
            },
        }

    return {
        "system_instruction": {
            "parts": [{"text": prompt.get("system", "")}],
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt.get("user", "")}],
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "responseMimeType": "application/json",
        },
    }


def _resolve_api_key(*env_names: str) -> str | None:
    for env_name in env_names:
        direct = os.getenv(env_name)
        if direct:
            return direct

        file_env = os.getenv(f"{env_name}_FILE")
        if not file_env:
            continue

        key_path = Path(file_env)
        try:
            key = key_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise LLMError(f"Unable to read API key file '{key_path}': {exc}") from exc

        if key:
            return key

    return None


def _llm_debug_enabled() -> bool:
    return os.getenv("TM_LLM_DEBUG", "").strip().lower() in {"1", "true", "yes", "on"}


def _llm_debug(message: str) -> None:
    print(f"[llm-debug] {message}", file=sys.stderr, flush=True)


def _truncate_debug(message: str, limit: int = 240) -> str:
    if len(message) <= limit:
        return message
    return message[: limit - 3] + "..."
