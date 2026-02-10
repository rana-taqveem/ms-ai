import numpy as np
import matplotlib.pyplot as plt

# Constraint size
t = 1.0

# --- Circle (L2) ---
theta = np.linspace(0, 2*np.pi, 400)
x_circle = 0.7 * t * np.cos(theta)   # scaled smaller so it's inside diamond
y_circle = 0.7 * t * np.sin(theta)

# --- Diamond (L1) ---
diamond_x = np.array([t, 0, -t, 0, t])
diamond_y = np.array([0, t, 0, -t, 0])

# --- Plot ---
plt.figure(figsize=(6,6))
plt.plot(diamond_x, diamond_y, 'r-', linewidth=2, label='L1 (Lasso)')
plt.plot(x_circle, y_circle, 'b-', linewidth=2, label='L2 (Ridge)')

plt.gca().set_aspect('equal', 'box')
plt.xlim(-1.2*t, 1.2*t)
plt.ylim(-1.2*t, 1.2*t)
plt.title("L1 Diamond Enclosing L2 Circle")
plt.xlabel("$w_1$")
plt.ylabel("$w_2$")
plt.legend()
plt.grid(True)
plt.show()
