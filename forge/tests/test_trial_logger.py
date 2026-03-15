"""Tests for the trial logger."""

import json
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from forge.lib.trial_logger import TrialLogger


class TestTrialLogger:
    def test_creates_log_file(self, tmp_path):
        logger = TrialLogger("test-session", str(tmp_path))
        assert Path(logger.log_path).exists()

    def test_logs_api_calls(self, tmp_path):
        logger = TrialLogger("test-session", str(tmp_path))
        logger.log_api_call_start("anthropic", "claude-opus-4-6", "sys...", "user...")
        logger.log_api_call_end("anthropic", "claude-opus-4-6", 1.5, 100, 200, "response...", True)

        with open(logger.log_path) as f:
            entries = [json.loads(line) for line in f]

        api_starts = [e for e in entries if e["event"] == "api_call_start"]
        api_ends = [e for e in entries if e["event"] == "api_call_end"]
        assert len(api_starts) == 1
        assert len(api_ends) == 1
        assert api_ends[0]["input_tokens"] == 100
        assert api_ends[0]["output_tokens"] == 200

    def test_logs_stages(self, tmp_path):
        logger = TrialLogger("test-session", str(tmp_path))
        logger.log_stage_start("parliament", {"agent_count": 3})
        logger.log_stage_end("parliament", "3/3 completed")

        with open(logger.log_path) as f:
            entries = [json.loads(line) for line in f]

        stage_starts = [e for e in entries if e["event"] == "stage_start"]
        assert len(stage_starts) == 1
        assert stage_starts[0]["agent_count"] == 3

    def test_summary(self, tmp_path):
        logger = TrialLogger("test-session", str(tmp_path))
        logger.log_api_call_start("mock", "mock", "s", "u")
        logger.log_api_call_end("mock", "mock", 0.5, 50, 100, "r", True)
        logger.log_api_call_start("mock", "mock", "s", "u")
        logger.log_api_call_end("mock", "mock", 0.3, 30, 60, "r", True)

        summary = logger.get_summary()
        assert summary["api_calls"] == 2
        assert summary["total_input_tokens"] == 80
        assert summary["total_output_tokens"] == 160
        assert summary["errors"] == 0

    def test_error_logging(self, tmp_path):
        logger = TrialLogger("test-session", str(tmp_path))
        logger.log_error("parliament", "Agent failed: timeout", recoverable=True)

        summary = logger.get_summary()
        assert summary["errors"] == 1

    def test_elapsed_tracking(self, tmp_path):
        logger = TrialLogger("test-session", str(tmp_path))

        with open(logger.log_path) as f:
            first_entry = json.loads(f.readline())

        assert "_elapsed_total" in first_entry
        assert first_entry["_elapsed_total"] >= 0
