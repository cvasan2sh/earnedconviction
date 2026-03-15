# The Forge

Multi-agent deliberation system. Takes hard problems and subjects them to adversarial multi-perspective examination.

## Quick Start

```bash
# Dry run (no API keys needed)
python -m forge.run --dry-run "Should I build a SaaS product for X?"

# Real run (needs API keys in forge/.env)
python -m forge.run "Your problem here"

# Interactive mode (pause after each agent)
python -m forge.run -i "Your problem here"

# Exploration only (stages 0-2, no conviction)
python -m forge.run --explore "Your problem here"

# Resume a saved session
python -m forge.run --resume forge-sessions/2026-03/session.state.json

# List all agents
python -m forge.run --list-agents
```

## Setup

```bash
cd forge
cp .env.example .env
# Fill in your API keys
```

Required keys depend on which agents you use:
- `ANTHROPIC_API_KEY` — First Principles, Falsification, Crucible, Problem Definition
- `OPENAI_API_KEY` — Forced Inversion
- `GOOGLE_API_KEY` — Historian, Platform

## Pipeline

```
Stage 0: Problem Definition    → Compress until dense, specific, falsifiable
Stage 1: Exploration           → Forced Inversion + blind parliament
Stage 2: Crucible Synthesis    → Tension map, convergence, conviction ranking
Stage 3: Mode Switch           → External contact triggers conviction mode
Stage 4: Conviction            → Ranked decision + steelman of abandonment
Stage 5: Human Clock           → "Did you decide?"
```

## Agents

**Permanent** (every session):
- **Historian** — Precedents, data, institutional positions (Gemini)
- **First Principles** — Rational derivation from base assumptions (Claude Opus)
- **Falsification** — Popperian logic, finds breaking points (Claude Opus)

**Contextual** (selected per problem):
- **Forced Inversion** — Counterintuitive reframing at intake (GPT-4o)
- **Consumer** — End-user empathy and real behaviour (Claude Sonnet)
- **Business** — Unit economics, defensibility, GTM (Claude Sonnet)
- **Platform** — Technology landscape, infra, regulation (Gemini)
- **Category Destruction** — Invalidates categories at 10-100 stage (Claude Opus)

**Crucible** — Receives all outputs, maps tensions, produces ranked conviction.

## Output

- **Session file**: `forge-sessions/YYYY-MM/date-slug.md`
- **State file**: `.state.json` (for resume)
- **Private conviction**: `.private.md` (never publish)
- **Trial log**: `forge/logs/timestamp-session-trial.jsonl`

## Tests

```bash
python -m pytest forge/tests/ -v
```
