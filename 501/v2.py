import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# --- 1. Setup ---
N = 1000  # Number of points

# Create 3 linearly independent basis vectors (as 3x1 columns)
v1 = np.array([3, 1, 1])
v2 = np.array([1, 2, -1])
v3 = np.array([1, -1, 3])

# Stack them into a (3, 3) matrix for matrix multiplicationa
# We use .T so that each *row* is a vector
V = np.array([v1, v2, v3]).T

# Create the figure
fig = plt.figure(figsize=(20, 7))
fig.suptitle('Visualizing Vector Combinations in R3', fontsize=16)

# --- 2. Plot 1: Linear Combination (2D Slice) ---
# This plot is intentionally misleading to contrast with the others.
# It only shows the span of v1 and v2.
ax1 = fig.add_subplot(1, 3, 1, projection='3d')
ax1.set_title("Linear Combination (Span of v1, v2)")

# Generate coefficients from a UNIFORM distribution (gives a square)
coeffs_2d = np.random.uniform(-1, 1, (N, 2))
# Get combinations of only v1 and v2
# We use V[:, :2] to select just the first two vectors
linear_points = coeffs_2d @ V[:, :2].T

ax1.scatter(linear_points[:, 0], linear_points[:, 1], linear_points[:, 2], alpha=0.2, s=5)


# --- 3. Plot 2: Affine Combination (3D Plane) ---
ax2 = fig.add_subplot(1, 3, 2, projection='3d')
ax2.set_title("Affine Combination (Plane)")

# Create a 2D grid for two coefficients
b1, b2 = np.meshgrid(np.linspace(-1, 2, 10), np.linspace(-1, 2, 10))
# Calculate the third coefficient: b3 = 1 - b1 - b2
b3 = 1 - b1 - b2

# Calculate the (x, y, z) coordinates of the plane
# This is a vectorized way to apply the combinations
X = b1*v1[0] + b2*v2[0] + b3*v3[0]
Y = b1*v1[1] + b2*v2[1] + b3*v3[1]
Z = b1*v1[2] + b2*v2[2] + b3*v3[2]

ax2.plot_surface(X, Y, Z, alpha=0.5, cmap='viridis')


# --- 4. Plot 3: Convex Combination (3D Triangle) ---
ax3 = fig.add_subplot(1, 3, 3, projection='3d')
ax3.set_title("Convex Combination (Triangle)")

# The 3 points of the triangle are just the 3 vectors
verts = [v1, v2, v3]
# Create the 3D polygon
tri = Poly3DCollection([verts])
tri.set_facecolor('cyan')
tri.set_edgecolor('k')
tri.set_alpha(0.7)
ax3.add_collection3d(tri)

# --- 5. Plot vectors and set labels for all subplots ---
for ax in [ax1, ax2, ax3]:
    # Plot the original vectors
    ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='r', label='v1', lw=2)
    ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='g', label='v2', lw=2)
    ax.quiver(0, 0, 0, v3[0], v3[1], v3[2], color='b', label='v3', lw=2)
    
    # Plot the tips of the vectors
    ax.scatter(V[0, :], V[1, :], V[2, :], color='k', s=50, label='Vector Tips')

    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Set axis limits
    ax.set_xlim([-4, 4])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 4])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()