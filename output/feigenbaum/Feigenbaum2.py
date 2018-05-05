import numpy as np
import matplotlib.pyplot as plt

def logistic(r, x):
    return r*x*(1-x)

n = 10000
r = np.linspace(2.5, 4.0, n)

iterations = 1000
last = 100

x = 1e-5 * np.ones(n)

lyapunov = np.zeros(n)

plt.subplot(211)
for i in range(iterations):
    x = logistic(r, x)
    lyapunov += np.log(abs(r - 2*r*x))
    if i >= (iterations - last):
        plt.plot(r, x, ", k", alpha = 0.02)
plt.xlim(2.5, 4)
plt.title("Feigenbaum-Diagramm")

plt.subplot(212)
plt.plot(r[lyapunov < 0], lyapunov[lyapunov < 0]/iterations, ",k", alpha = 0.1)
plt.plot(r[lyapunov >= 0], lyapunov[lyapunov >= 0] / iterations, ",r", alpha = 0.25)
plt.xlim(2.5, 4.0)
plt.ylim(-2, 1)
plt.title("Lyapunov-Exponent")

plt.show()