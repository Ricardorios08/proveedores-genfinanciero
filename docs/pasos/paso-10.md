# Paso 10: imprimir datos (HPrvIR10)

## Objeto

`HPrvIR10` es la pantalla "Imprimir Datos", rotulada "PASO 10 de 11" y titulada "Imprimir Solicitud de Inscripción". Recibe el usuario del proveedor y el modo. Desde acá se imprime la solicitud de inscripción (reporte `RPrvIR14m`) y, si corresponde, se descarga el anexo II (reporte `RPrvIR10`). Los dos reportes se abren en una ventana emergente; sus cuerpos no son parte de este paso.

El paso tiene dos presentaciones según el modo: en modo `I` es parte del asistente de alta; en los otros modos sirve para reimprimir la solicitud. Hacia atrás vuelve a `HPrvIR22` y hacia adelante pasa a `HPrvIR09`.

Fuentes: rev2 §12 y §17, XPZ `HPrvIR10`, Java `hprvir10_impl.java`.

## Datos que pide

Solo en la presentación de reimpresión (modo distinto de `I`) se pide un dato:

| Dato | Para qué | Bloque |
|---|---|---|
| Usuario | El usuario que el proveedor eligió en la inscripción, para habilitar el enlace de reimpresión | [V · capas: código, diseño · ev: hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start y 'Imprimir'] |

## Validaciones

- **R-320** En modo `I` el paso muestra el bloque de inscripción (instrucción de imprimir la solicitud, enlace de impresión, y los botones 'Anterior' y 'Siguiente') y oculta el de reimpresión. Los botones de navegación existen solo dentro de ese bloque, así que fuera del modo `I` este paso no tiene forma de avanzar a `HPrvIR09`. Clase por defecto. [V · capas: código, diseño · ev: hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start · clase: esencial]
- **R-321** En los otros modos el paso muestra el bloque de reimpresión, con el aviso fijo "La habilitación está en proceso. Espere la culminación del trámite." y el campo de usuario. El enlace de impresión aparece solo si el usuario escrito coincide con el del trámite. Es la única comprobación de identidad de la reimpresión, y el aviso no depende del estado real del proveedor. Clase por defecto. [V · capas: código, diseño · ev: hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start · clase: esencial]
- **R-322** Al pulsar 'Imprimir' sin haber escrito el usuario se muestra "Error: Debe ingresar su usuario para poder reimprimir"; si el usuario no coincide con el del trámite, "Error: Usuario ingresado no es correcto"; si coincide, se muestra el enlace de impresión. El evento está compilado como evento de cliente (`e17f01_client`) y su cuerpo no está en el Java extraído, así que esta regla se apoya solo en el XPZ. Clase por defecto. [S · capas: diseño · ev: XPZ HPrvIR10 Events 'Imprimir'; hprvir10_impl.java gx_button_ctrl 'Imprimir' (solo el botón) · clase: esencial]
- **R-323** El usuario escrito para reimprimir se pasa a mayúsculas, en el cliente al cambiar y salir del campo y en el servidor al leer el pedido, antes de compararlo con el del trámite. Clase por defecto. [V · capas: código · ev: hprvir10_impl.java strupF00 (lectura de variables) y gx_single_line_edit del campo de usuario · clase: esencial]
- **R-324** El enlace "aquí" de la solicitud abre el reporte `RPrvIR14m` en ventana emergente, con el usuario y el parámetro 'S'. [V · capas: código, diseño · ev: hprvir10_impl.java e14F02 ('Solicitud'); XPZ HPrvIR10 Events 'Solicitud' · clase: esencial]
- **R-325** El bloque del anexo II solo se muestra si el atributo de sistema ANEXOVERACIDAD no está vacío; si está vacío, se oculta. El anexo II y su leyenda (R-326) son de un cliente puntual, lo que sugiere un parche, pero la evidencia es indirecta. [V · capas: código, diseño · ev: hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start · clase: parche]
- **R-326** La leyenda del anexo II es un texto armado en el código, con datos fijos de un cliente (OSEP Mendoza) incrustados: qué organismo recibe el original y dónde. Lo único que sale de configuración es el nombre de la persona de atención, que se toma del atributo ANEXOVERACIDAD. Sin ese cliente, el texto es incorrecto. [V · capas: código, diseño · ev: hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start · clase: accidente]
- **R-327** La leyenda se corta en líneas de 123 caracteres y se reparte en tres bloques de texto; si saliera en más de tres líneas, el resto se descarta sin aviso. Clase por defecto. [V · capas: código, diseño · ev: hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start · clase: esencial]
- **R-328** El enlace "aquí" del anexo II abre el reporte `RPrvIR10` en ventana emergente, con un parámetro lógico (`Flag`) que este paso nunca asigna. Clase por defecto. [V · capas: código, diseño · ev: hprvir10_impl.java e15F02 ('Anexo2'); XPZ HPrvIR10 Events 'Anexo2' · clase: esencial]
- **R-329** 'Siguiente' (evento 'Confirmar') pasa a `HPrvIR09` con el usuario solamente; no le pasa el modo. [V · capas: código, diseño · ev: hprvir10_impl.java e12F02 ('Confirmar'); XPZ HPrvIR10 Events 'Confirmar' · clase: esencial]
- **R-330** 'Anterior' vuelve a `HPrvIR22` con el usuario y el modo. El comentario de la llamada recuerda que antes ese paso era el de apoderados. La rev2 §12 dice que el paso "avanza" a `HPrvIR22`; ver D-303. [V · capas: código, diseño · ev: hprvir10_impl.java e13F02 ('Anterior'); XPZ HPrvIR10 Events 'Anterior' · clase: esencial]

## Condición de avance

El avance a `HPrvIR09` ocurre con 'Siguiente' (R-329) y no tiene ninguna validación: no exige haber impreso la solicitud ni descargado el anexo II. Solo se puede avanzar en modo `I` (R-320). En los otros modos el paso es de consulta: se reimprime (R-321, R-322) y se sale por otro camino.

## Capas

Capas: diseño (XPZ `HPrvIR10` y rev2 §12 y §17) y código (Java `hprvir10_impl.java`). La ejecución todavía no se observó: ejecución: todavía no observado (E4). La intención (manuales) no se consultó para este paso.

R-322 queda en S porque el cuerpo del evento 'Imprimir' no está en el Java extraído: es un evento de cliente. Los valores de los atributos de sistema no se transcriben; el texto fijo de un cliente aparece nombrado en R-326 pero no copiado.
