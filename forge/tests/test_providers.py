"""Tests for the provider abstraction layer."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from forge.lib.providers import (
    MockProvider,
    ModelConfig,
    get_provider,
    call_llm,
    check_providers,
)
from forge.lib.trial_logger import TrialLogger


class TestMockProvider:
    def test_basic_call(self):
        provider = MockProvider()
        config = ModelConfig(provider="mock", model="mock-model")
        result = provider.call("You are a test agent", "Hello", config)
        assert "[MOCK RESPONSE #1]" in result
        assert provider._call_count == 1

    def test_canned_responses(self):
        provider = MockProvider(responses={
            "historian": "The historical record shows...",
            "falsification": "The breaking point is...",
        })
        config = ModelConfig(provider="mock", model="mock-model")

        result = provider.call("You are the Historian agent", "Test problem", config)
        assert result == "The historical record shows..."

        result = provider.call("You are the Falsification agent", "Test problem", config)
        assert result == "The breaking point is..."

    def test_is_available(self):
        provider = MockProvider()
        assert provider.is_available() is True

    def test_with_trial_logger(self, tmp_path):
        logger = TrialLogger("test-session", str(tmp_path))
        provider = MockProvider()
        config = ModelConfig(provider="mock", model="mock-model")

        result = provider.call("System", "User", config, logger)
        assert result is not None

        # Check that the trial log was written
        summary = logger.get_summary()
        assert summary["api_calls"] == 1


class TestProviderRegistry:
    def test_get_mock_provider(self):
        provider = get_provider("mock")
        assert isinstance(provider, MockProvider)

    def test_unknown_provider_raises(self):
        with pytest.raises(ValueError, match="Unknown provider"):
            get_provider("nonexistent")

    def test_call_llm_with_mock(self):
        config = ModelConfig(provider="mock", model="mock-model")
        result = call_llm("System prompt", "User message", config)
        assert "MOCK RESPONSE" in result

    def test_check_providers(self):
        available = check_providers()
        assert "mock" in available
        assert available["mock"] is True


class TestModelConfig:
    def test_defaults(self):
        config = ModelConfig(provider="anthropic", model="claude-opus-4-6")
        assert config.temperature == 0.7
        assert config.max_tokens == 4096

    def test_custom_values(self):
        config = ModelConfig(
            provider="openai",
            model="gpt-4o",
            temperature=0.9,
            max_tokens=2048,
        )
        assert config.temperature == 0.9
        assert config.max_tokens == 2048
