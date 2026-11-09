# Paso 7 — HPrvIR42, rubros

Séptimo panel del asistente. Lista los rubros en los que el proveedor quiere inscribirse y exige al menos uno para seguir o para salir. Es el único panel del asistente con una rama propia para el modo `A`. Fuentes: rev2 §9 y §18, `HPrvIR42` en el XML y `hprvir42_impl.java`; existe además `hprvir42m_impl.java`.

## Objeto

- `HPrvIR42`, "Rubros en los que desea inscribirse", rotulado "PASO 7 de 11". [V · capas: código, diseño · ev: hprvir42_impl.java (texto 'PASO 7 de 11'); XPZ HPrvIR42 Form]
- Recibe `PrvPUSr` y `Modulo`. [V · capas: código, diseño · ev: hprvir42_impl.java e141G52 ('Volver'); XPZ HPrvIR42 Parm]
- Llama a `TPrvRub` (ventana emergente de alta y baja de rubro), a `PPrvIR62` y navega a `HPrvIR06`, `HPrvIR18`, `HPrvIR41` y `HPrvIR39`. [V · capas: código, diseño · ev: hprvir42_impl.java e111G52 ('Agregar'), e121G52 ('Siguiente'), e131G52 ('Anterior'), e141G52 ('Volver'); XPZ HPrvIR42 Events]
- `HPrvIR42m` es una variante de solo consulta: lista los rubros del proveedor (`PrvRub`) y tiene solo el botón Volver, sin alta, baja ni validación. No está en el export; la referencia `hnupro16m_impl.java`, que está fuera de la familia del módulo, la menciona. No forma parte del asistente. [V · capas: código · ev: hprvir42m_impl.java e1222R2 (Start), e1122R2 ('Volver'), e1322R2 (Load); hnupro16m_impl.java]

## Datos que pide

El panel muestra la grilla de rubros y delega el alta a `TPrvRub`.

- Grilla con número de rubro (`PrvRubNro`), subrubro (`PrvRubSubRub`), bien o servicio (`PrvRubBsSrv`, combo) y descripción (`PrvRubDsc`), más el ícono Eliminar. [V · capas: código, diseño · ev: hprvir42_impl.java e121G52 ('Siguiente'), e161G52 (Load); XPZ HPrvIR42 Form]
- Agregar vacía número, subrubro y bien o servicio y abre `TPrvRub` en modo `INS`. [V · capas: código, diseño · ev: hprvir42_impl.java e111G52 ('Agregar'); XPZ HPrvIR42 Events 'Agregar']
- Eliminar usa el rubro seleccionado en la grilla y abre `TPrvRub` en modo `DLT`. No existe el modo `UPD` en este panel: un rubro no se modifica, se borra y se vuelve a agregar. [V · capas: código, diseño · ev: hprvir42_impl.java e171G52 ('Eliminar'); XPZ HPrvIR42 Events 'Eliminar']
- Tipo de persona (`PrvObs`) y categoría (`PrvCat`) se leen con `PPrvIR62` en Start. [V · capas: código, diseño · ev: hprvir42_impl.java e151G52 (Start); XPZ HPrvIR42 Events Start]

## Validaciones

Tabla de reglas del panel. Ids R-225 a R-236.

| Regla | Qué exige o hace el sistema |
|---|---|
| **R-225** | Para pasar al paso 8 hay que tener al menos un rubro; si no, "Debe ingresar por lo menos un rubro para poder continuar." [V · capas: código, diseño · ev: hprvir42_impl.java e121G52 ('Siguiente'); XPZ HPrvIR42 Events 'Siguiente'; rev2 §9 · clase: esencial] |
| **R-226** | Volver exige el mismo mínimo de un rubro, con el mismo mensaje, antes de salir. El conteo está escrito dos veces, una en Siguiente y otra en Volver. [V · capas: código, diseño · ev: hprvir42_impl.java e141G52 ('Volver'); XPZ HPrvIR42 Events 'Volver'; rev2 §9 · clase: esencial] |
| **R-227** | Eliminar sin rubro seleccionado muestra "Por favor seleccione el rubro a eliminar haciendo clic sobre el que desea eliminar (la línea seleccionada cambiará de color)". [V · capas: código, diseño · ev: hprvir42_impl.java e171G52 ('Eliminar'); XPZ HPrvIR42 Events 'Eliminar'; rev2 §9 · clase: esencial] |
| **R-228** | Eliminar el último rubro no se bloquea en el panel: el mínimo se controla recién al pulsar Siguiente o Volver (R-225, R-226). [V · capas: código, diseño · ev: hprvir42_impl.java e171G52 ('Eliminar'), e121G52 ('Siguiente'); XPZ HPrvIR42 Events 'Eliminar' · clase: esencial] |
| **R-229** | Anterior elige por tipo de persona: jurídica (`PrvObs` = 1) vuelve a `HPrvIR18` (paso 6), física a `HPrvIR41` (paso 5). Es el espejo de la bifurcación del paso 5 (R-202). [V · capas: código, diseño · ev: hprvir42_impl.java e131G52 ('Anterior'); XPZ HPrvIR42 Events 'Anterior'; rev2 §9 · clase: esencial] |
| **R-230** | Volver en modo `A` devuelve `Modulo` al llamador; en cualquier otro modo llama a `HPrvIR39`. Es la única rama explícita contra `A` en todo el asistente. Clase por defecto: no se sabe si el comportamiento distinto de `A` responde a una norma. [V · capas: código, diseño · ev: hprvir42_impl.java e141G52 ('Volver'); XPZ HPrvIR42 Events 'Volver'; rev2 §9 y §18 · clase: esencial] |
| **R-231** | La llamada de retorno a administración `HPrvIR21(PrvPUSr)` está comentada en la rama `A` de 'Volver'. [S · capas: diseño · ev: XPZ HPrvIR42 Events 'Volver' (línea comentada); rev2 §9 · clase: accidente] |
| **R-232** | En modo `I` el panel oculta Volver y muestra los botones y el rótulo del asistente, con el título "Rubros en los que desea inscribirse"; en `P` y `A` muestra el bloque de actualización y el título "Trabajar con Rubros". [V · capas: código, diseño · ev: hprvir42_impl.java e151G52 (Start); XPZ HPrvIR42 Events Start; rev2 §18 · clase: esencial] |
| **R-233** | La asignación del enlace del ícono Eliminar a `TPrvRub.Link` y el modo `DLT` están comentadas en Load; el enlace funciona por el evento Eliminar. [S · capas: diseño · ev: XPZ HPrvIR42 Events Load (líneas comentadas) · clase: accidente] |
| **R-234** | Start copia el usuario de la sesión de administración (clave `usr`) a una variable que ningún evento usa después. [V · capas: código, diseño · ev: hprvir42_impl.java e151G52 (Start); XPZ HPrvIR42 Events Start · clase: accidente] |
| **R-235** | Los rubros se dan de alta en la ventana emergente `TPrvRub` en todos los modos y el panel se refresca después. [V · capas: código, diseño · ev: hprvir42_impl.java e111G52 ('Agregar'); XPZ HPrvIR42 Events 'Agregar' · clase: esencial] |
| **R-236** | El mínimo de un rubro vale para todos los tipos de persona y categorías: el conteo no mira `PrvCat` ni `PrvObs`. Clase por defecto. [V · capas: código, diseño · ev: hprvir42_impl.java e121G52 ('Siguiente'); XPZ HPrvIR42 Events 'Siguiente' · clase: esencial] |

## Condición de avance

- Siguiente avanza a `HPrvIR06` solo con al menos un rubro (R-225). [V · capas: código, diseño · ev: hprvir42_impl.java e121G52 ('Siguiente'); XPZ HPrvIR42 Events 'Siguiente']
- Anterior no valida y vuelve al paso 6 o al 5 según el tipo de persona (R-229). [V · capas: código, diseño · ev: hprvir42_impl.java e131G52 ('Anterior'); XPZ HPrvIR42 Events 'Anterior']
- Volver exige un rubro y sale a administración (`A`) o a `HPrvIR39` (R-226, R-230). [V · capas: código, diseño · ev: hprvir42_impl.java e141G52 ('Volver'); XPZ HPrvIR42 Events 'Volver']

## Capas

Capas: código, diseño; ejecución: todavía no observado (E4). No se consultó el manual (intención).

Las reglas R-231 y R-233 son solo de diseño: el Java generado no conserva los comentarios. El chequeo de versión (E1) está pendiente.
