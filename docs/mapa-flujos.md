# Mapa de flujos

El módulo Registro de Proveedores de un vistazo: el alta en 11 pasos, la entrada según el estado del proveedor, la modificación de datos (modo `P`), la administración (modo `A`) y la habilitación. Los puntos marcados con ⚠ son puntos de dolor: cada uno enlaza a su decisión en [decisiones-rediseno.md](decisiones-rediseno.md).

Todo sale del código, salvo los pasos 1 a 3 del alta y las pantallas de administración, que se observaron en test el 2026-10-23. El detalle de cada paso está en `pasos/`, el de los estados en `estados.md` y el de los modos en `modos.md`.

## Alta y entrada por CUIT

```mermaid
flowchart TD
    P1["Paso 1 · CUIT<br/>HPrvIR02"] -->|flag F, P, A, N o T| P2["Paso 2 · usuario<br/>HPrvIr07<br/>⚠ DR-01 categoría descartada"]
    P1 -->|flag H, Q, G, X u otro| CORTE(["Corta con un mensaje"])
    P1 -->|flag E| P10
    P2 --> P3["Paso 3 · datos principales<br/>TPrvInsRP<br/>graba el perfil y el usuario en Services<br/>⚠ DR-09 clave por correo"]
    P3 -->|persona jurídica| P4["Paso 4 · sociedad<br/>HPrvIR17m<br/>⚠ DR-04 graba antes de validar"]
    P3 -->|persona física| P5
    P4 --> P5["Paso 5 · domicilios<br/>HPrvIR41"]
    P5 --> P6["Paso 6 · situación patrimonial<br/>HPrvIR18<br/>⚠ DR-02 no exige nada"]
    P6 --> P7["Paso 7 · rubros<br/>HPrvIR42"]
    P7 --> P8["Paso 8 · representantes<br/>HPrvIR06"]
    P8 --> P9["Paso 9 · cuentas bancarias<br/>HPrvIR22"]
    P9 --> P10["Paso 10 · imprimir solicitud<br/>HPrvIR10"]
    P10 --> P11["Paso 11 · confirmar<br/>HPrvIR09<br/>⚠ DR-05 pasa a E aunque falle el aviso"]
    P11 --> E(["Estado E · en espera de habilitación"])
    P3 -. "Anterior vuelve al paso 1 · ⚠ DR-03" .-> P1
    P9 -. "Anterior según variable de sesión · ⚠ DR-03" .-> P1
```

## Después del alta: modificación, administración y habilitación

```mermaid
flowchart TD
    E(["E · en espera"]) --> ADM25["Administración · HPrvIR25<br/>lista E y P"]
    ADM25 -->|Habilitar · PPrvIR04| H(["H · habilitado"])
    ADM25 -->|Provisorio o Revertir · PPrvIR04p| PROV(["P · provisoria"])
    PROV --> ADM25
    H --> MENU["Menú del proveedor · HPrvIR39<br/>modo P"]
    MENU -->|edita sus datos| Q(["Q · modificación pendiente<br/>⚠ DR-06 cinco rutas a Q"])
    Q --> ADM40["Administración · HPrvIR40<br/>lista Q y R<br/>exige PrvPAdminGral"]
    ADM40 -->|Habilitar · PPrvIR50| H
    Q -->|Renovar certificado · PPrvIR34<br/>⚠ DR-07 habilita sin revisar| H
    H -->|vence el certificado · APPRVIR32| V(["V · vencido"])
    V -->|Eliminar · HPrvIR27| X(["X · eliminado"])
    PERFIL["Enlace 'Perfil' del portal"] -->|"⚠ DR-08 abre el modo A sin permisos"| ADM21["Administración del perfil · HPrvIR21<br/>modo A<br/>⚠ DR-06 sin constancia ni revisión"]
```

## Puntos de dolor

| Marca | Dónde | Decisión |
|---|---|---|
| ⚠ DR-01 | Paso 1 a paso 2: la categoría se calcula y se descarta | [DR-01](decisiones-rediseno.md) |
| ⚠ DR-02 | Paso 6: no exige ejercicio ni balance | [DR-02](decisiones-rediseno.md) |
| ⚠ DR-03 | "Anterior" en los pasos 3, 5, 8 y 9 | [DR-03](decisiones-rediseno.md) |
| ⚠ DR-04 | Paso 4: graba la sociedad antes de validar | [DR-04](decisiones-rediseno.md) |
| ⚠ DR-05 | Paso 11: el estado cambia aunque falle el aviso | [DR-05](decisiones-rediseno.md) |
| ⚠ DR-06 | Modificación de datos en `P` y en `A` | [DR-06](decisiones-rediseno.md) |
| ⚠ DR-07 | Renovar el certificado habilita un `Q` sin revisión | [DR-07](decisiones-rediseno.md) |
| ⚠ DR-08 | Enlace "Perfil" al modo administración | [DR-08](decisiones-rediseno.md) |
| ⚠ DR-09 | Clave inicial en el correo de bienvenida | [DR-09](decisiones-rediseno.md) |

Las demás decisiones (DR-10 a DR-14) no cambian la secuencia del flujo: son de seguridad, datos de cliente, validaciones duplicadas, mensajería y código muerto.
