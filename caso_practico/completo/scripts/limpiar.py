"""Limpia los textos de datos/bruto/ y escribe datos/limpio/ y datos/fuentes.csv.

Uso (desde la carpeta del proyecto): python3 scripts/limpiar.py
"""
import csv
import html
import pathlib
import re
import subprocess
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "datos" / "bruto"
LIMPIO = RAIZ / "datos" / "limpio"


def normalizar_espacios(t):
    t = html.unescape(t).replace("\r", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n\s*", "\n\n", t)
    return t.strip() + "\n"


def quitar_interlocutores(t):
    """Quita las marcas de interlocutor de los diálogos (p. ej. «MARCIO.—», «Caronte.—»)."""
    t = re.sub(r"(^|\n)\s*[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑa-záéíóúñ ]{1,25}\.\s*[—–-]+\s*", r"\1", t)
    return t


def gutenberg(nombre, desde, hasta):
    lineas = (BRUTO / nombre).read_text(encoding="utf-8").replace("\r", "").split("\n")
    return "\n".join(lineas[desde - 1:hasta - 1])


def epub(nombre):
    z = zipfile.ZipFile(BRUTO / nombre)
    partes = sorted(n for n in z.namelist()
                    if n.endswith(".xhtml") and not n.endswith(("CoverPage.xhtml", "indice.xhtml")))
    textos = []
    for n in partes:
        x = z.read(n).decode("utf-8")
        x = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", x, flags=re.S)
        x = re.sub(r"</p>|<br\s*/?>|</h\d>", "\n", x)
        textos.append(re.sub(r"<[^>]+>", " ", x))
    return "\n".join(textos)


def lazarillo():
    t = gutenberg("lazarillo_1554_gutenberg.txt", 41, 2134)
    t = re.sub(r"\{.*?\}", " ", t, flags=re.S)          # interpolaciones de Alcalá, 1554
    t = re.sub(r"\[\d+\]", "", t)                        # llamadas a nota
    t = re.sub(r"^(Prólogo|Tratado \w+)\s*$", "", t, flags=re.M)
    return t


def guerra_granada():
    # Libros I-IV; la edición de 1842 añade después el Lazarillo, que se descarta
    t = gutenberg("hurtado_guerra_granada_gutenberg.txt", 1240, 6770)
    return re.sub(r"^\s*LIBRO [IVX]+\.\s*$", "", t, flags=re.M)


def segunda_parte_1555():
    w = (BRUTO / "segunda_parte_1555_wikisource.wiki").read_text(encoding="utf-8")
    w = re.sub(r"\{\{encabezado.*?\}\}", " ", w, flags=re.S)
    w = re.sub(r"\{\{[^{}]*\}\}", " ", w)
    w = re.sub(r"^=== .* ===$", "", w, flags=re.M)
    w = re.sub(r"'''.*?'''", " ", w, flags=re.S)        # títulos y epígrafes de capítulo
    w = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", w)
    w = re.sub(r"<[^>]+>", " ", w)
    # se descartan los preliminares (portada y privilegio) del prólogo
    return w[w.find("En este tiempo estaba en mi prosperidad"):]


def luna_1620():
    # pdftotext escribe en la salida estándar: datos/bruto/ no se toca
    t = subprocess.run(["pdftotext", str(BRUTO / "luna_segunda_parte_y_hurtado_caronte.pdf"), "-"],
                       check=True, capture_output=True, text=True).stdout
    ini = t.find("La ocasión, amigo lector")
    fin = t.find("FIN", t.find("Ésta es, amigo lector, en suma"))
    t = t[ini:fin]
    t = re.sub(r"-\n(\w)", r"\1", t)                    # guiones de final de línea
    t = re.sub(r"^\s*\d+\s*$", "", t, flags=re.M)        # números de página
    return t


TEXTOS = [
    # fichero limpio, función, autor, obra, año, edición, URL, ortografía
    ("Lazarillo_1554.txt", lazarillo, "Anónimo", "La vida de Lazarillo de Tormes", 1554,
     "Burgos 1554 (Proyecto Gutenberg), sin las interpolaciones de Alcalá",
     "https://www.gutenberg.org/cache/epub/320/pg320.txt", "parcialmente modernizada"),
    ("AValdes_Mercurio.txt", lambda: quitar_interlocutores(epub("alfonso_valdes_mercurio_caron.epub")),
     "Alfonso de Valdés", "Diálogo de Mercurio y Carón", 1529, "textos.info",
     "https://www.textos.info/alfonso-de-valdes/dialogo-de-mercurio-y-caron", "modernizada"),
    ("AValdes_Roma.txt", lambda: quitar_interlocutores(epub("alfonso_valdes_cosas_roma.epub")),
     "Alfonso de Valdés", "Diálogo de las cosas acaecidas en Roma", 1527, "textos.info",
     "https://www.textos.info/alfonso-de-valdes/dialogo-de-las-cosas-acaecidas-en-roma", "modernizada"),
    ("JValdes_Lengua.txt", lambda: quitar_interlocutores(epub("juan_valdes_dialogo_lengua.epub")),
     "Juan de Valdés", "Diálogo de la lengua", 1535, "textos.info",
     "https://www.textos.info/juan-de-valdes/dialogo-de-la-lengua", "modernizada"),
    ("Hurtado_Granada.txt", guerra_granada,
     "Diego Hurtado de Mendoza", "Guerra de Granada (libros I-IV)", 1570, "edición de 1842 (Proyecto Gutenberg)",
     "https://www.gutenberg.org/cache/epub/61022/pg61022.txt", "siglo XIX"),
    ("Villalon_Crotalon.txt", lambda: quitar_interlocutores(epub("villalon_crotalon.epub")),
     "Cristóbal de Villalón (atrib.)", "El Crótalon", 1553, "textos.info",
     "https://www.textos.info/cristobal-de-villalon/el-crotalon", "modernizada"),
    ("Anonimo_SegundaParte1555.txt", segunda_parte_1555,
     "Anónimo", "Segunda parte del Lazarillo (Amberes)", 1555, "Wikisource",
     "https://es.wikisource.org/wiki/La_segunda_parte_de_Lazarillo_de_Tormes", "original"),
    ("Luna_SegundaParte1620.txt", luna_1620,
     "Juan de Luna", "Segunda parte de la vida de Lazarillo de Tormes", 1620, "Biblioteca Antológica",
     "https://biblioteca-antologica.org/es/wp-content/uploads/2017/10/HURTADO-DE-MENDOZA-Segunda-vida-de-Lazarillo-de-Tormes.pdf",
     "modernizada"),
]


def main():
    LIMPIO.mkdir(parents=True, exist_ok=True)
    filas = []
    for fichero, funcion, autor, obra, anio, edicion, url, orto in TEXTOS:
        t = normalizar_espacios(funcion())
        (LIMPIO / fichero).write_text(t, encoding="utf-8")
        palabras = len(t.split())
        filas.append([fichero, autor, obra, anio, edicion, url, palabras, orto])
        print(f"{fichero:32} {palabras:7d}  | {t[:60]!r} ... {t[-60:]!r}")
    with open(RAIZ / "datos" / "fuentes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["fichero", "autor", "obra", "año", "edición", "url", "palabras", "ortografía"])
        w.writerows(filas)


if __name__ == "__main__":
    main()
