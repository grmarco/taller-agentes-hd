# ¿Quién escribió el Lazarillo?

Revisión estilométrica de las hipótesis de autoría de *La vida de Lazarillo de Tormes y de sus fortunas y adversidades* (1554).

## Pregunta

El Lazarillo se publicó anónimo. Se ha atribuido, entre otros, a Alfonso de Valdés, Juan de Valdés, Diego Hurtado de Mendoza, Sebastián de Horozco, Francisco Cervantes de Salazar y Fernando de Arce de Otálora. Hay estudios estilométricos publicados desde 2016 y no coinciden entre sí.

Queremos saber:

1. Qué dicen los estudios previos, con qué corpus y con qué método llegan a sus conclusiones.
2. Qué parte de ese trabajo se puede reproducir solo con textos en dominio público.
3. Si el método (Delta de Burrows y variantes) es fiable con un texto de unas 18 000 palabras y con ediciones de ortografía desigual.
4. A qué candidatos se parece más el Lazarillo en nuestro corpus, y qué se puede afirmar y qué no.

## Condiciones

- Solo textos en dominio público. De cada texto se registra la fuente (URL), la edición, el año, el número de palabras y si la ortografía está modernizada.
- Los textos descargados no se modifican: van a `datos/bruto/`. Las versiones limpias van a `datos/limpio/`.
- Los resultados, tablas y figuras van a `resultados/`.
- Ninguna afirmación sin su fuente o sin el resultado que la respalda.
- Distinguir siempre afinidad estilística de autoría.

## Herramientas disponibles

- R con el paquete `stylo` (Eder, Rybicki y Kestemont, 2016).
- Python 3.
- Git.
