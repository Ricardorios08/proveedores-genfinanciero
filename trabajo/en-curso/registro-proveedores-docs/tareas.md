# registro-proveedores-docs — Tareas

**Estado:** aprobado por responsable del proyecto el 2026-10-23 (versión 2, con la enmienda 1 y la revisión independiente del 2026-10-23)
**Fuente:** `diseno.md`

Cada tarea pertenece a un solo ámbito de la declaración y tiene **un** criterio de éxito. Las tareas de los grupos A a H son del ejecutor `docs`, ámbito `docs/`. Hay **dos excepciones**, que hace el coordinador de la unidad (la sesión principal) o el responsable, porque caen fuera de `docs/`:

- **X1:** la bitácora de altas, en la unidad.
- **X2:** la consulta a Emanuel.
- **X3:** las filas de la bitácora y las capturas de E3 a E6. El ejecutor `docs` informa los datos y el coordinador los escribe.

Abreviaturas: **rev2** = `../genfin-gx-extraido/peer/14-reglas-rev2.md` · **XML** = `../genfin-gx-extraido/xpz/GENFin-RegProv.xml` · **fin** = `../genfin-gx-extraido/fin/`.

## Grupo A — Convenciones, herramientas y esqueleto — ejecutor `docs`, ámbito `docs`

Depende de: ninguno · En paralelo con: ninguno (todo lo demás lo usa)

| ID | Tarea | Criterio de éxito |
|---|---|---|
| A1 | Escribir `docs/convenciones.md`: la tabla de estado calculado, la gramática del bloque, las clases, las citas y dos ejemplos reales sacados de fin | Los dos ejemplos pasan `verificar.py` (A5) y una variante de cada uno con el estado cambiado no lo pasa |
| A2 | Escribir `docs/herramientas/contar-xpz.py`, con el control 119/194 sobre los hijos directos de `<Objects>` y de `<Attributes>` | Sobre el XML real termina con 0, y sobre `fixtures/xpz-118.xml` termina distinto de 0 |
| A3 | Escribir `docs/herramientas/dependencias-xpz.py`, con columnas activas y comentadas y sus cuatro controles | Sobre el XML real termina con 0 y lista `TPrvESP` en activas y `RPrvIR63` en comentadas |
| A4 | Escribir el fixture sintético de `dependencias-xpz.py`, en el que cada control se rompe por separado | Corrido contra cada variante, el script falla exactamente en el control roto |
| A5 | Escribir `docs/herramientas/verificar.py`, con sus seis chequeos | Sobre `fixtures/verificar/` reporta exactamente los casos que deben fallar y ninguno de los que deben pasar |
| A6 | Crear los esqueletos de `pantallas.md`, `flujos.md`, `discrepancias.md`, `decisiones-rediseno.md`, `features.csv` y `README.md` | `verificar.py` corre sobre `docs/` sin errores de estructura |

## Grupo B — Inventarios — ejecutor `docs`, ámbito `docs`

Depende de: A · En paralelo con: C, D, E

| ID | Tarea | Criterio de éxito |
|---|---|---|
| B1 | `docs/inventario-objetos.md`, con la salida y el comando de `contar-xpz.py` | Volver a correr el comando da los mismos números |
| B2 | `docs/dependencias-faltantes.md`, con la salida de `dependencias-xpz.py` | Cada objeto de la §16 de la rev2 figura en activas o en comentadas, o tiene una nota que explica su ausencia |
| B3 | Columna `fuente` de cada faltante, buscada en fin | Ningún faltante queda sin `fuente` |
| B4 | Escribir `docs/herramientas/universo-fin.py` y `docs/universo-modulo.md`, con la frontera del diseño | Sobre fin termina con 0, con `hprvir21` y `pprvir50` dentro, `loginprov` en entradas externas y `pprvsendmail` en el borde *(ajustado en B4)* |

## Grupo E — Ejecución en test — ejecutor `docs`, ámbito `docs` (salvo X1 y X2)

Depende de: A · En paralelo con: B, C, D

Observación, sin altas:

| ID | Tarea | Criterio de éxito |
|---|---|---|
| E1 | Chequeo de versión por objeto: para cada panel de los 11 pasos y para `popro001`, buscar un texto o una condición que difiera entre el XPZ y el Java, y ver cuál muestra test | `convenciones.md` tiene una tabla con una fila por objeto (coincide con Java, coincide con XPZ, o no discrimina) y la fecha |
| E2 | Observar las pantallas de administración (`popro001`, `hprvir25`, `31`, `40`, `56`) sin operar | Cada una tiene su fila `Snn` en `pantallas.md`, con fecha |

Altas (esperan las preguntas abiertas de `diseno.md`):

| ID | Tarea | Criterio de éxito |
|---|---|---|
| X1 | *(Coordinador.)* Crear `trabajo/en-curso/registro-proveedores-docs/altas-prueba.md` | Existe, con las columnas usuario, CUIT, hora, resultado y baja, y sin filas |
| E3 | Antes de la primera alta: probar el CUIT inventado en el paso 1 y revisar los destinatarios de los mensajes internos | La bitácora registra que `PPrvIR02` dio "no existe" y que ningún mensaje interno le llega a una persona |
| E4 | Primera alta completa, de los 11 pasos | La bitácora tiene la fila, y cada paso tiene su `Snn` en `pantallas.md` |
| X2 | *(Coordinador o responsable.)* Pedirle a Emanuel que confirme que el usuario de E4 existe en GTF y no en producción, y que la base de GEN de test es independiente. **Es informativa: no bloquea E5 ni E6** | La consulta está enviada y anotada en la bitácora. Si la respuesta indica producción, se paran las altas |
| E5 | Llevar los usuarios de prueba a cada estado alcanzable operando la administración (`hprvir25`, `hprvir40`), solo sobre `zzprueba…`, y recorrer la retoma y el modo `P` en cada uno | Cada estado recorrido tiene su flujo en `flujos.md` con los clicks contados |
| E6 | Dar de baja los usuarios de prueba, o dejar escrito por qué no se puede | Cada fila de la bitácora tiene la columna `baja` completa |

## Grupo C — Los 11 pasos — ejecutor `docs`, ámbito `docs`

Depende de: A · En paralelo con: B, D, E

Cada tarea parte de la sección de la rev2, cruza cada regla con el `_impl.java` del panel (los 11 tienen Java) y asigna una clase a cada regla. El criterio es siempre el mismo: **`verificar.py` pasa sobre el archivo**. Eso incluye las secciones obligatorias, el estado calculado y la clase de cada `R-nn`.

| ID | Archivo | Objeto (rev2) |
|---|---|---|
| C1 | `paso-01.md` | `HPrvIR02` (§3) |
| C2 | `paso-02.md` | `HPrvIr07` (§4) |
| C3 | `paso-03.md` | `TPrvInsRP` (§5) |
| C4 | `paso-04.md` | `HPrvIR17m` (§6) |
| C5 | `paso-05.md` | `HPrvIR41` (§7) |
| C6 | `paso-06.md` | `HPrvIR18` (§8); la validación comentada entra como `R-nn` de clase accidente |
| C7 | `paso-07.md` | `HPrvIR42` (§9) |
| C8 | `paso-08.md` | `HPrvIR06` (§10) |
| C9 | `paso-09.md` | `HPrvIR22` (§11) |
| C10 | `paso-10.md` | `HPrvIR10` (§12) |
| C11 | `paso-11.md` | `HPrvIR09` (§13) |
| C12 | Volver sobre los 11 pasos con lo observado en E1, E4 y E5 | `verificar.py` pasa y la línea `Capas:` de cada paso incluye `ejecución` donde se observó |

C12 depende de E1, y de E4 y E5 si se hicieron. Si las altas no llegan a hacerse, C12 solo incorpora E1.

## Grupo D — Transversales — ejecutor `docs`, ámbito `docs`

Depende de: A, y D1 también de E2 · En paralelo con: B, C, E

| ID | Tarea | Criterio de éxito |
|---|---|---|
| D1 | `docs/modos.md`: el modo `A` por la cadena `popro001 → hprvir25/40 → hprvir21`, y el modo `P` por `hprvir39 → hprvir52` | Cada panel con modo `P` o `A` tiene su fila de diferencias, y `verificar.py` pasa |
| D2 | `docs/modelo-datos.md`: entidades, atributos y tipos | Cada atributo tiene tipo o está en **S** con motivo |
| D3 | `docs/modelo-datos.md`: tabla y clave de cada entidad | Las 6 hijas tienen tabla y clave en **V**, con su `DELETE ... WHERE` citado |
| D4 | `docs/estados.md`, como transiciones | Cada valor del flag de `PPrvIR02` y de `PrvPHabCS` aparece en una transición, o está en **S** con motivo |
| D5 | `docs/integraciones.md`, con la confirmación de PostgreSQL en `GXcfg.java` | Cada recurso `ACPS*RESOURCE` que usa el módulo tiene una fila |
| D6 | `docs/mensajes.md`, con el universo de `universo-modulo.md` (B4) más las entradas externas que disparan correos | Cada llamador del módulo a `PPrvSendMsg`, `PPrvSendMail` o `PPrvIR99` tiene su fila |
| D7 | `docs/configuracion.md` | Cada atributo de sistema y cada parámetro leídos por el módulo tienen su fila, y ningún valor figura |
| D8 | `docs/cliente-vs-producto.md` | Cada texto de OSEP fijo en el código tiene su fila y su `R-nn` de clase accidente |
| D9 | `docs/seguridad.md`, con la contraseña inicial | El hallazgo cita el Java y tiene su `R-nn` |

## Grupo F — Artefactos de recon — ejecutor `docs`, ámbito `docs`

Depende de: C1–C11, D, E1 y E2. E4 y E5 aportan, pero no bloquean · En paralelo con: ninguno

| ID | Tarea | Criterio de éxito |
|---|---|---|
| F1 | Completar `pantallas.md` | Cada panel de `universo-modulo.md` tiene pantalla o motivo de exclusión |
| F2 | Completar `flujos.md`: alta, modificación en modo `P`, lo que se pueda del modo `A`, y una retoma por cada uno de los 10 estados de `PPrvIR02` | Los 10 estados tienen su fila de retoma, marcada "recorrida" o "solo desde el código" |
| F3 | Completar `features.csv`, con `decision = pendiente` en todas las filas | `verificar.py` pasa sobre el CSV |
| F4 | Cruzar `features.csv` con las reglas de C y D | Cada `R-nn` pertenece a alguna fila del CSV |

## Grupo H — Rediseño — ejecutor `docs`, ámbito `docs`

Depende de: C12, D y F · En paralelo con: ninguno

| ID | Tarea | Criterio de éxito |
|---|---|---|
| H1 | `docs/discrepancias.md`: revalidar las tres conocidas y cargar las `D-nn` que surgieron en C, D y E | Cada marca `≠ D-nn` de `docs/` tiene su entrada, y cada entrada tiene sus dos lados citados |
| H2 | `docs/decisiones-rediseno.md`: una `DR-nn` por cada regla parche o accidente y por cada `D-nn`, más las de confirmación de las esenciales por defecto (agrupadas por paso) y la tabla "Se mantiene" de las esenciales con evidencia, ordenadas por impacto en el flujo | `verificar.py` (chequeo 5) no reporta ninguna regla ni discrepancia sin su `DR-nn` |
| H3 | `docs/mapa-flujos.md`: el diagrama Mermaid, con los puntos de dolor enlazados a sus `DR-nn` | Cada `DR-nn` que cambia la secuencia de pasos aparece en el diagrama |
| H4 | Aviso de calidad de la clasificación | Si más de un tercio de las reglas es "esencial por defecto", `decisiones-rediseno.md` lo dice en su encabezado |

## Grupo G — Cierre — ejecutor `docs`, ámbito `docs`

Depende de: B y H · En paralelo con: ninguno

| ID | Tarea | Criterio de éxito |
|---|---|---|
| G1 | Columna `cobertura` de `universo-modulo.md` (CA3) | Ningún objeto queda sin clasificar |
| G2 | `docs/README.md`, en orden de lectura: mapa, decisiones y después el respaldo | `verificar.py` (chequeo 1) no reporta diferencias |
| G3 | Corrida final de `verificar.py` sobre todo `docs/` | Termina con 0 |

Después de G3, el responsable lee `mapa-flujos.md` y `decisiones-rediseno.md` y confirma los criterios. La declaración no define `cierre`. Sus decisiones van al campo `decisión del responsable` de cada `DR-nn` y a la columna `decision` del CSV, y pueden llenarse después de cerrar la unidad.

## Orden

1. **A.**
2. **B, C1–C11, D y E1–E2**, en paralelo. D1 espera a E2.
3. **Las altas (X1, E3–E6)**, cuando estén las respuestas. No bloquean nada.
4. **C12**, después de E1, y de las altas si se hicieron.
5. **F.**
6. **H.**
7. **G.**

## Preguntas abiertas

- Las de `diseno.md`: la casilla de correo y si hay un rango de CUIT de prueba. Frenan X1 y E3–E6, nada más.
</content>
</invoke>
<invoke name="mcp__ccd_turn__update_plan">
<parameter name="advance">true