# Contexto de Modificaciones - Proyecto MMA (Data Science)

Este documento resume las últimas actualizaciones realizadas en el informe LaTeX basadas en las métricas correctas aportadas.

## 1. Archivos Modificados
- `informe/auxx.tex`: Se actualizaron las secciones del Árbol de Decisión y Naïve Bayes para reflejar las métricas reales evaluadas en el conjunto de prueba (Test).

## 2. Métricas Actualizadas en el Informe (Conjunto de Prueba)

### Árbol de Decisión (Criterio Entropía)
- **Exactitud (Accuracy):** 65.74%
- **Reporte de Clasificación:**
  - **Gana Blue (0):** Precision: 64%, Recall: 41%, F1-Score: 50%
  - **Gana Red (1):** Precision: 66%, Recall: 84%, F1-Score: 74%

### Naïve Bayes Gaussiano
- **Exactitud (Accuracy):** 65.00%
- **Reporte de Clasificación:**
  - **Gana Blue (0):** Precision: 59%, Recall: 53%, F1-Score: 56%
  - **Gana Red (1):** Precision: 69%, Recall: 74%, F1-Score: 71%

## 3. Justificaciones Técnicas Agregadas (Formato Académico / Humano)
- **Árbol de Decisión:** Se eligió por su interpretabilidad. Este algoritmo permite extraer reglas visuales sobre qué características influyen en una victoria, algo clave para que entrenadores y atletas entiendan el porqué de la predicción y puedan plantear una estrategia. Además, capta relaciones no lineales de forma natural.
- **Naïve Bayes Gaussiano:** Elegido como modelo de referencia por su rapidez y simplicidad. A pesar del fuerte supuesto matemático de que todos los atributos son independientes entre sí, en la práctica da buenos resultados sin requerir grandes recursos de procesamiento. Sirve para calcular un porcentaje claro de ventaja.

## 4. Notas y Limpiezas
- Se removieron del LaTeX las métricas de la fase de Entrenamiento y las Matrices de Confusión previas para evitar contradicciones. El informe ahora exhibe exclusivamente los datos consolidados de Prueba (Test).
- Se corrigió la notación Big O y la tipografía en la justificación de complejidad algorítmica ($\mathcal{O}(n \cdot d \log(n))$ y $\mathcal{O}(\text{profundidad})$).
- **Regla Inquebrantable:** Ningún código del notebook `.ipynb` fue modificado directamente por el sistema. Las correcciones requeridas al código se proveen por chat.
