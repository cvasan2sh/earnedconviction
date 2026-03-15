"""
Stage 0 — Problem Definition Loop

Takes a raw problem and iterates until it's dense, specific, and falsifiable.
The parliament does not activate until this stage produces a READY verdict.

This is an interactive stage — it loops with the user.
In non-interactive (batch) mode, it runs a single pass and assumes READY.
"""

from __future__ import annotations

import re
from typing import Optional, Callable

from forge.agents.registry import create_agent
from forge.lib.providers import ModelConfig, call_llm
from forge.lib.session import Session
from forge.lib.trial_logger import TrialLogger


def run_problem_definition(
    session: Session,
    trial_logger: Optional[TrialLogger] = None,
    get_user_input: Optional[Callable[[str], str]] = None,
    model_config: Optional[ModelConfig] = None,
    max_iterations: int = 5,
) -> Session:
    """
    Run the Problem Definition Loop.

    Args:
        session: Session with problem_raw set
        trial_logger: Optional diagnostics logger
        get_user_input: Callback to get user refinement. If None, runs single pass.
        model_config: Optional model override for the problem definition agent
        max_iterations: Max iterations before forcing READY

    Returns:
        Updated session with problem_refined, falsifiability_test, hidden_assumptions
    """
    agent = create_agent("problem_definition", model_config)

    if trial_logger:
        trial_logger.log_stage_start("problem_definition", metadata={
            "raw_problem": session.problem_raw[:200],
            "interactive": get_user_input is not None,
        })

    current_problem = session.problem_raw
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        session.definition_iterations = iteration

        # Call the Problem Definition agent
        output = call_llm(
            system_prompt=agent.system_prompt,
            user_message=f"Problem statement (iteration {iteration}):\n\n{current_problem}",
            model_config=agent.get_model_config(),
            trial_logger=trial_logger,
        )

        # Parse the output
        parsed = _parse_definition_output(output)

        # Update session with latest refinement
        if parsed.get("refined"):
            session.problem_refined = parsed["refined"]
        if parsed.get("falsifiability"):
            session.falsifiability_test = parsed["falsifiability"]
        if parsed.get("assumptions"):
            session.hidden_assumptions = parsed["assumptions"]

        # Check verdict
        is_ready = parsed.get("verdict", "").upper().startswith("READY")

        if trial_logger:
            trial_logger.log_decision(
                decision_type="problem_definition_verdict",
                value="READY" if is_ready else "NOT READY",
                reason=f"Iteration {iteration}: {parsed.get('verdict', 'unknown')}",
            )

        if is_ready:
            break

        # If interactive, get user refinement
        if get_user_input:
            user_response = get_user_input(output)
            if user_response.strip().lower() in ("accept", "ready", "go", "proceed"):
                # User overrides and accepts current state
                if not session.problem_refined:
                    session.problem_refined = current_problem
                break
            elif user_response.strip():
                current_problem = user_response
        else:
            # Non-interactive: accept after single pass
            if not session.problem_refined:
                session.problem_refined = current_problem
            break

    # Ensure we always have a refined problem
    if not session.problem_refined:
        session.problem_refined = current_problem

    session.current_stage = "problem_definition_complete"

    if trial_logger:
        trial_logger.log_stage_end(
            "problem_definition",
            outcome=f"Completed in {iteration} iterations",
            metadata={
                "iterations": iteration,
                "refined_problem": session.problem_refined[:200],
                "has_falsifiability": session.falsifiability_test is not None,
            },
        )

    return session


def _parse_definition_output(output: str) -> dict:
    """
    Parse the Problem Definition agent's structured output.

    Extracts:
    - assessment
    - assumptions (list)
    - refined problem statement
    - falsifiability test
    - verdict (READY or NOT READY)
    """
    result = {}

    # Extract refined problem statement
    refined_match = re.search(
        r"###?\s*Refined Problem Statement\s*\n+(.*?)(?=\n###|\n## |$)",
        output,
        re.DOTALL,
    )
    if refined_match:
        result["refined"] = refined_match.group(1).strip()

    # Extract falsifiability test
    falsify_match = re.search(
        r"###?\s*Falsifiability Test\s*\n+(.*?)(?=\n###|\n## |$)",
        output,
        re.DOTALL,
    )
    if falsify_match:
        result["falsifiability"] = falsify_match.group(1).strip()

    # Extract hidden assumptions
    assumptions_match = re.search(
        r"###?\s*Hidden Assumptions\s*\n+(.*?)(?=\n###|\n## |$)",
        output,
        re.DOTALL,
    )
    if assumptions_match:
        raw = assumptions_match.group(1).strip()
        assumptions = []
        for line in raw.split("\n"):
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                assumptions.append(line[2:].strip())
            elif line.startswith("•"):
                assumptions.append(line[1:].strip())
            elif line and not line.startswith("#"):
                assumptions.append(line)
        result["assumptions"] = assumptions if assumptions else None

    # Extract verdict
    verdict_match = re.search(
        r"###?\s*Verdict\s*\n+(.*?)(?=\n###|\n## |$)",
        output,
        re.DOTALL,
    )
    if verdict_match:
        result["verdict"] = verdict_match.group(1).strip()

    return result
