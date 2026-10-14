"""Prepara los datos del explorador web y genera explorador/index.html.

Uso (desde la carpeta del proyecto): python3 scripts/construir_explorador.py
Calcula, sobre los mismos fragmentos de 18 000 palabras que analisis.R:
frecuencias relativas, Delta de Burrows (300 palabras más frecuentes), un ACP en dos
dimensiones y las palabras características del Lazarillo frente a cada texto.
"""
import collections
import csv
import json
import math
import pathlib
import re

import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LIMPIO = RAIZ / "datos" / "limpio"
TAM = 18000
MFW = 300

ETIQUETAS = {
    "Lazarillo_1554": "Lazarillo (1554)",
    "AValdes_Mercurio": "A. de Valdés · Mercurio y Carón",
    "AValdes_Roma": "A. de Valdés · Cosas acaecidas en Roma",
    "JValdes_Lengua": "J. de Valdés · Diálogo de la lengua",
    "Hurtado_Granada": "Hurtado · Guerra de Granada",
    "Villalon_Crotalon": "El Crótalon",
    "Anonimo_SegundaParte1555": "Segunda parte (1555)",
    "Luna_SegundaParte1620": "J. de Luna · Segunda parte (1620)",
}
GRUPO = {"Lazarillo": "Lazarillo", "AValdes": "Alfonso de Valdés", "JValdes": "Juan de Valdés",
         "Hurtado": "Hurtado de Mendoza", "Villalon": "El Crótalon",
         "Anonimo": "Continuaciones", "Luna": "Continuaciones"}

TOKEN = re.compile(r"[a-záéíóúüñç]+")


def tokens(texto):
    return TOKEN.findall(texto.lower())


def main():
    fuentes = {f["fichero"]: f for f in csv.DictReader(open(RAIZ / "datos" / "fuentes.csv", encoding="utf-8"))}
    textos, fragmentos = [], []
    for fichero in sorted(LIMPIO.glob("*.txt")):
        clave = fichero.stem
        bruto = fichero.read_text(encoding="utf-8")
        toks = tokens(bruto)
        f = fuentes[fichero.name]
        textos.append({"id": clave, "etiqueta": ETIQUETAS[clave], "grupo": GRUPO[clave.split("_")[0]],
                       "autor": f["autor"], "obra": f["obra"], "año": f["año"], "edicion": f["edición"],
                       "url": f["url"], "ortografia": f["ortografía"], "palabras": int(f["palabras"]),
                       "texto": re.sub(r"\s+", " ", bruto).strip()})
        n = max(1, len(toks) // TAM)
        for i in range(n):
            trozo = toks[i * TAM:(i + 1) * TAM] if len(toks) >= TAM else toks
            fragmentos.append({"id": f"{clave}_{i + 1}" if n > 1 or clave != "Lazarillo_1554" else clave,
                               "texto": clave, "grupo": GRUPO[clave.split("_")[0]], "tokens": trozo})

    # Palabras más frecuentes del conjunto y frecuencias relativas por fragmento
    total = collections.Counter()
    for fr in fragmentos:
        total.update(fr["tokens"])
    mfw = [w for w, _ in total.most_common(MFW)]
    idx = {w: i for i, w in enumerate(mfw)}
    X = np.zeros((len(fragmentos), MFW))
    for r, fr in enumerate(fragmentos):
        c = collections.Counter(fr["tokens"])
        for w, k in c.items():
            if w in idx:
                X[r, idx[w]] = k / len(fr["tokens"])
    Z = (X - X.mean(0)) / X.std(0)
    delta = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)

    # ACP en dos dimensiones
    U, S, Vt = np.linalg.svd(Z - Z.mean(0), full_matrices=False)
    pcs = U[:, :2] * S[:2]
    var = (S ** 2 / (S ** 2).sum())[:2]
    cargas = {f"pc{k + 1}": [{"palabra": mfw[j], "peso": round(float(Vt[k, j]), 4)}
                             for j in sorted(np.argsort(-np.abs(Vt[k]))[:12], key=lambda j: Vt[k, j])]
              for k in range(2)}

    # Frecuencias por texto (para búsquedas): las 4000 palabras más frecuentes
    por_texto = {t["id"]: collections.Counter(tokens(t["texto"])) for t in textos}
    vocab = [w for w, _ in total.most_common(4000)]
    frec = {w: {t: round(por_texto[t][w] / sum(por_texto[t].values()) * 10000, 2) for t in por_texto} for w in vocab}

    # Palabras características del Lazarillo frente a cada texto (log-ratio con suavizado, entre las 1500 más frecuentes)
    laz = por_texto["Lazarillo_1554"]
    nl = sum(laz.values())
    caracteristicas = {}
    for t, c in por_texto.items():
        if t == "Lazarillo_1554":
            continue
        nt = sum(c.values())
        puntos = []
        for w in vocab[:1500]:
            a, b = laz[w], c[w]
            if a + b < 20:
                continue
            lr = math.log2(((a + 0.5) / nl) / ((b + 0.5) / nt))
            puntos.append((lr, w, a, b))
        puntos.sort()
        caracteristicas[t] = {
            "lazarillo": [{"palabra": w, "lr": round(lr, 2), "a": a, "b": b} for lr, w, a, b in puntos[::-1][:15]],
            "otro": [{"palabra": w, "lr": round(lr, 2), "a": a, "b": b} for lr, w, a, b in puntos[:15]],
        }

    datos = {
        "textos": textos,
        "fragmentos": [{"id": f["id"], "texto": f["texto"], "grupo": f["grupo"],
                        "x": round(float(p[0]), 3), "y": round(float(p[1]), 3)} for f, p in zip(fragmentos, pcs)],
        "varianza": [round(float(v), 3) for v in var],
        "cargas": cargas,
        "delta": [[round(float(v), 3) for v in fila] for fila in delta],
        "mfw": MFW,
        "frecuencias": frec,
        "caracteristicas": caracteristicas,
    }
    plantilla = (RAIZ / "explorador" / "plantilla.html").read_text(encoding="utf-8")
    salida = plantilla.replace("/*DATOS*/{}", json.dumps(datos, ensure_ascii=False, separators=(",", ":")))
    # versión autónoma para abrir en el navegador; la plantilla no lleva el esqueleto del documento
    cabecera = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n</head>\n<body>\n')
    (RAIZ / "explorador" / "index.html").write_text(cabecera + salida + "\n</body>\n</html>\n", encoding="utf-8")
    (RAIZ / "explorador" / "artefacto.html").write_text(salida, encoding="utf-8")
    print(f"{len(textos)} textos, {len(fragmentos)} fragmentos; varianza explicada {var.round(3)}; "
          f"{len(salida) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
