# Paso 5 — HPrvIR41, domicilios

Quinto panel del asistente de alta. El proveedor carga sus domicilios (legal y real, entre otros) y el panel decide a qué paso sigue según el tipo de persona. Fuentes: rev2 §7, `HPrvIR41` en el XML y `hprvir41_impl.java`.

## Objeto

- `HPrvIR41`, "Domicilios de su Empresa", rotulado "PASO 5 de 11". [V · capas: código, diseño · ev: hprvir41_impl.java (texto 'PASO 5 de 11'); XPZ HPrvIR41 Form]
- Recibe `PrvPUSr` y `Modulo` (valores `I`, `P` o `A`). [V · capas: código, diseño · ev: hprvir41_impl.java e141G42 ('Volver'); XPZ HPrvIR41 Parm]
- Llama a `TPrvDom` (ventana emergente de alta, cambio y baja), a `PPrvIR62` (categoría y tipo de persona) y navega a `HPrvIR18`, `HPrvIR42`, `TPrvInsRP`, `HPrvIR17m`, `HPrvIR02` y `HPrvIR39`. [V · capas: código, diseño · ev: hprvir41_impl.java e121G42 ('Siguiente'), e131G42 ('Atras'), e141G42 ('Volver'); XPZ HPrvIR41 Events]

## Datos que pide

El panel no pide campos de texto: muestra una grilla y delega la edición a `TPrvDom`, que queda fuera de esta unidad hasta que se documente como punto de contacto.

- Grilla "Domicilios" con la columna Tipo (derivada de `PrvDomTip` con el dominio `GenProDomTip`), calle `PrvDomCal`, número `PrvDomNro`, localidad `PrvDomLoc` y provincia `PrvDomPcia`. [V · capas: código, diseño · ev: hprvir41_impl.java e121G42 ('Siguiente'); XPZ HPrvIR41 Form]
- Columnas ocultas de la grilla: `PrvDomNroOrden` y `PrvDomTip`, que viajan a `TPrvDom` para identificar la fila. [V · capas: código, diseño · ev: hprvir41_impl.java e171G42 ('Modificar'); XPZ HPrvIR41 Form]
- Dominio `GenProDomTip`: 1 Domicilio Legal Local, 2 Domicilio Real, 3 Domicilio Especial / Otro, 4 Domicilio Representante Sucursal Local. [V · capas: código · ev: gxdomaingenprodomtip.java]
- Categoría del proveedor (`PrvCat`) y tipo de persona (`PrvObs`: 1 jurídica, 0 física) se leen con `PPrvIR62` al iniciar el panel. [V · capas: código, diseño · ev: hprvir41_impl.java e151G42 (Start); XPZ HPrvIR41 Events Start]
- Agregar, Modificar y Eliminar pasan a `TPrvDom` el modo `INS`, `UPD` o `DLT` junto con `PrvDomTip` y `PrvDomNroOrden`. [V · capas: código, diseño · ev: hprvir41_impl.java e111G42 ('Agregar'), e171G42 ('Modificar'), e181G42 ('Eliminar'); XPZ HPrvIR41 Events 'Agregar', 'Modificar', 'Eliminar']

## Validaciones

Tabla de reglas del panel. Ids R-201 a R-212.

| Regla | Qué exige o hace el sistema |
|---|---|
| **R-201** | Para pasar al paso siguiente tiene que haber al menos un domicilio legal (tipo 1). Con solo un domicilio real no alcanza. Si no, muestra "ERROR: No ha ingresado domicilio Legal OBLIGATORIO..." [D · capas: código, diseño, intención · ev: hprvir41_impl.java e121G42 ('Siguiente'); XPZ HPrvIR41 Events 'Siguiente'; rev2 §7; manual Registro p. 14 · clase: esencial · ≠ D-03] |
| **R-202** | La bifurcación de salida depende del tipo de persona: jurídica (`PrvObs` = 1) sigue a `HPrvIR18` (paso 6), física sigue a `HPrvIR42` (paso 7). [V · capas: código, diseño · ev: hprvir41_impl.java e121G42 ('Siguiente'); XPZ HPrvIR41 Events 'Siguiente'; rev2 §7 · clase: esencial] |
| **R-203** | El tipo de domicilio de la grilla no es editable (campo `TipoDom` deshabilitado desde Start). [V · capas: código, diseño · ev: hprvir41_impl.java e151G42 (Start); XPZ HPrvIR41 Events Start · clase: esencial] |
| **R-204** | El enlace Eliminar de la grilla se anula para el domicilio real (tipo 2) y, si la categoría es `1`, también para el legal (tipo 1). Los demás domicilios sí se pueden eliminar. Clase por defecto: la evidencia no dice qué norma lo motiva. [V · capas: código, diseño · ev: hprvir41_impl.java e161G42 (Domicilios.Load); XPZ HPrvIR41 Events Domicilios.Load · clase: esencial] |
| **R-205** | El texto "Si además Ud. ha optado por la CATEGORIA I, debe consignar obligatoriamente un domicilio LEGAL en la ciudad" se oculta siempre en Start, y ningún código exige que el domicilio legal esté en la ciudad: el único control es R-201. [V · capas: código, diseño · ev: hprvir41_impl.java e151G42 (Start), e121G42 ('Siguiente'); XPZ HPrvIR41 Events Start · clase: accidente] |
| **R-206** | Condición alternativa por categoría, comentada en 'Siguiente': combinaba domicilio legal y real según `PrvCat` = `1` o `2`. Hoy solo rige R-201. [S · capas: diseño · ev: XPZ HPrvIR41 Events 'Siguiente' (comentario con &doms y &PrvCat); no aparece en hprvir41_impl.java · clase: accidente] |
| **R-207** | En modo `I` el panel muestra los botones y textos del asistente (Anterior, Siguiente, "PASO 5 de 11") y oculta Volver. En `P` y `A` hace lo contrario y el título pasa a "Trabajar con Domicilios". Solo `P` muestra además la descripción UPDdsc, así que `A` queda sin ninguna descripción. [V · capas: código, diseño · ev: hprvir41_impl.java e151G42 (Start); XPZ HPrvIR41 Events Start; rev2 §18 · clase: esencial] |
| **R-208** | Anterior vuelve según la variable de sesión `regreso`: `0` (persona física) a `TPrvInsRP` (paso 3), `1` (jurídica) a `HPrvIR17m` (paso 4) y cualquier otro valor a `HPrvIR02` (paso 1, sesión expirada). Clase por defecto. [V · capas: código, diseño · ev: hprvir41_impl.java e131G42 ('Atras'); XPZ HPrvIR41 Events 'Atras' · clase: esencial] |
| **R-209** | Volver en modo `P` va a `HPrvIR39`; en cualquier otro modo devuelve `Modulo` al llamador. [V · capas: código, diseño · ev: hprvir41_impl.java e141G42 ('Volver'); XPZ HPrvIR41 Events 'Volver'; rev2 §7 · clase: esencial] |
| **R-210** | La llamada de retorno a administración `HPrvIR21(PrvPUSr)` está comentada en 'Volver'; quedó solo el `Return`. [S · capas: diseño · ev: XPZ HPrvIR41 Events 'Volver' (línea comentada); rev2 §18.1 · clase: accidente] |
| **R-211** | Start copia el usuario de la sesión de administración (clave `usr`) a una variable que ningún evento usa después. [V · capas: código, diseño · ev: hprvir41_impl.java e151G42 (Start); XPZ HPrvIR41 Events Start · clase: accidente] |
| **R-212** | Las altas, cambios y bajas de domicilio se hacen en la ventana emergente `TPrvDom` en los tres modos; después de cada una el panel se refresca. [V · capas: código, diseño · ev: hprvir41_impl.java e111G42 ('Agregar'), e171G42 ('Modificar'), e181G42 ('Eliminar'); XPZ HPrvIR41 Events 'Agregar' · clase: esencial] |

El interior de `TPrvDom` (qué campos pide y qué valida) no está en esta unidad.

## Condición de avance

- Siguiente avanza solo si hay domicilio legal (R-201). Destino: `HPrvIR18` si es persona jurídica, `HPrvIR42` si es física (R-202). [V · capas: código, diseño · ev: hprvir41_impl.java e121G42 ('Siguiente'); XPZ HPrvIR41 Events 'Siguiente' · clase: esencial]
- Anterior no valida nada y vuelve según `regreso` (R-208). [V · capas: código, diseño · ev: hprvir41_impl.java e131G42 ('Atras'); XPZ HPrvIR41 Events 'Atras']
- Eliminar el único domicilio legal no está bloqueado cuando la categoría no es `1`; el control recae solo en Siguiente. [V · capas: código · ev: hprvir41_impl.java e161G42 (Domicilios.Load), e121G42 ('Siguiente')]

## Capas

Capas: código, diseño; ejecución: todavía no observado (E4). No se consultó el manual (intención).

No hay versión cruzada con el portal de test: el chequeo de versión (E1) está pendiente.
