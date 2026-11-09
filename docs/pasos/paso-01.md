# Paso 1 — HPrvIR02, puerta de entrada por CUIT

Ids de este archivo: reglas R-101 a R-119. Los textos de mensajes se transcriben tal cual salen del Java. De los atributos de sistema y de los parámetros solo figuran los nombres.

## Objeto

- El objeto es el panel web `HPrvIR02`, que se muestra como "PASO 1 de 11" y pertenece al grupo `GENProveRegistro`. [V · capas: código, diseño · ev: hprvir02_impl.java wb_table2_5_5A2e; XPZ HPrvIR02 Form]
- Es la puerta de entrada del alta: con el CUIT decide si el proveedor puede seguir al paso 2, si salta al paso 10 o si el trámite se corta con un mensaje. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente']
- La decisión la toma el procedimiento `PPrvIR02`, que devuelve un flag de un carácter. El panel solo lo interpreta. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente']
- Al abrirse, el panel marca la sesión como asistente (clave de sesión `wizard`). Qué otros objetos leen esa clave no se investigó en este paso. [V · capas: código, diseño · ev: hprvir02_impl.java e115A2 (Start); XPZ HPrvIR02 Events Start]
- **R-101** Al abrirse (Start), el panel inicia sesión contra Services con el usuario y la clave que trae el atributo de sistema USUPORTALWEB, para obtener un contexto. Si el atributo no trae usuario o clave, solo escribe un aviso en la consola del servidor y el usuario no ve nada. El mismo bloque se repite en `TPrvInsRP0001` (paso 3). Clase por defecto: depende de Services, pero la duplicación podría ser un accidente. [V · capas: código, diseño · ev: hprvir02_impl.java e115A2 (Start); XPZ HPrvIR02 Events Start · clase: esencial]
- **R-102** Si el atributo de sistema ANEXODOCUMENTACION vale 'S', el panel muestra el enlace "aquí" que abre el anexo de documentación necesaria (informe `RPrvIR02`, compilado como `arprvir02`) en una ventana emergente. Con cualquier otro valor la tabla del anexo queda oculta. Clase por defecto. [V · capas: código, diseño · ev: hprvir02_impl.java e115A2 (Start) y e135A2 ('Anexo1'); XPZ HPrvIR02 Events Start y 'Anexo1' · clase: esencial]
- El texto "Mientras no confirme la información, podrá modificar sus datos." está en el formulario, pero Start lo oculta siempre. Ningún otro evento lo vuelve a mostrar. [V · capas: código, diseño · ev: hprvir02_impl.java e115A2 (Start); XPZ HPrvIR02 Events Start]

## Datos que pide

- El CUIT en tres campos numéricos: tipo (`PrvIgnTi`, 2 dígitos), número (`PrvIgnNr`, 8 dígitos) y dígito verificador (`PrvIgnDi`, 1 dígito). [V · capas: código, diseño · ev: hprvir02_impl.java initializeDynEvents (iparms de 'SIGUIENTE'); XPZ HPrvIR02 Variables]
- La pregunta "¿Es empleado de la Provincia o de alguna Municipalidad Provincial?", como opción de sí o no (variable `Pregunta`, que Start deja en falso). Debajo, en rojo, la leyenda "Si su respuesta fue SI, no puede continuar con la Inscripción". [V · capas: código, diseño · ev: hprvir02_impl.java wb_table6_52_5A2e y e115A2 (Start); XPZ HPrvIR02 Events Start]
- Un texto de ayuda con la advertencia de que los datos de cada paso tienen carácter de declaración jurada. [V · capas: código, diseño · ev: hprvir02_impl.java wb_table2_5_5A2e; XPZ HPrvIR02 Form]

## Validaciones

- **R-103** Si se marcó la pregunta del empleado público, "Siguiente" no valida nada: solo muestra la tabla con la leyenda de que no se puede continuar. Esta pregunta no figura en la rev2. Clase por defecto: parece una norma de incompatibilidad, pero la evidencia no lo dice. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente' · clase: esencial]
- **R-104** Si el número del CUIT es 0, muestra "ERROR: Debe ingresar el CUIT. Verifique." y no sigue. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'; rev2 §3 · clase: esencial]
- **R-105** Recalcula el dígito verificador con `PNuPro04`. Si no coincide con el ingresado, muestra "ERROR: El dígito verificador del CUIT no es válido. Verifique." y no sigue. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'; rev2 §3 · clase: esencial]
- **R-106** Flag `H` (proveedor habilitado): corta con "ERROR: El proveedor ya está Habilitado para operar. Ya puede ingresar al sistema". [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'; rev2 §3 · clase: esencial]
- **R-107** Flag `Q` (esperando habilitación de modificación de datos): corta con "ERROR: El proveedor está en espera de habilitación de modificación de datos." [D · capas: código, diseño, intención · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'; rev2 §3; manual Registro p. 5 · clase: esencial · ≠ D-01]
- **R-108** Flag `G` (Agente del Estado): corta con "ERROR: El proveedor es Agente del Estado. No puede darse de Alta." El comentario del XPZ que lista los flags no menciona `G`, pero el `case` sí lo trata. Clase por defecto. [D · capas: código, diseño, intención · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'; rev2 §3; manual Registro p. 5 · clase: esencial · ≠ D-01]
- **R-109** Flag `E` (esperando habilitación): rescata el usuario con `PPrvIR05` (rutina 'GETUSUARIO'), pone el módulo en `P` y salta al paso 10 (`HPrvIR10`) con ese usuario y ese módulo. No pasa por el paso 2. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente') y S122 ('PASO10'); XPZ HPrvIR02 Events 'Siguiente' y Sub 'Paso10'; rev2 §3 · clase: esencial]
- **R-110** Flags `P`, `A` o `N` (el proveedor existe en el sistema viejo PROVE, o existe sin estar habilitado): rescata el usuario con `PPrvIR05`, pone `band` en 1 ("existe el proveedor") y sigue al paso 2. Solo sigue si `PPrvIR05` devuelve `Prove` igual a '1' o a '0'. Con cualquier otro valor el panel no hace nada y no muestra ningún mensaje. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente') y S112 ('GETUSUARIO'); XPZ HPrvIR02 Events 'Siguiente' y Sub 'getUsuario'; rev2 §3 · clase: esencial]
- **R-111** Flag `F` (proveedor no encontrado): pone `band` en 0, la categoría en '9' y sigue al paso 2. Es el alta de un proveedor nuevo. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente') y S132 ('PASO2'); XPZ HPrvIR02 Events 'Siguiente' y Sub 'Paso2'; rev2 §3 · clase: esencial]
- **R-112** Flag `X` (el usuario ya existe): corta con "Error. Ya existe ese usuario." [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'; rev2 §3 · clase: esencial]
- **R-113** Flag `T` (perfil temporal, creado desde la compra de pliegos de licitación): pone `band` en 1, la categoría en '9' y sigue al paso 2. Puede ser un caso puntual pegado al flujo, pero la evidencia no alcanza: clase por defecto. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'; rev2 §3 · clase: esencial]
- **R-114** Cualquier otro flag: corta con "ERROR: No es posible continuar el proceso con el número de CUIT indicado." [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'; rev2 §3 · clase: esencial]
- **R-115** Para los flags `P`, `A` y `N` la categoría que se pasa al paso 2 es '1' si `Prove` vale '1' y la inscripción vale 1, y '9' si `Prove` vale '1' sin inscripción. Con `Prove` en '0' se pasa la que devolvió `PPrvIR05`. Con `F` y `T` es '9'. Pero el paso 2 descarta esa categoría y siempre usa '1' (ver R-121). Por eso la derivación no tiene efecto en el alta. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente') y S132 ('PASO2'); hprvir07_impl.java e11A22 (Start); XPZ HPrvIR02 Events 'Siguiente'; rev2 §3 · clase: accidente]
- **R-116** La llamada a `PPrvIR01`, que consultaba si el proveedor ya existe en `PRVPER` y su habilitación, está comentada en el XPZ y reemplazada por `PPrvIR02`. En el Java no queda rastro porque no se compila. [S · capas: diseño · ev: XPZ HPrvIR02 Events 'Siguiente' (línea comentada) · clase: accidente]

## Condición de avance

- Pasa al paso 2 (`HPrvIr07`) con tipo, número y dígito del CUIT, `Prove`, la categoría y `band`, cuando el CUIT es válido, la pregunta del empleado público no está marcada y el flag es `P`, `A`, `N` (con `Prove` en '0' o '1'), `F` o `T`. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente') y S132 ('PASO2'); XPZ HPrvIR02 Events 'Siguiente' y Sub 'Paso2']
- Salta al paso 10 (`HPrvIR10`) en modo `P` cuando el flag es `E`. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente') y S122 ('PASO10'); XPZ HPrvIR02 Events 'Siguiente' y Sub 'Paso10']
- En cualquier otro caso se queda en el paso 1 con un mensaje, salvo el caso mudo de R-110. [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente']

## Capas

Capas: diseño (XPZ y rev2 §3), código (Java generado); ejecución: todavía no observado (E4). Los manuales (intención) no se consultaron para este paso.

El XPZ y el Java coinciden en todo lo que hace el evento 'Siguiente'. Las únicas líneas del XPZ sin reflejo en el Java son comentarios (R-116). Los procedimientos `PPrvIR02`, `PPrvIR05`, `PNuPro04` y el sistema viejo PROVE están fuera de este paso: aquí solo se documenta cómo el panel interpreta lo que devuelven.
