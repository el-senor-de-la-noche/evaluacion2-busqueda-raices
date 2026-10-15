# Informe — La raíz que se esconde

Evaluación 2 — Laboratorio de Computación Numérica, UCM
Integrantes: Elías González, Daniel Navarrete

## 1. Objetivo

Implementar y comparar seis métodos numéricos para aproximar raíces, registrar las iteraciones y errores con tolerancia `1e-6` y máximo de 100 iteraciones, y analizar su convergencia mediante CSV y gráficos.

## 2. Ambiente controlado

**Parámetros comunes:** tolerancia `1e-6`, tope de `100` iteraciones y criterio de parada
`|f(xₙ)| < tol` **o** `|xₙ − xₙ₋₁| < tol`. El error que se reporta es el **error real**
`|xₙ − raíz|`, usando una raíz de referencia calculada con 200 pasos de bisección (o la raíz
exacta, en la raíz doble).

**Los seis métodos:** bisección, falsa posición, punto fijo, secante, Newton-Raphson y
Newton mejorado. Este último es el Newton para raíces múltiples:
`xₙ₊₁ = xₙ − f·f′ / (f′² − f·f″)`, que equivale a aplicar Newton a `u(x) = f(x)/f′(x)`,
función que tiene una raíz *simple* aunque `f` tenga una doble.





## 3. Resultados generales



## 4. Preguntas de convergencia

### P1. ¿Qué método convergió en menos iteraciones en cada función? ¿Por qué?


### P2. ¿Qué orden de convergencia tiene cada método y cómo se refleja en el gráfico |error| vs iteración?


### P3. ¿Qué métodos requieren un intervalo con cambio de signo y cuáles no?


### P4. En la raíz doble: ¿qué métodos fallan o no aplican y cuál se comporta mejor? ¿Por qué?


### P5. ¿Cómo influyen el intervalo inicial y la estimación inicial en las iteraciones y en si el método converge?


### P6. ¿Qué método recomiendan según el tipo de función, considerando velocidad y robustez?



## 4. Conclusión final

**¿Qué método elegir para cada tipo de función y por qué (velocidad vs robustez)?**


**¿Qué ocurrió en la raíz doble y qué dice sobre "tener raíz" frente a "cambiar de signo"?**


**¿Cómo cambió el número de iteraciones al mover el intervalo o la estimación inicial?**