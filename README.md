# Un equipo de una persona: flujos de trabajo con IA agéntica en humanidades digitales

Materiales del taller impartido en el seminario de investigación del grupo INHDIE (UNED), el 15 de octubre de 2026, por Guillermo Marco Remón (Grupo NLP & IR, UNED).

## Contenido

| Carpeta | Qué hay |
|---|---|
| [`slides/main.pdf`](slides/main.pdf) | La presentación. |
| [`prompts/`](prompts/) | Los prompts del caso práctico, en el orden de la charla: [`PROMPTS.md`](prompts/PROMPTS.md). |
| [`caso_practico/inicio/`](caso_practico/inicio/) | Punto de partida del caso práctico: solo el planteamiento de la investigación. |
| [`caso_practico/completo/`](caso_practico/completo/) | El caso práctico resuelto: corpus en dominio público, scripts, resultados y configuración de Claude Code. |
| [`caso_practico/completo/explorador/`](caso_practico/completo/explorador/) | Explorador web del corpus (mapa estilométrico, frecuencias, concordancias, palabras características). Se abre [`index.html`](caso_practico/completo/explorador/index.html) en el navegador tras descargarlo. |

## Caso práctico: ¿quién escribió el *Lazarillo*?

Revisión estilométrica de las hipótesis de autoría del *Lazarillo de Tormes* (1554) con textos en dominio público de Alfonso y Juan de Valdés, Diego Hurtado de Mendoza, *El Crótalon* y las continuaciones de 1555 y 1620. Es un ejercicio didáctico: reproduce de forma crítica un problema sobre el que ya hay estudios publicados, y su resultado es una afinidad estilística, no una atribución. Detalles en [`caso_practico/README.md`](caso_practico/README.md) e [informe de resultados](caso_practico/completo/resultados/informe.md).

Para seguir el taller:

1. Instalar [Claude Code](https://code.claude.com/docs/en/overview) (o Codex, OpenCode u otro agente).
2. Abrir el agente dentro de `caso_practico/inicio/` y seguir [`prompts/PROMPTS.md`](prompts/PROMPTS.md).
3. Si la recopilación del corpus se alarga, copiar `caso_practico/completo/datos/` y continuar con el análisis.

## Regenerar los resultados del caso práctico

```bash
cd caso_practico/completo
python3 scripts/limpiar.py
Rscript scripts/analisis.R
python3 scripts/construir_explorador.py
```

## Licencias

- Textos del corpus: dominio público; procedencia en [`caso_practico/completo/datos/fuentes.csv`](caso_practico/completo/datos/fuentes.csv).
- Código, prompts y presentación: CC BY 4.0, salvo las imágenes de terceros que aparecen en la presentación (capturas de prensa, fotografías y tuits), que se reproducen con fines docentes y conservan los derechos de sus autores.
