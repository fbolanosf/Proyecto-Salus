from tkinter import Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import control_estados as ce
import numpy as np

# Diccionario para almacenar los conteos acumulados de outliers
outliers_acumulados = {
    'Glucemia': 0,
    'Frecuencia Cardiaca': 0,
    'Sistolica': 0,
    'Diastolica': 0
}

def agregar_estadisticas(ax, data, label, color, color_outlier='red', color_out_of_range='red'):
    if not data.empty:
        # Calcular media y desviación estándar
        media = np.mean(data)
        desviacion = np.std(data)

        # Dibujar línea de media
        ax.axhline(y=media, color='green', linestyle='--', linewidth=1)

        # Dibujar líneas de desviación estándar
        ax.axhline(y=media + desviacion, color='orange', linestyle='--', linewidth=1)
        ax.axhline(y=media - desviacion, color='orange', linestyle='--', linewidth=1)

        # Identificar y dibujar outliers
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        outliers = data[(data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)]

        # Actualizar el conteo acumulado de outliers
        outliers_acumulados[label] += len(outliers)

        # Plotear los datos
        ax.plot(data.index, data, color=color, label=label)

        # Dibujar outliers en rojo
        if not outliers.empty:
            ax.scatter(outliers.index, outliers, color=color_outlier, edgecolor='black')

        # Dibujar la porción de la gráfica fuera del rango de desviación estándar en rojo
        if len(data) > 0:
            above_sd = data[data > media + desviacion]
            below_sd = data[data < media - desviacion]

            # Solo dibujar la porción fuera del rango
            if not above_sd.empty:
                ax.fill_between(above_sd.index, media + desviacion, above_sd, color=color_out_of_range, alpha=0.5)

            if not below_sd.empty:
                ax.fill_between(below_sd.index, media - desviacion, below_sd, color=color_out_of_range, alpha=0.5)

        # Añadir el recuadro de etiquetas con el conteo de outliers específico para esta serie de datos
        etiqueta_texto = f'Outliers: {outliers_acumulados[label]}'
        ax.text(0.95, 0.95, etiqueta_texto, transform=ax.transAxes, fontsize=6,  # Tamaño reducido a la mitad
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white'),
                color=color)  # Color del texto igual al color de la gráfica
    else:
        print(f"No hay datos para {label}")

def actualizar_graficos(df, axs, canvas, indice_actual):
    for ax in axs:
        ax.clear()

    # Verificar y graficar solo las columnas que deben mostrarse
    if ce.mostrar_glucemia and 'Glucemia' in df.columns:
        agregar_estadisticas(axs[0], df['Glucemia'][:indice_actual], 'Glucemia', 'blue')

    if ce.mostrar_frecuencia and 'Frecuencia Cardiaca' in df.columns:
        agregar_estadisticas(axs[1], df['Frecuencia Cardiaca'][:indice_actual], 'Frecuencia Cardiaca', 'green')

    if ce.mostrar_sistolica and 'Sistolica' in df.columns:
        agregar_estadisticas(axs[2], df['Sistolica'][:indice_actual], 'Sistolica', 'brown')

    if ce.mostrar_diastolica and 'Diastolica' in df.columns:
        agregar_estadisticas(axs[3], df['Diastolica'][:indice_actual], 'Diastolica', 'purple')

    for ax in axs:
        # Solo agregar la leyenda si hay datos que graficar
        if ax.get_legend_handles_labels()[1]:
            ax.legend()
        # Eliminar el título de la gráfica
        ax.set_title("")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")

    canvas.draw()

def abrir_ventana_graficos(df, root):
    top = Toplevel(root)
    top.title("Gráficas de Datos")

    # Crear la figura y los ejes
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))  # Ajuste a 2x2 para mostrar varias gráficas
    axs = axs.flatten()  # Convertir la matriz de ejes en un array plano
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.get_tk_widget().pack(fill='both', expand=True)

    # Verificar y mostrar las columnas del DataFrame
    print("Columnas del DataFrame en la ventana de gráficos:", df.columns)

    # Establecer el índice inicial para la actualización de gráficos
    indice_actual = 0
    actualizar_graficos(df, axs, canvas, indice_actual)
    
    # Actualizar gráficos cada segundo
    def actualizar():
        nonlocal indice_actual
        actualizar_graficos(df, axs, canvas, indice_actual)
        if indice_actual < len(df):
            indice_actual += 1
            top.after(1000, actualizar)
    
    # Iniciar la actualización de gráficos
    actualizar()
