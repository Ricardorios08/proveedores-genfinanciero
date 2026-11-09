# Modelo de datos

Entidades del Registro de Proveedores de GEN Financiero: tabla, clave, atributos y tipo de cada uno. Respalda a `decisiones-rediseno.md` y se lee junto con `estados.md`, que describe cómo cambia `PrvPHabCS`.

## Cómo leerlo

Cada entidad tiene una línea con su tabla y su clave, seguida de la tabla de atributos. La tabla y la clave de las entidades hijas salen del `DELETE ... WHERE` del `_impl.java` de su transacción: el export del XPZ trae una sola transacción (`TPrvInsRP`) y no trae ninguna de las hijas. El nombre que se cita junto al archivo es el del cursor SQL dentro de la clase `<objeto>__default`.

El tipo sale de dos fuentes. Del XML (capa `diseño`): `Length`, `Decimals` y `ATTCUSTOMTYPE` del atributo en `<Attributes>`. Del Java (capa `código`): el método con que se lee la columna en un `SELECT` (`getString(n, largo)`, `getByte`, `getInt`...). Un `getByte`, `getShort`, `getInt` o `getLong` dice cuántos dígitos caben, no cuántos tiene el atributo: se escribe como rango (por ejemplo, `Numeric (5-9 dígitos)`), salvo que el XML dé el largo exacto. Los dominios (`Domain:...`) no están en el export, así que la columna Dominio da solo el nombre y el tipo viene del Java.

La columna del bloque dice de dónde sale cada fila. Se cruzaron el tipo del XML y el del Java en todos los atributos que tienen ambos y no son de dominio, y no hay ninguna contradicción de tipo ni de largo, por eso no hay marcas `≠ D-nn` de tipos. Las 11 filas en estado S son atributos del XML que no son columna en ningún `INSERT` del Java y no traen tipo en el XML.

Las fechas de generación del Java van del 2025-09-23 al 2026-09-01 según el objeto (`tprvinsrp_impl.java` es del 2026-06-25, `tprvbco_impl.java` del 2026-04-13, `tprvpj_impl.java` del 2026-02-04). No se comparó cada objeto con el XPZ salvo `TPrvInsRP`; el chequeo de versión está en `convenciones.md`.

## PrvPerfil

- Tabla `PrvPerfil`, clave `PrvPUSr`. Transacción dueña: `TPrvInsRP` (Inscripción al Registro de Proveedores), la única del export. [V · capas: código, diseño · ev: tprvinsrp_impl.java cursor T00IZ20 (DELETE FROM PrvPerfil WHERE PrvPUSr); XPZ PrvPerfil Table Key; XPZ TPrvInsRP Structure (PrvPUSr con key True)]
- Índices del XPZ: `PrvPe1` único sobre `PrvPUSr`; duplicables `PrvPe2` (`PrvPNro`), `PrvPe4` (`PrvIgnTi`, `PrvIgnNr`, `PrvIgnDi`, el CUIT), `PrvPe5` (`PrvZonCod`), `PrvPe6` (`PrvFchVtoCer`), `PrvPe7` (`PrvPHabCS`, `PrvNomAux`) e `IPrvPerfil` (`PrvSocPaisCgo`, `PrvSocPciaCgo`, `PrvSocLocCgo`). Solo `PrvPe1` es único: nada en el índice impide dos perfiles con el mismo CUIT. [S · capas: diseño · ev: XPZ PrvPerfil Table Indexes]
- **R-401** Un perfil por usuario: `PrvPUSr` es la clave de `PrvPerfil` y el índice `PrvPe1` es único sobre ese atributo. [V · capas: código, diseño · ev: tprvinsrp_impl.java cursor T00IZ20; XPZ PrvPerfil Table Indexes (PrvPe1 Unique) · clase: esencial]
- **R-405** `PrvPerfil` no guarda solo proveedores: `PCADM001` (carga de usuarios, `HCADM002`) inserta en ella usuarios con `PrvPClaseUsr` en `I` (el significado de ese valor no está documentado en las fuentes), `PrvPHabCS` vacío y los datos del proveedor en blanco. [V · capas: código · ev: pcadm001.java privateExecute (asigna A5920PrvPClaseUsr con I) y cursor P015D3 (INSERT INTO PrvPerfil); hcadm002_impl.java llama a PCADM001 · clase: esencial]


| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ15; XPZ Attributes PrvPUSr] |
| `PrvCat` (Categoría de Proveedor) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvCat] |
| `PrvNomAux` (Nombre Proveedor) | Character(59) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvNomAux] |
| `PrvIgnDi` (I. Gan. Dígito verificador) | Numeric(1,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIgnDi] |
| `PrvIgnNr` (Nro) | Numeric(8,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIgnNr] |
| `PrvIgnTi` (Cuit o tipo) | Numeric(2,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIgnTi] |
| `PrvPCUIT` (CUIT) | Character(13) | DmnCuit | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvPCUIT] |
| `PrvPHabCS` (Habilitación módulo Compras y Suministros) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvPHabCS] |
| `PrvFchHabCS` (Fecha de habilitación) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchHabCS] |
| `PrvFchVtoCer` (Fecha Vto del certificado de habilitación) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchVtoCer] |
| `PrvPHabTGP` (Habilitación módulo TGP) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvPHabTGP] |
| `PrvIgnCa` (I. Gan. caracter) | Numeric(1,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIgnCa] |
| `PrvIVA` (Inscripto en IVA) | Numeric (1-2 dígitos) | GENIVASituacion | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIVA] |
| `PrvIib3` (Inscripción en Ingresos Brutos) | Numeric(3,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIib3] |
| `PrvIibNr` (Nro de IB) | Numeric(11,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIibNr] |
| `PrvIibDi` (Dígito verificador) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIibDi] |
| `PrvIibCa` (IB caracter) | Numeric(1,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIibCa] |
| `PrvObs` (Tipo de Persona) | Numeric (1-2 dígitos) | GenProveTipoPersona | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvObs] |
| `PrvCla` (Clase de proveedor) | Numeric(2,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvCla] |
| `PrvCerIE` (Nro de certificado de Importador/Exportador) | Character(15) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvCerIE] |
| `PrvMail` (Mail del proveedor) | Character(60) | CoMail | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvMail] |
| `PrvTel` (Teléfono) | Character(15) | CoTelefono | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvTel] |
| `PrvRprUltNroLin` (Ultimo nro de línea del representante) | Numeric(5,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvRprUltNroLin] |
| `PrvPodUltNroLin` (Ult. Nro linea Apoderado) | Numeric(5,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvPodUltNroLin] |
| `PrvBcoUltNroLin` (Ult. Nro Linea Cuenta Bancaria) | Numeric(5,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvBcoUltNroLin] |
| `PrvDomUltNroOrden` (Ultimo Nro de orden del domicilio) | Numeric(1,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvDomUltNroOrden] |
| `PrvFchPagVi` (Fecha de último pago vigente o la exención) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchPagVi] |
| `PRvPPass` (Contraseña) | Character(150) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PRvPPass] |
| `PrvFchCieBal` (Fecha cierre de Balance) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchCieBal] |
| `PrvFchCirBalAct` (Fecha cierre balance actual) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchCirBalAct] |
| `PrvFchDurRep` (Fecha fin representación de cargos) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchDurRep] |
| `PrvFchDisCar` (Acta de Directorio - Fch Distribución de Cargos) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchDisCar] |
| `PrvFchAprBal` (Acta de asamblea - Fch Aprobación balance) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchAprBal] |
| `PrvNroActAprBal` (Nro Acta aprobación Balance) | Numeric(6,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvNroActAprBal] |
| `PrvNroActDisCar` (Nro Acta Distribución de cargos) | Numeric(6,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvNroActDisCar] |
| `PrvDurSoc` (Duración de la sociedad en años) | Numeric(2,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvDurSoc] |
| `PrvRepLegForma` (Forma de representación legal) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvRepLegForma] |
| `PrvPJUltNro` (Ultimo nro de integrante) | Numeric(2,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvPJUltNro] |
| `PrvSexo` (Sexo Persona Física) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvSexo] |
| `PrvCerHTipNor` (Tipo Norma Legal) | Numeric (1-2 dígitos) | GSNorTip | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvCerHTipNor] |
| `PrvCerHNroNor` (Nro Norma Legal) | Numeric(5,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvCerHNroNor] |
| `PrvCerHLetNor` (Letra Norma Legal) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvCerHLetNor] |
| `PrvCerHAANor` (Año Norma Legal) | Numeric (3-4 dígitos) | CoAANor | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvCerHAANor] |
| `PrvEsEmpleador` (Es Empleador SUSS) | Numeric(1,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvEsEmpleador] |
| `PrvIniSoc` (Fecha de inicio de la sociedad) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvIniSoc] |
| `PrvNroInscSoc` (Nº de inscripción en el registro de sociedades) | Character(20) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvNroInscSoc] |
| `PrvDurManDir` (Duración mandato de directores) | Numeric(2,0) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvDurManDir] |
| `PrvFchConSoc` (Fecha de Constitución) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchConSoc] |
| `PrvUTE` (Es una UTE?) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvUTE] |
| `PrvFchInscSoc` (Fecha de Inscripción) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvFchInscSoc] |
| `PrvSocOtros` (Otros Datos) | LongVarChar | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvSocOtros] |
| `PrvPAdminEqu` (Es Admin Equivalencias) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvPAdminEqu; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPConsulta` (Usuario Consulta) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvPConsulta; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvZonCod` (Código de Zona) | Numeric (3-4 dígitos) | CoPrvZona | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvZonCod] |
| `PrvPNro` (Nº de proveedor) | Numeric (5-9 dígitos) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvPNro] |
| `PrvSocPaisCgo` (Código de Pais) | Numeric (3-4 dígitos) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvSocPaisCgo] |
| `PrvSocPciaCgo` (Código Provincia) | Numeric (1-2 dígitos) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvSocPciaCgo] |
| `PrvSocLocCgo` (Código Localidad) | Numeric (5-9 dígitos) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, tprvinsrp_impl.java cursor T00IZ2; XPZ Attributes PrvSocLocCgo] |
| `PrvPMail` (Mail) | Character(60) | CoMail | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, apprvp003.java cursor P012C3; XPZ Attributes PrvPMail; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPRstClave` (Resetear clave?) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y apprvp007.java cursor P011L3; XPZ Attributes PrvPRstClave; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPPagRec` (Recibe noticias de pagos?) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y apprvp003.java cursor P012C3; XPZ Attributes PrvPPagRec; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPGtFch` (Fecha de garantia uniificada) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y hcgtu001_impl.java cursor H00B22; XPZ Attributes PrvPGtFch; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPGtMnt` (Importe de la Garantia) | Numeric (2 decimales) | GenImporte | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, hcgtu001_impl.java cursor H00B22; XPZ Attributes PrvPGtMnt; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPGtEst` (Estado garantía uniifcada) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y hcgtu001_impl.java cursor H00B23; XPZ Attributes PrvPGtEst; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPPCGAcepta` (Aceptó pliego de condiciones generales) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y pcof0007.java cursor P016B2; XPZ Attributes PrvPPCGAcepta; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPPCGNro` (Nº de pliego aceptado) | Numeric (5-9 dígitos) | CpPliegoNro | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, pcof0007.java cursor P016B2; XPZ Attributes PrvPPCGNro; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPPCGFchAcepta` (Fecha de aceptación del PCG) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y cm0137.java cursor P04YL2; XPZ Attributes PrvPPCGFchAcepta; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPClaseUsr` (Clase Usuario) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y hcadm002_impl.java cursor H00BC3; XPZ Attributes PrvPClaseUsr; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPAdminGral` (Es Admin General) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y hcadm002_impl.java cursor H00BC2; XPZ Attributes PrvPAdminGral; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPAdminCat` (Es Admin Catálogo) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y hcadm002_impl.java cursor H00BC2; XPZ Attributes PrvPAdminCat; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPHabCat` (Habilitado para Catálogo) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y hcadm002_impl.java cursor H00BC2; XPZ Attributes PrvPHabCat; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPliegos` (Compra Pliegos) | Character(1) | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo XML, sin lector Java; XPZ Attributes PrvPliegos; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPFchInh` (Fecha de Inhabilitación) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y pprvir34.java cursor P01322; XPZ Attributes PrvPFchInh; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPHorInh` (Hora de Inhabilitación) | Character(8) | CoHora | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, pprvir34.java cursor P01322; XPZ Attributes PrvPHorInh; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPUsrInh` (Usuario Inhabilitación) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, pprvir34.java cursor P01322; XPZ Attributes PrvPUsrInh; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPFchNot` (Ultima Fecha de Notificación) | Date | — | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: XML y hcof0006_impl.java cursor H00C15; XPZ Attributes PrvPFchNot; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPHorNot` (Ultima Hora de Notificación) | Character(8) | CoHora | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, pprvir34.java cursor P01322; XPZ Attributes PrvPHorNot; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPUsuNot` (Ultimo Usuario de Notificación) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvinsrp_impl.java INSERT INTO PrvPerfil; tipo: solo Java, pprvir34.java cursor P01322; XPZ Attributes PrvPUsuNot; no está en la estructura de TPrvInsRP del XPZ] |
| `PrvPNom` (Nombre del proveedor) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvPNom; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |
| `PrvPUsrSrv` (Usuario Services) | sin tipo | ACPSUsuario | [S · capas: diseño · ev: XPZ Attributes PrvPUsrSrv; fórmula ParmModPrv.ServicesPrefijoUsuarios + PrvPUSr; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |
| `PrvSocPais` (Nombre Pais) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvSocPais; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |
| `PrvSocPcia` (Nombre Provincia) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvSocPcia; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |
| `PrvSocLoc` (Nombre Localidad) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvSocLoc; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |
| `PrvSocPos` (Código Postal) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvSocPos; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |

Hallazgos de esta tabla, en párrafo porque no son filas del modelo. Las 22 columnas que están en el `INSERT` del Java y no en la estructura de `TPrvInsRP` del XPZ (por ejemplo `PrvPClaseUsr`, `PrvPAdminCat` y `PrvPRstClave`) tienen su definición en `<Attributes>` y las escriben otros objetos (`PCADM001`, `APPRVP007`, `PPrvIR64`...): la tabla es la unión de varias transacciones y procedimientos. Los 6 atributos de la estructura del XPZ que no son columna (`PrvPNom`, `PrvPUsrSrv`, `PrvSocPais`, `PrvSocPcia`, `PrvSocLoc`, `PrvSocPos`) son inferidos o fórmula y quedan al final de la tabla en estado S.

## Entidades hijas de PrvPerfil

Las seis transacciones hijas que la propuesta marcó como faltantes en el export. Las claves salen del `DELETE ... WHERE` de su `_impl.java`.

- **R-402** La clave de cada tabla hija empieza con `PrvPUSr`: ninguna fila hija existe sin el usuario del perfil en su clave. [V · capas: código · ev: DELETE ... WHERE de tprvpj_impl.java T00CA13, tprvdom_impl.java T00C819, tprvesp_impl.java T00C911, tprvrub_impl.java T00C711, tprvrpr_impl.java T00C619, tprvbco_impl.java T00O219, tprvpod_impl.java T00CB19 y tprvperfildoc_impl.java T00N913 · clase: esencial]
- **R-403** El correlativo de las hijas `PrvPJ`, `PrvDom`, `PrvRpr`, `PrvPod` y `PrvBco` lo toma de un contador guardado en el perfil (`PrvPJUltNro`, `PrvDomUltNroOrden`, `PrvRprUltNroLin`, `PrvPodUltNroLin`, `PrvBcoUltNroLin`), y la transacción hija lo actualiza con un `UPDATE PrvPerfil`. `PrvRub` y `PrvESP` no tienen contador: su clave trae el dato. [V · capas: código · ev: tprvrpr_impl.java standaloneStartupServer (A5377PrvRprNroLin = A5394PrvRprUltNroLin) y cursor T00C623; igual en tprvpod_impl.java T00CB23, tprvbco_impl.java T00O223, tprvdom_impl.java T00C823 y tprvpj_impl.java T00CA14 · clase: esencial]

### PrvPJ

- Tabla `PrvPJ`, clave (`PrvPUSr`, `PrvPJNroInt`). Transacción `TPrvPJ` (Integrantes de la Sociedad), fuera del export. [V · capas: código · ev: tprvpj_impl.java cursor T00CA13 (DELETE FROM PrvPJ WHERE PrvPUSr y PrvPJNroInt); TPrvPJ no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvPJNroInt` (Nro integrante de la persona jurídica) | Numeric(2,0) | — | [V · capas: código, diseño · ev: tprvpj_impl.java INSERT INTO PrvPJ; tipo: XML y tprvpj_impl.java cursor T00CA15; XPZ Attributes PrvPJNroInt] |
| `PrvPJCargo` (Cargo) | Numeric(2,0) | — | [V · capas: código, diseño · ev: tprvpj_impl.java INSERT INTO PrvPJ; tipo: XML y tprvpj_impl.java cursor T00CA2; XPZ Attributes PrvPJCargo] |
| `PrvPJNombre` (Nombre) | Character(60) | CoNombre | [V · capas: código, diseño · ev: tprvpj_impl.java INSERT INTO PrvPJ; tipo: solo Java, tprvpj_impl.java cursor T00CA2; XPZ Attributes PrvPJNombre] |
| `PrvPJIgnTi` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: tprvpj_impl.java INSERT INTO PrvPJ; tipo: tprvpj_impl.java cursor T00CA2; sin definición en XPZ Attributes] |
| `PrvPJIgnNr` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: tprvpj_impl.java INSERT INTO PrvPJ; tipo: tprvpj_impl.java cursor T00CA2; sin definición en XPZ Attributes] |
| `PrvPJIgnDv` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: tprvpj_impl.java INSERT INTO PrvPJ; tipo: tprvpj_impl.java cursor T00CA2; sin definición en XPZ Attributes] |
| `PrvPJRepLeg` (Es representante legal) | Character(1) | — | [V · capas: código, diseño · ev: tprvpj_impl.java INSERT INTO PrvPJ; tipo: XML y tprvpj_impl.java cursor T00CA2; XPZ Attributes PrvPJRepLeg] |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvpj_impl.java INSERT INTO PrvPJ; tipo: solo Java, tprvpj_impl.java cursor T00CA15; XPZ Attributes PrvPUSr] |

### PrvDom

- Tabla `PrvDom`, clave (`PrvPUSr`, `PrvDomTip`, `PrvDomNroOrden`). Transacción `TPrvDom` (Domicilios del Proveedor), fuera del export. [V · capas: código · ev: tprvdom_impl.java cursor T00C819 (DELETE FROM PrvDom WHERE PrvPUSr, PrvDomTip y PrvDomNroOrden); TPrvDom no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvDomTip` (Tipo de Domicilio) | Numeric(2,0) | — | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: XML y tprvdom_impl.java cursor T00C813; XPZ Attributes PrvDomTip] |
| `PrvDomNroOrden` (Nro de línea del domicilio) | Numeric(1,0) | — | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: XML y tprvdom_impl.java cursor T00C813; XPZ Attributes PrvDomNroOrden] |
| `PrvDomCal` (Domicilio o calle) | Character(40) | CoDomCalle | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: solo Java, tprvdom_impl.java cursor T00C82; XPZ Attributes PrvDomCal] |
| `PrvDomNro` (Nº) | Character(5) | CoDomNro | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: solo Java, tprvdom_impl.java cursor T00C82; XPZ Attributes PrvDomNro] |
| `PrvDomPiso` (Piso) | Character(2) | CoDomPiso | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: solo Java, tprvdom_impl.java cursor T00C82; XPZ Attributes PrvDomPiso] |
| `PrvDomDto` (Depto) | Character(3) | CoDomDepto | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: solo Java, tprvdom_impl.java cursor T00C82; XPZ Attributes PrvDomDto] |
| `PrvDomBarrio` | Character(40) | — | [V · capas: código · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: tprvdom_impl.java cursor T00C82; sin definición en XPZ Attributes] |
| `PrvDomMzana` | Character(3) | — | [V · capas: código · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: tprvdom_impl.java cursor T00C82; sin definición en XPZ Attributes] |
| `PrvDomCasa` | Character(3) | — | [V · capas: código · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: tprvdom_impl.java cursor T00C82; sin definición en XPZ Attributes] |
| `PrvDomLote` | Character(3) | — | [V · capas: código · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: tprvdom_impl.java cursor T00C82; sin definición en XPZ Attributes] |
| `PrvDomTel` (Teléfono) | Character(15) | CoTelefono | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: solo Java, tprvdom_impl.java cursor T00C82; XPZ Attributes PrvDomTel] |
| `PrvDomCel` (Celular) | Numeric (10-18 dígitos) | CoTelCelular | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: solo Java, tprvdom_impl.java cursor T00C82; XPZ Attributes PrvDomCel] |
| `PrvDomMail` (Correo Electrónico) | Character(60) | CoMail | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: solo Java, tprvdom_impl.java cursor T00C82; XPZ Attributes PrvDomMail] |
| `PrvDomRep` (Representante o Contacto en el domicilio) | Character(40) | — | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: XML y tprvdom_impl.java cursor T00C82; XPZ Attributes PrvDomRep] |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: solo Java, tprvdom_impl.java cursor T00C813; XPZ Attributes PrvPUSr] |
| `PrvDomPaisCgo` | Numeric (3-4 dígitos) | — | [V · capas: código · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: tprvdom_impl.java cursor T00C82; sin definición en XPZ Attributes] |
| `PrvDomPciaCgo` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: tprvdom_impl.java cursor T00C82; sin definición en XPZ Attributes] |
| `PrvDomLocCgo` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: tprvdom_impl.java INSERT INTO PrvDom; tipo: tprvdom_impl.java cursor T00C82; sin definición en XPZ Attributes] |
| `PrvDomPcia` (Provincia) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvDomPcia; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |
| `PrvDomPos` (Código postal) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvDomPos; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |
| `PrvDomLoc` (Localidad) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvDomLoc; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |

### PrvESP

- Tabla `PrvESP`, clave (`PrvPUSr`, `PrvESPFchCie`). Transacción `TPrvESP` (Estado de Situación Patrimonial o Manifestación de Bienes), fuera del export, aunque `HPrvIR18` la llama (`TPrvESP.Popup`). [V · capas: código · ev: tprvesp_impl.java cursor T00C911 (DELETE FROM PrvESP WHERE PrvPUSr y PrvESPFchCie); TPrvESP no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvESPFchCie` (Fecha de cierre del Ejercicio) | Date | — | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: XML y tprvesp_impl.java cursor T00C912; XPZ Attributes PrvESPFchCie] |
| `PrvESPTAC` (Total Activo Corriente) | Numeric (2 decimales) | GenImporte | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPTAC] |
| `PrvESPTANC` (Total Activo No Corriente) | Numeric (2 decimales) | GenImporte | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPTANC] |
| `PrvESPTAE` | Numeric (2 decimales) | — | [V · capas: código · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: tprvesp_impl.java cursor T00C92; sin definición en XPZ Attributes] |
| `PrvESPTPC` (Total Pasivo Corriente) | Numeric (2 decimales) | GenImporte | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPTPC] |
| `PrvESPTPNC` (Total Pasivo No Corriente) | Numeric (2 decimales) | GenImporte | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPTPNC] |
| `PrvESPTPE` | Numeric (2 decimales) | — | [V · capas: código · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: tprvesp_impl.java cursor T00C92; sin definición en XPZ Attributes] |
| `PrvESPPNE` (Patrimonio Neto) | Numeric (2 decimales) | GenImporte | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPPNE] |
| `PrvESPTPPos` (Total Pasivo Positivo) | Numeric (2 decimales) | GenImporte | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPTPPos] |
| `PrvESPTVN` (Total Ventas Netas) | Numeric (2 decimales) | GenImporte | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPTVN] |
| `PrvESPRes` (Resultado del ejercicio) | Numeric (2 decimales) | GenImporte | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPRes] |
| `PrvESPNomCertificante` (Nombre del profesional certificante) | Character(60) | CoNombre | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPNomCertificante] |
| `PrvESPMatCertificante` (Nº Matrícula del profesional certificante) | Character(10) | — | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: XML y tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPMatCertificante] |
| `PrvESPFchLeg` (Fecha de Legalización en CPCE) | Date | — | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: XML y tprvesp_impl.java cursor T00C92; XPZ Attributes PrvESPFchLeg] |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvesp_impl.java INSERT INTO PrvESP; tipo: solo Java, tprvesp_impl.java cursor T00C912; XPZ Attributes PrvPUSr] |

### PrvRub

- Tabla `PrvRub`, clave (`PrvPUSr`, `PrvRubNro`, `PrvRubBsSrv`, `PrvRubSubRub`). Transacción `TPrvRub` (Rubros asociados al proveedor), fuera del export. [V · capas: código · ev: tprvrub_impl.java cursor T00C711 (DELETE FROM PrvRub WHERE PrvPUSr, PrvRubNro, PrvRubBsSrv y PrvRubSubRub); TPrvRub no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvRubNro` (Rubro de proveedor) | Numeric (5-9 dígitos) | RubroCod | [V · capas: código, diseño · ev: tprvrub_impl.java INSERT INTO PrvRub; tipo: solo Java, tprvrub_impl.java cursor T00C712; XPZ Attributes PrvRubNro] |
| `PrvRubBsSrv` (Bienes o servicios) | Numeric (1-2 dígitos) | GENBienServicio | [V · capas: código, diseño · ev: tprvrub_impl.java INSERT INTO PrvRub; tipo: solo Java, tprvrub_impl.java cursor T00C712; XPZ Attributes PrvRubBsSrv] |
| `PrvRubSubRub` (Subrubro de Proveedor) | Numeric(3,0) | — | [V · capas: código, diseño · ev: tprvrub_impl.java INSERT INTO PrvRub; tipo: XML y tprvrub_impl.java cursor T00C712; XPZ Attributes PrvRubSubRub] |
| `PrvRubDsc` (Nombre del Rubro/subrubro) | Character(70) | CoDet2 | [V · capas: código, diseño · ev: tprvrub_impl.java INSERT INTO PrvRub; tipo: solo Java, tprvrub_impl.java cursor T00C72; XPZ Attributes PrvRubDsc] |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvrub_impl.java INSERT INTO PrvRub; tipo: solo Java, tprvrub_impl.java cursor T00C712; XPZ Attributes PrvPUSr] |

### PrvRpr

- Tabla `PrvRpr`, clave (`PrvPUSr`, `PrvRprNroLin`). Transacción `TPrvRpr` (Representantes de Proveedores), fuera del export. [V · capas: código · ev: tprvrpr_impl.java cursor T00C619 (DELETE FROM PrvRpr WHERE PrvPUSr y PrvRprNroLin); TPrvRpr no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvRprNroLin` (Nro. de linea del representante) | Numeric(5,0) | — | [V · capas: código, diseño · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: XML y tprvrpr_impl.java cursor T00C613; XPZ Attributes PrvRprNroLin] |
| `PrvRprNom` (Nombre del Representante) | Character(59) | CoProveNom | [V · capas: código, diseño · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: solo Java, tprvrpr_impl.java cursor T00C62; XPZ Attributes PrvRprNom] |
| `PrvRprCal` | Character(40) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprDNro` | Character(5) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprDPiso` | Character(2) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprDDepto` | Character(3) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprDBarrio` | Character(40) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprDMzana` | Character(3) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprDCasa` | Character(3) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprDLote` | Character(3) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprTel` | Character(15) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprMail` (Mail) | Character(60) | CoMail | [V · capas: código, diseño · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: solo Java, tprvrpr_impl.java cursor T00C62; XPZ Attributes PrvRprMail] |
| `PrvRprCel` (Celular) | Numeric (10-18 dígitos) | CoTelCelular | [V · capas: código, diseño · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: solo Java, tprvrpr_impl.java cursor T00C62; XPZ Attributes PrvRprCel] |
| `PrvRprTipDoc` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprNroDoc` (Nro de Documento) | Numeric (10-18 dígitos) | CUIL | [V · capas: código, diseño · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: solo Java, tprvrpr_impl.java cursor T00C62; XPZ Attributes PrvRprNroDoc] |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: solo Java, tprvrpr_impl.java cursor T00C613; XPZ Attributes PrvPUSr] |
| `PrvRprPaisCgo` | Numeric (3-4 dígitos) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprPciaCgo` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |
| `PrvRprLocCgo` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: tprvrpr_impl.java INSERT INTO PrvRpr; tipo: tprvrpr_impl.java cursor T00C62; sin definición en XPZ Attributes] |

### PrvBco

- Tabla `PrvBco`, clave (`PrvPUSr`, `PrvBcoNroLin`). Transacción `TPrvBco` (Cuentas Bancarias del Proveedor), fuera del export. [V · capas: código · ev: tprvbco_impl.java cursor T00O219 (DELETE FROM PrvBco WHERE PrvPUSr y PrvBcoNroLin); TPrvBco no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvBcoNroLin` (Nro de Linea Cuenta Bancaria) | Numeric(5,0) | — | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: XML y tprvbco_impl.java cursor T00O213; XPZ Attributes PrvBcoNroLin] |
| `PrvBcoNro` (Nro de Cuenta) | Character(12) | CoCtaBco | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: solo Java, tprvbco_impl.java cursor T00O22; XPZ Attributes PrvBcoNro] |
| `PrvBcoSuc` (Sucursal) | Character(4) | CoBcoSuc | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: solo Java, tprvbco_impl.java cursor T00O22; XPZ Attributes PrvBcoSuc] |
| `PrvBcoVig` (Fecha de vigencia) | Date | — | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: XML y tprvbco_impl.java cursor T00O22; XPZ Attributes PrvBcoVig] |
| `PrvBcoCBU1` (CBU bloque 1) | Numeric (5-9 dígitos) | CoCBU1 | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: solo Java, tprvbco_impl.java cursor T00O22; XPZ Attributes PrvBcoCBU1] |
| `PrvBcoCBU2` (CBU bloque 2) | Numeric (10-18 dígitos) | CoCBU2 | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: solo Java, tprvbco_impl.java cursor T00O22; XPZ Attributes PrvBcoCBU2] |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: solo Java, tprvbco_impl.java cursor T00O213; XPZ Attributes PrvPUSr] |
| `PrvBcoMon` (Moneda) | Numeric (3-4 dígitos) | — | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: solo Java, tprvbco_impl.java cursor T00O22; XPZ Attributes PrvBcoMon] |
| `PrvBcoBco` (Banco) | Numeric (3-4 dígitos) | — | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: solo Java, tprvbco_impl.java cursor T00O22; XPZ Attributes PrvBcoBco] |
| `PrvBcoTip` (Tipo de cuenta bancaria) | Numeric (1-2 dígitos) | — | [V · capas: código, diseño · ev: tprvbco_impl.java INSERT INTO PrvBco; tipo: solo Java, tprvbco_impl.java cursor T00O22; XPZ Attributes PrvBcoTip] |
| `PrvBcoMonCursoLegal` (Moneda de Curso Legal) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvBcoMonCursoLegal; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |
| `PrvBcoMonSimb` (Simbolo de la moneda) | sin tipo | — | [S · capas: diseño · ev: XPZ Attributes PrvBcoMonSimb; atributo inferido: sin Length ni tipo en XPZ Attributes; no es columna en ningún INSERT del Java; motivo S: sin tipo en ninguna fuente] |

## Otras entidades del módulo

Fuera de las seis hijas del pedido, el Java trae cuatro tablas más que el módulo lee o escribe y una zona de referencia. Se documentan con el mismo criterio.

### PrvPod

- Tabla `PrvPod`, clave (`PrvPUSr`, `PrvPodNroLin`). Transacción `TPrvPod` (Apoderados del Proveedor), fuera del export. [V · capas: código · ev: tprvpod_impl.java cursor T00CB19 (DELETE FROM PrvPod WHERE PrvPUSr y PrvPodNroLin); TPrvPod no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvPodNroLin` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB13; sin definición en XPZ Attributes] |
| `PrvPodTipDoc` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodNroDoc` | Numeric (10-18 dígitos) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodNom` | Character(60) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodCal` | Character(40) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodNro` | Character(5) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodPiso` | Character(2) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodDepto` | Character(3) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodBarrio` | Character(40) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodMzana` | Character(3) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodCasa` | Character(3) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodLote` | Character(3) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodTel` | Character(15) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodTipPod` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodFecVto` | Date | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodMail` | Character(60) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodTipFma` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: solo Java, tprvpod_impl.java cursor T00CB13; XPZ Attributes PrvPUSr] |
| `PrvPodPaisCgo` | Numeric (3-4 dígitos) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodPciaCgo` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |
| `PrvPodLocCgo` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: tprvpod_impl.java INSERT INTO PrvPod; tipo: tprvpod_impl.java cursor T00CB2; sin definición en XPZ Attributes] |

### PrvPerfilDoc

- Tabla `PrvPerfilDoc`, clave (`PrvPUSr`, `PrvPDocId`). Transacción `TPrvPerfilDoc` (Documentación subida por el Proveedor), fuera del export. [V · capas: código · ev: tprvperfildoc_impl.java cursor T00N913 (DELETE FROM PrvPerfilDoc WHERE PrvPUSr y PrvPDocId); TPrvPerfilDoc no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvPDocId` | Numeric (3-4 dígitos) | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N910; sin definición en XPZ Attributes] |
| `PrvPDocArch` | Character(60) | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N92; sin definición en XPZ Attributes] |
| `PrvPDocDes` | Character(255) | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N92; sin definición en XPZ Attributes] |
| `PrvPDocGUID` | Character(36) | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N92; sin definición en XPZ Attributes] |
| `PrvPDocfec` | DateTime | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N92; sin definición en XPZ Attributes] |
| `PrvPDocFecVis` | DateTime | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N92; sin definición en XPZ Attributes] |
| `PrvPDocUsrVis` | Character(30) | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N92; sin definición en XPZ Attributes] |
| `PrvPDocFecVto` | Date | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N92; sin definición en XPZ Attributes] |
| `PrvPDocVtoNot` | DateTime | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N92; sin definición en XPZ Attributes] |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: solo Java, tprvperfildoc_impl.java cursor T00N910; XPZ Attributes PrvPUSr] |
| `PerDocCod` | Numeric (3-4 dígitos) | — | [V · capas: código · ev: tprvperfildoc_impl.java INSERT INTO PrvPerfilDoc; tipo: tprvperfildoc_impl.java cursor T00N92; sin definición en XPZ Attributes] |

### PrvHis

- Tabla `PrvHis`, clave (`PrvPUSr`, `PrvHFchSis`, `PrvHHorSis`, `PrvHError`). Transacción `TPrvHis` (Perfil portal histórico); la escribe `PPrvIR53` (historial de operaciones sobre el perfil). [V · capas: código · ev: tprvhis_impl.java cursor T00O312 (DELETE FROM PrvHis WHERE PrvPUSr, PrvHFchSis, PrvHHorSis y PrvHError); TPrvHis no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvHFchSis` (Fecha de proceso) | Date | — | [V · capas: código, diseño · ev: tprvhis_impl.java INSERT INTO PrvHis; tipo: XML y tprvhis_impl.java cursor T00O313; XPZ Attributes PrvHFchSis] |
| `PrvHHorSis` (Hora de proceso) | Character(8) | CoHora | [V · capas: código, diseño · ev: tprvhis_impl.java INSERT INTO PrvHis; tipo: solo Java, tprvhis_impl.java cursor T00O313; XPZ Attributes PrvHHorSis] |
| `PrvHError` (Secuencia) | Numeric (3-4 dígitos) | — | [V · capas: código, diseño · ev: tprvhis_impl.java INSERT INTO PrvHis; tipo: solo Java, tprvhis_impl.java cursor T00O313; XPZ Attributes PrvHError] |
| `PrvHUsrSis` (Usuario que procesa) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvhis_impl.java INSERT INTO PrvHis; tipo: solo Java, tprvhis_impl.java cursor T00O32; XPZ Attributes PrvHUsrSis] |
| `PrvHCgoOpe` (Código de operación) | Numeric (1-2 dígitos) | PrvHiCgoOpe | [V · capas: código, diseño · ev: tprvhis_impl.java INSERT INTO PrvHis; tipo: solo Java, tprvhis_impl.java cursor T00O32; XPZ Attributes PrvHCgoOpe] |
| `PrvHDatAnt` (Dato anterior) | Character(256) | — | [V · capas: código, diseño · ev: tprvhis_impl.java INSERT INTO PrvHis; tipo: XML y tprvhis_impl.java cursor T00O32; XPZ Attributes PrvHDatAnt] |
| `PrvHDatPos` (Dato posterior) | Character(256) | — | [V · capas: código, diseño · ev: tprvhis_impl.java INSERT INTO PrvHis; tipo: XML y tprvhis_impl.java cursor T00O32; XPZ Attributes PrvHDatPos] |
| `PrvHObs` (Observaciones) | Character(256) | — | [V · capas: código, diseño · ev: tprvhis_impl.java INSERT INTO PrvHis; tipo: XML y tprvhis_impl.java cursor T00O32; XPZ Attributes PrvHObs] |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: tprvhis_impl.java INSERT INTO PrvHis; tipo: solo Java, tprvhis_impl.java cursor T00O313; XPZ Attributes PrvPUSr] |

### PrvSolicitud

- Tabla `PrvSolicitud`, clave (`PrvPUSr`, `PrvSolFch`, `PrvSolTipo`). No tiene transacción propia en `fin/`: la crean `PPrvIR72` (tipo `C`, cambio de categoría) y `PPrvIR75` (tipo `R`, reinscripción) y la borra `PPrvIR76`. [V · capas: código · ev: pprvir76.java cursor P02VY2 (DELETE FROM PrvSolicitud WHERE PrvPUSr, PrvSolFch y PrvSolTipo); pprvir72.java cursor P02VV2 y pprvir75.java cursor P02VX3 (INSERT)]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvPUSr` (Usuario) | Character(30) | ACPSUsuario | [V · capas: código, diseño · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: solo Java, arprvir14_impl.java cursor P01ZH3; XPZ Attributes PrvPUSr] |
| `PrvSolFch` | Date | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: arprvir14_impl.java cursor P01ZH3; sin definición en XPZ Attributes] |
| `PrvSolTipo` | Character(1) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: arprvir14_impl.java cursor P01ZH3; sin definición en XPZ Attributes] |
| `PrvSolHor` | Character(8) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: arprvir14_impl.java cursor P01ZH3; sin definición en XPZ Attributes] |
| `PrvSolARBaj` | Numeric (3-4 dígitos) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: arprvir88_impl.java cursor P02W93; sin definición en XPZ Attributes] |
| `PrvSolNRBaj` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: arprvir88_impl.java cursor P02W93; sin definición en XPZ Attributes] |
| `PrvSolLRBaj` | Character(1) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: pprvir67.java cursor P02VR2; sin definición en XPZ Attributes] |
| `PrvSolTRBaj` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: pprvir67.java cursor P02VR2; sin definición en XPZ Attributes] |
| `PrvSolFCon` | Date | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: arprvir14_impl.java cursor P01ZH3; sin definición en XPZ Attributes] |
| `PrvSolUCon` | Character(30) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: pprvir29.java cursor P012X3; sin definición en XPZ Attributes] |
| `PrvSolHCon` | Character(8) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: pprvir29.java cursor P012X3; sin definición en XPZ Attributes] |
| `PrvSolCSol` | Character(1) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: arprvir14_impl.java cursor P01ZH3; sin definición en XPZ Attributes] |
| `PrvSolResolucion` | Numeric (largo sin fuente) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: solo la clase, por el valor literal por defecto del INSERT; sin lector Java ni definición en XPZ Attributes: falta el largo] |
| `PrvSolNroBolOficial` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: pprvir29.java cursor P012X5; sin definición en XPZ Attributes] |
| `PrvSolFchBolOficial` | Date | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: pprvir29.java cursor P012X5; sin definición en XPZ Attributes] |
| `PrvSolNCartaDoc` | Numeric (3-4 dígitos) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: pprvir29.java cursor P012X5; sin definición en XPZ Attributes] |
| `PrvSolARAlt` | Numeric (3-4 dígitos) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: hprvir82_impl.java cursor H01EM2; sin definición en XPZ Attributes] |
| `PrvSolNRAlt` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: hprvir82_impl.java cursor H01EM2; sin definición en XPZ Attributes] |
| `PrvSolLRAlt` | Character (largo sin fuente) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: solo la clase, por el valor literal por defecto del INSERT; sin lector Java ni definición en XPZ Attributes: falta el largo] |
| `PrvSolTRAlt` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: pprvir82.java cursor P02W42; sin definición en XPZ Attributes] |
| `PrvSolArchivo` | Character(254) | — | [V · capas: código · ev: pprvir75.java INSERT INTO PrvSolicitud; tipo: hprvir74_impl.java cursor H01EV4; sin definición en XPZ Attributes] |

### PrvZon

- Tabla `PrvZon`, clave `PrvZonCod`. Transacción `TPrvZon` (Zonas de los proveedores); `PrvPerfil.PrvZonCod` la referencia. [V · capas: código · ev: tprvzon_impl.java cursor T00CD10 (DELETE FROM PrvZon WHERE PrvZonCod); TPrvZon no figura entre los objetos del XPZ]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `PrvZonCod` (Código de Zona) | Numeric (3-4 dígitos) | CoPrvZona | [V · capas: código, diseño · ev: tprvzon_impl.java INSERT INTO PrvZon; tipo: solo Java, tprvzon_impl.java cursor T00CD15; XPZ Attributes PrvZonCod] |
| `PrvZonDsc` | Character(40) | — | [V · capas: código · ev: tprvzon_impl.java INSERT INTO PrvZon; tipo: tprvzon_impl.java cursor T00CD2; sin definición en XPZ Attributes] |
| `PrvZonHabCat` | Character(1) | — | [V · capas: código · ev: tprvzon_impl.java INSERT INTO PrvZon; tipo: tprvzon_impl.java cursor T00CD2; sin definición en XPZ Attributes] |

## Integridad al borrar

- **R-404** El borrado físico de un proveedor (`PPrvIR35` en modo `D`) borra a mano, en este orden, `PrvDom`, `PrvPJ`, `PrvESP`, `PrvRpr`, `PrvPod`, `PrvRub`, `PrvPerfilDoc` y `PrvPerfil`, y, si el perfil tiene `PrvPNro`, deja `Prove.ProveArcest` en 1. No borra `PrvBco`, `PrvHis` ni `PrvSolicitud`: sus filas quedan sin perfil. [V · capas: código · ev: pprvir35.java privateExecute (rama modo D) con los cursores P01337 a P013315 · clase: esencial]

La clase de R-404 es `esencial` por defecto: la evidencia dice qué borra y qué no, no si omitir `PrvBco` fue una decisión. Las fuentes no traen restricciones de clave foránea ni borrado en cascada de la base, así que la integridad entre el perfil y sus hijas la sostienen los procedimientos.

## Tabla de GEN que el módulo toca: Prove

`Prove` es el padrón de proveedores de GEN y no pertenece al módulo. Se listan solo las columnas que `PPrvIR02`, `PPrvIR35` y `PPrvIR64` leen o escriben.

- Tabla `Prove`, identificada por `ProveNro` en el `WHERE` de los `UPDATE` del módulo (clave deducida del `WHERE`, no de un `DELETE`). [V · capas: código · ev: pprvir35.java cursores P01334 y P01335 (SELECT y UPDATE Prove WHERE ProveNro); pprvir64.java cursor P02VP4]

| Atributo | Tipo | Dominio | bloque |
| --- | --- | --- | --- |
| `ProveNro` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: pprvir02.java cursor P04K23 (SELECT FROM Prove); sin tipo en el XML] |
| `ProveIgnTip` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: pprvir02.java cursor P04K23; sin tipo en el XML] |
| `ProveIgnNro` | Numeric (5-9 dígitos) | — | [V · capas: código · ev: pprvir02.java cursor P04K23; sin tipo en el XML] |
| `ProveIgnDig` | Numeric (1-2 dígitos) | — | [V · capas: código · ev: pprvir02.java cursor P04K23; sin tipo en el XML] |
| `ProveFecBaja` | Date | — | [V · capas: código · ev: pprvir02.java cursor P04K23; sin tipo en el XML] |
| `ProveTip` | Character(1) | — | [V · capas: código · ev: pprvir02.java cursor P04K23; sin tipo en el XML] |
| `ProveArcest` (Inscripto en el registro) | Numeric (1-2 dígitos) | GenProvInsReg | [V · capas: código, diseño · ev: pprvir35.java cursor P01334 (SELECT ProveNro, ProveArcest); XPZ Attributes ProveArcest con idBasedOn Domain:GenProvInsReg y sin Length] |

## Huecos

Lo que estas fuentes no permiten cerrar, en párrafo.

Los atributos `PrvSolResolucion` y `PrvSolLRAlt` de `PrvSolicitud` solo figuran con su valor por defecto en el `INSERT` (un número y una cadena vacía): se sabe la clase de tipo y falta el largo. Los dominios (`ACPSUsuario`, `CoMail`, `GenImporte`...) no están en el export, así que no se puede decir de qué tipo base ni de qué largo es cada uno más allá de lo que lee el Java. `PrvPHabTGP`, la otra columna de habilitación, no se documenta acá (ver `estados.md`).
