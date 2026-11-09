# Paso 2 — HPrvIr07, usuario y categoría

Ids de este archivo: reglas R-120 a R-139 y discrepancias D-110 a D-112. Los textos de mensajes se transcriben tal cual salen del Java.

## Objeto

- El objeto es el panel web `HPrvIr07`, que se muestra como "PASO 2 de 11" con el subtítulo "Alta en el Registro de Proveedores". Recibe el CUIT (`PrvIgnTi`, `PrvIgnNr`, `PrvIgnDi`), `Prove`, la categoría recibida (`CatRec`) y `band`, y fija el módulo en `I`. [V · capas: código, diseño · ev: hprvir07_impl.java e11A22 (Start) y wb_table2_5_A22e; XPZ HPrvIr07 Rules (parm) y Events Start]
- Sirve para que el proveedor elija el nombre de usuario con el que va a entrar al sistema. Después llama al paso 3 (`TPrvInsRP`) con el usuario, la categoría, `Prove` (que el paso 3 recibe como `BloqueaNombre`), el CUIT, el módulo y el modo `INS` o `UPD`. [V · capas: código, diseño · ev: hprvir07_impl.java S122 ('INSREG'); XPZ HPrvIr07 Events Sub 'insReg'; tprvinsrp Rules (parm)]
- **R-120** Al abrirse (Start), busca en `PrvPerfil` un perfil con ese CUIT. Si existe, oculta la tabla de elección, muestra "Su nombre de usuario se muestra a continuación. Para continuar haga click en Siguiente." con el usuario deshabilitado, y deja `Valida` en 0. Si no existe, llama a `PPrvIR03` para obtener un usuario desde PROVE, muestra la tabla de elección y deja `Valida` en 1. [D · capas: código, diseño, intención · ev: hprvir07_impl.java e11A22 (Start); XPZ HPrvIr07 Events Start; manual Registro p. 8 · clase: esencial · ≠ D-02]
- El XPZ declara también una variable `Pass2`, pero ningún campo del panel ni ningún evento la usan. [V · capas: código, diseño · ev: hprvir07_impl.java e11A22 (Start) y e12A22 ('Siguiente'); XPZ HPrvIr07 Variables]

## Datos que pide

- El nombre de usuario (variable `PrvPUSr`): un campo de 20 posiciones, que el navegador convierte a mayúsculas al editar. [V · capas: código, diseño · ev: hprvir07_impl.java wb_table6_40_A22e; XPZ HPrvIr07 Variables]
- La categoría (variable `Cat`): un grupo de opciones que existe en el formulario pero está oculto. Start lo oculta y deja el valor en '1'. [V · capas: código, diseño · ev: hprvir07_impl.java e11A22 (Start) y wb_table7_59_A22; XPZ HPrvIr07 Events Start]
- No hay ningún campo de contraseña en el panel. [V · capas: código, diseño · ev: hprvir07_impl.java wb_table6_40_A22e y wb_table7_59_A22; XPZ HPrvIr07 Variables y Events]
> **Corrección a la rev2** (rev2 §4, retirado D-111): La rev2 dice que este paso pide "nombre de usuario, contraseña y categoría".
- El texto "El Nombre de Usuario debe tener entre 5 y 20 caracteres, y se recomienda que contenga letras y números. No se permiten caracteres especiales ni espacios." está visible en pantalla. [V · capas: código, diseño · ev: hprvir07_impl.java wb_table5_28_A22; XPZ HPrvIr07 Form]
- El texto "Además, es necesario que indique con que Categoría desea registrarse." está en el formulario, pero oculto junto con el grupo de opciones. [V · capas: código, diseño · ev: hprvir07_impl.java wb_table5_28_A22 y e11A22 (Start); XPZ HPrvIr07 Form y Events Start]

## Validaciones

- **R-121** La categoría se descarta: Start la deja en '1' y el valor que llega del paso 1 (`CatRec`, '1' o '9') no se lee en ningún evento. El paso 3 siempre recibe '1' por esta vía, así que la categoría '9' que calcula el paso 1 no tiene efecto. Eso hace que en el alta, el número de Ingresos Brutos sea obligatorio en el paso 3 (R-145). [V · capas: código, diseño · ev: hprvir07_impl.java e11A22 (Start) y S122 ('INSREG'); XPZ HPrvIr07 Events Start · clase: accidente]
- **R-122** Si el usuario o la categoría están vacíos, muestra "ERROR: Debe seleccionar un Nombre de Usuario" y le agrega ", y una Categoría. " solo si la etiqueta de categoría está visible (nunca lo está). Con la categoría fija en '1', la única condición que puede dispararse es la del usuario. [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente'); XPZ HPrvIr07 Events 'Siguiente'; rev2 §4 · clase: esencial]
- **R-123** El nombre de usuario tiene que tener al menos 5 caracteres: si no, muestra "ERROR: El nombre de usuario no puede ser menor de 5 caracteres." [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente'); XPZ HPrvIr07 Events 'Siguiente'; rev2 §4 · clase: esencial]
- **R-124** El máximo de 20 caracteres no lo valida el evento: lo impone el tamaño del campo, y coincide con el texto de pantalla. [V · capas: código · ev: hprvir07_impl.java wb_table6_40_A22e · clase: esencial]
- **R-125** El valor se pasa a mayúsculas: el navegador lo hace al editar y el servidor vuelve a hacerlo al leer el campo. [V · capas: código · ev: hprvir07_impl.java wb_table6_40_A22e y strupA20 · clase: esencial]
- **R-126** Unicidad: si no existe perfil con ese CUIT (`Exist` distinto de 5) y otro `PrvPerfil` ya tiene ese usuario, muestra "ERROR: El "Nombre de Usuario" que ha seleccionado ya ha sido elegido por otro proveedor. Por favor seleccione otro Nombre de Usuario." Si el perfil del propio CUIT existe, la comprobación se salta. [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente'); XPZ HPrvIr07 Events 'Siguiente'; rev2 §4 · clase: esencial]
- **R-127** Juego de caracteres: la rutina 'CONTROLA' recorre el usuario y rechaza cualquier carácter que no sea de la A a la Z o del 0 al 9. El mensaje es "ERROR: El nombre seleccionado incluye caracteres no permitidos, como por ejemplo: Ñ¡?=# o espacios. Por Favor, haga el reemplazo." (la variante del caso con `PPrvIR09` pierde el punto final). La rutina corre cuando `band` es 0, o cuando `band` no es 0 y `Valida` es 1. Cuando el perfil ya existe (`Valida` en 0) no corre. [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente') y S112 ('CONTROLA'); XPZ HPrvIr07 Events 'Siguiente' y Sub 'Controla'; rev2 §4 · clase: esencial]
- **R-128** Si `band` es 0 (el proveedor no existe en PROVE), el modo para el paso 3 es `INS`: se crea el perfil en el paso 3. [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente'); XPZ HPrvIr07 Events 'Siguiente'; rev2 §4 · clase: esencial]
- **R-129** Si `band` no es 0 y `Valida` es 1, llama a `PPrvIR09` con el CUIT y el usuario. Solo si devuelve `P` el modo es `UPD` y sigue; si devuelve otra cosa muestra "ERROR: No se pudo generar el usuario ingresado." [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente'); XPZ HPrvIr07 Events 'Siguiente'; rev2 §4 · clase: esencial]
> **Corrección a la rev2** (rev2 §4, retirado D-110): La rev2 explica el modo `UPD` como "el perfil ya existía". En el Java, `PPrvIR09` devuelve `P` justo después de insertar un `PrvPerfil` (con sus domicilios, representantes y rubros) copiado del sistema viejo PROVE. Si el perfil ya existía, devuelve el estado de habilitación que tenía.
- En el Java, `PPrvIR09` devuelve `P` solo después de insertar el perfil nuevo desde PROVE. [V · capas: código · ev: pprvir09.java privateExecute (rama que asigna el flag P antes del INSERT en PrvPerfil)]
- **R-130** Si `band` no es 0 y `Valida` es 0 (el perfil ya existe), el modo es `UPD` y sigue sin llamar a `PPrvIR09` y sin controlar caracteres. [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente'); XPZ HPrvIr07 Events 'Siguiente' · clase: esencial]
- **R-131** La llamada a `Pprvir07(&PrvPUSr,&PrvPUSrAux)`, que cambiaría el nombre de usuario de un perfil ya existente cuando no tiene nombre auxiliar, está comentada en el XPZ. También está comentada una condición `and not &PrvNomAux.IsEmpty()` en Start. [S · capas: diseño · ev: XPZ HPrvIr07 Events 'Siguiente' y Start (líneas comentadas) · clase: accidente]

## Condición de avance

- Llama al paso 3 (`TPrvInsRP`) en modo `INS` o `UPD` según R-128, R-129 y R-130, cuando el usuario pasó R-122 a R-127. [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente') y S122 ('INSREG'); XPZ HPrvIr07 Events 'Siguiente' y Sub 'insReg']
- Si falla cualquier validación se queda en el paso 2 con el mensaje. [V · capas: código, diseño · ev: hprvir07_impl.java e12A22 ('Siguiente'); XPZ HPrvIr07 Events 'Siguiente']
- El botón "Anterior" usa el evento estándar de cancelación; su destino no se investigó en este paso. [V · capas: código · ev: hprvir07_impl.java wb_table2_5_A22e]

## Capas

Capas: diseño (XPZ y rev2 §4), código (Java generado); ejecución: todavía no observado (E4). Los manuales (intención) no se consultaron para este paso.

XPZ y Java coinciden en el comportamiento del evento 'Siguiente'. Las discrepancias son de la rev2 contra el código: la contraseña que el paso no pide (D-111), la interpretación del modo `UPD` (D-110) y el texto de categoría que el panel oculta (D-112). `PPrvIR03`, `PPrvIR09` y la tabla `PrvPerfil` se tocaron solo en la medida necesaria para entender el modo.
