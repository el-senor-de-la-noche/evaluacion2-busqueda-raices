
#Generaremos un CSV con los valores de x y f(x) para cada función, un resumen de convergencia 
# de los métodos numéricos, un ambiente controlado para las funciones y todos los gráficos necesarios para el análisis.
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import metodos as m
from funciones import FUNCIONES, raiz_referencia

SRC = Path(__file__).resolve().parents[1]
DATA, ASSETS = SRC / "data", SRC / "assets"
DATA.mkdir(exist_ok=True); ASSETS.mkdir(exist_ok=True)
METODOS = ["Bisección", "Falsa posición", "Punto fijo", "Secante", "Newton-Raphson", "Newton mejorado"]


def _cerrado(metodo, f, ab):
    if ab is None:
        raise ValueError("sin intervalo: no hay cambio de signo")
    return metodo(f, *ab)


def correr(fn):
    """Ejecuta los 6 métodos; devuelve {método: dict(xs, ok, motivo, aplica)}."""
    f, df, d2f, g = fn["f"], fn["df"], fn["d2f"], fn["g"]
    llamadas = {
        "Bisección": lambda: _cerrado(m.biseccion, f, fn["ab"]),
        "Falsa posición": lambda: _cerrado(m.falsa_posicion, f, fn["ab"]),
        "Punto fijo": lambda: m.punto_fijo(g, fn["x0"], f=f),
        "Secante": lambda: m.secante(f, fn["x0"], fn["x1"]),
        "Newton-Raphson": lambda: m.newton(f, df, fn["x0"]),
        "Newton mejorado": lambda: m.newton_mejorado(f, df, d2f, fn["x0"]),
    }
    res = {}
    with np.errstate(all="ignore"):
        for nombre, call in llamadas.items():
            try:
                xs, ok, motivo = call()
                res[nombre] = dict(xs=xs, ok=ok, motivo=motivo, aplica=True)
            except ValueError as e:
                res[nombre] = dict(xs=[], ok=False, motivo=str(e), aplica=False)
    return res


if __name__ == "__main__":
    resumen, ambiente, todo = [], [], {}
    for fn in FUNCIONES:
        f, raiz = fn["f"], raiz_referencia(fn)
        fn["raiz_ref"] = raiz
        # CSV (x, f(x)) 
        if fn["ab"]:
            xa, xb = fn["ab"][0] - 0.25, fn["ab"][1] + 0.25
            if fn["clave"] in ("logaritmica", "mixta"):
                xa = max(xa, 0.01)
        else:
            xa, xb = 1.0, 3.0
        xs_plot = np.linspace(xa, xb, 400)
        with np.errstate(all="ignore"):
            ys_plot = f(xs_plot)
        np.savetxt(DATA / f"{fn['clave']}.csv", np.column_stack([xs_plot, ys_plot]),
                   delimiter=",", header="x,f(x)", comments="", fmt="%.10g")
        #  ambiente controlado 
        fr, dfr = float(f(raiz)), float(fn["df"](raiz))
        if fn["ab"]:
            a, b = fn["ab"]
            ambiente.append([fn["clave"], fn["nombre"], f"[{a}, {b}]", fn["x0"], fn["x1"], m.TOL, m.MAX_ITER,
                             f(a), f(b), f(a)*f(b), fr, dfr, "Bolzano: f(a)*f(b)<0 -> hay raíz en [a, b]"])
        else:
            ambiente.append([fn["clave"], fn["nombre"], "sin intervalo (f>=0 en todo x)", fn["x0"], fn["x1"], m.TOL,
                             m.MAX_ITER, "", "", "", fr, dfr,
                             "Tangencia: f(2)=0 y f'(2)=0, f(x)>=0 en todo x (toca el eje sin cruzarlo)"])
        #  métodos 
        res = correr(fn)
        todo[fn["clave"]] = res
        for nombre, r in res.items():
            if r["aplica"] and r["xs"]:
                xf = r["xs"][-1]
                resumen.append([fn["clave"], nombre, "sí", len(r["xs"]), xf, abs(xf - raiz), abs(f(xf)),
                                "sí" if r["ok"] else "no", r["motivo"]])
            else:
                resumen.append([fn["clave"], nombre, "no" if not r["aplica"] else "sí", "", "", "", "",
                                "no", r["motivo"]])

    with open(DATA / "resumen_convergencia.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["funcion", "metodo", "aplica", "iteraciones", "raiz", "error_abs", "f(raiz)", "convergio", "nota"])
        w.writerows(resumen)
    with open(DATA / "ambiente_controlado.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["funcion", "expresion", "intervalo", "x0", "x1", "tol", "max_iter", "f(a)", "f(b)", "f(a)*f(b)",
                    "f(raiz)", "f'(raiz)", "demostracion"])
        w.writerows(ambiente)
    with open(DATA / "historial_iteraciones.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["funcion", "metodo", "iteracion", "x", "error_abs"])
        for fn in FUNCIONES:
            for nombre, r in todo[fn["clave"]].items():
                for k, x in enumerate(r["xs"], 1):
                    w.writerow([fn["clave"], nombre, k, x, abs(x - fn["raiz_ref"])])

    #  gráficos: cada función con su raíz (y respaldo de Bolzano / tangencia) 
    for fn in FUNCIONES:
        d = np.loadtxt(DATA / f"{fn['clave']}.csv", delimiter=",", skiprows=1)
        fig, ax = plt.subplots(figsize=(7, 4.4))
        ax.plot(d[:, 0], d[:, 1], label=f"f(x) = {fn['nombre']}")
        ax.axhline(0, color="k", lw=0.8)
        if fn["ab"]:
            a, b = fn["ab"]
            fa, fb = fn["f"](a), fn["f"](b)
            ax.plot(a, fa, "g^", ms=8, label=f"a = {a:g},  f(a) = {fa:.4f}")
            ax.plot(b, fb, "gv", ms=8, label=f"b = {b:g},  f(b) = {fb:.4f}")
            sub = f"Bolzano: f(a)·f(b) = {fa*fb:.4f} < 0  |  tol = {m.TOL:g}, tope = {m.MAX_ITER}"
        else:
            ax.plot(fn["x0"], fn["f"](fn["x0"]), "ks", ms=7, label=f"x0 = {fn['x0']} (inicio métodos abiertos)")
            ax.annotate("tangencia al eje x\n(raíz doble)", (2, 0), (2.25, 0.55),
                        arrowprops=dict(arrowstyle="->"))
            sub = f"f(2) = 0, f'(2) = 0, f(x) ≥ 0 ∀x: toca el eje sin cruzarlo  |  tol = {m.TOL:g}, tope = {m.MAX_ITER}"
        ax.plot(fn["raiz_ref"], 0, "ro", ms=8, label=f"raíz ≈ {fn['raiz_ref']:.6f}")
        ax.set_xlabel("x"); ax.set_ylabel("f(x)")
        ax.set_title(f"{fn['categoria']}: f(x) = {fn['nombre']}\n{sub}", fontsize=9)
        ax.grid(alpha=0.3); ax.legend(fontsize=8)
        fig.tight_layout(); fig.savefig(ASSETS / f"funcion_{fn['clave']}.png", dpi=130); plt.close(fig)

    #  gráficos: convergencia |error| vs iteración 
    for fn in FUNCIONES:
        fig, ax = plt.subplots(figsize=(6.5, 4))
        for nombre, r in todo[fn["clave"]].items():
            if r["xs"]:
                err = np.maximum(np.abs(np.array(r["xs"]) - fn["raiz_ref"]), 1e-17)
                ax.semilogy(range(1, len(err) + 1), err, "o-", ms=4, label=nombre)
        ax.axhline(m.TOL, color="gray", ls="--", lw=0.8, label="tol = 1e-6")
        ax.set_xlabel("iteración"); ax.set_ylabel("|error| = |x_k − raíz|  (escala log)")
        ax.set_title(f"Convergencia: f(x) = {fn['nombre']}  (error 0 se dibuja en 1e-17)", fontsize=9)
        ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=7)
        fig.tight_layout(); fig.savefig(ASSETS / f"convergencia_{fn['clave']}.png", dpi=130); plt.close(fig)

    #  resumen de iteraciones por método y función 
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ancho = 0.13
    for i, nombre in enumerate(METODOS):
        vals = []
        for fn in FUNCIONES:
            r = todo[fn["clave"]][nombre]
            vals.append(len(r["xs"]) if (r["aplica"] and r["xs"]) else np.nan)
        pos = np.arange(len(FUNCIONES)) + (i - 2.5) * ancho
        ax.bar(pos, np.nan_to_num(vals), ancho, label=nombre)
        for p, v in zip(pos, vals):
            if np.isnan(v):
                ax.text(p, 0.5, "N/A", rotation=90, ha="center", fontsize=7)
    ax.set_xticks(np.arange(len(FUNCIONES))); ax.set_xticklabels([fn["clave"] for fn in FUNCIONES])
    ax.set_ylabel("iteraciones (tol = 1e-6)"); ax.set_xlabel("función")
    ax.set_title("Resumen de iteraciones por método y función (N/A = no aplica)")
    ax.legend(fontsize=7, ncol=3); ax.grid(alpha=0.3, axis="y")
    fig.tight_layout(); fig.savefig(ASSETS / "resumen_iteraciones.png", dpi=130); plt.close(fig)

    print(f"{'función':15s} {'método':16s} {'iter':>5s} {'raíz':>14s} {'error':>10s}  nota")
    for fila in resumen:
        it = fila[3] if fila[3] != "" else "-"
        rz = f"{fila[4]:.8f}" if fila[4] != "" else "-"
        er = f"{fila[5]:.2e}" if fila[5] != "" else "-"
        print(f"{fila[0]:15s} {fila[1]:16s} {str(it):>5s} {rz:>14s} {er:>10s}  {fila[8]}")