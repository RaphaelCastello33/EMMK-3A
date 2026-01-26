import numpy as np
import matplotlib.pyplot as plt
import math

def taylor_sin(x, order=3):
    approx = np.zeros_like(x)
    for n in range(order):
        approx += ((-1)**n) * x**(2*n+1) / math.factorial(2*n+1)
    return approx

# Tracer sur deux périodes de sin(x) pour voir un sinus complet
x = np.linspace(-2*np.pi, 2*np.pi, 400)
y_true = np.sin(x)

orders = [1, 3, 5, 7, 10]

plt.figure(figsize=(12,6))
plt.plot(x, y_true, label='sin(x)', color='black', linewidth=2)

for order in orders:
    y_approx = taylor_sin(x, order)
    plt.plot(x, y_approx, linestyle='--', label=f'Taylor order {order}')

# Ajuster l'échelle pour voir le sinus entier
plt.xlim(-2*np.pi, 2*np.pi)
plt.ylim(-1.2, 1.2)  # petit peu au-dessus et en dessous de [-1,1] pour le confort

plt.title('Approximation of sine(x) with Taylor series')
plt.xlabel('x')
plt.ylabel('y')
plt.xticks(
    [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
    ['-2π','-3π/2','-π','-π/2','0','π/2','π','3π/2','2π']
)
plt.grid(True)
plt.legend()
plt.show()
