#Respondiendo la pregunta 5, se puede observar que la elección del intervalo y de la estimación inicial
# tiene un impacto significativo en el número de iteraciones necesarias para que los métodos converjan a la raíz.
# En general, elegir un intervalo más cercano a la raíz o una estimación inicial más precisa tiende a reducir
# el número de iteraciones requeridas. Por otro lado, intervalos más amplios o estimaciones iniciales más alejadas
# de la raíz pueden aumentar el número de iteraciones o incluso llevar a la no convergencia del método.
import csv
from pathlib import Path
import numpy as np
import metodos as m
from funciones import FUNCIONES

DATA = Path(__file__).resolve().parents[1] / "data"
INTERVALOS = {
    "polinomica": [(1, 2), (0, 3), (-5, 5)],
    "logaritmica": [(2, 3), (1, 10), (0.5, 100)],
    "exponencial": [(0, 1), (-1, 2), (-10, 10)],
    "trigonometrica": [(0, 1), (-1, 2), (-10, 10)],
    "mixta": [(0.1, 1), (0.01, 3), (0.001, 10)],
}

#esta variable contiene los valores iniciales x0 que se utilizarán para cada función en los métodos iterativos.
X0S = {
    "polinomica": [1.5, 0.5, 5, -3],
    "logaritmica": [2.5, 0.5, 10, 50],
    "exponencial": [0.5, -2, 5, 20],
    "trigonometrica": [0.5, -3, 3, 10],
    "mixta": [0.5, 0.05, 2, 10],
    "doble": [1.2, 0.0, 3.5, 10],
}


def its(r):
    xs, ok, _ = r
    return len(xs) if ok else "no converge"


filas = []
with np.errstate(all="ignore"):
    for fn in FUNCIONES:
        k = fn["clave"]
        for a, b in INTERVALOS.get(k, []):
            for nom, met in (("Bisección", m.biseccion), ("Falsa posición", m.falsa_posicion)):
                try:
                    filas.append([k, nom, f"[{a}, {b}]", its(met(fn["f"], a, b))])
                except ValueError:
                    filas.append([k, nom, f"[{a}, {b}]", "no aplica"])
        for x0 in X0S[k]:
            filas.append([k, "Punto fijo", f"x0={x0}", its(m.punto_fijo(fn["g"], x0, f=fn["f"]))])
            filas.append([k, "Secante", f"x0={x0}, x1={x0+0.5}", its(m.secante(fn["f"], x0, x0 + 0.5))])
            filas.append([k, "Newton-Raphson", f"x0={x0}", its(m.newton(fn["f"], fn["df"], x0))])
            filas.append([k, "Newton mejorado", f"x0={x0}", its(m.newton_mejorado(fn["f"], fn["df"], fn["d2f"], x0))])

with open(DATA / "sensibilidad.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["funcion", "metodo", "intervalo_o_x0", "iteraciones"])
    w.writerows(filas)
for f_ in filas:
    print(f"{f_[0]:15s} {f_[1]:16s} {f_[2]:22s} {f_[3]}")