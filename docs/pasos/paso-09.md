# Paso 9: cuentas bancarias (HPrvIR22)

## Objeto

`HPrvIR22` es la pantalla "Cuentas Bancarias" del asistente de alta, rotulada "PASO 9 de 11". Recibe el usuario del proveedor y el modo de operación (`I` inscripción, `P` proveedor existente, `A` administración). Antes del paso 9 estaba el paso de apoderados (`HPrvIR20`), que ya no forma parte del flujo; el código lo dice en un comentario de la llamada.

La pantalla lista las cuentas ya cargadas en una grilla y delega el alta, la modificación y la baja en el popup `TPrvBco`. Desde acá se llega a `HPrvIR10` (siguiente), a `HPrvIR06` o `HPrvIR02` (anterior) y, en modo `P`, a `HPrvIR39` (volver). El modo `A` lo consume el código, pero su llamador (`HPrvIR21`) no es parte de las fuentes de este paso.

Fuentes: rev2 §11 y §17, XPZ `HPrvIR22`, Java `hprvir22_impl.java`.

## Datos que pide

La pantalla no tiene campos de entrada propios: las cuentas se cargan en el popup `TPrvBco`, que queda fuera de este paso. La grilla muestra estas columnas por cuenta:

| Dato | Qué muestra | Bloque |
|---|---|---|
| Moneda y símbolo | Moneda de la cuenta y su símbolo | [V · capas: código, diseño · ev: hprvir22_impl.java sendrow_632; XPZ HPrvIR22 Form] |
| Tipo de cuenta | Identificador del tipo de cuenta bancaria | [V · capas: código, diseño · ev: hprvir22_impl.java sendrow_632; XPZ HPrvIR22 Form] |
| Número de cuenta | Número de cuenta | [V · capas: código, diseño · ev: hprvir22_impl.java sendrow_632; XPZ HPrvIR22 Form] |
| CBU, bloques 1 y 2 | Las dos partes del CBU | [V · capas: código, diseño · ev: hprvir22_impl.java sendrow_632; XPZ HPrvIR22 Form] |
| Banco y sucursal | Número del banco y código de sucursal | [V · capas: código, diseño · ev: hprvir22_impl.java sendrow_632; XPZ HPrvIR22 Form] |
| Fecha de vigencia | Fecha de vigencia de la cuenta | [V · capas: código, diseño · ev: hprvir22_impl.java sendrow_632; XPZ HPrvIR22 Form] |
| Moneda de curso legal | Marca de si es la moneda de curso legal | [V · capas: código, diseño · ev: hprvir22_impl.java sendrow_632; XPZ HPrvIR22 Form] |

## Validaciones

- **R-301** Alta, modificación y baja de una cuenta se hacen en el popup `TPrvBco`, abierto con el modo `INS`, `UPD` o `DLT` según el botón; la pantalla se refresca al volver. [V · capas: código, diseño · ev: hprvir22_impl.java e1125M2 ('Agregar'), e1725M2 ('Modificar'), e1825M2 ('Eliminar'); XPZ HPrvIR22 Events 'Agregar', 'Modificar', 'Eliminar' · clase: esencial]
- **R-302** Si el atributo de sistema COMPRAS_OBLIGACTABCO vale 'S' y la grilla no tiene ninguna cuenta, 'Siguiente' no avanza y muestra "ERROR: Es OBLIGATORIO ingresar al menos una Cuenta Bancaria." Si el atributo no vale 'S', el paso avanza sin cuentas. Clase por defecto: la evidencia no alcanza para decir si la obligatoriedad es una norma general o un caso de un cliente; que sea configurable sugiere lo segundo. [D · capas: código, diseño, intención · ev: hprvir22_impl.java e1225M2 ('Siguiente'); XPZ HPrvIR22 Events 'Siguiente'; manual Registro p. 20 · clase: esencial · ≠ D-05]
- **R-303** La cantidad de cuentas que se compara con la obligatoriedad es la cantidad de filas de la grilla que llegan en el pedido, no una consulta aparte a la base. Clase por defecto. [V · capas: código, diseño · ev: hprvir22_impl.java S112 ('VALIDA'); XPZ HPrvIR22 Sub 'Valida' · clase: esencial]
- **R-304** El texto de ayuda depende del atributo COMPRAS_OBLIGACTABCO y no del modo: con 'S' se muestra "Es OBLIGATORIO el ingreso de al menos una Cuenta Bancaria." y con otro valor "De otro modo, presione en Siguiente para continuar." Hay dos juegos de textos, uno dentro del bloque del asistente (modo `I`) y otro dentro del bloque de actualización (otros modos), y en cada modo solo uno de los bloques es visible. La rev2 dice que los textos se invierten según el modo; ver D-302. [V · capas: código, diseño · ev: hprvir22_impl.java e1525M2 (Start); XPZ HPrvIR22 Events Start y Form (tablas wizdesc y UPDDsc) · clase: esencial]
- **R-305** En modo `I` se muestran los botones del asistente (anterior y siguiente) y el rótulo del paso, se oculta el bloque de actualización y el título es "Datos de Cuentas Bancarias". En los otros modos pasa al revés y el título es "Trabajar con Cuentas Bancarias". Clase por defecto. [V · capas: código, diseño · ev: hprvir22_impl.java e1525M2 (Start); XPZ HPrvIR22 Events Start · clase: esencial]
- **R-306** 'Siguiente', cuando valida, pasa a `HPrvIR10` con el usuario y el modo. [V · capas: código, diseño · ev: hprvir22_impl.java e1225M2 ('Siguiente'); XPZ HPrvIR22 Events 'Siguiente' · clase: esencial]
- **R-307** 'Anterior' vuelve al paso 8 (`HPrvIR06`) si la variable de sesión `regreso` vale '1'; si no, vuelve al paso 1 (`HPrvIR02`). El comentario del XPZ explica el segundo caso como "expiró la sesión". Clase por defecto: el uso de una variable de sesión para saber de qué paso se viene no tiene más respaldo que ese comentario. [V · capas: código, diseño · ev: hprvir22_impl.java e1325M2 ('Anterior'); XPZ HPrvIR22 Events 'Anterior' · clase: esencial]
- **R-308** 'Volver' lleva a `HPrvIR39` en modo `P` y, en los otros modos, retorna al llamador con el modo. El comentario del código dice que el modo `P` "no se usa". Clase por defecto. [V · capas: código, diseño · ev: hprvir22_impl.java e1425M2 ('Volver'); XPZ HPrvIR22 Events 'Volver' · clase: esencial]
- **R-309** Dos textos fijos sobre la documentación respaldatoria que debe presentarse en las oficinas se asignan en el arranque y se dejan con visibilidad apagada; ningún evento los enciende, así que nunca se muestran. [D · capas: código, diseño, intención · ev: hprvir22_impl.java e1525M2 (Start); XPZ HPrvIR22 Events Start; manual Registro p. 20 · clase: accidente · ≠ D-06]
- **R-310** El arranque lee el usuario de la sesión de administración en una variable que nadie usa después, y apaga un bloque auxiliar ("TableHide") que tampoco se enciende en ningún lado: código muerto. [V · capas: código, diseño · ev: hprvir22_impl.java e1525M2 (Start); XPZ HPrvIR22 Events Start · clase: accidente]

## Condición de avance

El asistente avanza al paso 10 con 'Siguiente' (R-306). La única condición es R-302: solo bloquea si COMPRAS_OBLIGACTABCO vale 'S' y no hay cuentas en la grilla (R-303). Con el atributo en otro valor se puede avanzar sin cargar ninguna cuenta. Ninguna otra validación de las cuentas ocurre en esta pantalla; las del contenido de cada cuenta viven en `TPrvBco`, que no es parte de este paso.

## Capas

Capas: diseño (XPZ `HPrvIR22` y rev2 §11 y §17) y código (Java `hprvir22_impl.java`). La ejecución todavía no se observó: ejecución: todavía no observado (E4). La intención (manuales) no se consultó para este paso.

El Java coincide con el XPZ en todos los eventos leídos. Los parámetros de configuración no aparecen en este paso; el único valor externo es el atributo de sistema COMPRAS_OBLIGACTABCO, del que solo se anota el nombre.
