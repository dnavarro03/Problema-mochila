import time
from itertools import combinations
from dimod import BinaryQuadraticModel, ExactSolver

# Datos del problema
values = [60, 100, 120]
weights = [1, 2, 3]
max_weight = 3
num_items = len(values)

try:
    # Validar peso máximo
    if max_weight >= sum(weights):
        raise ValueError("Error: El peso máximo debe ser menor que el peso total de todos los objetos.")

    # Construir QUBO manualmente
    Q = {}

    # Coeficientes lineales (valor negativo)
    for i in range(num_items):
        Q[(i, i)] = -values[i]

    # Coeficientes cuadráticos (restricción peso)
    penalty_coeff_A = sum(values) + 1 

    for i in range(num_items):
        Q[(i, i)] += penalty_coeff_A * (weights[i] ** 2)
        for j in range(i + 1, num_items):
            Q[(i, j)] = Q.get((i, j), 0) + 2 * penalty_coeff_A * weights[i] * weights[j]

    # Ajuste lineal para la restricción de peso
    for i in range(num_items):
        Q[(i, i)] += -2 * penalty_coeff_A * max_weight * weights[i]

    # Crear modelo BQM para D-Wave
    bqm = BinaryQuadraticModel.from_qubo({(f'x_{i}', f'x_{j}'): coeff for (i, j), coeff in Q.items()})

    print(f"QUBO (BQM) creado con {len(bqm.variables)} variables.")

    # Usar ExactSolver clásico y exacto
    solver = ExactSolver()

    start_time = time.time()
    sampleset = solver.sample(bqm) 
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time:.4f} segundos")

    # Obtener mejor solución y energía
    best_sample = sampleset.first.sample
    best_energy = sampleset.first.energy

    print(f"\nMejor solución (energía: {best_energy:.4f}):")
    
    # Extraer ítems seleccionados
    items_seleccionados = [i for i in range(num_items) if best_sample.get(f'x_{i}', 0) > 0.5]

    peso_total = sum(weights[i] for i in items_seleccionados)
    valor_total = sum(values[i] for i in items_seleccionados)

    print(f"Items seleccionados: {items_seleccionados}")
    print(f"Peso total: {peso_total}")
    print(f"Valor total: {valor_total}")
    print(f"Tiempo total: {execution_time:.4f} segundos\n")

except ValueError as e:
    print(f"\n[ERROR] {e}")
except Exception as e:
    print(f"\n[ERROR INESPERADO] {e}")
