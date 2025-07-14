import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# Datos reales y configuración

cantidades_objetos_reales = np.array([0, 3, 5, 7, 10])
tiempos_clasico_reales = np.array([0, 0.000013, 0.000016, 0.000033, 0.000042])
tiempos_cuantico_reales = np.array([0, 0.0010, 0.0010, 0.0010, 0.0020])
max_objetos_proyeccion = 20



# Funciones utilitarias

def forzar_monotonia_no_decreciente(arr):
    arr_mon = arr.copy()
    for i in range(1, len(arr_mon)):
        if arr_mon[i] < arr_mon[i - 1]:
            arr_mon[i] = arr_mon[i - 1]
    return arr_mon


def proyectar_tiempos(cantidades_objetos, cantidades_reales, tiempos_reales, grado_pol):
    """Interpola y proyecta los tiempos a futuro asegurando que no decrezcan."""
    interpolados = np.interp(cantidades_objetos, cantidades_reales, tiempos_reales)
    modelo = np.poly1d(np.polyfit(cantidades_reales, tiempos_reales, grado_pol))
    proyeccion = interpolados.copy()
    limite_real = cantidades_reales[-1]

    for i in range(limite_real + 1, len(cantidades_objetos)):
        proyeccion[i] = max(modelo(i), proyeccion[i - 1], 0)

    return forzar_monotonia_no_decreciente(proyeccion), modelo


def estimar_punto_corte_teorico(modelo_clasico, modelo_cuantico, limite_real):
    modelo_dif = modelo_clasico - modelo_cuantico
    coefs_dif = modelo_dif.coefficients[::-1]
    raices = Polynomial(coefs_dif).roots()
    reales_positivas = raices[np.isreal(raices)].real
    candidatas = [r for r in reales_positivas if r > limite_real]
    return min(candidatas) if candidatas else None


def detectar_punto_corte(diferencias):
    indices = np.where(diferencias > 0)[0]
    return indices[0] if len(indices) > 0 else None


def graficar_resultados(cantidades_objetos, tiempos_clasico, tiempos_cuantico,
                        punto_corte, punto_corte_teorico, max_objetos_proyeccion):
    plt.figure(figsize=(12, 6))
    plt.plot(cantidades_objetos, tiempos_clasico, 'b-', label='Clásico')
    plt.plot(cantidades_objetos, tiempos_cuantico, 'g-', label='Cuántico')

    if punto_corte is not None:
        x_corte = cantidades_objetos[punto_corte]
        plt.axvline(x=x_corte, color='r', linestyle='--', label=f'Corte en {x_corte} objetos')
        plt.scatter(x_corte, tiempos_clasico[punto_corte], color='red')
    elif punto_corte_teorico is not None and punto_corte_teorico > max_objetos_proyeccion:
        plt.text(
            0.5 * max_objetos_proyeccion,
            max(tiempos_clasico[-1], tiempos_cuantico[-1]) * 0.8,
            f"Corte estimado fuera del rango\n(~{int(punto_corte_teorico)} objetos)",
            fontsize=12, color='red', ha='center',
            bbox=dict(facecolor='white', edgecolor='red')
        )

    plt.xlabel('N° Objetos')
    plt.ylabel('Tiempo de Ejecución (s)')
    plt.title(f'Comparación de Tiempo: Clásico vs Cuántico (hasta {max_objetos_proyeccion} objetos)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Ejecución principal

cantidades_objetos = np.arange(0, max_objetos_proyeccion + 1)

tiempos_clasico, modelo_clasico = proyectar_tiempos(
    cantidades_objetos, cantidades_objetos_reales, tiempos_clasico_reales, grado_pol=3)

tiempos_cuantico, modelo_cuantico = proyectar_tiempos(
    cantidades_objetos, cantidades_objetos_reales, tiempos_cuantico_reales, grado_pol=1)

diferencias = tiempos_clasico - tiempos_cuantico

punto_corte = detectar_punto_corte(diferencias)
punto_corte_teorico = estimar_punto_corte_teorico(modelo_clasico, modelo_cuantico, cantidades_objetos_reales[-1])

# Mensajes en consola

if punto_corte is not None:
    print(f"[✔] Punto de corte detectado dentro del rango: desde {cantidades_objetos[punto_corte]} objetos.")
else:
    print("[!] No hay punto de corte dentro del rango proyectado.")
    if punto_corte_teorico is not None:
        print(f"[~] Estimación teórica: Cuántico sería más rápido desde aproximadamente {punto_corte_teorico:.2f} objetos.")
    else:
        print("[×] No se estima ningún cruce futuro: el modelo cuántico no alcanza al clásico.")

# Gráfico final

graficar_resultados(cantidades_objetos, tiempos_clasico, tiempos_cuantico,
                    punto_corte, punto_corte_teorico, max_objetos_proyeccion)
