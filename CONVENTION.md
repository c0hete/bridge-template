# BRIDGE CONVENTION — [PROJECT NAME]

## What it is
A coordination hub in a star topology for running this project with multiple specialized AI
sessions, keeping context recoverable across sessions. The repo IS the project's memory.

## Topology (star) — hard rule
- Executors talk ONLY to the ORCHESTRATOR. Never to each other.
- The ORCHESTRATOR is the only one who sees every front and routes the cross-cutting items.
- An executor that needs something from another front asks the orchestrator for it.

## Mailboxes (append-only)
- `mailbox/to-orchestrator.md` -> uplink: executors WRITE to the orchestrator.
- `mailbox/to-executors.md`    -> downlink: the orchestrator WRITES to the executors.
- A message is never rewritten or deleted. You only append at the end.
- Message format:
  `## [FROM->TO · YYYY-MM-DD (topic)] title`
  body...
  `[FROM]`  (signature at the close)

## Operational integrity — hard rule (commit=push)
- Every change is ONE atomic cycle, IN THIS ORDER:
  `git add -A && git commit -m "..."`  ->  `git pull --rebase`  ->  `git push`.
- COMMIT BEFORE YOU PULL. `git pull --rebase` with unstaged changes fails ("cannot pull with
  rebase: you have unstaged changes"). Commit your work first, rebase it on top of the remote,
  then push. Pulling first only works when the tree is already clean.
- If it isn't pushed, it doesn't exist. Local work left unpushed STALLS the whole star
  without anyone knowing why. That's why it's a hard rule, not a suggestion.

## PLAN as the single source of truth
- `docs/PLAN.md` is the ONLY source of truth for project state.
- On any conflict between a chat and the PLAN, the PLAN wins.
- A fresh session gets up to speed by reading the PLAN, not by re-reading the message history.
- The orchestrator keeps it current.

## Observe, don't guess — hard rule
- You diagnose by REPRODUCING or MEASURING, not by assuming. You verify against the real
  source (the code, the log, the config, the data) BEFORE asserting anything.
- Anything brought in from OUTSIDE the project (external docs, forums, another repo) is tagged
  with its verification level: `verified` / `inferred` / `unverified`. An assumption is never
  mixed with a fact.
- If a local check exists (compile, build, schema-validate, lint, test), RUN it before you push.
  Don't ship config or code you could have validated at your desk — a local build catches config
  and compile errors at commit time, not at the human's runtime.

## Judgment over obedience — hard rule
- An executor STOPS before breaking something (a hard stop) and flags the risk, instead of
  executing blindly.
- If an order looks like it will break something, or isn't safe, you halt and tell the
  orchestrator — you don't run it and break things. Genuine judgment is valued over literal
  compliance.
- This is distinct from Gates: Gates say WHICH actions wait for a human OK; this rule is about
  HOW an executor behaves in the face of any order.

## Shared resource = one turn at a time — hard rule
- If several sessions share a MUTABLE resource (Docker, a database, a working tree, a state
  file), only ONE touches it at a time. The orchestrator sequences the turns.
- Check that the resource is free before taking it (don't assume). Release it when done.

## Secrets — hard rule
- The bridge is a git repo: the VALUE of a secret NEVER goes in it, only its POINTER.
- The credential map lives in `docs/CREDENTIALS-INVENTORY.md` (pointers only); the values live
  in a secrets manager or the server-side `.env`. Secret handoffs happen OUT OF BAND, not
  through the bridge.
- A PAT/token is stored ONLY via the wake-up script's hidden input. NEVER write `.env` with the
  token value in a visible command, never paste it into a file inline, never print it. Never
  embed it in a remote URL; use a credential helper, or if you must embed it for one clone, scrub
  it immediately with `git remote set-url origin <clean-url>`. The value must never appear in
  command output, a transcript, or a committed file.

## Domain integrity — hard rule   [FILL IN ON FORK]
> Every domain has ONE integrity rule that isn't up for negotiation. Write yours here.
> Real examples from other bridges:
>  - Game server: "economic actions get double-reviewed (spec -> review -> human OK)".
>  - Legal case: "every piece of evidence carries source+date+custody; fact is kept separate
>    from interpretation; a missing data point is never fabricated or filled in".
>  - Infra: "production changes require the owner present; nothing destructive without a backup".
> (Replace this block with your rule. If your project seems to have none, look again: there's always one.)

## Gates   [FILL IN ON FORK]
- Sensitive, irreversible, or outward-facing actions are marked `[HUMAN]` and wait for an OK.
- List here which ones apply to your domain (e.g. publishing, deploying to prod, contacting
  someone, deleting data, spending money).

## Bootstrap doctrine
- Pilot small and grow. Don't over-design before you need it.
- Each session, on opening, reads its ROLE + this file + the PLAN -> it's up to speed.
- The ORCHESTRATOR is rotated when it starts making formatting errors (a sign of a saturated
  context, not that it broke): a fresh session gets up to speed by reading the PLAN.
