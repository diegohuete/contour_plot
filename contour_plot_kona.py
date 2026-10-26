import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


#1. Cargamos los datos públicos
url = (
    "https://raw.githubusercontent.com/entalpi-no/"
    "kona-2022/main/gustav_iden_copyright_entalpi_as.csv"
)

df = pd.read_csv(url)

print("Dimensiones originales:", df.shape)
print(df.head())


#2. Seleccionamos y limpiamos las variables
columnas = ["speed", "heartrate", "cadence"]
df = df[columnas].copy()
df = df.dropna(subset=columnas)

# Eliminar registros sin movimiento o con valores no válidos.
df = df[
    (df["speed"] > 0.5) &
    (df["heartrate"].between(100, 190)) &
    (df["cadence"] > 0)
].copy()

#Reducimos el peso de las observaciones repetidas:
#Agrupamos por frecuencia cardiaca y cadencia redondeadas.
df["heartrate_bin"] = df["heartrate"].round().astype(int)
df["cadence_bin"] = df["cadence"].round().astype(int)

datos = (
    df.groupby(["heartrate_bin", "cadence_bin"], as_index=False)
      .agg(
          speed=("speed", "mean"),
          n=("speed", "size")
      )
)

#Evitamos interpretar como representativas las combinaciones que solo aparecen una vez.
datos = datos[datos["n"] >= 2].copy()

print("Combinaciones disponibles:", len(datos))

#3. Preparar la superficie de interpolación

x = datos["heartrate_bin"].to_numpy()
y = datos["cadence_bin"].to_numpy()
z = datos["speed"].to_numpy()

#Creamos una cuadrícula regular.
xi = np.linspace(x.min(), x.max(), 150)
yi = np.linspace(y.min(), y.max(), 150)

X, Y = np.meshgrid(xi, yi)

#Interpolamos la velocidad en cada punto de la cuadrícula.
Z = griddata(
    points=(x, y),
    values=z,
    xi=(X, Y),
    method="linear"
)

#4. Dibujar el Contour Plot

fig, ax = plt.subplots(figsize=(11, 7))

niveles = np.linspace(
    np.nanpercentile(Z, 5),
    np.nanpercentile(Z, 95),
    12
)

relleno = ax.contourf(
    X, Y, Z,
    levels=niveles,
    cmap="viridis"
)

lineas = ax.contour(
    X, Y, Z,
    levels=niveles,
    colors="black",
    linewidths=0.6,
    alpha=0.6
)

ax.clabel(lineas, inline=True, fontsize=8, fmt="%.1f")

barra = fig.colorbar(relleno, ax=ax)
barra.set_label("Velocidad estimada (m/s)")

ax.set_title(
    "Rendimiento al límite: velocidad, frecuencia cardiaca y cadencia",
    fontsize=14,
    pad=15
)

ax.set_xlabel("Frecuencia cardiaca (latidos/min)")
ax.set_ylabel("Cadencia de carrera (registros/min)")

ax.grid(alpha=0.15)
fig.tight_layout()

from pathlib import Path

#Guardamos el gráfico en el escritorio
ruta_salida = Path.home() / "Desktop" / "contour_ironman_kona.png"

fig.savefig(
    ruta_salida,
    dpi=300,
    bbox_inches="tight"
)

print(f"Gráfico guardado correctamente en: {ruta_salida}")

plt.show()