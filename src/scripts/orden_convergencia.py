#Integrantes: Elias Gonzalez Daniel Navarrete

import csv
from pathlib import Path
import numpy as np
import metodos as m
from funciones import FUNCIONES

DATA = Path(__file__).resolve().parents[1] / "data"


def orden(xs):
    d = np.abs(np.diff(np.array(xs, dtype=float)))
    d = d[np.isfinite(d) & (d > 1e-14)]
    ps = []
    for k in range(1, len(d) - 1):
        if d[k] < d[k - 1] and d[k + 1] < d[k]:
            ps.append(np.log(d[k + 1] / d[k]) / np.log(d[k] / d[k - 1]))
    return float(np.median(ps)) if ps else float("nan")


filas = []
with np.errstate(all="ignore"):
    for fn in FUNCIONES:
        f, df, d2f, g, t = fn["f"], fn["df"], fn["d2f"], fn["g"], 1e-15
        xn0 = fn["ab"][1] if fn["ab"] else fn["x0"]   # partir más lejos da más puntos medibles
        corridas = {"Punto fijo": m.punto_fijo(g, fn["x0"], f=f, tol=t),
                    "Secante": m.secante(f, fn["x0"], fn["x1"], tol=t),
                    "Newton-Raphson": m.newton(f, df, xn0, tol=t),
                    "Newton mejorado": m.newton_mejorado(f, df, d2f, xn0, tol=t)}
        if fn["ab"]:
            corridas["Bisección"] = m.biseccion(f, *fn["ab"], tol=t)
            corridas["Falsa posición"] = m.falsa_posicion(f, *fn["ab"], tol=t)
        for nombre, (xs, _, _) in corridas.items():
            filas.append([fn["clave"], nombre, orden(xs)])

with open(DATA / "orden_convergencia.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["funcion", "metodo", "orden_estimado"])
    w.writerows(filas)
for f_ in filas:
    print(f"{f_[0]:15s} {f_[1]:16s} p ≈ {f_[2]:.2f}")
