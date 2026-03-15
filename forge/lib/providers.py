"""
LLM Provider abstraction layer.

Supports Anthropic (Claude), OpenAI (GPT), and Google (Gemini).
Each agent can specify its own provider and model.
"""

from __future__ import annotations

import os
import time
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from forge.lib.trial_logger import TrialLogger


# ---------------------------------------------------------------------------
# Provider configuration
# ---------------------------------------------------------------------------

@dataclass
class ModelConfig:
    """Configuration for a specific model call."""
    provider: str  # "anthropic", "openai", "google"
    model: str  # e.g. "claude-opus-4-6", "gpt-4o", "gemini-2.5-pro"
    temperature: float = 0.7
    max_tokens: int = 4096


# ---------------------------------------------------------------------------
# Base provider
# ---------------------------------------------------------------------------

class LLMProvider(ABC):
    """Abstract base for LLM providers."""

    @abstractmethod
    def call(
        self,
        system_prompt: str,
        user_message: str,
        model_config: ModelConfig,
        trial_logger: Optional[TrialLogger] = None,
    ) -> str:
        """Send a message and return the response text."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider's API key is configured."""
        ...


# ---------------------------------------------------------------------------
# Anthropic (Claude)
# ---------------------------------------------------------------------------

class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            from anthropic import Anthropic
            self._client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        return self._client

    def is_available(self) -> bool:
        return bool(os.environ.get("ANTHROPIC_API_KEY"))

    def call(
        self,
        system_prompt: str,
        user_message: str,
        model_config: ModelConfig,
        trial_logger: Optional[TrialLogger] = None,
    ) -> str:
        client = self._get_client()
        start = time.time()

        if trial_logger:
            trial_logger.log_api_call_start(
                provider="anthropic",
                model=model_config.model,
                system_prompt_preview=system_prompt[:200],
                user_message_preview=user_message[:200],
            )

        try:
            response = client.messages.create(
                model=model_config.model,
                max_tokens=model_config.max_tokens,
                temperature=model_config.temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            elapsed = time.time() - start
            text = response.content[0].text

            if trial_logger:
                trial_logger.log_api_call_end(
                    provider="anthropic",
                    model=model_config.model,
                    elapsed_seconds=elapsed,
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens,
                    response_preview=text[:300],
                    success=True,
                )
            return text

        except Exception as e:
            elapsed = time.time() - start
            if trial_logger:
                trial_logger.log_api_call_end(
                    provider="anthropic",
                    model=model_config.model,
                    elapsed_seconds=elapsed,
                    input_tokens=0,
                    output_tokens=0,
                    response_preview="",
                    success=False,
                    error=str(e),
                )
            raise


# ---------------------------------------------------------------------------
# OpenAI (GPT)
# ---------------------------------------------------------------------------

class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        return self._client

    def is_available(self) -> bool:
        return bool(os.environ.get("OPENAI_API_KEY"))

    def call(
        self,
        system_prompt: str,
        user_message: str,
        model_config: ModelConfig,
        trial_logger: Optional[TrialLogger] = None,
    ) -> str:
        client = self._get_client()
        start = time.time()

        if trial_logger:
            trial_logger.log_api_call_start(
                provider="openai",
                model=model_config.model,
                system_prompt_preview=system_prompt[:200],
                user_message_preview=user_message[:200],
            )

        try:
            response = client.chat.completions.create(
                model=model_config.model,
                max_tokens=model_config.max_tokens,
                temperature=model_config.temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            elapsed = time.time() - start
            text = response.choices[0].message.content

            if trial_logger:
                trial_logger.log_api_call_end(
                    provider="openai",
                    model=model_config.model,
                    elapsed_seconds=elapsed,
                    input_tokens=response.usage.prompt_tokens if response.usage else 0,
                    output_tokens=response.usage.completion_tokens if response.usage else 0,
                    response_preview=text[:300],
                    success=True,
                )
            return text

        except Exception as e:
            elapsed = time.time() - start
            if trial_logger:
                trial_logger.log_api_call_end(
                    provider="openai",
                    model=model_config.model,
                    elapsed_seconds=elapsed,
                    input_tokens=0,
                    output_tokens=0,
                    response_preview="",
                    success=False,
                    error=str(e),
                )
            raise


# ---------------------------------------------------------------------------
# Google (Gemini)
# ---------------------------------------------------------------------------

class GoogleProvider(LLMProvider):
    """Google Gemini provider."""

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            from google import genai
            self._client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        return self._client

    def is_available(self) -> bool:
        return bool(os.environ.get("GOOGLE_API_KEY"))

    def call(
        self,
        system_prompt: str,
        user_message: str,
        model_config: ModelConfig,
        trial_logger: Optional[TrialLogger] = None,
    ) -> str:
        client = self._get_client()
        start = time.time()

        if trial_logger:
            trial_logger.log_api_call_start(
                provider="google",
                model=model_config.model,
                system_prompt_preview=system_prompt[:200],
                user_message_preview=user_message[:200],
            )

        try:
            from google.genai import types

            response = client.models.generate_content(
                model=model_config.model,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=model_config.temperature,
                    max_output_tokens=model_config.max_tokens,
                ),
            )
            elapsed = time.time() - start
            text = response.text

            if trial_logger:
                input_tok = getattr(response.usage_metadata, "prompt_token_count", 0) or 0
                output_tok = getattr(response.usage_metadata, "candidates_token_count", 0) or 0
                trial_logger.log_api_call_end(
                    provider="google",
                    model=model_config.model,
                    elapsed_seconds=elapsed,
                    input_tokens=input_tok,
                    output_tokens=output_tok,
                    response_preview=text[:300],
                    success=True,
                )
            return text

        except Exception as e:
            elapsed = time.time() - start
            if trial_logger:
                trial_logger.log_api_call_end(
                    provider="google",
                    model=model_config.model,
                    elapsed_seconds=elapsed,
                    input_tokens=0,
                    output_tokens=0,
                    response_preview="",
                    success=False,
                    error=str(e),
                )
            raise


# ---------------------------------------------------------------------------
# Mock provider (for testing and dry runs)
# ---------------------------------------------------------------------------

class MockProvider(LLMProvider):
    """Mock provider for testing — returns canned responses."""

    def __init__(self, responses: Optional[dict[str, str]] = None):
        self._responses = responses or {}
        self._call_count = 0

    def is_available(self) -> bool:
        return True

    def call(
        self,
        system_prompt: str,
        user_message: str,
        model_config: ModelConfig,
        trial_logger: Optional[TrialLogger] = None,
    ) -> str:
        self._call_count += 1
        start = time.time()

        if trial_logger:
            trial_logger.log_api_call_start(
                provider="mock",
                model="mock-model",
                system_prompt_preview=system_prompt[:200],
                user_message_preview=user_message[:200],
            )

        # Check if there's a canned response for any keyword in the system prompt
        response_text = None
        for keyword, response in self._responses.items():
            if keyword.lower() in system_prompt.lower():
                response_text = response
                break

        if response_text is None:
            response_text = (
                f"[MOCK RESPONSE #{self._call_count}]\n\n"
                f"System prompt received ({len(system_prompt)} chars). "
                f"User message received ({len(user_message)} chars).\n\n"
                f"This is a mock response for testing. In production, this would be "
                f"a real LLM response from {model_config.provider}/{model_config.model}."
            )

        elapsed = time.time() - start
        if trial_logger:
            trial_logger.log_api_call_end(
                provider="mock",
                model="mock-model",
                elapsed_seconds=elapsed,
                input_tokens=len(system_prompt.split()) + len(user_message.split()),
                output_tokens=len(response_text.split()),
                response_preview=response_text[:300],
                success=True,
            )

        return response_text


# ---------------------------------------------------------------------------
# Provider registry
# ---------------------------------------------------------------------------

_PROVIDERS: dict[str, type[LLMProvider]] = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "google": GoogleProvider,
    "mock": MockProvider,
}

_instances: dict[str, LLMProvider] = {}


def get_provider(name: str) -> LLMProvider:
    """Get or create a provider instance by name."""
    if name not in _instances:
        if name not in _PROVIDERS:
            raise ValueError(
                f"Unknown provider '{name}'. Available: {list(_PROVIDERS.keys())}"
            )
        _instances[name] = _PROVIDERS[name]()
    return _instances[name]


def call_llm(
    system_prompt: str,
    user_message: str,
    model_config: ModelConfig,
    trial_logger: Optional[TrialLogger] = None,
) -> str:
    """
    Universal LLM call — routes to the correct provider based on model_config.
    This is the single function the rest of the system uses.
    """
    provider = get_provider(model_config.provider)
    return provider.call(system_prompt, user_message, model_config, trial_logger)


def check_providers() -> dict[str, bool]:
    """Check which providers are available (have API keys configured)."""
    return {name: cls().is_available() for name, cls in _PROVIDERS.items()}
