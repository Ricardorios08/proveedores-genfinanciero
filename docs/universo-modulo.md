# Universo del módulo en el Java generado

Hasta dónde llega el módulo Registro de Proveedores dentro de `fin/` (tarea B4, "Frontera del módulo" del diseño). Reemplaza a "objetos del XPZ más sus dependencias" como universo de cobertura: la administración, el modo `P` y quienes habilitan al proveedor solo están en `fin/`, y en el XML aparecen 0 veces.

Comando, desde la raíz del repo:

```
python3 -I docs/herramientas/universo-fin.py ../genfin-gx-extraido/fin --markdown
```

**Regla.** *Dentro del módulo* entra la clausura de referencias desde los puntos de entrada (los 11 paneles del alta, `hprvir39` y `popro001`), siguiendo solo la familia `hprv*`, `pprv*`, `tprv*`, `rprv*` y `popro*`, con una `a` opcional adelante: GeneXus genera así los reportes (`arprvir10`) y los procedimientos que también corren como programa (`pprvir03.java` es un envoltorio de `apprvir03`). Lo demás que el módulo referencia es *punto de contacto*. Los objetos de fuera de la familia que referencian al módulo son *entradas externas*. Los de la familia que la clausura no alcanza quedan en el *borde*, para revisarlos a mano.

**Controles** (pasaron el 2026-10-23; recalculado el mismo día al agregar el prefijo `a`, que movió 2 objetos de punto de contacto a dentro del módulo y sumó 3 al borde): `hprvir21` y `pprvir50` quedan dentro, `loginprov` (el login del proveedor) en entradas externas, y `pprvsendmail` en el borde, llamado por `loginrecuperarpwd`.

**Lo que muestra el borde (revisión pendiente, G1):**
- **La recuperación de clave del proveedor no pasa por el módulo:** `loginrecuperarpwd` usa `pprvsendmail` y `tprvinsrp0002`, que ningún punto de entrada alcanza. Es candidata a entrar al alcance, porque es parte del ciclo de vida del usuario proveedor.
- **Los `hprvp*` parecen ser otro subsistema** con el mismo prefijo (se llaman entre sí y desde `acpshookdummycalls`).
- **Los `rprvir*` sin la `a` son stubs:** el reporte que corre es `arprvir*`, que sí queda dentro.
- Hay objetos que nadie referencia: son candidatos a código muerto.

La columna `Cobertura` (CA3) se completa al final (G1).

## Dentro del módulo (149)

| Objeto | Punto de entrada |
|---|---|
| `apprvir03` |  |
| `apprvp002` |  |
| `arprvir02` |  |
| `arprvir10` |  |
| `arprvir11` |  |
| `arprvir14` |  |
| `arprvir14m` |  |
| `arprvir53` |  |
| `arprvir54` |  |
| `arprvir88` |  |
| `arprvir89` |  |
| `arprvir91` |  |
| `hprvir02` | sí |
| `hprvir03` |  |
| `hprvir06` | sí |
| `hprvir07` | sí |
| `hprvir09` | sí |
| `hprvir10` | sí |
| `hprvir12` |  |
| `hprvir17m` | sí |
| `hprvir18` | sí |
| `hprvir19` |  |
| `hprvir19p` |  |
| `hprvir20` |  |
| `hprvir21` |  |
| `hprvir22` | sí |
| `hprvir23` |  |
| `hprvir24` |  |
| `hprvir25` |  |
| `hprvir27` |  |
| `hprvir28` |  |
| `hprvir28m` |  |
| `hprvir29` |  |
| `hprvir30` |  |
| `hprvir31` |  |
| `hprvir32` |  |
| `hprvir33` |  |
| `hprvir35` |  |
| `hprvir36` |  |
| `hprvir37` |  |
| `hprvir38` |  |
| `hprvir39` | sí |
| `hprvir40` |  |
| `hprvir41` | sí |
| `hprvir42` | sí |
| `hprvir44` |  |
| `hprvir45` |  |
| `hprvir46` |  |
| `hprvir50` |  |
| `hprvir51` |  |
| `hprvir51b` |  |
| `hprvir52` |  |
| `hprvir53` |  |
| `hprvir54` |  |
| `hprvir55` |  |
| `hprvir56` |  |
| `hprvir74` |  |
| `hprvir75` |  |
| `hprvir76` |  |
| `hprvir77` |  |
| `hprvir78` |  |
| `hprvir80` |  |
| `hprvir81` |  |
| `hprvir82` |  |
| `hprvir83` |  |
| `popro001` | sí |
| `pprvir02` |  |
| `pprvir03` |  |
| `pprvir04` |  |
| `pprvir04p` |  |
| `pprvir05` |  |
| `pprvir09` |  |
| `pprvir12` |  |
| `pprvir13` |  |
| `pprvir15` |  |
| `pprvir16b` |  |
| `pprvir17` |  |
| `pprvir21m` |  |
| `pprvir23` |  |
| `pprvir25` |  |
| `pprvir25m` |  |
| `pprvir26` |  |
| `pprvir27` |  |
| `pprvir28` |  |
| `pprvir29` |  |
| `pprvir34` |  |
| `pprvir35` |  |
| `pprvir36` |  |
| `pprvir38` |  |
| `pprvir39` |  |
| `pprvir40` |  |
| `pprvir44` |  |
| `pprvir45` |  |
| `pprvir46` |  |
| `pprvir48` |  |
| `pprvir49` |  |
| `pprvir50` |  |
| `pprvir51` |  |
| `pprvir53` |  |
| `pprvir54` |  |
| `pprvir55` |  |
| `pprvir56` |  |
| `pprvir62` |  |
| `pprvir64` |  |
| `pprvir65` |  |
| `pprvir67` |  |
| `pprvir68` |  |
| `pprvir70` |  |
| `pprvir71` |  |
| `pprvir72` |  |
| `pprvir74` |  |
| `pprvir75` |  |
| `pprvir76` |  |
| `pprvir77` |  |
| `pprvir79` |  |
| `pprvir80` |  |
| `pprvir81` |  |
| `pprvir82` |  |
| `pprvir83` |  |
| `pprvir84` |  |
| `pprvir86` |  |
| `pprvir87` |  |
| `pprvir88` |  |
| `pprvir90` |  |
| `pprvir99` |  |
| `pprvp002` |  |
| `pprvp009` |  |
| `pprvperfildoc` |  |
| `pprvperfildoc002` |  |
| `pprvsendmsg` |  |
| `rprvir28` |  |
| `rprvir44` |  |
| `rprvir52` |  |
| `rprvir56` |  |
| `rprvir59` |  |
| `rprvir63` |  |
| `rprvir94` |  |
| `rprvir95` |  |
| `tprvbco` |  |
| `tprvdom` |  |
| `tprvesp` |  |
| `tprvinsreg001` |  |
| `tprvinsrp` | sí |
| `tprvinsrp0001` |  |
| `tprvperfildoc` |  |
| `tprvpj` |  |
| `tprvpod` |  |
| `tprvrpr` |  |
| `tprvrub` |  |

## Puntos de contacto (70)

| Objeto | Lo referencian |
|---|---|
| `acpschecksumfile` | `pprvperfildoc002` |
| `acpsdmgetcontentdownloadlink` | `hprvir44` |
| `acpsgetattributevalue` | `hprvir46` |
| `acpsgetgxtempmediadirectory` | `hprvir56`, `rprvir44` |
| `acpsgetsiscod` | `pprvir99`, `pprvsendmsg`, `tprvinsrp0001` |
| `acpsgetsysattvalue` | `arprvir02`, `hprvir02`, `hprvir09`, `hprvir10`, `hprvir22`, `hprvir25`, `hprvir44`, `hprvir45`, `tprvinsrp0001` |
| `acpsgetsystemattvalue` | `arprvir10`, `arprvir14m` |
| `acpsgetuserattvalue` | `tprvinsrp0001` |
| `acpsgetvarparameter` | `arprvir10`, `hprvir02`, `hprvir31`, `hprvir44`, `tprvinsrp0001` |
| `acpsgetwebapptempmediadirectory` | `hprvir44`, `hprvir56` |
| `acpshttpdownloadfile` | `hprvir44` |
| `acpslistmessages` | `hprvir23`, `hprvir38`, `hprvir45`, `pprvsendmsg`, `tprvinsrp` |
| `acpslistmessageswithformat` | `hprvir09` |
| `acpsopenaspopup` | `hprvir02`, `hprvir09`, `hprvir10`, `hprvir19`, `hprvir25`, `hprvir31`, `hprvir40`, `hprvir45`, `hprvir55`, `hprvir56`, `hprvir82`, `hprvir83` |
| `acpsrcrudmessages` | `pprvsendmsg` |
| `acpsrcrudusers` | `tprvinsrp0001` |
| `acpsrdeliveremail` | `pprvir99` |
| `acpsrdmapplytemplate` | `arprvir10` |
| `acpsrgetdmdocuments` | `hprvir44` |
| `acpsrinsertdmdocumentversion` | `pprvperfildoc002` |
| `acpssenddmdocumentattachment` | `pprvperfildoc002` |
| `acpsurldissect` | `hprvir44` |
| `appmasterpage` | `hprvir03`, `hprvir19`, `hprvir19p`, `hprvir21`, `hprvir23`, `hprvir24`, `hprvir25`, `hprvir27`, `hprvir28`, `hprvir28m`, `hprvir31`, `hprvir33`, `hprvir35`, `hprvir36`, `hprvir38`, `hprvir40`, `hprvir44`, `hprvir45`, `hprvir46`, `hprvir50`, `hprvir51b`, `hprvir52`, `hprvir53`, `hprvir54`, `hprvir55`, `hprvir56`, `hprvir74`, `hprvir75`, `hprvir76`, `hprvir77`, `hprvir81`, `hprvir83`, `popro001` |
| `crontabauthorizeuser` | `hprvir02`, `tprvinsrp0001` |
| `gelocalid04` | `hprvir17m`, `hprvir19`, `hprvir19p` |
| `gelocalid05` | `hprvir17m`, `hprvir19`, `hprvir19p` |
| `gelocalid06` | `hprvir17m`, `hprvir19`, `hprvir19p` |
| `gempprvir` | `hprvir02`, `hprvir06`, `hprvir07`, `hprvir09`, `hprvir10`, `hprvir17m`, `hprvir18`, `hprvir20`, `hprvir22`, `hprvir39`, `hprvir41`, `hprvir42`, `tprvbco`, `tprvdom`, `tprvesp`, `tprvinsrp`, `tprvperfildoc`, `tprvpj`, `tprvpod`, `tprvrpr`, `tprvrub` |
| `genbrd0006` | `arprvir11`, `arprvir14m`, `rprvir95` |
| `genmon0002` | `tprvbco` |
| `genuprm01` | `arprvir11`, `tprvbco` |
| `genuprm02` | `arprvir14m` |
| `gxdomaingenivasituacion` | `arprvir14` |
| `gxdomaingenprodomtip` | `arprvir11`, `arprvir14`, `arprvir14m`, `hprvir41`, `hprvir51b` |
| `hcadm001` | `popro001` |
| `hccat023` | `hprvir03` |
| `hcgtu001` | `hprvir31` |
| `hcof0027` | `hprvir55` |
| `hnupro16m` | `hprvir21` |
| `hnupro19` | `hprvir03` |
| `hnupro39` | `hprvir03` |
| `htpropodhistorian` | `pprvir27` |
| `htprovehistorian` | `pprvir27`, `pprvir50` |
| `loadcontext` | `arprvir02`, `arprvir10`, `arprvir11`, `arprvir14m`, `hprvir02`, `hprvir09`, `hprvir10`, `hprvir22`, `hprvir25`, `hprvir31`, `hprvir39`, `hprvir40`, `hprvir44`, `hprvir45`, `hprvir46`, `hprvir56`, `popro001`, `pprvir04`, `pprvir04p`, `pprvir99`, `rprvir44`, `rprvir95`, `tprvinsreg001`, `tprvinsrp` |
| `loginprov001` | `hprvir35`, `hprvir39` |
| `pcadm003` | `hprvir03`, `hprvir27`, `hprvir31`, `hprvir33`, `hprvir38`, `hprvir40`, `hprvir74`, `hprvir77`, `hprvir83` |
| `pcmsg001` | `pprvir65`, `tprvinsrp0001` |
| `pli00015` | `hprvir56`, `rprvir95` |
| `pli00051` | `hprvir53`, `hprvir74`, `hprvir77`, `hprvir80` |
| `pnunro02` | `pprvir27` |
| `pnunro05` | `pprvir38` |
| `pnupro01` | `pprvir27`, `pprvir38` |
| `pnupro03` | `arprvir91` |
| `pnupro04` | `hprvir02`, `tprvinsrp`, `tprvpj` |
| `promptbco` | `tprvbco` |
| `promptbcosuc` | `tprvbco` |
| `promptloc` | `hprvir17m`, `tprvdom`, `tprvpod`, `tprvrpr` |
| `promptmasterpage` | `hprvir12` |
| `promptpaises` | `hprvir17m`, `tprvdom`, `tprvpod`, `tprvrpr` |
| `promptperdoc` | `hprvir44` |
| `promptprovin` | `hprvir17m`, `hprvir19`, `hprvir19p`, `tprvdom`, `tprvpod`, `tprvrpr` |
| `promptrub` | `hprvir56` |
| `prvir28` | `hprvir19p` |
| `prvperfildoc` | `hprvir44` |
| `prvperfildoc002` | `hprvir44` |
| `pseg0008` | `hprvir27`, `hprvir32`, `hprvir33`, `hprvir38`, `hprvir74`, `hprvir77`, `hprvir83` |
| `rcoc5003` | `hprvir19p` |
| `rgxpencriptaprv` | `pprvir09`, `pprvp009`, `tprvinsrp` |
| `rnupro75` | `pprvir27`, `pprvir50` |
| `wwtprvhis01` | `hprvir23`, `hprvir25`, `hprvir31` |

## Entradas externas (30)

| Objeto | Referencia a |
|---|---|
| `acpshookdummycalls` | `hprvir02`, `hprvir03`, `hprvir21`, `hprvir39`, `popro001` |
| `cm0145` | `pprvir99` |
| `crontab0020` | `pprvir54`, `pprvir56` |
| `gempprvir` | `hprvir02`, `hprvir21` |
| `hcadm001` | `popro001` |
| `hccat023` | `hprvir03` |
| `hcgtu001` | `hprvir31` |
| `hcof0006` | `hprvir39` |
| `hli00010` | `hprvir12` |
| `hli00010p` | `hprvir12` |
| `hli00014` | `pprvir99` |
| `hnupro16` | `tprvinsreg001` |
| `hnupro16m` | `tprvinsreg001` |
| `hnupro19` | `hprvir03` |
| `hnupro39` | `hprvir03` |
| `loginprov` | `hprvir02` |
| `mainmenuwidgetproveedores` | `hprvir21` |
| `oficina` | `pprvir39` |
| `tjuzgados` | `pprvir39` |
| `tprodom` | `pprvir39` |
| `tpropod` | `pprvir13`, `pprvir39` |
| `tprorpr` | `pprvir13`, `pprvir39` |
| `tprove` | `pprvir39` |
| `tprovrub` | `hprvir12` |
| `wsgenerarprov` | `pprvir13` |
| `wsgenerarprovnew` | `pprvir13` |
| `wsgenerarprovnocommit` | `pprvir13` |
| `wwtlioftasm` | `tprvinsreg001` |
| `wwtlioftasm1` | `tprvinsreg001` |
| `wwtlioftasmej` | `tprvinsreg001` |

## Borde: familia fuera de la clausura (68)

| Objeto | Lo referencian |
|---|---|
| `apprvir32` | `pprvir32` |
| `apprvp003` | `pprvp003` |
| `apprvp007` | `pprvp007` |
| `arprvir55` | (nadie) |
| `arprvir57` | (nadie) |
| `arprvir58` | (nadie) |
| `arprvp506` | (nadie) |
| `hprvir04` | (nadie) |
| `hprvir16` | (nadie) |
| `hprvir26` | (nadie) |
| `hprvir34` | `hcoc0002`, `hcoc0003`, `hnupro19`, `hnupro40` |
| `hprvir42m` | `hnupro16m` |
| `hprvir47` | `wwdoctrngar` |
| `hprvir48` | `wwdoctrn` |
| `hprvir79` | (nadie) |
| `hprvirpp` | `lipc022` |
| `hprvp001` | `hprvp009`, `hprvp043` |
| `hprvp002` | `acpshookdummycalls` |
| `hprvp009` | `hprvp002`, `hprvp044` |
| `hprvp010` | `hprvp009` |
| `hprvp012` | (nadie) |
| `hprvp025` | `hprvp002`, `hprvp042` |
| `hprvp026` | `hprvp009` |
| `hprvp030` | `hprvp002`, `hprvp043` |
| `hprvp042` | (nadie) |
| `hprvp043` | `hprvp042` |
| `hprvp044` | `acpshookdummycalls` |
| `hprvp045` | `hprvp010` |
| `hprvp046` | `hprvp042` |
| `pprvcm01` | `hnupro16`, `hprvirpp`, `lipc019m`, `lipc022` |
| `pprvcm02` | `hnupro16`, `hnupro16m` |
| `pprvir06` | `hnupro16m` |
| `pprvir088` | `dis0067`, `geche0009`, `gegto0005`, `gemig0009`, `gemig0018`, `gemig0025`, `gemig0032`, `geopa036`, `geopa037`, `geopa038`, `invca010`, `invcc001`, `rinv0066`, `tgtofac`, `tinvcargo`, `wlibdeuda`, `wtprovedato` |
| `pprvir10` | `geche0000`, `gegto0005` |
| `pprvir32` | (nadie) |
| `pprvir41` | `tprove`, `tprove006`, `tprovebc` |
| `pprvir42` | `pprvir43`, `tprove`, `tprove006`, `tprovebc` |
| `pprvir43` | `tprovrub` |
| `pprvir47` | `exportwwdoctrn`, `hprvir47`, `hprvir48`, `wcdoctrn`, `wwdoctrn`, `wwdoctrngar` |
| `pprvir52` | `acpshookdmaftercruddocument`, `cm0097`, `lipc017m` |
| `pprvir78` | `hprvir79` |
| `pprvp003` | (nadie) |
| `pprvp007` | (nadie) |
| `pprvp010` | `geopa037` |
| `pprvperfildoc001` | `lipc021`, `prvperfildoc` |
| `pprvsendmail` | `loginrecuperarpwd` |
| `rprvir02` | (nadie) |
| `rprvir10` | (nadie) |
| `rprvir11` | (nadie) |
| `rprvir14` | (nadie) |
| `rprvir14m` | (nadie) |
| `rprvir53` | (nadie) |
| `rprvir54` | (nadie) |
| `rprvir55` | (nadie) |
| `rprvir57` | (nadie) |
| `rprvir58` | (nadie) |
| `rprvir88` | (nadie) |
| `rprvir89` | (nadie) |
| `rprvir91` | (nadie) |
| `rprvir93` | `cofdet`, `tcofede` |
| `rprvir96` | `cm0135` |
| `rprvnohab` | (nadie) |
| `rprvp506` | (nadie) |
| `rprvp510` | `hprvp025` |
| `tprvhis` | (nadie) |
| `tprvinsrp0002` | `loginrecuperarpwd` |
| `tprvlicfav` | (nadie) |
| `tprvzon` | `wwtprvzon` |

