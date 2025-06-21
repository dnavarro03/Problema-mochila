import time
from qiskit_optimization.applications import Knapsack
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

# Datos del problema
values = [60, 100, 120]
weights = [1, 2, 3]
max_weight = 3

try:
    # Validar que el problema no sea trivial
    if max_weight >= sum(weights):
        raise ValueError("Error: El peso máximo no debe ser igual o mayor a la suma total de los pesos de los objetos.")

    # Crear el problema de la mochila como modelo QUBO
    kp = Knapsack(values, weights, max_weight)
    qp = kp.to_quadratic_program()
    qubo = QuadraticProgramToQubo().convert(qp)

    # Crear sampler y optimizador clásico
    sampler = Sampler()
    optimizer_clasico = COBYLA(maxiter=100)

    # Crear instancia QAOA
    qaoa = QAOA(sampler=sampler, optimizer=optimizer_clasico, reps=1)

    # Ejecutar y medir tiempo
    start_time = time.time()
    solver = MinimumEigenOptimizer(qaoa)
    resultado = solver.solve(qubo)
    end_time = time.time()

    # Extraer resultados
    variables = resultado.x
    items_seleccionados = [i for i, selected in enumerate(variables) if selected > 0.5]
    peso_total = sum(weights[i] for i in items_seleccionados)
    valor_total = sum(values[i] for i in items_seleccionados)
    tiempo = end_time - start_time

    # Mostrar resultados
    print("\nResultados del problema de la mochila con QAOA:")
    print(f"Items seleccionados: {items_seleccionados}")
    print(f"Peso total: {peso_total}")
    print(f"Valor total: {valor_total}")
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos\n")

except ValueError as e:
    print(f"\n[ERROR] {e}")
except Exception as e:
    print(f"\n[ERROR INESPERADO] {e}")
