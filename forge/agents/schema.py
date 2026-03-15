"""
Agent schema — defines what an agent IS in The Forge.

Every agent is a perspective with constraints, not a personality.
The system prompt is the soul of the agent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from forge.lib.providers import ModelConfig


@dataclass
class AgentDefinition:
    """
    A Forge agent definition.

    An agent is not a chatbot. It is an epistemological lens —
    a constrained way of examining a problem. The system_prompt
    encodes what the agent sees, what it ignores, and how it reasons.
    """

    # Identity
    name: str
    role: str  # One-line description of the agent's function
    description: str  # Longer explanation of the agent's epistemology

    # The system prompt — this is the agent
    system_prompt: str

    # Model configuration — which LLM and settings to use
    model_config: ModelConfig

    # Behaviour flags
    is_permanent: bool = True  # Permanent agents run in every session
    is_contextual: bool = False  # Contextual agents are selected per problem
    active_when: Optional[str] = None  # Condition for contextual activation
    intake_only: bool = False  # If True, runs at intake before parliament (e.g. Forced Inversion)

    # Output constraints
    max_output_tokens: Optional[int] = None  # Override model_config if set

    def get_model_config(self) -> ModelConfig:
        """Return model config, applying any per-agent overrides."""
        if self.max_output_tokens and self.max_output_tokens != self.model_config.max_tokens:
            return ModelConfig(
                provider=self.model_config.provider,
                model=self.model_config.model,
                temperature=self.model_config.temperature,
                max_tokens=self.max_output_tokens,
            )
        return self.model_config
