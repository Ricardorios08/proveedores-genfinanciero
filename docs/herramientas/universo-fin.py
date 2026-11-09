#!/usr/bin/env python3
"""Calcula el universo del módulo Registro de Proveedores dentro del Java generado.

Uso:
    python3 -I docs/herramientas/universo-fin.py <dir fin/> [--markdown]

Regla de frontera (diseño, "Frontera del módulo"):
  - dentro del módulo: la clausura de referencias desde los puntos de entrada
    (los 11 paneles del alta, hprvir39 y popro001), siguiendo solo objetos de la
    familia hprv*, pprv*, tprv*, rprv* y popro*, con una "a" opcional adelante
    (arprv* son reportes; apprv* son procedimientos generados como programa);
  - punto de contacto: cualquier otro objeto que el módulo referencie;
  - entrada externa: objetos de fuera de la familia que referencian al módulo;
  - borde: objetos de la familia que la clausura NO alcanza, con quién los
    referencia. Se revisan a mano: pueden ser de otro subsistema con el mismo
    prefijo, código muerto, o parte del módulo a la que se entra por otro lado
    (por ejemplo la recuperación de clave).

Una referencia es cualquier `com.fin.<nombre>` en el archivo: `new com.fin.x(` en
llamadas a procedimientos, y "com.fin.x" en enlaces a paneles. Los nombres se
normalizan (sin `_impl`, `__default`, `_bc`) y solo cuentan si existe el archivo.

Controles (si alguno falla, termina con código 1): hprvir21 y pprvir50 quedan
dentro; loginprov (el login del proveedor) queda en entradas externas; y
pprvsendmail queda en el borde, referenciado por loginrecuperarpwd. El control
original esperaba loginrecuperarpwd como entrada externa: falló el 2026-10-23
porque solo llama a objetos del borde (pprvsendmail, tprvinsrp0002).
"""
import collections
import pathlib
import re
import sys

ENTRADAS = [
    "hprvir02", "hprvir07", "tprvinsrp", "hprvir17m", "hprvir41", "hprvir18",
    "hprvir42", "hprvir06", "hprvir22", "hprvir10", "hprvir09", "hprvir39", "popro001",
]
# Prefijo "a" opcional: GeneXus genera con una "a" adelante los reportes
# (RPrvIR10 en el XPZ es com.fin.arprvir10) y los procedimientos que también
# corren como programa principal (pprvir03.java es un envoltorio que llama a
# com.fin.apprvir03, donde está el código real).
FAMILIA = re.compile(r"^a?(hprv|pprv|tprv|rprv|popro)")
RE_REF = re.compile(r"com\.fin\.([a-z0-9_]+)")
SUFIJOS = ("_impl", "__default", "_bc")


def normalizar(nombre):
    cambio = True
    while cambio:
        cambio = False
        for s in SUFIJOS:
            if nombre.endswith(s):
                nombre, cambio = nombre[: -len(s)], True
    return nombre


def indexar(fin):
    """objeto -> lista de archivos .java que lo implementan."""
    archivos = collections.defaultdict(list)
    for p in fin.glob("*.java"):
        archivos[normalizar(p.stem.lower())].append(p)
    return archivos


def referencias(archivos, objeto, conocidos):
    refs = set()
    for p in archivos[objeto]:
        texto = p.read_text(encoding="utf-8", errors="replace")
        for m in RE_REF.finditer(texto):
            n = normalizar(m.group(1).lower())
            if n != objeto and n in conocidos:
                refs.add(n)
    return refs


def calcular(fin):
    archivos = indexar(fin)
    conocidos = set(archivos)
    faltan = [e for e in ENTRADAS if e not in conocidos]
    if faltan:
        raise SystemExit(f"puntos de entrada sin archivo en {fin}: {faltan}")

    modulo, contacto = set(), collections.defaultdict(set)
    pendientes = list(ENTRADAS)
    while pendientes:
        o = pendientes.pop()
        if o in modulo:
            continue
        modulo.add(o)
        for r in referencias(archivos, o, conocidos):
            if FAMILIA.match(r):
                if r not in modulo:
                    pendientes.append(r)
            else:
                contacto[r].add(o)

    externas = collections.defaultdict(set)
    patron = re.compile(r"com\.fin\.(" + "|".join(sorted(modulo, key=len, reverse=True)) + r")(?:_impl|__default|_bc)?\b")
    for o, ps in archivos.items():
        if FAMILIA.match(o) or o in modulo:
            continue
        for p in ps:
            for m in patron.finditer(p.read_text(encoding="utf-8", errors="replace")):
                externas[o].add(m.group(1))
    borde = collections.defaultdict(set)
    fuera = [o for o in archivos if FAMILIA.match(o) and o not in modulo]
    if fuera:
        patron_b = re.compile(r"com\.fin\.(" + "|".join(sorted(fuera, key=len, reverse=True)) + r")(?:_impl|__default|_bc)?\b")
        for o, ps in archivos.items():
            for p in ps:
                for m in patron_b.finditer(p.read_text(encoding="utf-8", errors="replace")):
                    if m.group(1) != o:
                        borde[m.group(1)].add(o)
        for o in fuera:
            borde.setdefault(o, set())
    # Un objeto que el módulo llama y que también llama al módulo es contacto y externo a la vez.
    return modulo, contacto, externas, borde


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    modulo, contacto, externas, borde = calcular(pathlib.Path(args[0]))

    if "--markdown" in argv:
        print(f"## Dentro del módulo ({len(modulo)})\n")
        print("| Objeto | Punto de entrada |\n|---|---|")
        for o in sorted(modulo):
            print(f"| `{o}` | {'sí' if o in ENTRADAS else ''} |")
        print(f"\n## Puntos de contacto ({len(contacto)})\n")
        print("| Objeto | Lo referencian |\n|---|---|")
        for o in sorted(contacto):
            print(f"| `{o}` | {', '.join(f'`{x}`' for x in sorted(contacto[o]))} |")
        print(f"\n## Entradas externas ({len(externas)})\n")
        print("| Objeto | Referencia a |\n|---|---|")
        for o in sorted(externas):
            print(f"| `{o}` | {', '.join(f'`{x}`' for x in sorted(externas[o]))} |")
        print(f"\n## Borde: familia fuera de la clausura ({len(borde)})\n")
        print("| Objeto | Lo referencian |\n|---|---|")
        for o in sorted(borde):
            refs = ', '.join(f'`{x}`' for x in sorted(borde[o])) or '(nadie)'
            print(f"| `{o}` | {refs} |")
        print()
    else:
        print(f"Dentro del módulo: {len(modulo)}")
        print(f"Puntos de contacto: {len(contacto)}")
        print(f"Entradas externas: {len(externas)}")
        print(f"Borde (familia fuera de la clausura): {len(borde)}")

    fallas = []
    for o in ("hprvir21", "pprvir50"):
        if o not in modulo:
            fallas.append(f"{o} no quedó dentro del módulo")
    if "loginprov" not in externas:
        fallas.append("loginprov no quedó en entradas externas")
    if "loginrecuperarpwd" not in borde.get("pprvsendmail", set()):
        fallas.append("pprvsendmail no quedó en el borde referenciado por loginrecuperarpwd")
    if fallas:
        print("CONTROL FALLIDO: " + "; ".join(fallas), file=sys.stderr)
        return 1
    print("Controles: OK (hprvir21 y pprvir50 dentro, loginprov externa, pprvsendmail en el borde)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
