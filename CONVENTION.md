# CONVENTION — la doctrina del puente

> Corta a propósito. La simpleza es lo que hace que el sistema funcione. Cada regla nació de una cicatriz
> real; se refuerza de acá en adelante, NO se aplica retroactivamente.

## Topología estrella
Un ORQUESTADOR central; N ejecutores que hablan SOLO con él, nunca entre sí. La coordinación cruzada pasa
siempre por el centro. (Detalle en `roles/ROLE-ORCHESTRATOR.md`.)

## Principio rector: no dupliques git
Git ya sabe **cuándo** (timestamp), **qué archivo** y **qué cambió** (diff), con precisión perfecta. El
mailbox NO repite eso. El mailbox lleva lo que git NO captura: **el razonamiento, la decisión, el porqué.**

## Los 3 metadatos que SÍ habilitan filtrado (git no los da)
Todo mensaje abre con un header ASCII grep-safe (sin acentos):
```
## [AUTOR->DESTINO · YYYY-MM-DD · CODE: XXX[,YYY] · STATUS: ...]
```
1. **Clave de interlocutor** — `[ORQUESTADOR->EJECUTOR:<apellido>]`, `[EJECUTOR:<apellido>->ORQUESTADOR]`,
   `[...->ALL]`. Filtrás por quién habla a quién.
2. **Tema / CODE** — la tarea o frente. Campo de primera clase. Si tu proyecto define códigos, van en
   `docs/INDICE-TEMAS.md`. Si ninguno encaja: `MISC` (imprecisión deliberada, filtrable). Nunca sin nada.
3. **STATUS** — `DONE` / `IN-PROGRESS` / `BLOCKED` / `REQUIRES-ORQUESTADOR` / `REQUIRES-USUARIO`.

**Quién taggea:** cada autor el suyo AL ESCRIBIR (en origen, autoritativo). Cicatriz: clasificar por
heurística DESPUÉS adivina y sesga; taggear en origen es determinístico.

## Puntero de archivo: mínimo, no exacto
Un puntero corto para saber dónde mirar ("está en `knowledge/`") sí; la ruta con línea (`.../x.py:142`) no
— eso lo da git. El mailbox orienta; git precisa.

## Densidad sobre fragmentación
**Un mensaje = una unidad de trabajo con su decisión.** No fragmentes una tarea en diez mensajes. Mejor uno
denso y auto-contenido que cinco cortos.

## Dos lugares, no diez
- `docs/PLAN.md` = índice maestro, "estado actual" siempre fresco. Si algo afecta el estado, va acá.
- `mailbox/raw/*` = registro histórico append-only. Lo que es historia queda acá.
Si importa para el estado → PLAN. Si es historia → mailbox. Nada de un tercer lugar.
(Y para el estado entre sesiones existe el Canon, en su repo propio — ver ROLE-ORCHESTRATOR.)

## Un clone por sesión concurrente
Cicatriz real: varias sesiones sobre el MISMO clone local se pisaron el WIP (una tapó el trabajo de otra).
Regla: **cada sesión ejecutora concurrente trabaja en SU PROPIO clone** (o un `git worktree` por apellido).
El remoto es el punto de encuentro, no la carpeta local. Si encontrás WIP ajeno en un working tree
compartido heredado: stash → pull → pop (preservar, nunca descartar lo ajeno), avisar por mailbox, migrar a
tu propio clone. Commit+push ANTES de ceder la sesión (el WIP local es invisible para todos).

## Domain integrity — hard rule   [FILL IN ON FORK]
> Cada dominio tiene UNA regla de integridad no negociable. Escribí la tuya.
> Ejemplos de otros puentes:
>  - Servidor de juego: "las acciones económicas se revisan doble (spec -> review -> OK humano)".
>  - Caso legal: "cada evidencia con fuente+fecha+custodia; el hecho se separa de la interpretación".
>  - Infra/producto: "los cambios a producción requieren al owner presente".
>  - Herramienta con automatización: "NUNCA trabajar sobre supuestos; verificar, no asumir".
> (Reemplazá este bloque con tu regla. Si parece que no tenés ninguna, mirá de nuevo: siempre hay una.)

## Gates   [FILL IN ON FORK]
- Acciones sensibles, irreversibles o hacia afuera se marcan `[HUMAN]` y esperan OK del usuario.
- Listá las de tu dominio (ej. publicar, deploy a prod, contactar a alguien, borrar datos, gastar dinero,
  encender automatización, tocar archivos con secretos).

## Commit = push, verificado
Un commit sin push no existe y traba la cola. El ciclo es atómico: `pull --rebase` → editar → commit →
`push` confirmado. Nada pudriéndose en local.
