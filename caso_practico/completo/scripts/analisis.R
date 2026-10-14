# Validación del método y análisis estilométrico del Lazarillo.
# Uso (desde la carpeta del proyecto): Rscript scripts/analisis.R
suppressMessages(library(stylo))

dir.create("resultados", showWarnings = FALSE)
TAM <- 18000   # tamaño de fragmento: el del Lazarillo

autor_de <- function(f) sub("_.*", "", f)

normalizar <- function(palabras) {
  p <- chartr("áéíóúàèìòùâêîôûäëïöüç", "aeiouaeiouaeiouaeiouz", palabras)
  gsub("v", "u", p)
}

leer <- function(f, norm) {
  t <- tolower(paste(readLines(file.path("datos/limpio", f), encoding = "UTF-8", warn = FALSE), collapse = " "))
  p <- txt.to.words.ext(t, corpus.lang = "Spanish")
  if (norm) normalizar(p) else p
}

trocear <- function(palabras, nombre) {
  n <- floor(length(palabras) / TAM)
  if (n == 0) return(setNames(list(palabras), nombre))
  setNames(lapply(seq_len(n), function(i) palabras[((i - 1) * TAM + 1):(i * TAM)]),
           paste0(nombre, "_", seq_len(n)))
}

ficheros <- list.files("datos/limpio", pattern = "\\.txt$")
conocidos <- setdiff(ficheros, "Lazarillo_1554.txt")

preparar <- function(norm) {
  frag <- list()
  for (f in conocidos) frag <- c(frag, trocear(leer(f, norm), sub("\\.txt$", "", f)))
  frag[["Lazarillo_1554"]] <- leer("Lazarillo_1554.txt", norm)
  frag
}

distancias <- function(frag, mfw, medida) {
  frecs <- make.frequency.list(frag, head = mfw)
  tabla <- make.table.of.frequencies(frag, frecs)
  if (medida == "clasica") as.matrix(dist.delta(tabla)) else as.matrix(dist.wurzburg(tabla))
}

# --- 1. Validación: ¿el fragmento más próximo es del mismo autor? -------------------
validacion <- data.frame()
for (norm in c(FALSE, TRUE)) {
  frag <- preparar(norm)
  for (mfw in c(100, 200, 300, 500)) for (medida in c("clasica", "coseno")) {
    d <- distancias(frag, mfw, medida)
    nombres <- setdiff(rownames(d), "Lazarillo_1554")
    autores <- autor_de(nombres)
    # solo se evalúan los autores con al menos dos fragmentos
    evaluables <- nombres[autores %in% names(which(table(autores) > 1))]
    aciertos <- sapply(evaluables, function(n) {
      otros <- setdiff(nombres, n)
      autor_de(otros[which.min(d[n, otros])]) == autor_de(n)
    })
    validacion <- rbind(validacion, data.frame(normalizada = norm, mfw = mfw, delta = medida,
                                               fragmentos = length(evaluables), acierto = mean(aciertos)))
  }
}
write.csv(validacion, "resultados/validacion.csv", row.names = FALSE)
print(validacion)

# --- 1b. Prueba más exigente: entre obras distintas del mismo autor -----------------
# Los fragmentos de una misma obra comparten tema, personajes y edición, y se parecen
# por eso. Solo Alfonso de Valdés tiene dos obras en el corpus: ¿el fragmento de una
# obra queda más cerca de la otra obra de Valdés que de las de otros autores?
obra_de <- function(n) sub("_\\d+$", "", n)
entre_obras <- data.frame()
for (norm in c(FALSE, TRUE)) {
  frag <- preparar(norm)
  for (mfw in c(100, 200, 300, 500)) for (medida in c("clasica", "coseno")) {
    d <- distancias(frag, mfw, medida)
    nombres <- setdiff(rownames(d), "Lazarillo_1554")
    for (n in nombres[autor_de(nombres) == "AValdes"]) {
      otros <- nombres[obra_de(nombres) != obra_de(n)]
      entre_obras <- rbind(entre_obras, data.frame(normalizada = norm, mfw = mfw, delta = medida,
        fragmento = n, mas_cercano = otros[which.min(d[n, otros])],
        acierto = autor_de(otros[which.min(d[n, otros])]) == "AValdes"))
    }
  }
}
write.csv(entre_obras, "resultados/validacion_entre_obras.csv", row.names = FALSE)
cat("\nAcierto entre obras (Alfonso de Valdés):", round(mean(entre_obras$acierto), 2), "\n")
print(aggregate(acierto ~ normalizada + delta, entre_obras, mean))

# --- 2. Aplicación al Lazarillo con la mejor configuración ----------------------------
mejor <- validacion[order(-validacion$acierto, -validacion$mfw), ][1, ]
cat("\nMejor configuración:", if (mejor$normalizada) "normalizada" else "sin normalizar",
    mejor$mfw, "MFW, Delta", mejor$delta, "- acierto", mejor$acierto, "\n")
if (mejor$acierto < 0.9) cat("AVISO: el método no alcanza el 90 % de acierto; los resultados son solo indicativos.\n")

frag <- preparar(mejor$normalizada)
d <- distancias(frag, mejor$mfw, mejor$delta)
laz <- d["Lazarillo_1554", setdiff(colnames(d), "Lazarillo_1554")]
ranking <- data.frame(fragmento = names(laz), autor = autor_de(names(laz)), distancia = round(laz, 3))
ranking <- ranking[order(ranking$distancia), ]
write.csv(ranking, "resultados/distancias_lazarillo.csv", row.names = FALSE)
print(ranking)

# Dendrograma
png("resultados/dendrograma.png", width = 1600, height = 1000, res = 160)
par(mar = c(2, 2, 3, 12))
plot(as.dendrogram(hclust(as.dist(d), method = "ward.D2")), horiz = TRUE,
     main = sprintf("Delta %s, %d palabras más frecuentes (%s)", if (mejor$delta == "clasica") "clásica" else "coseno", mejor$mfw,
                    if (mejor$normalizada) "ortografía normalizada" else "sin normalizar"))
dev.off()

# Árbol de consenso (100 a 500 MFW) con stylo, sobre los mismos fragmentos
dir.create("resultados/fragmentos", showWarnings = FALSE)
unlink(list.files("resultados/fragmentos", full.names = TRUE))
for (n in names(frag)) writeLines(paste(frag[[n]], collapse = " "), file.path("resultados/fragmentos", paste0(n, ".txt")))
olddir <- setwd("resultados")
r <- stylo(gui = FALSE, custom.graph.title = "Lazarillo y candidatos", corpus.dir = "fragmentos", corpus.lang = "Other", analysis.type = "BCT",
           mfw.min = 100, mfw.max = 500, mfw.incr = 100, consensus.strength = 0.5,
           distance.measure = if (mejor$delta == "clasica") "dist.delta" else "dist.wurzburg",
           write.png.file = TRUE, plot.custom.width = 10, plot.custom.height = 8, display.on.screen = FALSE)
setwd(olddir)
file.rename(list.files("resultados", pattern = "Consensus.*\\.png$", full.names = TRUE)[1], "resultados/consenso.png")
unlink(c(list.files("resultados", pattern = "Consensus.*EDGES\\.csv$", full.names = TRUE),
         "resultados/stylo_config.txt", "resultados/table_with_frequencies.txt", "resultados/wordlist.txt"))
