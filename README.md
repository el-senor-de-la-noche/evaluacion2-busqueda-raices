# Evaluacion2 — La raíz que se esconde

**Asignatura:** Computación Numérica  
**Institución:** Universidad Católica del Maule  
**Integrantes:** Elías González y Daniel Navarrete

En este proyecto realizamos la comparación de seis métodos de búsqueda de raíces (bisección, falsa posición, punto fijo,
secante, Newton-Raphson y Newton mejorado) sobre funciones polinómicas, logarítmica,
exponencial, trigonométrica y mixta, incluyendo un caso de raíz doble.

## Requisitos

- Python 3.10 o superior.
- NumPy.
- Matplotlib.
- Un entorno para ejecutar scripts de Python.
- Git, para administrar las versiones del proyecto.

## Estructura

```
evaluacion2-busqueda-raices/
├── README.md             <- este archivo: entorno y qué hace cada script
├── requirements.txt      <- numpy, matplotlib
├── informe.md            <- respuestas a las preguntas de convergencia + conclusión
└── src/
    ├── assets/           <- gráficos PNG generados
    ├── data/             <- CSV generados (por función y resúmenes)
    └── scripts/          <- todos los scripts de Python
```

## Entorno

Requiere Python 3.9 o superior.

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

Los scripts guardan sus resultados en `src/data/` y `src/assets/` (las crean si no existen). Ejecutar en este orden desde la carpeta `src/scripts`:

```bash
cd src/scripts
python ejecutar_todo.py
python orden_convergencia.py
python sensibilidad.py
```

## Descripción de los scripts

- **`funciones.py`:** define las funciones de prueba, sus derivadas, las funciones de iteración y los valores iniciales utilizados.
- **`metodos.py`:** implementa los seis métodos de búsqueda de raíces y sus criterios de parada.
- **`orden_convergenci.py`:** estima el orden de convergencia a partir de las aproximaciones obtenidas y genera un archivo CSV con los resultados.
- **`sensibilidad.py`:** compara el comportamiento de los métodos al modificar los intervalos y las estimaciones iniciales.

