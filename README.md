# bridge-template

A minimal **bridge**: a coordination hub in a **star topology** for running a project with
multiple specialized AI sessions, keeping **context recoverable across sessions**. The repo
IS the project's memory.

It doesn't add tooling for its own sake: it starts with **git + a simple discipline**, and
grows its own tools only once their usefulness is proven (the first: `kcell`, the knowledge
cell). That's the idea — slow, verified evolution over up-front design.

## How to use it
1. Click **"Use this template"** (top of the page) to create your own repo from this base.
2. Follow `FORK.md` — the checklist for adapting it to your project.
3. Generate a minimal-scope PAT (this repo only, rotatable).
4. Run the INITIAL-ANALYZER session (it breaks the project down), then the ORCHESTRATOR.

## Core pieces
- `CONVENTION.md` — the doctrine (the engine): star topology, commit=push, single PLAN, append-only mailboxes, and the hard rules every session inherits.
- `roles/` — ROLE-ORCHESTRATOR (coordinates), ROLE-EXECUTOR (base template), ROLE-INITIAL-ANALYZER (one-shot bootstrap).
- `mailbox/` — `to-orchestrator.md` (executors → orchestrator) and `to-executors.md` (orchestrator → executors). Append-only.
- `docs/PLAN.md` — the single source of truth for project state.
- `docs/CREDENTIALS-INVENTORY.md` — a credential map (pointers only; the value never lives here).
- `knowledge/kcell.py` — a recoverable knowledge cell (optional; see `knowledge/README.md`).
- `prompts/` — bootstrap templates for each session.

## Philosophy
Pilot small and grow. Don't over-design before you need it. What's specific to your domain
lives in the hooks marked `[FILL IN ON FORK]`, not in a rewrite of the engine.
