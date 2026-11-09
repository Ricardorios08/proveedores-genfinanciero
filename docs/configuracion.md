# Configuración

Qué lee el módulo de la configuración del ambiente (CA13): atributos de sistema, atributos de usuario, las claves del dominio `ParmModPrv` y las claves de la configuración de Services que usa la capa de acceso. Cada fila dice el nombre, quién lo lee y qué cambia. **Nunca el valor.** Tampoco el ejemplo de formato que el código trae como comentario para USUPORTALWEB.

**Cómo se resuelve un atributo de sistema.** `acpsgetsysattvalue` pasa por `acpsgetsystemattvalue`, que busca primero en la caché general; si no está, lee la propiedad del archivo de configuración de Services con el mismo nombre; si tampoco está, toma el atributo del sistema en el contexto de ACPS. El resultado se guarda en la caché general; el código revisado no muestra cuándo se vacía. El nombre del archivo de configuración lo resuelve `acpsconfigfilename`.

- La resolución de un atributo de sistema pasa por tres fuentes en este orden: caché general, archivo de configuración y atributo del contexto de ACPS. [V · capas: código · ev: acpsgetsystemattvalue.java privateExecute; acpsgetsysattvalue.java privateExecute]
- El módulo lee seis atributos de sistema distintos. La rev2 lista cinco porque solo cubría los objetos del export: el sexto, HAB_PROVISORIA, está únicamente en `fin/`. [V · capas: código, diseño · ev: hprvir25_impl.java e13A42 (Start); XPZ HPrvIR02, HPrvIR22, HPrvIR10 y HPrvIR09 Events Start]

## Atributos de sistema

| Id | Nombre | Quién lo lee | Efecto | Bloque |
|---|---|---|---|---|
| **R-519** | USUPORTALWEB | `hprvir02` (Start) y `tprvinsrp0001` | Contiene la credencial de la cuenta de servicio del portal: el código la parte en las subclaves usr, pass y passEncryp. Si passEncryp vale S, la clave se descifra con `crontab9016` antes de autenticar. Si falta el usuario o la clave, solo escribe un mensaje en la consola del servidor y sigue sin contexto. Ver `seguridad.md`. | [V · capas: código, diseño · ev: hprvir02_impl.java e115A2 (Start); tprvinsrp0001.java privateExecute; XPZ HPrvIR02 Events Start · clase: esencial] |
| **R-520** | ANEXODOCUMENTACION | `hprvir02` (Start) y `hprvir44` (Start) | En `hprvir02`, si vale S muestra la tabla del anexo de documentación del paso 1; si no, la oculta. En `hprvir44`, si no vale S o la rutina HAYPERDOC da cero, oculta el filtro y las columnas por documento. La clase es la de por defecto: no hay evidencia de quién lo usa. | [V · capas: código, diseño · ev: hprvir02_impl.java e115A2 (Start); hprvir44_impl.java e162842 (Start); XPZ HPrvIR02 Events Start · clase: esencial] |
| **R-521** | COMPRAS_OBLIGACTABCO | `hprvir22` (Start y 'Siguiente') | Si vale S, la cuenta bancaria es obligatoria: 'Siguiente' corta con el mensaje de error si no hay ninguna cuenta, y se intercambian cuatro textos de la pantalla según el modo. Si no vale S, el paso avanza sin cuentas. La clase es la de por defecto: la evidencia no dice qué instalaciones lo usan. | [V · capas: código, diseño · ev: hprvir22_impl.java e1525M2 (Start) y e1225M2 ('Siguiente'); XPZ HPrvIR22 Events Start · clase: esencial] |
| **R-522** | COMPRAS_HABFORMULARIO | `hprvir09` (Start) | Si vale S, el paso 11 muestra el grupo que invita a descargar el Formulario de Inscripción y a adjuntarlo en la documentación del proveedor. El comentario del XML dice que, por ahora, lo usa un solo cliente (que nombra con una sigla). | [V · capas: código, diseño · ev: hprvir09_impl.java e11AI2 (Start); XPZ HPrvIR09 Events Start (comentario) · clase: parche] |
| **R-523** | ANEXOVERACIDAD | `hprvir10` (Start) y `hprvir45` (Start) | En `hprvir10`, si está vacío oculta el grupo del anexo II; si no, lo muestra y su contenido pasa a ser el nombre de la persona que atiende, que se inserta en una leyenda fija de la pantalla (ver `cliente-vs-producto.md`). En `hprvir45`, si está vacío oculta dos textos del anexo. La clase es la de por defecto. | [V · capas: código, diseño · ev: hprvir10_impl.java e11F02 (Start); hprvir45_impl.java e112892 (Start); XPZ HPrvIR10 Events Start · clase: esencial] |
| **R-524** | HAB_PROVISORIA | `hprvir25` (Start y Proveedores_Load) | Si no vale S, la grilla de habilitación oculta las acciones de habilitación provisoria y de revertirla. No figura en el export ni en la rev2. La clase es la de por defecto. | [V · capas: código · ev: hprvir25_impl.java e13A42 (Start) y e11A42 (Proveedores_Load) · clase: esencial] |

## Atributo de usuario

| Id | Nombre | Quién lo lee | Efecto | Bloque |
|---|---|---|---|---|
| **R-525** | CUCPORDEFECTO | `tprvinsrp0001`, vía `acpsgetuserattvalue` | Lee el valor que la cuenta de servicio autenticada tiene para este atributo y lo copia como atributo del usuario nuevo del proveedor en Services. Si el login de la cuenta falló, el contexto está vacío y el atributo va vacío. La clase es la de por defecto. | [V · capas: código · ev: tprvinsrp0001.java privateExecute · clase: esencial] |

## Claves de ParmModPrv

`ParmModPrv` es un dominio de cadenas fijas, no una tabla editable: cada miembro tiene un nombre (el de esta columna) y un literal que el generador copia en el Java. Los literales no se transcriben acá; están en `gxdomainparmmodprv.java`. Como el dominio queda inlineado, el Java no "lee" nada en tiempo de ejecución: cada objeto trae su copia.

| Id | Clave | Quién la usa | Efecto | Bloque |
|---|---|---|---|---|
| **R-526** | ServicesPrefijoUsuarios | `tprvinsrp` (fórmula `PrvPUsrSrv`), `tprvinsrp0001`, `tprvinsrp0002`, `pprvsendmsg`, `loginprov002` y `loginrecuperarpwd` | Se antepone al usuario del proveedor para formar su código de usuario en Services. También se usa para reconocer en la sesión a un proveedor y para quitarlo de los mensajes de error que se muestran. | [V · capas: código, diseño · ev: tprvinsrp_impl.java standaloneNotModal; tprvinsrp0001.java privateExecute; loginprov002.java S111; XPZ atributo PrvPUsrSrv (fórmula) · clase: esencial] |
| **R-527** | ServicesPerfilProveedor | `tprvinsrp0001` | Perfil de Services que recibe el usuario del proveedor al crearlo. | [V · capas: código · ev: tprvinsrp0001.java privateExecute · clase: esencial] |
| **R-528** | ServicesUsuarioGestion | `hprvir09` ('Confirmar'), `pprvir04` y `tprvinsrp0001` | Remitente de los mensajes de canal del alta y de la habilitación. En `tprvinsrp0001` identifica además el proceso que opera sobre el usuario en Services. | [V · capas: código, diseño · ev: hprvir09_impl.java e13AI2 ('Confirmar'); pprvir04.java privateExecute; tprvinsrp0001.java privateExecute; XPZ HPrvIR09 Events 'Confirmar' · clase: esencial] |
| **R-529** | CanalRegistro | `hprvir09` ('Confirmar') | Canal del mensaje del alta, pero solo como respaldo: primero toma el código de sistema de la tabla `ACPSParm` y solo si viene vacío usa esta clave. | [V · capas: código, diseño · ev: hprvir09_impl.java e13AI2 ('Confirmar'); XPZ HPrvIR09 Events 'Confirmar' · clase: esencial] |
| **R-530** | CanalHabilitacion | `pprvir04` | Canal del mensaje de habilitación definitiva. | [V · capas: código · ev: pprvir04.java privateExecute · clase: esencial] |
| **R-531** | CanalCertificado | `hprvir28` (rutina ENVIARMAIL) | Canal del mensaje de renovación del certificado. | [V · capas: código · ev: hprvir28_impl.java S112 ('ENVIARMAIL') · clase: esencial] |
| **R-532** | CanalReinscripcion | `hprvir40` (rutina ENVIARMAIL) | Canal del mensaje cuando la habilitación pendiente es una reinscripción (estado R). | [V · capas: código · ev: hprvir40_impl.java S112 ('ENVIARMAIL') · clase: esencial] |
| **R-533** | CanalUpdateDatos | `hprvir40` (rutina ENVIARMAIL) | Canal del mensaje en cualquier otro caso de habilitación de modificaciones. | [V · capas: código · ev: hprvir40_impl.java S112 ('ENVIARMAIL') · clase: esencial] |
| **R-534** | CanalPresentarDocResp | `tprvinsrp` (Start, cuando el proveedor modifica sus datos), `hprvir35` ('guardar') y las transacciones `tprvesp`, `tprvrpr`, `tprvrub`, `tprvpj`, `tprvdom` y `tprvpod` | Canal del aviso de que hay que presentar documentación respaldatoria. La rev2 solo menciona a `TPrvInsRP`; el Java lo arma en ocho objetos y la condición exacta de los siete restantes no se analizó. | [V · capas: código, diseño · ev: tprvinsrp_impl.java e11IZ2 (Start); hprvir35_impl.java e12BA2 ('guardar'); tprvesp_impl.java; tprvdom_impl.java; XPZ TPrvInsRP Events · clase: esencial] |
| **R-535** | CanalDatosIncompletos | `hprvir38` ('Notificar') | Canal del aviso a los proveedores con inscripción incompleta. | [V · capas: código · ev: hprvir38_impl.java e14A72 ('Notificar') · clase: esencial] |
| **R-536** | ParamUsuario | `hprvir09` ('Confirmar') y `pprvir04` | Nombre del parámetro que lleva el usuario en el mensaje de canal. | [V · capas: código, diseño · ev: hprvir09_impl.java e13AI2 ('Confirmar'); pprvir04.java privateExecute; XPZ HPrvIR09 Events 'Confirmar' · clase: esencial] |
| **R-537** | ParamNombre | `hprvir09` ('Confirmar') y `pprvir04` | Nombre del parámetro que lleva el nombre del proveedor. | [V · capas: código, diseño · ev: hprvir09_impl.java e13AI2 ('Confirmar'); pprvir04.java privateExecute; XPZ HPrvIR09 Events 'Confirmar' · clase: esencial] |
| **R-538** | ParamFecha | `pprvir04` | Nombre del parámetro que lleva la fecha de vencimiento del certificado en el mensaje de habilitación. | [V · capas: código · ev: pprvir04.java privateExecute · clase: esencial] |
| **R-539** | ParamPassword | `pprvir04` | Nombre del parámetro de clave en el mensaje de habilitación. El valor que se manda es siempre vacío: la variable que lo carga se inicializa y nunca se asigna. Es un resto de cuando el mensaje llevaba la clave. | [V · capas: código · ev: pprvir04.java privateExecute · clase: accidente] |
| **R-540** | ParamRepositorio | `pprvperfildoc002` | Nombre del repositorio documental de Services donde se guarda la documentación del proveedor. | [V · capas: código · ev: pprvperfildoc002.java privateExecute · clase: esencial] |

## Claves de la configuración de Services

Las lee la capa de acceso (`acpsrestparm`, `acpsrestroute`) cada vez que el módulo llama a Services. No son atributos de sistema ni del módulo, pero sin ellas ninguna integración de `integraciones.md` funciona. Solo nombres.

| Clave | Quién la lee | Efecto | Bloque |
|---|---|---|---|
| ENDPOINTSERVICES:BASEURL | `acpsrestparm` | Parte fija de la ruta de los recursos | [V · capas: código · ev: acpsrestparm.java privateExecute] |
| ENDPOINTSERVICES:HOST | `acpsrestparm` | Servidor de Services | [V · capas: código · ev: acpsrestparm.java privateExecute] |
| ENDPOINTSERVICES:PORT | `acpsrestparm` | Puerto de Services | [V · capas: código · ev: acpsrestparm.java privateExecute] |
| ENDPOINTSERVICES:SECURE | `acpsrestparm` | Si la conexión es segura | [V · capas: código · ev: acpsrestparm.java privateExecute] |
| ENDPOINTSERVICES:TIMEOUT | `acpsrestparm` | Tiempo máximo de espera de cada llamada | [V · capas: código · ev: acpsrestparm.java privateExecute] |
| ENDPOINTSERVICES:ACPSCRUDUSERSRESOURCE | `acpsrestroute` | Ruta del recurso de usuarios (R-501) | [V · capas: código · ev: acpsrestroute.java privateExecute; acpsrcrudusers.java privateExecute] |
| ENDPOINTSERVICES:ACPSUSERAUTHORIZATIONRESOURCE | `acpsrestroute` | Ruta del recurso de autenticación (R-502) | [V · capas: código · ev: acpsrestroute.java privateExecute; acpsrauthorizeuser.java privateExecute] |
| ENDPOINTSERVICES:ACPSDELIVEREMAILRESOURCE | `acpsrestroute` | Ruta del recurso de correo (R-503) | [V · capas: código · ev: acpsrestroute.java privateExecute; acpsrdeliveremail.java privateExecute] |
| ENDPOINTSERVICES:ACPSCRUDMESSAGESRESOURCE | `acpsrestroute` | Ruta del recurso de mensajes de canal (R-504) | [V · capas: código · ev: acpsrestroute.java privateExecute; acpsrcrudmessages.java privateExecute] |
| ENDPOINTSERVICES:ACPSGETDOCUMENTSRESOURCE | `acpsrestroute` | Ruta del recurso de lectura de documentos (R-505) | [V · capas: código · ev: acpsrestroute.java privateExecute; acpsrgetdmdocuments.java privateExecute] |
| ENDPOINTSERVICES:ACPSSENDDOCUMENTRESOURCE | `acpsrestroute` | Ruta del recurso de adjuntos (R-506) | [V · capas: código · ev: acpssenddmdocumentattachment.java privateExecute] |
| ENDPOINTSERVICES:ACPSINSERTDOCUMENTVERSIONRESOURCE | `acpsrestroute` | Ruta del recurso de versiones de documento (R-507) | [V · capas: código · ev: acpsrestroute.java privateExecute; acpsrinsertdmdocumentversion.java privateExecute] |
| ENDPOINTSERVICES:ACPSCHANGEPASSWORDRESOURCE | `acpsrestroute` | Ruta del recurso de cambio de clave (R-508) | [V · capas: código · ev: acpsrestroute.java privateExecute; acpsrchangepassword.java privateExecute] |
