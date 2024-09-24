from tkinter import simpledialog
from tkinter import Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import KMeans
import pandas as pd

def realizar_clustering(df, root):
    # Verificar si el DataFrame contiene las columnas necesarias
    if not all(col in df.columns for col in ['Glucemia', 'Frecuencia Cardiaca']):
        simpledialog.messagebox.showerror("Error", "El DataFrame debe contener las columnas 'Glucemia' y 'Frecuencia Cardiaca'.")
        return

    num_clusters = simpledialog.askinteger("Input", "¿Cuántos clusters quieres?", minvalue=1, maxvalue=10)
    if num_clusters is not None:
        columnas_clustering = ['Glucemia', 'Frecuencia Cardiaca']
        data_clustering = df[columnas_clustering].dropna()  # Eliminar filas con datos faltantes
        if data_clustering.empty:
            simpledialog.messagebox.showerror("Error", "No hay datos suficientes para realizar clustering.")
            return

        kmeans = KMeans(n_clusters=num_clusters)
        df['cluster'] = kmeans.fit_predict(data_clustering)

        top = Toplevel(root)
        fig, ax = plt.subplots()
        scatter = ax.scatter(df['Glucemia'], df['Frecuencia Cardiaca'], c=df['cluster'], cmap='viridis', s=60)
        plt.xlabel('Glucemia')
        plt.ylabel('Frecuencia Cardiaca')

        # Graficar los centros de los clusters
        centers = kmeans.cluster_centers_
        ax.scatter(centers[:, 0], centers[:, 1], c='red', marker='o')

        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.draw()
    else:
        simpledialog.messagebox.showwarning("Advertencia", "Número de clusters no especificado.")