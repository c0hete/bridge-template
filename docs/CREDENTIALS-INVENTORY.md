# CREDENTIALS INVENTORY — [PROJECT NAME] (a MAP, not a vault)

## What it is and what it is NOT
A single map of ALL the project's credentials: what exists, what it unlocks, where the value
lives, who uses it, rotation status. It exists because without a map you don't know where the
locks are or where the keys are. The ORCHESTRATOR maintains it (global view); each front
reports the POINTERS for ITS credentials.

## HARD RULE
**The VALUE of a credential NEVER goes here. Only POINTERS** (location, variable/entry name,
host/port). The value lives in the VAULT (secrets manager) or in the environment's `.env`
that uses it. This doc is a git repo -> a value here = a leak. **Pointers yes, secrets no.**
- **Vault** (secrets manager) = where the VALUES are kept.
- **This inventory** = the MAP (what exists and what each thing opens).

## Fields
`ID · What it unlocks · Where the value lives (POINTER) · Who uses it · Rotation · Sensitivity`
Sensitivity: **CRITICAL** (prod / people's data) · **HIGH** · **MEDIUM** · **LOW**.

## Inventory

| ID | What it unlocks | Where it lives (pointer) | Who uses it | Rotation | Sens. |
|----|-----------------|--------------------------|-------------|----------|-------|
| EXAMPLE-PAT | Contents R/W on the bridge repo (fine-grained, 1 repo) | secrets manager, entry `BRIDGE_TOKEN` | orchestrator + executors | rotatable, with expiry | LOW |
| _(fill in with yours — pointer, never the value)_ | | | | | |

## How it's maintained
Each front reports to the orchestrator the pointer of a new or rotated credential (never the
value) -> the orchestrator updates this map. Each rotation is noted with a date. The goal: that
at any moment you can tell, without guessing, where each lock is and where its key is.
