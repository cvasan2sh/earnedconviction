"""Tests for agent definitions and registry."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from forge.agents.schema import AgentDefinition
from forge.agents.registry import (
    create_agent,
    get_permanent_agents,
    get_contextual_agents,
    get_parliament,
    list_all_agents,
)
from forge.lib.providers import ModelConfig


class TestAgentCreation:
    def test_create_historian(self):
        agent = create_agent("historian")
        assert agent.name == "Historian"
        assert agent.is_permanent is True
        assert agent.model_config.provider == "anthropic"
        assert len(agent.system_prompt) > 100

    def test_create_first_principles(self):
        agent = create_agent("first_principles")
        assert agent.name == "First Principles"
        assert agent.is_permanent is True
        assert agent.model_config.provider == "anthropic"

    def test_create_falsification(self):
        agent = create_agent("falsification")
        assert agent.name == "Falsification"
        assert agent.is_permanent is True

    def test_create_forced_inversion(self):
        agent = create_agent("forced_inversion")
        assert agent.name == "Forced Inversion"
        assert agent.is_contextual is True
        assert agent.intake_only is True

    def test_create_crucible(self):
        agent = create_agent("crucible")
        assert agent.name == "Crucible"
        assert agent.model_config.max_tokens == 6144  # Crucible gets extra tokens

    def test_create_problem_definition(self):
        agent = create_agent("problem_definition")
        assert agent.name == "Problem Definition"

    def test_create_with_override(self):
        override = ModelConfig(provider="mock", model="mock-model")
        agent = create_agent("historian", override)
        assert agent.model_config.provider == "mock"

    def test_create_unknown_agent_raises(self):
        with pytest.raises(ValueError, match="Unknown agent"):
            create_agent("nonexistent_agent")

    def test_all_agents_have_system_prompts(self):
        agents_list = list_all_agents()
        for agent_info in agents_list:
            agent = create_agent(agent_info["key"])
            assert len(agent.system_prompt) > 50, f"{agent.name} has no system prompt"

    def test_all_agents_have_blind_rule(self):
        """Permanent + contextual agents must have blind output rule in prompt."""
        skip = {"Problem Definition", "Crucible", "Forced Inversion"}
        agents_list = list_all_agents()
        for agent_info in agents_list:
            agent = create_agent(agent_info["key"])
            if agent.name in skip:
                continue
            assert "blind" in agent.system_prompt.lower(), (
                f"{agent.name} is missing blind output rule in system prompt"
            )


class TestPermanentAgents:
    def test_returns_three_permanent(self):
        agents = get_permanent_agents()
        names = {a.name for a in agents}
        assert "Historian" in names
        assert "First Principles" in names
        assert "Falsification" in names
        assert "Crucible" not in names  # Crucible is separate
        assert "Problem Definition" not in names

    def test_override_models(self):
        mock = ModelConfig(provider="mock", model="mock-model")
        agents = get_permanent_agents({"historian": mock})
        historian = next(a for a in agents if a.name == "Historian")
        assert historian.model_config.provider == "mock"


class TestContextualAgents:
    def test_0_1_stage_includes_forced_inversion(self):
        agents = get_contextual_agents("0-1")
        names = {a.name for a in agents}
        assert "Forced Inversion" in names

    def test_10_100_stage_includes_category_destruction(self):
        agents = get_contextual_agents("10-100")
        names = {a.name for a in agents}
        assert "Category Destruction" in names

    def test_explicit_include(self):
        agents = get_contextual_agents("0-1", include=["Consumer", "Business"])
        names = {a.name for a in agents}
        assert "Consumer" in names
        assert "Business" in names


class TestParliament:
    def test_parliament_0_1(self):
        parliament = get_parliament("0-1")
        names = {a.name for a in parliament}
        # Should have 3 permanent — Forced Inversion is intake-only, excluded
        assert "Historian" in names
        assert "First Principles" in names
        assert "Falsification" in names
        assert "Forced Inversion" not in names  # Intake-only
        assert "Crucible" not in names

    def test_parliament_10_100(self):
        parliament = get_parliament("10-100")
        names = {a.name for a in parliament}
        assert "Category Destruction" in names

    def test_parliament_with_extras(self):
        parliament = get_parliament("0-1", include_contextual=["Consumer"])
        names = {a.name for a in parliament}
        assert "Consumer" in names


class TestListAgents:
    def test_lists_all(self):
        agents = list_all_agents()
        assert len(agents) >= 10  # We defined 10 agents
        names = {a["name"] for a in agents}
        assert "Historian" in names
        assert "Crucible" in names
