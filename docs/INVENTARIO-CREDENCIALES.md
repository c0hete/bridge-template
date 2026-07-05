# INVENTARIO DE CREDENCIALES — [NOMBRE DEL PROYECTO] (MAPA, no bóveda)

## Qué es y qué NO es
Mapa único de TODAS las credenciales del proyecto: qué existe, qué desbloquea, dónde vive el
valor, quién la usa, estado de rotación. Nace porque sin un mapa no se sabe dónde están los
candados ni dónde las llaves. Lo mantiene el ORQUESTADOR (visión global); cada frente reporta
los PUNTEROS de SUS credenciales.

## REGLA DURA
**Acá NUNCA va el VALOR de una credencial. Solo PUNTEROS** (ubicación, nombre de variable/
entrada, host/puerto). El valor vive en la BÓVEDA (gestor de secretos) o en el `.env` del
entorno que lo usa. Este doc es un repo git → un valor acá = filtración. **Punteros sí,
secretos no.**
- **Bóveda** (gestor de secretos) = dónde se guardan los VALORES.
- **Este inventario** = el MAPA (qué hay y qué abre cada cosa).

## Campos
`ID · Qué desbloquea · Dónde vive el valor (PUNTERO) · Quién la usa · Rotación · Sensibilidad`
Sensibilidad: **CRÍTICA** (prod / datos de personas) · **ALTA** · **MEDIA** · **BAJA**.

## Inventario

| ID | Qué desbloquea | Dónde vive (puntero) | Quién la usa | Rotación | Sens. |
|----|----------------|----------------------|--------------|----------|-------|
| EJEMPLO-PAT | Contents R/W en el repo del puente (fine-grained, 1 repo) | gestor de secretos, entrada `BRIDGE_TOKEN` | orquestador + ejecutores | rotable, con expiración | BAJA |
| _(completá con lo tuyo — puntero, nunca el valor)_ | | | | | |

## Cómo se mantiene
Cada frente reporta al orquestador el puntero de una credencial nueva o rotada (jamás el
valor) → el orquestador actualiza este mapa. Cada rotación se anota con fecha. Objetivo: que
en cualquier momento se sepa, sin adivinar, dónde está cada candado y dónde su llave.
