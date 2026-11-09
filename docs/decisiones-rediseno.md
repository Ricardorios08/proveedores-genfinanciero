# Decisiones de rediseño

Lo que el responsable tiene que decidir para rediseñar el módulo, ordenado por impacto en el flujo: primero lo que cambia la secuencia de pasos, después seguridad, validaciones y notificaciones, y al final el código muerto. Cada decisión agrupa las reglas `R-nnn` que la sostienen; el detalle y la evidencia de cada regla están en su archivo de respaldo.

Cada entrada dice qué hace hoy el sistema, por qué parece un parche o un accidente, qué se pierde si se saca y una recomendación: `mantener`, `rediseñar` o `eliminar`. El campo **decisión del responsable** queda vacío hasta que decida; la decisión se copia después a la columna `decision` de `features.csv`.

Al final están las reglas esenciales: las que tienen poca evidencia como **confirmación rápida**, agrupadas por archivo, y las demás en **Se mantiene**.

**Calidad de la clasificación.** De 300 reglas, 46 son esenciales por defecto (15 %), por debajo del umbral de un tercio del diseño: la clasificación se apoya en evidencia en la mayoría de los casos.


## Cambia la secuencia del flujo

### DR-01 — La categoría del proveedor: se calcula y se tira

- **Reglas:** R-115, R-121, R-145, R-205, R-206, R-216, R-214.
- **Qué hace hoy:** El paso 1 calcula una categoría ('1' o '9') según el padrón, y el paso 2 la descarta: la fija siempre en '1' (R-115, R-121). Como consecuencia, Ingresos Brutos es siempre obligatorio en el paso 3 (R-145), y todo lo que dependía de la categoría quedó muerto: textos ocultos (R-205, R-216), una condición de domicilios comentada (R-206) y la validación de balance para categoría 1 (R-214).
- **Por qué parece parche o accidente:** Es una regla de negocio a medio sacar: la categoría existe en los datos, pero el alta no la usa. Es el patrón típico de un cambio de política que se aplicó tapando la variable en lugar de quitar la lógica.
- **Qué se pierde si se saca:** Si la categoría 9 (no inscripto en Ingresos Brutos) es una situación real, hoy esos proveedores no pueden registrarse sin inventar un número de inscripción.
- **Recomendación: `rediseñar`.** Decidir si la categoría existe. Si existe, que la calcule un solo lugar y que de ella dependan las obligaciones. Si no existe, borrar todo lo que la menciona.
- **Decisión del responsable:** 

### DR-02 — El paso 6 (situación patrimonial) no exige nada

- **Reglas:** R-213, R-214, R-215, R-224.
- **Qué hace hoy:** El paso 6 avanza siempre, sin pedir ningún ejercicio ni balance (R-213). Las dos validaciones que lo exigían están comentadas en el XPZ y no existen en el Java (R-214, R-215), y lo que el panel consulta para ellas no se usa (R-224).
- **Por qué parece parche o accidente:** Validaciones desactivadas que siguen en el código: accidente.
- **Qué se pierde si se saca:** Si el balance es requisito para contratar, hoy el registro no lo controla y alguien lo revisa a mano después (o nadie).
- **Recomendación: `rediseñar`.** Decidir si los estados contables son obligatorios y para quién. Si no lo son, el paso se vuelve opcional de forma explícita; si lo son, la validación se escribe de nuevo.
- **Decisión del responsable:** 

### DR-03 — La navegación hacia atrás está rota

- **Reglas:** R-169, R-238, R-239, R-208, R-307, R-222, R-230, R-308.
- **Qué hace hoy:** El botón 'Anterior' del paso 3 siempre vuelve al paso 1, y el propio código dice 'Revisar' (R-169). Los pasos 5, 8 y 9 deciden adónde volver con una variable de sesión (`regreso`) que el paso 8 pisa (R-238, R-239, R-208, R-307): una persona física que retrocede puede caer en el paso de persona jurídica. 'Volver' se comporta distinto según el panel (R-222, R-230, R-308).
- **Por qué parece parche o accidente:** La navegación depende de estado global mutable compartido entre pantallas: un parche sobre otro.
- **Qué se pierde si se saca:** Nada: es un defecto.
- **Recomendación: `rediseñar`.** Un asistente con historial propio (cada paso sabe cuál es el anterior por la secuencia, no por una variable de sesión).
- **Decisión del responsable:** 

### DR-04 — El paso 4 graba antes de validar

- **Reglas:** R-187, R-188, R-191.
- **Qué hace hoy:** 'Siguiente' en persona jurídica graba la sociedad antes de comprobar que haya integrantes (R-187), y 'Agregar integrante' graba sin ninguna validación (R-188). El bloque de validación está copiado dos veces (R-191).
- **Por qué parece parche o accidente:** Orden invertido validar/grabar más duplicación: accidente.
- **Qué se pierde si se saca:** Nada: hoy quedan sociedades grabadas a medias.
- **Recomendación: `rediseñar`.** Guardar como borrador explícito, o validar todo antes de grabar. La validación, en un solo lugar.
- **Decisión del responsable:** 

### DR-05 — Confirmar el alta pasa a 'En espera' aunque falle el aviso

- **Reglas:** R-466, R-518, R-357, R-701, R-515, R-719.
- **Qué hace hoy:** El paso 11 tiene `|| true` en la condición que debía exigir que el mensaje de registro saliera bien (R-466, R-518): el estado cambia siempre y la rama de error es inalcanzable (R-357). Nadie mira el resultado de los avisos del alta (R-701, R-515, R-719).
- **Por qué parece parche o accidente:** Alguien desactivó el control para que el alta no se trabara cuando fallaba la mensajería: parche que quedó.
- **Qué se pierde si se saca:** Que el alta nunca se trabe por la mensajería. Ese objetivo vale; la forma no.
- **Recomendación: `rediseñar`.** El cambio de estado no depende del aviso, pero el aviso queda en una cola con reintento y con su resultado registrado.
- **Decisión del responsable:** 

### DR-06 — Modificar datos: dos caminos distintos para lo mismo

- **Reglas:** R-612, R-613, R-621, R-630, R-610, R-611, R-449, R-450, R-465, R-464, R-153.
- **Qué hace hoy:** El proveedor (modo `P`) y la administración (modo `A`) editan los mismos datos con pantallas distintas y con conjuntos distintos (R-612, R-613). En `A` ninguna edición deja constancia ni pasa a revisión (R-621). En `P` se puede editar en casi cualquier estado (R-630). Hay cinco rutas que llevan a `Q` y no coinciden entre sí (R-449, R-450, R-465), con reglas redundantes o inalcanzables (R-464, R-153) y ramas de pantalla que nadie alcanza (R-610, R-611).
- **Por qué parece parche o accidente:** Creció por agregados: cada pantalla nueva trajo su propia regla de 'cambio pendiente'.
- **Qué se pierde si se saca:** Que la administración pueda corregir sin pasar por revisión. Si eso es necesario, tiene que quedar registrado.
- **Recomendación: `rediseñar`.** Un solo editor de datos del proveedor, con permisos por rol y una única regla de 'cambio pendiente de aprobación', con historial de quién cambió qué.
- **Decisión del responsable:** 

### DR-07 — Habilitar al proveedor: tres caminos con criterios distintos

- **Reglas:** R-446, R-447, R-448, R-444, R-445, R-458, R-459, R-463.
- **Qué hace hoy:** Un proveedor llega a `H` por tres procedimientos (R-446, R-447, R-448), y ninguno revisa el estado de origen: la condición está en la pantalla que lo llama. Renovar el certificado (R-448) habilita un `Q` sin pasar por la revisión de modificaciones. La provisoria tiene su propio circuito (R-444, R-445) y su vigencia se calcula distinto según quién la muestra (R-463). El vencimiento (R-458) lo dispara un proceso externo y no hay vuelta de `V` a `H` (R-459).
- **Por qué parece parche o accidente:** Una máquina de estados implícita, repartida entre pantallas.
- **Qué se pierde si se saca:** Nada de lo que hoy se puede hacer, si la máquina nueva cubre los mismos estados.
- **Recomendación: `rediseñar`.** Una máquina de estados explícita en el backend, con transiciones y condiciones en un solo lugar y auditoría de cada cambio. Ver `estados.md` como inventario de partida.
- **Decisión del responsable:** 


## Seguridad

### DR-08 — El proveedor puede entrar a la administración de su propio perfil

- **Reglas:** R-604, R-609, R-605.
- **Qué hace hoy:** El enlace 'Perfil' abre `HPrvIR21` en modo `A` sin controlar permisos (R-604); por lectura del código, no observado en test. Solo `HPrvIR40` controla el perfil de administrador (R-605), y su enlace está oculto pero el objeto sigue vivo (R-609).
- **Por qué parece parche o accidente:** Falta de control de acceso: accidente grave.
- **Qué se pierde si se saca:** Nada.
- **Recomendación: `rediseñar`.** Control de acceso por rol en el backend, no por visibilidad de enlaces. **Además, conviene avisarle hoy a quien mantiene el sistema actual**, y confirmarlo en test.
- **Decisión del responsable:** 

### DR-09 — Contraseñas generadas débiles, cifradas de forma reversible y enviadas en texto claro

- **Reglas:** R-549, R-550, R-551, R-552, R-553, R-155, R-168.
- **Qué hace hoy:** La contraseña inicial es un número de 8 dígitos con `Random()` (R-549, R-155), cifrado con una clave escrita en el código y reversible (R-550). Hay dos credenciales por proveedor (R-551). La clave de Services viaja en texto claro por correo (R-552, R-168), y la recuperación reinicia la clave con solo el usuario o solo el correo y la manda en claro (R-553).
- **Por qué parece parche o accidente:** Prácticas de credenciales de otra época: accidente.
- **Qué se pierde si se saca:** Nada: lo de negocio (que el proveedor reciba acceso y pueda recuperarlo) se conserva con otro mecanismo.
- **Recomendación: `rediseñar`.** Una sola identidad, con alta por enlace de activación de un solo uso y recuperación por enlace con vencimiento. Nunca una clave en un correo.
- **Decisión del responsable:** 

### DR-10 — La cuenta de servicio de Services: en un atributo y en los logs

- **Reglas:** R-554, R-555, R-101, R-166.
- **Qué hace hoy:** El portal se autentica en Services con una cuenta guardada en un atributo de sistema (R-554), y cada paso 1 y cada alta la usan (R-101, R-166). `crontabauthorizeuser` imprime esa clave en la salida estándar del servidor (R-555): comprobado en el Java.
- **Por qué parece parche o accidente:** Accidente de seguridad, con efecto hoy.
- **Qué se pierde si se saca:** Nada.
- **Recomendación: `rediseñar`.** La credencial en un gestor de secretos y nunca en logs. **Avisar hoy**: la clave actual pudo quedar en los logs de cualquier ambiente y conviene rotarla.
- **Decisión del responsable:** 


## Validaciones y datos

### DR-11 — Datos de un cliente escritos en el código

- **Reglas:** R-326, R-541, R-542, R-543, R-545, R-546, R-547, R-325, R-350, R-522.
- **Qué hace hoy:** Textos de OSEP Mendoza, direcciones, enlaces al boletín, prefijos y remitentes fijos están escritos en el código (R-326, R-541, R-542, R-543, R-545, R-546, R-547). Otras reglas dependen de atributos de sistema que parecen pensados para una sola instalación (R-325, R-350, R-522).
- **Por qué parece parche o accidente:** Personalización de un cliente hecha en el producto: accidente o parche.
- **Qué se pierde si se saca:** Nada, si la configuración nueva permite expresar lo mismo.
- **Recomendación: `rediseñar`.** Todo dato propio de una instalación va a configuración por instalación (textos, organismo, enlaces, formularios). El código no nombra a ningún cliente.
- **Decisión del responsable:** 

### DR-12 — Validaciones duplicadas o que nunca corren

- **Reglas:** R-143, R-153, R-191, R-539.
- **Qué hace hoy:** El correo se valida dos veces con mensajes distintos (R-143); hay una regla de estado que nunca se ejecuta (R-153), un bloque de validación copiado (R-191) y un parámetro de clave que se envía siempre vacío (R-539).
- **Por qué parece parche o accidente:** Duplicación: accidente.
- **Qué se pierde si se saca:** Nada.
- **Recomendación: `eliminar`.** No replicar: cada validación, una vez.
- **Decisión del responsable:** 


## Notificaciones

### DR-13 — La mensajería no tiene un responsable único

- **Reglas:** R-702, R-703, R-704, R-705, R-707, R-708, R-709, R-710, R-711, R-712, R-713, R-714, R-716, R-718, R-722, R-725, R-726, R-727, R-728, R-544.
- **Qué hace hoy:** Trece objetos mandan mensajes de canal y solo uno mira el resultado (R-702 a R-714). Hay envíos que nunca salen (R-725, R-726, R-727), la renovación avisa por dos caminos distintos (R-703 y R-716), un aviso fallido de vencimiento no se reintenta (R-718), un oferente sin correo corta el recorrido de compras (R-722) y el registro de envíos guarda una casilla de pruebas fija como remitente (R-728, R-544).
- **Por qué parece parche o accidente:** Cada pantalla resolvió su propio aviso: crecimiento por agregados.
- **Qué se pierde si se saca:** Nada, si el servicio nuevo cubre los mismos eventos.
- **Recomendación: `rediseñar`.** Un servicio de notificaciones único: eventos con nombre, plantillas por instalación, cola con reintento y registro del resultado. `mensajes.md` es el inventario de eventos.
- **Decisión del responsable:** 


## Código muerto (no requiere decisión, solo confirmación)

### DR-14 — Restos de la administración vieja y variables sin uso

- **Reglas:** R-116, R-131, R-193, R-210, R-211, R-223, R-231, R-233, R-234, R-242, R-245, R-246, R-310, R-360, R-309, R-359, R-631, R-632.
- **Qué hace hoy:** Llamadas a `HPrvIR21`, `PPrvIR01` y `Pprvir07` comentadas (R-116, R-131, R-193, R-210, R-223, R-231, R-242), una variable de sesión de administración que se lee y no se usa en varios paneles (R-211, R-234, R-246, R-310), enlaces comentados (R-233, R-245), mensajes y textos que nunca se muestran (R-309, R-359, R-360) y opciones de impresión que no hacen nada (R-631, R-632).
- **Por qué parece parche o accidente:** Código muerto: accidente.
- **Qué se pierde si se saca:** Nada: no tiene efecto hoy.
- **Recomendación: `eliminar`.** No replicar. Si alguno de esos textos ocultos expresa una regla que se quiere, se decide en su decisión temática (por ejemplo, la categoría o el paso 6).
- **Decisión del responsable:** 


## Confirmación rápida: esenciales con poca evidencia

Reglas que el análisis dejó como esenciales **por defecto**, porque la evidencia no alcanzaba para llamarlas parche o accidente. La recomendación es `mantener`; si alguna no la querés, decilo en la decisión del grupo.

### DR-15 — Confirmar las esenciales por defecto de `modos.md`

- **R-601** El modo `I` lo fija solo el paso 2, de forma constante, antes de abrir `TPrvInsRP`. Ningún otro camino de entrada del alta lo
- **R-602** El modo `P` del menú lo fija `HPrvIR39` en Start, sin recibirlo por parámetro. A ese menú se llega desde `HCOF0006` ('Inicio') cuando el estado del proveedor no es `H` (si es `H` va a `HNUPRO16`) y desde el 'Volver' de…
- **R-607** `HPrvIR21` abre `TPrvInsRP`, `HPrvIR41`, `HPrvIR06`, `HPrvIR22`, `HPrvIR50`, `HPrvIR17m` y `HPrvIR42` como ventanas emergentes y les pasa `A`; `TPrvInsRP` se abre con modo `UPD` y `BloqueaNombre` vacío. 'Documentos'…
- **R-608** `HPrvIR21` muestra u oculta dos opciones según el perfil: 'Cambiar Estado de Habilitación' se oculta si el proveedor tiene número de norma de certificado, y 'Cambiar Categoría' aparece si hay una solicitud de cambio…
- **R-614** `HPrvIR50` ("Trabajar con Balances") es el panel de balances de los modos `P` y `A`, con alta, modificación y baja por la ventana `TPrvESP`. Su 'volver' solo tiene ramas para `P` (a `HPrvIR39`) y para `A` (devuelve el…
- **R-620** La edición del nombre depende de quién abre el panel: el menú `P` pasa `BloqueaNombre` igual a '1' (el nombre queda fijo con el del padrón) y `HPrvIR21` lo pasa vacío (el nombre se puede cambiar). El aviso del panel…
- **R-633** El cambio de categoría tiene cuatro salidas desde `HPrvIR39`. Con una solicitud pendiente y categoría `2`, `HPrvIR75` en modo 'E' (eliminarla). Si no hay esa solicitud pendiente, y `PPrvIR71` devuelve 0, `HPrvIR51b`…
- **R-634** La reinscripción depende del estado: en `I` el texto es "Emitir Solicitud de Reinscripción" y se oculta el mensaje; en `R`, si hay una solicitud sin confirmar, el texto pasa a "Eliminar Solicitud de Reinscripción"; en…
- **R-635** `HPrvIR52` ("Estado Situación Patrimonial para cambio de Categoría") recibe `Modulo` y no lo compara: solo lo reenvía a `HPrvIR51` en 'Anterior'. 'Volver' va siempre a
- **R-636** 'Siguiente' en `HPrvIR52` exige la fecha del último ejercicio ("Debe ingresar al menos los datos del último ejercicio para poder continuar."). Si el tipo de persona es 0, exige además un balance cerrado según `RPrvIR63`…

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-16 — Confirmar las esenciales por defecto de `pasos/paso-01.md`

- **R-102** Si el atributo de sistema ANEXODOCUMENTACION vale 'S', el panel muestra el enlace "aquí" que abre el anexo de documentación necesaria (informe `RPrvIR02`, compilado como `arprvir02`) en una ventana emergente. Con…
- **R-103** Si se marcó la pregunta del empleado público, "Siguiente" no valida nada: solo muestra la tabla con la leyenda de que no se puede continuar. Esta pregunta no figura en la
- **R-108** Flag `G` (Agente del Estado): corta con "ERROR: El proveedor es Agente del Estado. No puede darse de Alta." El comentario del XPZ que lista los flags no menciona `G`, pero el `case` sí lo
- **R-113** Flag `T` (perfil temporal, creado desde la compra de pliegos de licitación): pone `band` en 1, la categoría en '9' y sigue al paso 2. Puede ser un caso puntual pegado al flujo, pero la evidencia no alcanza: clase por…

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-17 — Confirmar las esenciales por defecto de `pasos/paso-03.md`

- **R-141** El prefijo de Ingresos Brutos (`PrvIib3`) puede ser 0 o mayor que 900. Si está entre 1 y 900 muestra "El número de inscripción en ingresos brutos puede ser 0 o mayor que  900" (con dos
- **R-161** Qué campos se pueden editar depende del módulo cuando el modo es `UPD`. En `P` (el proveedor modifica sus datos) se bloquean tipo y sexo, clase, IVA, Ingresos Brutos, certificado y CUIT. En `I` se habilitan tipo, sexo,…

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-18 — Confirmar las esenciales por defecto de `pasos/paso-04.md`

- **R-190** La lista de Tipo de Asociación (`PrvCla`) depende del tipo de persona: para una jurídica se quitan las opciones 1 y 2; para una física quedan solo "UNIPERSONAL" y "SOCIEDAD DE HECHO". El campo lleva '*' en pantalla,…

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-19 — Confirmar las esenciales por defecto de `pasos/paso-05.md`

- **R-204** | El enlace Eliminar de la grilla se anula para el domicilio real (tipo 2) y, si la categoría es `1`, también para el legal (tipo 1). Los demás domicilios sí se pueden

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-20 — Confirmar las esenciales por defecto de `pasos/paso-06.md`

- **R-219** | Eliminar abre `TPrvESP` en modo `DLT` sobre el ejercicio del selector y después vuelve a llamar a `HPrvIR18` para recargarlo. No pide confirmación en el panel y no comprueba que el ejercicio

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-21 — Confirmar las esenciales por defecto de `pasos/paso-07.md`

- **R-236** | El mínimo de un rubro vale para todos los tipos de persona y categorías: el conteo no mira `PrvCat` ni

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-22 — Confirmar las esenciales por defecto de `pasos/paso-08.md`

- **R-237** | No hay obligatoriedad de representantes: Siguiente no cuenta ni valida filas. A diferencia de rubros (R-225) y cuentas bancarias, un proveedor puede seguir sin

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-23 — Confirmar las esenciales por defecto de `pasos/paso-09.md`

- **R-302** Si el atributo de sistema COMPRAS_OBLIGACTABCO vale 'S' y la grilla no tiene ninguna cuenta, 'Siguiente' no avanza y muestra "ERROR: Es OBLIGATORIO ingresar al menos una Cuenta Bancaria." Si el atributo no vale 'S', el…
- **R-303** La cantidad de cuentas que se compara con la obligatoriedad es la cantidad de filas de la grilla que llegan en el pedido, no una consulta aparte a la
- **R-305** En modo `I` se muestran los botones del asistente (anterior y siguiente) y el rótulo del paso, se oculta el bloque de actualización y el título es "Datos de Cuentas Bancarias". En los otros modos pasa al revés y el…

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-24 — Confirmar las esenciales por defecto de `pasos/paso-10.md`

- **R-320** En modo `I` el paso muestra el bloque de inscripción (instrucción de imprimir la solicitud, enlace de impresión, y los botones 'Anterior' y 'Siguiente') y oculta el de reimpresión. Los botones de navegación existen solo…
- **R-321** En los otros modos el paso muestra el bloque de reimpresión, con el aviso fijo "La habilitación está en proceso. Espere la culminación del trámite." y el campo de usuario. El enlace de impresión aparece solo si el…
- **R-322** Al pulsar 'Imprimir' sin haber escrito el usuario se muestra "Error: Debe ingresar su usuario para poder reimprimir"; si el usuario no coincide con el del trámite, "Error: Usuario ingresado no es correcto"; si coincide,…
- **R-323** El usuario escrito para reimprimir se pasa a mayúsculas, en el cliente al cambiar y salir del campo y en el servidor al leer el pedido, antes de compararlo con el del
- **R-327** La leyenda se corta en líneas de 123 caracteres y se reparte en tres bloques de texto; si saliera en más de tres líneas, el resto se descarta sin
- **R-328** El enlace "aquí" del anexo II abre el reporte `RPrvIR10` en ventana emergente, con un parámetro lógico (`Flag`) que este paso nunca

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 

### DR-25 — Confirmar las esenciales por defecto de `pasos/paso-11.md`

- **R-352** El enlace "aquí" para ver de nuevo los datos abre el reporte `RPrvIR14` con el usuario y el parámetro 'S'. El paso 10 imprime la misma solicitud con `RPrvIR14m`: hay dos variantes del reporte y esta evidencia no dice…
- **R-353** El arranque fija el modo en `I` sin importar cómo se llegó. Es coherente con que el paso 10 solo permite avanzar en modo `I` (R-320), y hace que 'Anterior' vuelva siempre al paso 10 en modo
- **R-358** Tras confirmar, la pantalla muestra "¡Muchas gracias por registrarse!", un recordatorio del nombre de usuario y el aviso de que la contraseña para acceder al sistema se enviará por correo electrónico; oculta el…

- **Recomendación: `mantener`.**
- **Decisión del responsable:** 


## Discrepancias entre capas

Lo que el manual (capa intención) dice distinto del código. El detalle de cada una está en `discrepancias.md`.

### DR-26 — Paso 1: el manual promete el paso 2 y el sistema corta en dos casos

- **Discrepancia:** D-01.
- **Qué hace hoy:** Un Agente del Estado (R-108) y un proveedor con una modificación pendiente (R-107) se quedan en el paso 1 con un error que el manual no anticipa.
- **Por qué parece parche o accidente:** No es parche ni accidente del código: el código aplica una política que el manual no cuenta.
- **Qué se pierde si se saca:** Si se sacan los dos cortes, un agente del Estado podría registrarse como proveedor, y un proveedor con un cambio pendiente podría abrir un segundo trámite.
- **Recomendación: `mantener`.** Mantener los dos cortes como reglas de negocio explícitas, y que el manual y los mensajes de pantalla digan lo mismo.
- **Decisión del responsable:** 

### DR-27 — Paso 2: el nombre de usuario lo asigna el sistema, lo sugiere o lo elige el proveedor

- **Discrepancia:** D-02.
- **Qué hace hoy:** El manual dice que el sistema genera 'P' más el número de proveedor. El código lo propone y lo deja editable (R-120), y si el número tiene menos de 4 dígitos agrega los ceros al final. Además, el campo admite 20 caracteres y el dominio del modelo, 30.
- **Por qué parece parche o accidente:** El relleno con ceros a la derecha es un defecto. El resto es una regla de negocio que quedó a medias entre generar y elegir.
- **Qué se pierde si se saca:** Nada, si la regla nueva queda clara.
- **Recomendación: `rediseñar`.** Una sola regla para el identificador del proveedor (asignado o elegido, no las dos cosas a la vez) y un solo largo máximo.
- **Decisión del responsable:** 

### DR-28 — Paso 5: ¿el domicilio real es obligatorio?

- **Discrepancia:** D-03.
- **Qué hace hoy:** El manual dice que se validan el real y el legal. El código exige solo el legal (R-201), y la condición que combinaba los dos está comentada (R-206).
- **Por qué parece parche o accidente:** Una validación sacada sin actualizar el manual.
- **Qué se pierde si se saca:** Si el real no se exige, hay proveedores sin domicilio real cargado.
- **Recomendación: `rediseñar`.** Decidir si el domicilio real es obligatorio, y que el código y el manual digan lo mismo.
- **Decisión del responsable:** 

### DR-29 — Paso 6: el manual dice obligatorio y el código no exige nada

- **Discrepancia:** D-04.
- **Qué hace hoy:** El cuerpo del manual dice que el último ejercicio es obligatorio y que se valida su fecha de cierre. El código avanza siempre (R-213) y no hace esa validación. El encabezado del manual dice 'Dato No Obligatorio'.
- **Por qué parece parche o accidente:** Ver DR-02: es la misma decisión vista desde el manual.
- **Qué se pierde si se saca:** Ver DR-02.
- **Recomendación: `rediseñar`.** Se resuelve junto con DR-02.
- **Decisión del responsable:** 

### DR-30 — Paso 9: la cuenta bancaria es obligatoria u opcional según la instalación, y el manual no lo dice

- **Discrepancia:** D-05.
- **Qué hace hoy:** El manual presenta la cuenta como opcional. El código la exige cuando COMPRAS_OBLIGACTABCO vale 'S' (R-302).
- **Por qué parece parche o accidente:** Una regla configurable por instalación, que no se documentó.
- **Qué se pierde si se saca:** Si se saca la configuración, alguna instalación pierde la obligatoriedad que hoy tiene.
- **Recomendación: `mantener`.** Mantener la regla configurable (ver DR-11) y que la ayuda en pantalla muestre la regla vigente en cada instalación.
- **Decisión del responsable:** 

### DR-31 — Avisos de documentación a presentar: el manual los muestra y el código los oculta

- **Discrepancia:** D-06.
- **Qué hace hoy:** Las capturas del manual muestran avisos sobre la documentación que hay que presentar en las oficinas (pasos 4, 6, 9 y 11). El código los asigna y nunca los muestra (R-309, R-359), o los tiene comentados (R-360). Puede que el manual describa una versión anterior; falta verlo en test.
- **Por qué parece parche o accidente:** Textos apagados que siguen en el código: accidente (ver DR-14).
- **Qué se pierde si se saca:** Si la presentación de documentación es un requisito, hoy el proveedor no se entera por la pantalla.
- **Recomendación: `rediseñar`.** Decidir si el proveedor tiene que presentar documentación. Si sí, el sistema lo informa con un texto de configuración por instalación (ver DR-11); si no, se eliminan los textos.
- **Decisión del responsable:** 


## Se mantiene

Reglas esenciales con evidencia: el análisis no ve motivo para cambiarlas. Se listan por archivo; el detalle está en cada uno.

| Archivo | Reglas | Cantidad |
|---|---|---|
| `cliente-vs-producto.md` | R-548 | 1 |
| `configuracion.md` | R-519, R-520, R-521, R-523, R-524, R-525, R-526, R-527, R-528, R-529, R-530, R-531, R-532, R-533, R-534, R-535, R-536, R-537, R-538, R-540 | 20 |
| `estados.md` | R-431, R-421, R-422, R-423, R-424, R-425, R-426, R-427, R-428, R-429, R-430, R-441, R-442, R-443, R-451, R-452, R-453, R-454, R-455, R-456, R-457, R-460, R-461, R-462 | 24 |
| `integraciones.md` | R-501, R-502, R-503, R-504, R-505, R-506, R-507, R-508, R-509, R-510, R-511, R-512, R-513, R-514, R-516, R-517 | 16 |
| `mensajes.md` | R-706, R-715, R-717, R-720, R-721, R-723, R-724 | 7 |
| `modelo-datos.md` | R-401, R-405, R-402, R-403, R-404 | 5 |
| `modos.md` | R-603, R-606 | 2 |
| `pasos/paso-01.md` | R-104, R-105, R-106, R-107, R-109, R-110, R-111, R-112, R-114 | 9 |
| `pasos/paso-02.md` | R-120, R-122, R-123, R-124, R-125, R-126, R-127, R-128, R-129, R-130 | 10 |
| `pasos/paso-03.md` | R-140, R-142, R-144, R-146, R-147, R-148, R-149, R-150, R-151, R-152, R-154, R-156, R-157, R-158, R-159, R-160, R-162, R-163, R-164, R-165, R-167 | 21 |
| `pasos/paso-04.md` | R-180, R-181, R-182, R-183, R-184, R-185, R-186, R-189, R-192, R-194 | 10 |
| `pasos/paso-05.md` | R-201, R-202, R-203, R-207, R-209, R-212 | 6 |
| `pasos/paso-06.md` | R-217, R-218, R-220, R-221 | 4 |
| `pasos/paso-07.md` | R-225, R-226, R-227, R-228, R-229, R-232, R-235 | 7 |
| `pasos/paso-08.md` | R-240, R-241, R-243, R-244 | 4 |
| `pasos/paso-09.md` | R-301, R-304, R-306 | 3 |
| `pasos/paso-10.md` | R-324, R-329, R-330 | 3 |
| `pasos/paso-11.md` | R-351, R-354, R-355, R-356, R-361 | 5 |
