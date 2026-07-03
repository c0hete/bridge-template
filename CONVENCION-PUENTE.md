# CONVENCIÓN DEL PUENTE — [NOMBRE DEL PROYECTO]

## Qué es
Hub de coordinación en topología estrella para trabajar este proyecto con múltiples
sesiones de IA especializadas, manteniendo el contexto recuperable entre sesiones.
El repo ES la memoria del proyecto.

## Topología (estrella) — regla dura
- Los ejecutores hablan SOLO con el ORQUESTADOR. Nunca entre ellos.
- El ORQUESTADOR es el único que ve todos los frentes y rutea los cruces.
- Un ejecutor que necesita algo de otro frente se lo pide al orquestador.

## Mailboxes (append-only)
- `mailbox/to-orquestador.md` -> uplink: ejecutores ESCRIBEN al orquestador.
- `mailbox/to-ejecutores.md`  -> downlink: orquestador ESCRIBE a los ejecutores.
- Nunca se reescribe ni se borra un mensaje. Solo se agrega al final.
- Formato de mensaje:
  `## [DE->PARA · AAAA-MM-DD (tema)] título`
  cuerpo...
  `[DE]`  (firma al cierre)

## Integridad de la operación — regla dura (commit=push)
- Toda acción sobre el repo: `git pull --rebase -q` -> `commit` -> `push`, atómico.
- Si no está pusheado, no existe. Trabajo local sin pushear FRENA a toda la estrella
  sin que nadie sepa por qué. Por eso es regla dura, no sugerencia.

## PLAN como fuente única
- `docs/PLAN.md` es la ÚNICA fuente de verdad del estado del proyecto.
- Ante conflicto entre una charla y el PLAN, gana el PLAN.
- Una sesión fresca se pone al día leyendo el PLAN, no releyendo el historial de mensajes.
- El orquestador lo mantiene al día.

## Integridad del dominio — regla dura   [COMPLETAR EN EL FORK]
> Todo dominio tiene UNA regla de integridad que no se negocia. Escribí la tuya acá.
> Ejemplos reales de otros puentes:
>  - Server de juego: "las acciones económicas se superrevisan (spec -> revisión -> OK humano)".
>  - Caso legal: "cada evidencia lleva fuente+fecha+custodia; el hecho se separa de la interpretación; nunca se fabrica ni se rellena un dato faltante".
>  - Infra: "cambios en producción requieren al dueño presente; nada destructivo sin backup".
> (Reemplazá este bloque por tu regla. Si tu proyecto no tuviera ninguna, mirá de nuevo: siempre hay una.)

## Gates   [COMPLETAR EN EL FORK]
- Acciones sensibles, irreversibles o hacia afuera se marcan `[HUMANO]` y esperan OK.
- Listá acá cuáles aplican a tu dominio (ej: publicar, desplegar a prod, contactar a alguien,
  borrar datos, gastar dinero).

## Doctrina de arranque
- Pilotar chico y crecer. No sobre-diseñar antes de necesitarlo.
- Cada sesión, al abrir, lee su ROL + este archivo + el PLAN -> queda al día.
- El ORQUESTADOR se rota cuando empieza a errar formato (señal de contexto saturado,
  no de que se rompió): una sesión nueva se pone al día leyendo el PLAN.
