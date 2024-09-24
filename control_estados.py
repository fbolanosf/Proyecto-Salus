# Variables globales para controlar la visibilidad de las gráficas
mostrar_glucemia = False
mostrar_frecuencia = False
mostrar_sistolica = False
mostrar_diastolica = False

def alternar_glucemia():
    """Alternar la visibilidad de la gráfica de Glucemia y mostrar el estado."""
    global mostrar_glucemia
    mostrar_glucemia = not mostrar_glucemia
    print(f"Glucemia: {mostrar_glucemia}")

def alternar_frecuencia():
    """Alternar la visibilidad de la gráfica de Frecuencia Cardiaca y mostrar el estado."""
    global mostrar_frecuencia
    mostrar_frecuencia = not mostrar_frecuencia
    print(f"Frecuencia Cardiaca: {mostrar_frecuencia}")

def alternar_sistolica():
    """Alternar la visibilidad de la gráfica de Sistolica y mostrar el estado."""
    global mostrar_sistolica
    mostrar_sistolica = not mostrar_sistolica
    print(f"Sistolica: {mostrar_sistolica}")

def alternar_diastolica():
    """Alternar la visibilidad de la gráfica de Diastolica y mostrar el estado."""
    global mostrar_diastolica
    mostrar_diastolica = not mostrar_diastolica
    print(f"Diastolica: {mostrar_diastolica}")