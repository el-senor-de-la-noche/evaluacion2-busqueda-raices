#Integrantes: Elias Gonzalez
#             Daniel Navarrete
#Ramo: Computacion Numerica
#Profesor: Juan Cabezas

import numpy as np

FUNCIONES = [
    dict(clave="polinomica", nombre="x^3 - x - 2", categoria="Polinómica (raíz simple)",
         f=lambda x: x**3 - x - 2, df=lambda x: 3*x**2 - 1, d2f=lambda x: 6*x,
         g=lambda x: np.cbrt(x + 2), g_txt="g(x)=(x+2)^(1/3)",
         ab=(1.0, 2.0), x0=1.5, x1=2.0, doble=False),
    dict(clave="doble", nombre="(x-2)^2", categoria="Polinómica (raíz doble)",
         f=lambda x: (x - 2)**2, df=lambda x: 2*(x - 2), d2f=lambda x: 2.0 + 0*x,
         g=lambda x: x - (x - 2)**2, g_txt="g(x)=x-(x-2)^2",
         ab=None, x0=1.2, x1=1.4, doble=True, raiz=2.0),
    dict(clave="logaritmica", nombre="ln(x) + x - 4", categoria="Logarítmica",
         f=lambda x: np.log(x) + x - 4, df=lambda x: 1/x + 1, d2f=lambda x: -1/x**2,
         g=lambda x: 4 - np.log(x), g_txt="g(x)=4-ln(x)",
         ab=(2.0, 3.0), x0=2.5, x1=3.0, doble=False),
    dict(clave="exponencial", nombre="e^(-x) - x", categoria="Exponencial",
         f=lambda x: np.exp(-x) - x, df=lambda x: -np.exp(-x) - 1, d2f=lambda x: np.exp(-x),
         g=lambda x: np.exp(-x), g_txt="g(x)=e^(-x)",
         ab=(0.0, 1.0), x0=0.5, x1=1.0, doble=False),
    dict(clave="trigonometrica", nombre="cos(x) - x", categoria="Trigonométrica",
         f=lambda x: np.cos(x) - x, df=lambda x: -np.sin(x) - 1, d2f=lambda x: -np.cos(x),
         g=lambda x: np.cos(x), g_txt="g(x)=cos(x)",
         ab=(0.0, 1.0), x0=0.5, x1=1.0, doble=False),
    dict(clave="mixta", nombre="sqrt(x) - cos(x)", categoria="Mixta",
         f=lambda x: np.sqrt(x) - np.cos(x),
         df=lambda x: 0.5/np.sqrt(x) + np.sin(x),
         d2f=lambda x: -0.25*x**-1.5 + np.cos(x),
         g=lambda x: (x + np.cos(x)**2) / 2, g_txt="g(x)=(x+cos(x)^2)/2",
         ab=(0.1, 1.0), x0=0.5, x1=1.0, doble=False),
]


def raiz_referencia(fn):
    # aqui nosotros calculamos la raíz de referencia usando el método de bisección, que es confiable 
    # para encontrar raíces en un intervalo donde la función cambia de signo. Si la función tiene una raíz doble,
    # simplemente devolvemos la raíz conocida.
    if "raiz" in fn:
        return fn["raiz"]
    a, b = fn["ab"]
    f = fn["f"]
    for _ in range(200):
        c = (a + b) / 2
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
    return (a + b) / 2
