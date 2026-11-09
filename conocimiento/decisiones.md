# Decisiones

Decisiones vigentes del proyecto. Las escribe `/archivar` cuando una unidad deja una, o una persona. Una decisión que se reemplaza no se borra: se marca como reemplazada y se cita la nueva.

## Formato

```
## D-<número> — <título>

**Fecha:** <fecha> · **Revisar el:** <fecha de revisión> · **Marca:** impuesta | escrita
**Unidad:** <unidad de origen> · **Estado:** vigente | reemplazada por D-<número>

**Decisión:** <qué se decidió, en una o dos frases>
**Por qué:** <el motivo, con lo que se descartó>
**Cómo se cumple:** <si es impuesta: qué la hace cumplir (una configuración, un hook, una prueba); si es escrita: quién o qué tiene que leerla>
```

- **Fecha de revisión:** cuándo hay que volver a mirarla, aunque nada haya fallado. Toda decisión tiene una.
- **Impuesta:** algo la hace cumplir sin depender de que alguien la lea.
- **Escrita:** depende de que alguien la lea y la respete. Si una escrita se viola seguido, es candidata a volverse impuesta.

## Decisiones

## D-1 — Frontend de la fase 2: React 18 + MUI con el design system de GEN Financiero

**Fecha:** 2026-10-23 · **Revisar el:** 2027-01-23, o antes, al abrir la primera unidad de la fase 2 · **Marca:** escrita
**Unidad:** ninguna (la tomó el responsable del proyecto) · **Estado:** vigente

**Decisión:** el frontend de la fase 2 (`app/`) se construye con React 18 y MUI, usando el design system de GEN Financiero como fuente de verdad visual. Los colores, sombras, radios, espaciados y duraciones salen de sus tokens, y los temas `lightTheme` y `darkTheme` se arman desde `tokens.json`.
**Por qué:** el design system de NómadeSoft para GEN Financiero está hecho para React 18 + MUI. Además, reutiliza 14 componentes que ya existen en GENProcesos. Usar otra librería de componentes obligaría a reescribir esos 14 y a mapear los tokens a mano. No se evaluaron alternativas: viene con el design system.
**Cómo se cumple:** la lee quien abra una unidad de la fase 2. El paquete está fuera del repo, en `../genfin-gx-extraido/design-system/GEN-Financiero-design-system/`, y se entra por `AGENTE.md`. Para reutilizar los componentes heredados hace falta acceso al repo de GENProcesos (`src/components/...`). Puede volverse impuesta con un lint que rechace colores en hex fuera de los tokens.
