# The Forge — Build Plan

---
version: 1.0
date: 2026-03-14
status: draft — awaiting Siva's review
---

---

## Architecture Decision

The Forge lives at **`forge/`** at the repo root, completely separate from the Next.js website in `src/`.

Why root-level, not inside `src/`:
- The website deploys to Vercel. The Forge runs locally. Different runtimes, different concerns.
- The Forge should be portable — works from Claude Code, Cowork, or standalone CLI.
- Clean boundary: `src/` is the public site. `forge/` is the thinking engine. `forge-sessions/` is the output archive. Content flows one way: Forge → sessions → published writing.

**Tech choice: TypeScript + Anthropic SDK.**
Not a web app. Not a framework. A CLI pipeline that orchestrates Claude calls with structured agent prompts, manages session state, and writes output files. Node.js because the repo is already a TypeScript project — zero new toolchain.

---

## Directory Structure

```
forge/
├── package.json                  # Standalone — own deps (anthropic SDK, yaml, chalk)
├── tsconfig.json
├── .env.example                  # ANTHROPIC_API_KEY placeholder
│
├── agents/                       # Agent definitions — one file per agent
│   ├── _schema.ts                # TypeScript type for agent config
│   ├── historian.ts              # Permanent agent
│   ├── first-principles.ts       # Permanent agent
│   ├── falsification.ts          # Permanent agent
│   ├── forced-inversion.ts       # Contextual — intake only
│   ├── consumer.ts               # Contextual
│   ├── business.ts               # Contextual
│   ├── platform.ts               # Contextual
│   ├── category-destruction.ts   # Contextual — 10-100 only
│   └── crucible.ts               # The synthesis agent
│
├── stages/                       # Stage logic — one file per stage
│   ├── 0-problem-definition.ts   # Compression + falsifiability loop
│   ├── 1-exploration.ts          # Parliament orchestrator
│   ├── 2-crucible.ts             # Synthesis
│   ├── 3-mode-switch.ts          # External contact flag
│   ├── 4-conviction.ts           # Force output format
│   └── 5-human-clock.ts          # Decision prompt
│
├── lib/                          # Shared utilities
│   ├── claude.ts                 # Anthropic SDK wrapper — single call interface
│   ├── parliament.ts             # Orchestrator — randomised sequence, blind execution
│   ├── session.ts                # Session state management (create, load, save)
│   ├── logger.ts                 # Markdown session logger
│   └── config.ts                 # Stage configs (agent selection per problem type)
│
├── run.ts                        # Main entry point — `npx tsx forge/run.ts`
└── README.md                     # Usage instructions
```

---

## The Eight Components — Build Order

Build order follows the deliberation pipeline. Each phase is usable on its own before moving to the next. No phase depends on a future phase.

### Phase 1 — Foundation (Day 1)

**1.1 Claude wrapper (`lib/claude.ts`)**
- Thin wrapper around `@anthropic-ai/sdk`
- Single function: `callAgent(systemPrompt, userMessage, conversationHistory?) → string`
- Handles API key from env, model selection, token limits
- Returns raw text response — no parsing, no opinions

**1.2 Session manager (`lib/session.ts`)**
- `createSession(problem)` → creates session object with ID, timestamp, stage, history
- `saveSession(session)` → writes to `forge-sessions/YYYY-MM/YYYY-MM-DD-problem-slug.md`
- `loadSession(path)` → resumes from saved file
- Session state: problem, stage, agent outputs (map), crucible output, conviction output, metadata

**1.3 Agent schema + three permanent agents**
- Agent config type: `{ name, role, systemPrompt, isContextual, activeWhen? }`
- Write system prompts for Historian, First Principles, Falsification
- Each prompt encodes the agent's epistemology, constraints, and output format
- System prompts are the soul of the system — they need to be precise, opinionated, and adversarial to each other

**Milestone: Can call any single agent with a problem and get a structured response.**

---

### Phase 2 — Problem Definition Loop (Day 1-2)

**2.1 Stage 0: Problem Definition (`stages/0-problem-definition.ts`)**
- Single-agent loop (dedicated compression agent, not the parliament)
- Takes raw problem statement from user
- Iterates: compress → test falsifiability → compress again
- Exit condition: problem is dense, specific, and a cold reader knows what a good solution looks like
- Interactive — prompts the user for confirmation before parliament activates
- Outputs: refined problem statement + falsifiability criteria

**Milestone: Can take a vague problem and compress it into something worth deliberating.**

---

### Phase 3 — Parliament (Day 2-3)

**3.1 Parliament orchestrator (`lib/parliament.ts`)**
- Takes: refined problem, list of active agents, session
- Randomises agent execution order (every session is different)
- Calls each agent sequentially
- **Blind outputs** — each agent sees only the problem statement, never other agents' responses
- Collects all outputs into session state
- Logs each agent's output to session file in real-time

**3.2 Forced Inversion Agent**
- Runs at intake, before parliament
- Takes the refined problem and generates the most counterintuitive, category-violating version
- Parliament receives both the original problem AND the inversion as context
- Not a permanent agent — structural intake mechanism

**3.3 Contextual agent selection (`lib/config.ts`)**
- Maps problem type to active agents:
  - 0-1 stage: permanents + Forced Inversion (always) + Consumer/Business/Platform as needed
  - 1-10 stage: permanents + Falsification prominent + steelman requirement
  - 10-100 stage: permanents + Category Destruction Agent activates
- User can override: add/remove contextual agents per session

**Milestone: Full parliament runs — multiple agents deliberate a problem independently, blind to each other.**

---

### Phase 4 — Crucible Synthesis (Day 3)

**4.1 Crucible agent (`agents/crucible.ts`)**
- Receives ALL agent outputs simultaneously (this is the only agent that sees everything)
- Does NOT summarise. Does NOT average.
- Produces:
  1. **Tension map** — where agents genuinely disagree and why
  2. **Convergence points** — where independent reasoning reached the same conclusion
  3. **Ranked conviction output** — with confidence levels (high/medium/low/uncertain)
  4. **Bias disclosure** — explicit statement of where the Crucible felt pulled toward a conclusion
- Output format is strictly enforced via system prompt

**4.2 Stage 2 runner (`stages/2-crucible.ts`)**
- Assembles all agent outputs into Crucible's input
- Calls Crucible
- Appends to session
- Saves session file

**Milestone: End-to-end exploration mode works. Problem → Definition → Parliament → Crucible → Session file.**

---

### Phase 5 — Conviction Mode (Day 4)

**5.1 Mode switch (`stages/3-mode-switch.ts`)**
- Not automated — this is a human signal
- CLI prompt: "Has external contact occurred? (customer call, prototype reaction, market data)"
- Flags session as switched from Exploration → Conviction
- Records what the external signal was

**5.2 Conviction output formatter (`stages/4-conviction.ts`)**
- Activates Force Output Format
- Takes Crucible synthesis + external signal
- Produces:
  1. Ranked decision with confidence levels
  2. **Steelman of abandonment** — explicit best case for NOT doing this
  3. Conditions under which this decision should be reversed
  4. Recommended next action

**5.3 Human Clock (`stages/5-human-clock.ts`)**
- Simple, brutal prompt: "Did you decide?"
- Not what the Forge produced. Not whether the analysis was good. Just — did you decide.
- Records answer. Closes session.

**Milestone: Full six-stage pipeline runs end-to-end.**

---

### Phase 6 — Session Logger + Publishing (Day 4-5)

**6.1 Markdown logger (`lib/logger.ts`)**
- Writes session to `forge-sessions/YYYY-MM/YYYY-MM-DD-problem-slug.md`
- Uses the existing `_template.md` structure
- Real-time: writes as each stage completes, not just at the end
- Includes metadata: date, agents active, stage, duration, mode switches

**6.2 Publish command**
- `npx tsx forge/run.ts --publish <session-path>`
- Reads completed session
- Strips private conviction output (only exploration is publishable)
- Generates MDX frontmatter (title, date, description, tags, stage, agents)
- Copies to `src/content/writing/YYYY-MM-DD-slug.mdx`
- User pushes to main → live on earnedconviction.com

**Milestone: Sessions are saved, archivable, and publishable to the website.**

---

### Phase 7 — Polish + Custom Agents (Day 5)

**7.1 Custom agent creation**
- `npx tsx forge/run.ts --new-agent`
- Interactive: name, role, epistemology, constraints
- Generates agent config file in `forge/agents/custom/`
- Available for selection in future sessions

**7.2 Session resume**
- `npx tsx forge/run.ts --resume <session-path>`
- Loads saved session, picks up from last completed stage
- Useful when waiting for external contact (mode switch)

**7.3 Remaining contextual agents**
- Consumer Agent, Business Agent, Platform Agent, Category Destruction Agent
- Lower priority — permanents + Crucible carry most sessions

---

## What This Plan Does NOT Include (Future)

These are listed in the PRD as "To Build — Future" and are separate projects:
- `forge.earnedconviction.com` — public web interface
- Session archive browser
- Agent Whitepaper generator pipeline
- GEO explainer pipeline

The local CLI system must be rock-solid before any of these make sense.

---

## Key Design Decisions

**Why sequential, not parallel agent calls?**
The PRD requires randomised order. If agents ran in parallel, order wouldn't matter. Sequential execution means the *system* processes them in a random order, which affects how the Crucible weights early vs. late outputs if there's any context leakage. More importantly — sequential is simpler to build, debug, and log.

**Why blind outputs?**
Prevents anchoring bias (Tversky). The PRD explicitly calls this out in the Risk Registry. Each agent must reason from the problem alone, not from what another agent said.

**Why TypeScript CLI and not a Cowork skill?**
Portability. The PRD says "Claude Code on Windows PC." A TS CLI works in Claude Code, Cowork, or standalone terminal. A Cowork skill only works in Cowork. Build for the widest surface, then add convenience layers later.

**Why own `package.json` inside `forge/`?**
The Next.js site and The Forge have different dependencies. The site needs React, MDX, Tailwind. The Forge needs the Anthropic SDK and that's about it. Separate `package.json` keeps both clean. No risk of the Forge pulling in website deps or vice versa.

---

## Estimated Effort

| Phase | Components | Estimate |
|-------|-----------|----------|
| 1 — Foundation | Claude wrapper, session manager, 3 agent prompts | 2-3 hours |
| 2 — Problem Definition | Stage 0 interactive loop | 1-2 hours |
| 3 — Parliament | Orchestrator, Forced Inversion, agent config | 2-3 hours |
| 4 — Crucible | Synthesis agent, Stage 2 runner | 1-2 hours |
| 5 — Conviction Mode | Mode switch, conviction formatter, Human Clock | 1-2 hours |
| 6 — Logger + Publishing | Session files, MDX export | 1-2 hours |
| 7 — Polish | Custom agents, resume, contextual agents | 2-3 hours |
| **Total** | | **10-17 hours** |

Phases 1-4 get you a working Exploration mode. That's the core. Phases 5-7 complete the system.

---

## How to Run (Once Built)

```bash
# Start a new Forge session
cd forge && npx tsx run.ts

# Resume a paused session (waiting for external contact)
cd forge && npx tsx run.ts --resume ../forge-sessions/2026-03/2026-03-14-problem-slug.md

# Publish a completed session to the website
cd forge && npx tsx run.ts --publish ../forge-sessions/2026-03/2026-03-14-problem-slug.md

# Create a custom agent
cd forge && npx tsx run.ts --new-agent
```

---

## Open Questions for Siva

1. **API key** — Do you have an Anthropic API key, or should the Forge use a different LLM provider? (The system is designed for Claude, but the wrapper can abstract this.)

2. **Model choice** — Claude Sonnet for speed during parliament, Opus for Crucible synthesis? Or Opus everywhere for maximum depth?

3. **Interactivity level** — Should the CLI pause after each agent output for you to read, or run the full parliament uninterrupted and present everything at the end?

4. **Session privacy** — The PRD says conviction output is private and exploration is publishable. Should the session file contain both (with a marker), or should conviction output go to a separate file?
