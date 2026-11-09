# Paso 4 — HPrvIR17m, datos de la sociedad (persona jurídica)

Ids de este archivo: reglas R-180 a R-199. Los textos de mensajes se transcriben tal cual salen del Java. La rev2 tomó este objeto solo del XPZ; acá se cruza además con el Java generado.

## Objeto

- El objeto es el panel web `HPrvIR17m`, que se muestra como "PASO 4 de 11" con las secciones "Datos del Contrato Constitutivo" e "Integrantes de la Sociedad". Recibe el usuario (`PrvPUSr`) y el módulo. [V · capas: código, diseño · ev: hprvir17m_impl.java wb_table3_22_25K2e y e1925K2 (Start); XPZ HPrvIR17m Rules (parm)]
- Solo se llega desde el paso 3 cuando el tipo de persona es jurídica. Si es física, el paso 3 salta al 5. [V · capas: código, diseño · ev: tprvinsrp_impl.java e12IZ2 (After Trn); XPZ TPrvInsRP Events After Trn]
- En el módulo `I` el título es "Ingrese los Datos de la Sociedad" y se muestran los botones de asistente. En los demás es "Trabajar Datos de la Sociedad" y se muestran "Aceptar" y "Volver". [V · capas: código, diseño · ev: hprvir17m_impl.java e1925K2 (Start); XPZ HPrvIR17m Events Start]
- Al abrirse (Start) lee los datos ya guardados de la sociedad con `PPrvIR25m`, los nombres de país, provincia y localidad con `PPrvIR17`, y la categoría y el tipo de persona con `PPrvIR62`. [V · capas: código, diseño · ev: hprvir17m_impl.java e1925K2 (Start); XPZ HPrvIR17m Events Start]
- La leyenda "La documentación respaldatoria de la información consignada en esta pantalla debe ser presentada en nuestras oficinas." se asigna en Start, pero el XPZ la deja con `Visible = 0`: nunca se muestra. [D · capas: diseño, intención · ev: XPZ HPrvIR17m Events Start; manual Registro p. 12 · ≠ D-06]
- Un cartel fijo avisa: "Atención: Debe ingresar al menos un integrante para poder continuar. Para ello, luego de completar los datos iniciales haga clic en el botón agregar que se encuentra en la parte inferior de la pantalla." [V · capas: código, diseño · ev: hprvir17m_impl.java wb_table3_22_25K2e; XPZ HPrvIR17m Form]

## Datos que pide

- Fecha de Constitución (`PrvFchConSoc`), marcada con '*'. [V · capas: código, diseño · ev: hprvir17m_impl.java wb_table4_37_25K2; XPZ HPrvIR17m Form]
- Fecha de Inscripción (`PrvFchInscSoc`), marcada con '*'. [V · capas: código, diseño · ev: hprvir17m_impl.java wb_table4_37_25K2; XPZ HPrvIR17m Form]
- País, Provincia y Localidad de Inscripción (`PrvSocPaisCgo`, `PrvSocPciaCgo`, `PrvSocLocCgo`), marcadas con '*'. Se ingresan por código, con ayuda de las pantallas de búsqueda (`PromptPaises`, `PromptProvin`, `PromptLoc`). El nombre se completa solo al cambiar cada código con `GELocalid04`, `GELocalid05` y `GELocalid06`. [V · capas: código, diseño · ev: hprvir17m_impl.java e1625K2, e1725K2, e1825K2 y S122, S132, S142; XPZ HPrvIR17m Rules (prompt) y Events]
- Tipo de Asociación (`PrvCla`), marcado con '*' pero sin validación (R-190). [V · capas: código, diseño · ev: hprvir17m_impl.java wb_table4_37_25K2 y e1225K2 ('Siguiente'); XPZ HPrvIR17m Form y Events 'Siguiente']
- Otros Datos (`PrvSocOtros`), texto libre. [V · capas: código, diseño · ev: hprvir17m_impl.java wb_table4_37_25K2; XPZ HPrvIR17m Form]
- Una grilla de integrantes, con el cargo y si es representante legal ("Sí" o "No"). El panel traduce los 17 cargos del 0 al 16 (de Presidente a Otro) con una tabla escrita en el propio evento de carga. [V · capas: código, diseño · ev: hprvir17m_impl.java e2025K2 (Integrantes_Load); XPZ HPrvIR17m Events integrantes.Load]

## Validaciones

- **R-180** La fecha de constitución es obligatoria: si falta, muestra "Debe ingresar la fecha de constitución de la sociedad". [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); XPZ HPrvIR17m Events 'Siguiente'; rev2 §6 · clase: esencial]
- **R-181** La fecha de inscripción es obligatoria: si falta, muestra "Debe ingresar la fecha de inscripción de la sociedad". [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); XPZ HPrvIR17m Events 'Siguiente'; rev2 §6 · clase: esencial]
- **R-182** El país es obligatorio: si falta, muestra "Debe ingresar país". [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); XPZ HPrvIR17m Events 'Siguiente'; rev2 §6 · clase: esencial]
- **R-183** La provincia es obligatoria: si falta, muestra "Debe ingresar provincia". [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); XPZ HPrvIR17m Events 'Siguiente'; rev2 §6 · clase: esencial]
- **R-184** La localidad es obligatoria: si falta, muestra "Debe ingresar localidad". [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); XPZ HPrvIR17m Events 'Siguiente'; rev2 §6 · clase: esencial]
- **R-185** La combinación de país, provincia y localidad tiene que existir en la tabla `Localidade` (`PPrvIR13`). Si no, muestra "No existe país, provincia, localidad. Por favor revise los datos ingresados." Las reglas anteriores se evalúan primero, en el orden de R-180 a R-184. [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); pprvir13.java privateExecute; XPZ HPrvIR17m Events 'Siguiente'; rev2 §6 · clase: esencial]
- **R-186** Hay que tener al menos un integrante (`PPrvIR26` devuelve 'S' si existe alguna fila de `PrvPJ` y el perfil tiene `PrvPJUltNro` de 1 o más). Si devuelve 'N', muestra "Debe ingresar los integrantes de la sociedad para poder continuar." Si devuelve otra cosa, o si la grabación previa no dio '1', muestra "ERROR. No se guardaron los datos." [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); pprvir26.java privateExecute; XPZ HPrvIR17m Events 'Siguiente'; rev2 §6 · clase: esencial]
- **R-187** "Siguiente" graba los datos de la sociedad con `PPrvIR21m` antes de comprobar los integrantes. Si falta el integrante, los datos igual quedan guardados y el paso no avanza. `PPrvIR21m` actualiza en `PrvPerfil` las fechas, el lugar, "otros datos" y la clase. [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); pprvir21m.java privateExecute; XPZ HPrvIR17m Events 'Siguiente' · clase: esencial]
- **R-188** "Agregar" integrante graba primero la sociedad con `PPrvIR21m`, sin ninguna de las validaciones de R-180 a R-185, y abre `TPrvPJ` en una ventana emergente en modo `INS`. [V · capas: código, diseño · ev: hprvir17m_impl.java e1125K2 ('Agregar'); XPZ HPrvIR17m Events 'Agregar'; rev2 §6 · clase: esencial]
- **R-189** "Modificar" y "Eliminar" abren `TPrvPJ` en una ventana emergente, en modo `UPD` y `DLT`, y refrescan el panel. [V · capas: código, diseño · ev: hprvir17m_impl.java e2125K2 ('Modificar') y e2225K2 ('Eliminar'); XPZ HPrvIR17m Events 'Modificar' y 'Eliminar'; rev2 §6 · clase: esencial]
- **R-190** La lista de Tipo de Asociación (`PrvCla`) depende del tipo de persona: para una jurídica se quitan las opciones 1 y 2; para una física quedan solo "UNIPERSONAL" y "SOCIEDAD DE HECHO". El campo lleva '*' en pantalla, pero ni 'Siguiente' ni 'Aceptar' lo validan. El mismo atributo `PrvCla` se pide en el paso 3 como "Clase de Persona Jurídica". Clase por defecto. [V · capas: código, diseño · ev: hprvir17m_impl.java e1925K2 (Start) y e1225K2 ('Siguiente'); XPZ HPrvIR17m Events Start · clase: esencial]
- **R-191** Todo el bloque de validación y grabación (R-180 a R-187) está escrito dos veces, idéntico, en 'Siguiente' (módulo `I`) y en 'Aceptar' (otros módulos). Solo cambia el destino: 'Siguiente' abre el paso 5 y 'Aceptar' vuelve al llamador. La rev2 lo cita como "85-96 y repetido en 130-141". [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente') y e1525K2 ('Aceptar'); XPZ HPrvIR17m Events 'Siguiente' y 'Aceptar'; rev2 §6 · clase: accidente]
- **R-192** "Anterior" vuelve al paso 3 (`TPrvInsRP`) en modo `UPD`, tomando de la sesión el CUIT y la clave `Prove` que dejaron los pasos anteriores y la categoría de `PPrvIR62`. [V · capas: código, diseño · ev: hprvir17m_impl.java e1325K2 ('Anterior'); XPZ HPrvIR17m Events 'Anterior'; rev2 §6 · clase: esencial]
- **R-193** En la rutina 'perfilMenu', la llamada a `HPrvIR21` (Administración) está comentada en el XPZ y solo queda el `Return`. [S · capas: diseño · ev: XPZ HPrvIR17m Events Sub 'perfilMenu' (línea comentada) · clase: accidente]
- **R-194** La rutina 'perfilMenu' devuelve los parámetros al llamador con `Return`. Es el único destino real de 'Volver' y de 'Aceptar'. [V · capas: código, diseño · ev: hprvir17m_impl.java S112 ('PERFILMENU'); XPZ HPrvIR17m Events Sub 'perfilMenu' · clase: esencial]

## Condición de avance

- Pasa al paso 5 (`HPrvIR41`) desde 'Siguiente' cuando pasan R-180 a R-186 y la grabación de `PPrvIR21m` devuelve '1'. [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); XPZ HPrvIR17m Events 'Siguiente'; rev2 §6]
- En los módulos distintos de `I`, 'Aceptar' hace las mismas comprobaciones y vuelve al llamador. [V · capas: código, diseño · ev: hprvir17m_impl.java e1525K2 ('Aceptar'); XPZ HPrvIR17m Events 'Aceptar']
- Se queda en el paso 4 con un mensaje cuando falla cualquiera de las anteriores. [V · capas: código, diseño · ev: hprvir17m_impl.java e1225K2 ('Siguiente'); XPZ HPrvIR17m Events 'Siguiente']

## Capas

Capas: diseño (XPZ y rev2 §6), código (Java generado, más `PPrvIR13`, `PPrvIR26` y `PPrvIR21m` leídos para fijar su efecto); ejecución: todavía no observado (E4). Los manuales (intención) no se consultaron para este paso.

La rev2 tomó este paso solo del XPZ, porque no importó a la KB. El Java generado coincide con el XPZ en cada evento. La rev2 omite la lista de Tipo de Asociación (R-190), el guardado previo a la comprobación de integrantes (R-187) y la grabación sin validar de 'Agregar' (R-188).
