# Informe: afinidad estilométrica del Lazarillo con los candidatos en dominio público

Resultados de `scripts/analisis.R` (Delta de Burrows, paquete `stylo`) sobre los textos de `datos/limpio/`. Fecha: 14 de octubre de 2026.

## Corpus

| Texto | Palabras | Ortografía |
|---|---|---|
| *Lazarillo* (Burgos, 1554) | 18 369 | parcialmente modernizada |
| Alfonso de Valdés, *Mercurio y Carón* | 53 789 | modernizada |
| Alfonso de Valdés, *Cosas acaecidas en Roma* | 24 425 | modernizada |
| Juan de Valdés, *Diálogo de la lengua* | 39 213 | modernizada |
| Diego Hurtado de Mendoza, *Guerra de Granada* (libros I-IV) | 63 233 | edición de 1842 |
| *El Crótalon* (Villalón, atrib.) | 111 867 | modernizada |
| *Segunda parte* anónima (Amberes, 1555) | 25 461 | original |
| Juan de Luna, *Segunda parte* (1620) | 23 478 | modernizada |

Procedencia completa en `datos/fuentes.csv`. Falta Arce de Otálora, el candidato que favorecen los estudios computacionales (Madrigal 2020, 2022, 2024), porque sus *Coloquios* solo están en edición moderna con derechos.

## Validación del método

- Los textos de autor conocido se trocearon en fragmentos de 18 000 palabras (el tamaño del *Lazarillo*).
- En todas las configuraciones probadas (100 a 500 palabras más frecuentes; Delta clásica y coseno; con y sin normalizar la ortografía), el fragmento más próximo a cada fragmento es del mismo autor: 14 de 14 (`resultados/validacion.csv`).
- Esa prueba es optimista: los fragmentos de una misma obra comparten tema, personajes y edición.
- Prueba más exigente: entre obras distintas de Alfonso de Valdés, el único autor con dos obras en el corpus, el fragmento más próximo sigue siendo suyo en todas las configuraciones (`resultados/validacion_entre_obras.csv`).

## Resultados

Distancia mínima del *Lazarillo* a cada grupo (Delta clásica, 500 palabras más frecuentes, sin normalizar):

| Texto | Distancia |
|---|---|
| Juan de Luna, *Segunda parte* (1620) | 0,77 |
| *Segunda parte* anónima (1555) | 0,88 |
| *El Crótalon* | 0,90 |
| Alfonso de Valdés | 0,98 |
| Juan de Valdés | 1,12 |
| Hurtado de Mendoza | 1,22 |

El dendrograma (`resultados/dendrograma.png`) y el árbol de consenso de 100 a 500 palabras (`resultados/consenso.png`) agrupan el *Lazarillo* con sus dos continuaciones.

## Qué se puede afirmar y qué no

- **Se puede afirmar** que, en este corpus, el *Lazarillo* se parece más a sus continuaciones y a la narrativa lucianesca de *El Crótalon* que a los diálogos de los Valdés o a la crónica de Hurtado.
- **No se puede afirmar** nada sobre su autor:
  - las continuaciones imitan al *Lazarillo* y comparten protagonista y vocabulario;
  - los textos de los candidatos son de otros géneros (diálogo, crónica);
  - la *Guerra de Granada* está en una edición del siglo XIX, y su lejanía puede deberse tanto a la edición y al género como al autor;
  - falta el candidato más citado por los estudios computacionales.
- **Siguiente paso razonable**: comparar con textos narrativos de los candidatos y con ediciones de ortografía homogénea, e incorporar los *Coloquios* de Otálora si se consigue un texto utilizable.
