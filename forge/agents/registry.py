"""
Agent Registry — single source of truth for all Forge agents.

Handles agent creation, listing, and selection based on problem stage.
"""

from __future__ import annotations

from typing import Optional

from forge.agents.schema import AgentDefinition
from forge.lib.providers import ModelConfig

# Import all agent modules
from forge.agents import (
    historian,
    first_principles,
    falsification,
    forced_inversion,
    consumer,
    business,
    platform,
    category_destruction,
    crucible,
    problem_definition,
)


# Map of agent name -> module
_AGENT_MODULES = {
    "historian": historian,
    "first_principles": first_principles,
    "falsification": falsification,
    "forced_inversion": forced_inversion,
    "consumer": consumer,
    "business": business,
    "platform": platform,
    "category_destruction": category_destruction,
    "crucible": crucible,
    "problem_definition": problem_definition,
}


def create_agent(
    name: str,
    model_config: Optional[ModelConfig] = None,
) -> AgentDefinition:
    """Create a single agent by name, optionally overriding its model config."""
    key = name.lower().replace(" ", "_").replace("-", "_")
    if key not in _AGENT_MODULES:
        raise ValueError(
            f"Unknown agent '{name}'. Available: {list(_AGENT_MODULES.keys())}"
        )
    return _AGENT_MODULES[key].create(model_config)


def get_permanent_agents(
    model_overrides: Optional[dict[str, ModelConfig]] = None,
) -> list[AgentDefinition]:
    """Return all permanent parliament agents (excludes Crucible and Problem Definition)."""
    overrides = model_overrides or {}
    agents = []
    for key, mod in _AGENT_MODULES.items():
        agent = mod.create(overrides.get(key))
        if agent.is_permanent and agent.name not in ("Crucible", "Problem Definition"):
            agents.append(agent)
    return agents


def get_contextual_agents(
    stage: str,
    include: Optional[list[str]] = None,
    model_overrides: Optional[dict[str, ModelConfig]] = None,
) -> list[AgentDefinition]:
    """
    Return contextual agents appropriate for the given stage.

    Args:
        stage: "0-1", "1-10", or "10-100"
        include: Optional list of additional agent names to include
        model_overrides: Optional per-agent model config overrides
    """
    overrides = model_overrides or {}
    include_set = set((include or []))
    agents = []

    for key, mod in _AGENT_MODULES.items():
        agent = mod.create(overrides.get(key))
        if not agent.is_contextual:
            continue

        # Stage-based activation
        should_include = False

        if agent.name == "Forced Inversion" and stage == "0-1":
            should_include = True
        elif agent.name == "Category Destruction" and stage == "10-100":
            should_include = True
        elif agent.name in include_set:
            should_include = True

        if should_include:
            agents.append(agent)

    return agents


def get_parliament(
    stage: str,
    include_contextual: Optional[list[str]] = None,
    model_overrides: Optional[dict[str, ModelConfig]] = None,
) -> list[AgentDefinition]:
    """
    Assemble the full parliament for a session.

    Returns permanent agents + stage-appropriate contextual agents.
    Does NOT include Crucible or Problem Definition (they're separate stages).
    """
    permanent = get_permanent_agents(model_overrides)
    contextual = get_contextual_agents(stage, include_contextual, model_overrides)
    # Exclude intake-only agents — they run before parliament, not in it
    contextual = [a for a in contextual if not a.intake_only]
    return permanent + contextual


def list_all_agents() -> list[dict[str, str]]:
    """List all available agents with their metadata."""
    result = []
    for key, mod in _AGENT_MODULES.items():
        agent = mod.create()
        result.append({
            "key": key,
            "name": agent.name,
            "role": agent.role,
            "permanent": agent.is_permanent,
            "contextual": agent.is_contextual,
            "intake_only": agent.intake_only,
            "default_provider": agent.model_config.provider,
            "default_model": agent.model_config.model,
        })
    return result
