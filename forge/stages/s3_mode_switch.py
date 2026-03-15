"""
Stage 3 — Mode Switch Trigger

External contact only — customer call, prototype reaction, market data.
Not a judgment call. Not a feeling. First genuine external signal flips
to conviction mode.

This stage is interactive — it waits for the human to report an external signal.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Callable

from forge.lib.session import Session
from forge.lib.trial_logger import TrialLogger


def run_mode_switch(
    session: Session,
    trial_logger: Optional[TrialLogger] = None,
    get_user_input: Optional[Callable[[str], str]] = None,
    external_signal: Optional[str] = None,
) -> Session:
    """
    Handle the mode switch from Exploration to Conviction.

    Args:
        session: Session with crucible_output populated
        trial_logger: Optional diagnostics logger
        get_user_input: Interactive callback — prompts user for external signal
        external_signal: Pre-supplied signal (for batch/resume mode)

    Returns:
        Updated session with mode_switched flag
    """
    if trial_logger:
        trial_logger.log_stage_start("mode_switch")

    signal = external_signal

    if signal is None and get_user_input:
        prompt = (
            "MODE SWITCH — The Forge needs external contact to proceed.\n\n"
            "What external signal has occurred? This must be real contact with "
            "reality — a customer call, prototype reaction, market data, user "
            "feedback, or other genuine external input.\n\n"
            "Describe the external signal (or type 'skip' to end the session "
            "in exploration mode):"
        )
        signal = get_user_input(prompt)

    if signal and signal.strip().lower() not in ("skip", "none", ""):
        session.mode_switched = True
        session.external_signal = signal.strip()
        session.mode_switch_time = datetime.now().isoformat()
        session.current_stage = "mode_switch_complete"

        if trial_logger:
            trial_logger.log_decision(
                decision_type="mode_switch",
                value="switched",
                reason=signal.strip()[:200],
            )
            trial_logger.log_stage_end("mode_switch", outcome="switched to conviction")
    else:
        session.current_stage = "exploration_final"

        if trial_logger:
            trial_logger.log_decision(
                decision_type="mode_switch",
                value="skipped",
                reason="User chose to remain in exploration mode",
            )
            trial_logger.log_stage_end("mode_switch", outcome="skipped — staying in exploration")

    return session
