# docs/ — Registro de Proveedores de GEN Financiero

Ingeniería inversa del módulo Registro de Proveedores (GeneXus 18), hecha para **decidir su rediseño** sin estudiar el sistema original. Unidad de trabajo: `trabajo/en-curso/registro-proveedores-docs/`.

## Leer primero

- [mapa-flujos.md](mapa-flujos.md): el flujo completo de un vistazo, con los puntos de dolor marcados.
- [decisiones-rediseno.md](decisiones-rediseno.md): qué mantener, qué rediseñar y qué eliminar, con recomendación.

## Respaldo

- [convenciones.md](convenciones.md): capas, estados (V, S, D), formato de afirmaciones y reglas, ids, citas y chequeo de versión.

**Los 11 pasos del alta (modo I):**

- [pasos/paso-01.md](pasos/paso-01.md): `HPrvIR02`, entrada por CUIT y estado del proveedor.
- [pasos/paso-02.md](pasos/paso-02.md): `HPrvIr07`, nombre de usuario y categoría.
- [pasos/paso-03.md](pasos/paso-03.md): `TPrvInsRP`, datos principales del proveedor.
- [pasos/paso-04.md](pasos/paso-04.md): `HPrvIR17m`, persona jurídica e integrantes.
- [pasos/paso-05.md](pasos/paso-05.md): `HPrvIR41`, domicilios.
- [pasos/paso-06.md](pasos/paso-06.md): `HPrvIR18`, estado de situación patrimonial.
- [pasos/paso-07.md](pasos/paso-07.md): `HPrvIR42`, rubros.
- [pasos/paso-08.md](pasos/paso-08.md): `HPrvIR06`, representantes.
- [pasos/paso-09.md](pasos/paso-09.md): `HPrvIR22`, cuentas bancarias.
- [pasos/paso-10.md](pasos/paso-10.md): `HPrvIR10`, impresión de la solicitud.
- [pasos/paso-11.md](pasos/paso-11.md): `HPrvIR09`, confirmación.

**Transversales:**

- [modos.md](modos.md): qué cambia en los modos `P` (el proveedor modifica sus datos) y `A` (administración) respecto del alta, panel por panel.
- [modelo-datos.md](modelo-datos.md): entidades, tablas, claves, atributos y tipos.
- [estados.md](estados.md): estados del proveedor como transiciones (flag de `PPrvIR02` y `PrvPHabCS`), y quién habilita.
- [integraciones.md](integraciones.md): puntos de contacto con GEN y con ACPS Services, y entradas externas.
- [mensajes.md](mensajes.md): cada correo y mensaje que envía el módulo, con su evento, canal, destinatario y asunto.
- [configuracion.md](configuracion.md): atributos de sistema y parámetros de `ParmModPrv` que lee el módulo, y su efecto (sin valores).
- [cliente-vs-producto.md](cliente-vs-producto.md): qué reglas son de un cliente (OSEP) y cuáles del producto.
- [seguridad.md](seguridad.md): hallazgos de seguridad, documentados como son y no como requisitos.

**Inventarios:**

- [inventario-objetos.md](inventario-objetos.md): los 119 objetos del export, con tipo y fecha de versión.
- [dependencias-faltantes.md](dependencias-faltantes.md): lo que el export llama y no trae, activo y comentado, con su fuente en `fin/`.
- [universo-modulo.md](universo-modulo.md): hasta dónde llega el módulo en el Java (dentro, contacto, externas y borde).
- [pantallas.md](pantallas.md): inventario de pantallas `Snn`.
- [flujos.md](flujos.md): inventario de flujos `Fnn`, incluidas las retomas por estado.
- [discrepancias.md](discrepancias.md): contradicciones entre capas `D-nn`.
- [features.csv](features.csv): matriz de funcionalidades, con la decisión tomada sobre cada una.

## Herramientas

- [herramientas/contar-xpz.py](herramientas/contar-xpz.py): conteo de objetos y atributos del export.
- [herramientas/dependencias-xpz.py](herramientas/dependencias-xpz.py): objetos llamados que no vienen en el export, activos y comentados.
- [herramientas/verificar.py](herramientas/verificar.py): los seis chequeos de `docs/`.
- [herramientas/universo-fin.py](herramientas/universo-fin.py): frontera del módulo dentro del Java generado.
- [herramientas/probar.py](herramientas/probar.py): prueba que cada control de las herramientas pueda fallar.

Las entradas sintéticas de las pruebas están en `herramientas/fixtures/`, que no forma parte del índice.
