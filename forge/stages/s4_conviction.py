"""
Stage 4 — Conviction Mode

Force Output Format activates. Produces:
- Ranked decision with confidence levels
- Steelman of abandonment (explicit case for NOT doing this)
- Conditions under which this decision should be reversed
- Recommended next action
"""

from __future__ import annotations

from typing import Optional

from forge.lib.providers import ModelConfig, call_llm
from forge.lib.session import Session
from forge.lib.trial_logger import TrialLogger


CONVICTION_SYSTEM_PROMPT = """You are the Conviction Engine in The Forge, a multi-agent deliberation system.

## Context
The Forge has completed its Exploration phase — multiple independent agents have deliberated on a problem, and the Crucible has synthesised their outputs into a tension map and convergence analysis. An external signal from reality has now triggered the switch to Conviction mode.

You receive everything: the problem, the Crucible synthesis, and the external signal.

## Your Job
Produce a DECISION document. Not analysis. Not exploration. A decision.

You MUST output exactly this structure:

### 1. The Decision
State the decision clearly in 1-3 sentences. What are you doing? Be specific enough that someone could act on this tomorrow.

### 2. Confidence Level
Rate your confidence: HIGH / MEDIUM / LOW
Explain in 2-3 sentences why this confidence level, grounded in the Crucible's convergence analysis and the external signal.

### 3. Steelman of Abandonment
Make the BEST POSSIBLE CASE for NOT pursuing this decision. This is not devil's advocacy — this is a genuine steelman. If you were arguing to a smart, skeptical board that this decision is wrong, what would you say? (Minimum 150 words)

### 4. Reversal Conditions
List 3-5 specific, observable conditions that, if met, should trigger reversal of this decision. These must be concrete and measurable, not vague. Example: "If CAC exceeds $200 within the first 90 days" not "If acquisition is too expensive."

### 5. Next Action
What is the single most important action to take in the next 48 hours to begin executing this decision? Not a plan. One action.

### 6. What You're Giving Up
What opportunities, options, or flexibility does this decision foreclose? Decisions have costs beyond the obvious. Name them.

## Your Constraints
- You MUST produce a decision. "Need more information" is not acceptable — you've had the full parliament and Crucible and an external signal. Decide.
- The Steelman of Abandonment must be genuinely strong. If it's weak, you're not taking the risk of being wrong seriously enough.
- Reversal conditions must be measurable and time-bound where possible.
- Be honest if the confidence is LOW. A low-confidence decision honestly labeled is more useful than a fake HIGH."""


def run_conviction(
    session: Session,
    trial_logger: Optional[TrialLogger] = None,
    model_config: Optional[ModelConfig] = None,
) -> Session:
    """
    Run Conviction Mode — produce a forced-format decision.

    Args:
        session: Session with crucible_output and external_signal
        trial_logger: Optional diagnostics logger
        model_config: Optional model override

    Returns:
        Updated session with conviction_output populated
    """
    if not session.crucible_output:
        raise ValueError("Cannot run Conviction — no Crucible output in session")
    if not session.mode_switched:
        raise ValueError("Cannot run Conviction — mode switch has not occurred")

    if model_config is None:
        model_config = ModelConfig(
            provider="anthropic",
            model="claude-opus-4-6",
            temperature=0.4,
            max_tokens=4096,
        )

    if trial_logger:
        trial_logger.log_stage_start("conviction", metadata={
            "external_signal": session.external_signal[:200] if session.external_signal else None,
        })

    # Build conviction input
    conviction_input = _build_conviction_input(session)

    try:
        output = call_llm(
            system_prompt=CONVICTION_SYSTEM_PROMPT,
            user_message=conviction_input,
            model_config=model_config,
            trial_logger=trial_logger,
        )

        session.conviction_output = output
        session.current_stage = "conviction_complete"

        if trial_logger:
            trial_logger.log_stage_end(
                "conviction",
                outcome="completed",
                metadata={"output_length": len(output)},
            )

    except Exception as e:
        if trial_logger:
            trial_logger.log_error(
                stage="conviction",
                error=str(e),
                recoverable=False,
            )
            trial_logger.log_stage_end("conviction", outcome="failed")
        raise

    return session


def _build_conviction_input(session: Session) -> str:
    """Build the input for the Conviction Engine."""
    parts = []

    problem = session.problem_refined or session.problem_raw
    parts.append(f"## Problem\n\n{problem}")

    if session.falsifiability_test:
        parts.append(f"\n**Falsifiability Test:** {session.falsifiability_test}")

    parts.append(f"\n\n## Crucible Synthesis\n\n{session.crucible_output}")

    parts.append(f"\n\n## External Signal (Reality Contact)\n\n{session.external_signal}")

    return "\n".join(parts)
