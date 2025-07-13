import time
from qiskit_optimization.applications import Knapsack
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler
<<<<<<< HEAD

# Datos del problema
values = [60, 100, 220]
weights = [1, 2, 3]
max_weight = 3

try:
    # Validar que el problema no sea trivial
    if max_weight >= sum(weights):
        raise ValueError("Error: El peso máximo no debe ser igual o mayor a la suma total de los pesos de los objetos.")

    # Crear el problema de la mochila como modelo QUBO
=======
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
>>>>>>> parent of 130a971 (Update formato codigo)
    kp = Knapsack(values, weights, max_weight)
    qp = kp.to_quadratic_program()
    qubo = QuadraticProgramToQubo().convert(qp)

<<<<<<< HEAD
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
=======
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
>>>>>>> parent of 130a971 (Update formato codigo)
    items_seleccionados = [i for i, selected in enumerate(variables) if selected > 0.5]
    peso_total = sum(weights[i] for i in items_seleccionados)
    valor_total = sum(values[i] for i in items_seleccionados)
    tiempo = end_time - start_time

<<<<<<< HEAD
    # Mostrar resultados
=======
>>>>>>> parent of 130a971 (Update formato codigo)
    print("\nResultados del problema de la mochila con QAOA:")
    print(f"Items seleccionados: {items_seleccionados}")
    print(f"Peso total: {peso_total}")
    print(f"Valor total: {valor_total}")
<<<<<<< HEAD
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos\n")
=======
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")

        # 🧠 Mostrar los bitstrings más probables
    eigenstate = result.min_eigen_solver_result.eigenstate
    if hasattr(eigenstate, 'binary_probabilities'):
        probs = eigenstate.binary_probabilities()
        print("\n🎯 Bitstrings más probables:")
        print(f"{'Bitstring':<10} {'Valor':>6} {'Peso':>6} {'Probabilidad':>14}")
        print("-" * 40)

        for bitstring, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True)[:10]:
            bits = [int(b) for b in bitstring[::-1][:len(weights)]]  # invertir y cortar a n bits
            peso = sum(weights[i] for i, b in enumerate(bits) if b)
            valor = sum(values[i] for i, b in enumerate(bits) if b)
            print(f"{bitstring:<10} {valor:>6} {peso:>6} {prob*100:>10.3f} %")
    else:
        print("⚠️ No se pudieron obtener probabilidades del estado final.")

    # Obtener parámetros desde result
    optimal_params = result.min_eigen_solver_result.optimal_point
    param_dict = dict(zip(qaoa.ansatz.parameters, optimal_params))
    bound_circuit = qaoa.ansatz.assign_parameters(param_dict)

    # Exportar circuito en QASM 2.0
    qasm_circuit = transpile(bound_circuit, basis_gates=["u3", "cx"], optimization_level=0)
    with open("qaoa_knapsack.qasm", "w") as f:
        f.write(qasm_circuit.qasm())

    print("✅ Circuito exportado correctamente como 'qaoa_knapsack.qasm'")
>>>>>>> parent of 130a971 (Update formato codigo)

except ValueError as e:
    print(f"\n[ERROR] {e}")
except Exception as e:
    print(f"\n[ERROR INESPERADO] {e}")