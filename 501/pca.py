import numpy as np
import matplotlib.pyplot as plt

# Centered data
Xc = np.array([
    [2, -0.4],
    [0, 1.6],
    [1, 0.6],
    [-1, -1.4],
    [-2, -0.4]
])

# Principal component (unit vector)
v1 = np.array([0.940272, 0.340425])

# Project onto v1
Z1 = Xc @ v1

# Reconstruct projected points back in 2D space
proj_points = np.outer(Z1, v1)

# Plot
plt.figure(figsize=(6,6))
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)

# Original points
plt.scatter(Xc[:,0], Xc[:,1], color='blue', label='Original (centered) points')

# PCA axis line
line = np.linspace(-3,3,10)
plt.plot(line*v1[0], line*v1[1], 'r--', label='First principal axis (v1)')

# Projected points
plt.scatter(proj_points[:,0], proj_points[:,1], color='orange', label='Projections (on v1)')

# Draw lines from each point to its projection
for i in range(len(Xc)):
    plt.plot([Xc[i,0], proj_points[i,0]], [Xc[i,1], proj_points[i,1]], 'k:', alpha=0.5)

plt.axis('equal')
plt.legend()
plt.title('Projection of Data onto First Principal Component')
plt.show()
