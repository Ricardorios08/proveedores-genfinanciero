# Paso 11: confirmación (HPrvIR09)

## Objeto

`HPrvIR09` es la pantalla "Confirmar Datos", rotulada "PASO 11 de 11" y titulada "Confirmación de Datos". Cierra el alta: permite ver de nuevo la solicitud, descargar el formulario de inscripción si está habilitado, y confirmar. Al confirmar envía un mensaje al proveedor, deja el trámite "En espera" y muestra una pantalla final de agradecimiento.

Recibe un único parámetro, el usuario del proveedor. No recibe el modo: lo fija en `I` al arrancar. Hacia atrás vuelve a `HPrvIR10`. Los objetos que ejecutan el envío (`PPrvSendMsg`) y el cambio de estado (`PPrvIR16b`) se llaman desde acá, pero sus cuerpos son de otros pasos de análisis.

Fuentes: rev2 §13, §15 y §17, XPZ `HPrvIR09`, Java `hprvir09_impl.java`.

## Datos que pide

Este paso no pide ningún dato. Lee el nombre auxiliar del proveedor para armar el mensaje (R-354) y solo ofrece botones y enlaces.

## Validaciones

- **R-350** El bloque del formulario de inscripción ("Le informamos que debe descargar el Formulario de Inscripción", con la indicación de adjuntarlo en la opción de documentación del proveedor) solo se muestra si el atributo de sistema COMPRAS_HABFORMULARIO vale 'S'. El comentario del código dice que, por ahora, es solo para un cliente (MGU), lo que lo hace un parche. [V · capas: código, diseño · ev: hprvir09_impl.java e11AI2 (Start); XPZ HPrvIR09 Events Start · clase: parche]
- **R-351** El enlace del formulario abre el reporte `RPrvIR11` en ventana emergente con el usuario. [V · capas: código, diseño · ev: hprvir09_impl.java e15AI2 ('Formulario'); XPZ HPrvIR09 Events 'Formulario' · clase: esencial]
- **R-352** El enlace "aquí" para ver de nuevo los datos abre el reporte `RPrvIR14` con el usuario y el parámetro 'S'. El paso 10 imprime la misma solicitud con `RPrvIR14m`: hay dos variantes del reporte y esta evidencia no dice cuál prevalece. Clase por defecto. [V · capas: código, diseño · ev: hprvir09_impl.java e12AI2 ('Solicitud'); XPZ HPrvIR09 Events 'Solicitud' · clase: esencial]
- **R-353** El arranque fija el modo en `I` sin importar cómo se llegó. Es coherente con que el paso 10 solo permite avanzar en modo `I` (R-320), y hace que 'Anterior' vuelva siempre al paso 10 en modo `I`. Clase por defecto. [V · capas: código, diseño · ev: hprvir09_impl.java e11AI2 (Start); XPZ HPrvIR09 Events Start · clase: esencial]
- **R-354** Al arrancar se lee del registro del proveedor su nombre auxiliar, que se usa más tarde como parámetro del mensaje. [V · capas: código, diseño · ev: hprvir09_impl.java e11AI2 (Start); XPZ HPrvIR09 Events Start · clase: esencial]
- **R-355** 'Confirmar' arma y envía un mensaje con el proveedor, un canal (el código de sistema que lee de la tabla de sistemas, o el canal por defecto de la configuración del módulo si no hay), un remitente de la configuración, el asunto fijo "Alta Proveedor del Estado" y dos parámetros (usuario y nombre, cuyas claves también vienen de la configuración). Los nombres de las claves de configuración son `CanalRegistro`, `ServicesUsuarioGestion`, `ParamUsuario` y `ParamNombre`; el Java trae sus valores ya incrustados desde el dominio `ParmModPrv`, y acá no se transcriben. [V · capas: código, diseño · ev: hprvir09_impl.java e13AI2 ('Confirmar'); XPZ HPrvIR09 Events 'Confirmar'; gxdomainparmmodprv.java · clase: esencial]
- **R-356** Después del envío, 'Confirmar' deja el trámite "En espera" llamando a `PPrvIR16b` con el estado 'E', sin condicionarlo al resultado del envío: la condición escrita es "el estado es 'S' o verdadero", y siempre se cumple. La rev2 §13 lo describe como condicionado al éxito del envío; ver D-301. [V · capas: código, diseño · ev: hprvir09_impl.java e13AI2 ('Confirmar'); XPZ HPrvIR09 Events 'Confirmar' · clase: esencial]
- **R-357** La rama de error de 'Confirmar' ("Ocurrió un error al procesar sus datos:" y la lista de mensajes del envío) es inalcanzable, por la misma condición siempre verdadera de R-356. Si el envío falla, el proveedor igual ve la pantalla de éxito y queda "En espera" sin haber recibido el mensaje. [V · capas: código, diseño · ev: hprvir09_impl.java e13AI2 ('Confirmar'); XPZ HPrvIR09 Events 'Confirmar' · clase: accidente]
- **R-358** Tras confirmar, la pantalla muestra "¡Muchas gracias por registrarse!", un recordatorio del nombre de usuario y el aviso de que la contraseña para acceder al sistema se enviará por correo electrónico; oculta el formulario, el rótulo del paso, la leyenda y los botones. Clase por defecto. [V · capas: código, diseño · ev: hprvir09_impl.java e13AI2 ('Confirmar'); XPZ HPrvIR09 Events 'Confirmar' · clase: esencial]
- **R-359** El texto "Luego de confirmar su información, se le enviará por correo electrónico el resto de la documentación que debe presentar personalmente en nuestras oficinas" se asigna en el arranque y se deja con visibilidad apagada: nunca se muestra. La rev2 §13 lo cita como comportamiento del paso. [D · capas: código, diseño, intención · ev: hprvir09_impl.java e11AI2 (Start); XPZ HPrvIR09 Events Start; manual Registro p. 25 · clase: accidente · ≠ D-06]
- **R-360** En 'Confirmar' hay una línea comentada que asignaba un segundo mensaje final (sobre los instructivos de la página web), y en su lugar el mensaje 2 queda con texto vacío. [D · capas: diseño, intención · ev: XPZ HPrvIR09 Events 'Confirmar' (línea comentada); manual Registro p. 25 · clase: accidente · ≠ D-06]
- **R-361** 'Anterior' vuelve a `HPrvIR10` con el usuario y el modo. [V · capas: código, diseño · ev: hprvir09_impl.java e14AI2 ('Anterior'); XPZ HPrvIR09 Events 'Anterior' · clase: esencial]

## Condición de avance

Es el último paso: no hay siguiente. El alta queda cerrada cuando 'Confirmar' llega a mostrar la pantalla final, y eso ocurre siempre (R-356, R-357): ni el envío del mensaje ni el cambio de estado pueden impedirlo desde esta pantalla. El resultado real del envío no se verifica acá.

## Capas

Capas: diseño (XPZ `HPrvIR09` y rev2 §13, §15 y §17) y código (Java `hprvir09_impl.java` y `gxdomainparmmodprv.java`). La ejecución todavía no se observó: ejecución: todavía no observado (E4). La intención (manuales) no se consultó para este paso.

R-360 queda en S porque la línea comentada solo existe en el XPZ; el Java generado no conserva los comentarios del fuente. Los cuerpos de `PPrvSendMsg` y `PPrvIR16b` se resuelven en otros archivos de análisis.
