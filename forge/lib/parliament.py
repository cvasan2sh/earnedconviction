"""
Parliament Orchestrator — runs agents sequentially, randomised order, blind outputs.

Each agent sees ONLY the problem statement (+ forced inversion if applicable).
No agent sees another agent's output. The Crucible sees everything — but that's
handled in Stage 2, not here.

This is where the Cascade Contamination risk is mitigated.
"""

from __future__ import annotations

import random
from typing import Optional, Callable

from forge.agents.schema import AgentDefinition
from forge.lib.providers import ModelConfig, call_llm
from forge.lib.session import Session
from forge.lib.trial_logger import TrialLogger


def run_parliament(
    session: Session,
    agents: list[AgentDefinition],
    trial_logger: Optional[TrialLogger] = None,
    on_agent_complete: Optional[Callable[[str, str, int, int], None]] = None,
    interactive: bool = False,
) -> Session:
    """
    Run the agent parliament on a session.

    Args:
        session: The session with a refined problem statement
        agents: List of agents to run (permanents + contextual, no Crucible)
        trial_logger: Optional trial logger for diagnostics
        on_agent_complete: Optional callback(agent_name, output, position, total)
            called after each agent finishes — used for real-time display
        interactive: If True, the callback should pause for user input

    Returns:
        Updated session with agent_outputs and agent_order populated
    """
    # Randomise agent order — core mitigation for anchoring bias
    agents_shuffled = list(agents)
    random.shuffle(agents_shuffled)

    order = [a.name for a in agents_shuffled]
    session.agent_order = order

    if trial_logger:
        trial_logger.log_stage_start(
            "parliament",
            metadata={
                "agent_count": len(agents_shuffled),
                "agent_order": order,
                "problem_length": len(session.problem_refined or session.problem_raw),
            },
        )

    # Build the problem context each agent will see
    problem_context = _build_problem_context(session)

    # Run each agent — sequential, blind
    for i, agent in enumerate(agents_shuffled):
        agent_name = agent.name
        position = i + 1
        total = len(agents_shuffled)

        if trial_logger:
            trial_logger.log_agent_start(agent_name, position, total)

        try:
            output = call_llm(
                system_prompt=agent.system_prompt,
                user_message=problem_context,
                model_config=agent.get_model_config(),
                trial_logger=trial_logger,
            )

            session.agent_outputs[agent_name] = output

            if trial_logger:
                trial_logger.log_agent_end(agent_name, len(output))

            if on_agent_complete:
                on_agent_complete(agent_name, output, position, total)

        except Exception as e:
            error_msg = f"[AGENT ERROR: {agent_name}] {str(e)}"
            session.agent_outputs[agent_name] = error_msg

            if trial_logger:
                trial_logger.log_error(
                    stage="parliament",
                    error=f"Agent {agent_name} failed: {str(e)}",
                    recoverable=True,
                )
                trial_logger.log_agent_end(agent_name, len(error_msg))

    if trial_logger:
        successful = sum(
            1 for v in session.agent_outputs.values()
            if not v.startswith("[AGENT ERROR")
        )
        trial_logger.log_stage_end(
            "parliament",
            outcome=f"{successful}/{len(agents_shuffled)} agents completed",
            metadata={"successful_agents": successful},
        )

    return session


def _build_problem_context(session: Session) -> str:
    """
    Build the problem context that agents will see.

    Includes:
    - Refined problem statement (or raw if not yet refined)
    - Forced inversion output (if available)
    - Problem stage
    - Falsifiability test
    """
    parts = []

    # Problem statement
    problem = session.problem_refined or session.problem_raw
    parts.append(f"## Problem Statement\n\n{problem}")

    # Stage
    parts.append(f"\n\n**Problem Stage:** {session.stage}")

    # Falsifiability test
    if session.falsifiability_test:
        parts.append(f"\n\n**Falsifiability Test:** {session.falsifiability_test}")

    # Hidden assumptions
    if session.hidden_assumptions:
        assumptions = "\n".join(f"- {a}" for a in session.hidden_assumptions)
        parts.append(f"\n\n**Hidden Assumptions Identified:**\n{assumptions}")

    # Forced Inversion (if available)
    if session.inversion_output:
        parts.append(
            f"\n\n---\n\n## Forced Inversion\n"
            f"*The following is a deliberate inversion of the problem — "
            f"a counterintuitive reframing designed to prevent legibility creep. "
            f"Consider it alongside the original problem.*\n\n"
            f"{session.inversion_output}"
        )

    return "\n".join(parts)
