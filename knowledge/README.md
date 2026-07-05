# knowledge/ — celda de conocimiento recuperable (kcell)

`kcell.py` es el **core común de las celdas de conocimiento**: un sistema de 2 capas,
sin dependencias (stdlib), local-first.

- **Capa 1 (map)** → emite el mapa base + contratos de un dominio (contexto inyectable a una sesión).
- **Capa 2 (search)** → retrieval léxico BM25-lite sobre *chunks*, con boost a la línea `PREGUNTAS`.
- **lookup** → ficha exacta por nombre (O(1) sobre un índice `by_name`).

## Por qué está acá
La premisa original del puente era "solo git + disciplina, sin herramientas". Esa premisa
era del arranque, para no sobre-construir antes de saber si servía. La utilidad de kcell
está probada → se adopta. **El motor sigue siendo git + disciplina; kcell es una herramienta
opcional para proyectos con conocimiento recuperable** (y la base sobre la que se construye
la capa de memoria/índice).

## Cómo se usa
1. Copiá `cell.json.example` → `cell.json` y completá los campos de tu dominio.
2. Poné tus `chunks.jsonl` (un chunk por línea) en el `artifacts_dir`.
3. Corré `python kcell.py map` / `lookup <nombre>` / `search "<consulta>"`.

Cada celda es un `cell.json` + sus artefactos; el `kcell.py` es el mismo para todas.
No se toca el motor: se configura por `cell.json`.
