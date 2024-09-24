from tkinter import Toplevel, Frame, Label, LEFT
import numpy as np
import pandas as pd

# Función para inicializar variables acumulativas
def inicializar_acumuladores(df):
    acumuladores = {}
    for columna in df.columns:
        acumuladores[columna] = {
            'suma': 0.0,
            'suma_cuadrados': 0.0,
            'n': 0,
            'datos': []
        }
    return acumuladores

# Función para actualizar los acumuladores con nuevos datos
def actualizar_acumuladores(acumuladores, df, indice_actual):
    for columna in df.columns:
        if columna in df.columns:
            datos_col = df[columna][:indice_actual]
            if not datos_col.empty:
                acumuladores[columna]['datos'].extend(datos_col.tolist())
                acumuladores[columna]['suma'] += datos_col.sum()
                acumuladores[columna]['suma_cuadrados'] += (datos_col ** 2).sum()
                acumuladores[columna]['n'] = len(acumuladores[columna]['datos'])
    return acumuladores

# Función para calcular estadísticas en tiempo real
def calcular_estadisticas(acumuladores):
    estadisticas = {}
    for columna, acum in acumuladores.items():
        n = acum['n']
        if n > 0:
            media = acum['suma'] / n
            varianza = (acum['suma_cuadrados'] / n) - (media ** 2)
            desviacion = np.sqrt(varianza)
            
            # Contar outliers usando el criterio IQR
            datos_col = np.array(acum['datos'])
            q1 = np.percentile(datos_col, 25)
            q3 = np.percentile(datos_col, 75)
            iqr = q3 - q1
            outliers = np.sum((datos_col < q1 - 1.5 * iqr) | (datos_col > q3 + 1.5 * iqr))
            
            # Guardar estadísticas en un diccionario
            estadisticas[columna] = {
                'media': media,
                'desviacion': desviacion,
                'varianza': varianza,
                'outliers': outliers
            }
    
    return estadisticas

# Función para mostrar las estadísticas en tiempo real
def mostrar_estadisticas(df, root):
    top = Toplevel(root)
    top.title("Estadísticas")
    top.configure(bg="white")

    # Crear el contenedor para los recuadros
    frame_estadisticas = Frame(top, bg="white")
    frame_estadisticas.pack(fill='both', expand=True)

    etiquetas = {}
    acumuladores = inicializar_acumuladores(df)

    # Crear recuadros para cada columna
    for columna in df.columns:
        frame_columna = Frame(frame_estadisticas, relief='solid', bd=2, padx=10, pady=10, bg="white")
        frame_columna.pack(side=LEFT, padx=10, pady=10)
        
        # Título de la columna
        label_titulo = Label(frame_columna, text=columna, font=("Helvetica", 14, "bold"), bg="white", fg="black")
        label_titulo.pack()

        # Etiquetas para mostrar estadísticas
        etiquetas[columna] = {
            'media': Label(frame_columna, text="Media: ", font=("Helvetica", 12), bg="white", fg="black"),
            'desviacion': Label(frame_columna, text="Desviación Estándar: ", font=("Helvetica", 12), bg="white", fg="black"),
            'varianza': Label(frame_columna, text="Varianza: ", font=("Helvetica", 12), bg="white", fg="black"),
            'outliers': Label(frame_columna, text="Outliers: ", font=("Helvetica", 12), bg="white", fg="red")
        }
        
        # Empaquetar las etiquetas
        etiquetas[columna]['media'].pack()
        etiquetas[columna]['desviacion'].pack()
        etiquetas[columna]['varianza'].pack()
        etiquetas[columna]['outliers'].pack()

    # Función para actualizar las estadísticas en tiempo real
    def actualizar_estadisticas(indice_actual):
        # Actualizar acumuladores con los datos actuales
        acumuladores_actualizados = actualizar_acumuladores(acumuladores, df, indice_actual)
        estadisticas = calcular_estadisticas(acumuladores_actualizados)

        # Actualizar los valores de las etiquetas para cada columna
        for columna, stats in estadisticas.items():
            etiquetas[columna]['media'].config(text=f"Media: {int(stats['media'])}")
            etiquetas[columna]['desviacion'].config(text=f"Desviación Estándar: {int(stats['desviacion'])}")
            etiquetas[columna]['varianza'].config(text=f"Varianza: {int(stats['varianza'])}")
            etiquetas[columna]['outliers'].config(text=f"Outliers: {stats['outliers']}")

        # Actualizar el índice para la próxima actualización
        if indice_actual < len(df):
            top.after(1000, lambda: actualizar_estadisticas(indice_actual + 1))

    # Iniciar la actualización de estadísticas
    actualizar_estadisticas(1)
