# bridge-template

Plantilla mínima de un **puente**: un hub de coordinación en **topología estrella**
para trabajar un proyecto con múltiples sesiones de IA especializadas, manteniendo
el **contexto recuperable entre sesiones**. El repo ES la memoria del proyecto.

No inventa herramientas por inventar: arranca con **git + una disciplina simple**, y suma
herramientas propias solo cuando su utilidad está probada (la primera: `kcell`, la celda de
conocimiento). Esa es la idea — evolución lenta y verificada, no sobre-diseño.

## Cómo se usa
1. Apretá **"Use this template"** (arriba) → creás tu propio repo a partir de esta base.
2. Seguí `FORK.md` — el checklist de acomodo a tu proyecto.
3. Generá un PAT de alcance mínimo (solo tu repo, rotable).
4. Corré la sesión ANALIZADOR-INICIAL (descompone el proyecto) → luego la ORQUESTADOR.

## Las piezas del core
- `CONVENCION-PUENTE.md` — la doctrina (el motor). Estrella, commit=push, PLAN único, mailboxes append-only.
- `roles/` — ROL-ORQUESTADOR (coordina), ROL-EJECUTOR (plantilla base), ROL-ANALIZADOR-INICIAL (arranque de un solo uso).
- `mailbox/` — `to-orquestador.md` (ejecutores → orquestador) y `to-ejecutores.md` (orquestador → ejecutores). Append-only.
- `docs/PLAN.md` — la fuente única de verdad del estado.
- `docs/INVENTARIO-CREDENCIALES.md` — mapa de credenciales (punteros-only; el valor nunca acá).
- `knowledge/kcell.py` — celda de conocimiento recuperable (opcional; ver `knowledge/README.md`).
- `prompts/` — plantillas de arranque de cada sesión.

## Filosofía
Pilotá chico y crecé. No sobre-diseñes antes de necesitarlo. Lo específico de tu
dominio va en los ganchos marcados `[COMPLETAR EN EL FORK]`, no reescribiendo el motor.
