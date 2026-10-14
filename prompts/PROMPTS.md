# Prompts del taller

En el orden de la charla. En la presentación, cada caja P01, P02… corresponde a uno de estos.

## P01 · Chat: pedir el texto

*chat (claude.ai, ChatGPT…)*

```text
Necesito el texto del Lazarillo de Tormes (1554) en una edición de dominio público para un análisis estilométrico. Descárgamelo y dime cuántas palabras tiene.
```

## P02 · Agente: mismo encargo, con comprobación

*Claude Code, en la carpeta caso_practico*

```text
Necesito el texto del Lazarillo de Tormes (1554) en una edición de dominio público para un análisis estilométrico. Guarda el original tal cual y prepara aparte una versión limpia, sin cabeceras, notas ni las interpolaciones de la edición de Alcalá. Antes de terminar, comprueba que la versión limpia tiene entre 17 000 y 20 000 palabras y muéstrame la primera y la última frase.
```

## P03 · Instrucciones permanentes

*Claude Code*

```text
/init
```

## P04 · Completar CLAUDE.md

*Claude Code*

```text
Añade a CLAUDE.md, en no más de seis líneas: escribe en español idiomático, porque los informes los leen filólogos; ninguna afirmación sin su fuente o sin el resultado que la respalda; no modifiques nunca los textos originales descargados; distingue siempre afinidad estilística de autoría.
```

## P05 · Planificar la investigación

*Claude Code (modo plan: Mayús+Tab)*

```text
/plan Lee PROYECTO.md y propón un plan de trabajo con subagentes: estado de la cuestión, construcción del corpus (un subagente por candidato), validación del método y análisis. Para cada subagente indica qué modelo usa y por qué (Haiku para descargar y limpiar, Sonnet para buscar y leer bibliografía), cuántos turnos como máximo y cuánto calculas que costará. Incluye cómo comprobaremos que cada parte está bien hecha. No ejecutes nada todavía.
```

## P06 · Definir los subagentes

*Claude Code*

```text
Crea tres subagentes para este proyecto. Un bibliógrafo (con Sonnet y búsqueda en internet) que compruebe que cada estudio existe antes de citarlo y me devuelva un resumen de diez líneas. Un constructor de corpus (con Haiku, el modelo barato) que busque, descargue y limpie los textos en dominio público de un autor y anote de dónde salen. Y un revisor (con Sonnet) que solo pueda leer, no modificar.
```

## P07 · Orquestar el trabajo en paralelo

*Claude Code*

```text
Ejecuta el plan: lanza a la vez el bibliógrafo y un constructor de corpus por cada candidato con textos en dominio público (Alfonso de Valdés, Juan de Valdés, Diego Hurtado de Mendoza) y otro para los textos de control (Segunda parte de 1555, Juan de Luna 1620, El Crótalon de Villalón). Cuando terminen, resume en una tabla qué tenemos de cada candidato y qué nos falta respecto a los estudios previos.
```

## P08 · Convertir en skill

*Claude Code*

```text
Convierte en una skill llamada anadir-texto lo que hemos hecho para añadir un texto al corpus: recibe un enlace, un autor y una obra; descarga, limpia, cuenta palabras, enseña el principio y el final y anota la procedencia. Si la edición tiene derechos o el texto tiene menos de 5 000 palabras, que no lo añada y explique por qué.
```

## P09 · Usar la skill

*Claude Code*

```text
/anadir-texto https://es.wikisource.org/wiki/La_segunda_parte_de_Lazarillo_de_Tormes Anónimo Segunda_parte_1555
```

## P10 · Validar el método

*Claude Code*

```text
Antes de aplicar el método al Lazarillo, valídalo. Con stylo en R, trocea los textos de autor conocido en fragmentos de unas 18 000 palabras y comprueba si Delta (clásica y coseno, de 100 a 500 palabras más frecuentes) agrupa cada fragmento con su autor. Repítelo con la ortografía normalizada. Da el método por bueno solo si acierta al menos el 90 % de los fragmentos; si no llega, explícame por qué y no sigas.
```

## P11 · Aplicar el método al Lazarillo

*Claude Code*

```text
Aplica al Lazarillo la configuración que mejor ha funcionado: dendrograma, tabla de distancias a cada candidato y árbol de consenso. Escribe un informe que compare con el estado de la cuestión y separe lo que se puede afirmar de lo que no.
```

## P12 · Hook que protege los textos

*Claude Code*

```text
Añade un hook, una regla que se cumpla siempre, que impida modificar los textos originales descargados. Después explícame por qué es más fiable que pedírtelo en CLAUDE.md.
```

## P13 · Revisión independiente

*Claude Code, tras /clear*

```text
Pide al revisor que examine los resultados y los scripts. Quiero solo los problemas que afecten a la validez de las conclusiones.
```

## P14 · Guardar el trabajo con git

*Claude Code*

```text
Inicializa un repositorio git si no existe y haz un commit con lo hecho hasta ahora, con un mensaje descriptivo en español.
```

## P15 · Trabajo por lotes sin conversación

*terminal (modo headless)*

```text
for f in datos/limpio/*.txt; do
  claude -p "Resume en una línea el género, la fecha y el registro de $f" --model haiku >> resultados/fichas.txt
done
```

## P16 · Figuras para el informe

*Claude Code*

```text
Haz tres figuras para el informe: un mapa de componentes principales de los fragmentos, coloreados por autor; un mapa de calor de las distancias Delta; y un gráfico con las palabras que más pesan en cada eje del mapa. Explícame qué muestra cada figura y qué no se puede concluir de ella.
```

## P17 · Un explorador web del corpus

*Claude Code*

```text
Construye un explorador web del corpus en una sola página HTML que funcione sin servidor, con cinco pestañas: la tabla del corpus con sus fuentes; el mapa estilométrico interactivo con el mapa de calor; un comparador de frecuencias de palabras por texto; concordancias (KWIC) con filtro por texto; y las palabras características del Lazarillo frente a cada candidato. Ábrelo en el navegador y comprueba que cada pestaña funciona antes de darlo por terminado.
```
