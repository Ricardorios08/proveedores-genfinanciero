# Paso 8 — HPrvIR06, representantes

Octavo panel del asistente. Lista a los representantes designados de la empresa y permite agregarlos, modificarlos y eliminarlos. **No exige ninguno**: el paso se puede atravesar vacío. Fuentes: rev2 §10 y §18, `HPrvIR06` en el XML y `hprvir06_impl.java`.

## Objeto

- `HPrvIR06`, "Datos de los Representantes de la Empresa", rotulado "PASO 8 de 11". [V · capas: código, diseño · ev: hprvir06_impl.java (texto 'PASO 8 de 11'); XPZ HPrvIR06 Form]
- Recibe `PrvPUSr` y `Modulo`. [V · capas: código, diseño · ev: hprvir06_impl.java e14AD2 ('Volver'); XPZ HPrvIR06 Parm]
- Llama a `TPrvRpr` (ventana emergente de representantes) y navega a `HPrvIR22`, `HPrvIR42` y `HPrvIR39`. [V · capas: código, diseño · ev: hprvir06_impl.java e11AD2 ('Agregar'), e12AD2 ('Siguiente'), e13AD2 ('Anterior'), e14AD2 ('Volver'); XPZ HPrvIR06 Events]

## Datos que pide

El panel muestra la grilla de representantes y delega la edición a `TPrvRpr`.

- Grilla con los íconos Modificar y Eliminar y la clave de línea `PrvRprNroLin`; el contenido de cada representante se carga en `TPrvRpr`, fuera de esta unidad. [V · capas: código, diseño · ev: hprvir06_impl.java e16AD2 (Load); XPZ HPrvIR06 Events Load]
- Agregar pone la línea en cero (valor nulo) y abre `TPrvRpr` en modo `INS`. [V · capas: código, diseño · ev: hprvir06_impl.java e11AD2 ('Agregar'); XPZ HPrvIR06 Events 'Agregar']
- Modificar y Eliminar abren `TPrvRpr` en modo `UPD` y `DLT` sobre la línea de la fila. [V · capas: código, diseño · ev: hprvir06_impl.java e18AD2 ('Modificar'), e17AD2 ('Eliminar'); XPZ HPrvIR06 Events 'Modificar', 'Eliminar']

## Validaciones

Tabla de reglas del panel. Ids R-237 a R-246.

| Regla | Qué exige o hace el sistema |
|---|---|
| **R-237** | No hay obligatoriedad de representantes: Siguiente no cuenta ni valida filas. A diferencia de rubros (R-225) y cuentas bancarias, un proveedor puede seguir sin ninguno. Clase por defecto: el texto de pantalla ("si Ud tiene Representantes designados, puede ingresarlos") coincide, pero la evidencia no dice si lo exige alguna norma. [V · capas: código, diseño · ev: hprvir06_impl.java e12AD2 ('Siguiente'); XPZ HPrvIR06 Events 'Siguiente'; XPZ HPrvIR06 Form (texto de pantalla); rev2 §10 · clase: esencial] |
| **R-238** | Siguiente fija la variable de sesión `regreso` en `1` y sigue a `HPrvIR22`. [V · capas: código, diseño · ev: hprvir06_impl.java e12AD2 ('Siguiente'); XPZ HPrvIR06 Events 'Siguiente' · clase: parche] |
| **R-239** | `HPrvIR22` usa `regreso` = `1` para que su Anterior vuelva a este panel; con otro valor vuelve a `HPrvIR02`. Pero `TPrvInsRP` ya había guardado en `regreso` el tipo de persona (0 o 1), y `HPrvIR41` lo lee para decidir su Anterior: al pisarlo, una persona física que retrocede desde el paso 7 hasta el 5 y pulsa Anterior iría a `HPrvIR17m` (paso 4, de persona jurídica) en vez de a `TPrvInsRP`. Es una lectura del código, sin ejecutar. [V · capas: código · ev: hprvir22_impl.java e1325M2 ('Anterior'); tprvinsrp_impl.java (escribe regreso con el tipo de persona); hprvir41_impl.java e131G42 ('Atras'); hprvir06_impl.java e12AD2 ('Siguiente') · clase: accidente] |
| **R-240** | Anterior vuelve siempre a `HPrvIR42` (paso 7). [V · capas: código, diseño · ev: hprvir06_impl.java e13AD2 ('Anterior'); XPZ HPrvIR06 Events 'Anterior'; rev2 §10 · clase: esencial] |
| **R-241** | Volver en modo `P` va a `HPrvIR39`; en cualquier otro modo devuelve `Modulo` al llamador. [V · capas: código, diseño · ev: hprvir06_impl.java e14AD2 ('Volver'); XPZ HPrvIR06 Events 'Volver'; rev2 §18 · clase: esencial] |
| **R-242** | La llamada de retorno a administración `HPrvIR21(PrvPUSr)` está comentada en 'Volver'; quedó el `Return`. [S · capas: diseño · ev: XPZ HPrvIR06 Events 'Volver' (línea comentada); rev2 §18.1 · clase: accidente] |
| **R-243** | En modo `I` el panel muestra el asistente (rótulo del paso, Siguiente, Anterior) con el título "Datos de los Representantes de la Empresa"; en `P` y `A` muestra el bloque de actualización y el título "Trabajar con Representantes", y oculta el rótulo del paso. [V · capas: código, diseño · ev: hprvir06_impl.java e15AD2 (Start); XPZ HPrvIR06 Events Start; rev2 §18 · clase: esencial] |
| **R-244** | Alta, cambio y baja de representantes se hacen en la ventana emergente `TPrvRpr` en los tres modos, y el panel se refresca después. [V · capas: código, diseño · ev: hprvir06_impl.java e11AD2 ('Agregar'), e18AD2 ('Modificar'), e17AD2 ('Eliminar'); XPZ HPrvIR06 Events 'Agregar', 'Modificar', 'Eliminar'; rev2 §10 · clase: esencial] |
| **R-245** | Las asignaciones de enlace de Modificar y Eliminar a `TPrvRpr.Link` están comentadas en Load; el enlace funciona por los eventos. [S · capas: diseño · ev: XPZ HPrvIR06 Events Load (líneas comentadas) · clase: accidente] |
| **R-246** | Start copia el usuario de la sesión de administración (clave `usr`) a una variable que ningún evento usa después. [V · capas: código, diseño · ev: hprvir06_impl.java e15AD2 (Start); XPZ HPrvIR06 Events Start · clase: accidente] |

## Condición de avance

- Siguiente avanza siempre a `HPrvIR22`, sin validar filas (R-237). [V · capas: código, diseño · ev: hprvir06_impl.java e12AD2 ('Siguiente'); XPZ HPrvIR06 Events 'Siguiente']
- Anterior vuelve a `HPrvIR42` sin validar (R-240). [V · capas: código, diseño · ev: hprvir06_impl.java e13AD2 ('Anterior'); XPZ HPrvIR06 Events 'Anterior']

## Capas

Capas: código, diseño; ejecución: todavía no observado (E4). No se consultó el manual (intención); el texto de pantalla citado en R-237 sale del XML.

Las reglas R-242 y R-245 son solo de diseño: el Java generado no conserva los comentarios. El chequeo de versión (E1) está pendiente.
