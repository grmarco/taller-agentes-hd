---
name: anadir-texto
description: Añade un texto en dominio público al corpus del proyecto, con su ficha de procedencia. Úsala cada vez que haya que incorporar una obra.
argument-hint: "<URL> <Autor> <obra>"
---
Añade al corpus el texto indicado en `$ARGUMENTS`.

1. Descárgalo en `datos/bruto/` sin modificarlo.
2. Crea `datos/limpio/Autor_obra.txt` solo con el texto de la obra (sin prólogos del editor, notas, índices ni cabeceras de la web).
3. Cuenta las palabras y comprueba que el principio y el final del fichero limpio son los de la obra; muéstrame las primeras y últimas dos líneas.
4. Añade su fila a `datos/fuentes.csv` (autor, obra, año, edición, URL, palabras, ortografía original o modernizada).
5. Si la edición tiene derechos de autor o el texto tiene menos de 5 000 palabras, no lo añadas y explica por qué.
