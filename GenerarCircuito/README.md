## Generación de circuito cuántico

Este proyecto no solo resuelve el problema de la mochila mediante computación cuántica utilizando el algoritmo QAOA, sino que además **genera el circuito cuántico asociado a la solución óptima obtenida** y el **conjunto de bitstrings con mayor probabilidad**. Este circuito es exportado automáticamente al archivo `qaoa_knapsack.qasm` en formato **OpenQASM 2.0**, lo que permite visualizarlo y ejecutarlo en simuladores o QPUs reales compatibles con OpenQASM, como los de **IBM Quantum Composer**.

### Archivo generado

- `qaoa_knapsack.qasm`: contiene el circuito de QAOA generado con los parámetros óptimos (gamma, beta) resultantes del proceso de optimización.

### ¿Qué representa este circuito?

El circuito representa el *ansatz* de QAOA con los parámetros óptimos obtenidos para maximizar la función objetivo del problema de la mochila. Cada bit del registro cuántico corresponde a una posible inclusión de un objeto en la mochila (1: incluido, 0: excluido). El circuito puede ser interpretado como una receta de compuertas cuánticas que prepara un estado en superposición y lo guía hacia el óptimo usando una serie de operadores de mezcla y costo.

### ¿Cómo utilizar el circuito `.qasm`?

1. Accede a [IBM Quantum Composer](https://quantum.cloud.ibm.com/composer).
2. Inicia sesión
3. Abre un nuevo proyecto y selecciona "Import QASM".
4. Carga el archivo `qaoa_knapsack.qasm` generado.
5. Puedes simularlo usando `ibmq_qasm_simulator`.
6. Al finalizar la simulación, analiza la distribución de los bitstrings para identificar el estado más probable.

### Consideraciones

- El circuito generado se basa en la solución encontrada por el optimizador clásico (COBYLA) al aplicar QAOA en un entorno sin ruido (simulado).
- Este circuito **puede no coincidir exactamente** con la solución impresa por consola si el backend utilizado introduce ruido o si se modifica el número de repeticiones (`reps`) o la precisión del optimizador (`maxiter`).
- Para obtener mayor fidelidad al resultado esperado, se recomienda usar `optimization_level=0` al transpilar, lo cual evita transformaciones agresivas del circuito.