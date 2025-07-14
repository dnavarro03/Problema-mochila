import time
from dimod import BinaryQuadraticModel, ExactSolver


def validarDatos(weights, max_weight):
    if max_weight >= sum(weights):
        raise ValueError("Error: El peso máximo debe ser menor que el peso total de todos los objetos.")

def construirQubo(values, weights, max_weight):
    num_items = len(values)
    Q = {}

    # Coeficientes lineales (objetivo: maximizar valor)
    for i in range(num_items):
        Q[(i, i)] = -values[i]

    # Penalización por violar restricción de peso
    A = sum(values) + 1

    # Términos cuadráticos para penalización (i ≠ j)
    for i in range(num_items):
        Q[(i, i)] += A * (weights[i] ** 2)  # Término cuadrático en la diagonal
        for j in range(i + 1, num_items):
            Q[(i, j)] = Q.get((i, j), 0) + 2 * A * weights[i] * weights[j]

    # Ajuste lineal por el término cruzado con peso máximo
    for i in range(num_items):
        Q[(i, i)] += -2 * A * max_weight * weights[i]

    return Q

def convertirABqm(Q):
    return BinaryQuadraticModel.from_qubo({(f'x_{i}', f'x_{j}'): coeff for (i, j), coeff in Q.items()})

def resolverBqm(bqm):
    solver = ExactSolver()
    inicio = time.time()
    sampleset = solver.sample(bqm)
    fin = time.time()
    return sampleset, fin - inicio

def interpretarSolucion(sampleset, values, weights):
    best_sample = sampleset.first.sample
    energy = sampleset.first.energy

    items_seleccionados = [
        i for i in range(len(values)) if best_sample.get(f'x_{i}', 0) > 0.5
    ]
    peso_total = sum(weights[i] for i in items_seleccionados)
    valor_total = sum(values[i] for i in items_seleccionados)

    return items_seleccionados, peso_total, valor_total, energy


def main():
    # Datos de entrada
    values = [60, 100, 120]
    weights = [1, 2, 3]
    max_weight = 3

    try:
        validarDatos(weights, max_weight)

        Q = construirQubo(values, weights, max_weight)
        bqm = convertirABqm(Q)
        print(f"QUBO (BQM) creado con {len(bqm.variables)} variables.")

        sampleset, tiempo = resolverBqm(bqm)
        print(f"Tiempo de ejecución: {tiempo:.4f} segundos")

        items, peso_total, valor_total, energia = interpretarSolucion(sampleset, values, weights)

        print(f"\nMejor solución (energía: {energia:.4f}):")
        print(f"Items seleccionados: {items}")
        print(f"Peso total: {peso_total}")
        print(f"Valor total: {valor_total}")
        print(f"Tiempo total: {tiempo:.4f} segundos\n")

    except ValueError as e:
        print(f"\n[ERROR] {e}")
    except Exception as e:
        print(f"\n[ERROR INESPERADO] {e}")


if __name__ == "__main__":
    main()
