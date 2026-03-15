"""
Stage 5 — Human Clock

Simple, brutal prompt: "Did you decide?"

Not what the Forge produced. Not whether the analysis was good.
Just — did you decide.

Exists entirely outside the system's epistemology.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Callable

from forge.lib.session import Session
from forge.lib.trial_logger import TrialLogger


def run_human_clock(
    session: Session,
    trial_logger: Optional[TrialLogger] = None,
    get_user_input: Optional[Callable[[str], str]] = None,
    decided: Optional[bool] = None,
) -> Session:
    """
    The Human Clock — one question, one answer.

    Args:
        session: Session with conviction_output populated
        trial_logger: Optional diagnostics logger
        get_user_input: Interactive callback
        decided: Pre-supplied answer (for batch mode)

    Returns:
        Updated session with human_decided flag
    """
    if trial_logger:
        trial_logger.log_stage_start("human_clock")

    answer = decided

    if answer is None and get_user_input:
        response = get_user_input(
            "\n\nHUMAN CLOCK\n\n"
            "One question. One answer.\n\n"
            "Did you decide? (yes/no)"
        )
        answer = response.strip().lower() in ("yes", "y", "decided", "done")

    session.human_decided = answer
    session.decision_time = datetime.now().isoformat()
    session.current_stage = "complete"

    if trial_logger:
        trial_logger.log_decision(
            decision_type="human_clock",
            value="decided" if answer else "not decided",
        )
        trial_logger.log_stage_end(
            "human_clock",
            outcome="decided" if answer else "not decided",
        )

    return session
