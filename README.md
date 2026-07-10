# bridge-template

Un **puente**: el hub de coordinación en **topología estrella** para correr un proyecto con varias
sesiones de IA especializadas, manteniendo el **contexto recuperable entre sesiones**. El repo ES la
memoria del proyecto.

## El espíritu (por qué este template es distinto)

No es un andamiaje vacío. Es la **destilación de un puente que funcionó** — sus reglas no se diseñaron
de entrada, **evolucionaron de cicatrices reales.** Cada regla dura de acá lleva el *por qué* que la
originó: por qué no usás `git add -A` (coló un archivo rechazado al historial), por qué cada sesión
trabaja en su propio clone (dos sesiones se pisaron el trabajo), por qué taggeás en origen y no después
(clasificar por heurística sesga). **Una regla sin su cicatriz se rompe sin entender por qué estaba;**
por eso las cicatrices viajan con las reglas.

Tres ideas rectoras:
- **No dupliques git.** Git ya sabe cuándo, qué archivo y qué cambió. El mailbox lleva lo que git NO
  captura: el razonamiento, la decisión, el porqué.
- **Nunca sobre supuestos.** Verificá antes de afirmar/decidir/construir. Verificar es barato; un
  supuesto falso es caro (lo descubrís con medio sistema encima).
- **Piloteá chico y crecé.** No sobre-diseñes antes de necesitarlo. Las herramientas se ganan su lugar
  cuando prueban su utilidad, no antes.

## Cómo se usa
1. **"Use this template"** (arriba) para crear tu repo desde esta base.
2. Seguí `FORK.md` — el checklist para adaptarlo a tu proyecto (llenás los hooks `[FILL IN ON FORK]`,
   NO reescribís el motor).
3. Generá un PAT de alcance mínimo (solo este repo, `contents:write`, rotable).
4. Forkeá también un **Canon** (de `canon-template`) — es la memoria de estado entre sesiones.
5. Corré el ORQUESTADOR: lee el Canon primero, el PLAN después, y coordina a los ejecutores.

## Las piezas
- `CONVENTION.md` — la doctrina: topología estrella, no-dupliques-git, los 3 metadatos de filtrado
  (autor/CODE/STATUS), densidad sobre fragmentación, un-clone-por-sesión, commit=push. Las reglas que
  toda sesión hereda.
- `roles/ROLE-ORCHESTRATOR.md` — la capa de razonamiento: arranca leyendo el Canon, coordina, gatea lo
  sensible, valida los tags del usuario (son input, no verdad absoluta), mantiene el lock ni-0-ni-2.
- `roles/ROLE-EXECUTOR.md` — el manual de inducción del ejecutor: git exacto (con cicatrices), commit=push,
  secretos por referencia nunca por valor, escala en vez de improvisar.
- `roles/ROLE-DOCUMENTALIST.md` — rol a demanda (opcional): destila estado (foto) y evolución
  histórica vía arqueología de git (película). No toca el flujo diario.
- `mailbox/raw/` — `to-orchestrator.md` (ejecutor → orquestador) y `to-executors.md` (orquestador →
  ejecutor). Append-only. Header: `## [AUTOR->DESTINO · YYYY-MM-DD · CODE: XXX · STATUS: ...]`.
- `docs/PLAN.md` — el estado actual del proyecto (el orquestador lo mantiene fresco).
- `docs/CREDENTIALS-INVENTORY.md` — mapa de credenciales (punteros; el valor NUNCA vive acá).
- `knowledge/kcell.py` — celda de conocimiento recuperable (opcional).

## Dos memorias, distintas
- **PLAN** (acá) = estado ACTUAL, fresco, sobreescribible. "¿Dónde estamos hoy?"
- **Canon** (repo aparte, de `canon-template`) = TRAYECTORIA con fechas ancladas. "¿Cómo y por qué
  llegamos acá?" El orquestador lo lee primero al arrancar; es su memoria entre resets.

## Seguridad de base
- Topología estrella: los ejecutores hablan solo con el orquestador, nunca entre sí.
- Secretos: nunca en un commit, en el mailbox, ni en el chat. Solo punteros (archivo + variable).
- Gates: lo destructivo/irreversible/hacia-afuera espera OK humano.
- PAT de alcance mínimo y rotable — asumí que puede quedar expuesto en un transcript.
