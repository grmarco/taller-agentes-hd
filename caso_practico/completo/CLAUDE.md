# ¿Quién escribió el Lazarillo?

Revisión estilométrica de las hipótesis de autoría del *Lazarillo de Tormes* (1554). El planteamiento completo está en @PROYECTO.md.

## Estructura

- `datos/bruto/`: textos tal como se descargaron. No se modifican nunca.
- `datos/limpio/`: un fichero por obra, `Autor_obra.txt`, generado con `python3 scripts/limpiar.py`.
- `datos/fuentes.csv`: procedencia de cada texto (URL, edición, palabras, ortografía).
- `scripts/analisis.R`: validación del método y análisis con `stylo` (`Rscript scripts/analisis.R`).
- `resultados/`: tablas, figuras e informe.

## Normas

- Escribir en español idiomático: los informes los leen filólogos.
- Ninguna afirmación sin su fuente o sin el resultado que la respalda.
- Solo textos en dominio público, con su procedencia anotada en `datos/fuentes.csv`.
- Distinguir siempre afinidad estilística de autoría.
- Antes de aplicar un método al Lazarillo, validarlo con textos de autor conocido.
