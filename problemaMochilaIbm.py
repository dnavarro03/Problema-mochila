import time
from qiskit_optimization.applications import Knapsack
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler


def validar_datos(weights, max_weight):
    if max_weight >= sum(weights):
        raise ValueError("El peso máximo no debe ser igual o mayor a la suma total de los pesos.")

def construir_qubo_knapsack(values, weights, max_weight):
    problema_knapsack = Knapsack(values, weights, max_weight)
    qp = problema_knapsack.to_quadratic_program()
    qubo = QuadraticProgramToQubo().convert(qp)
    return qubo

def configurar_qaoa():
    sampler = Sampler()
    optimizador = COBYLA(maxiter=100)
    qaoa = QAOA(sampler=sampler, optimizer=optimizador, reps=1)
    return MinimumEigenOptimizer(qaoa)

def resolver_mochila_qaoa(qubo, solver):
    inicio = time.time()
    resultado = solver.solve(qubo)
    fin = time.time()
    return resultado, fin - inicio

def interpretar_resultado(resultado, values, weights):
    variables = resultado.x
    items = [i for i, val in enumerate(variables) if val > 0.5]
    peso = sum(weights[i] for i in items)
    valor = sum(values[i] for i in items)
    return items, peso, valor

def mostrar_resultados(items, peso, valor, tiempo):
    print("\nResultados del problema de la mochila con QAOA:")
    print(f"Items seleccionados: {items}")
    print(f"Peso total: {peso}")
    print(f"Valor total: {valor}")
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos\n")


def main():
    # Datos del problema
    values = [60, 100, 220]
    weights = [1, 2, 3]
    max_weight = 3

    try:
        validar_datos(weights, max_weight)

        qubo = construir_qubo_knapsack(values, weights, max_weight)
        solver = configurar_qaoa()

        resultado, tiempo = resolver_mochila_qaoa(qubo, solver)
        items, peso_total, valor_total = interpretar_resultado(resultado, values, weights)

        mostrar_resultados(items, peso_total, valor_total, tiempo)

    except ValueError as e:
        print(f"\n[ERROR] {e}")
    except Exception as e:
        print(f"\n[ERROR INESPERADO] {e}")

if __name__ == "__main__":
    main()
