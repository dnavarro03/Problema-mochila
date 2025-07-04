# Resolución y comparación de las soluciones cuanticas y clasicas del problema de la mochila
Este proyecto implementa y analiza la resolución del problema de la mochila (0-1) mediante computación cuántica, utilizando el algoritmo QAOA (Quantum Approximate Optimization Algorithm). Se compara el enfoque cuántico con la solución clásica para evaluar su escalabilidad, eficiencia y sus limitaciones con los recursos disponibles.

## Instalación

Entorno Qiskit  
Este proyecto usa Python 3.10+ y Qiskit. Puedes instalar las dependencias con:
```bash
pip install "qiskit==1.0.1" "qiskit-terra==0.25.0" "qiskit-aer==0.12.1" "qiskit-algorithms==0.3.0" "qiskit-optimization==0.6.1"
```

Entorno D-Wave  
Para resolver el mismo problema utilizando quantum annealing con D-Wave, se requiere:
```bash
pip install "dimod==0.12.20" "numpy==2.2.6" "setuptools==65.5.0"
```
