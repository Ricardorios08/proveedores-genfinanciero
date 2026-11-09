# Bitácora de altas de prueba

Registro de cada alta y cada operación de administración hecha en el portal de **test** (`GENFinancieroGTF`), según las condiciones de la pregunta 5 de la propuesta y la sección "Capa de ejecución" del diseño. La lleva el coordinador (tarea X1).

**Reglas:**
- El usuario empieza con `zzprueba` y sigue un número. La razón social dice "PRUEBA".
- El correo es la casilla sandbox del responsable. La dirección no se escribe en el repo. En test la cola de correo está desactivada.
- La administración se opera **solo** sobre proveedores `zzprueba…`, confirmando en pantalla antes de cada operación.
- **CUIT:** no hay rango de prueba acordado. Se usa un CUIT inventado con dígito válido, con prefijo 20 y número en el rango de 99 millones, que hoy no asigna el DNI. Antes de usarlo se prueba en el paso 1: tiene que dar "no existe" (flag `F`). Queda un riesgo residual, porque no se puede garantizar que no pertenezca a nadie.
- **Sin usuario administrador general** (`PrvPAdminGral`): `hprvir40` no se puede operar.

## Verificación previa (E3)

| Fecha y hora | Control | Resultado |
|---|---|---|
| 2026-10-23 | CUIT 20-99123456-0 en el paso 1 (`hprvir02`) | **No existe.** El paso 2 recibió `band = 0`, `CatRec = 9` y `Prove` vacío (leído del `GXState` de la página), que es el camino del flag `F` (R-111). No se grabó nada: el paso 1 y el Start del paso 2 solo leen. |
| 2026-10-23 | Destinatarios de mensajes internos | Según `docs/mensajes.md` (D6), ningún destinatario fijo es una persona: todos salen del propio proveedor. `pcmsg001` lo crea `CADMIN` y lo recibe el usuario del proveedor. **Queda abierto:** qué hace Services de test con los 7 canales, cuya configuración no está en el repo. La cola de correo de test está desactivada (Emanuel, 2026-10-23). |
| 2026-10-23 | Cómo se operan los botones | Los botones GeneXus (`data-gx-evt`) no responden al click de ratón de `agent-browser`. Se disparan con `.click()` por JavaScript. Un click sin efecto no prueba nada: hay que confirmar con la navegación o con el `GXState`. |

| 2026-10-23 20:10 | Códigos geográficos válidos en test | Leídos de los nomencladores `wwtprovincia` y `wwtlocalidad`, solo consulta: país 1 (ARGENTINA), provincia 1 (TIERRA DEL FUEGO), localidad 1 (USHUAIA). En el popup de domicilio la provincia no se valida al salir del campo, solo el país. `promptloc` filtra por la provincia que trae el popup: con 0 no devuelve nada. |

## Altas y operaciones

| Fecha y hora | Usuario | CUIT | Operación | Resultado | Baja |
|---|---|---|---|---|---|
| 2026-10-23 19:34 | `ZZPRUEBA01` (cargado en minúsculas; el sistema lo pasa a mayúsculas) | 20-99123456-0 | Paso 2: elección de usuario | Avanzó al paso 3 en modo `INS` | — |
| 2026-10-23 19:35 | `ZZPRUEBA01` | 20-99123456-0 | Paso 3: datos inventados (razón social "PRUEBA ZZPRUEBA01 DATOS INVENTADOS", persona física, casilla sandbox del responsable) | **Grabó**: avanzó directo al paso 5 (Domicilios), saltando el 4 por ser persona física. Según el código, a esta altura `TPrvInsRP` insertó el `PrvPerfil` y `TPrvInsRP0001` creó el usuario en Services de test (sin confirmar del lado de Services) | pendiente (E6) |
| 2026-10-23 19:40–20:05 | `ZZPRUEBA01` | 20-99123456-0 | Paso 5: alta de domicilio legal (popup `TPrvDom`) | **Sin grabar, alta en pausa.** País = 1 (ARGENTINA) se valida bien. Provincia y localidad: no se encontró un código válido. Ningún código probado (7, 12, 13, 50) trae descripción, y `promptloc` no devuelve localidades. El popup se canceló: no se grabó ningún domicilio. El proveedor queda con el perfil creado en el paso 3 y sin domicilios | pendiente (E6) |
