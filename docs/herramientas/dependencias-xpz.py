#!/usr/bin/env python3
"""Lista los objetos que el código del export llama y que no vienen en el export.

Uso:
    python3 -I docs/herramientas/dependencias-xpz.py <export.xml> [--detalle]

Lee las partes de código de cada objeto (Events, Rules y Conditions), detecta
las llamadas y les resta los objetos y atributos presentes, más las funciones
y palabras reservadas de GeneXus. Separa:

  - activas:      al menos una llamada fuera de comentarios;
  - comentadas:   todas sus llamadas están dentro de /* */ o después de //.

Formas de llamada reconocidas:
    Obj.Call(  Obj.Popup(  Obj.Link(  Obj.Submit(  Obj.Udp(
    Call(Obj  Link(Obj  Submit(Obj  Popup(Obj      Obj(   (llamada directa)

Controles (CA4 de la propuesta). Si alguno falla, termina con código 1:
  - TPrvESP figura en activas (llamada viva en HPrvIR18);
  - RPrvIR63 figura en comentadas y no en activas;
  - HPrvIR42 no figura (está en el export);
  - StrReplace no figura (es una función nativa y el export la usa). Se eligió
    StrReplace y no Msg porque Msg no pasa el filtro de forma de _parece_objeto:
    su control no podía fallar por la lista NATIVAS (lo mostró probar.py).
Con --sin-control se omiten, para correr sobre fixtures que no son el módulo.
"""
import collections
import re
import sys
import xml.etree.ElementTree as ET

# GUID de parte -> nombre. Solo se leen las partes de código.
PARTES_CODIGO = {
    "c44bd5ff-f918-415b-98e6-aca44fed84fa": "Events",
    "9b0a32a3-de6d-4be1-a4dd-1b85d3741534": "Rules",
    "763f0d8b-d8ac-4db4-8dd4-de8979f2b5b9": "Conditions",
}

# Funciones, comandos y palabras reservadas de GeneXus que se escriben como llamada.
# Se comparan sin distinguir mayúsculas.
NATIVAS = {
    "abs", "accept", "add", "and", "asc", "call", "chr", "color", "commit", "confirm",
    "confirmation", "ctod", "ctot", "date", "day", "default", "defined", "delete", "do",
    "dow", "dtoc", "dtos", "else", "endfor", "endif", "error", "exit", "for", "format",
    "fromstring", "if", "iif", "in", "int", "isempty", "isnull", "len", "link", "load",
    "lower", "ltrim", "minute", "mod", "month", "msg", "new", "newline", "noaccept",
    "not", "now", "null", "nullvalue", "or", "order", "padl", "padr", "parm", "popup",
    "print", "prompt", "random", "refresh", "return", "rollback", "round", "rtrim",
    "serial", "servernow", "serverdate", "servertime", "space", "str", "strreplace",
    "strsearch", "strsearchrev", "submit", "substr", "sum", "count", "max", "min",
    "average", "find", "ttoc", "today", "tostring", "trim", "udp", "upper", "using",
    "val", "when", "where", "while", "year", "ymdtod", "ymdhmstot", "noskip",
    "readonly", "enabled", "visible", "allownulls", "equal", "case", "otherwise",
    "endcase", "sub", "endsub", "event", "endevent", "hour", "second", "addmonths",
    "addyears", "adddays", "ageofyear", "age", "eom", "cmonth", "cdow", "concat",
    "converttostring", "setempty", "settoday", "gettime", "getdate", "isvalid",
    "go", "returnonclick", "refreshcontrols", "sleep", "time", "userid",
    "noprompt", "gxmlines", "gxgetmli",
}

RE_EVENTO = re.compile(r"^\s*(Event\s+(?:'[^']*'|\S+)|Sub\s+'[^']*')", re.IGNORECASE | re.MULTILINE)
RE_METODO = re.compile(r"(?<![&.\w])([A-Za-z_]\w*)\s*\.\s*(Call|Popup|Link|Submit|Udp)\s*\(", re.IGNORECASE)
RE_FUNCION_OBJ = re.compile(r"(?<![&.\w])(Call|Link|Submit|Popup)\s*\(\s*'?([A-Za-z_]\w*)", re.IGNORECASE)
RE_DIRECTA = re.compile(r"(?<![&.\w'\"])([A-Za-z_]\w*)\s*\(")


def mascaras(texto):
    """Devuelve dos listas booleanas del largo del texto: (en_comentario, en_cadena).
    Los literales entre comillas no abren comentarios, y lo que está dentro de una
    cadena no es una llamada (por ejemplo, 'de Compras de OSEP (atención ...')."""
    en_com = [False] * len(texto)
    en_cad = [False] * len(texto)
    i, n = 0, len(texto)
    while i < n:
        c = texto[i]
        if c in "'\"":
            j = texto.find(c, i + 1)
            fin_linea = texto.find("\n", i + 1)
            if j == -1 or (fin_linea != -1 and j > fin_linea):
                j = i  # comilla sin cerrar en la línea: se trata como carácter suelto
            for k in range(i, j + 1):
                en_cad[k] = True
            i = j + 1
        elif texto.startswith("/*", i):
            j = texto.find("*/", i + 2)
            j = n if j == -1 else j + 2
            for k in range(i, j):
                en_com[k] = True
            i = j
        elif texto.startswith("//", i):
            j = texto.find("\n", i)
            j = n if j == -1 else j
            for k in range(i, j):
                en_com[k] = True
            i = j
        else:
            i += 1
    return en_com, en_cad


def evento_en(texto, pos):
    ultimo = "(inicio)"
    for m in RE_EVENTO.finditer(texto, 0, pos):
        ultimo = " ".join(m.group(1).split())
    return ultimo


def llamadas(texto):
    """Genera (nombre, posición, forma) por cada llamada candidata del texto."""
    for m in RE_METODO.finditer(texto):
        yield m.group(1), m.start(1), m.group(2)
    for m in RE_FUNCION_OBJ.finditer(texto):
        yield m.group(2), m.start(2), m.group(1) + "()"
    for m in RE_DIRECTA.finditer(texto):
        yield m.group(1), m.start(1), "directa"


def analizar(ruta):
    raiz = ET.parse(ruta).getroot()
    presentes = set()
    for o in raiz.find("Objects"):
        presentes.add(o.get("name", "").lower())
    for a in raiz.find("Attributes"):
        presentes.add(a.get("name", "").lower())

    # nombre en minúsculas -> {"nombre": forma original, "activa": [...], "comentada": [...]}
    hallazgos = collections.OrderedDict()
    for o in raiz.find("Objects"):
        nombre_obj = o.get("name", "")
        for p in o.findall("Part"):
            parte = PARTES_CODIGO.get(p.get("type"))
            fuente = p.find("Source")
            if parte is None or fuente is None or not fuente.text:
                continue
            texto = fuente.text
            en_com, en_cad = mascaras(texto)
            for nombre, pos, forma in llamadas(texto):
                if en_cad[pos]:
                    continue
                clave = nombre.lower()
                if clave in presentes or clave in NATIVAS:
                    continue
                if forma == "directa" and not _parece_objeto(nombre):
                    continue
                h = hallazgos.setdefault(clave, {"nombre": nombre, "activa": [], "comentada": []})
                donde = f"{nombre_obj} {parte} {evento_en(texto, pos)}"
                (h["comentada"] if en_com[pos] else h["activa"]).append(donde)
    return hallazgos


def _parece_objeto(nombre):
    """Una llamada directa cuenta como objeto solo si el nombre tiene forma de objeto
    de la KB: empieza en mayúscula y tiene al menos otra mayúscula o un dígito
    (PPrvIR39, LoadContext, ACPSGetSysAttValue). Descarta palabras sueltas."""
    if not nombre[0].isupper() or len(nombre) < 4:
        return False
    resto = nombre[1:]
    return any(ch.isupper() or ch.isdigit() for ch in resto)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    hallazgos = analizar(args[0])
    activas = {k: v for k, v in hallazgos.items() if v["activa"]}
    comentadas = {k: v for k, v in hallazgos.items() if not v["activa"]}

    def imprimir(titulo, grupo, campo):
        print(f"## {titulo} ({len(grupo)})")
        for k in sorted(grupo):
            v = grupo[k]
            lugares = sorted(set(v[campo]))
            extra = f" · también en comentario: {len(set(v['comentada']))}" if campo == "activa" and v["comentada"] else ""
            print(f"- {v['nombre']} — {len(lugares)} lugar(es){extra}")
            if "--detalle" in argv:
                for lugar in lugares:
                    print(f"    · {lugar}")
        print()

    imprimir("Activas", activas, "activa")
    imprimir("Solo en comentarios", comentadas, "comentada")

    if "--sin-control" in argv:
        return 0
    fallas = []
    if "tprvesp" not in activas:
        fallas.append("TPrvESP no está en activas")
    if "rprvir63" not in comentadas:
        fallas.append("RPrvIR63 no está en comentadas")
    if "hprvir42" in hallazgos:
        fallas.append("HPrvIR42 aparece, pero está en el export")
    if "strreplace" in hallazgos:
        fallas.append("StrReplace aparece, pero es una función nativa")
    if fallas:
        print("CONTROL FALLIDO: " + "; ".join(fallas), file=sys.stderr)
        return 1
    print("Controles: OK (TPrvESP activa, RPrvIR63 comentada, HPrvIR42 y StrReplace ausentes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
