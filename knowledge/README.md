# knowledge/ — recoverable knowledge cell (kcell)

`kcell.py` is the **shared core of the knowledge cells**: a 2-layer system, with no
dependencies (stdlib), local-first.

- **Layer 1 (map)** -> emits the base map + contracts of a domain (context you can inject into a session).
- **Layer 2 (search)** -> BM25-lite lexical retrieval over *chunks*, with a boost to the `QUESTIONS` line.
- **lookup** -> exact record by name (O(1) over a `by_name` index).

## Why it's here
The bridge's original premise was "just git + discipline, no tools". That premise was from the
start, to avoid over-building before we knew it was useful. kcell's usefulness is proven -> it
gets adopted. **The engine is still git + discipline; kcell is an optional tool for projects
with recoverable knowledge** (and the base the memory/index layer is built on).

## How to use it
1. Copy `cell.json.example` -> `cell.json` and fill in your domain's fields.
2. Put your `chunks.jsonl` (one chunk per line) in the `artifacts_dir`.
3. Run `python kcell.py map` / `lookup <name>` / `search "<query>"`.

Each cell is a `cell.json` + its artifacts; `kcell.py` is the same for all of them.
You don't touch the engine: you configure it via `cell.json`.
