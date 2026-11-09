# Convenciones de docs/

Cómo se escribe y cómo se lee todo lo que hay en `docs/`. Si un documento contradice este archivo, vale este archivo, y el documento se corrige.

## Para qué es docs/

Para decidir el **rediseño** del módulo Registro de Proveedores de GEN Financiero sin estudiar el sistema original. Se lee en este orden:

1. `mapa-flujos.md`: el flujo de un vistazo, con los puntos de dolor.
2. `decisiones-rediseno.md`: qué mantener, qué rediseñar y qué eliminar, cada una con su recomendación.
3. El resto es **respaldo**: cada decisión enlaza a afirmaciones con evidencia, para verificarla sin abrir el XPZ ni el manual.

## Capas

Las fuentes se agrupan por capa. Dos fuentes de la misma capa repiten la misma mirada.

| Capa | Fuente | Qué prueba |
|---|---|---|
| `diseño` | XML del export GeneXus (`GENFin-RegProv.xpz`) y el Agente GeneXus, que tiene importado el mismo export. **Cuentan como una sola** | Lo que se definió en la KB |
| `código` | Java generado (`fin.zip`) | Lo que se compiló |
| `ejecución` | Portal de test, observado con fecha | Lo que pasa de verdad, con la configuración de ese ambiente |
| `intención` | Manuales PDF | Lo que el usuario cree que hace |

## Estado de una afirmación

El estado se escribe para que el lector lo vea, pero **no se elige**: `verificar.py` lo recalcula a partir de las capas y rechaza el archivo si no coincide.

| Capas presentes | Estado |
|---|---|
| Incluye `código` | **V**, verificado |
| Incluye `ejecución`, y el objeto de la pantalla pasó el chequeo de versión | **V** |
| Incluye `ejecución`, y el objeto no pasó o no se chequeó | **S**, sospechado |
| Solo `diseño`, solo `intención`, o `diseño` + `intención` | **S** |
| Cualquier combinación con una marca `≠ D-nn` | **D**, en discrepancia |

Una afirmación en **D** no se usa como verdad en ningún otro lado: se cita su `D-nn`. Qué vale lo decide el responsable en la decisión `DR-nn` correspondiente.

Las reglas de la rev2 del Agente GeneXus (`[V]` = "leído en la KB") son de la capa `diseño`. Entran como **S** hasta encontrarlas en el Java o en test.

## Formato

### Afirmaciones

En los archivos de comportamiento (`pasos/`, `modos.md`, `modelo-datos.md`, `estados.md`, `integraciones.md`, `mensajes.md`, `configuracion.md`, `cliente-vs-producto.md` y `seguridad.md`), **cada ítem de lista de primer nivel y cada fila de tabla es una afirmación y lleva un bloque**. El texto explicativo va en párrafos, no en listas.

Gramática del bloque:

```
[<V|S|D> · capas: <capa>(, <capa>)* · ev: <evidencia sin corchetes> (· clase: <esencial|parche|accidente>)? (· ≠ D-<nn>)?]
```

### Reglas

Una regla es una afirmación que dice qué exige o qué hace el sistema. Lleva un id `**R-nn**` al principio y siempre un campo `clase`. Los ids no se reutilizan.

### Ids

| Id | Qué es | Dónde vive |
|---|---|---|
| `R-nn` | Regla | Archivos de comportamiento |
| `D-nn` | Discrepancia entre capas | `discrepancias.md` |
| `DR-nn` | Decisión de rediseño | `decisiones-rediseno.md` |
| `Snn` | Pantalla (objeto + modo) | `pantallas.md` |
| `Fnn` | Flujo | `flujos.md` |

## Ejemplos reales

Verificados contra el Java el 2026-10-23. `probar.py` los lee de este bloque y comprueba que su estado coincide con el calculado, y que con el estado cambiado dejan de coincidir.

```
- El nombre de usuario tiene que tener al menos 5 caracteres: si no, el paso 2 muestra "ERROR: El nombre de usuario no puede ser menor de 5 caracteres." [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente'); XPZ HPrvIr07 Events 'Siguiente']
- **R-ej** Si el atributo de sistema COMPRAS_OBLIGACTABCO vale 'S', en el alta (modo I) el paso 9 oculta el enlace txt_Sgte y muestra el texto TextObliga. [V · capas: código, diseño · ev: hprvir22_impl.java e1525M2 (Start); XPZ HPrvIR22 Events Start · clase: esencial]
```

La clase del segundo ejemplo es `esencial` por defecto: la evidencia no alcanza todavía para decir si es un parche.

## Clases (CA22)

La clase es una **propuesta del análisis**. La decisión es del responsable.

- **esencial**: la exige el negocio o una norma.
- **parche**: resuelve un caso puntual y quedó pegada.
- **accidente**: código comentado o muerto, un dato de un cliente fijo en el código, lógica duplicada entre modos, o un texto de pantalla que contradice al código.

Si la evidencia no alcanza para elegir, va `esencial`, la más conservadora, y la regla llega igual al responsable como confirmación rápida en `decisiones-rediseno.md`.

## Citas

- **XPZ:** objeto, parte y evento: `XPZ HPrvIR18 Events 'Siguiente'`. Sin número de línea, porque la línea no es estable.
- **Java:** archivo y método, con el evento entre paréntesis cuando el método lo dice en su comentario (`/* 'Siguiente' Routine */`): `hprvir07_impl.java e12A22 ('Siguiente')`.
- **Ejecución:** `Snn` y la fecha de la observación: `S03 2026-10-24`. Nunca la captura, que queda fuera del repositorio.
- **Manual:** archivo y página.

Se transcriben solo las líneas necesarias. Ni el Java ni el código GeneXus se copian en bloque.

## Datos

- Nombres de atributos de sistema, de parámetros y de variables: sí. **Sus valores: nunca.**
- Datos personales del manual, del ambiente de test o de los metadatos del XML: nunca. Si hace falta un ejemplo, se inventa y se marca como inventado.

## Herramientas

Todas se corren desde la raíz del repo con `python3 -I`, y reciben las rutas como argumento.

| Script | Qué hace |
|---|---|
| `herramientas/contar-xpz.py <xml>` | Cuenta objetos y atributos del export. Control: 119 y 194 |
| `herramientas/dependencias-xpz.py <xml>` | Lista lo que el código llama y no viene en el export, separando lo activo de lo comentado |
| `herramientas/verificar.py [docs]` | Los seis chequeos (índice, gramática, estado, clase, decisiones y CSV) |
| `herramientas/probar.py` | Comprueba que cada control de las otras herramientas pueda fallar |

`herramientas/fixtures/` tiene las entradas sintéticas de las pruebas. No contiene código del XPZ ni datos.

## Chequeo de versión

`fin/` no es una sola generación: sus archivos van del 2025-09-23 al 2026-09-14. Por cada objeto se busca algo que **difiera** entre el XPZ y el Java, y se mira cuál de los dos muestra el portal de test. Solo los objetos con resultado "coincide con Java" permiten que una observación en test dé **V** sin la capa `código`.

Método (2026-10-23): se compararon los literales de texto de las partes de código activas y del formulario de cada panel del XPZ contra su `_impl.java`, y los textos vistos en test contra el Java.

| Objeto | Resultado | Fecha |
|---|---|---|
| `HPrvIR02` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 1) | 2026-10-23 |
| `HPrvIr07` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 2) | 2026-10-23 |
| `TPrvInsRP` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 3) | 2026-10-23 |
| `HPrvIR17m` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 4) | 2026-10-23 |
| `HPrvIR41` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 5) | 2026-10-23 |
| `HPrvIR18` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 6) | 2026-10-23 |
| `HPrvIR42` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 7) | 2026-10-23 |
| `HPrvIR06` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 8) | 2026-10-23 |
| `HPrvIR22` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 9) | 2026-10-23 |
| `HPrvIR10` | no discrimina: los dos únicos textos que difieren son del evento de cliente 'Imprimir', que el Java extraído no contiene (paso 10) | 2026-10-23 |
| `HPrvIR09` | no discrimina: el XPZ y el Java tienen los mismos textos visibles (paso 11) | 2026-10-23 |
| `popro001` | coincide con Java (título, vistos en test el 2026-10-23). No está en el XPZ, así que no hay contra qué discriminar | 2026-10-23 |
| `hprvir25` | coincide con Java (título y columna 'Estado Habilitación', vistos en test el 2026-10-23). No está en el XPZ, así que no hay contra qué discriminar | 2026-10-23 |
| `hprvir31` | coincide con Java (título, vistos en test el 2026-10-23). No está en el XPZ, así que no hay contra qué discriminar | 2026-10-23 |
| `hprvir40` | coincide con Java (título, vistos en test el 2026-10-23). No está en el XPZ, así que no hay contra qué discriminar | 2026-10-23 |
| `hprvir56` | coincide con Java (título de ventana, título de panel y opción 'Registro Incompleto', vistos en test el 2026-10-23). No está en el XPZ, así que no hay contra qué discriminar | 2026-10-23 |

**Conclusión.** En los 11 pasos el XPZ y el Java coinciden en todo lo visible, así que una observación en test no puede decir cuál de las dos versiones corre. Para esos pasos, una afirmación **V** tiene que tener la capa `código`: la `ejecución` sola da **S**. En las pantallas de administración, que solo existen en el Java, test coincide con el Java en todo lo comparado.
