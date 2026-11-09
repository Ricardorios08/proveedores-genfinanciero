#!/usr/bin/env python3
"""Cuenta los objetos y atributos de un export GeneXus (XML extraído del .xpz).

Uso:
    python3 -I docs/herramientas/contar-xpz.py <export.xml> [--listar]

Cuenta solo los hijos directos de <Objects> y de <Attributes> ("primer nivel").
Con --listar imprime además una fila por objeto: nombre, tipo y versionDate.

Control: el export del módulo (GENFin-RegProv.xpz, leído el 2026-10-19) tiene
119 objetos y 194 atributos. Si el total no coincide, termina con código 1.
Si llega otro export, se actualizan ESPERADO_* a mano diciendo por qué.
"""
import collections
import sys
import xml.etree.ElementTree as ET

ESPERADO_OBJETOS = 119
ESPERADO_ATRIBUTOS = 194

# GUID de tipo de objeto GeneXus -> nombre legible.
TIPOS = {
    "c9584656-94b6-4ccd-890f-332d11fc2c25": "WebPanel",
    "1db606f2-af09-4cf9-a3b5-b481519d28f6": "Transaction",
    "84a12160-f59b-4ad7-a683-ea4481ac23e9": "Procedure",
    "447527b5-9210-4523-898b-5dccb17be60a": "SDT",
    "00972a17-9975-449e-aab1-d26165d51393": "Domain",
    "857ca50e-7905-0000-0007-c5d9ff2975ec": "Table",
}


def contar(ruta):
    raiz = ET.parse(ruta).getroot()
    objetos = raiz.find("Objects")
    atributos = raiz.find("Attributes")
    if objetos is None or atributos is None:
        raise SystemExit(f"{ruta}: no tiene <Objects> o <Attributes> bajo la raíz")
    filas = []
    for o in objetos:
        if o.tag != "Object":
            continue
        guid = o.get("type", "")
        filas.append((o.get("name", ""), TIPOS.get(guid, f"desconocido:{guid}"), o.get("versionDate", "")[:10]))
    n_atributos = sum(1 for a in atributos if a.tag == "Attribute")
    return filas, n_atributos


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    filas, n_atributos = contar(args[0])

    por_tipo = collections.Counter(tipo for _, tipo, _ in filas)
    print("Objetos por tipo:")
    for tipo, n in sorted(por_tipo.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {tipo:<12} {n}")
    print(f"Total objetos:   {len(filas)}")
    print(f"Total atributos: {n_atributos}")

    if "--listar" in argv:
        print("\nnombre\ttipo\tversionDate")
        for nombre, tipo, fecha in sorted(filas, key=lambda f: (f[1], f[0].lower())):
            print(f"{nombre}\t{tipo}\t{fecha}")

    if (len(filas), n_atributos) != (ESPERADO_OBJETOS, ESPERADO_ATRIBUTOS):
        print(
            f"\nCONTROL FALLIDO: se esperaban {ESPERADO_OBJETOS} objetos y "
            f"{ESPERADO_ATRIBUTOS} atributos; se contaron {len(filas)} y {n_atributos}.",
            file=sys.stderr,
        )
        return 1
    print("\nControl: OK (coincide con el conteo del 2026-10-19)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
