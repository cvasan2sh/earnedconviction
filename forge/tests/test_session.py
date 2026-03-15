"""Tests for session management."""

import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from forge.lib.session import (
    Session,
    create_session,
    save_session,
    load_session,
    _slugify,
)


class TestSessionCreation:
    def test_create_session(self):
        session = create_session("Should I build a SaaS product?")
        assert session.problem_raw == "Should I build a SaaS product?"
        assert session.stage == "0-1"
        assert session.session_id is not None
        assert session.current_stage == "problem_definition"

    def test_create_with_stage(self):
        session = create_session("Scaling issue", stage="10-100")
        assert session.stage == "10-100"


class TestSlugify:
    def test_basic(self):
        assert _slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert _slugify("Should I build a SaaS?") == "should-i-build-a-saas"

    def test_truncation(self):
        long = "a" * 100
        slug = _slugify(long)
        assert len(slug) <= 60


class TestSessionSerialization:
    def test_round_trip(self):
        session = create_session("Test problem")
        session.problem_refined = "Refined test problem"
        session.agent_outputs = {"Historian": "History says...", "Falsification": "Breaks at..."}
        session.agent_order = ["Historian", "Falsification"]

        data = session.to_dict()
        restored = Session.from_dict(data)

        assert restored.problem_raw == session.problem_raw
        assert restored.problem_refined == session.problem_refined
        assert restored.agent_outputs == session.agent_outputs
        assert restored.agent_order == session.agent_order


class TestSessionSaveLoad:
    def test_save_and_load(self, tmp_path):
        session = create_session("Should I pivot?")
        session.problem_refined = "Is there evidence that pivoting to B2B will yield better unit economics within 12 months?"
        session.falsifiability_test = "Fails if CAC exceeds $500 in first quarter"
        session.hidden_assumptions = ["Current market is saturated", "Team can execute B2B"]
        session.agent_outputs = {
            "Historian": "History shows pivots succeed 30% of the time...",
            "First Principles": "From first principles, the value chain suggests...",
        }
        session.agent_order = ["Historian", "First Principles"]
        session.crucible_output = "The tension between Historian and First Principles reveals..."

        # Save
        saved_path = save_session(session, str(tmp_path))
        assert Path(saved_path).exists()

        # Check markdown content
        content = Path(saved_path).read_text()
        assert "Problem Definition" in content
        assert "Refined statement" in content
        assert "Historian" in content
        assert "Crucible Synthesis" in content

        # Check state file
        state_path = saved_path.replace(".md", ".state.json")
        assert Path(state_path).exists()

        # Load
        loaded = load_session(state_path)
        assert loaded.problem_refined == session.problem_refined
        assert loaded.agent_outputs == session.agent_outputs

    def test_save_with_conviction(self, tmp_path):
        session = create_session("Should I hire?")
        session.problem_refined = "Hire a senior engineer?"
        session.mode_switched = True
        session.external_signal = "Customer called asking for feature"
        session.conviction_output = "DECISION: Hire. Confidence: HIGH."

        saved_path = save_session(session, str(tmp_path))

        # Check private file exists
        private_path = saved_path.replace(".md", ".private.md")
        assert Path(private_path).exists()

        private_content = Path(private_path).read_text()
        assert "PRIVATE" in private_content
        assert "DECISION: Hire" in private_content

        # Main file should NOT have conviction output
        main_content = Path(saved_path).read_text()
        assert "DECISION: Hire" not in main_content
