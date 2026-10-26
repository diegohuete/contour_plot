Contour Plot: Rendimiento deportivo en Ironman Kona 2022

Objetivo
Explorar la relación entre la frecuencia cardíaca, la cadencia de carrera y la velocidad durante una competición de resistencia.

Visualización
El gráfico de contorno representa la velocidad estimada a partir de la combinación de dos variables: frecuencia cardíaca y cadencia.

- Eje X: frecuencia cardíaca (latidos/min).
- Eje Y: cadencia registrada (registros/min).
- Color e isolíneas: velocidad estimada (m/s).

Metodología
El análisis se ha realizado en Python con pandas, NumPy, Matplotlib y SciPy. Se han procesado los datos, seleccionado las variables relevantes e interpolado las observaciones para construir una superficie de contorno.

La interpolación permite visualizar patrones entre las observaciones, pero las zonas interpoladas deben interpretarse como estimaciones.


Datos
Los datos utilizados corresponden al registro deportivo de Gustav Iden durante el Campeonato Mundial de Ironman de Kona de 2022.

Fuente: Repositorio original de los datos en GitHub. El repositorio original indica una licencia CC BY-NC 4.0.

Tecnologías:
- Python
- pandas
- NumPy
- Matplotlib
- SciPy

Autoría: Diego García Huete.
Proyecto académico de Visualización de Datos.