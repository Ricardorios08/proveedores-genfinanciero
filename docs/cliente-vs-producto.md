# Cliente o producto

Qué reglas y datos del módulo pertenecen al cliente (OSEP), cuáles al producto (GEN Financiero y la plataforma ACPS) y cuáles solo se sospechan de uno u otro (CA16). Sirve para decidir qué se lleva al rediseño como configuración o contenido propio del cliente y qué es comportamiento del producto.

**Criterio.** Es **cliente** lo que nombra a OSEP, a su área o a su jurisdicción, o lo que un comentario del código limita a un cliente. Es **producto** lo que cualquier instalación tendría que tener igual. Es **sospechado** lo que depende de una configuración o de un texto que suena a una institución pública pero no la nombra: la evidencia no alcanza para asignarlo.

Todo texto de OSEP fijo en el código es de clase accidente (convenciones.md): un dato de un cliente escrito en un objeto del producto. Acá no se transcribe el nombre de la persona de contacto ni la dirección: alcanza con decir que existe y dónde.

## Reglas con dato de cliente fijo en el código

| Regla | De quién es | Evidencia | Bloque |
|---|---|---|---|
| **R-541** Una leyenda del anexo II, en el paso 10 (`hprvir10`), tiene escrito en el código el nombre de OSEP, el área de compras que recibe los originales y su dirección postal, más una condición para proveedores de otra provincia. La persona que atiende sale del atributo ANEXOVERACIDAD (R-523). | cliente | Un solo texto fijo, repetido tal cual en el XML y en el Java. Es el único objeto de la clausura donde aparece el nombre de OSEP. | [V · capas: código, diseño · ev: hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start · clase: accidente] |
| **R-542** El enlace al boletín oficial que arma la pantalla de notificaciones del proveedor (`hprvir53`, rutina ARMALINKBOLETIN) apunta a un sitio del gobierno provincial escrito en el código. | cliente | El dominio es del gobierno de la provincia del cliente; no se transcribe. | [V · capas: código · ev: hprvir53_impl.java S112 ('ARMALINKBOLETIN') · clase: accidente] |
| **R-543** Los correos de vencimiento de `pprvir29` tienen escritos en el código la dirección y el nombre del remitente, el enlace al boletín y la carpeta de adjuntos, todos en un dominio del proveedor del software. | sospechado | Un dominio fijo que no es de una instalación en particular: podría ser del producto, pero lo escribió alguien para un ambiente concreto. | [V · capas: código · ev: pprvir29.java privateExecute · clase: accidente] |
| **R-544** `pprvir99` graba como remitente en el registro de envíos una dirección de pruebas fija que no es del cliente ni del proveedor. No es un destino: el correo sale por Services. | producto | Dato de un ambiente de desarrollo escrito en un objeto de producción. Nada del código lo usa para enviar. | [V · capas: código · ev: pprvir99.java privateExecute · clase: accidente] |
| **R-545** El prefijo con que el módulo forma el código de usuario en Services está escrito como literal en seis objetos (`tprvinsrp0001`, `tprvinsrp`, `pprvsendmsg`, `tprvinsrp0002`, `loginprov002` y `loginrecuperarpwd`), además de estar en el dominio `ParmModPrv` (R-526). | producto | Lógica duplicada: un cambio de prefijo obliga a tocar seis objetos y el dominio no lo evita. | [V · capas: código · ev: tprvinsrp0001.java privateExecute; pprvsendmsg.java privateExecute; tprvinsrp0002.java privateExecute; loginprov002.java S111; loginrecuperarpwd_impl.java S112 ('RECUPERARPWD'); tprvinsrp_impl.java standaloneNotModal · clase: accidente] |

## Reglas con texto o código fijo de origen dudoso

| Regla | De quién es | Evidencia | Bloque |
|---|---|---|---|
| **R-546** El mensaje interno de bienvenida del alta sale con origen fijo CADMIN y con dos códigos fijos (LICIT y AP). Si la instalación no tiene ese usuario o esos códigos, el mensaje queda mal armado o no se ve. | sospechado | Tres literales sin parámetro. Nada en el código dice si son de GEN o de cada instalación. | [V · capas: código · ev: tprvinsrp0001.java privateExecute · clase: parche] |
| **R-547** El asunto y el cuerpo del correo de bienvenida están escritos en el código (`tprvinsrp0001`), mientras que el resto de las notificaciones usa canales cuyas plantillas viven en Services. | producto | Es la excepción del módulo: el texto no nombra a ningún cliente, pero tampoco se puede cambiar sin recompilar. | [V · capas: código · ev: tprvinsrp0001.java privateExecute · clase: parche] |
| **R-548** Los asuntos de los mensajes de canal del alta y de la habilitación están escritos en el código, y el del alta habla de "Proveedor del Estado". | sospechado | El texto sugiere un cliente del sector público, pero no lo nombra; no hay evidencia de que otras instalaciones lo vean igual. La clase es la de por defecto. | [V · capas: código, diseño · ev: hprvir09_impl.java e13AI2 ('Confirmar'); pprvir04.java privateExecute; XPZ HPrvIR09 Events 'Confirmar' · clase: esencial] |

## Reglas definidas en otros archivos, clasificadas acá

La regla vive en el archivo que se cita; esta tabla solo dice de quién es.

| Regla | De quién es | Evidencia | Bloque |
|---|---|---|---|
| R-522 (`configuracion.md`): el paso 11 ofrece la descarga del Formulario de Inscripción solo si COMPRAS_HABFORMULARIO vale S. | cliente | El comentario del XML dice que la opción es, por ahora, de un solo cliente. | [V · capas: código, diseño · ev: hprvir09_impl.java e11AI2 (Start); XPZ HPrvIR09 Events Start (comentario)] |
| R-521 (`configuracion.md`): la cuenta bancaria es obligatoria solo si COMPRAS_OBLIGACTABCO vale S. | sospechado | Que sea configurable indica que no todas las instalaciones lo quieren igual; el código no dice cuáles. | [V · capas: código, diseño · ev: hprvir22_impl.java e1525M2 (Start); XPZ HPrvIR22 Events Start] |
| R-524 (`configuracion.md`): la habilitación provisoria solo se ofrece si HAB_PROVISORIA vale S. | sospechado | Atributo configurable que ni el export ni la rev2 mencionan; el código no dice quién lo usa. | [V · capas: código · ev: hprvir25_impl.java e13A42 (Start)] |
| R-520 y R-523 (`configuracion.md`): los anexos de documentación y de veracidad se muestran según ANEXODOCUMENTACION y ANEXOVERACIDAD. | sospechado | Dos atributos configurables que gobiernan texto del cliente (R-541); el mecanismo es del producto, el contenido del cliente. | [V · capas: código, diseño · ev: hprvir02_impl.java e115A2 (Start); hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start] |
| R-526 a R-540 (`configuracion.md`): los nombres de canal, parámetros y perfil de `ParmModPrv`. | producto | Constantes del módulo, iguales en cualquier instalación. Lo que cada canal dice es contenido de Services, que no se revisó. | [V · capas: código, diseño · ev: gxdomainparmmodprv.java; XPZ objeto ParmModPrv (dominio)] |
| R-519 (`configuracion.md`): la cuenta de servicio del portal sale de USUPORTALWEB. | producto | El mecanismo es de la plataforma; el valor es de cada instalación y no se documenta. | [V · capas: código, diseño · ev: hprvir02_impl.java e115A2 (Start); tprvinsrp0001.java privateExecute] |
