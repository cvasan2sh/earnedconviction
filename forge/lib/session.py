"""
Session Manager — The Forge's state backbone.

A session tracks the full lifecycle of a Forge deliberation:
problem → definition → inversion → parliament → crucible → (mode switch) → conviction → decision.

Sessions are saved as markdown files in forge-sessions/YYYY-MM/.
Conviction output goes to a separate .private.md file.
"""

from __future__ import annotations

import os
import re
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Any
from pathlib import Path


@dataclass
class Session:
    """
    A Forge deliberation session.

    This is the mutable state object that flows through all stages.
    """

    # Identity
    session_id: str
    created_at: str  # ISO format
    problem_raw: str  # Original problem from user

    # Stage 0 output
    problem_refined: Optional[str] = None
    falsifiability_test: Optional[str] = None
    hidden_assumptions: Optional[list[str]] = None
    definition_iterations: int = 0

    # Stage config
    stage: str = "0-1"  # "0-1", "1-10", "10-100"
    contextual_agents: list[str] = field(default_factory=list)

    # Forced Inversion output (intake)
    inversion_output: Optional[str] = None

    # Parliament outputs — agent_name -> output text
    agent_outputs: dict[str, str] = field(default_factory=dict)
    agent_order: list[str] = field(default_factory=list)  # Execution order (randomised)

    # Crucible output
    crucible_output: Optional[str] = None

    # Mode switch
    mode_switched: bool = False
    external_signal: Optional[str] = None
    mode_switch_time: Optional[str] = None

    # Conviction output (private)
    conviction_output: Optional[str] = None

    # Human Clock
    human_decided: Optional[bool] = None
    decision_time: Optional[str] = None

    # Current stage tracker
    current_stage: str = "problem_definition"  # tracks where we are in the pipeline

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "problem_raw": self.problem_raw,
            "problem_refined": self.problem_refined,
            "falsifiability_test": self.falsifiability_test,
            "hidden_assumptions": self.hidden_assumptions,
            "definition_iterations": self.definition_iterations,
            "stage": self.stage,
            "contextual_agents": self.contextual_agents,
            "inversion_output": self.inversion_output,
            "agent_outputs": self.agent_outputs,
            "agent_order": self.agent_order,
            "crucible_output": self.crucible_output,
            "mode_switched": self.mode_switched,
            "external_signal": self.external_signal,
            "mode_switch_time": self.mode_switch_time,
            "conviction_output": self.conviction_output,
            "human_decided": self.human_decided,
            "decision_time": self.decision_time,
            "current_stage": self.current_stage,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Session":
        """Deserialize from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


def create_session(problem: str, stage: str = "0-1") -> Session:
    """Create a new Forge session."""
    now = datetime.now()
    session_id = now.strftime("%Y%m%d-%H%M%S")

    return Session(
        session_id=session_id,
        created_at=now.isoformat(),
        problem_raw=problem,
        stage=stage,
    )


def _slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:60].rstrip('-')


def get_session_dir(session: Session, base_dir: str | None = None) -> str:
    """Get the directory for a session's output files."""
    if base_dir is None:
        base_dir = str(Path(__file__).parent.parent.parent / "forge-sessions")

    month = datetime.fromisoformat(session.created_at).strftime("%Y-%m")
    session_dir = os.path.join(base_dir, month)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir


def _get_session_filename(session: Session) -> str:
    """Generate the filename for a session."""
    date = datetime.fromisoformat(session.created_at).strftime("%Y-%m-%d")
    slug = _slugify(session.problem_raw[:80])
    return f"{date}-{slug}"


def save_session(session: Session, base_dir: str | None = None) -> str:
    """
    Save session to markdown file. Returns the file path.

    Exploration output → main file
    Conviction output → separate .private.md file
    """
    session_dir = get_session_dir(session, base_dir)
    filename = _get_session_filename(session)

    # Main exploration file
    main_path = os.path.join(session_dir, f"{filename}.md")
    main_content = _render_exploration_markdown(session)
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(main_content)

    # Private conviction file (only if conviction output exists)
    if session.conviction_output:
        private_path = os.path.join(session_dir, f"{filename}.private.md")
        private_content = _render_conviction_markdown(session)
        with open(private_path, "w", encoding="utf-8") as f:
            f.write(private_content)

    # JSON state file (for resume capability)
    state_path = os.path.join(session_dir, f"{filename}.state.json")
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(session.to_dict(), f, indent=2, default=str, ensure_ascii=False)

    return main_path


def load_session(path: str) -> Session:
    """Load a session from its .state.json file."""
    # If given a .md path, try to find the .state.json
    if path.endswith(".md"):
        state_path = path.rsplit(".", 1)[0]
        if state_path.endswith(".private"):
            state_path = state_path.rsplit(".", 1)[0]
        state_path += ".state.json"
    else:
        state_path = path

    with open(state_path, encoding="utf-8") as f:
        data = json.load(f)

    return Session.from_dict(data)


def _render_exploration_markdown(session: Session) -> str:
    """Render the exploration (public) markdown output."""
    lines = []

    # Frontmatter
    lines.append("---")
    lines.append(f"date: {datetime.fromisoformat(session.created_at).strftime('%Y-%m-%d')}")
    lines.append(f"problem: {session.problem_refined or session.problem_raw}")
    lines.append(f"stage: {session.stage}")
    agents = list(session.agent_outputs.keys())
    lines.append(f"agents: [{', '.join(agents)}]")
    lines.append(f"status: {'refined' if session.crucible_output else 'raw'}")
    lines.append("---")
    lines.append("")

    # Problem Definition
    lines.append("## Problem Definition")
    lines.append("")
    if session.problem_refined:
        lines.append(f"**Raw input:** {session.problem_raw}")
        lines.append("")
        lines.append(f"**Refined statement:** {session.problem_refined}")
        lines.append("")
        if session.falsifiability_test:
            lines.append(f"**Falsifiability test:** {session.falsifiability_test}")
            lines.append("")
        if session.hidden_assumptions:
            lines.append("**Hidden assumptions:**")
            for assumption in session.hidden_assumptions:
                lines.append(f"- {assumption}")
            lines.append("")
    else:
        lines.append(session.problem_raw)
        lines.append("")

    # Forced Inversion (if exists)
    if session.inversion_output:
        lines.append("## Forced Inversion")
        lines.append("")
        lines.append(session.inversion_output)
        lines.append("")

    # Agent Outputs
    lines.append("## Agent Outputs")
    lines.append("")
    for agent_name in session.agent_order:
        if agent_name in session.agent_outputs:
            lines.append(f"### {agent_name} Agent")
            lines.append("")
            lines.append(session.agent_outputs[agent_name])
            lines.append("")

    # Crucible Synthesis
    if session.crucible_output:
        lines.append("## Crucible Synthesis")
        lines.append("")
        lines.append(session.crucible_output)
        lines.append("")

    return "\n".join(lines)


def _render_conviction_markdown(session: Session) -> str:
    """Render the conviction (private) markdown output."""
    lines = []

    lines.append("---")
    lines.append(f"date: {datetime.fromisoformat(session.created_at).strftime('%Y-%m-%d')}")
    lines.append(f"problem: {session.problem_refined or session.problem_raw}")
    lines.append("type: conviction (PRIVATE)")
    lines.append("---")
    lines.append("")

    lines.append("## PRIVATE — Conviction Output")
    lines.append("")
    lines.append("*This file contains private decision output. Do not publish.*")
    lines.append("")

    if session.external_signal:
        lines.append(f"**External signal:** {session.external_signal}")
        lines.append(f"**Mode switch time:** {session.mode_switch_time}")
        lines.append("")

    if session.conviction_output:
        lines.append(session.conviction_output)
        lines.append("")

    if session.human_decided is not None:
        lines.append("## Human Clock")
        lines.append("")
        lines.append(f"**Did you decide?** {'Yes' if session.human_decided else 'No'}")
        lines.append(f"**Decision time:** {session.decision_time}")
        lines.append("")

    return "\n".join(lines)
