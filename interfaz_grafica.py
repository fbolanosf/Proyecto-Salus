import tkinter as tk
from tkinter import filedialog
import pandas as pd
import clustering as cl
import graficas as gr
import estadisticas as est
import control_estados as ce

def iniciar_programa():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Análisis de Datos")

    # Leer archivo Excel
    ruta_archivo = filedialog.askopenfilename()
    if not ruta_archivo:
        return  # Salir si no se selecciona archivo

    df = pd.read_excel(ruta_archivo)

    # Crear botones para las acciones principales
    btn_clustering = tk.Button(root, text="Realizar Clustering", command=lambda: cl.realizar_clustering(df, root))
    btn_clustering.pack(pady=10)

    btn_graficos = tk.Button(root, text="Mostrar Gráficos", command=lambda: gr.abrir_ventana_graficos(df, root))
    btn_graficos.pack(pady=10)

    btn_estadisticas = tk.Button(root, text="Estadísticas Descriptivas", command=lambda: est.mostrar_estadisticas(df, root))
    btn_estadisticas.pack(pady=10)

    # Crear botones para alternar la visibilidad de las variables en las gráficas
    btn_glucemia = tk.Button(root, text="Glucemia", command=lambda: ce.alternar_glucemia())
    btn_glucemia.pack(pady=5)

    btn_frecuencia = tk.Button(root, text="Frecuencia Cardiaca", command=lambda: ce.alternar_frecuencia())
    btn_frecuencia.pack(pady=5)

    btn_sistolica = tk.Button(root, text="Sistólica", command=lambda: ce.alternar_sistolica())
    btn_sistolica.pack(pady=5)

    btn_diastolica = tk.Button(root, text="Diastólica", command=lambda: ce.alternar_diastolica())
    btn_diastolica.pack(pady=5)

    # Iniciar el loop principal de la ventana
    root.mainloop()