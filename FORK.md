# FORK.md — checklist para acomodar el puente a tu proyecto

Este archivo es el manual de acomodo. Al crear tu repo desde el template, seguí
estos pasos. Lo que NO está acá (el motor) no se toca; solo se rellenan los ganchos.

## 1. Identidad del proyecto
- [ ] En `README.md` y `CONVENCION-PUENTE.md`, reemplazá el nombre genérico por el de tu proyecto.
- [ ] Escribí el objetivo real del proyecto en `docs/PLAN.md`.

## 2. Completá los ganchos de dominio (buscá `[COMPLETAR EN EL FORK]`)
- [ ] `CONVENCION-PUENTE.md` → sección **Integridad del dominio**: definí la regla dura
      propia de tu caso. Ejemplos reales: "acciones económicas superrevisadas" (server de juego),
      "cada evidencia con fuente+fecha+custodia; hecho ≠ interpretación" (caso legal),
      "cambios en producción requieren dueño presente" (infra). SIEMPRE existe una; escribí la tuya.
- [ ] `CONVENCION-PUENTE.md` → sección **Gates**: qué acciones son irreversibles/sensibles
      en tu dominio y deben esperar OK humano.

## 3. Definí tus roles
- [ ] Duplicá `roles/ROL-EJECUTOR.md` una vez por cada frente de tu proyecto y especializalo
      (ej: ROL-CORREOS, ROL-SERVER, ROL-REDACTOR...). El ROL-EJECUTOR base es la plantilla.
- [ ] Ajustá `roles/ROL-ORQUESTADOR.md` solo si tu proyecto necesita algo especial (normalmente no).
- [ ] Creá un índice de dominio si lo necesitás (ej: `docs/INDICE-*.md`) — es el catálogo de lo custom.

## 4. Nombres de mailbox (opcional)
- [ ] Por defecto: `to-orquestador.md` / `to-ejecutores.md`. Renombralos si preferís, pero
      hacelo ANTES de arrancar (se hereda a todos los mensajes).

## 5. Seguridad / secretos
- [ ] Decidí si el repo es público o **privado** (si maneja algo sensible → privado).
- [ ] Generá un **PAT fine-grained de alcance mínimo**: solo este repo, `Contents: Read and write`,
      con expiración. Rotable. Nunca subas secretos al repo — solo su índice.

## 6. Arranque
- [ ] Completá los huecos `[...]` en `prompts/PROMPT-ORQUESTADOR.md` y `prompts/PROMPT-ANALIZADOR-INICIAL.md`.
- [ ] Corré primero el ANALIZADOR-INICIAL (llena `docs/DESCOMPOSICION-INICIAL.md`).
- [ ] Después la sesión ORQUESTADOR: lee el puente, confirma entendimiento, arma el PLAN y delega.

## Doctrina que conviene no romper
- Topología estrella: los ejecutores hablan solo con el orquestador.
- commit=push atómico: trabajo no pusheado = trabajo que no existe (y frena la fila).
- El PLAN es la fuente única: una sesión fresca se pone al día leyendo el PLAN, no el historial de chat.
- Pilotá chico. Sumá roles cuando el volumen lo pida, no antes.
