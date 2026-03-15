#!/usr/bin/env python3
"""
The Forge — Multi-agent deliberation system.
CLI entry point.

Usage:
    python -m forge.run "Your problem statement here"
    python -m forge.run --interactive "Your problem statement here"
    python -m forge.run --resume path/to/session.state.json
    python -m forge.run --dry-run "Test problem"
    python -m forge.run --list-agents
"""

from __future__ import annotations

import sys
import os
import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

# Ensure forge package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from forge.lib.config import (
    load_env,
    get_model_overrides_from_env,
    use_mock_provider,
    get_forge_sessions_dir,
)
from forge.lib.providers import check_providers, ModelConfig
from forge.lib.session import create_session, save_session, load_session, Session
from forge.lib.trial_logger import TrialLogger
from forge.agents.registry import list_all_agents, get_parliament, create_agent
from forge.stages.s0_problem_definition import run_problem_definition
from forge.stages.s1_exploration import run_exploration
from forge.stages.s2_crucible import run_crucible
from forge.stages.s3_mode_switch import run_mode_switch
from forge.stages.s4_conviction import run_conviction
from forge.stages.s5_human_clock import run_human_clock


app = typer.Typer(
    name="forge",
    help="The Forge — Multi-agent deliberation system",
    add_completion=False,
)
console = Console()


def _display_agent_output(agent_name: str, output: str, position: int, total: int):
    """Callback to display agent output in the terminal."""
    console.print()
    console.print(Panel(
        Markdown(output),
        title=f"[bold]{agent_name} Agent[/bold] ({position}/{total})",
        border_style="red",
        padding=(1, 2),
    ))


def _get_interactive_input(prompt: str) -> str:
    """Get input from the user in interactive mode."""
    console.print()
    console.print(Panel(prompt, border_style="yellow", title="[bold]Input Required[/bold]"))
    return input("\n> ").strip()


def _run_full_pipeline(
    session: Session,
    trial_logger: TrialLogger,
    interactive: bool = False,
    model_overrides: Optional[dict[str, ModelConfig]] = None,
) -> Session:
    """Run the full Forge pipeline on a session."""

    get_input = _get_interactive_input if interactive else None

    # ── Stage 0: Problem Definition ──
    console.print("\n[bold red]═══ STAGE 0: PROBLEM DEFINITION ═══[/bold red]\n")
    session = run_problem_definition(
        session=session,
        trial_logger=trial_logger,
        get_user_input=get_input,
        model_config=(model_overrides or {}).get("problem_definition"),
    )
    console.print(f"\n[green]✓ Problem refined:[/green] {session.problem_refined}")
    if session.falsifiability_test:
        console.print(f"[green]✓ Falsifiability:[/green] {session.falsifiability_test}")

    # Save checkpoint
    save_session(session)

    # ── Stage 1: Exploration ──
    console.print("\n[bold red]═══ STAGE 1: EXPLORATION ═══[/bold red]\n")

    agents = get_parliament(
        stage=session.stage,
        include_contextual=session.contextual_agents,
        model_overrides=model_overrides,
    )
    agent_names = [a.name for a in agents]
    console.print(f"Parliament assembled: {', '.join(agent_names)}")
    console.print(f"Order will be randomised.\n")

    session = run_exploration(
        session=session,
        trial_logger=trial_logger,
        model_overrides=model_overrides,
        on_agent_complete=_display_agent_output,
        interactive=interactive,
    )

    # Save checkpoint
    save_session(session)

    # ── Stage 2: Crucible ──
    console.print("\n[bold red]═══ STAGE 2: CRUCIBLE SYNTHESIS ═══[/bold red]\n")

    session = run_crucible(
        session=session,
        trial_logger=trial_logger,
        model_config=(model_overrides or {}).get("crucible"),
    )

    console.print(Panel(
        Markdown(session.crucible_output),
        title="[bold]CRUCIBLE SYNTHESIS[/bold]",
        border_style="red",
        padding=(1, 2),
    ))

    # Save checkpoint
    save_session(session)

    # ── Stage 3: Mode Switch ──
    console.print("\n[bold red]═══ STAGE 3: MODE SWITCH ═══[/bold red]\n")

    session = run_mode_switch(
        session=session,
        trial_logger=trial_logger,
        get_user_input=get_input,
    )

    if not session.mode_switched:
        console.print("[yellow]Session ending in exploration mode.[/yellow]")
        save_session(session)
        return session

    # ── Stage 4: Conviction ──
    console.print("\n[bold red]═══ STAGE 4: CONVICTION ═══[/bold red]\n")

    session = run_conviction(
        session=session,
        trial_logger=trial_logger,
        model_config=(model_overrides or {}).get("conviction"),
    )

    console.print(Panel(
        Markdown(session.conviction_output),
        title="[bold]CONVICTION OUTPUT (PRIVATE)[/bold]",
        border_style="bright_red",
        padding=(1, 2),
    ))

    # Save checkpoint
    save_session(session)

    # ── Stage 5: Human Clock ──
    console.print("\n[bold red]═══ STAGE 5: HUMAN CLOCK ═══[/bold red]\n")

    session = run_human_clock(
        session=session,
        trial_logger=trial_logger,
        get_user_input=get_input,
    )

    save_session(session)
    return session


@app.command()
def deliberate(
    problem: Optional[str] = typer.Argument(None, help="The problem to deliberate on (short statements)"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to a .txt or .md file containing the problem statement"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Pause after each agent for review"),
    stage: str = typer.Option("0-1", "--stage", "-s", help="Problem stage: 0-1, 1-10, or 10-100"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Use mock provider — no API calls"),
    resume: Optional[str] = typer.Option(None, "--resume", "-r", help="Resume from a saved session (.state.json or .md)"),
    include_agents: Optional[str] = typer.Option(None, "--agents", "-a", help="Comma-separated contextual agents to include"),
    list_agents_flag: bool = typer.Option(False, "--list-agents", help="List all available agents and exit"),
    exploration_only: bool = typer.Option(False, "--explore", help="Run exploration mode only (stages 0-2), skip conviction"),
):
    """
    Run a Forge deliberation session.
    """
    env_loaded = load_env()
    if env_loaded:
        console.print(f"[dim]Loaded env from: {env_loaded}[/dim]")
    else:
        console.print("[dim]No .env file found[/dim]")

    # List agents mode
    if list_agents_flag:
        _list_agents()
        return

    # Resolve problem source: --file, --resume, or inline argument
    if resume:
        session = load_session(resume)
        console.print(f"[green]Resumed session:[/green] {session.session_id}")
        console.print(f"[green]Current stage:[/green] {session.current_stage}")
        console.print(f"[green]Problem:[/green] {session.problem_refined or session.problem_raw}")
    elif file:
        file_path = Path(file)
        if not file_path.exists():
            console.print(f"[red]Error: File not found: {file}[/red]")
            raise typer.Exit(1)
        problem_text = file_path.read_text(encoding="utf-8").strip()
        if not problem_text:
            console.print(f"[red]Error: File is empty: {file}[/red]")
            raise typer.Exit(1)
        console.print(f"[green]Loaded problem from:[/green] {file} ({len(problem_text)} chars)")
        session = create_session(problem_text, stage=stage)
    elif problem:
        session = create_session(problem, stage=stage)
    else:
        console.print("[red]Error: Provide a problem statement, use --file, or use --resume[/red]")
        raise typer.Exit(1)

    # Parse contextual agents
    if include_agents:
        session.contextual_agents = [a.strip() for a in include_agents.split(",")]

    # Model overrides
    if dry_run:
        model_overrides = use_mock_provider()
        console.print("[yellow]DRY RUN — using mock provider, no API calls[/yellow]\n")
    else:
        model_overrides = get_model_overrides_from_env()
        # Check providers
        available = check_providers()
        available_names = [k for k, v in available.items() if v]
        if not available_names and not dry_run:
            console.print("[red]No API keys configured. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.[/red]")
            console.print("[yellow]Tip: Use --dry-run to test with mock responses.[/yellow]")
            raise typer.Exit(1)
        console.print(f"[green]Available providers:[/green] {', '.join(available_names)}")

    # Create trial logger
    trial_logger = TrialLogger(session.session_id)
    console.print(f"[dim]Trial log: {trial_logger.log_path}[/dim]\n")

    # Header
    console.print(Panel(
        f"[bold]Problem:[/bold] {session.problem_raw}\n"
        f"[bold]Stage:[/bold] {session.stage}\n"
        f"[bold]Session:[/bold] {session.session_id}\n"
        f"[bold]Mode:[/bold] {'Interactive' if interactive else 'Batch'}",
        title="[bold red]THE FORGE[/bold red]",
        border_style="red",
    ))

    try:
        if exploration_only:
            # Run stages 0-2 only
            get_input = _get_interactive_input if interactive else None

            console.print("\n[bold red]═══ STAGE 0: PROBLEM DEFINITION ═══[/bold red]\n")
            session = run_problem_definition(session, trial_logger, get_input,
                                             (model_overrides or {}).get("problem_definition"))
            console.print(f"\n[green]✓ Problem refined:[/green] {session.problem_refined}")
            save_session(session)

            console.print("\n[bold red]═══ STAGE 1: EXPLORATION ═══[/bold red]\n")
            session = run_exploration(session, trial_logger, model_overrides,
                                     _display_agent_output, interactive)
            save_session(session)

            console.print("\n[bold red]═══ STAGE 2: CRUCIBLE SYNTHESIS ═══[/bold red]\n")
            session = run_crucible(session, trial_logger,
                                   (model_overrides or {}).get("crucible"))
            console.print(Panel(Markdown(session.crucible_output),
                                title="[bold]CRUCIBLE SYNTHESIS[/bold]",
                                border_style="red", padding=(1, 2)))
            save_session(session)
        else:
            session = _run_full_pipeline(session, trial_logger, interactive, model_overrides)

    except KeyboardInterrupt:
        console.print("\n[yellow]Session interrupted. Saving...[/yellow]")
        save_session(session)
        trial_logger.log_session_end("interrupted")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        trial_logger.log_error("pipeline", str(e), recoverable=False)
        save_session(session)
        trial_logger.log_session_end("error", metadata={"error": str(e)})
        raise

    # Session complete
    session_path = save_session(session)
    summary = trial_logger.get_summary()
    trial_logger.log_session_end("complete", metadata=summary)

    console.print("\n")
    console.print(Panel(
        f"[bold]Session saved:[/bold] {session_path}\n"
        f"[bold]Trial log:[/bold] {trial_logger.log_path}\n"
        f"[bold]API calls:[/bold] {summary['api_calls']}\n"
        f"[bold]Total tokens:[/bold] {summary['total_tokens']:,}\n"
        f"[bold]Total time:[/bold] {summary['total_elapsed']:.1f}s\n"
        f"[bold]Errors:[/bold] {summary['errors']}",
        title="[bold green]SESSION COMPLETE[/bold green]",
        border_style="green",
    ))


def _list_agents():
    """Display all available agents."""
    agents = list_all_agents()
    console.print("\n[bold]Available Forge Agents[/bold]\n")

    for a in agents:
        type_label = ""
        if a["permanent"]:
            type_label = "[green]permanent[/green]"
        elif a["contextual"]:
            type_label = "[yellow]contextual[/yellow]"
        if a["intake_only"]:
            type_label += " [dim](intake only)[/dim]"

        console.print(
            f"  [bold]{a['name']}[/bold] — {a['role']}\n"
            f"    Type: {type_label}  |  Default: {a['default_provider']}/{a['default_model']}"
        )
        console.print()


if __name__ == "__main__":
    app()
