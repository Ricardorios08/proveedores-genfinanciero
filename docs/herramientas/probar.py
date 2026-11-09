#!/usr/bin/env python3
"""Prueba que los controles de las herramientas puedan fallar.

Uso:
    python3 -I docs/herramientas/probar.py

Cada caso arma una entrada (desde los fixtures sintéticos de fixtures/) que
rompe UN control, y comprueba que la herramienta falle exactamente por ese
control. También comprueba que la entrada base pase. Un control que nunca se
vio fallar no prueba nada.
"""
import contextlib
import importlib.util
import io
import pathlib
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
FIX = AQUI / "fixtures"


def cargar(nombre):
    spec = importlib.util.spec_from_file_location(nombre.replace("-", "_"), AQUI / f"{nombre}.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def correr(modulo, argv):
    """Corre main() capturando la salida. Devuelve (código, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = modulo.main(argv)
    return rc, out.getvalue(), err.getvalue()


def con_texto(texto):
    f = tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8")
    f.write(texto)
    f.close()
    return f.name


resultados = []


def caso(nombre, ok, detalle=""):
    resultados.append((nombre, ok, detalle))


# --- contar-xpz.py ---------------------------------------------------------
contar = cargar("contar-xpz")
rc, _, err = correr(contar, ["contar-xpz", str(FIX / "xpz-118.xml")])
caso("contar: 118 objetos falla", rc == 1 and "CONTROL FALLIDO" in err, err.strip())

# --- dependencias-xpz.py ---------------------------------------------------
dep = cargar("dependencias-xpz")
base = (FIX / "dependencias-base.xml").read_text(encoding="utf-8")

rc, out, err = correr(dep, ["dependencias-xpz", con_texto(base)])
caso("dependencias: base pasa", rc == 0, err.strip())

variantes = {
    "TPrvESP no está en activas": base.replace("\tTPrvESP.Popup(&Usuario, &Modo)", "\t// TPrvESP.Popup(&Usuario, &Modo)"),
    "RPrvIR63 no está en comentadas": base.replace("\t/*\n\tRPrvIR63(&Usuario, &Flag)\n\t*/", "\tRPrvIR63(&Usuario, &Flag)"),
    "HPrvIR42 aparece": base.replace('    <Object name="HPrvIR42" type="c9584656-94b6-4ccd-890f-332d11fc2c25" />\n', ""),
}
for esperado, texto in variantes.items():
    assert texto != base, f"la variante '{esperado}' no cambió el fixture"
    rc, _, err = correr(dep, ["dependencias-xpz", con_texto(texto)])
    otros = [v for v in list(variantes) + ["StrReplace aparece"] if v != esperado and v in err]
    caso(f"dependencias: falla solo por '{esperado}'", rc == 1 and esperado in err and not otros, err.strip())

# StrReplace es nativa por la lista NATIVAS, no por el fixture: se saca de la lista.
dep.NATIVAS.discard("strreplace")
rc, _, err = correr(dep, ["dependencias-xpz", con_texto(base)])
caso("dependencias: falla solo por 'StrReplace aparece'", rc == 1 and "StrReplace aparece" in err and err.count(";") == 0, err.strip())
dep.NATIVAS.add("strreplace")

# --- verificar.py ----------------------------------------------------------
import re
import shutil

ver = cargar("verificar")
OK = FIX / "verificar-ok"

rc, out, _ = correr(ver, ["verificar", str(OK)])
caso("verificar: fixture ok pasa", rc == 0, out.strip())


def mutar(archivo, viejo, nuevo):
    """Copia el fixture ok a un directorio temporal y reemplaza viejo por nuevo en archivo.
    Con viejo=None crea el archivo con contenido nuevo."""
    destino = pathlib.Path(tempfile.mkdtemp()) / "docs"
    shutil.copytree(OK, destino)
    p = destino / archivo
    if viejo is None:
        p.write_text(nuevo, encoding="utf-8")
    else:
        texto = p.read_text(encoding="utf-8")
        assert texto.count(viejo) == 1, f"mutación ambigua o inexistente en {archivo}: {viejo!r}"
        p.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
    return destino


R01 = "- **R-01** Regla accidental. [V · capas: código · ev: objsinta_impl.java E11 · clase: accidente]"
mutaciones = [
    ("C1", "archivo fuera del índice", "extra.md", None, "# Extra\n"),
    ("C1", "índice nombra un archivo inexistente", "README.md", "- `features.csv`: dos filas.", "- `features.csv`: dos filas.\n- [falta.md](falta.md): no existe."),
    ("C2", "afirmación sin bloque", "pasos/paso-01.md", "Texto explicativo en párrafo: no es una afirmación.", "- Afirmación sin bloque."),
    ("C2", "capa inválida", "pasos/paso-01.md", "capas: código, diseño · ev: objsinta_impl.java E10", "capas: código, base · ev: objsinta_impl.java E10"),
    ("C3", "código escrito como S", "pasos/paso-01.md", "[V · capas: código, diseño", "[S · capas: código, diseño"),
    ("C3", "ejecución sin versión escrita como V", "pasos/paso-01.md", "[S · capas: ejecución · ev: S02", "[V · capas: ejecución · ev: S02"),
    ("C3", "diseño solo escrito como V", "pasos/paso-01.md", "[S · capas: diseño · ev: XPZ ObjSintA Events 'Uno'", "[V · capas: diseño · ev: XPZ ObjSintA Events 'Uno'"),
    ("C4", "regla sin clase", "pasos/paso-01.md", "E11 · clase: accidente]", "E11]"),
    ("C4", "regla repetida", "pasos/paso-01.md", R01, R01 + "\n" + R01.replace("Regla accidental", "Otra")),
    ("C5", "accidente sin DR", "decisiones-rediseno.md", "Cubre R-01 y D-01.", "Cubre D-01."),
    ("C5", "esencial fuera de 'Se mantiene'", "decisiones-rediseno.md", "| R-02 | Esencial. |", "| (ninguna) | — |"),
    ("C5", "marca a una discrepancia inexistente", "pasos/paso-01.md", "≠ D-01]", "≠ D-09]"),
    ("C6", "columna faltante", "features.csv", ",capas,evidencia,decision", ",evidencia,decision"),
    ("C6", "evidencia vacía", "features.csv", "código,objsinta_impl.java,pendiente", "código,,pendiente"),
    ("C6", "decisión sin DR", "features.csv", "ver DR-01,", "sin referencia,"),
]
for codigo, desc, archivo, viejo, nuevo in mutaciones:
    rc, out, _ = correr(ver, ["verificar", str(mutar(archivo, viejo, nuevo))])
    codigos = set(re.findall(r"^\[(C\d)\]", out, re.MULTILINE))
    caso(f"verificar: '{desc}' falla solo en {codigo}", rc == 1 and codigos == {codigo}, out.strip())

# --- universo-fin.py -------------------------------------------------------
uni = cargar("universo-fin")


def fin_sintetico(sin=()):
    """Arma un fin/ mínimo, con clases vacías que solo se referencian entre sí.
    `sin` lista las referencias (origen, destino) que se omiten."""
    refs = {
        "hprvir02": ["hprvir21", "acpsrestadp"],
        "hprvir21": ["hprvir40"],
        "loginprov": ["hprvir02"],
        "loginrecuperarpwd": ["pprvsendmail"],
        "hprvir40": ["pprvir50", "pprvir03"],
        "pprvir03": ["apprvir03"],
    }
    d = pathlib.Path(tempfile.mkdtemp())
    objetos = set(uni.ENTRADAS) | {"hprvir21", "hprvir40", "pprvir50", "pprvir03", "apprvir03", "acpsrestadp", "loginprov", "loginrecuperarpwd", "pprvsendmail"}
    for o in objetos:
        cuerpo = "".join(f"new com.fin.{r}();\n" for r in refs.get(o, []) if (o, r) not in sin)
        (d / f"{o}.java").write_text(f"// sintético\nclass {o} {{\n{cuerpo}}}\n", encoding="utf-8")
    return d


rc, _, err = correr(uni, ["universo-fin", str(fin_sintetico())])
caso("universo: fin sintético pasa", rc == 0, err.strip())
modulo, _, _, borde = uni.calcular(fin_sintetico())
caso("universo: un procedimiento apprv* detrás de su envoltorio queda dentro", "apprvir03" in modulo and "apprvir03" not in borde, str(sorted(modulo)))
for falta, esperado in [
    (("hprvir40", "pprvir50"), "pprvir50 no quedó dentro"),
    (("loginprov", "hprvir02"), "loginprov no quedó en entradas externas"),
    (("loginrecuperarpwd", "pprvsendmail"), "pprvsendmail no quedó en el borde"),
]:
    rc, _, err = correr(uni, ["universo-fin", str(fin_sintetico(sin={falta}))])
    caso(f"universo: falla solo por '{esperado}'", rc == 1 and esperado in err and err.count(";") == 0, err.strip())

# --- ejemplos de convenciones.md -------------------------------------------
conv = (AQUI.parent / "convenciones.md").read_text(encoding="utf-8")
seccion = conv.split("## Ejemplos reales", 1)[1].split("\n## ", 1)[0]
ejemplos = [l for l in seccion.split("```")[1].splitlines() if l.startswith("- ")]
caso("convenciones: hay dos ejemplos", len(ejemplos) == 2, str(ejemplos))
for i, linea in enumerate(ejemplos, 1):
    b = ver.RE_BLOQUE.search(linea)
    campos = ver.parsear_bloque(b.group(2)) if b else "sin bloque"
    if isinstance(campos, str):
        caso(f"convenciones: ejemplo {i} bien formado", False, campos)
        continue
    calc = ver.estado_calculado(campos, set(), {})
    caso(f"convenciones: ejemplo {i} declara el estado calculado ({calc})", b.group(1) == calc, linea)
    otro = {"V": "S", "S": "V", "D": "V"}[b.group(1)]
    caso(f"convenciones: ejemplo {i} con estado {otro} deja de coincidir", otro != calc, linea)

# --- resumen ---------------------------------------------------------------
fallos = 0
for nombre, ok, detalle in resultados:
    print(f"{'OK  ' if ok else 'FALLA'} {nombre}")
    if not ok:
        fallos += 1
        print(f"      {detalle}")
print(f"\n{len(resultados) - fallos}/{len(resultados)} casos como se esperaba")
sys.exit(1 if fallos else 0)
