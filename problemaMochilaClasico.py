import time

def knapsack_dp(values, weights, max_weight):
    n = len(values)
    dp = [[0 for w in range(max_weight + 1)] for i in range(n + 1)]

    # Llenar tabla DP
    for i in range(1, n + 1):
        for w in range(max_weight + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruir solución
    w = max_weight
    selected = [0] * n
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected[i - 1] = 1
            w -= weights[i - 1]

    total_value = dp[n][max_weight]
    return total_value, selected

# Datos de entrada
values = [120, 340, 180, 220, 90, 310]

weights = [10, 30, 20, 25, 5, 40]

max_weight = 100 

# Resolver
start_time = time.time()
total_value, selected_items = knapsack_dp(values, weights, max_weight)
end_time = time.time()

# Mostrar objetos seleccionados con peso y valor
print("\nObjetos seleccionados:")
for i in range(len(selected_items)):
    if selected_items[i]:
        print(f" - Objeto {i}: Peso = {weights[i]}, Valor = {values[i]}")

# Mostrar resultados
print("Valor total:", total_value)
print("Peso total:", sum(weights[i] for i in range(len(weights)) if selected_items[i] == 1))
print("Tiempo real de ejecución: {:.6f} segundos".format(end_time - start_time))
