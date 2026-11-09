# Dependencias que faltan en el export

Objetos que el código del export **llama** y que **no vienen** en el export (CA4), sacados de las llamadas en el código y no de `ObjectsIdentityMapping`, que no registra el código comentado. Se separan las llamadas **activas** de las que están **solo en comentarios**. La columna `fuente` dice de dónde sale lo que se documenta de cada uno (CA5).

Comando, desde la raíz del repo:

```
python3 -I docs/herramientas/dependencias-xpz.py ../genfin-gx-extraido/xpz/GENFin-RegProv.xml --detalle
```

Controles del script (todos pasaron el 2026-10-23): `TPrvESP` en activas, `RPrvIR63` en comentadas, `HPrvIR42` y `StrReplace` ausentes. `probar.py` comprueba que cada uno pueda fallar.

El sistema **PROVE** (padrón externo) que nombra la rev2 §16 no aparece como objeto llamado: lo consulta algún procedimiento de la lista. Se busca al documentar `integraciones.md`.

## Activas (40)

| Objeto | Llamadas | Desde (objeto, parte, evento) | Fuente | En la rev2 §16 |
|---|---|---|---|---|
| `ACPSGEtSysAttValue` | 4 | HPrvIR02 Events Event Start; HPrvIR09 Events Event Start; HPrvIR10 Events Event Start; HPrvIR22 Events Event Start | `fin/acpsgetsysattvalue.java` | — |
| `ACPSGetVarParameter` | 1 | HPrvIR02 Events Event Start | `fin/acpsgetvarparameter.java` | — |
| `ACPSListMessages` | 1 | TPrvInsRP Rules (inicio) | `fin/acpslistmessages.java` | — |
| `ACPSOpenAsPopUp` | 5 | HPrvIR02 Events Event 'Anexo1'; HPrvIR09 Events Event 'Formulario'; HPrvIR09 Events Event 'Solicitud'; HPrvIR10 Events Event 'Anexo2'; HPrvIR10 Events Event 'Solicitud' | `fin/acpsopenaspopup.java` | — |
| `CronTabAuthorizeUser` | 1 | HPrvIR02 Events Event Start | `fin/crontabauthorizeuser.java` | — |
| `GELocalid04` | 1 | HPrvIR17m Events Sub 'Pais' | `fin/gelocalid04.java` | — |
| `GELocalid05` | 1 | HPrvIR17m Events Sub 'Provincia' | `fin/gelocalid05.java` | — |
| `GELocalid06` | 1 | HPrvIR17m Events Sub 'Localidad' | `fin/gelocalid06.java` | — |
| `HPrvIR39` | 5 | HPrvIR06 Events Event 'Volver'; HPrvIR22 Events Event 'Volver'; HPrvIR41 Events Event 'Volver'; HPrvIR42 Events Event 'Volver'; TPrvInsRP Events Event After | `fin/hprvir39_impl.java` | sí |
| `LoadContext` | 5 | HPrvIR02 Events Event Start; HPrvIR09 Events Event Start; HPrvIR10 Events Event Start; HPrvIR22 Events Event Start; TPrvInsRP Events Event Start | `fin/loadcontext.java` | — |
| `PNuPro04` | 2 | HPrvIR02 Events Event 'Siguiente'; TPrvInsRP Rules (inicio) | `fin/pnupro04.java` | sí |
| `PPrvIR02` | 1 | HPrvIR02 Events Event 'Siguiente' | `fin/pprvir02.java` | sí |
| `PPrvIR03` | 1 | HPrvIr07 Events Event Start | `fin/pprvir03.java` | — |
| `PPrvIR05` | 1 | HPrvIR02 Events Sub 'getUsuario' | `fin/pprvir05.java` | — |
| `PPrvIR09` | 1 | HPrvIr07 Events Event 'Siguiente' | `fin/pprvir09.java` | — |
| `PPrvIR13` | 2 | HPrvIR17m Events Event 'Aceptar'; HPrvIR17m Events Event 'Siguiente' | `fin/pprvir13.java` | — |
| `PPrvIR16b` | 1 | HPrvIR09 Events Event 'Confirmar' | `fin/pprvir16b.java` | sí |
| `PPrvIR17` | 1 | HPrvIR17m Events Event Start | `fin/pprvir17.java` | — |
| `PPrvIR21m` | 3 | HPrvIR17m Events Event 'Aceptar'; HPrvIR17m Events Event 'Agregar'; HPrvIR17m Events Event 'Siguiente' | `fin/pprvir21m.java` | — |
| `PPrvIR23` | 2 | HPrvIR18 Events Event Refresh; HPrvIR18 Events Event Start | `fin/pprvir23.java` | sí |
| `PPrvIR25m` | 1 | HPrvIR17m Events Event Start | `fin/pprvir25m.java` | — |
| `PPrvIR26` | 2 | HPrvIR17m Events Event 'Aceptar'; HPrvIR17m Events Event 'Siguiente' | `fin/pprvir26.java` | — |
| `PPrvIR39` | 1 | TPrvInsRP Rules (inicio) | `fin/pprvir39.java` | sí |
| `PPrvIR53` | 1 | TPrvInsRP Rules (inicio) | `fin/pprvir53.java` | sí |
| `PPrvIR62` | 5 | HPrvIR17m Events Event Start; HPrvIR18 Events Event Refresh; HPrvIR18 Events Event Start; HPrvIR41 Events Event Start; HPrvIR42 Events Event Start | `fin/pprvir62.java` | sí |
| `PPrvIR88` | 1 | TPrvInsRP Rules (inicio) | `fin/pprvir88.java` | sí |
| `PPrvSendMsg` | 2 | HPrvIR09 Events Event 'Confirmar'; TPrvInsRP Events Event After | `fin/pprvsendmsg.java` | — |
| `RGXPEncriptaPrv` | 1 | TPrvInsRP Rules (inicio) | `fin/rgxpencriptaprv.java` | — |
| `RPrvIR02` | 1 | HPrvIR02 Events Event 'Anexo1' | `fin/rprvir02.java` | — |
| `RPrvIR10` | 1 | HPrvIR10 Events Event 'Anexo2' | `fin/rprvir10.java` | sí |
| `RPrvIR11` | 1 | HPrvIR09 Events Event 'Formulario' | `fin/rprvir11.java` | sí |
| `RPrvIR14` | 1 | HPrvIR09 Events Event 'Solicitud' | `fin/rprvir14.java` | sí |
| `RPrvIR14m` | 1 | HPrvIR10 Events Event 'Solicitud' | `fin/rprvir14m.java` | sí |
| `TPrvBco` | 3 | HPrvIR22 Events Event 'Agregar'; HPrvIR22 Events Event 'Eliminar'; HPrvIR22 Events Event 'Modificar' | `fin/tprvbco_impl.java` | sí |
| `TPrvDom` | 3 | HPrvIR41 Events Event 'Agregar'; HPrvIR41 Events Event 'Eliminar'; HPrvIR41 Events Event 'Modificar' | `fin/tprvdom_impl.java` | sí |
| `TPrvESP` | 3 | HPrvIR18 Events Event 'Agregar'; HPrvIR18 Events Event 'Eliminar'; HPrvIR18 Events Event 'Modificar' | `fin/tprvesp_impl.java` | sí |
| `TPrvInsRP0001` | 1 | TPrvInsRP Rules (inicio) | `fin/tprvinsrp0001.java` | sí |
| `TPrvPJ` | 3 | HPrvIR17m Events Event 'Agregar'; HPrvIR17m Events Event 'Eliminar'; HPrvIR17m Events Event 'Modificar' | `fin/tprvpj_impl.java` | sí |
| `TPrvRpr` | 3 | HPrvIR06 Events Event 'Agregar'; HPrvIR06 Events Event 'Eliminar'; HPrvIR06 Events Event 'Modificar' (también en comentario: 1) | `fin/tprvrpr_impl.java` | sí |
| `TPrvRub` | 2 | HPrvIR42 Events Event 'Agregar'; HPrvIR42 Events Event 'Eliminar' (también en comentario: 1) | `fin/tprvrub_impl.java` | sí |

## Solo en comentarios (4)

| Objeto | Llamadas | Desde (objeto, parte, evento) | Fuente | En la rev2 §16 |
|---|---|---|---|---|
| `HPrvIR21` | 6 | HPrvIR06 Events Event 'Volver'; HPrvIR17m Events Sub 'perfilMenu'; HPrvIR18 Events Event 'Volver'; HPrvIR41 Events Event 'Volver'; HPrvIR42 Events Event 'Volver'; TPrvInsRP Events Event After | `fin/hprvir21_impl.java` | sí |
| `PPrvIR01` | 1 | HPrvIR02 Events Event 'Siguiente' | ninguna → **hueco** | — |
| `Pprvir07` | 1 | HPrvIr07 Events Event 'Siguiente' | ninguna → **hueco** | — |
| `RPrvIR63` | 1 | HPrvIR18 Events Event 'Siguiente' | `fin/rprvir63.java` | sí |

## Cruce con la rev2

Objetos de la §16 de la rev2 que no aparecen en ninguna de las dos listas: ninguno.

Los dos objetos sin fuente (`PPrvIR01` y `Pprvir07`) solo se llaman desde comentarios. No existen en `fin/`: es código muerto que nombra objetos que ya no están.
