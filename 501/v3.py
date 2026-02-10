import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- 1. Setup ---
N = 500000  # Number of points

# Create 3 linearly independent basis vectors
# We can use randn() here; the vectors can be anything.
v1 = np.random.randn(3)
v2 = np.random.randn(3)
v3 = np.random.randn(3)

# Stack them into a (3, 3) matrix where each ROW is a vector
V = np.array([v1, v2, v3])

# Create the figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.set_title("Linear Combination (Parallelepiped)", fontsize=16)


# --- 2. Generate Coefficients ---
#
# THIS IS THE KEY CHANGE:
# We use np.random.uniform() to create an evenly distributed
# "cube" of coefficients between -1 and 1.
#
coefficients = np.random.uniform(-1, 1, (N, 3))


# --- 3. Calculate Linear Combinations ---
# (N, 3) @ (3, 3) --> (N, 3) matrix of points
linear_combination = coefficients @ V
print(f"Linear combinations shape: {linear_combination.shape}")


# --- 4. Plot the Subspace (Parallelepiped) ---
ax.scatter(linear_combination[:, 0], 
            linear_combination[:, 1], 
            linear_combination[:, 2], 
            label='Span (Uniform Coeffs)', 
            alpha=0.08,  # Use low alpha for many points
            s=3)        # Use small points


# --- 5. Plot the Basis Vectors ---
ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='r', label='v1', lw=3, length=2)
ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='g', label='v2', lw=3, length=2)
ax.quiver(0, 0, 0, v3[0], v3[1], v3[2], color='b', label='v3', lw=3, length=2)


# --- 6. Final Plotting ---
lim = np.max(np.abs(linear_combination)) * 1.1
ax.set_xlim([-lim, lim])
ax.set_ylim([-lim, lim])
ax.set_zlim([-lim, lim])
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.legend()
ax.grid(True)

plt.show()