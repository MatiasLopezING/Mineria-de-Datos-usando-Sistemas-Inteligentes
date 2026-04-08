## 1) Medidas descriptivas (media, cuartiles, etc.)

Para una variable \(x_1,\dots,x_n\):

- Media: \(\bar{x}=\frac{1}{n}\sum x_i\)
- Mediana:
  - ordenar datos
  - si \(n\) impar: posición \((n+1)/2\)
  - si \(n\) par: promedio entre posiciones \(n/2\) y \(n/2+1\)
- Q1 y Q3: sobre datos ordenados (aclarar el criterio que usan, porque hay varios)
- RI: \(RI=Q3-Q1\)

En el informe:

- poner una tabla con valores ordenados y posiciones
- marcar qué elementos corresponden a Q1, mediana, Q3

---

## 2) Discretización por frecuencia (qcut “a mano”)

Para 2 intervalos:

1. Ordenar `Luminosidad`.
2. Dividir en dos grupos con igual cantidad de observaciones (o lo más parecido).
3. Definir cortes con esos valores frontera.
4. Mostrar:
   - Intervalo 1 (Baja): rango y cantidad
   - Intervalo 2 (Alta): rango y cantidad

En el informe:

- tabla de datos ordenados
- línea donde se parte en mitad
- rangos obtenidos + conteo por rango

---

## 3) Discretización por rango (cut “a mano”)

Para 2 intervalos de igual ancho:

1. Calcular mínimo y máximo.
2. Ancho: \(h=\frac{\max-\min}{2}\)
3. Intervalos:
   - I1: \([\min, \min+h)\)
   - I2: \([\min+h, \max]\) (aclarar inclusión de extremos)
4. Contar cuántos datos caen en cada intervalo.

En el informe:

- mostrar cálculo numérico de \(\min\), \(\max\), \(h\)
- tabla de conteos por intervalo

---

## 4) Correlación lineal (Pearson) “a mano”

Usar tabla con columnas:

- \(x=\) Luminosidad
- \(y=\) Temperatura
- \(x-\bar{x}\)
- \(y-\bar{y}\)
- \((x-\bar{x})(y-\bar{y})\)
- \((x-\bar{x})^2\)
- \((y-\bar{y})^2\)

Fórmula:
\[
r=\frac{\sum (x_i-\bar{x})(y_i-\bar{y})}
{\sqrt{\sum (x_i-\bar{x})^2\;\sum (y_i-\bar{y})^2}}
\]

Luego interpretar:

- signo de \(r\): positiva/negativa
- magnitud \(|r|\): débil/fuerte (aclarar criterio, por ejemplo: <0.3 baja, 0.3-0.7 media/débil-moderada, >0.7 fuerte)

---

## 5) Diagrama de Caja de Tukey “a mano”

1. Ordenar datos de Luminosidad.
2. Hallar Q1, Q2 (mediana), Q3.
3. \(RI=Q3-Q1\).
4. Límites de bigotes:
   - inferior: \(Q1-1.5RI\)
   - superior: \(Q3+1.5RI\)
5. Atípicos leves/extremos:
   - leves: fuera de \(1.5RI\)
   - extremos: fuera de \(3RI\), usando:
     - inferior extremo: \(Q1-3RI\)
     - superior extremo: \(Q3+3RI\)

En el informe:

- incluir tabla final como la consigna
- dibujar el boxplot (puede ser con software), pero acompañarlo con cuentas manuales
