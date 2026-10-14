# Caso práctico: ¿quién escribió el *Lazarillo*?

Dos carpetas:

- **`inicio/`**: el punto de partida del taller. Solo contiene `PROYECTO.md`, el planteamiento de la investigación. Se abre Claude Code dentro de esta carpeta y se sigue la secuencia de prompts.
- **`completo/`**: el proyecto ya hecho, como respaldo o para ir directamente a la parte interactiva:
  - `datos/bruto/`: los textos tal como se descargaron (todos en dominio público);
  - `datos/limpio/` y `datos/fuentes.csv`: el corpus limpio y la procedencia de cada texto;
  - `scripts/limpiar.py` y `scripts/analisis.R`: limpieza y análisis con `stylo`;
  - `resultados/`: validación, distancias, dendrograma, árbol de consenso e informe;
  - `CLAUDE.md` y `.claude/`: instrucciones del proyecto, subagentes (bibliógrafo, constructor de corpus, revisor), la skill `/anadir-texto` y un hook que protege `datos/bruto/`.

Para regenerar todo desde `completo/`:

```bash
python3 scripts/limpiar.py
Rscript scripts/analisis.R
```

Requisitos: Python 3, `pdftotext` (poppler) y R con el paquete `stylo` (`install.packages("stylo")`).
