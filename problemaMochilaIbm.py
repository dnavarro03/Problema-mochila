import time
from qiskit_optimization.applications import Knapsack
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler
from qiskit import transpile
from qiskit.utils import algorithm_globals

# Variables del problema
algorithm_globals.random_seed = 42
values = [60, 100, 220]
weights = [1, 2, 3]
max_weight = 3
reps = 3
maxiter = 300

try:
    if max_weight >= sum(weights):
        raise ValueError("Error: El peso máximo no debe ser igual o mayor a la suma total de los pesos de los objetos.")

    # Crear modelo QUBO
    kp = Knapsack(values, weights, max_weight)
    qp = kp.to_quadratic_program()
    qubo = QuadraticProgramToQubo().convert(qp)

    # Sampler y optimizador
    sampler = Sampler()
    optimizer = COBYLA(maxiter=maxiter)
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    solver = MinimumEigenOptimizer(qaoa)

    # Resolver
    start_time = time.time()
    result = solver.solve(qubo)
    end_time = time.time()

    # Resultado final
    variables = result.x
    items_seleccionados = [i for i, selected in enumerate(variables) if selected > 0.5]
    peso_total = sum(weights[i] for i in items_seleccionados)
    valor_total = sum(values[i] for i in items_seleccionados)
    tiempo = end_time - start_time

    print("\nResultados del problema de la mochila con QAOA:")
    print(f"Items seleccionados: {items_seleccionados}")
    print(f"Peso total: {peso_total}")
    print(f"Valor total: {valor_total}")
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")

    # Obtener parámetros desde result
    optimal_params = result.min_eigen_solver_result.optimal_point
    param_dict = dict(zip(qaoa.ansatz.parameters, optimal_params))
    bound_circuit = qaoa.ansatz.assign_parameters(param_dict)

    # Exportar circuito en QASM 2.0
    qasm_circuit = transpile(bound_circuit, basis_gates=["u3", "cx"], optimization_level=0)
    with open("qaoa_knapsack.qasm", "w") as f:
        f.write(qasm_circuit.qasm())

    print("✅ Circuito exportado correctamente como 'qaoa_knapsack.qasm'")

except ValueError as e:
    print(f"\n[ERROR] {e}")
except Exception as e:
    print(f"\n[ERROR INESPERADO] {e}")