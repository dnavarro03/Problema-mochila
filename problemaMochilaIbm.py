import time
from qiskit_optimization.applications import Knapsack
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler
from qiskit import transpile

# Datos del problema
values = [60, 100, 220]
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
    qaoa = QAOA(sampler=sampler, optimizer=optimizer_clasico, reps=2)

    # Convertir QUBO a operador de Ising (necesario para QAOA)
    operator, offset = qubo.to_ising()

    # Ejecutar y medir tiempo con QAOA directamente
    start_time = time.time()
    qaoa_result = qaoa.compute_minimum_eigenvalue(operator)
    end_time = time.time()

    # Recuperar solución del estado óptimo (bitstring más probable)
    eigenstate = qaoa_result.eigenstate
    bitstring = max(eigenstate.binary_probabilities().items(), key=lambda x: x[1])[0]
    variables = [int(bit) for bit in bitstring]

    # Extraer solución
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

    # Exportar el circuito con parámetros óptimos
    params = qaoa_result.optimal_point  # [gamma, beta]
    param_dict = dict(zip(qaoa.ansatz.parameters, params))
    bound_circuit = qaoa.ansatz.assign_parameters(param_dict)

    # Transpilar a compuertas válidas para OpenQASM 2.0
    qasm_circuit = transpile(bound_circuit, basis_gates=["u3", "cx"], optimization_level=0)

    # Exportar circuito a archivo .qasm
    with open("qaoa_knapsack.qasm", "w") as f:
        f.write(qasm_circuit.qasm())

    print("✅ Circuito exportado correctamente como 'qaoa_knapsack.qasm'")

except ValueError as e:
    print(f"\n[ERROR] {e}")
except Exception as e:
    print(f"\n[ERROR INESPERADO] {e}")