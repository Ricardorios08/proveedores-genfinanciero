# registro-proveedores-docs — Diseño

**Estado:** aprobado por responsable del proyecto el 2026-10-23 (versión 2, con la enmienda 1 y la revisión independiente del 2026-10-23)
**Fuente:** `propuesta.md` (aprobada el 2026-10-23, enmienda 1 aprobada el mismo día)

## Para qué es esto

El responsable no conoce el flujo completo y no lo va a estudiar. Va a decidir **solo** qué se mantiene, qué se rediseña y qué se elimina, leyendo tres cosas en este orden:

1. `docs/mapa-flujos.md`
2. `docs/decisiones-rediseno.md`
3. el respaldo, solo cuando quiera verificar una decisión.

Todo el diseño apunta a que esas dos primeras piezas sean confiables. Por eso cada decisión enlaza a afirmaciones con evidencia, y el estado de cada afirmación se calcula, no se declara.

## Cómo se cumple cada criterio

Todos los archivos nuevos van en `docs/`, que todavía no existe. Las rutas de insumos son relativas a la raíz del repo; `../genfin-gx-extraido/` queda fuera de él.

| Criterio | Cómo se cumple | Piezas que cambian | Piezas nuevas |
|---|---|---|---|
| CA1 | Índice escrito a mano, con una línea por archivo, en orden de lectura (mapa y decisiones primero). `verificar.py` lo compara con los archivos en las dos direcciones | — | `docs/README.md` |
| CA2 | `contar-xpz.py` cuenta los hijos directos de `<Objects>` y de `<Attributes>`, por tipo GeneXus. El documento copia la salida y el comando | — | `docs/herramientas/contar-xpz.py`, `docs/inventario-objetos.md` |
| CA3 | Columna `cobertura` en el inventario, que se completa al final | `docs/inventario-objetos.md` | — |
| CA4 | `dependencias-xpz.py` extrae las llamadas del código de cada objeto, separa las activas de las que están dentro de `/* */` o de `//`, y les resta los objetos presentes y las funciones nativas. Trae los cuatro controles de la propuesta | — | `docs/herramientas/dependencias-xpz.py`, `docs/dependencias-faltantes.md` |
| CA5 | Columna `fuente` por faltante: `fin/<archivo>`, `otro export` o `ninguna → hueco` | `docs/dependencias-faltantes.md` | — |
| CA6 | Un archivo por paso con las mismas secciones. Cada validación es una **regla** con id (`R-nn`). Se parte de la rev2 y se cruza con el `_impl.java` del panel; los 11 paneles tienen Java | — | `docs/pasos/paso-01.md` … `paso-11.md` |
| CA7 | Tabla por panel con lo que cambia en `P` y en `A` respecto de `I`. El modo `A` se documenta por la cadena `popro001 → hprvir25/40 → hprvir21 → paneles`, y el `P` desde `hprvir39` | — | `docs/modos.md` |
| CA8, CA9 | Una tabla por entidad con atributo, tipo y dominio, y encima tabla y clave con evidencia. Las claves de las 6 hijas salen del `DELETE ... WHERE` de su Java | — | `docs/modelo-datos.md` |
| CA10 | Estados escritos como transiciones: origen → destino, con el objeto que asigna y la condición en quien lo llama | — | `docs/estados.md` |
| CA11 | Tabla de puntos de contacto: sistema, dirección, objeto, recurso `ACPS*RESOURCE` | — | `docs/integraciones.md` |
| CA12 | Tabla de envíos con el universo acotado a los objetos del módulo (B1 + B2), más una fila por cada envío que Services hace a pedido del módulo, como la bienvenida | — | `docs/mensajes.md` |
| CA13 | Tabla con nombre, quién lo lee y su efecto. Nunca el valor | — | `docs/configuracion.md` |
| CA14 | Una entrada `D-nn` por discrepancia, con fuente y capa de cada lado. Las tres conocidas se **revalidan** antes de cargarse | — | `docs/discrepancias.md` |
| CA15 | Formato fijo de afirmación y de regla, con el estado calculado por `verificar.py` (ver "Estado de una afirmación") | — | `docs/convenciones.md`, `docs/herramientas/verificar.py` |
| CA16 | Tabla de reglas con la columna "de quién es": cliente, producto o sospechado | — | `docs/cliente-vs-producto.md` |
| CA17 | Una fila por par objeto + modo, con id `Snn`. Las capturas van a `../genfin-gx-extraido/screens/` | — | `docs/pantallas.md` |
| CA18 | Una fila por flujo con id `Fnn`. Hay una retoma por cada uno de los 10 estados de `PPrvIR02`, cada una "recorrida" o "solo desde el código" | — | `docs/flujos.md` |
| CA19, CA24 | CSV con las columnas `feature,area,priority,original,clone,notes,capas,evidencia,decision`. `decision` arranca en `pendiente` | — | `docs/features.csv` |
| CA20 | Línea `Capas:` en cada paso y en cada flujo. La recalcula la tarea C12, después de las altas | `docs/pasos/*`, `docs/flujos.md` | — |
| CA21 | Diagrama Mermaid del flujo, con cada punto de dolor marcado y enlazado a su `DR-nn` | — | `docs/mapa-flujos.md` |
| CA22 | Campo `clase:` obligatorio en el bloque de cada regla `R-nn` | `docs/pasos/*` y transversales | — |
| CA23 | Una entrada `DR-nn` por regla parche o accidente y por discrepancia `D-nn`, con recomendación. `verificar.py` controla que existan | — | `docs/decisiones-rediseno.md` |

### Frontera del módulo *(decisión del coordinador, 2026-10-23, a partir del builder check)*

"El módulo" no son solo los objetos del XPZ (B1) más los que el XPZ llama (B2). La administración (`popro001`, `hprvir25`, `hprvir31`, `hprvir40`, `hprvir56`), el modo `P` (`hprvir52`) y quienes asignan `H` (`pprvir04`, `pprvir34`, `pprvir50`) están solo en `fin/`, y en el XML aparecen 0 veces. Regla:

- **Dentro del módulo:** la clausura de llamadas en `fin/` a partir de los puntos de entrada (los 11 paneles del alta, `hprvir39` y `popro001`), siguiendo solo objetos de la familia del módulo (nombre `hprv*`, `pprv*`, `tprv*`, `rprv*` o `popro*`). Se documentan por dentro.
- **Punto de contacto:** cualquier otro objeto que el módulo llame (por ejemplo `acpsrestadp`, `pcmsg001`). Se lista en `integraciones.md` con su dirección, sin documentar su interior.
- **Entrada externa:** objetos de fuera de la familia que llaman al módulo (por ejemplo `loginrecuperarpwd`, `cm0145`, `hli00014`). Se listan en `integraciones.md`, y si disparan un correo del módulo, también en `mensajes.md`.

La clausura la calcula `universo-fin.py`. Controles: `hprvir21` y `pprvir50` tienen que quedar dentro, y `loginprov` en entradas externas. *(Ajuste del 2026-10-23, durante B4: el control decía `loginrecuperarpwd`, pero ese objeto solo llama a objetos de la familia que la clausura no alcanza (`pprvsendmail`, `tprvinsrp0002`). Se agregó la lista **borde**, con los objetos de la familia fuera de la clausura y quién los llama, para revisar a mano; `pprvsendmail` tiene que quedar ahí. Además, la familia admite una `a` adelante: GeneXus genera los reportes `RPrvIR*` como `arprvir*` y algunos procedimientos como `apprvir*`, detrás de un envoltorio `pprvir*.java` (corregido el 2026-10-23, durante E4, al leer `apprvir03`).)* El universo resultante (`docs/universo-modulo.md`) reemplaza a "B1 + B2" en CA3, CA12, CA17 y F1.

Además, sin CA propio: `docs/seguridad.md`, con el hallazgo de la contraseña inicial. Lo exige "Restricciones duras" de la propuesta, y genera su propia entrada `DR-nn`.

## Detalle

### Estado de una afirmación (calculado, no declarado)

Cada afirmación lleva un bloque con sus **capas** y su **evidencia**. El estado se escribe, para que lo vea el lector (CA15), pero `verificar.py` lo **recalcula** con esta tabla y rechaza el archivo si no coincide:

| Capas presentes (deduplicadas) | Estado |
|---|---|
| Incluye `código` | **V** |
| Incluye `ejecución`, y el objeto pasó el chequeo de versión (E1) | **V** |
| Incluye `ejecución`, y el objeto no pasó o no se chequeó | **S** |
| Solo `diseño`, solo `intención`, o `diseño` + `intención` | **S** |
| Cualquier combinación con una marca `≠ D-nn` | **D**, en discrepancia |

- El Agente GeneXus y el XPZ son la misma capa. `diseño, diseño` cuenta como una sola.
- Una afirmación en **D** no se usa como verdad en ningún otro lado: se cita su `D-nn`. Qué vale lo decide el responsable en la `DR-nn` correspondiente (pregunta 3, enmienda 1).
- La rev2 usa `[V]` para "leído en la KB", que es la capa de diseño. Por eso todo lo que viene de ella entra como **S** hasta encontrarlo en el Java o en test.

### Formato

Afirmación:

```
- El usuario debe tener al menos 5 caracteres. [V · capas: código, diseño · ev: hprvir07_impl.java E112; XPZ HPrvIr07 Events]
```

Regla, que además lleva id y clase:

```
- **R-07** Si COMPRAS_OBLIGACTABCO = 'S', la cuenta bancaria es obligatoria. [V · capas: código, diseño · ev: hprvir22_impl.java E132; XPZ HPrvIR22 Events 'Siguiente' · clase: parche]
```

> Los dos ejemplos ilustran el formato. Sus métodos (`E112`, `E132`) y las clases son de muestra. La tarea A1 los reemplaza por casos reales, verificados contra el Java.

Gramática que valida `verificar.py`:

```
[<V|S|D> · capas: <capa>(, <capa>)* · ev: <texto sin corchetes> (· clase: <esencial|parche|accidente>)? (· ≠ D-<nn>)?]
```

Capas válidas: `diseño`, `código`, `ejecución` e `intención`.

### Citas

- **XPZ:** objeto, parte y evento (`HPrvIR18 Events 'Siguiente'`), sin número de línea, porque la línea no es estable.
- **Java:** archivo y método (`hprvir18_impl.java E142`).
- **Ejecución:** `Snn` más la fecha, nunca la captura.
- **Manual:** archivo y página.

### Herramientas

Los tres scripts viven en `docs/herramientas/`, reciben las rutas como argumento y se corren con `python3 -I`. Sus fixtures son XML y Markdown **sintéticos**, escritos a mano en `docs/herramientas/fixtures/`: no se copia código del XPZ al repo. Cada script trae sus controles adentro y falla si alguno no se cumple.

- **`contar-xpz.py`.** Control: 119 objetos y 194 atributos, contando los hijos directos de `<Objects>` y de `<Attributes>`. Es un número fijo y está bien que lo sea, porque el XPZ no cambia. Si llega otro export, se actualiza a mano diciendo por qué. Fixture: un XML sintético con un objeto menos, que tiene que fallar.
- **`dependencias-xpz.py`.** Controles sobre el XML real:
  - `TPrvESP` en "activas", por `TPrvESP.Popup` en `HPrvIR18`;
  - `RPrvIR63` en "solo comentario";
  - `HPrvIR42` ausente, porque está presente en el export;
  - `StrReplace` ausente, porque es una función nativa. *(Era `Msg`; se cambió en A3 porque su control no podía fallar.)*
- **`verificar.py`.** Hace seis chequeos:
  1. índice contra archivos (CA1);
  2. gramática del bloque (CA15);
  3. estado declarado contra estado calculado (CA15);
  4. cada `R-nn` con su `clase` (CA22);
  5. cada `R-nn` tiene su lugar en `decisiones-rediseno.md`: una `DR-nn` propia si es parche o accidente, una `DR-nn` de confirmación si es esencial por defecto, o una fila de "Se mantiene" si es esencial con evidencia. Cada `D-nn` tiene su `DR-nn`, y cada `≠ D-nn` existe en `discrepancias.md` (CA14 y CA23);
  6. columnas del CSV, evidencia no vacía y `decision` respaldada (CA19 y CA24).

  Fixture: un caso que debe fallar en cada chequeo y uno que debe pasar.

### Clasificación (CA22)

- **Esencial:** la exige el negocio o una norma. Por ejemplo, validar el CUIT.
- **Parche:** resuelve un caso puntual y quedó pegada. Por ejemplo, una condición atada a un atributo de sistema que solo usa un cliente.
- **Accidente:**
  - código comentado o muerto (la validación del paso 6, las llamadas a `HPrvIR21` comentadas);
  - datos de un cliente fijos en el código (OSEP);
  - lógica duplicada entre modos;
  - texto de pantalla que contradice al código.

La clase es una **propuesta del análisis**. Si la evidencia no alcanza para elegir, se pone la más conservadora (`esencial`) y la entrada lo dice.

### Decisiones de rediseño (CA23)

Cada entrada `DR-nn` tiene:
- título;
- qué hace hoy, con enlaces a `R-nn` o `D-nn`;
- por qué parece parche o accidente;
- qué se pierde si se saca;
- recomendación (`mantener`, `rediseñar` o `eliminar`) con su motivo, en una línea;
- `decisión del responsable:`, vacío.

**Esenciales** *(decisión del responsable, 2026-10-23)*:
- Las **esenciales por defecto** (poca evidencia) llevan entradas de **confirmación rápida**, agrupadas por paso (`DR-nn` con varias `R-nn`), con la recomendación "mantener" y una línea de por qué.
- Las **esenciales con evidencia** van en una tabla final, "Se mantiene", con una fila por `R-nn`, que se recorre en un minuto.

Se ordenan **por impacto en el flujo**: primero las que cambian la secuencia de pasos, después las de validación y por último las cosméticas. Como decide una sola persona, la recomendación es directa, no un menú.

### Capa de ejecución

- **Navegación.** Antes de cada observación se carga `~/.config/genfin-gx.env` y se usa `agent-browser --session genfin`, abriendo `servlet/com.fin.<objeto>` directo.
- **Administración sobre usuarios de prueba** *(autorizado por el responsable, 2026-10-23)*. Se puede habilitar, dejar en espera o rechazar, **solo** sobre proveedores `zzprueba…`, para observar los estados de `PPrvIR02` y de `PrvPHabCS`. Antes de cada operación se confirma en pantalla que el proveedor seleccionado es uno de prueba. Cada operación va a la bitácora.
- **Quién escribe qué.** La bitácora y las capturas quedan fuera de `docs/`. Las escribe el coordinador; el ejecutor `docs` solo escribe en `docs/`.
- **Bitácora.** `trabajo/en-curso/registro-proveedores-docs/altas-prueba.md` lleva, por cada alta: usuario, CUIT usado, hora, resultado y fecha de baja. Vive en la unidad, no en `docs/`.
- **Altas.** El usuario empieza con `zzprueba` y sigue un número. La razón social dice "PRUEBA". El correo es una casilla propia.
- **Antes de la primera alta:**
  - el CUIT inventado se prueba primero en el paso 1: si `PPrvIR02` responde que no existe, se puede usar, y la prueba no expone ningún dato personal;
  - se revisa quién recibe los mensajes internos (`pcmsg001` a `CADMIN`, canales `ParmModPrv` a usuarios de Services), para que ninguno le llegue a una persona real.
- **Después de la primera alta:** se le pide a Emanuel que confirme que el usuario `zzprueba…` existe en GTF y **no** en producción. La consulta es **informativa y no bloquea**: el responsable decidió el 2026-10-23 tomar el Services de test como propio. Lo que frena las altas es una señal de producción, venga de esa respuesta o de cualquier otro lado.
- **Configuración del ambiente.** Si se compara contra la de producción, se anota "coincide" o "no coincide", nunca el valor.
- **Datos ajenos.** Ningún dato de un proveedor que ya exista en test se copia a `docs/`.

### Pendientes heredados

| Pendiente de `contexto-vivo.md` | Dónde se resuelve |
|---|---|
| Cruzar la rev2 con el Java | Tareas C y D |
| Estados como transiciones (`PPrvIR04`, `PPrvIR34`, `PPrvIR50`) | `estados.md` |
| Leer `HPrvIR39`→`HPrvIR52` | `modos.md` |
| Confirmar PostgreSQL en `GXcfg.java` | `integraciones.md` |
| Paso 6 | Resuelto en la enmienda 1: no es discrepancia, es un candidato a accidente |
| Citar los paneles del XML por evento | Convención de citas |

## Sospechado

| Supuesto | Cómo se verifica | Qué cambia si es falso |
|---|---|---|
| Cada objeto de `fin/` corresponde a la misma versión que corre en test. `fin/` no es una sola generación: va del 2025-09-23 al 2026-09-14 | E1, por objeto: elegir un texto o una condición que **difiera** entre el XPZ y el Java de ese objeto, y ver cuál de los dos muestra test | Ese objeto no puede dar **V** solo con `ejecución` (ver la tabla de estado) |
| El Java de `fin/` y el XPZ describen la misma versión del módulo | Cada diferencia que aparezca en C y D se carga como `D-nn` | Más entradas en `decisiones-rediseno.md`, no menos confianza en el método |
| El Services de test es propio (aceptado por el responsable) | Confirmación informativa de Emanuel después de la primera alta | Si la respuesta, o cualquier otra señal, indica producción: se paran las altas, se le avisa y se da de baja lo creado |
| La base de GEN de test es independiente de la de producción | Preguntarle a Emanuel junto con lo anterior | Lo mismo |
| La familia de nombres (`hprv*`, `pprv*`, `tprv*`, `rprv*`, `popro*`) delimita el módulo | Revisar a mano los objetos del borde: los que la clausura deja afuera por un solo salto | Se amplía la regla y se recalcula `universo-modulo.md` |
| Los mensajes internos del alta no le llegan a una persona real | Revisión previa a la primera alta (ver "Capa de ejecución") | Se posterga el alta hasta desviarlos |
| `features.csv` sigue siendo legible por `parity.py` de replica-recon con tres columnas extra y evidencias con comas | Leer `parity.py` sin instalarlo | Se entrega una vista con las seis columnas originales |
| La clasificación esencial/parche/accidente se puede justificar desde las fuentes | Si en C y D más de un tercio de las reglas cae en "esencial por defecto", se avisa | Las decisiones se apoyan más en la intuición del responsable que en evidencia, y hay que decírselo |

## Alternativas descartadas

- **Documentar primero todo el sistema y después pensar el rediseño.** El responsable no lo va a leer entero. El rediseño tiene que salir del análisis, no después de él.
- **Estado `[V]`/`[S]` escrito a mano.** Lo declarado vence: el estado se calcula a partir de las capas.
- **Un solo documento grande, como la rev2.** No deja controlar la cobertura por criterio.
- **Copiar la rev2 y corregirla encima.** Arrastra su `[V]`, que mide la capa de diseño.
- **Inventarios a mano, o desde `ObjectsIdentityMapping`.** Ese mapeo no registra el código comentado y no distingue lo activo de lo muerto.
- **Capturas o fragmentos de XPZ dentro del repo.** Pueden mostrar datos o copiar código. Los fixtures son sintéticos.

## Preguntas abiertas

- **Casilla de correo para las altas.** No llega nada porque la cola está desactivada, pero el campo es obligatorio y pasa por `PPrvIR39`.
- **¿Hay un rango de CUIT de prueba acordado en test?** Si no lo hay, se usa el método del paso 1 de "Capa de ejecución".
</content>
</invoke>
<invoke name="mcp__ccd_turn__update_plan">
<parameter name="advance">true