"""
Stage 2 — Crucible Synthesis

Receives ALL agent outputs simultaneously. Does not summarise. Does not average.
Maps tensions, finds convergence, produces ranked conviction output with confidence
levels, and explicitly surfaces its own bias.
"""

from __future__ import annotations

from typing import Optional

from forge.agents.registry import create_agent
from forge.lib.providers import ModelConfig, call_llm
from forge.lib.session import Session
from forge.lib.trial_logger import TrialLogger


def run_crucible(
    session: Session,
    trial_logger: Optional[TrialLogger] = None,
    model_config: Optional[ModelConfig] = None,
) -> Session:
    """
    Run the Crucible synthesis on a session with completed parliament outputs.

    Args:
        session: Session with agent_outputs populated from Stage 1
        trial_logger: Optional diagnostics logger
        model_config: Optional model override for the Crucible

    Returns:
        Updated session with crucible_output populated
    """
    if not session.agent_outputs:
        raise ValueError("Cannot run Crucible — no agent outputs in session")

    agent = create_agent("crucible", model_config)

    if trial_logger:
        trial_logger.log_stage_start("crucible", metadata={
            "agent_count": len(session.agent_outputs),
            "agents": list(session.agent_outputs.keys()),
        })

    # Build the Crucible's input — problem + ALL agent outputs
    crucible_input = _build_crucible_input(session)

    try:
        output = call_llm(
            system_prompt=agent.system_prompt,
            user_message=crucible_input,
            model_config=agent.get_model_config(),
            trial_logger=trial_logger,
        )

        session.crucible_output = output
        session.current_stage = "crucible_complete"

        if trial_logger:
            trial_logger.log_stage_end(
                "crucible",
                outcome="completed",
                metadata={"output_length": len(output)},
            )

    except Exception as e:
        if trial_logger:
            trial_logger.log_error(
                stage="crucible",
                error=str(e),
                recoverable=False,
            )
            trial_logger.log_stage_end("crucible", outcome="failed")
        raise

    return session


def _build_crucible_input(session: Session) -> str:
    """
    Build the input that the Crucible receives.

    This includes:
    - The problem statement (refined)
    - The forced inversion (if exists)
    - ALL agent outputs, clearly labeled
    - Problem stage and metadata
    """
    parts = []

    # Problem
    problem = session.problem_refined or session.problem_raw
    parts.append(f"## Problem Statement\n\n{problem}")

    if session.falsifiability_test:
        parts.append(f"\n**Falsifiability Test:** {session.falsifiability_test}")

    if session.hidden_assumptions:
        assumptions = "\n".join(f"- {a}" for a in session.hidden_assumptions)
        parts.append(f"\n**Hidden Assumptions:**\n{assumptions}")

    parts.append(f"\n**Problem Stage:** {session.stage}")

    # Forced Inversion
    if session.inversion_output:
        parts.append(f"\n\n---\n\n## Forced Inversion Output\n\n{session.inversion_output}")

    # Agent outputs — presented in execution order
    parts.append("\n\n---\n\n## Agent Parliament Outputs")
    parts.append(f"\n*{len(session.agent_outputs)} agents deliberated in the following order: {', '.join(session.agent_order)}*")
    parts.append("*Each agent worked independently and could not see any other agent's output.*\n")

    for agent_name in session.agent_order:
        if agent_name in session.agent_outputs:
            output = session.agent_outputs[agent_name]
            parts.append(f"\n### {agent_name} Agent\n\n{output}")

    return "\n".join(parts)
