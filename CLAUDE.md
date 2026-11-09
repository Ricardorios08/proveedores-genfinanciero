# Instrucciones del proyecto

Este proyecto trabaja con andamio. Este archivo solo clasifica y apunta: el contenido del proyecto vive en los archivos de abajo, no acá.

## Antes de cualquier pedido

1. Leé `contexto-vivo.md`: qué está en curso y qué quedó pendiente.
2. Si el pedido toca cómo es el sistema, mirá `conocimiento/mapa/`.
3. Si el pedido contradice algo de `conocimiento/decisiones.md`, decilo antes de hacer nada.

## Clasificá el pedido

| Si el pedido es… | Hacés |
|---|---|
| Una pregunta, una lectura, una explicación | Respondés. Sin unidad de trabajo |
| Un cambio cuyo criterio de éxito entra en una frase y toca un solo lugar | Lo hacés directo. Sin unidad de trabajo |
| Cualquier otro cambio | Sugerís `/proponer <descripción>` y no empezás a cambiar nada |

Ante la duda entre las dos últimas, preguntá.

### Cuándo no usar el ciclo

Si el criterio de éxito entra en una frase y toca un solo lugar, no necesita unidad de trabajo: el ciclo cuesta más que el cambio. Ejemplos del tipo: corregir un error de tipeo, renombrar una variable local, actualizar un valor en un único archivo de configuración.

Todo lo demás pasa por el ciclo: `/proponer` → `/aplicar` → `/verificar` → `/archivar`.

## Dónde está cada cosa

| Archivo | Qué es |
|---|---|
| `.claude/andamio/declaracion.yml` | Cómo trabaja este proyecto: tipo, ejecutores y ámbitos, lo protegido, qué cierra una tarea, credenciales (solo nombres) |
| `.claude/andamio/plantillas/` | Bases de propuesta, diseño y tareas de una unidad |
| `contexto-vivo.md` | Estado actual. Se sobrescribe, no se acumula |
| `conocimiento/mapa/` | Cómo es el sistema, con estado epistémico por afirmación |
| `conocimiento/decisiones.md` | Decisiones vigentes, con fecha de revisión |
| `conocimiento/patrones.md` | Formas de hacer que se repiten en este proyecto |
| `conocimiento/lecciones.md` | Lo aprendido, con la situación que lo enseñó |
| `conocimiento/candidatas.md` | Lecciones que podrían servir fuera de este proyecto |
| `trabajo/en-curso/<unidad>/` | Unidades abiertas |
| `trabajo/archivo/<unidad>/` | Unidades cerradas. **Inmutables** |

## Reglas que no dependen del pedido

- **Credenciales:** nunca pidas, leas, imprimas ni escribas un valor. Solo nombres, los de la declaración.
- **Lo protegido** (ver la declaración) no se toca sin que una persona lo pida explícitamente.
- **`trabajo/archivo/`** no se modifica. Si una unidad archivada necesita cambios, se abre una nueva que la cite.
- **Commits** con rutas explícitas. El push lo hace una persona.
- Si el guardián de terminal frena un comando, leé el motivo: dice qué hacer en su lugar.
