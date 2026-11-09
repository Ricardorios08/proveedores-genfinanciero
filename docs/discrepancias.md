# Discrepancias entre capas

Una entrada `D-nn` por cada contradicción entre dos capas (CA14), con la fuente y la capa de cada lado. Una afirmación en discrepancia lleva la marca `≠ D-nn` y queda en estado **D**. Qué vale lo decide el responsable en `decisiones-rediseno.md`.

Las discrepancias conocidas de la propuesta (paso 2: largo del usuario; paso 9: cuenta bancaria según configuración; paso 1: el manual no menciona "Agente del Estado") se **revalidan** antes de cargarse (tarea H1). La del paso 6 se retiró en la enmienda 1: no es una discrepancia.

Resultado de la revalidación (H1, 2026-10-24), contra el manual de registro (`contexto/Manual Registro de Proveedores Portal.pdf`, 28 páginas) y contra el código:

- Paso 1, "Agente del Estado": **se sostiene y es más ancha** de lo anotado. El manual no menciona el caso, y además dice que todo CUIT encontrado y no habilitado pasa al paso 2. Es D-01.
- Paso 9, cuenta bancaria: **se sostiene con un matiz**. Es D-05.
- Paso 2, largo del usuario: **no se sostiene como discrepancia entre capas**. No se carga. El texto del manual (p. 8) dice "al menos 5" y la captura "entre 5 y 20"; el código exige al menos 5 (R-123) y el campo admite 20 (R-124). Lo que queda es el 30 del dominio `ACPSUsuario` (`modelo-datos.md`): es una capacidad del modelo de datos, no algo que el usuario crea distinto de lo que pasa. Es una pregunta para `decisiones-rediseno.md` (20 o 30), no una discrepancia.

Las demás entradas (D-02, D-03, D-04 y D-06) salieron de recorrer el manual paso por paso contra `docs/pasos/`.

## Discrepancias entre capas

En todas, un lado es la capa `intención` (manual de registro) y el otro la capa `código`. Las páginas son las del PDF. Una captura del manual vale como intención: muestra lo que el usuario ve y cree. En ningún caso la ejecución en test está observada todavía (E4), así que el lado código no tiene la capa `ejecución`.

### D-01 — Paso 1: el manual manda al paso 2 a todo CUIT existente no habilitado; el código corta con un error en dos casos

- **Lado intención** (capa `intención`, manual Registro p. 5): si el sistema encuentra el CUIT, muestra el estado de habilitación, y solo cuando el proveedor ya está habilitado avisa que puede ingresar; "para los demás casos pasa al Paso 2". El manual no menciona el caso "Agente del Estado" ni el de modificación en espera. La p. 7 describe el CUIT ya registrado con la habilitación en proceso, que coincide con el salto al paso 10 (R-109) y por eso no se marca.
- **Lado código** (capas `código`, `diseño`): `hprvir02_impl.java` e125A2 ('Siguiente'), con el mismo comportamiento en `XPZ HPrvIR02 Events 'Siguiente'`. El flag `G` (Agente del Estado) corta con "ERROR: El proveedor es Agente del Estado. No puede darse de Alta." (R-108). El flag `Q` (espera de habilitación de modificación de datos) corta con un error (R-107). Ninguno de los dos llega al paso 2.
- **Qué cree el usuario y qué pasa de verdad:** quien lee el manual espera seguir al paso 2 con cualquier CUIT que ya exista y no esté habilitado. Un Agente del Estado, o un proveedor con una modificación pendiente, se queda en el paso 1 con un error que el manual no anticipa. Los flags `X` y "cualquier otro" (R-112, R-114) no se marcan: el manual no dice que el CUIT exista en esos casos.

Decide el responsable en decisiones-rediseno.md.

### D-02 — Paso 2: el manual dice que el sistema genera el usuario; el código lo propone, se puede cambiar y lo rellena con ceros

- **Lado intención** (capa `intención`, manual Registro p. 8): si el CUIT es un proveedor del GEN que todavía no tiene usuario en el Portal, "el sistema genera un nombre de usuario con la letra P seguida del número de proveedor". Si no lo encuentra, el proveedor lo carga.
- **Lado código** (capa `código`): `hprvir07_impl.java` e11A22 (Start) llama a `PPrvIR03` (`apprvir03.java`, `privateExecute`), que arma "P" más el número de proveedor y, si el número tiene menos de 4 dígitos, le **agrega ceros a la derecha** hasta 5 caracteres (un número de 1 dígito da "P" + número + "000"). Después muestra la tabla de elección con el campo **habilitado** y `Valida` en 1 (R-120): es una propuesta que el proveedor puede cambiar, sujeta a R-123 a R-127.
- **Qué cree el usuario y qué pasa de verdad:** el manual describe un usuario asignado por el sistema y con una forma predecible (P seguida del número). En el código es un valor sugerido y editable, y los ceros se agregan al final, no entre la P y el número.

Decide el responsable en decisiones-rediseno.md.

### D-03 — Paso 5: el manual exige domicilio real y legal; el código exige solo el legal

- **Lado intención** (capa `intención`, manual Registro p. 14): "el portal valida que haya ingresado domicilio Real y domicilio Legal". La captura de esa misma página dice "Es OBLIGATORIO el ingreso de un domicilio LEGAL", así que el manual se contradice a sí mismo.
- **Lado código** (capas `código`, `diseño`): `hprvir41_impl.java` e121G42 ('Siguiente'). Avanza si hay legal solo o legal y real (flags `L` y `A`); un domicilio real sin legal da el error (R-201). El domicilio real nunca es obligatorio. La comprobación de la combinación real y legal está comentada en el XPZ (R-206).
- **Qué cree el usuario y qué pasa de verdad:** según el texto del manual, el proveedor cree que debe cargar los dos. En el código puede avanzar sin domicilio real. La parte del manual sobre "no más de un real ni más de un legal" sí coincide con el código (`tprvdom_impl.java`, mensajes "Ya posee un domicilio Legal" y "Ya posee un domicilio Real").

Decide el responsable en decisiones-rediseno.md.

### D-04 — Paso 6: el manual dice que el último ejercicio se ingresa obligatoriamente; el código no exige nada

- **Lado intención** (capa `intención`, manual Registro p. 15): "el usuario debe ingresar obligatoriamente los datos del último ejercicio", y "el sistema valida que la fecha de cierre del ejercicio concuerde con el día/mes definido en el Paso 4". El encabezado de la misma página (y el índice, p. 2) dice "Dato No Obligatorio", así que el manual también se contradice a sí mismo.
- **Lado código** (capas `código`, `diseño`): `hprvir18_impl.java` e15AC2 ('Siguiente') avanza siempre a `HPrvIR42` (R-213). Las validaciones que exigían el último ejercicio están comentadas (R-214, R-215). En `tprvesp_impl.java` (`checkExtendedTableC9391`) la única validación del ejercicio es que estén los campos marcados con '*'; no se encontró ninguna que compare el día y el mes de cierre con otro dato, y el paso 4 no pide un día de cierre.
- **Qué cree el usuario y qué pasa de verdad:** el texto del cuerpo del manual dice que cargar el ejercicio es obligatorio y que el sistema valida la fecha; el código deja atravesar el paso vacío y no valida esa fecha.
- **Nota:** no es la discrepancia del paso 6 retirada en la enmienda 1. Aquella comparaba el título "Dato No Obligatorio" con el código y el título coincidía. Esta compara el **cuerpo del manual**, que no se había consultado, con el código.

Decide el responsable en decisiones-rediseno.md.

### D-05 — Paso 9: el manual presenta la cuenta bancaria como opcional; el código la hace obligatoria según un atributo de sistema

- **Lado intención** (capa `intención`, manual Registro p. 20): el paso dice que "puede registrar" las cuentas y, si no, "presione en Siguiente para continuar". Ninguna página dice que la cuenta pueda ser obligatoria ni que dependa de la configuración.
- **Lado código** (capas `código`, `diseño`): `hprvir22_impl.java` e1225M2 ('Siguiente'). Con COMPRAS_OBLIGACTABCO en 'S' y sin ninguna cuenta en la grilla no avanza y muestra "ERROR: Es OBLIGATORIO ingresar al menos una Cuenta Bancaria." (R-302). El texto de ayuda cambia con el mismo atributo (R-304).
- **Qué cree el usuario y qué pasa de verdad:** la captura del manual muestra el texto de la rama sin obligatoriedad, que es coherente con el código para un atributo distinto de 'S'. El matiz: el manual no dice que existe la otra rama, así que en una instalación con 'S' el proveedor que lo siga se encuentra con un error que el manual no menciona. Cuál es el valor en cada instalación no está en las fuentes (los valores de atributos de sistema no se transcriben).

Decide el responsable en decisiones-rediseno.md.

### D-06 — Pasos 4, 9 y 11: el manual muestra leyendas sobre la documentación a presentar que el código oculta o no escribe

- **Lado intención** (capa `intención`, manual Registro p. 12, p. 20 y p. 25): las capturas muestran, visible, la leyenda "La documentación respaldatoria de la información consignada en esta pantalla debe ser presentada en nuestras oficinas" en los pasos 4 y 9 (y en el 6, p. 15). La p. 25 muestra en el paso 11 la frase "Luego de confirmar su información, se le enviará por correo electrónico el resto de la documentación que debe presentar personalmente en nuestras oficinas", y en la pantalla final un párrafo que remite a los instructivos de la página web.
- **Lado código** (capas `código`, `diseño`): los paneles asignan el texto en Start y lo dejan con visibilidad apagada, y ningún evento lo enciende: `hprvir17m_impl.java` e1925K2 (Start), `hprvir22_impl.java` e1525M2 (Start) (R-309), `hprvir09_impl.java` e11AI2 (Start) (R-359). El párrafo final sobre los instructivos solo existe como línea comentada en el XPZ (R-360).
- **Qué cree el usuario y qué pasa de verdad:** el manual le dice que la pantalla le avisa qué documentación llevar a las oficinas y que se la mandan por correo. En el código esos avisos nunca se muestran. Es posible que el manual describa una versión anterior de las pantallas: eso no está observado, y la ejecución en test lo resolverá (E4). El paso 6 muestra lo mismo en el manual y en el código (`hprvir18_impl.java`, texto oculto), pero `pasos/paso-06.md` no tiene una afirmación sobre ese texto, así que no lleva marca.

Decide el responsable en decisiones-rediseno.md.

## Ids retirados: no eran discrepancias del sistema

Durante C y D (2026-10-23) los ejecutores marcaron doce afirmaciones con un `≠ D-nn`. Revisadas por el coordinador, **ninguna es una contradicción entre capas**: en todas, el XPZ y el Java coinciden. Las marcas se sacaron y los ids quedan retirados (no se reutilizan). Se agrupan en tres tipos.

**Errores de lectura de la rev2.** La rev2 es la capa `diseño`, igual que el XPZ. Si el XPZ y el Java coinciden en algo distinto, la que se equivoca es la rev2, no el sistema:
- D-110 (paso 2): la rev2 explica el modo `UPD` como "el perfil ya existía"; en el Java, `PPrvIR09` devuelve `P` después de **crear** el perfil a partir de PROVE.
- D-111 (paso 2): la rev2 dice que el paso pide una contraseña; el panel no tiene ningún campo de contraseña.
- D-301 (paso 11): la rev2 dice que el trámite pasa a "En espera" solo si el mensaje salió bien; el código tiene `|| true` y el cambio es incondicional.
- D-302 (paso 9): la rev2 dice que los textos "se invierten" según el modo; hay dos juegos de textos, uno por modo.
- D-303 (paso 10): la rev2 dice que el paso 10 avanza a `HPrvIR22`; esa es la vuelta atrás, y el avance es a `HPrvIR09`.

**Accidentes dentro del mismo código.** Un texto o una marca de pantalla que no corresponde a la regla, en el mismo objeto. Se tratan como reglas de clase accidente, no como discrepancias:
- D-112 (paso 2): el texto que pide elegir categoría está en el formulario, oculto, y la categoría queda fija en '1'.
- D-120 (paso 3): el asterisco de obligatorio junto a Ingresos Brutos, cuando la regla lo exige solo para la categoría '1' (que hoy es siempre).

**Comentarios desactualizados en el código.** El comentario de `HPrvIR02` que enumera los flags no coincide con lo que hacen el XPZ y el Java:
- D-401 (estados): el flag `G` se usa pero el comentario no lo nombra.
- D-402 (estados): el comentario define `P`, `A` y `T` de una forma que ningún código cumple.

**Contradicción interna sin resolver:**
- D-121 (paso 3): en el modo `A`, las reglas declaran el CUIT como no editable y el Start lo habilita. Queda anotada en `pasos/paso-03.md` como pendiente de observar en test (E5). Además corrige a la rev2, que dice que el CUIT se bloquea siempre.

**Lección.** Es la misma forma que la "discrepancia" del paso 6 retirada en la enmienda 1: una afirmación de la rev2 contra el código parece un cruce entre capas, pero el XPZ, que es la misma capa que la rev2, dice lo mismo que el código.
