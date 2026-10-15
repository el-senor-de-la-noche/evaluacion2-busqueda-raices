#Integrantes: Elias Gonzalez
#             Daniel Navarrete
#Ramo: Computacion Numerica
#Profesor: Juan Cabezas



import csv
import subprocess
from pathlib import Path
import numpy as np
import metodos as m
from funciones import FUNCIONES, raiz_referencia
from ejecutar_todo import correr

SRC = Path(__file__).resolve().parents[1]
REPO = SRC.parent
fallas = 0


def chequea(cond, msg):
    global fallas
    print(("OK    " if cond else "FALLA ") + msg)
    fallas += (not cond)


#A) CORRECTITUD 
print("--- A) Correctitud de los métodos ---")
res_all = {fn["clave"]: correr(fn) for fn in FUNCIONES}
for fn in FUNCIONES:
    r0, res = raiz_referencia(fn), res_all[fn["clave"]]
    if fn["doble"]:
        continue
    for nom, r in res.items():
        chequea(r["aplica"] and r["ok"] and abs(r["xs"][-1] - r0) < 1e-5,
                f"{fn['clave']:15s} {nom:16s} converge a la raíz (error<1e-5)")
    a, b = fn["ab"]
    chequea(fn["f"](a) * fn["f"](b) < 0, f"{fn['clave']:15s} Bolzano f(a)·f(b)<0")

d = res_all["doble"]
chequea(not d["Bisección"]["aplica"] and not d["Falsa posición"]["aplica"], "doble: bisección y falsa posición NO aplican")
chequea(not d["Punto fijo"]["ok"], "doble: punto fijo (g=x-(x-2)^2) diverge desde 1.2")
chequea(len(d["Newton mejorado"]["xs"]) <= 2 and abs(d["Newton mejorado"]["xs"][-1] - 2) < 1e-9,
        "doble: Newton mejorado llega a 2 en ≤2 iteraciones")
chequea(len(d["Newton-Raphson"]["xs"]) > 5, "doble: Newton clásico es lento (convergencia lineal)")
chequea(abs(m.TOL - 1e-6) < 1e-18 and m.MAX_ITER >= 100, "tolerancia 1e-6 y tope de iteraciones ≥ 100")


def orden(fn, nombre):
    r0, f = raiz_referencia(fn), fn["f"]
    xs = []
    if nombre == "Newton":
        x = 3.0
        for _ in range(6):
            x = x - f(x) / fn["df"](x); xs.append(x)
    else:
        x0, x1 = 3.0, 3.5
        for _ in range(7):
            x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0)); xs.append(x2); x0, x1 = x1, x2
    e = np.abs(np.array(xs) - r0); e = e[e > 1e-12]
    return np.log(e[-1] / e[-2]) / np.log(e[-2] / e[-3])


p_n, p_s = orden(FUNCIONES[0], "Newton"), orden(FUNCIONES[0], "Secante")
chequea(1.7 < p_n < 2.3, f"orden Newton ≈ 2 (medido {p_n:.2f})")
chequea(1.3 < p_s < 1.9, f"orden secante ≈ 1.618 (medido {p_s:.2f})")

#B) RÚBRICA 
print("\n--- B) Rúbrica ---")
# T1
for nombre in ["biseccion", "falsa_posicion", "punto_fijo", "secante", "newton", "newton_mejorado"]:
    chequea(hasattr(m, nombre), f"T1 método implementado: {nombre}")
# T2
claves = [fn["clave"] for fn in FUNCIONES]
chequea(len(FUNCIONES) >= 6 and any(fn["doble"] for fn in FUNCIONES), "T2 ≥5 categorías + una raíz doble")
chequea(all(c in claves for c in ["polinomica", "logaritmica", "exponencial", "trigonometrica", "mixta", "doble"]),
        "T2 polinómica, logarítmica, exponencial, trigonométrica, mixta y doble")
# T3
amb = SRC / "data" / "ambiente_controlado.csv"
if amb.exists():
    filas = list(csv.DictReader(open(amb, encoding="utf-8")))
    chequea(len(filas) == len(FUNCIONES) and all(float(f["tol"]) == 1e-6 for f in filas),
            "T3 ambiente controlado: todas las funciones con tol 1e-6 y tope declarado")
    chequea(all(f["demostracion"] for f in filas), "T3 demostración de la raíz (Bolzano / tangencia) en cada función")
else:
    chequea(False, "T3 falta src/data/ambiente_controlado.csv (ejecuta ejecutar_todo.py)")
# T4
ok4 = all((SRC / "data" / f"{c}.csv").exists() for c in claves)
chequea(ok4, "T4 un CSV (x, f(x)) por función")
if ok4:
    chequea(all(open(SRC / "data" / f"{c}.csv", encoding="utf-8").readline().strip() == "x,f(x)" for c in claves),
            "T4 columnas exactas: x,f(x)")
rc = SRC / "data" / "resumen_convergencia.csv"
if rc.exists():
    filas = list(csv.DictReader(open(rc, encoding="utf-8")))
    chequea(len(filas) == 36 and {"iteraciones", "raiz", "error_abs"} <= set(filas[0]),
            "T4 resumen de convergencia (6 funciones × 6 métodos con iteraciones, raíz y error)")
else:
    chequea(False, "T4 falta resumen_convergencia.csv")
# T5
for c in claves:
    chequea((SRC / "assets" / f"funcion_{c}.png").exists(), f"T5 gráfico de la función con su raíz: {c}")
    chequea((SRC / "assets" / f"convergencia_{c}.png").exists(), f"T5 gráfico |error| vs iteración (log): {c}")
chequea((SRC / "assets" / "resumen_iteraciones.png").exists(), "T5 resumen de iteraciones por método y función")
# T6
inf = REPO / "informe.md"
if inf.exists():
    t = inf.read_text(encoding="utf-8")
    for k in ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"]:
        chequea(f"### {k}" in t, f"T6 informe responde la pregunta {k}")
    chequea("## 4. Conclusión" in t, "T6/B2 informe cierra con conclusión")
else:
    print("PEND  T6 falta informe.md: lo redactan ustedes con sus datos y gráficos")
# T7
chequea((REPO / "README.md").exists() and (REPO / "requirements.txt").exists(), "T7 README.md y requirements.txt en la raíz")
if (REPO / "README.md").exists():
    rd = (REPO / "README.md").read_text(encoding="utf-8")
    chequea("venv" in rd and "pip install -r requirements.txt" in rd, "T7 README explica el entorno (venv)")
    scripts = [p.name for p in (SRC / "scripts").glob("*.py")]
    chequea(all(s in rd for s in scripts), f"T7 README describe cada script ({len(scripts)} scripts)")
if (REPO / "requirements.txt").exists():
    rq = (REPO / "requirements.txt").read_text(encoding="utf-8").lower()
    chequea("numpy" in rq and "matplotlib" in rq, "T7 requirements.txt contiene numpy y matplotlib")
chequea(all((SRC / d_).is_dir() for d_ in ["assets", "data", "scripts"]), "T7 carpetas src/assets, src/data, src/scripts")
# T8 (solo si es repo git)
def git(*a):
    return subprocess.run(["git", "-C", str(REPO), *a], capture_output=True, text=True)
if git("rev-parse", "--is-inside-work-tree").stdout.strip() == "true":
    ramas = [r.strip("* ").strip() for r in git("branch", "--list").stdout.splitlines()]
    chequea("main" in ramas and 2 <= len(ramas) <= 3, f"T8 2 o 3 ramas con main (ramas: {ramas})")
    sin_main = [r for r in ramas if r != "main" and git("rev-list", f"main..{r}").stdout.strip()]
    chequea(not sin_main, f"T8 todo el código de las ramas está integrado en main (pendientes: {sin_main})")
    chequea(len(git("log", "--oneline", "main").stdout.splitlines()) >= 3, "T8 historial de commits en main")
else:
    print("PEND  T8 no es un repositorio git todavía: ver comandos en el README")

print("\nTODO CORRECTO" if fallas == 0 else f"\n{fallas} prueba(s) fallaron")