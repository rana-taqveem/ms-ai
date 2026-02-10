import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import cm

num_of_combinations = 50000
v1 = np.random.randn(3)
v2 = np.random.randn(3)
v3 = np.random.randn(3)

vectors = np.array([v1, v2, v3])
fig = plt.figure(figsize=(16,4))

def linear_combinations(num_of_combinations, vectors, fig):
    
    ax1 = fig.add_subplot(1, 4, 1, projection ='3d')
    
    coefficients = np.random.uniform(-1, 1, (num_of_combinations, 3))
    linear_combinations = coefficients @ vectors
    
    z_colors =linear_combinations[:, 2]
    ax1.scatter(linear_combinations[:, 0],
            linear_combinations[:, 1], 
            linear_combinations[:, 2], 
            c=z_colors,
            label='Linear Combination', 
            alpha=0.07, 
            cmap=cm.coolwarm,
            zorder=1,
            s=3)

    v1 = vectors[0, :]
    v2 = vectors[1, :]
    v3 = vectors[2, :]
    ax1.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='r', label='v1', lw=2, zorder=10)
    ax1.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='g', label='v2', lw=2, zorder=10)
    ax1.quiver(0, 0, 0, v3[0], v3[1], v3[2], color='b', label='v3', lw=2, zorder=10)
    ax1.scatter(vectors[:, 0], vectors[:, 1], vectors[:, 2], color='k', s=20, zorder=11, label='Vectot Tips')
    lim = np.max(np.abs(linear_combinations)) * 1.1
    ax1.set_xlim([-lim, lim])
    ax1.set_ylim([-lim, lim])
    ax1.set_zlim([-lim, lim])
    ax1.set_xlabel('X-axis')
    ax1.set_ylabel('Y-axis')
    ax1.set_zlabel('Z-axis')
    ax1.set_title("Linear Combination")
    ax1.grid(True)
    
    
def affine_combinations(num_of_combinations, vectors, fig):
    
    v1 = vectors[0, :]
    v2 = vectors[1, :]
    v3 = vectors[2, :]
    
    c1 = np.linspace(-2, 3, 10)
    c2 = np.linspace(-2, 3, 10)
    C1, C2 = np.meshgrid(c1, c2)
    C3 = 1 - C1 - C2

    X = C1*v1[0] + C2*v2[0] + C3*v3[0]
    Y = C1*v1[1] + C2*v2[1] + C3*v3[1]
    Z = C1*v1[2] + C2*v2[2] + C3*v3[2]
    
    ax2 = fig.add_subplot(1,3,2, projection = '3d')
    ax2.plot_surface(X, Y, Z, alpha=0.7, cmap=cm.coolwarm)
    ax2.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='r', label='v1', lw=2)
    ax2.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='g', label='v2', lw=2)
    ax2.quiver(0, 0, 0, v3[0], v3[1], v3[2], color='b', label='v3', lw=2)
    ax2.scatter(vectors[:, 0], vectors[:, 1], vectors[:, 2], color='k', s=20)
    ax2.set_xlabel('X-axis')
    ax2.set_ylabel('Y-axis')
    ax2.set_zlabel('Z-axis')
    ax2.set_title("Affine Combination")
    ax2.grid(True)

def convex_combinations(num_of_combinations, v1, v2, v3, fig):
    
    V = np.vstack([v1, v2, v3])
    coefficients = np.abs(np.random.rand(num_of_combinations, 3))
    coefficients = coefficients / coefficients.sum(axis=1, keepdims=True)
    
    convex_combinations = coefficients @ V

    ax3 = fig.add_subplot(1,3,3, projection = '3d')
    
    z_colors =convex_combinations[:, 2]
    ax3.scatter(convex_combinations[:, 0],
            convex_combinations[:, 1], 
            convex_combinations[:, 2], 
            c=z_colors,
            label='Linear Combination', 
            alpha=0.03, 
            cmap=cm.coolwarm,
            s=5)
    
    ax3.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='r', label='v1', lw=2)
    ax3.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='g', label='v2', lw=2)
    ax3.quiver(0, 0, 0, v3[0], v3[1], v3[2], color='b', label='v3', lw=2)
    ax3.scatter(V[:, 0], V[:, 1], V[:, 2], color='k', s=20)
    
    lim = np.max(np.abs(convex_combinations)) * 1.1
    ax3.set_xlim([-lim, lim])
    ax3.set_ylim([-lim, lim])
    ax3.set_zlim([-lim, lim])
    
    ax3.set_xlabel('X-axis')
    ax3.set_ylabel('Y-axis')
    ax3.set_zlabel('Z-axis')
    ax3.set_title("Convex Combination")
    ax3.grid(True)
    
linear_combinations(num_of_combinations, vectors, fig)
affine_combinations(num_of_combinations, vectors, fig)
convex_combinations(num_of_combinations, v1, v2, v3, fig)
plt.show()
