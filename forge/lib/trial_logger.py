"""
Trial Logger — The Forge's debug and audit trail system.

Every Forge session produces a trial log that captures:
- Every LLM API call (provider, model, tokens, latency, truncated I/O)
- Every stage transition
- Every decision point
- Errors and retries
- Timing data

The trial log is separate from the session output. The session is the
deliberation product. The trial log is the engineering artifact that tells
you what went wrong (or right) mechanically.

Output: forge/logs/YYYY-MM-DD-HH-MM-SS-<session-id>-trial.jsonl
Each line is a JSON object — easy to grep, parse, or feed into analysis.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class TrialLogger:
    """Append-only JSONL logger for Forge session diagnostics."""

    def __init__(self, session_id: str, log_dir: Optional[str] = None):
        self.session_id = session_id
        self.start_time = time.time()
        self._entries: list[dict[str, Any]] = []

        if log_dir is None:
            log_dir = str(Path(__file__).parent.parent / "logs")

        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.log_path = os.path.join(
            log_dir, f"{timestamp}-{session_id}-trial.jsonl"
        )

        # Write header entry
        self._write_entry({
            "event": "session_start",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
        })

    def _write_entry(self, entry: dict[str, Any]):
        """Write a single log entry to the JSONL file."""
        entry["_elapsed_total"] = round(time.time() - self.start_time, 3)
        self._entries.append(entry)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str, ensure_ascii=False) + "\n")

    # ----- API call logging -----

    def log_api_call_start(
        self,
        provider: str,
        model: str,
        system_prompt_preview: str,
        user_message_preview: str,
    ):
        self._write_entry({
            "event": "api_call_start",
            "provider": provider,
            "model": model,
            "system_prompt_preview": system_prompt_preview,
            "user_message_preview": user_message_preview,
        })

    def log_api_call_end(
        self,
        provider: str,
        model: str,
        elapsed_seconds: float,
        input_tokens: int,
        output_tokens: int,
        response_preview: str,
        success: bool,
        error: Optional[str] = None,
    ):
        self._write_entry({
            "event": "api_call_end",
            "provider": provider,
            "model": model,
            "elapsed_seconds": round(elapsed_seconds, 3),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "response_preview": response_preview,
            "success": success,
            "error": error,
        })

    # ----- Stage logging -----

    def log_stage_start(self, stage: str, metadata: Optional[dict] = None):
        self._write_entry({
            "event": "stage_start",
            "stage": stage,
            **(metadata or {}),
        })

    def log_stage_end(self, stage: str, outcome: str, metadata: Optional[dict] = None):
        self._write_entry({
            "event": "stage_end",
            "stage": stage,
            "outcome": outcome,
            **(metadata or {}),
        })

    # ----- Agent logging -----

    def log_agent_start(self, agent_name: str, order_position: int, total_agents: int):
        self._write_entry({
            "event": "agent_start",
            "agent_name": agent_name,
            "order_position": order_position,
            "total_agents": total_agents,
        })

    def log_agent_end(self, agent_name: str, output_length: int):
        self._write_entry({
            "event": "agent_end",
            "agent_name": agent_name,
            "output_length": output_length,
        })

    # ----- Decision logging -----

    def log_decision(self, decision_type: str, value: str, reason: Optional[str] = None):
        """Log any human or system decision point."""
        self._write_entry({
            "event": "decision",
            "decision_type": decision_type,
            "value": value,
            "reason": reason,
        })

    # ----- Error logging -----

    def log_error(self, stage: str, error: str, recoverable: bool = True):
        self._write_entry({
            "event": "error",
            "stage": stage,
            "error": error,
            "recoverable": recoverable,
        })

    # ----- Session end -----

    def log_session_end(self, outcome: str, metadata: Optional[dict] = None):
        self._write_entry({
            "event": "session_end",
            "session_id": self.session_id,
            "outcome": outcome,
            "total_elapsed_seconds": round(time.time() - self.start_time, 3),
            "total_entries": len(self._entries) + 1,  # +1 for this entry
            **(metadata or {}),
        })

    # ----- Summary -----

    def get_summary(self) -> dict[str, Any]:
        """Return a summary of the trial log for quick review."""
        api_calls = [e for e in self._entries if e["event"] == "api_call_end"]
        errors = [e for e in self._entries if e["event"] == "error"]
        stages = [e for e in self._entries if e["event"] == "stage_end"]

        total_input_tokens = sum(e.get("input_tokens", 0) for e in api_calls)
        total_output_tokens = sum(e.get("output_tokens", 0) for e in api_calls)
        total_api_time = sum(e.get("elapsed_seconds", 0) for e in api_calls)

        return {
            "session_id": self.session_id,
            "total_elapsed": round(time.time() - self.start_time, 3),
            "api_calls": len(api_calls),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "total_api_time": round(total_api_time, 3),
            "errors": len(errors),
            "stages_completed": len(stages),
            "log_path": self.log_path,
        }
