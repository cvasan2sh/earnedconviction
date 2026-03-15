"""
Stage 1 — Exploration Mode

Runs the Forced Inversion (intake) and then the full parliament.
Dynamic agent parliament. Sequential, randomised order, blind outputs.
"""

from __future__ import annotations

from typing import Optional, Callable

from forge.agents.registry import create_agent, get_parliament
from forge.lib.providers import ModelConfig, call_llm
from forge.lib.parliament import run_parliament
from forge.lib.session import Session
from forge.lib.trial_logger import TrialLogger


def run_forced_inversion(
    session: Session,
    trial_logger: Optional[TrialLogger] = None,
    model_config: Optional[ModelConfig] = None,
) -> Session:
    """
    Run the Forced Inversion agent (intake only, before parliament).

    Takes the refined problem and generates the counterintuitive version.
    """
    agent = create_agent("forced_inversion", model_config)

    if trial_logger:
        trial_logger.log_stage_start("forced_inversion")

    problem = session.problem_refined or session.problem_raw

    try:
        output = call_llm(
            system_prompt=agent.system_prompt,
            user_message=f"Problem to invert:\n\n{problem}",
            model_config=agent.get_model_config(),
            trial_logger=trial_logger,
        )
        session.inversion_output = output

        if trial_logger:
            trial_logger.log_stage_end(
                "forced_inversion",
                outcome="completed",
                metadata={"output_length": len(output)},
            )

    except Exception as e:
        if trial_logger:
            trial_logger.log_error(
                stage="forced_inversion",
                error=str(e),
                recoverable=True,
            )
            trial_logger.log_stage_end("forced_inversion", outcome="failed")
        # Non-fatal — parliament can proceed without inversion

    return session


def run_exploration(
    session: Session,
    trial_logger: Optional[TrialLogger] = None,
    model_overrides: Optional[dict[str, ModelConfig]] = None,
    on_agent_complete: Optional[Callable[[str, str, int, int], None]] = None,
    interactive: bool = False,
    skip_inversion: bool = False,
) -> Session:
    """
    Run full Stage 1 — Forced Inversion + Parliament.

    Args:
        session: Session with problem_refined set (from Stage 0)
        trial_logger: Optional diagnostics logger
        model_overrides: Optional per-agent model config overrides
        on_agent_complete: Callback after each agent finishes
        interactive: If True, pause after each agent
        skip_inversion: If True, skip the Forced Inversion step
    """
    if trial_logger:
        trial_logger.log_stage_start("exploration", metadata={
            "stage": session.stage,
            "skip_inversion": skip_inversion,
        })

    # Step 1: Forced Inversion (if applicable)
    if not skip_inversion and session.stage == "0-1":
        inversion_override = (model_overrides or {}).get("forced_inversion")
        session = run_forced_inversion(session, trial_logger, inversion_override)

    # Step 2: Assemble parliament
    agents = get_parliament(
        stage=session.stage,
        include_contextual=session.contextual_agents,
        model_overrides=model_overrides,
    )

    # Step 3: Run parliament
    session = run_parliament(
        session=session,
        agents=agents,
        trial_logger=trial_logger,
        on_agent_complete=on_agent_complete,
        interactive=interactive,
    )

    session.current_stage = "exploration_complete"

    if trial_logger:
        trial_logger.log_stage_end(
            "exploration",
            outcome=f"{len(session.agent_outputs)} agents completed",
        )

    return session
