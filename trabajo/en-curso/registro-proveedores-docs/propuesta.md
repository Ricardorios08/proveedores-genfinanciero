# registro-proveedores-docs — Propuesta

**Estado:** aprobada por responsable del proyecto el 2026-10-23; enmienda 1 aprobada el mismo día
**Fecha:** 2026-10-19 (revisada el mismo día, después de leer el XPZ extraído; 2026-10-23: fuentes por capa y formatos de recon; 2026-10-23, enmienda 1: el propósito pasa a ser la reingeniería, y se corrigen hechos)

> **Enmienda 1 (2026-10-23).** El responsable no conoce el flujo completo y no va a estudiarlo: la ingeniería inversa existe para que no tenga que hacerlo. Las decisiones de rediseño las toma él solo. Por eso el producto central pasa a ser **la lista de decisiones de rediseño**, y lo que ya estaba (inventarios, pasos, modelo de datos) queda como respaldo de esas decisiones. Una revisión independiente encontró además tres errores de hecho, que se corrigen en el texto: `RPrvIR63` está comentado, la "discrepancia" del paso 6 no existe y `HPrvIR21` está en `fin/`. Cambian "Qué tiene que pasar", CA4, CA6, CA9, CA11, CA12 y la pregunta 3, y se suman CA21 a CA24.

## Por qué

La fase 2 reimplementa el módulo Registro de Proveedores de GEN Financiero con React, PostgreSQL y LoopBack. Hoy su comportamiento está repartido en tres fuentes que nadie leyó juntas:

- el manual de usuario (`contexto/Manual Registro de Proveedores Portal.pdf`, 28 páginas);
- el export GeneXus (`contexto/GENFin-RegProv.xpz`), extraído fuera del repositorio en `genfin-gx-extraido/xpz/GENFin-RegProv.xml`;
- el Java generado de todo GENFin (`contexto-local/fin.zip`), extraído el 2026-10-22 en `genfin-gx-extraido/fin/`.

Quien escriba `db/`, `api/` o `app/` no tiene de dónde sacar qué entidades hay, qué valida cada paso ni cuándo un proveedor queda habilitado. Si arranca solo desde el manual, hereda sus errores: contrastado con el código, el manual ya falla en varios puntos (ver "Lo que dice el XPZ").

### Lo que dice el XPZ (leído el 2026-10-19)

Conteos hechos sobre el XML extraído (export KMW 4.0, build 180599, KB `GENFin18U8`). Los conteos cuentan los elementos `<Object>` y `<Attribute>` de primer nivel.

- **Contenido:** 119 objetos y 194 atributos.
  - 10 web panels: `HPrvIR02`, `HPrvIr07`, `HPrvIR17m`, `HPrvIR41`, `HPrvIR18`, `HPrvIR42`, `HPrvIR06`, `HPrvIR22`, `HPrvIR10`, `HPrvIR09`.
  - 1 transacción: `TPrvInsRP`.
  - 1 tabla: `PrvPerfil`, con clave `PrvPUSr` y 7 índices.
  - 20 SDT y 87 dominios.
- **Los 11 pasos tienen objeto (verificado).** Cada paso se ubica por su texto "PASO n de 11": paso 1 `HPrvIR02`, 2 `HPrvIr07`, 3 `TPrvInsRP`, 4 `HPrvIR17m`, 5 `HPrvIR41`, 6 `HPrvIR18`, 7 `HPrvIR42`, 8 `HPrvIR06`, 9 `HPrvIR22`, 10 `HPrvIR10`, 11 `HPrvIR09`.
- **El export está incompleto. Es el hallazgo principal.** El código exportado llama a objetos que no vienen en el export:
  - 6 transacciones que guardan las entidades hijas: `TPrvPJ` (integrantes), `TPrvDom`, `TPrvESP`, `TPrvRub`, `TPrvRpr` y `TPrvBco`. De sus atributos se exportó la definición (por ejemplo `PrvDom*`, `PrvBco*`, `PrvRub*`), pero no la estructura: no se sabe en qué tabla está cada uno ni cuál es su clave.
  - Unos 30 procedimientos. Entre ellos están el validador del dígito del CUIT (`PNuPro04`), la consulta del estado del proveedor (`PPrvIR02`, `PPrvIR03`, `PPrvIR05`), el alta del usuario en Services (`TPrvInsRP0001`), el cifrado de la contraseña (`RGXPEncriptaPrv`), la validación del mail (`PPrvIR39`) y el envío de mensajes (`PPrvSendMsg`).
  - El panel `HPrvIR39`, que todo indica que es el menú "Modificar los Datos Registrados".

  La lista de referencias que trae el propio export (`ObjectsIdentityMapping`) no se usa como inventario: describe lo que GeneXus registró, no lo que el código llama. *(Corregido por la enmienda 1. El texto original decía que `RPrvIR63` "se llama en el paso 6 y no figura en ella". Es falso: su única aparición en el XML está dentro de un bloque comentado del evento `Siguiente` de `HPrvIR18`, y `hprvir18_impl.java` no lo nombra. Que no figure es lo esperable. Las llamadas vivas a `rprvir63` están en `hprvir39_impl.java` y `hprvir52_impl.java`.)* El inventario de dependencias sale de las llamadas en el código, separando las activas de las que solo están en comentarios.
- **Los mismos paneles sirven para tres cosas.** Una variable `&Modulo` elige el modo: `I` es el alta, `P` es el proveedor ya inscripto modificando sus datos y `A` es la administración. Según un comentario del paso 9, el modo `A` se llamaría desde `HPrvIR21`, que no está en el export; las llamadas a `HPrvIR21` están comentadas.
- **Estados.** El paso 1 distingue los estados que devuelve `PPrvIR02`: `H`, `E`, `Q`, `N`, `F`, `P`, `A`, `X`, `T` y `G`. `G` ("Agente del Estado") se usa en el código pero falta en el comentario que enumera los valores. `PrvPHabCS` arranca en `N` (pendiente) y pasa a `Q` cuando el proveedor modifica sus datos.
- **Partes del comportamiento dependen de la configuración.** Hay atributos de sistema (`USUPORTALWEB`, `ANEXODOCUMENTACION`, `ANEXOVERACIDAD`, `COMPRAS_OBLIGACTABCO`, `COMPRAS_HABFORMULARIO`) y parámetros de `ParmModPrv` (canales de mensajería, usuario de gestión, prefijo de usuarios).
- **Hay texto del cliente escrito en el código.** El paso 10 tiene la dirección de la oficina de OSEP Mendoza fija en el código, y el nombre de la persona de contacto sale de un atributo de sistema.
- **Discrepancias ya confirmadas entre manual y código:**
  - Paso 2, largo del nombre de usuario: la pantalla dice "entre 5 y 20". El código exige al menos 5, y el dominio `ACPSUsuario` permite hasta 30.
  - ~~Paso 6: el título dice "Dato No Obligatorio", pero el código no deja avanzar sin el último ejercicio.~~ *(Retirada por la enmienda 1: la validación del último ejercicio está comentada en el XPZ y también en el Java, así que no obliga y el título coincide con el código. No es una discrepancia. Sí es un candidato a "accidente": una validación desactivada que sigue en el código.)*
  - Paso 9: el manual lo presenta como opcional. En el código es obligatorio cuando `COMPRAS_OBLIGACTABCO = 'S'`.
  - Paso 1: el manual no menciona el caso "Agente del Estado".
- **Seguridad, a documentar tal como está:** la contraseña inicial es un número pseudoaleatorio de 8 dígitos (`Random()`), y se cifra con un procedimiento que no viene en el export.

### Fuentes, por capa (agregado 2026-10-23)

Las fuentes no se cuentan una por una sino por **capa**: dos fuentes de la misma capa repiten la misma mirada, y su acuerdo no confirma nada. Lo que vale es el acuerdo, o la contradicción, entre capas distintas.

| Capa | Fuentes | Qué prueba | Qué no prueba |
|---|---|---|---|
| Diseño | Agente GeneXus (ATLAS, vía MCP) y el XML del XPZ | Lo que se definió en la KB | Que se haya compilado así. Las dos fuentes son **la misma KB**: el agente tiene importado el mismo `.xpz`, así que cuentan como una |
| Código generado | Java de `fin.zip` | Lo que efectivamente se compiló. Una validación comentada no aparece (la del paso 6 está comentada en las dos capas) | La regla tal como la escribió el desarrollador, ni la versión exacta respecto del XPZ (ver pregunta 1) |
| Ejecución | Agente de navegación (`agent-browser`) sobre el portal de test | Lo que pasa de verdad: pantallas, estados, mensajes, correos | Por qué pasa. Además, depende de la configuración de ese ambiente (atributos de sistema, `ParmModPrv`) |
| Intención | Manuales PDF | Lo que el usuario cree que hace el módulo | Lo que hace |

Una contradicción entre dos capas es un hallazgo, no ruido: va a la sección de discrepancias (CA14). *(Enmienda 1: el texto original citaba el paso 6 como ejemplo de una discrepancia entre diseño y código. Era falso; ver "Discrepancias ya confirmadas".)*

**Descartado:** un agente de ingeniería inversa del sistema (REA, `morluto/rea`). Analiza binarios y apps sin código fuente; acá el código generado ya está disponible, así que no agrega una capa nueva y reconstruiría con menos fidelidad lo que se lee directo.

**Formatos de recon.** El inventario de pantallas, los flujos y la matriz de funcionalidades toman el formato de `replica-recon` (`Jakeschincariol/replica-skill`, MIT): ids estables `S01…` y `F01…`, estados por pantalla, casos borde por flujo y una matriz `features.csv` con prioridad. Se adoptan **las plantillas, no la skill**: sus reglas son de clean-room y prohíben leer código fuente, que acá es la capa más precisa. Nada de ese repositorio se instala.

## Qué tiene que pasar

*(Reescrito por la enmienda 1.)* El responsable puede decidir **qué se mantiene, qué se rediseña y qué se elimina** de los flujos del módulo **sin estudiar el sistema original**. Lo que lo hace posible, en orden de lectura:

1. **Un mapa de flujos** que se lee en minutos: los 11 pasos, los tres modos y las retomas, con los puntos de dolor marcados.
2. **Una lista de decisiones de rediseño.** Cada una dice qué hace hoy el sistema, por qué parece esencial, parche o accidente, qué se pierde si se saca, y trae una recomendación.
3. **El respaldo:** la descripción del módulo en `docs/` (pasos, modos, modelo de datos, estados, integraciones, configuración), con la que se puede verificar cada decisión sin abrir el XPZ ni el PDF. Cada afirmación dice de qué fuente sale, de qué capa es y si se comprobó. Lo que falta en las fuentes queda escrito como hueco, con lo que haría falta para cerrarlo.

Además quedan tres artefactos que la fase 2 usa directamente: el inventario de pantallas, el de flujos y la matriz de funcionalidades. La matriz registra la decisión tomada sobre cada funcionalidad, y después mide cuánto le falta a la reimplementación **respecto de esa decisión**, no respecto del original.

## Criterios de aceptación

| # | Criterio | Caso de error |
|---|---|---|
| CA1 | `docs/README.md` lista cada documento de `docs/` con una línea que dice qué cubre | Si un archivo de `docs/` no figura en el índice, o el índice nombra un archivo que no existe, la revisión lo rechaza |
| CA2 | Existe un inventario de los objetos y atributos del XPZ, sacado del XML (no armado a mano), con el conteo por tipo GeneXus y el comando con que se contó | Si el conteo no coincide con el que mida de nuevo quien revise, el inventario se marca incompleto |
| CA3 | Cada objeto del inventario está clasificado como "documentado en <archivo>" o "fuera de alcance: <motivo>" | Si un objeto queda sin clasificar, se informa como hueco de cobertura |
| CA4 | Existe un inventario de los objetos que el código exportado llama y que no están en el export, sacado de las llamadas en el código y no de `ObjectsIdentityMapping`. Separa las llamadas **activas** de las que están **solo en comentarios** *(enmienda 1)* | Control de las activas: `TPrvESP` (llamada viva en `HPrvIR18`). Control de las comentadas: `RPrvIR63`. Controles negativos: un objeto presente (`HPrvIR42`) y una función nativa (`StrReplace`) no deben aparecer. *(Ajuste del 2026-10-23, durante A3: el control original usaba `Msg`, que el filtro de forma del script descarta antes de mirar la lista de nativas, así que no podía fallar. `StrReplace` sí lo usa el export y pasa el filtro.)* Si falla cualquiera de los cuatro, el método se rechaza |
| CA5 | Cada objeto del inventario de CA4 dice de dónde salió lo que se documenta de él (otro export, `fin.zip` o nada) | Si no hay fuente, el objeto se lista como hueco y todo lo que dependa de él se marca **sospechado** |
| CA6 | Cada uno de los 11 pasos del alta tiene una sección con su objeto GeneXus, los datos que pide, sus validaciones y la condición que lleva al paso siguiente | Si una validación vive en un objeto que no está en ninguna fuente (ni el export ni `fin/`), se marca **sospechado** y se nombra ese objeto *(enmienda 1: decía "en el export")* |
| CA7 | Para cada panel que tiene los modos `P` y `A`, una sección describe qué cambia respecto del modo `I` | Si el punto de entrada de un modo no está en ninguna fuente, se dice así, sin inventar el flujo. *(Enmienda 1: `HPrvIR39` y `HPrvIR21` sí están en `fin/`, y la cadena del modo `A` es `popro001 → hprvir25/40 → hprvir21 → paneles`)* |
| CA8 | Cada entidad del módulo figura en el modelo de datos con sus atributos y el tipo de cada uno (sacado de su dominio o de su definición) | Si un atributo no tiene tipo en la fuente, se marca **sospechado** |
| CA9 | Cada entidad del modelo de datos dice su tabla y su clave, citando de qué objeto salen | Si la clave no está en ninguna fuente, se marca **sospechado** y no se deduce de los nombres. *(Enmienda 1: las claves de las 6 hijas `TPrvPJ`, `TPrvDom`, `TPrvESP`, `TPrvRub`, `TPrvRpr` y `TPrvBco` salen del `DELETE ... WHERE` de su `_impl.java`)* |
| CA10 | Cada valor de estado (los del flag que devuelve `PPrvIR02` y los de `PrvPHabCS`) figura con su significado y con qué lo asigna | Si un valor se usa en el código sin figurar en el comentario que los enumera (por ejemplo `G`), se anota como discrepancia (CA14) |
| CA11 | Cada punto de contacto con el resto de GEN Financiero o con ACPS Services figura con su dirección (lee o escribe) y con el objeto que lo implementa. Por ejemplo: la tabla de proveedores de GEN, el usuario en Services, la mensajería | Si el objeto no está en ninguna fuente, se marca **sospechado** *(enmienda 1: decía "en el export")* |
| CA12 | Cada correo o mensaje que envía un objeto del módulo, o que Services envía por pedido del módulo, figura con el evento que lo dispara, el canal (`ParmModPrv.*`) y el asunto *(enmienda 1: universo acotado al módulo)* | Si el envío aparece en el manual sin objeto que lo haga (por ejemplo, el mail con la contraseña inicial), se marca **sospechado** |
| CA13 | Cada atributo de sistema y cada parámetro de `ParmModPrv` que lee el módulo figura con su efecto sobre el comportamiento | Si el efecto no se puede leer en el código exportado, se marca **sospechado** |
| CA14 | Hay una sección de discrepancias entre capas (diseño, código generado, ejecución, intención), con las dos fuentes citadas en cada una, sus capas y la regla de desempate aplicada | Si otra sección contradice a una fuente sin que esa contradicción figure en esta lista, la revisión lo rechaza. Un acuerdo entre el Agente GeneXus y el XPZ no cuenta como confirmación entre capas |
| CA15 | Cada afirmación sobre el comportamiento lleva su estado (**verificado** o **sospechado**), su evidencia (objeto y parte del XPZ, archivo de `fin.zip`, pantalla `Snn` observada en test con fecha, o página del manual) y las capas que la sostienen | Si una afirmación aparece sin estado, sin evidencia o sin capa, se cuenta como sospechada y se lista |
| CA16 | Las reglas propias del cliente quedan separadas de las del producto. Por ejemplo: textos de OSEP Mendoza fijos en el código, anexos, lista de documentación | Si no se puede saber si una regla es del cliente o del producto, se marca **sospechado** |
| CA17 | Existe un inventario de pantallas con ids estables (`S01`, `S02`…). Una pantalla es un par objeto + modo (`HPrvIR18` en modo `I` y en modo `P` son dos filas si se ven distintas). Cada fila tiene: cómo se llega, objeto GeneXus, modo, propósito, componentes y los estados vistos (vacío, completo, error de validación, sin permiso), cada estado con su capa | Si un estado figura solo en el código y no se vio en test, se marca así; si un panel del inventario de CA2 no tiene pantalla ni motivo de exclusión, se informa como hueco |
| CA18 | Existe un inventario de flujos con ids estables (`F01`…), cada uno con su objetivo, la secuencia de pantallas `Snn`, la cantidad de clicks del camino feliz y sus casos borde. Como mínimo: alta completa, retoma de un alta según cada estado de `PPrvIR02`, modificación de datos (modo `P`) y lo que se pueda del modo `A` (pregunta 4) | Si un flujo no se recorrió en test, dice "solo desde el código" y sus clicks quedan sin contar, no estimados |
| CA19 | Existe `docs/features.csv` con una fila por funcionalidad del módulo y las columnas `feature,area,priority,original,clone,notes` más `capas` y `evidencia`. `priority` es `must`/`should`/`could`, `original` es `yes`/`partial`/`skip` (con motivo en `notes`), y `clone` arranca en `no` para todas las filas. Los nombres de las seis primeras columnas son los de `replica-recon`, para poder medir la paridad de la fase 2 con su `parity.py` sin adaptarlo | Si una funcionalidad documentada en CA6–CA13 no tiene fila, o una fila no tiene evidencia, la revisión lo rechaza |
| CA20 | Cada paso de CA6 y cada flujo de CA18 dice qué capas lo cubren. Si la capa de ejecución no lo cubre, se dice por qué (no se llegó en test, depende de una configuración que test no tiene, requiere un alta no autorizada todavía) | Si un paso queda cubierto solo por la capa de diseño, se marca **sospechado** aunque el Agente GeneXus y el XPZ coincidan |
| CA21 | *(Enmienda 1.)* Existe `docs/mapa-flujos.md`: una página con un diagrama de los 11 pasos, los tres modos y las retomas, y los puntos de dolor marcados con un enlace a su decisión de CA23 | Si un punto de dolor no enlaza a una decisión, o una decisión de CA23 que cambia el flujo no aparece en el mapa, la revisión lo rechaza |
| CA22 | *(Enmienda 1.)* Cada regla documentada en CA6–CA13 está clasificada como **esencial** (la exige el negocio o una norma), **parche** (resuelve un caso puntual y quedó pegada) o **accidente** (código muerto, validación comentada, dato fijo de un cliente, duplicación). La clasificación la propone el análisis, con su evidencia | Si una regla no tiene clase, o la clase no tiene evidencia, cuenta como **sin clasificar** y se lista. La clase es una propuesta: la decisión sobre ella es de CA23 |
| CA23 | *(Enmienda 1.)* Existe `docs/decisiones-rediseno.md`, con una entrada por cada regla o tramo de flujo clasificado como parche o accidente, y por cada discrepancia de CA14. Cada entrada tiene: qué hace hoy (con enlace al respaldo), por qué parece parche o accidente, qué se pierde si se saca, una recomendación (`mantener`, `rediseñar` o `eliminar`), y un campo `decisión del responsable` que arranca vacío | Si una regla parche o accidente de CA22, o una discrepancia de CA14, no tiene entrada, la revisión lo rechaza. Una recomendación sin "qué se pierde" cuenta como incompleta. *(Decidido por el responsable el 2026-10-23.)* Las reglas **esenciales por defecto** (las que tienen poca evidencia) llevan entradas de confirmación rápida, agrupadas por paso. Las esenciales con evidencia van en una sola tabla final de "mantener". Si una esencial no figura en ninguna de las dos, la revisión lo rechaza |
| CA24 | *(Enmienda 1.)* `docs/features.csv` suma la columna `decision` (`mantener`, `rediseñar`, `eliminar` o `pendiente`), que arranca en `pendiente` y se llena desde CA23 | Si una fila tiene `decision` distinta de `pendiente` sin una entrada de CA23 que la respalde, la revisión lo rechaza |

## Qué no se toca

- `contexto/` y `contexto-local/`: se leen, no se modifican. Lo que se extraiga va fuera del repositorio, como el XML actual.
- `app/`, `api/` y `db/`: esta unidad no escribe código, ni esquema, ni migraciones.
- `conocimiento/`: lo actualiza `/archivar` al cerrar.
- El Portal de Compras (búsqueda de compras, ofertas, impugnaciones). Solo se nombra donde el Registro le entrega algo.
- `.claude/` y `trabajo/archivo/`.
- No se instalan skills, plugins ni servidores MCP de terceros (`replica-skill`, REA). De `replica-recon` se toman solo los formatos.

## Restricciones duras

- Lo protegido en la declaración es de solo lectura.
- Credenciales y configuración: en `docs/` aparecen los nombres de los atributos de sistema y de las variables declaradas, nunca sus valores. El ejemplo de formato que trae el código para `USUPORTALWEB` no se copia.
- Datos personales: no se copian los de los manuales ni los del ambiente de test. Tampoco se copian los usuarios de desarrollador que trae el XML en sus metadatos (atributo `user`, ruta UNC) ni el nombre de contacto que llena `ANEXOVERACIDAD`. Si hace falta un ejemplo, se usan valores inventados con una marca que lo diga.
- `docs/` se versiona y `contexto-local/` está en `.gitignore`. Ni el Java generado ni el código GeneXus se copian en bloque: se citan por objeto y parte, y se transcriben solo los fragmentos necesarios.
- Capturas del portal de test: van fuera del repositorio (`genfin-gx-extraido/screens/`), porque pueden mostrar datos del ambiente. En `docs/` se cita la pantalla por su id `Snn` y la fecha de la observación, no se copia la imagen.
- Navegación a ritmo humano, sin bucles ni barridos automáticos, con las credenciales cargadas desde `~/.config/genfin-gx.env` y nunca en la línea de comando.
- El mecanismo de la contraseña inicial se documenta como es, marcado como hallazgo de seguridad. No se presenta como requisito a replicar.
- Todo en español. Fechas en ISO 8601.
- La declaración no define `cierre`: la unidad termina cuando el responsable del proyecto confirma los criterios.

## Preguntas abiertas

1. **(Nueva) ¿De dónde salen los objetos que faltan en el export?** Faltan las 6 transacciones de las entidades hijas, unos 30 procedimientos, `HPrvIR39` y `RPrvIR63`. Esto define el modelo de datos (CA9) y la mitad de las validaciones, así que no puede quedar para después. Opciones:
   - (a) Que una persona haga un segundo export de la misma KB (`GENFin18U8`) con esos objetos.
   - (b) Leerlos en el Java generado de `fin.zip`.
   - (c) Documentarlos como huecos y seguir.

   **Recomiendo (a).** Es la misma fuente, en el mismo formato. Si no se puede, (b), sabiendo que el Java generado muestra lo que hace el código pero no siempre la regla tal como la escribió el desarrollador. Con (c), el modelo de datos sale con la mayoría de las claves **sospechadas**.

   **Decidido (2026-10-22): (b).** (a) no está disponible: el "Agente GeneXus" de ATLAS tiene una KB importada del mismo `.xpz`, sin vínculo con ningún GeneXus Server, y el origen que declara el XPZ no resuelve por DNS. `fin.zip` se extrajo fuera del repositorio, en `genfin-gx-extraido/fin/` (12.654 archivos). Los 9 objetos que faltaban están todos, más los procedimientos que se revisaron (`PNuPro04`, `PPrvIR02/03/05/39`, `TPrvInsRP0001`, `RGXPEncriptaPrv`, `PPrvSendMsg`). Tabla y clave de cada transacción, sacadas del `DELETE ... WHERE` de su `_impl.java`. Control positivo: `PrvPerfil` da `PrvPUSr`, igual que en el XPZ.
   - `TPrvPJ` → `PrvPJ` (`PrvPUSr`, `PrvPJNroInt`)
   - `TPrvDom` → `PrvDom` (`PrvPUSr`, `PrvDomTip`, `PrvDomNroOrden`)
   - `TPrvESP` → `PrvESP` (`PrvPUSr`, `PrvESPFchCie`)
   - `TPrvRub` → `PrvRub` (`PrvPUSr`, `PrvRubNro`, `PrvRubBsSrv`, `PrvRubSubRub`)
   - `TPrvRpr` → `PrvRpr` (`PrvPUSr`, `PrvRprNroLin`)
   - `TPrvBco` → `PrvBco` (`PrvPUSr`, `PrvBcoNroLin`)

   **Versión de las dos fuentes (comprobado en parte):** las entradas de `fin.zip` **no tienen una fecha única**: van del 2025-09-23 al 2026-09-14 (7.242 archivos de 2025-09; 1.643 de 2026-08; 989 de 2026-09), y cada panel tiene la suya (por ejemplo, `hprvir18_impl.java` del 2026-02-04 y `hprvir22_impl.java` del 2026-04-13). *(Enmienda 1: decía "fecha 2026-08".)* La versión se compara objeto por objeto. El XPZ trae `versionDate` de 2020. Se comparó el `INSERT INTO PrvPerfil` del Java (78 columnas) con la estructura de `TPrvInsRP` en el XPZ (62 atributos):
   - 22 columnas están solo en el Java, por ejemplo `PrvPAdminCat`, `PrvPClaseUsr` y `PrvPRstClave`. Las 6 que se revisaron tienen definición en el XPZ y aparecen escritas por otros objetos Java con `UPDATE PrvPerfil`. Eso es compatible con que la tabla sea la unión de varias transacciones.
   - 6 atributos están solo en el XPZ (`PrvPNom`, `PrvPUsrSrv`, `PrvSoc*`). Pueden ser inferidos o fórmulas, que no se guardan como columna.

   No aparece ninguna contradicción, pero tampoco está probado que sean la misma versión. Cada regla que se saque de una sola fuente se cita con esa fuente. El SQL generado usa `SAVEPOINT`, propio de PostgreSQL, así que GENFin ya corre sobre PostgreSQL; falta confirmarlo en `GXcfg.java`.

   **Reparto acordado:** el Agente GeneXus extrae reglas de su KB y del XML del XPZ, y las entrega por paso, con su objeto y su estado. Esta unidad integra eso en `docs/` y cubre lo que sale de `fin.zip`.
2. **¿Para quién es la documentación?** (a) Especificación para la reimplementación. (b) Manual funcional. (c) Las dos. **Recomiendo (a)**; los criterios están escritos para eso.

   **Decidido (2026-10-23): (a)**, especificación para la reimplementación.
3. **Si el manual y el código no coinciden, ¿cuál vale?** Ya hay cuatro casos confirmados (ver "Lo que dice el XPZ"). *(Enmienda 1: son tres; el del paso 6 se retiró.)* **Recomiendo que valga el código, con la discrepancia anotada.** La excepción: cuando toca una validación o el modelo de datos (por ejemplo, el largo máximo del usuario: 20 o 30), se le pregunta a la persona. Define CA14.

   **Decidido (2026-10-23):** vale el código y la discrepancia se anota. Si toca una validación o el modelo de datos, se le pregunta al responsable del proyecto.

   **Reemplazado por la enmienda 1 (2026-10-23):** el código dice qué **hace** el sistema, y eso es lo que se documenta como comportamiento actual. Qué **debe** hacer la reimplementación lo decide el responsable, regla por regla, en `decisiones-rediseno.md` (CA23). Cada discrepancia entre capas entra ahí como una decisión pendiente, con su recomendación. Ya no se le pregunta al responsable a medida que aparecen.
4. **(Cambió) ¿Se documenta el modo administración (`&Modulo = 'A'`)?** Ya no es "¿dónde termina el módulo?": el XPZ muestra que la administración usa los mismos paneles en modo `A`, aunque su punto de entrada (`HPrvIR21`) no está en el export y sus llamadas están comentadas. Opciones: (a) documentar lo que hacen los paneles en modo `A` y dejar el punto de entrada como hueco; (b) dejar el modo `A` fuera de alcance. **Recomiendo (a).** Es código que está en el export, y la reimplementación va a necesitar saber qué puede cambiar un administrador que el proveedor no.

   **Decidido (2026-10-23): (a).** *(Enmienda 1: el punto de entrada no es un hueco. `hprvir21_impl.java` está en `fin/`, asigna `Modulo = "A"` y lo llaman `hprvir25_impl` y `hprvir40_impl`.)* Dato de ejecución del mismo día: el portal de test tiene la opción "Administración del Registro de Proveedor" (`popro001`), que enlaza a `hprvir25`, `hprvir31`, `hprvir40` y `hprvir56`. Puede cubrir en la práctica parte del hueco del punto de entrada.
5. **¿Se puede usar el portal de test (`GENFIN_TEST_*`)?** **Recomiendo usarlo solo para mirar pantallas, sin completar un alta.** Un alta crea datos y dispara correos en un sistema ajeno; eso necesita una autorización aparte.

   **Aclarado (2026-10-22):** el acceso es al ambiente de **test**, como dice la declaración. Mirar pantallas está autorizado. Escribir (completar un alta de prueba) también: el responsable del proyecto lo confirmó para test el mismo día. Condiciones:
   - Los datos que se carguen son inventados y marcados como prueba. Nada de CUIT ni correos de personas reales.
   - Antes del primer alta se comprueba adónde van los correos de test (`ParmModPrv`) y si el usuario que se crea en ACPS Services cae en un ambiente compartido con producción. *(2026-10-23: los correos van al mail del proveedor que se carga en el alta, vía Services, así que se usa una casilla propia. Lo de Services queda pendiente: el endpoint está en el `services.config` del servidor y se le pidió a Emanuel. Respuesta del mismo día: test usa `aush5.intranet:8080/GENServicesGTF/rest/api/`, la cola de correo está desactivada y los correos de los proveedores se alteran (`@`→`#`). El responsable decidió ese mismo día tomarlo como Services propio de test por el sufijo `GTF`, sin comparar con producción. La primera alta queda destrabada.)*
   - Cada alta de prueba se registra: qué usuario se creó y cuándo.
   - *(Ampliado por el responsable el 2026-10-23.)* También está autorizado operar la administración en test (habilitar, dejar en espera, rechazar) **solo sobre los proveedores de prueba propios** (`zzprueba…`). Cada operación se anota en la bitácora.
6. **(Cambió) ¿La reimplementación es del producto o de una instalación?** El XPZ tiene texto de OSEP Mendoza fijo en el código, y varias reglas dependen de atributos de sistema por instalación (por ejemplo, si la cuenta bancaria es obligatoria). **Recomiendo tratarla como producto:** lo que hoy está fijo para OSEP se documenta como dato del cliente (CA16), y lo que depende de atributos de sistema, como configuración (CA13). Si el destino es OSEP puntualmente, decilo, porque cambia qué se considera regla.

   **Decidido (2026-10-23): se trata como producto.** Lo refuerza un dato de ese día: el portal de test muestra el logo de otra institución, no el de OSEP, así que el módulo corre en más de una instalación. El logo no se identificó con certeza.
