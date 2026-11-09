# Modos de operación — I, P y A

Ids de este archivo: reglas R-601 a R-699. No hay discrepancias entre capas en lo que cubre, así que no se usa ningún D-6nn. De los atributos de sistema y de los parámetros solo figuran los nombres. Los textos de pantalla se transcriben tal cual salen del Java.

`Modulo` es un parámetro de un carácter que reciben todos los paneles del alta. Tiene tres valores: `I` (inscripción, el asistente de 11 pasos), `P` (el proveedor ya registrado modifica sus datos) y `A` (administración). Este archivo no repite las reglas del alta: en cada tabla la columna `I` enlaza a la regla del paso por su id (sin negrita) y las columnas `P` y `A` dicen qué cambia. Las reglas con id propio (`R-6nn`) son los comportamientos que ningún paso documenta.

Fuentes. Los once paneles del alta están en el XPZ y en `fin/`. La cadena de administración (`popro001`, `hprvir25`, `hprvir40`, `hprvir21`), el menú del modo `P` (`hprvir39`, `hprvir52`, `hprvir50`) y la página maestra solo están en `fin/`, así que sus afirmaciones tienen la capa `código` y nada de diseño. Para los objetos que figuran en el chequeo de versión de `convenciones.md` con "coincide con Java", la observación en test de `pantallas.md` (S12 a S16) es compatible con lo que dice el Java.

**Cómo se lee el mapa de llamadas.** Para decir que un panel "no se alcanza" en un modo se barrió `fin/` buscando `com.fin.<objeto>` entre los llamadores y se miró en cada uno si el botón que llama está visible en ese modo. El control positivo del barrido es que `hprvir21` aparece entre los llamadores de `hprvir22`, `hprvir42`, `hprvir41`, `hprvir17m` y `hprvir06`.

## 1. Cómo se llega a cada modo

| Modo | Quién lo asigna | Desde dónde se entra | bloque |
|---|---|---|---|
| `I` | `HPrvIr07` en Start, antes de abrir el paso 3 | Paso 1 (`HPrvIR02`), paso 2 y de ahí todo el asistente | [V · capas: código, diseño · ev: hprvir07_impl.java e11A22 (Start); XPZ HPrvIr07 Events Start] |
| `P` (menú) | `HPrvIR39` en Start, sin leer ningún parámetro | `HCOF0006` en 'Inicio' cuando el estado no es `H`; y el 'Volver' de los paneles que corren en `P` | [V · capas: código · ev: hprvir39_impl.java e15552 (Start); hcof0006_impl.java e12C12 ('Inicio')] |
| `P` (retoma) | `HPrvIR02` cuando el flag de `PPrvIR02` es `E` | Salta al paso 10 (`HPrvIR10`) sin pasar por el menú (R-109, R-422) | [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'] |
| `A` (administración) | `HPrvIR21` en Start | Botón 'Modificar' de `HPrvIR25` (llamador 25) y columna de modificar datos de `HPrvIR40` (llamador 40) | [V · capas: código · ev: hprvir21_impl.java e11592 (Start); hprvir25_impl.java e20A42 ('Modificar'); hprvir40_impl.java e15AB2 (Prvmodif_Load)] |
| `A` (proveedor) | `HPrvIR21` en Start, el mismo | Enlace "Perfil" de la página maestra `GeMpPrvIR` y del menú `MainMenuWidgetProveedores`, con el usuario del contexto y llamador vacío | [V · capas: código · ev: gempprvir_impl.java e111HH2 (Start); mainmenuwidgetproveedores_impl.java e112332 (Start)] |

- **R-601** El modo `I` lo fija solo el paso 2, de forma constante, antes de abrir `TPrvInsRP`. Ningún otro camino de entrada del alta lo fija. Clase por defecto. [V · capas: código, diseño · ev: hprvir07_impl.java e11A22 (Start); XPZ HPrvIr07 Events Start; rev2 §2 · clase: esencial]
- **R-602** El modo `P` del menú lo fija `HPrvIR39` en Start, sin recibirlo por parámetro. A ese menú se llega desde `HCOF0006` ('Inicio') cuando el estado del proveedor no es `H` (si es `H` va a `HNUPRO16`) y desde el 'Volver' de los paneles que corren en `P`. Además `HPrvIR39` llama a `LoginProv001` al arrancar. Clase por defecto. [V · capas: código · ev: hprvir39_impl.java e15552 (Start); hcof0006_impl.java e12C12 ('Inicio'); hprvir41_impl.java e141G42 ('Volver') · clase: esencial]
- **R-603** El modo `A` lo fija `HPrvIR21` al final de su Start, sin condición alguna sobre quién la abre ni por dónde. Todo panel que `HPrvIR21` abre recibe `A`. [V · capas: código · ev: hprvir21_impl.java e11592 (Start) · clase: esencial]
- **R-604** El enlace "Perfil" de la página maestra del alta y del menú del portal abre `HPrvIR21` con el usuario del contexto cuando `LoginProv002` dice que hay sesión de proveedor. `HPrvIR21` no consulta ningún permiso, y `HPrvIR25` tampoco. Solo `HPrvIR40` consulta `PrvPAdminGral` (R-605). Resultado: un proveedor con sesión entra en el modo `A`, el de administración, sobre su propio perfil, sin pasar por el modo `P` y por tanto sin el cambio a `Q` ni el aviso de documentación (R-621). No se observó en test. Clase por defecto, pero es el candidato más fuerte a rediseño de este archivo. [V · capas: código · ev: gempprvir_impl.java e111HH2 (Start); mainmenuwidgetproveedores_impl.java e112332 (Start); hprvir21_impl.java e11592 (Start); busqueda de PrvPAdminGral en hprvir21, hprvir25 y hprvir40 · clase: esencial]
- **R-605** La administración ofrece el modo `A` solo para proveedores en ciertos estados: `HPrvIR25` lista los que están en `E` o `P` (los que esperan habilitación) y `HPrvIR40` los que están en `Q` o `R` (modificación o reinscripción pendiente), y su tabla solo se muestra con `PrvPAdminGral` igual a 'S'. Con el usuario de test, `HPrvIR25` se ve completa y `HPrvIR40` no muestra la tabla. [V · capas: código, ejecución · ev: hprvir25_impl.java addWhere PrvPHabCS E o P; hprvir40_impl.java e14AB2 (Start) y addWhere PrvPHabCS Q o R; S13 2026-10-23; S15 2026-10-23 · clase: esencial]
- **R-606** El 'Volver' de `HPrvIR21` elige el destino por el llamador: 40 vuelve a `HPrvIR40`, 25 a `HPrvIR25` y cualquier otro valor (el del enlace "Perfil", que es vacío) a `HNUPRO16M`. [V · capas: código · ev: hprvir21_impl.java e22592 ('Volver') · clase: esencial]
- **R-607** `HPrvIR21` abre `TPrvInsRP`, `HPrvIR41`, `HPrvIR06`, `HPrvIR22`, `HPrvIR50`, `HPrvIR17m` y `HPrvIR42` como ventanas emergentes y les pasa `A`; `TPrvInsRP` se abre con modo `UPD` y `BloqueaNombre` vacío. 'Documentos' abre `HPrvIR44` en la misma ventana, con el modo y el llamador. 'Estado' (`HPrvIR29`) y 'Categoría' (`HPrvIR30`) se abren sin modo. Como los paneles son ventanas hijas, su `Return` devuelve el control a `HPrvIR21` sin navegar: las llamadas a `HPrvIR21` comentadas en los paneles (R-210, R-231) no hacen falta. Clase por defecto. [V · capas: código · ev: hprvir21_impl.java e12592 ('Datos Empresa'), e13592 ('Domicilios'), e14592 ('Representantes'), e15592 ('Apoderados'), e16592 ('Balances'), e17592 ('Sociedad'), e18592 ('Rubros'), e19592 ('Estado'), e20592 ('Documentos'), e21592 ('categoria') · clase: esencial]
- **R-608** `HPrvIR21` muestra u oculta dos opciones según el perfil: 'Cambiar Estado de Habilitación' se oculta si el proveedor tiene número de norma de certificado, y 'Cambiar Categoría' aparece si hay una solicitud de cambio pendiente (con el texto "Cambiar Categoría (hay una solicitud de cambio)") o si el estado es `E` (con el texto "Cambiar Categoría"). Las otras ocho opciones están siempre. Clase por defecto. [V · capas: código · ev: hprvir21_impl.java e11592 (Start) · clase: esencial]
- **R-609** `POPRO001` oculta en Start el enlace "Proveedores esperando Habilitación", que apunta a `HPrvIR40`, y deja visibles los otros cuatro. `HPrvIR40` sigue vivo: lo referencian `HPrvIR03`, `HPrvIR21` y `HPrvIR23`. Clase por defecto: no hay evidencia de por qué se ocultó. [V · capas: código, ejecución · ev: popro001_impl.java e1122O2 (Start); S12 2026-10-23 · clase: esencial]

Sobre S15. `pantallas.md` dice que `hprvir40` se llega por URL directa y que está "enlazada desde S13". En `hprvir25_impl.java` no hay ninguna referencia a `hprvir40`. No se marca como discrepancia porque la observación no dice cuál era el enlace; queda para confirmar al operar `HPrvIR40` en E5.

## 2. Qué paneles existen en cada modo

| Paso | Panel | `I` | `P` | `A` | bloque |
|---|---|---|---|---|---|
| 1 | `HPrvIR02` | Sí (no recibe modo) | Solo asigna `P` y salta al paso 10 (R-109) | No | [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIR02 Events 'Siguiente'] |
| 2 | `HPrvIr07` | Sí, fija `I` | No | No | [V · capas: código, diseño · ev: hprvir07_impl.java e11A22 (Start); llamadores de hprvir07 en fin/: solo hprvir02; XPZ HPrvIr07 Events Start] |
| 3 | `TPrvInsRP` | Desde el paso 2 (modo `INS` o `UPD`) | Desde `HPrvIR39`, en `UPD` | Desde `HPrvIR21`, en `UPD` | [V · capas: código, diseño · ev: hprvir07_impl.java S122 ('INSREG'); hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e12592 ('Datos Empresa'); XPZ HPrvIr07 Sub 'insReg'] |
| 4 | `HPrvIR17m` | Sí, si es persona jurídica | No: el menú `P` ofrece `HPrvIR35` y `HPrvIR36` (R-612) | Sí, 'Sociedad' | [V · capas: código · ev: hprvir21_impl.java e17592 ('Sociedad'); hprvir39_impl.java e16552 (Grid1_Load); llamadores de hprvir17m en fin/: hprvir21, hprvir41 y tprvinsrp] |
| 5 | `HPrvIR41` | Sí | Sí, 'Modificar Datos de Domicilios' | Sí, 'Domicilios' | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e13592 ('Domicilios'); hprvir41_impl.java e151G42 (Start)] |
| 6 | `HPrvIR18` | Sí, si es persona jurídica | No: usa `HPrvIR50` (R-610, R-614) | No: usa `HPrvIR50` (R-610, R-614) | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e16592 ('Balances'); llamadores de hprvir18 en fin/: hprvir41 y hprvir42 desde botones del asistente] |
| 7 | `HPrvIR42` | Sí | Sí, 'Modificar Rubros' | Sí, 'Rubros' | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e18592 ('Rubros'); hprvir42_impl.java e151G52 (Start)] |
| 8 | `HPrvIR06` | Sí | Sí, 'Modificar Datos de Representantes' | Sí, 'Representantes' | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e14592 ('Representantes'); hprvir06_impl.java e15AD2 (Start)] |
| 9 | `HPrvIR22` | Sí | No: el menú `P` no ofrece cuentas bancarias (R-611, R-613) | Sí, 'Cambiar datos de Cuenta Bancaria' | [V · capas: código · ev: hprvir21_impl.java e15592 ('Apoderados'); hprvir39_impl.java e16552 (Grid1_Load); llamadores de hprvir22 en fin/: hprvir10, hprvir21 y hprvir06] |
| 10 | `HPrvIR10` | Sí | Solo por la retoma del flag `E` | No | [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente'); hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start] |
| 11 | `HPrvIR09` | Sí | No | No | [V · capas: código, diseño · ev: hprvir09_impl.java e11AI2 (Start); llamadores de hprvir09 en fin/: solo hprvir10, desde el bloque del asistente; XPZ HPrvIR09 Events Start] |
| — | `HPrvIR50` (Trabajar con Balances) | No | Sí, 'Ver Balances' | Sí, 'Balances' | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e16592 ('Balances'); hprvir50_impl.java e121ER2 ('volver')] |

- **R-610** La rama de `HPrvIR18` para los modos distintos de `I` (título, botón de actualización, 'Volver') no la alcanza ningún camino: el menú `P` y `HPrvIR21` mandan los balances a `HPrvIR50`, y las llamadas que quedan a `HPrvIR18` salen de botones del asistente que `P` y `A` ocultan. Es código muerto. [V · capas: código · ev: hprvir18_impl.java e11AC2 (Start) y e17AC2 ('Volver'); hprvir41_impl.java e151G42 (Start) y bloque tblWizbtn; hprvir42_impl.java e151G52 (Start) y bloque tblWizbtn · clase: accidente]
- **R-611** La rama `P` del 'Volver' de `HPrvIR22` (a `HPrvIR39`) no la alcanza ningún camino: el menú `P` no tiene cuentas bancarias, y las llamadas a `HPrvIR22` que quedan salen de `HPrvIR10` y `HPrvIR06`, de botones del asistente. El comentario del XPZ "P=llamado dde hprvir39(no se usa)" es correcto para este panel. [V · capas: código, diseño · ev: hprvir22_impl.java e1425M2 ('Volver'); hprvir39_impl.java e16552 (Grid1_Load); XPZ HPrvIR22 Events Start (comentario del modo) · clase: accidente]
- **R-612** El modo `P` no edita la sociedad en `HPrvIR17m` sino en dos paneles propios, `HPrvIR35` ("Modificación Datos Sociedad") y `HPrvIR36` ("Modificación Datos Integrantes de la Sociedad"), que piden otros datos (aprobación del balance, actas, cierre de balance, fin de representación). El modo `A` sí usa `HPrvIR17m` (fechas de constitución e inscripción, país, provincia, localidad e integrantes). El mismo concepto, "datos de la sociedad", tiene dos pantallas con campos distintos según quién edita. Clase por defecto: `HPrvIR35` y `HPrvIR36` no están en el XPZ y no se leyeron por dentro. [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir35_impl.java e12BA2 ('guardar'); hprvir17m_impl.java e1225K2 ('Siguiente') · clase: esencial]
- **R-613** Los dos modos ofrecen conjuntos distintos de datos del proveedor: el menú `P` ofrece Apoderados (`HPrvIR20`) y no ofrece cuentas bancarias ni documentos; `HPrvIR21` ofrece cuentas bancarias (el evento se llama 'Apoderados' pero abre `HPrvIR22`) y documentos, y no ofrece apoderados. El comentario del XPZ en `HPrvIR06` dice que el paso 9 del asistente fue antes el de apoderados (`HPrvIR20`). Clase por defecto. [V · capas: código, diseño · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e15592 ('Apoderados') y e20592 ('Documentos'); XPZ HPrvIR06 Events (comentario Paso 9 Antes Apoderados) · clase: esencial]
- **R-614** `HPrvIR50` ("Trabajar con Balances") es el panel de balances de los modos `P` y `A`, con alta, modificación y baja por la ventana `TPrvESP`. Su 'volver' solo tiene ramas para `P` (a `HPrvIR39`) y para `A` (devuelve el control): con cualquier otro modo no hace nada. Clase por defecto. [V · capas: código · ev: hprvir50_impl.java e121ER2 ('volver') · clase: esencial]

## 3. Qué cambia en cada panel del alta

Las tablas tienen una fila por aspecto. Una celda con `R-nnn` sin negrita enlaza a la regla que ya lo documenta.

### 3.1 Pasos 1 y 2 — `HPrvIR02` y `HPrvIr07`

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| Parámetro `Modulo` | `HPrvIr07` lo asigna `I` (R-601); `HPrvIR02` no lo recibe | `HPrvIR02` lo asigna `P` en la rama del flag `E` (R-109) | No llega | [V · capas: código, diseño · ev: hprvir07_impl.java e11A22 (Start); hprvir02_impl.java e125A2 ('Siguiente'); XPZ HPrvIr07 Events Start; XPZ HPrvIR02 Events 'Siguiente'] |
| Qué hace el paso | Puerta por CUIT (R-101 a R-119) y elección de usuario (paso 2) | Salta al paso 10 con el usuario rescatado (R-109) | No existe | [V · capas: código, diseño · ev: hprvir02_impl.java e125A2 ('Siguiente') y S122 ('PASO10'); XPZ HPrvIR02 Events 'Siguiente'] |

### 3.2 Paso 3 — `TPrvInsRP`

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| Título y botones | "PASO 3 de 11" y botones del asistente | "Trabajar datos de la empresa" y botón Aceptar | Igual que `P` | [V · capas: código, diseño · ev: tprvinsrp_impl.java e11IZ2 (Start); XPZ TPrvInsRP Events Start] |
| Nombre y número de proveedor | El paso 2 pasa `BloqueaNombre` igual a `Prove` (R-158) | `BloqueaNombre` es '1': el nombre queda fijo y toma el del padrón; el número se muestra | `BloqueaNombre` llega vacío: el nombre se puede editar; el número se muestra | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e12592 ('Datos Empresa'); tprvinsrp_impl.java e11IZ2 (Start)] |
| Campos editables en modo `UPD` | tipo de persona, sexo, clase y certificado (R-161) | todo bloqueado: tipo, sexo, clase, IVA, Ingresos Brutos, certificado y CUIT (R-161) | todo habilitado, CUIT incluido; qué prevalece contra `NOACCEPT` queda pendiente de E5 (R-161) | [V · capas: código, diseño · ev: tprvinsrp_impl.java e11IZ2 (Start); XPZ TPrvInsRP Events Start] |
| Descripción del asistente y aviso de denominación | Ambos visibles en `UPD` | Ambos ocultos | La descripción del asistente oculta; el aviso queda en su valor por defecto, visible | [V · capas: código, diseño · ev: tprvinsrp_impl.java e11IZ2 (Start) y valor inicial de tblAviso_Visible; XPZ TPrvInsRP Events Start] |
| Estado que deja al grabar | `N` por defecto en el alta (R-441) | `Q` siempre (R-449); la segunda regla es redundante (R-464) | No lo cambia (R-621) | [V · capas: código, diseño · ev: tprvinsrp_impl.java onLoadActionsIZ382 y checkExtendedTableIZ382; XPZ TPrvInsRP Rules] |
| Aviso de documentación | No | Sale (R-163) | No sale (R-621) | [V · capas: código, diseño · ev: tprvinsrp_impl.java e12IZ2 (After Trn); XPZ TPrvInsRP Events After Trn] |
| A dónde va después de grabar | Paso 4 o 5 (R-164) | `HPrvIR39` (R-163) | `Return` a `HPrvIR21` (R-165) | [V · capas: código, diseño · ev: tprvinsrp_impl.java e12IZ2 (After Trn); XPZ TPrvInsRP Events After Trn] |

- **R-620** La edición del nombre depende de quién abre el panel: el menú `P` pasa `BloqueaNombre` igual a '1' (el nombre queda fijo con el del padrón) y `HPrvIR21` lo pasa vacío (el nombre se puede cambiar). El aviso del panel dice que "los cambios de denominación sólo pueden ser efectuados por la Dirección de Compras y Suministros", y ese aviso queda oculto en `P`, donde el nombre sí está bloqueado, y visible en `A`, donde el nombre se puede editar. Clase por defecto. [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e12592 ('Datos Empresa'); tprvinsrp_impl.java e11IZ2 (Start) · clase: esencial]
- **R-621** En el modo `A` la variable `flagUpdatePrv` queda en 'N': `TPrvInsRP` no fuerza `Q` y no manda el aviso `PROVEEDOR_PRESENTARDOCUMENTACION`. Ninguna transacción hija (`TPrvPJ`, `TPrvDom`, `TPrvRpr`, `TPrvRub`, `TPrvESP`, `TPrvPod`) cambia el estado en `A`, porque todas comparan solo contra `P`; `TPrvBco` ni siquiera compara el modo. Editar un perfil como `A` deja el estado como estaba y no deja constancia de que hay datos por aprobar. Clase por defecto. [V · capas: código, diseño · ev: tprvinsrp_impl.java e11IZ2 (Start) y e12IZ2 (After Trn); tprvpj_impl.java e12CA2 (After Trn); tprvdom_impl.java e12C82 (After Trn); tprvrpr_impl.java e12C62 (After Trn); tprvrub_impl.java e12C72 (After Trn); tprvesp_impl.java e12C92 (After Trn); tprvpod_impl.java e12CB2 (After Trn); tprvbco_impl.java e12O22 (After Trn); XPZ TPrvInsRP Events Start · clase: esencial]

> **Corrección a la rev2** (rev2 §2): la rev2 dice que el modo `A` habilita "lo de `I` más situación ante IVA e Ingresos Brutos". El XPZ y el Java habilitan además los tres componentes del CUIT. Es un error de lectura de la rev2, no una discrepancia: ya está tratado en la nota del paso 3 (R-161).

### 3.3 Paso 4 — `HPrvIR17m`

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| Alcanzable | Sí, si el tipo de persona es jurídica | No (R-612) | Sí | [V · capas: código · ev: hprvir21_impl.java e17592 ('Sociedad'); llamadores de hprvir17m en fin/: hprvir21, hprvir41 y tprvinsrp] |
| Título y botones | "Ingrese los Datos de la Sociedad" y botones del asistente | — | "Trabajar Datos de la Sociedad", con Aceptar y Volver; oculta el rótulo del paso | [V · capas: código, diseño · ev: hprvir17m_impl.java e1925K2 (Start); XPZ HPrvIR17m Events Start] |
| Validación y grabación | 'Siguiente' (R-180 a R-187) | — | 'Aceptar', con las mismas comprobaciones (R-191) | [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente') y e1525K2 ('Aceptar'); XPZ HPrvIR17m Events 'Siguiente' y 'Aceptar'] |
| Salida | Abre el paso 5 | — | 'Aceptar' y 'Volver' ejecutan 'perfilMenu' y devuelven el control (R-194) | [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'), e1425K2 ('Volver') y S112 ('PERFILMENU'); XPZ HPrvIR17m Events Sub 'perfilMenu'] |
| Estado que deja | — | — | No lo cambia: `TPrvPJ` compara solo contra `P` (R-621) | [V · capas: código · ev: tprvpj_impl.java e12CA2 (After Trn)] |

### 3.4 Paso 5 — `HPrvIR41`

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| Título, botones y descripción | Botones y textos del asistente, sin Volver (R-207) | Título "Trabajar con Domicilios", Volver, y el texto "Aquí Ud. puede ingresar los datos correspondientes a sus domicilios." (R-207) | Igual que `P` pero sin ese texto: queda sin ninguna descripción (R-207) | [V · capas: código, diseño · ev: hprvir41_impl.java e151G42 (Start); XPZ HPrvIR41 Events Start] |
| Volver | No existe | Va a `HPrvIR39` (R-209) | Devuelve el control a `HPrvIR21` (R-209) | [V · capas: código, diseño · ev: hprvir41_impl.java e141G42 ('Volver'); XPZ HPrvIR41 Events 'Volver'] |
| Alta, cambio y baja de domicilios | `TPrvDom` en ventana emergente (R-212) | `TPrvDom` con `P`: al grabar deja `Q` (R-450) | `TPrvDom` con `A`: no cambia el estado (R-621) | [V · capas: código · ev: hprvir41_impl.java e111G42 ('Agregar'); tprvdom_impl.java e12C82 (After Trn)] |

### 3.5 Paso 6 — `HPrvIR18`

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| Alcanzable | Sí, solo para persona jurídica | No: usa `HPrvIR50` (R-610) | No: usa `HPrvIR50` (R-610) | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); hprvir21_impl.java e16592 ('Balances')] |
| Rama del modo | Botones y descripción del asistente (R-220) | Rama muerta | Rama muerta | [V · capas: código, diseño · ev: hprvir18_impl.java e11AC2 (Start); XPZ HPrvIR18 Events Start] |
| Volver | Devuelve el control sin mirar el modo (R-222) | No se usa | No se usa | [V · capas: código, diseño · ev: hprvir18_impl.java e17AC2 ('Volver'); XPZ HPrvIR18 Events 'Volver'] |
| Balances en el modo | — | `HPrvIR50` con `P`; el 'Modificar Balance' abre `TPrvESP`, que al grabar deja `Q` (R-450) | `HPrvIR50` con `A`; `TPrvESP` no cambia el estado (R-621) | [V · capas: código · ev: hprvir50_impl.java e121ER2 ('volver'); tprvesp_impl.java e12C92 (After Trn)] |

### 3.6 Paso 7 — `HPrvIR42`

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| Título, botones y rótulo | Asistente, título "Rubros en los que desea inscribirse", sin Volver (R-232) | "Trabajar con Rubros", con Volver (R-232) | Igual que `P` (R-232) | [V · capas: código, diseño · ev: hprvir42_impl.java e151G52 (Start); XPZ HPrvIR42 Events Start] |
| Volver | No existe | Exige al menos un rubro (R-226) y va a `HPrvIR39` (R-230) | Exige al menos un rubro (R-226) y devuelve el control (R-230) | [V · capas: código, diseño · ev: hprvir42_impl.java e141G52 ('Volver'); XPZ HPrvIR42 Events 'Volver'] |
| Alta y baja de rubros | `TPrvRub` en ventana emergente (R-235) | `TPrvRub` con `P`: al grabar deja `Q` salvo que ya esté en `Q`, `I` o `R` (R-451) | `TPrvRub` con `A`: no cambia el estado (R-621) | [V · capas: código · ev: hprvir42_impl.java e111G52 ('Agregar'); tprvrub_impl.java e12C72 (After Trn)] |

### 3.7 Paso 8 — `HPrvIR06`

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| Título, botones y rótulo | Asistente y título "Datos de los Representantes de la Empresa" (R-243) | Bloque de actualización y título "Trabajar con Representantes" (R-243) | Igual que `P` (R-243) | [V · capas: código, diseño · ev: hprvir06_impl.java e15AD2 (Start); XPZ HPrvIR06 Events Start] |
| Volver | No existe | Va a `HPrvIR39` (R-241) | Devuelve el control (R-241) | [V · capas: código, diseño · ev: hprvir06_impl.java e14AD2 ('Volver'); XPZ HPrvIR06 Events 'Volver'] |
| Alta, cambio y baja de representantes | `TPrvRpr` en ventana emergente | `TPrvRpr` con `P`: al grabar deja `Q` (R-450) | `TPrvRpr` con `A`: no cambia el estado (R-621) | [V · capas: código · ev: hprvir06_impl.java e11AD2 ('Agregar'); tprvrpr_impl.java e12C62 (After Trn)] |

### 3.8 Paso 9 — `HPrvIR22`

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| Alcanzable | Sí | No (R-611) | Sí | [V · capas: código · ev: hprvir21_impl.java e15592 ('Apoderados'); hprvir39_impl.java e16552 (Grid1_Load)] |
| Título, botones y rótulo | Asistente, título "Datos de Cuentas Bancarias" (R-305) | Rama no alcanzable | "Trabajar con Cuentas Bancarias", con el bloque de actualización (R-305) | [V · capas: código, diseño · ev: hprvir22_impl.java e1525M2 (Start); XPZ HPrvIR22 Events Start] |
| Texto de ayuda de la obligatoriedad | Un juego de textos dentro del bloque del asistente (R-304) | Rama no alcanzable | Otro juego dentro del bloque de actualización (R-304) | [V · capas: código, diseño · ev: hprvir22_impl.java e1525M2 (Start); XPZ HPrvIR22 Events Start] |
| Volver | No existe | Iría a `HPrvIR39` (R-308); no se alcanza | Devuelve el control (R-308) | [V · capas: código, diseño · ev: hprvir22_impl.java e1425M2 ('Volver'); XPZ HPrvIR22 Events 'Volver'] |
| Alta, cambio y baja de cuentas | `TPrvBco` en ventana emergente | — | `TPrvBco` con `A`: no mira el modo ni cambia el estado (R-621) | [V · capas: código · ev: tprvbco_impl.java e12O22 (After Trn)] |

### 3.9 Pasos 10 y 11 — `HPrvIR10` y `HPrvIR09`

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| `HPrvIR10`: bloque que se muestra | Bloque de inscripción con Anterior y Siguiente (R-320) | Bloque de reimpresión con el aviso "La habilitación está en proceso. Espere la culminación del trámite." (R-321) | No se alcanza | [V · capas: código, diseño · ev: hprvir10_impl.java e11F02 (Start); XPZ HPrvIR10 Events Start] |
| `HPrvIR10`: cómo se sale | Anterior y Siguiente (R-329, R-330) | No hay botón: los botones del asistente están ocultos y el panel no tiene Volver propio | No se alcanza | [V · capas: código · ev: hprvir10_impl.java e11F02 (Start), e12F02 ('Confirmar') y e13F02 ('Anterior')] |
| `HPrvIR09` | Sí; fija `I` en Start (R-353) | No se alcanza | No se alcanza | [V · capas: código, diseño · ev: hprvir09_impl.java e11AI2 (Start); XPZ HPrvIR09 Events Start] |

> **Corrección a la rev2** (rev2 §18.1, consecuencia 2): la rev2 dice que quien entró en `A` o `P` y llegó al paso 11 reaparece en el paso 10 en modo `I`. No puede pasar, porque el paso 10 solo ofrece avanzar a `HPrvIR09` en modo `I` (R-320), y `A` no llega al paso 10. Es un error de lectura de la rev2: el XPZ y el Java coinciden.

## 4. El menú del modo P: `HPrvIR39`

`HPrvIR39` ("Menú Modificación de Datos") es la pantalla de inicio de un proveedor que no está habilitado. Lista opciones según el estado y abre los paneles con `P`. No está en el XPZ.

| Opción | Aparece cuando | Destino | bloque |
|---|---|---|---|
| Imprimir datos de la empresa | Estado `H`, `R` o `Q` | Sin enlace asignado (R-631) | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Modificar Datos de la Empresa | Estado distinto de `R` | `TPrvInsRP` en `UPD` con `P` y nombre bloqueado | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Modificar Datos de la Sociedad | Estado distinto de `R` | `HPrvIR35` | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Modificar Integrantes de Sociedad | Estado distinto de `R` | `HPrvIR36` con `P` | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Modificar Datos de Domicilios | Estado distinto de `R` | `HPrvIR41` con `P` | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Modificar Rubros | Estado distinto de `R` | `HPrvIR42` con `P` | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Ver Balances | Estado distinto de `R` | `HPrvIR50` con `P` | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Modificar Datos de Representantes | Estado distinto de `R` | `HPrvIR06` con `P` | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Modificar Datos de Apoderados | Estado distinto de `R` | `HPrvIR20` con `P` | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Imprimir Solicitud de Modificación | Estado `Q` o `R` | No se emite (R-632) | [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load)] |
| Solicitud de cambio de categoría | Si la categoría no es `1` | `HPrvIR75`, `HPrvIR51b` o `HPrvIR52` según el caso (R-633) | [V · capas: código · ev: hprvir39_impl.java e15552 (Start) y e12552 ('SolCambioCat')] |
| Solicitud de reinscripción | Estado `R` o `I` | `HPrvIR76` (R-634) | [V · capas: código · ev: hprvir39_impl.java e15552 (Start) y e13552 ('SolReinscripcion')] |
| Notificaciones | Si el proveedor tiene alguna | `HPrvIR53` | [V · capas: código · ev: hprvir39_impl.java e15552 (Start) y e14552 ('Notificaciones')] |

- **R-630** Las ocho opciones de edición (empresa, sociedad, integrantes, domicilios, rubros, balances, representantes y apoderados) aparecen para todo estado distinto de `R`, sin mirar nada más: también para `N`, `E`, `Q`, `P`, `I`, `V` y `X`, y para sociedad e integrantes sin mirar el tipo de persona. Como `TPrvInsRP` en `P` fuerza `Q` sin mirar el estado (R-449), un proveedor en `N` o `E` que edita sus datos pasa a `Q`. Clase por defecto. [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load); tprvinsrp_impl.java checkExtendedTableIZ382 · clase: esencial]
- **R-631** La opción "Imprimir datos de la empresa" se arma con el texto y el destino de ventana nueva, pero el código no le asigna ningún enlace: queda con el valor inicial, vacío. No se observó en test. [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load) y valor inicial de lblUnlink_Link · clase: accidente]
- **R-632** La opción "Imprimir Solicitud de Modificación" para `Q` y `R` solo cambia el texto de la variable del enlace después de la última fila emitida, y el ciclo termina enseguida: nunca llega a una fila. Es código muerto. [V · capas: código · ev: hprvir39_impl.java e16552 (Grid1_Load) · clase: accidente]
- **R-633** El cambio de categoría tiene cuatro salidas desde `HPrvIR39`. Con una solicitud pendiente y categoría `2`, `HPrvIR75` en modo 'E' (eliminarla). Si no hay esa solicitud pendiente, y `PPrvIR71` devuelve 0, `HPrvIR51b` (domicilios para el cambio). Si no, y `RPrvIR63` devuelve un `FlagBalance` en 0, `HPrvIR52` (balance). En el resto, `HPrvIR75` en modo 'C' (crear). Con categoría `1` la opción no existe. Clase por defecto: la norma que justifica la categoría `1` sin cambio no está en las fuentes. [V · capas: código · ev: hprvir39_impl.java e15552 (Start) y e12552 ('SolCambioCat') · clase: esencial]
- **R-634** La reinscripción depende del estado: en `I` el texto es "Emitir Solicitud de Reinscripción" y se oculta el mensaje; en `R`, si hay una solicitud sin confirmar, el texto pasa a "Eliminar Solicitud de Reinscripción"; en cualquier otro estado se ocultan el bloque y el mensaje. Ambos casos abren `HPrvIR76` con el operador 'C' o 'E'. Clase por defecto. [V · capas: código · ev: hprvir39_impl.java e15552 (Start) y e13552 ('SolReinscripcion') · clase: esencial]

### 4.1 `HPrvIR52` — estado de situación patrimonial para el cambio de categoría

`HPrvIR52` recibe el modo pero no decide nada con él.

- **R-635** `HPrvIR52` ("Estado Situación Patrimonial para cambio de Categoría") recibe `Modulo` y no lo compara: solo lo reenvía a `HPrvIR51` en 'Anterior'. 'Volver' va siempre a `HPrvIR39`. Clase por defecto. [V · capas: código · ev: hprvir52_impl.java e161EP2 ('Anterior') y e171EP2 ('Volver') · clase: esencial]
- **R-636** 'Siguiente' en `HPrvIR52` exige la fecha del último ejercicio ("Debe ingresar al menos los datos del último ejercicio para poder continuar."). Si el tipo de persona es 0, exige además un balance cerrado según `RPrvIR63` ("Debe ingresar el último Balance Cerrado, con fecha ... para poder continuar."). Cumplido eso llama a `PPrvIR72` con el destino '1', que deja el estado en `Q` (R-453), y muestra "Su solitud de cambio de categoría fue creada satisfactoriamente" (con "solitud" mal escrito) y oculta el botón. La llamada a `PPrvIR72` está escrita dos veces, una por cada rama del tipo de persona. Clase por defecto. [V · capas: código · ev: hprvir52_impl.java e151EP2 ('Siguiente') · clase: esencial]

## 5. La cadena de administración y su efecto en el estado

| Aspecto | `I` | `P` | `A` | bloque |
|---|---|---|---|---|
| Quién edita | El proveedor que se inscribe | El proveedor con sesión, por el menú `HPrvIR39` | La administración por `HPrvIR25` y `HPrvIR40`, y el proveedor con sesión por "Perfil" (R-604) | [V · capas: código · ev: hprvir39_impl.java e15552 (Start); hprvir21_impl.java e11592 (Start); gempprvir_impl.java e111HH2 (Start)] |
| Estado de partida del proveedor | Sin perfil o `N` (R-424, R-425) | Cualquiera menos `R` (R-630) | `E` o `P` por `HPrvIR25`; `Q` o `R` por `HPrvIR40`; cualquiera por "Perfil" (R-605, R-604) | [V · capas: código · ev: hprvir25_impl.java addWhere PrvPHabCS E o P; hprvir40_impl.java addWhere PrvPHabCS Q o R; hprvir39_impl.java e16552 (Grid1_Load)] |
| Estado que deja | `N`, y `E` en el paso 11 (R-441, R-443) | `Q` (R-449 a R-453) | Ninguno (R-621) | [V · capas: código · ev: tprvinsrp_impl.java checkExtendedTableIZ382; tprvdom_impl.java e12C82 (After Trn); tprvpj_impl.java e12CA2 (After Trn)] |
| Cómo vuelve a `H` | No aplica | La administración lo aprueba en `HPrvIR40` con `PPrvIR50` (R-447) | No hace falta: no sale de su estado | [V · capas: código · ev: hprvir40_impl.java e13AB2 ('Habilitar'); pprvir50.java privateExecute] |

## Capas

Capas: código (Java generado) para todo lo de `HPrvIR21`, `HPrvIR39`, `HPrvIR50`, `HPrvIR52`, `HPrvIR25`, `HPrvIR40`, `POPRO001` y las páginas maestras; código y diseño para los once paneles del alta; ejecución solo en R-605 y R-609 (S12, S13 y S15).

Clases. Todo lo que no tiene evidencia de que sea una norma queda como `esencial` por defecto y llega al responsable como confirmación rápida. Los accidentes de este archivo son tres ramas muertas (R-610, R-611, R-632) y una opción sin enlace (R-631).

Lo que el archivo no resolvió: el interior de `HPrvIR35`, `HPrvIR36`, `HPrvIR20`, `HPrvIR51b`, `HPrvIR75` y `HPrvIR76`, que solo se leyeron lo necesario para saber a dónde llevan y con qué modo; y si "Perfil" (R-604) deja de verdad entrar a un proveedor en `A`, que no se observó en test.
