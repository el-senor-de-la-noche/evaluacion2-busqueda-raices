#Integrantes: Elias Gonzalez
#             Daniel Navarrete
#Ramo: Computacion Numerica
#Profesor: Juan Cabezas


import numpy as np

TOL = 1e-6
MAX_ITER = 100

def _ok(x):
    return bool(np.isfinite(x)) and bool(np.abs(x) < 1e12)

def _parar(fx, paso, tol):
    return bool(np.abs(fx) < tol or (paso is not None and np.abs(paso) < tol ))

def biseccion(f, a, b, tol = TOL, max_iter = MAX_ITER):
    fa, fb = f(a), f(b)
    if fa*fb > 0:
        raise ValueError("No hay cambio de signo f(a)*f(b)>0")
    xs, c_prev = [], None
    for _ in range(max_iter):
        c = (a+b)/2
        fc = f(c)
        xs.append(c)
        if _parar(fc, None if c_prev is None else c -c_prev, tol):
            return xs, True, "okey"
        if fa*fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        c_prev = c
    return xs, False, "tope de iteraciones"

def falsa_posicion(f, a, b, tol = TOL, max_iter = MAX_ITER):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("no hay cambio de signo f(a)*f(b)>0")
    xs, c_prev = [], None
    for _ in range(max_iter):
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        xs.append(c)
        if _parar(fc, None if c_prev is None else c - c_prev, tol):
            return xs, True, "okey"
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        c_prev = c
    return xs, False, "tope de iteraciones"

def punto_fijo(g, x0, f=None, tol=TOL, max_iter=MAX_ITER):
    xs, x = [], x0
    for _ in range(max_iter):
        xn = g(x)
        if not _ok(xn):
            return xs, False, "diverge / sale del dominio"
        xs.append(xn)
        if _parar(f(xn) if f is not None else np.inf, xn - x, tol):
            return xs, True, "okey"
        x = xn
    return xs, False, "tope de iteraciones"

def secante(f, x0, x1, tol=TOL, max_iter=MAX_ITER):
    xs = []
    for _ in range(max_iter):
        f0, f1 = f(x0), f(x1)
        if f1 == f0:
            return xs, False, "f(x1)=f(x0): división por cero"
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        if not _ok(x2):
            return xs, False, "diverge"
        xs.append(x2)
        if _parar(f(x2), x2 - x1, tol):
            return xs, True, "okey"
        x0, x1 = x1, x2
    return xs, False, "tope de iteraciones"

def newton(f, df, x0, tol=TOL, max_iter=MAX_ITER):
    xs, x = [], x0
    for _ in range(max_iter):
        d = df(x)
        if d == 0 or not _ok(d):
            return xs, False, "f'(x)=0"
        xn = x - f(x) / d
        if not _ok(xn):
            return xs, False, "diverge"
        xs.append(xn)
        if _parar(f(xn), xn - x, tol):
            return xs, True, "okey"
        x = xn
    return xs, False, "tope de iteraciones"

def newton_mejorado(f, df, d2f, x0, tol=TOL, max_iter=MAX_ITER):
    xs, x = [], x0
    if np.abs(f(x)) < tol:
        return [x], True, "x0 ya es raíz"
    for _ in range(max_iter):
        fx, d, d2 = f(x), df(x), d2f(x)
        den = d * d - fx * d2
        if den == 0 or not _ok(den):
            return xs, False, "denominador 0"
        xn = x - fx * d / den
        if not _ok(xn):
            return xs, False, "diverge"
        xs.append(xn)
        if _parar(f(xn), xn - x, tol):
            return xs, True, "okey"
        x = xn
    return xs, False, "tope de iteraciones"