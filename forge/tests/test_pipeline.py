"""End-to-end pipeline tests using mock provider."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from forge.lib.providers import ModelConfig, MockProvider, _instances
from forge.lib.session import create_session, save_session
from forge.lib.trial_logger import TrialLogger
from forge.lib.config import use_mock_provider
from forge.stages.s0_problem_definition import run_problem_definition, _parse_definition_output
from forge.stages.s1_exploration import run_exploration
from forge.stages.s2_crucible import run_crucible
from forge.stages.s3_mode_switch import run_mode_switch
from forge.stages.s4_conviction import run_conviction
from forge.stages.s5_human_clock import run_human_clock


@pytest.fixture
def mock_overrides():
    """Provide mock model overrides for all agents."""
    return use_mock_provider()


@pytest.fixture
def session():
    return create_session("Should small-holder farmers in India use AI-powered crop planning tools?")


@pytest.fixture
def trial_logger(tmp_path):
    return TrialLogger("test-pipeline", str(tmp_path))


class TestProblemDefinitionParsing:
    def test_parse_ready_output(self):
        output = """### Assessment
The problem is well-formed but needs compression.

### Hidden Assumptions
- Farmers have smartphone access
- AI models can handle local crop varieties
- Cost is affordable

### Refined Problem Statement
Can an AI crop planning tool improve yield by >15% for smallholder farmers (<5 acres) in semi-arid Indian regions within one growing season, at a cost below ₹500/season?

### Falsifiability Test
This approach fails if yield improvement is <5% or adoption rate is <10% in pilot districts after two seasons.

### Verdict
READY — the problem is dense, specific, and falsifiable."""

        parsed = _parse_definition_output(output)
        assert parsed["refined"] is not None
        assert "15%" in parsed["refined"]
        assert parsed["falsifiability"] is not None
        assert len(parsed["assumptions"]) == 3
        assert "READY" in parsed["verdict"]

    def test_parse_not_ready_output(self):
        output = """### Assessment
Too vague. What kind of AI? Which farmers?

### Hidden Assumptions
- Technology exists

### Refined Problem Statement
Needs more work.

### Falsifiability Test
Cannot define one yet.

### Verdict
NOT READY — needs specific farmer segment and measurable outcome."""

        parsed = _parse_definition_output(output)
        assert "NOT READY" in parsed["verdict"]


class TestStage0:
    def test_problem_definition_single_pass(self, session, trial_logger, mock_overrides):
        pd_config = mock_overrides.get("problem_definition")
        session = run_problem_definition(
            session=session,
            trial_logger=trial_logger,
            model_config=pd_config,
        )
        # In mock mode, refined problem defaults to raw
        assert session.problem_refined is not None
        assert session.current_stage == "problem_definition_complete"


class TestStage1:
    def test_exploration_runs(self, session, trial_logger, mock_overrides):
        session.problem_refined = "Test refined problem"
        session = run_exploration(
            session=session,
            trial_logger=trial_logger,
            model_overrides=mock_overrides,
        )
        assert len(session.agent_outputs) > 0
        assert len(session.agent_order) > 0
        assert session.current_stage == "exploration_complete"

    def test_agents_are_randomised(self, trial_logger, mock_overrides):
        """Run exploration twice — agent order should differ (probabilistically)."""
        orders = []
        for _ in range(10):
            s = create_session("Test")
            s.problem_refined = "Test problem"
            s = run_exploration(s, trial_logger, mock_overrides)
            orders.append(tuple(s.agent_order))
        # With 3+ agents and 10 runs, extremely unlikely all orders are identical
        assert len(set(orders)) > 1, "Agent order was not randomised"


class TestStage2:
    def test_crucible_runs(self, session, trial_logger, mock_overrides):
        session.problem_refined = "Test problem"
        session.agent_outputs = {
            "Historian": "History shows...",
            "First Principles": "From base truths...",
            "Falsification": "The breaking point...",
        }
        session.agent_order = ["Historian", "First Principles", "Falsification"]

        session = run_crucible(
            session=session,
            trial_logger=trial_logger,
            model_config=mock_overrides.get("crucible"),
        )
        assert session.crucible_output is not None
        assert session.current_stage == "crucible_complete"

    def test_crucible_fails_without_outputs(self, session, trial_logger, mock_overrides):
        with pytest.raises(ValueError, match="no agent outputs"):
            run_crucible(session, trial_logger, mock_overrides.get("crucible"))


class TestStage3:
    def test_mode_switch_with_signal(self, session, trial_logger):
        session.crucible_output = "Synthesis..."
        session = run_mode_switch(
            session=session,
            trial_logger=trial_logger,
            external_signal="Customer interview showed strong interest",
        )
        assert session.mode_switched is True
        assert session.external_signal is not None

    def test_mode_switch_skip(self, session, trial_logger):
        session.crucible_output = "Synthesis..."
        session = run_mode_switch(
            session=session,
            trial_logger=trial_logger,
            external_signal="skip",
        )
        assert session.mode_switched is False


class TestStage4:
    def test_conviction_runs(self, session, trial_logger, mock_overrides):
        session.problem_refined = "Test problem"
        session.crucible_output = "Synthesis output..."
        session.mode_switched = True
        session.external_signal = "Customer validated the concept"

        session = run_conviction(
            session=session,
            trial_logger=trial_logger,
            model_config=mock_overrides.get("conviction"),
        )
        assert session.conviction_output is not None
        assert session.current_stage == "conviction_complete"

    def test_conviction_fails_without_crucible(self, session, trial_logger, mock_overrides):
        session.mode_switched = True
        session.external_signal = "test"
        with pytest.raises(ValueError, match="no Crucible output"):
            run_conviction(session, trial_logger, mock_overrides.get("conviction"))

    def test_conviction_fails_without_mode_switch(self, session, trial_logger, mock_overrides):
        session.crucible_output = "test"
        with pytest.raises(ValueError, match="mode switch has not occurred"):
            run_conviction(session, trial_logger, mock_overrides.get("conviction"))


class TestStage5:
    def test_human_clock_yes(self, session, trial_logger):
        session.conviction_output = "Decision made"
        session = run_human_clock(session, trial_logger, decided=True)
        assert session.human_decided is True
        assert session.current_stage == "complete"

    def test_human_clock_no(self, session, trial_logger):
        session.conviction_output = "Decision made"
        session = run_human_clock(session, trial_logger, decided=False)
        assert session.human_decided is False


class TestFullPipeline:
    def test_exploration_pipeline(self, tmp_path, mock_overrides):
        """Full pipeline: Problem Definition → Exploration → Crucible."""
        session = create_session(
            "Should small-holder farmers in India use AI-powered crop planning tools?",
            stage="0-1",
        )
        logger = TrialLogger("full-test", str(tmp_path))

        # Stage 0
        session = run_problem_definition(session, logger,
                                          model_config=mock_overrides.get("problem_definition"))
        assert session.problem_refined is not None

        # Stage 1
        session = run_exploration(session, logger, mock_overrides)
        assert len(session.agent_outputs) >= 3

        # Stage 2
        session = run_crucible(session, logger, mock_overrides.get("crucible"))
        assert session.crucible_output is not None

        # Save
        path = save_session(session, str(tmp_path))
        assert Path(path).exists()

        # Check trial log
        summary = logger.get_summary()
        assert summary["api_calls"] > 0
        assert summary["errors"] == 0

    def test_full_pipeline_with_conviction(self, tmp_path, mock_overrides):
        """Full pipeline including conviction mode."""
        session = create_session("Should I launch a B2B SaaS?", stage="0-1")
        logger = TrialLogger("full-conviction-test", str(tmp_path))

        # Stages 0-2
        session = run_problem_definition(session, logger,
                                          model_config=mock_overrides.get("problem_definition"))
        session = run_exploration(session, logger, mock_overrides)
        session = run_crucible(session, logger, mock_overrides.get("crucible"))

        # Stage 3 — mode switch
        session = run_mode_switch(session, logger,
                                   external_signal="Pilot customer signed LOI")

        # Stage 4 — conviction
        session = run_conviction(session, logger, mock_overrides.get("conviction"))
        assert session.conviction_output is not None

        # Stage 5 — human clock
        session = run_human_clock(session, logger, decided=True)
        assert session.human_decided is True
        assert session.current_stage == "complete"

        # Save and verify both files
        path = save_session(session, str(tmp_path))
        assert Path(path).exists()
        private_path = path.replace(".md", ".private.md")
        assert Path(private_path).exists()
