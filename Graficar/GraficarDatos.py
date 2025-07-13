import numpy as np
import matplotlib.pyplot as plt

# Datos reales
objetos_reales = np.arange(0, 9)
tiempos_clasico_reales = np.array([0, 0.0005, 0.0006, 0.01, 0.02, 1, 3, 7, 10])
tiempos_cuantico_reales = np.array([0, 0.3, 0.4, 0.6, 0.6, 0.7, 0.8, 1, 1.01])

# Modelos de ajuste polinomial
modelo_clasico = np.poly1d(np.polyfit(objetos_reales, tiempos_clasico_reales, 3))
modelo_cuantico = np.poly1d(np.polyfit(objetos_reales, tiempos_cuantico_reales, 2))

# Generar datos hasta el objeto 20
objetos_total = np.arange(0, 21)
tiempos_clasico = np.array([
    tiempos_clasico_reales[i] if i < len(tiempos_clasico_reales) else modelo_clasico(i)
    for i in objetos_total
])
tiempos_cuantico = np.array([
    tiempos_cuantico_reales[i] if i < len(tiempos_cuantico_reales) else modelo_cuantico(i)
    for i in objetos_total
])

# Buscar punto de corte (donde cuántico es más rápido que clásico)
diferencias = tiempos_clasico - tiempos_cuantico
punto_corte_idx = np.where(diferencias > 0)[0]
punto_corte = punto_corte_idx[0] if len(punto_corte_idx) > 0 else None

# Ajustar el rango del gráfico
if punto_corte is not None:
    rango_max = min(len(objetos_total) - 1, punto_corte + 3)
else:
    rango_max = len(objetos_total) - 1

# Seleccionar el rango visible
objetos_visible = objetos_total[:rango_max + 1]
tiempos_clasico_visible = tiempos_clasico[:rango_max + 1]
tiempos_cuantico_visible = tiempos_cuantico[:rango_max + 1]

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(objetos_visible, tiempos_clasico_visible, 'b-', label='Clásico')
plt.plot(objetos_visible, tiempos_cuantico_visible, 'g-', label='Cuántico')

# Marcar el punto de corte si existe
if punto_corte is not None and punto_corte <= rango_max:
    plt.axvline(x=objetos_total[punto_corte], color='r', linestyle='--',
                label=f'Corte en {objetos_total[punto_corte]} objetos')
    plt.scatter(objetos_total[punto_corte], tiempos_clasico[punto_corte], color='red')

plt.xlabel('N° Objetos')
plt.ylabel('Tiempo de Ejecución (s)')
plt.title('Comparación de Tiempo: Clásico vs Cuántico')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
