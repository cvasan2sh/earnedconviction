"""
Configuration — default model assignments, stage configs, env loading.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from forge.lib.providers import ModelConfig


# ---------------------------------------------------------------------------
# Default model assignments per agent
# These can be overridden via environment variables or CLI flags
# ---------------------------------------------------------------------------

DEFAULT_AGENT_MODELS: dict[str, ModelConfig] = {
    # Permanent agents
    "historian": ModelConfig(
        provider="anthropic", model="claude-sonnet-4-6",
        temperature=0.4, max_tokens=4096,
    ),
    "first_principles": ModelConfig(
        provider="anthropic", model="claude-opus-4-6",
        temperature=0.7, max_tokens=4096,
    ),
    "falsification": ModelConfig(
        provider="anthropic", model="claude-opus-4-6",
        temperature=0.5, max_tokens=4096,
    ),

    # Crucible — strongest available
    "crucible": ModelConfig(
        provider="anthropic", model="claude-opus-4-6",
        temperature=0.6, max_tokens=6144,
    ),

    # Problem Definition — needs precision
    "problem_definition": ModelConfig(
        provider="anthropic", model="claude-opus-4-6",
        temperature=0.4, max_tokens=2048,
    ),

    # Contextual agents
    "forced_inversion": ModelConfig(
        provider="anthropic", model="claude-sonnet-4-6",
        temperature=0.9, max_tokens=2048,
    ),
    "consumer": ModelConfig(
        provider="anthropic", model="claude-sonnet-4-6",
        temperature=0.6, max_tokens=4096,
    ),
    "business": ModelConfig(
        provider="anthropic", model="claude-sonnet-4-6",
        temperature=0.5, max_tokens=4096,
    ),
    "platform": ModelConfig(
        provider="anthropic", model="claude-sonnet-4-6",
        temperature=0.4, max_tokens=4096,
    ),
    "category_destruction": ModelConfig(
        provider="anthropic", model="claude-opus-4-6",
        temperature=0.8, max_tokens=4096,
    ),

    # Conviction mode
    "conviction": ModelConfig(
        provider="anthropic", model="claude-opus-4-6",
        temperature=0.4, max_tokens=4096,
    ),
}


def get_project_root() -> Path:
    """Get the project root (parent of forge/)."""
    return Path(__file__).parent.parent.parent


def get_forge_sessions_dir() -> str:
    """Get the forge-sessions directory path."""
    return str(get_project_root() / "forge-sessions")


def load_env() -> str | None:
    """Load environment variables from .env file. Returns path loaded, or None."""
    # Search order: forge/.env, project root .env.local, project root .env, forge/.env.example
    candidates = [
        Path(__file__).parent.parent / ".env",
        get_project_root() / ".env.local",
        get_project_root() / ".env",
        Path(__file__).parent.parent / ".env.example",
    ]

    env_path = None
    for candidate in candidates:
        if candidate.exists():
            env_path = candidate
            break

    if env_path is None:
        return None

    loaded_count = 0
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"")
                if key and value:
                    os.environ.setdefault(key, value)
                    loaded_count += 1

    return str(env_path)


def get_model_overrides_from_env() -> dict[str, ModelConfig]:
    """
    Check for model override environment variables.

    Format: FORGE_MODEL_{AGENT_NAME}={provider}:{model}
    Example: FORGE_MODEL_HISTORIAN=anthropic:claude-sonnet-4-6
    """
    overrides = {}
    for key, value in os.environ.items():
        if key.startswith("FORGE_MODEL_"):
            agent_key = key[len("FORGE_MODEL_"):].lower()
            if ":" in value:
                provider, model = value.split(":", 1)
                if agent_key in DEFAULT_AGENT_MODELS:
                    base = DEFAULT_AGENT_MODELS[agent_key]
                    overrides[agent_key] = ModelConfig(
                        provider=provider.strip(),
                        model=model.strip(),
                        temperature=base.temperature,
                        max_tokens=base.max_tokens,
                    )
    return overrides


def use_mock_provider() -> dict[str, ModelConfig]:
    """Return model overrides that route everything through the mock provider."""
    return {
        agent: ModelConfig(provider="mock", model="mock-model", temperature=0.5, max_tokens=4096)
        for agent in DEFAULT_AGENT_MODELS
    }
