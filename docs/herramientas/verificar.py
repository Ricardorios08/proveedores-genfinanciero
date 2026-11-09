#!/usr/bin/env python3
"""Verifica docs/ contra las convenciones de registro-proveedores-docs.

Uso:
    python3 -I docs/herramientas/verificar.py [<raíz de docs>]   (por defecto: docs)

Seis chequeos. Cada problema sale en una línea con su código:

  [C1] índice: un archivo de docs/ no figura en README.md, o README.md nombra
       uno que no existe (CA1).
  [C2] gramática: un bloque mal formado, o una afirmación de un archivo de
       comportamiento sin bloque (CA15).
  [C3] estado: el estado escrito no coincide con el calculado desde las capas
       (CA15).
  [C4] clase: una regla R-nn sin clase, o un R-nn repetido (CA22).
  [C5] decisiones: una regla o discrepancia sin su lugar en
       decisiones-rediseno.md, o una marca ≠ D-nn sin entrada (CA14, CA23).
  [C6] csv: columnas de features.csv, evidencia vacía, decision fuera del
       vocabulario o sin DR-nn que la respalde (CA19, CA24).

Termina con 0 si no hay problemas y con 1 si hay alguno. Los bloques dentro de
bloques de código (```) no se leen: ahí van los ejemplos.
"""
import csv
import pathlib
import re
import sys

CAPAS = {"diseño", "código", "ejecución", "intención"}
CLASES = {"esencial", "parche", "accidente"}
COLUMNAS_CSV = ["feature", "area", "priority", "original", "clone", "notes", "capas", "evidencia", "decision"]
DECISIONES = {"mantener", "rediseñar", "eliminar", "pendiente"}

# Archivos de comportamiento: cada ítem de lista de primer nivel y cada fila de
# tabla es una afirmación y lleva bloque.
COMPORTAMIENTO = {
    "modos.md", "modelo-datos.md", "estados.md", "integraciones.md", "mensajes.md",
    "configuracion.md", "cliente-vs-producto.md", "seguridad.md",
}
EXCLUIDOS_INDICE = ("herramientas/fixtures/",)

RE_BLOQUE = re.compile(r"\[([VSD]) · ([^\[\]]*)\]")
RE_BLOQUE_SUELTO = re.compile(r"\[[VSD] ·")
RE_REGLA = re.compile(r"\*\*(R-\d{2,})\*\*")
RE_DREF = re.compile(r"≠ (D-\d{2,})")
RE_SNN = re.compile(r"\bS\d{2,}\b")


def lineas_utiles(texto):
    """Genera (número, línea) saltando los bloques de código cercados."""
    dentro = False
    for n, linea in enumerate(texto.splitlines(), 1):
        if linea.lstrip().startswith("```"):
            dentro = not dentro
            continue
        if not dentro:
            yield n, linea


def parsear_bloque(cuerpo):
    """'capas: a, b · ev: x · clase: y · ≠ D-01' -> dict, o str con el error."""
    campos = {}
    for parte in [p.strip() for p in cuerpo.split(" · ")]:
        if parte.startswith("≠ "):
            if not re.fullmatch(r"≠ D-\d{2,}", parte):
                return f"marca de discrepancia mal formada: '{parte}'"
            campos.setdefault("discrepa", []).append(parte[2:])
            continue
        if ": " not in parte:
            return f"campo sin 'nombre: valor': '{parte}'"
        clave, valor = parte.split(": ", 1)
        campos[clave] = valor.strip()
    if "capas" not in campos or "ev" not in campos:
        return "faltan 'capas' o 'ev'"
    capas = [c.strip() for c in campos["capas"].split(",")]
    malas = [c for c in capas if c not in CAPAS]
    if malas:
        return f"capas inválidas: {malas}"
    if not campos["ev"]:
        return "evidencia vacía"
    if "clase" in campos and campos["clase"] not in CLASES:
        return f"clase inválida: '{campos['clase']}'"
    campos["capas"] = set(capas)
    extra = set(campos) - {"capas", "ev", "clase", "discrepa"}
    if extra:
        return f"campos desconocidos: {sorted(extra)}"
    return campos


def estado_calculado(campos, objetos_ok, pantalla_objeto):
    if campos.get("discrepa"):
        return "D"
    capas = campos["capas"]
    if "código" in capas:
        return "V"
    if "ejecución" in capas:
        pantallas = RE_SNN.findall(campos["ev"])
        objs = {pantalla_objeto.get(s) for s in pantallas}
        if pantallas and None not in objs and objs <= objetos_ok:
            return "V"
    return "S"


def leer_version(raiz):
    """Objetos que pasaron el chequeo de versión (E1): tabla de convenciones.md bajo
    un título que contiene 'Chequeo de versión', cuyo resultado empieza con
    'coincide con Java'. Se exige la frase al principio y no solo la palabra: un
    resultado como 'no discrimina (XPZ y Java coinciden)' no aprueba."""
    ok = set()
    conv = raiz / "convenciones.md"
    if not conv.exists():
        return ok
    en_seccion = False
    for _, linea in lineas_utiles(conv.read_text(encoding="utf-8")):
        if linea.startswith("#"):
            en_seccion = "chequeo de versión" in linea.lower()
            continue
        if en_seccion and linea.startswith("|") and not set(linea) <= set("|-: "):
            celdas = [c.strip().strip("`") for c in linea.strip("|").split("|")]
            if len(celdas) >= 2 and celdas[1].lower().startswith("coincide con java"):
                ok.add(celdas[0].lower())
    return ok


def leer_pantallas(raiz):
    """Snn -> objeto, desde las filas '| Snn | objeto | ...' de pantallas.md."""
    mapa = {}
    p = raiz / "pantallas.md"
    if p.exists():
        for _, linea in lineas_utiles(p.read_text(encoding="utf-8")):
            m = re.match(r"\|\s*(S\d{2,})\s*\|\s*`?([^|`]+?)`?\s*\|", linea)
            if m:
                mapa[m.group(1)] = m.group(2).strip().lower()
    return mapa


def es_afirmacion(linea):
    if linea.startswith("- "):
        return True
    if linea.startswith("|") and not set(linea) <= set("|-: "):
        return True
    return False


def verificar(raiz):
    problemas = []
    archivos = sorted(p for p in raiz.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    # Los fixtures no son parte de docs/: no se indexan ni se verifican.
    rel = {
        r: p for p in archivos
        if not (r := p.relative_to(raiz).as_posix()).startswith(EXCLUIDOS_INDICE)
    }

    # C1 — índice
    readme = raiz / "README.md"
    if not readme.exists():
        problemas.append("[C1] falta README.md")
    else:
        texto = readme.read_text(encoding="utf-8")
        nombrados = set(re.findall(r"\]\(([^)#]+)\)", texto)) | set(re.findall(r"`([\w./-]+\.(?:md|csv|py))`", texto))
        nombrados = {n.removeprefix("./") for n in nombrados}
        for r in rel:
            if r == "README.md" or r.startswith(EXCLUIDOS_INDICE):
                continue
            if r not in nombrados:
                problemas.append(f"[C1] {r} no figura en README.md")
        for n in sorted(nombrados):
            if n not in rel:
                problemas.append(f"[C1] README.md nombra {n}, que no existe")

    objetos_ok = leer_version(raiz)
    pantalla_objeto = leer_pantallas(raiz)
    reglas = {}          # R-nn -> (archivo, clase)
    discrepancias_ref = set()

    # C2, C3, C4 — bloques, estados y reglas
    for r, p in rel.items():
        if p.suffix != ".md":
            continue
        comportamiento = r in COMPORTAMIENTO or r.startswith("pasos/")
        for n, linea in lineas_utiles(p.read_text(encoding="utf-8")):
            bloques = list(RE_BLOQUE.finditer(linea))
            if len(RE_BLOQUE_SUELTO.findall(linea)) != len(bloques):
                problemas.append(f"[C2] {r}:{n} bloque mal cerrado o con corchetes adentro")
            if comportamiento and es_afirmacion(linea) and not bloques and not linea.startswith("| ---"):
                if not _es_encabezado_tabla(p, n):
                    problemas.append(f"[C2] {r}:{n} afirmación sin bloque")
            for b in bloques:
                campos = parsear_bloque(b.group(2))
                if isinstance(campos, str):
                    problemas.append(f"[C2] {r}:{n} {campos}")
                    continue
                calc = estado_calculado(campos, objetos_ok, pantalla_objeto)
                if b.group(1) != calc:
                    problemas.append(f"[C3] {r}:{n} dice {b.group(1)}, corresponde {calc}")
                discrepancias_ref.update(campos.get("discrepa", []))
                m = RE_REGLA.search(linea)
                if m:
                    rid = m.group(1)
                    if rid in reglas:
                        problemas.append(f"[C4] {r}:{n} {rid} repetido (ya en {reglas[rid][0]})")
                    if "clase" not in campos:
                        problemas.append(f"[C4] {r}:{n} {rid} sin clase")
                    reglas[rid] = (r, campos.get("clase"))

    # C5 — decisiones y discrepancias
    dec = raiz / "decisiones-rediseno.md"
    dis = raiz / "discrepancias.md"
    texto_dec = dec.read_text(encoding="utf-8") if dec.exists() else ""
    texto_dis = dis.read_text(encoding="utf-8") if dis.exists() else ""
    entradas_d = set(re.findall(r"^#+\s*(D-\d{2,})\b", texto_dis, re.MULTILINE))
    secciones_dr = _secciones(texto_dec, r"DR-\d{2,}")
    seccion_mantener = _seccion_titulada(texto_dec, "se mantiene")
    for d in sorted(discrepancias_ref - entradas_d):
        problemas.append(f"[C5] la marca ≠ {d} no tiene entrada en discrepancias.md")
    for rid, (archivo, clase) in sorted(reglas.items()):
        en_dr = any(re.search(rf"\b{rid}\b", cuerpo) for cuerpo in secciones_dr.values())
        if clase in ("parche", "accidente") and not en_dr:
            problemas.append(f"[C5] {rid} ({clase}, {archivo}) no tiene DR-nn")
        if clase == "esencial" and not en_dr and not re.search(rf"\b{rid}\b", seccion_mantener):
            problemas.append(f"[C5] {rid} (esencial, {archivo}) no está ni en una DR-nn ni en 'Se mantiene'")
    for d in sorted(entradas_d):
        if not any(re.search(rf"\b{d}\b", cuerpo) for cuerpo in secciones_dr.values()):
            problemas.append(f"[C5] {d} no tiene DR-nn")

    # C6 — features.csv
    fcsv = raiz / "features.csv"
    if fcsv.exists():
        with fcsv.open(encoding="utf-8", newline="") as f:
            lector = csv.reader(f)
            encabezado = next(lector, [])
            if encabezado != COLUMNAS_CSV:
                problemas.append(f"[C6] columnas {encabezado}, se esperaban {COLUMNAS_CSV}")
            else:
                for n, fila in enumerate(lector, 2):
                    if len(fila) != len(COLUMNAS_CSV):
                        problemas.append(f"[C6] features.csv:{n} tiene {len(fila)} columnas")
                        continue
                    v = dict(zip(COLUMNAS_CSV, fila))
                    if not v["evidencia"].strip():
                        problemas.append(f"[C6] features.csv:{n} sin evidencia")
                    if v["decision"] not in DECISIONES:
                        problemas.append(f"[C6] features.csv:{n} decision '{v['decision']}' fuera del vocabulario")
                    elif v["decision"] != "pendiente":
                        refs = re.findall(r"DR-\d{2,}", v["notes"] + " " + v["evidencia"])
                        if not refs or any(x not in secciones_dr for x in refs):
                            problemas.append(f"[C6] features.csv:{n} decision '{v['decision']}' sin DR-nn existente que la respalde")
    return problemas


def _es_encabezado_tabla(p, n):
    """True si la línea n es el encabezado de una tabla (la siguiente es el separador)."""
    lineas = p.read_text(encoding="utf-8").splitlines()
    return n < len(lineas) and set(lineas[n].strip()) <= set("|-: ") and lineas[n].strip().startswith("|")


def _secciones(texto, patron_id):
    """id -> cuerpo, para cada título que empieza con el id."""
    secciones, actual, cuerpo = {}, None, []
    for linea in texto.splitlines():
        m = re.match(rf"^#+\s*({patron_id})\b", linea)
        if m or linea.startswith("#"):
            if actual:
                secciones[actual] = "\n".join(cuerpo)
            actual, cuerpo = (m.group(1) if m else None), []
            continue
        cuerpo.append(linea)
    if actual:
        secciones[actual] = "\n".join(cuerpo)
    return secciones


def _seccion_titulada(texto, titulo):
    cuerpo, dentro = [], False
    for linea in texto.splitlines():
        if linea.startswith("#"):
            dentro = titulo in linea.lower()
            continue
        if dentro:
            cuerpo.append(linea)
    return "\n".join(cuerpo)


def main(argv):
    raiz = pathlib.Path(argv[1] if len(argv) > 1 else "docs")
    if not raiz.is_dir():
        print(f"{raiz}: no es un directorio", file=sys.stderr)
        return 2
    problemas = verificar(raiz)
    for p in problemas:
        print(p)
    print(f"\n{len(problemas)} problema(s) en {raiz}")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
