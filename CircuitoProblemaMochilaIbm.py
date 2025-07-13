import time
from qiskit_optimization.applications import Knapsack
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler
from qiskit import transpile
from qiskit.utils import algorithm_globals

def validarPeso(weights, max_weight):
    if max_weight >= sum(weights):
        raise ValueError("El peso máximo no debe ser igual o mayor a la suma total de los pesos.")

def construirQubo(values, weights, max_weight):
    knapsack = Knapsack(values, weights, max_weight)
    qp = knapsack.to_quadratic_program()
    return QuadraticProgramToQubo().convert(qp)

def configurarQAOA(maxiter, reps):
    sampler = Sampler()
    optimizer = COBYLA(maxiter=maxiter)
    return QAOA(sampler=sampler, optimizer=optimizer, reps=reps)

def resolverQubo(qaoa, qubo):
    solver = MinimumEigenOptimizer(qaoa)
    start = time.time()
    result = solver.solve(qubo)
    duration = time.time() - start
    return result, duration

def procesarResultado(result, values, weights):
    variables = result.x
    seleccionados = [i for i, v in enumerate(variables) if v > 0.5]
    peso = sum(weights[i] for i in seleccionados)
    valor = sum(values[i] for i in seleccionados)
    return seleccionados, peso, valor

def mostrarResultado(result, tiempo, values, weights):
    seleccionados, peso, valor = procesarResultado(result, values, weights)
    print("\n📊 Resultados del problema de la mochila con QAOA:")
    print(f"Items seleccionados: {seleccionados}")
    print(f"Peso total: {peso}")
    print(f"Valor total: {valor}")
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")

    eigenstate = result.min_eigen_solver_result.eigenstate
    if hasattr(eigenstate, 'binary_probabilities'):
        probs = eigenstate.binary_probabilities()
        print("\n🎯 Bitstrings más probables:")
        print(f"{'Bitstring':<10} {'Valor':>6} {'Peso':>6} {'Probabilidad':>14}")
        print("-" * 40)

        for bitstring, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True)[:10]:
            bits = [int(b) for b in bitstring[::-1][:len(weights)]]
            peso_b = sum(weights[i] for i, b in enumerate(bits) if b)
            valor_b = sum(values[i] for i, b in enumerate(bits) if b)
            print(f"{bitstring:<10} {valor_b:>6} {peso_b:>6} {prob*100:>10.3f} %")
    else:
        print("⚠️ No se pudieron obtener probabilidades del estado final.")

def exportarCircuito(qaoa, result, nombre_archivo="qaoa_knapsack.qasm"):
    optimal_params = result.min_eigen_solver_result.optimal_point
    param_dict = dict(zip(qaoa.ansatz.parameters, optimal_params))
    circuito = qaoa.ansatz.assign_parameters(param_dict)
    circuito_qasm = transpile(circuito, basis_gates=["u3", "cx"], optimization_level=0)

    with open(nombre_archivo, "w") as f:
        f.write(circuito_qasm.qasm())
    print(f"✅ Circuito exportado correctamente como '{nombre_archivo}'")

def main():
    # Parámetros del problema
    algorithm_globals.random_seed = 42
    values = [60, 100, 220]
    weights = [1, 2, 3]
    max_weight = 3
    reps = 3
    maxiter = 300

    try:
        validarPeso(weights, max_weight)
        qubo = construirQubo(values, weights, max_weight)
        qaoa = configurarQAOA(maxiter, reps)
        result, tiempo = resolverQubo(qaoa, qubo)
        mostrarResultado(result, tiempo, values, weights)
        exportarCircuito(qaoa, result)

    except ValueError as e:
        print(f"\n[ERROR] {e}")
    except Exception as e:
        print(f"\n[ERROR INESPERADO] {e}")

if __name__ == "__main__":
    main()