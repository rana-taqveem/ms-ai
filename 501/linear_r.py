import numpy as np

# Data
x1 = np.array([10, 12, 20, 22, 30, 35])  # visitors
x2 = np.array([2, 1, 3, 4, 3, 5])        # ad spend
y = np.array([25, 28, 45, 48, 70, 82])   # revenue

print("="*60)
print("LINEAR REGRESSION: y = β0 + β1*x1 + β2*x2")
print("="*60)

# Step 1: Construct the design matrix A
# Column 1: ones (for intercept β0)
# Column 2: x1 (for β1)
# Column 3: x2 (for β2)
ones = np.ones(len(x1))
A = np.column_stack([ones, x1, x2])

print("\n1. DESIGN MATRIX A")
print(f"   Shape: {A.shape} (6 observations × 3 parameters [β0, β1, β2])")
print(f"\n   Structure: [1's column | x1 column | x2 column]")
print(f"              [for β0     | for β1    | for β2   ]")
print("\n   Matrix A:")
print("   obs | β0(1) | x1 | x2")
print("   " + "-"*25)
for i in range(len(A)):
    print(f"    {i+1}  |  {A[i,0]:.0f}   | {A[i,1]:2.0f} | {A[i,2]:.0f}")

print("\n   Full matrix A:")
print(A)

# Step 2: Response vector y
print(f"\n2. RESPONSE VECTOR y")
print(f"   Shape: {y.shape}")
print(f"   y = {y}")

# Step 3: Compute A^T (transpose of A)
A_T = A.T
print(f"\n3. TRANSPOSE A^T")
print(f"   Shape: {A_T.shape} (3 parameters × 6 observations)")
print(A_T)

# Step 4: Compute A^T A
A_T_A = A_T @ A
print(f"\n4. MATRIX A^T A (Normal Equations Matrix)")
print(f"   Shape: {A_T_A.shape}")
print(f"   This is a symmetric 3×3 matrix:")
print(A_T_A)

# Step 5: Compute determinant of A^T A
det_A_T_A = np.linalg.det(A_T_A)
print(f"\n5. DETERMINANT of A^T A")
print(f"   det(A^T A) = {det_A_T_A:.4f}")
if abs(det_A_T_A) > 1e-10:
    print("   ✓ Matrix is invertible (det ≠ 0)")
else:
    print("   ✗ Matrix is singular (det ≈ 0)")

# Step 6: Compute (A^T A)^(-1)
A_T_A_inv = np.linalg.inv(A_T_A)
print(f"\n6. INVERSE (A^T A)^(-1)")
print(f"   Shape: {A_T_A_inv.shape}")
print(A_T_A_inv)

# Verify the inverse
identity_check = A_T_A @ A_T_A_inv
print(f"\n   Verification: (A^T A) × (A^T A)^(-1) should equal I:")
print(f"   (showing should be close to identity matrix)")
print(identity_check)

# Step 7: Compute A^T y
A_T_y = A_T @ y
print(f"\n7. VECTOR A^T y")
print(f"   Shape: {A_T_y.shape}")
print(f"   A^T y = {A_T_y}")

# Step 8: Compute β_OLS = (A^T A)^(-1) A^T y
beta_OLS = A_T_A_inv @ A_T_y
print(f"\n8. OLS ESTIMATES β_OLS = (A^T A)^(-1) A^T y")
print(f"   Shape: {beta_OLS.shape}")
print(f"\n   β = [{beta_OLS[0]:.6f}, {beta_OLS[1]:.6f}, {beta_OLS[2]:.6f}]^T")
print(f"\n   β0 (intercept) = {beta_OLS[0]:.6f}")
print(f"   β1 (visitors)  = {beta_OLS[1]:.6f}")
print(f"   β2 (ad spend)  = {beta_OLS[2]:.6f}")

print("\n" + "="*60)
print("REGRESSION EQUATION:")
print(f"y = {beta_OLS[0]:.4f} + {beta_OLS[1]:.4f}*x1 + {beta_OLS[2]:.4f}*x2")
print("="*60)

# Step 9: Model diagnostics
y_pred = A @ beta_OLS
residuals = y - y_pred
SSE = np.sum(residuals**2)
SST = np.sum((y - np.mean(y))**2)
R_squared = 1 - (SSE / SST)

print(f"\n9. MODEL FIT AND DIAGNOSTICS")
print(f"\n   Observed vs Predicted:")
print(f"   obs | y_actual | y_predicted | residual")
print("   " + "-"*45)
for i in range(len(y)):
    print(f"    {i+1}  |   {y[i]:5.1f}   |    {y_pred[i]:6.2f}    |  {residuals[i]:6.2f}")

print(f"\n   SSE (Sum of Squared Errors): {SSE:.4f}")
print(f"   SST (Total Sum of Squares):  {SST:.4f}")
print(f"   R² (Coefficient of Determination): {R_squared:.6f}")
print(f"   → The model explains {R_squared*100:.2f}% of the variance in revenue")

print("\n" + "="*60)
print("INTERPRETATION:")
print(f"• For each additional visitor, revenue increases by ${beta_OLS[1]:.4f}")
print(f"• For each additional $ in ad spend, revenue increases by ${beta_OLS[2]:.4f}")
print(f"• Base revenue (with 0 visitors and $0 ad spend) is ${beta_OLS[0]:.4f}")
print("="*60)