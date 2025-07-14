import time

def knapsackDp(values, weights, max_weight):
    n = len(values)
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    # Llenar tabla de programación dinámica
    for i in range(1, n + 1):
        for w in range(max_weight + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruir solución óptima
    selected = reconstruirSeleccion(dp, weights, n, max_weight)
    total_value = dp[n][max_weight]

    return total_value, selected

def reconstruirSeleccion(dp, weights, n, max_weight):
    w = max_weight
    selected = [0] * n

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected[i - 1] = 1
            w -= weights[i - 1]

    return selected

def imprimirResultados(values, weights, selected, total_value, exec_time):
    print("\nObjetos seleccionados:")
    for i in range(len(selected)):
        if selected[i]:
            print(f" - Objeto {i}: Peso = {weights[i]}, Valor = {values[i]}")

    peso_total = sum(weights[i] for i in range(len(weights)) if selected[i])
    print(f"Valor total: {total_value}")
    print(f"Peso total: {peso_total}")
    print(f"Tiempo real de ejecución: {exec_time:.6f} segundos\n")



def main():
    # Datos de entrada
    values = [120, 340, 180, 220, 90, 310]
    weights = [10, 30, 20, 25, 5, 40]
    max_weight = 100

    # Resolver problema con medición de tiempo
    start = time.time()
    total_value, selected = knapsackDp(values, weights, max_weight)
    end = time.time()
    exec_time = end - start

    # Mostrar resultados
    imprimirResultados(values, weights, selected, total_value, exec_time)

if __name__ == "__main__":
    main()
