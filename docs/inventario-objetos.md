# Inventario de objetos del export

Objetos y atributos de `GENFin-RegProv.xpz` (KB `GENFin18U8`), contados desde el XML extraído, no a mano (CA2). Se cuentan los hijos directos de `<Objects>` y de `<Attributes>`.

Comando, desde la raíz del repo:

```
python3 -I docs/herramientas/contar-xpz.py ../genfin-gx-extraido/xpz/GENFin-RegProv.xml --listar
```

Salida del resumen (2026-10-23):

```
Objetos por tipo:
  Domain       87
  SDT          20
  WebPanel     10
  Table        1
  Transaction  1
Total objetos:   119
Total atributos: 194
```

## Fechas de versión

El export **no es todo de 2020**, como decía la propuesta: los `versionDate` de los objetos van de 2020-06-24 a 2026-04-23. Por año: 2020: 101, 2021: 2, 2022: 2, 2024: 4, 2026: 10. Esto pesa en el chequeo de versión (E1): un objeto de 2026 en el XPZ puede estar más cerca del Java de `fin/` que uno de 2020.

## Objetos

La columna `cobertura` dice dónde está documentado cada objeto, o por qué queda fuera de alcance. Se completa al final (G1), contra `universo-modulo.md`.

| Nombre | Tipo | versionDate | Cobertura |
|---|---|---|---|
| `ACPSAtributo` | Domain | 2020-06-24 | *(G1)* |
| `ACPSCnlNombre` | Domain | 2020-06-24 | *(G1)* |
| `ACPSCnlTipoConv` | Domain | 2020-06-24 | *(G1)* |
| `ACPSDMDocCnt` | Domain | 2020-06-24 | *(G1)* |
| `ACPSDMDocGUID` | Domain | 2020-06-24 | *(G1)* |
| `ACPSEmail` | Domain | 2020-06-24 | *(G1)* |
| `ACPSEmailCheck` | Domain | 2020-06-24 | *(G1)* |
| `ACPSEmailPriority` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgAsunto` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgCnvDescripcion` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgCnvEstado` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgCnvVisualizacion` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgDstEstado` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgDstTipo` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgEstado` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgEtqDescripcion` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgEtqJerarquia` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgEtqNombre` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgFH` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgIdent` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgTexto` | Domain | 2020-06-24 | *(G1)* |
| `ACPSMsgUsuForm` | Domain | 2020-06-24 | *(G1)* |
| `ACPSSistema` | Domain | 2020-06-24 | *(G1)* |
| `ACPSTelefono` | Domain | 2020-06-24 | *(G1)* |
| `ACPSTipoDeDatoAtributo` | Domain | 2020-06-24 | *(G1)* |
| `ACPSUserFullName` | Domain | 2020-06-24 | *(G1)* |
| `ACPSUserName` | Domain | 2020-06-24 | *(G1)* |
| `ACPSUsuario` | Domain | 2020-10-07 | *(G1)* |
| `ACPSValorAtributo` | Domain | 2020-09-22 | *(G1)* |
| `Boolean` | Domain | 2020-06-24 | *(G1)* |
| `CoAANor` | Domain | 2020-06-24 | *(G1)* |
| `CoBco` | Domain | 2020-06-24 | *(G1)* |
| `CoBcoSuc` | Domain | 2020-06-24 | *(G1)* |
| `CoCBU1` | Domain | 2020-06-24 | *(G1)* |
| `CoCBU2` | Domain | 2020-06-24 | *(G1)* |
| `CoCCosto` | Domain | 2020-06-24 | *(G1)* |
| `CoCodPosNue` | Domain | 2020-06-24 | *(G1)* |
| `CoCtaBco` | Domain | 2020-06-24 | *(G1)* |
| `CoCuc` | Domain | 2020-06-24 | *(G1)* |
| `CoCucMay` | Domain | 2020-06-24 | *(G1)* |
| `CoDependencia` | Domain | 2020-06-24 | *(G1)* |
| `CoDet2` | Domain | 2020-06-24 | *(G1)* |
| `CoDomCalle` | Domain | 2020-06-24 | *(G1)* |
| `CoDomDepto` | Domain | 2020-06-24 | *(G1)* |
| `CoDomDpt` | Domain | 2020-06-24 | *(G1)* |
| `CoDomNro` | Domain | 2020-06-24 | *(G1)* |
| `CoDomPais` | Domain | 2020-06-24 | *(G1)* |
| `CoDomPcia` | Domain | 2020-06-24 | *(G1)* |
| `CoDomPiso` | Domain | 2020-06-24 | *(G1)* |
| `CoEjer` | Domain | 2020-06-24 | *(G1)* |
| `CoHora` | Domain | 2020-06-24 | *(G1)* |
| `CoIntCar` | Domain | 2020-06-24 | *(G1)* |
| `CoIntJur` | Domain | 2020-06-24 | *(G1)* |
| `CoIntUor` | Domain | 2020-06-24 | *(G1)* |
| `CoLocalidad` | Domain | 2020-06-24 | *(G1)* |
| `CoMail` | Domain | 2020-06-24 | *(G1)* |
| `CoMoneda` | Domain | 2020-06-24 | *(G1)* |
| `CoNombre` | Domain | 2020-06-24 | *(G1)* |
| `CoNro` | Domain | 2020-06-24 | *(G1)* |
| `CoPais` | Domain | 2020-06-24 | *(G1)* |
| `CoProveedor` | Domain | 2020-06-24 | *(G1)* |
| `CoProveNom` | Domain | 2020-06-24 | *(G1)* |
| `CoProvincia` | Domain | 2020-06-24 | *(G1)* |
| `CoPrvZona` | Domain | 2020-06-24 | *(G1)* |
| `CoTelCelular` | Domain | 2020-06-24 | *(G1)* |
| `CoTelefono` | Domain | 2026-02-24 | *(G1)* |
| `CpPliegoNro` | Domain | 2020-06-24 | *(G1)* |
| `CUIL` | Domain | 2020-06-24 | *(G1)* |
| `DmnCuit` | Domain | 2020-06-24 | *(G1)* |
| `GENBienServicio` | Domain | 2020-06-24 | *(G1)* |
| `GenCjaOpeNro` | Domain | 2020-06-24 | *(G1)* |
| `GenImporte` | Domain | 2021-10-25 | *(G1)* |
| `GENIVASituacion` | Domain | 2020-06-24 | *(G1)* |
| `GENProDomTip` | Domain | 2026-04-21 | *(G1)* |
| `GenProveTipoPersona` | Domain | 2020-06-24 | *(G1)* |
| `GenProvInsReg` | Domain | 2020-06-24 | *(G1)* |
| `GSDepciaNom` | Domain | 2020-06-24 | *(G1)* |
| `GSEjerEst` | Domain | 2020-06-24 | *(G1)* |
| `GSNorTip` | Domain | 2020-06-24 | *(G1)* |
| `GSTipCtaBancaria` | Domain | 2020-06-24 | *(G1)* |
| `Lb4GxExcIndex` | Domain | 2020-06-24 | *(G1)* |
| `ParmModPrv` | Domain | 2021-12-27 | *(G1)* |
| `PrvHiCgoOpe` | Domain | 2024-11-19 | *(G1)* |
| `RDscMed` | Domain | 2020-06-24 | *(G1)* |
| `RRHHCodGen` | Domain | 2020-07-15 | *(G1)* |
| `RRHHUsoGen` | Domain | 2020-07-15 | *(G1)* |
| `RubroCod` | Domain | 2020-06-24 | *(G1)* |
| `ACPSContext` | SDT | 2020-06-24 | *(G1)* |
| `ACPSContextActiveEnvironment` | SDT | 2020-06-24 | *(G1)* |
| `ACPSContextAttribute` | SDT | 2020-06-24 | *(G1)* |
| `ACPSContextContext` | SDT | 2020-06-24 | *(G1)* |
| `ACPSContextEnvironment` | SDT | 2020-06-24 | *(G1)* |
| `ACPSContextSystem` | SDT | 2020-06-24 | *(G1)* |
| `ACPSContextUser` | SDT | 2020-06-24 | *(G1)* |
| `ACPSConversationHead` | SDT | 2020-06-24 | *(G1)* |
| `ACPSEmlQueue` | SDT | 2020-06-24 | *(G1)* |
| `ACPSMapDataType` | SDT | 2020-06-24 | *(G1)* |
| `ACPSMasterContext` | SDT | 2020-06-24 | *(G1)* |
| `ACPSMessage` | SDT | 2020-06-24 | *(G1)* |
| `ACPSMessagesToSend` | SDT | 2020-06-24 | *(G1)* |
| `ACPSMsgRecipient` | SDT | 2020-06-24 | *(G1)* |
| `ACPSStatus` | SDT | 2020-06-24 | *(G1)* |
| `ACPSTag` | SDT | 2020-06-24 | *(G1)* |
| `Context` | SDT | 2020-06-24 | *(G1)* |
| `PPrvSendMsgSDT` | SDT | 2020-06-24 | *(G1)* |
| `Prvhisparam` | SDT | 2022-11-02 | *(G1)* |
| `SDTCjuo` | SDT | 2020-06-24 | *(G1)* |
| `PrvPerfil` | Table | 2022-11-08 | *(G1)* |
| `TPrvInsRP` | Transaction | 2026-04-23 | *(G1)* |
| `HPrvIR02` | WebPanel | 2026-01-15 | *(G1)* |
| `HPrvIR06` | WebPanel | 2026-01-15 | *(G1)* |
| `HPrvIr07` | WebPanel | 2024-09-27 | *(G1)* |
| `HPrvIR09` | WebPanel | 2026-01-15 | *(G1)* |
| `HPrvIR10` | WebPanel | 2024-11-19 | *(G1)* |
| `HPrvIR17m` | WebPanel | 2026-01-15 | *(G1)* |
| `HPrvIR18` | WebPanel | 2026-01-15 | *(G1)* |
| `HPrvIR22` | WebPanel | 2026-03-11 | *(G1)* |
| `HPrvIR41` | WebPanel | 2026-04-21 | *(G1)* |
| `HPrvIR42` | WebPanel | 2024-11-19 | *(G1)* |

Los 194 atributos no se listan acá: sus definiciones y tipos están en `modelo-datos.md`.
