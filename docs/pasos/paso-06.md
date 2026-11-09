# Paso 6 — HPrvIR18, estado de situación patrimonial

Sexto panel del asistente. Solo lo recorre la persona jurídica (el paso 5 manda a la física directo al paso 7). Muestra los dos últimos ejercicios cerrados y permite agregarlos, modificarlos y eliminarlos. **El panel no valida nada: la validación del último balance está comentada** y Siguiente avanza siempre. Fuentes: rev2 §8, `HPrvIR18` en el XML y `hprvir18_impl.java`.

## Objeto

- `HPrvIR18`, "Estado de Situación Patrimonial o Manifestación de Bienes", rotulado "PASO 6 de 11". [V · capas: código, diseño · ev: hprvir18_impl.java (texto 'PASO 6 de 11'); XPZ HPrvIR18 Form]
- Recibe `PrvPUSr` y `Modulo`. [V · capas: código, diseño · ev: hprvir18_impl.java e17AC2 ('Volver'); XPZ HPrvIR18 Parm]
- Llama a `TPrvESP` (ventana emergente de ejercicios), `PPrvIR23` (datos de los dos ejercicios) y `PPrvIR62` (categoría y tipo de persona). Navega a `HPrvIR41` y `HPrvIR42`. [V · capas: código, diseño · ev: hprvir18_impl.java e11AC2 (Start), e12AC2 ('Agregar'), e15AC2 ('Siguiente'), e16AC2 ('Anterior'); XPZ HPrvIR18 Events]
- `RPrvIR63` (fecha del último balance exigible) está en el export pero solo lo invoca el bloque comentado de 'Siguiente'. [S · capas: diseño · ev: XPZ HPrvIR18 Events 'Siguiente' (bloque comentado); sin llamada en hprvir18_impl.java]

## Datos que pide

El panel no pide campos: los carga `PPrvIR23` y se editan en `TPrvESP`. Muestra dos columnas, "Último Ejercicio" y "Ejercicio Anterior".

- Por ejercicio: fecha de cierre (`EjerCer1`, `EjerCer2`), activo corriente, no corriente y total, pasivo corriente, no corriente y total, patrimonio neto, total pasivo más patrimonio neto, ventas netas y resultado del ejercicio. [V · capas: código, diseño · ev: hprvir18_impl.java e11AC2 (Start), e18AC2 (Refresh); XPZ HPrvIR18 Events Start, Refresh]
- Por ejercicio: nombre y matrícula del profesional certificante y fecha de legalización en el consejo profesional. [V · capas: código, diseño · ev: hprvir18_impl.java e18AC2 (Refresh); XPZ HPrvIR18 Events Refresh]
- Un selector `modi` (Modificar/Eliminar) elige sobre cuál de los dos ejercicios actúan Modificar y Eliminar: 1 el último, 0 el anterior. [V · capas: código, diseño · ev: hprvir18_impl.java e13AC2 ('Modificar'), e14AC2 ('Eliminar'); XPZ HPrvIR18 Events 'Modificar', 'Eliminar']
- Categoría (`PrvCat`) y tipo de persona (`PrvObs`) se leen con `PPrvIR62` en Start y en Refresh. [V · capas: código, diseño · ev: hprvir18_impl.java e11AC2 (Start), e18AC2 (Refresh); XPZ HPrvIR18 Events Start, Refresh]

## Validaciones

Tabla de reglas del panel. Ids R-213 a R-224.

| Regla | Qué exige o hace el sistema |
|---|---|
| **R-213** | Siguiente avanza siempre a `HPrvIR42`, sin condición: no exige ejercicio cargado, ni balance, ni categoría. Es lo único activo del evento. [D · capas: código, diseño, intención · ev: hprvir18_impl.java e15AC2 ('Siguiente'); XPZ HPrvIR18 Events 'Siguiente'; rev2 §8; manual Registro p. 15 · clase: accidente · ≠ D-04] |
| **R-214** | Validación comentada: si la categoría es `1` y la persona es jurídica, exigía el último balance cerrado consultando `RPrvIR63` y su `FlagBalance`; si faltaba, mostraba "Debe ingresar el último Balance Cerrado, con fecha ... para poder continuar." El Java generado no la contiene. [S · capas: diseño · ev: XPZ HPrvIR18 Events 'Siguiente' (bloque comentado); rev2 §8; ausente en hprvir18_impl.java e15AC2 ('Siguiente') · clase: accidente] |
| **R-215** | Validación comentada: antes de la anterior, exigía al menos un ejercicio cargado (o categoría `2`); si no, "Debe ingresar al menos los datos del último ejercicio para poder continuar." Para persona física nunca se exigía. [S · capas: diseño · ev: XPZ HPrvIR18 Events 'Siguiente' (bloque comentado); rev2 §8; ausente en hprvir18_impl.java e15AC2 ('Siguiente') · clase: accidente] |
| **R-216** | El texto "La carga de la información de Situación Patrimonial es Obligatoria en caso que haya seleccionado inscribirse en la Categoría 1" se oculta en Start en todos los modos, y ningún código activo la exige (ver R-213). [V · capas: código, diseño · ev: hprvir18_impl.java e11AC2 (Start); XPZ HPrvIR18 Events Start · clase: accidente] |
| **R-217** | Modificar abre `TPrvESP` en modo `UPD` sobre el ejercicio que indica el selector; si ese ejercicio no está cargado muestra "No existe el ejercicio por favor ingrese datos para el mismo haciendo clic en Agregar". [V · capas: código, diseño · ev: hprvir18_impl.java e13AC2 ('Modificar'); XPZ HPrvIR18 Events 'Modificar' · clase: esencial] |
| **R-218** | Agregar abre `TPrvESP` en modo `INS` con la fecha de ejercicio vacía y refresca el panel. [V · capas: código, diseño · ev: hprvir18_impl.java e12AC2 ('Agregar'); XPZ HPrvIR18 Events 'Agregar' · clase: esencial] |
| **R-219** | Eliminar abre `TPrvESP` en modo `DLT` sobre el ejercicio del selector y después vuelve a llamar a `HPrvIR18` para recargarlo. No pide confirmación en el panel y no comprueba que el ejercicio exista. Clase por defecto: la evidencia no dice si la confirmación está en `TPrvESP`. [V · capas: código, diseño · ev: hprvir18_impl.java e14AC2 ('Eliminar'); XPZ HPrvIR18 Events 'Eliminar' · clase: esencial] |
| **R-220** | En modo `I` el panel muestra los botones y la descripción del asistente y oculta el bloque de actualización; en `P` y `A` hace lo contrario y oculta el rótulo del paso. [V · capas: código, diseño · ev: hprvir18_impl.java e11AC2 (Start); XPZ HPrvIR18 Events Start; rev2 §18 · clase: esencial] |
| **R-221** | Anterior vuelve siempre a `HPrvIR41`. Es coherente porque al paso 6 solo llega la persona jurídica; no mira el tipo de persona. [V · capas: código, diseño · ev: hprvir18_impl.java e16AC2 ('Anterior'); XPZ HPrvIR18 Events 'Anterior' · clase: esencial] |
| **R-222** | Volver no mira el modo: siempre devuelve `PrvPUSr` y `Modulo` al llamador. En los otros paneles `P` va a `HPrvIR39`; acá no. Clase por defecto. [V · capas: código, diseño · ev: hprvir18_impl.java e17AC2 ('Volver'); XPZ HPrvIR18 Events 'Volver'; rev2 §18 · clase: esencial] |
| **R-223** | La llamada de retorno a administración `HPrvIR21(PrvPUSr)` está comentada en 'Volver'; quedó el `Return`. [S · capas: diseño · ev: XPZ HPrvIR18 Events 'Volver' (línea comentada); rev2 §18.1 · clase: accidente] |
| **R-224** | Start y Refresh consultan `PPrvIR62` (categoría y tipo de persona) pero ningún evento activo usa esos valores: solo los usaba el bloque comentado. [V · capas: código, diseño · ev: hprvir18_impl.java e11AC2 (Start), e18AC2 (Refresh), e15AC2 ('Siguiente'); XPZ HPrvIR18 Events Start · clase: accidente] |

## Condición de avance

- Siguiente no condiciona nada: el paso 6 se atraviesa vacío (R-213). [V · capas: código, diseño · ev: hprvir18_impl.java e15AC2 ('Siguiente'); XPZ HPrvIR18 Events 'Siguiente']
- Anterior vuelve al paso 5 sin validar (R-221). [V · capas: código, diseño · ev: hprvir18_impl.java e16AC2 ('Anterior'); XPZ HPrvIR18 Events 'Anterior']
- El texto de pantalla dice que la carga es obligatoria en categoría 1; el código activo no la exige. Se trata como accidente (R-213, R-216) y no como discrepancia, porque el texto está oculto y la validación quedó comentada a propósito. [V · capas: código, diseño · ev: hprvir18_impl.java e11AC2 (Start), e15AC2 ('Siguiente'); XPZ HPrvIR18 Events 'Siguiente' · clase: accidente]

## Capas

Capas: código, diseño; ejecución: todavía no observado (E4). No se consultó el manual (intención).

Las reglas R-214, R-215 y R-223 son solo de diseño: el Java generado no conserva los comentarios. El chequeo de versión (E1) está pendiente.
