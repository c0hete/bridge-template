# FORK.md — checklist for adapting the bridge to your project

This is the setup manual. When you create your repo from the template, follow these steps.
What's NOT here (the engine) isn't touched; you only fill in the hooks.

## 1. Project identity
- [ ] In `README.md` and `CONVENTION.md`, replace the generic name with your project's.
- [ ] Write the real project goal in `docs/PLAN.md`.

## 2. Fill in the domain hooks (search for `[FILL IN ON FORK]`)
- [ ] `CONVENTION.md` → **Domain integrity** section: define the hard rule specific to your
      case. Real examples: "economic actions are double-reviewed" (game server), "every piece
      of evidence with source+date+custody; fact != interpretation" (legal case), "production
      changes require the owner present" (infra). There is ALWAYS one; write yours.
- [ ] `CONVENTION.md` → **Gates** section: which actions are irreversible/sensitive in your
      domain and must wait for a human OK.

## 3. Define your roles
- [ ] Duplicate `roles/ROLE-EXECUTOR.md` once per front of your project and specialize it
      (e.g. ROLE-EMAIL, ROLE-SERVER, ROLE-WRITER...). ROLE-EXECUTOR is the base template.
- [ ] Adjust `roles/ROLE-ORCHESTRATOR.md` only if your project needs something special (usually not).
- [ ] Create a domain index if you need one (e.g. `docs/INDEX-*.md`) — the catalog of what's custom.

## 4. Mailbox names (optional)
- [ ] Default: `to-orchestrator.md` / `to-executors.md`. Rename them if you prefer, but do it
      BEFORE you start (the names are inherited by every message).

## 5. Security / secrets
- [ ] Decide whether the repo is public or **private** (if it handles anything sensitive -> private).
- [ ] Generate a **fine-grained, minimal-scope PAT**: this repo only, `Contents: Read and write`,
      with an expiry. Rotatable. Never push secrets to the repo — only their index.
- [ ] The artifact is ready: `docs/CREDENTIALS-INVENTORY.md` (pointers-only map). Seed it with
      your credentials — a pointer (location + variable name), NEVER the value. Each front reports
      its own pointers; the orchestrator maintains the map.

## 5b. Knowledge cell (optional)
- [ ] If your project handles recoverable knowledge (a large domain, docs, a history to index),
      use `knowledge/kcell.py`: copy `cell.json.example` -> `cell.json`, add your `chunks.jsonl`,
      and query with `map` / `lookup` / `search`. The engine is git + discipline; kcell is an
      optional, already-proven tool. See `knowledge/README.md`.

## 6. Bootstrap
- [ ] Fill in the `[...]` gaps in `prompts/PROMPT-ORCHESTRATOR.md` and `prompts/PROMPT-INITIAL-ANALYZER.md`.
- [ ] Run the INITIAL-ANALYZER first (it fills `docs/INITIAL-BREAKDOWN.md`).
- [ ] Then the ORCHESTRATOR session: reads the bridge, confirms understanding, builds the PLAN, and delegates.

## Doctrine worth not breaking
- Star topology: executors talk only to the orchestrator.
- Atomic commit=push: unpushed work = work that doesn't exist (and it stalls the queue).
- The PLAN is the single source of truth: a fresh session gets up to speed from the PLAN, not the chat history.
- Pilot small. Add roles when volume demands it, not before.
