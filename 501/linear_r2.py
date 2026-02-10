import numpy as np

# Data
x1 = np.array([10, 12, 20, 22, 30, 35])  # visitors
x2 = np.array([2, 1, 3, 4, 3, 5])        # ad spend
y = np.array([25, 28, 45, 48, 70, 82])   # revenue

print("="*80)
print("OLS AND RIDGE REGRESSION: TRAINING ON FULL DATA, EVALUATING ON TRAIN/TEST SPLIT")
print("="*80)

# ============================================================================
# PART 1: COMPUTE β_OLS USING FULL DATA (ALL 6 OBSERVATIONS)
# ============================================================================
print("\n" + "="*80)
print("PART 1: OLS ESTIMATION USING FULL DATA (6 observations)")
print("="*80)

# Construct design matrix A using all data
ones = np.ones(len(x1))
A_full = np.column_stack([ones, x1, x2])

print("\n1. DESIGN MATRIX A (Full Data)")
print(f"   Shape: {A_full.shape} (6 observations × 3 parameters)")
print(f"\n   {'Obs':<6} {'β0(1)':<10} {'x1':<10} {'x2':<10}")
print("   " + "-"*40)
for i in range(len(A_full)):
    print(f"   {i+1:<6} {A_full[i,0]:<10.0f} {A_full[i,1]:<10.0f} {A_full[i,2]:<10.0f}")
print("\n   Full matrix:")
print(A_full)

# Compute A^T
A_T = A_full.T
print(f"\n2. TRANSPOSE A^T")
print(f"   Shape: {A_T.shape}")
print(A_T)

# Compute A^T A
A_T_A = A_T @ A_full
print(f"\n3. MATRIX A^T A")
print(f"   Shape: {A_T_A.shape}")
print(A_T_A)

# Compute determinant
det_A_T_A = np.linalg.det(A_T_A)
print(f"\n4. DETERMINANT of A^T A")
print(f"   det(A^T A) = {det_A_T_A:.6f}")
if abs(det_A_T_A) > 1e-10:
    print("   ✓ Matrix is invertible")
else:
    print("   ✗ Matrix is singular")

# Compute inverse
A_T_A_inv = np.linalg.inv(A_T_A)
print(f"\n5. INVERSE (A^T A)^(-1)")
print(f"   Shape: {A_T_A_inv.shape}")
print(A_T_A_inv)

# Compute A^T y
A_T_y = A_T @ y
print(f"\n6. VECTOR A^T y")
print(f"   Shape: {A_T_y.shape}")
print(A_T_y)

# Compute β_OLS
beta_OLS = A_T_A_inv @ A_T_y
print(f"\n7. β_OLS = (A^T A)^(-1) A^T y")
print(f"   Shape: {beta_OLS.shape}")
print(f"\n   β0 (intercept) = {beta_OLS[0]:.6f}")
print(f"   β1 (visitors)  = {beta_OLS[1]:.6f}")
print(f"   β2 (ad spend)  = {beta_OLS[2]:.6f}")
print(f"\n   OLS Equation: y = {beta_OLS[0]:.4f} + {beta_OLS[1]:.4f}*x1 + {beta_OLS[2]:.4f}*x2")

# ============================================================================
# PART 2: COMPUTE β_RIDGE USING FULL DATA WITH λ=10
# ============================================================================
lambda_val = 10

print("\n" + "="*80)
print(f"PART 2: RIDGE ESTIMATION USING FULL DATA (λ = {lambda_val})")
print("="*80)

# Identity matrix
I_3 = np.eye(3)
print(f"\n1. Identity Matrix I_3")
print(f"   Shape: {I_3.shape}")
print(I_3)

# λI
lambda_I = lambda_val * I_3
print(f"\n2. λI (λ = {lambda_val})")
print(f"   Shape: {lambda_I.shape}")
print(lambda_I)

# A^T A + λI
A_T_A_plus_lambdaI = A_T_A + lambda_I
print(f"\n3. A^T A + λI")
print(f"   Shape: {A_T_A_plus_lambdaI.shape}")
print(A_T_A_plus_lambdaI)

# Determinant
det_ridge = np.linalg.det(A_T_A_plus_lambdaI)
print(f"\n4. Determinant of (A^T A + λI): {det_ridge:.6f}")

# Inverse
A_T_A_plus_lambdaI_inv = np.linalg.inv(A_T_A_plus_lambdaI)
print(f"\n5. (A^T A + λI)^(-1)")
print(f"   Shape: {A_T_A_plus_lambdaI_inv.shape}")
print(A_T_A_plus_lambdaI_inv)

# β_ridge
beta_ridge = A_T_A_plus_lambdaI_inv @ A_T_y
print(f"\n6. β_ridge = (A^T A + λI)^(-1) A^T y")
print(f"   Shape: {beta_ridge.shape}")
print(f"\n   β0 (intercept) = {beta_ridge[0]:.6f}")
print(f"   β1 (visitors)  = {beta_ridge[1]:.6f}")
print(f"   β2 (ad spend)  = {beta_ridge[2]:.6f}")
print(f"\n   Ridge Equation: y = {beta_ridge[0]:.4f} + {beta_ridge[1]:.4f}*x1 + {beta_ridge[2]:.4f}*x2")

# ============================================================================
# COEFFICIENT COMPARISON
# ============================================================================
print("\n" + "="*80)
print("COEFFICIENT COMPARISON: OLS vs RIDGE")
print("="*80)
print(f"\n{'Parameter':<15} {'β_OLS':<20} {'β_Ridge (λ=10)':<20} {'Shrinkage':<15}")
print("-"*80)
for i, param in enumerate(['β0 (intercept)', 'β1 (visitors)', 'β2 (ad spend)']):
    shrinkage = beta_OLS[i] - beta_ridge[i]
    print(f"{param:<15} {beta_OLS[i]:<20.6f} {beta_ridge[i]:<20.6f} {shrinkage:<15.6f}")

# ============================================================================
# PART 3: TRAIN/TEST SPLIT AND MSE CALCULATION
# ============================================================================
print("\n" + "="*80)
print("PART 3: TRAIN/TEST SPLIT AND MSE EVALUATION")
print("="*80)

# Split indices
train_idx = [0, 1, 2, 3]  # Observations 1-4
test_idx = [4, 5]         # Observations 5-6

# Training data
x1_train = x1[train_idx]
x2_train = x2[train_idx]
y_train = y[train_idx]
A_train = A_full[train_idx, :]

# Test data
x1_test = x1[test_idx]
x2_test = x2[test_idx]
y_test = y[test_idx]
A_test = A_full[test_idx, :]

print("\nDATA SPLIT:")
print("\nTRAINING DATA (Observations 1-4):")
print(f"{'Obs':<6} {'x1':<10} {'x2':<10} {'y':<10}")
print("-"*40)
for i, idx in enumerate(train_idx):
    print(f"{idx+1:<6} {x1[idx]:<10.0f} {x2[idx]:<10.0f} {y[idx]:<10.0f}")

print("\nTEST DATA (Observations 5-6):")
print(f"{'Obs':<6} {'x1':<10} {'x2':<10} {'y':<10}")
print("-"*40)
for i, idx in enumerate(test_idx):
    print(f"{idx+1:<6} {x1[idx]:<10.0f} {x2[idx]:<10.0f} {y[idx]:<10.0f}")

# ============================================================================
# PREDICTIONS AND MSE - TRAINING SET
# ============================================================================
print("\n" + "="*80)
print("TRAINING SET PREDICTIONS AND ERRORS")
print("="*80)

y_train_pred_OLS = A_train @ beta_OLS
y_train_pred_ridge = A_train @ beta_ridge
errors_train_OLS = y_train - y_train_pred_OLS
errors_train_ridge = y_train - y_train_pred_ridge

print(f"\n{'Obs':<6} {'y_actual':<12} {'ŷ_OLS':<12} {'ŷ_Ridge':<12} {'e_OLS':<12} {'e_Ridge':<12}")
print("-"*80)
for i in range(len(y_train)):
    print(f"{train_idx[i]+1:<6} {y_train[i]:<12.2f} {y_train_pred_OLS[i]:<12.4f} "
          f"{y_train_pred_ridge[i]:<12.4f} {errors_train_OLS[i]:<12.4f} {errors_train_ridge[i]:<12.4f}")

# Training MSE
mse_train_OLS = np.mean(errors_train_OLS**2)
mse_train_ridge = np.mean(errors_train_ridge**2)

print(f"\nTRAINING MSE:")
print(f"  MSE_OLS   = {mse_train_OLS:.6f}")
print(f"  MSE_Ridge = {mse_train_ridge:.6f}")
print(f"  Difference = {abs(mse_train_OLS - mse_train_ridge):.6f}")

# ============================================================================
# PREDICTIONS AND MSE - TEST SET
# ============================================================================
print("\n" + "="*80)
print("TEST SET PREDICTIONS AND ERRORS")
print("="*80)

y_test_pred_OLS = A_test @ beta_OLS
y_test_pred_ridge = A_test @ beta_ridge
errors_test_OLS = y_test - y_test_pred_OLS
errors_test_ridge = y_test - y_test_pred_ridge

print(f"\n{'Obs':<6} {'y_actual':<12} {'ŷ_OLS':<12} {'ŷ_Ridge':<12} {'e_OLS':<12} {'e_Ridge':<12}")
print("-"*80)
for i in range(len(y_test)):
    print(f"{test_idx[i]+1:<6} {y_test[i]:<12.2f} {y_test_pred_OLS[i]:<12.4f} "
          f"{y_test_pred_ridge[i]:<12.4f} {errors_test_OLS[i]:<12.4f} {errors_test_ridge[i]:<12.4f}")

# Test MSE
mse_test_OLS = np.mean(errors_test_OLS**2)
mse_test_ridge = np.mean(errors_test_ridge**2)

print(f"\nTEST MSE:")
print(f"  MSE_OLS   = {mse_test_OLS:.6f}")
print(f"  MSE_Ridge = {mse_test_ridge:.6f}")
print(f"  Difference = {abs(mse_test_OLS - mse_test_ridge):.6f}")

# ============================================================================
# MSE COMPARISON SUMMARY
# ============================================================================
print("\n" + "="*80)
print("MSE COMPARISON SUMMARY TABLE")
print("="*80)
print(f"\n{'Dataset':<20} {'MSE_OLS':<20} {'MSE_Ridge':<20} {'Winner':<20}")
print("-"*80)
print(f"{'Training (obs 1-4)':<20} {mse_train_OLS:<20.6f} {mse_train_ridge:<20.6f} "
      f"{'OLS' if mse_train_OLS < mse_train_ridge else 'Ridge':<20}")
print(f"{'Test (obs 5-6)':<20} {mse_test_OLS:<20.6f} {mse_test_ridge:<20.6f} "
      f"{'OLS' if mse_test_OLS < mse_test_ridge else 'Ridge':<20}")

# ============================================================================
# ANALYSIS: BIAS-VARIANCE TRADEOFF AND COLLINEARITY
# ============================================================================
print("\n" + "="*80)
print("ANALYSIS: BIAS-VARIANCE TRADEOFF AND COLLINEARITY EFFECTS")
print("="*80)

# Check correlation between predictors
correlation_x1_x2 = np.corrcoef(x1, x2)[0, 1]
print(f"\n1. COLLINEARITY ANALYSIS:")
print(f"   Correlation between x1 and x2: {correlation_x1_x2:.6f}")
if abs(correlation_x1_x2) > 0.7:
    print(f"   → HIGH collinearity detected (|r| > 0.7)")
elif abs(correlation_x1_x2) > 0.5:
    print(f"   → MODERATE collinearity detected (|r| > 0.5)")
else:
    print(f"   → LOW collinearity (|r| < 0.5)")

# Condition number
eigenvalues = np.linalg.eigvals(A_T_A)
condition_number = np.sqrt(np.max(eigenvalues) / np.min(eigenvalues))
print(f"\n   Condition number of A^T A: {condition_number:.4f}")
if condition_number > 30:
    print(f"   → HIGH condition number (> 30): Multicollinearity present")
elif condition_number > 10:
    print(f"   → MODERATE condition number (> 10): Some multicollinearity")
else:
    print(f"   → LOW condition number (< 10): No significant multicollinearity")

# Variance Inflation Factor (VIF) approximation
print(f"\n2. COEFFICIENT STABILITY:")
print(f"   Ridge shrinkage factors:")
for i, param in enumerate(['β0', 'β1', 'β2']):
    if beta_OLS[i] != 0:
        shrinkage_pct = (1 - beta_ridge[i]/beta_OLS[i]) * 100
        print(f"   {param}: {shrinkage_pct:.2f}% shrinkage")

# Determine winner and explain
winner = "Ridge" if mse_test_ridge < mse_test_OLS else "OLS"
print(f"\n3. TEST MSE COMPARISON:")
print(f"   Winner: {winner}")
print(f"   Test MSE reduction: {abs(mse_test_OLS - mse_test_ridge):.6f}")
print(f"   Percentage difference: {abs(mse_test_OLS - mse_test_ridge)/max(mse_test_OLS, mse_test_ridge)*100:.2f}%")

print(f"\n4. EXPLANATION - WHY {winner.upper()} PERFORMS BETTER:")
print("-"*80)

if winner == "Ridge":
    print("""
   Ridge regression achieves lower test MSE due to:
   
   a) BIAS-VARIANCE TRADEOFF:
      • Ridge introduces a small amount of bias by shrinking coefficients
      • This bias reduces variance significantly, leading to better generalization
      • The penalty term (λ=10) prevents overfitting to training data
      • Trade-off favors Ridge when: Variance reduction > Bias increase
   
   b) COLLINEARITY EFFECTS:
      • When predictors are correlated, OLS coefficients become unstable
      • Small changes in data lead to large changes in coefficient estimates
      • Ridge stabilizes estimates by adding λI to A^T A, improving conditioning
      • Regularization reduces sensitivity to collinear predictors
   
   c) SMALL SAMPLE SIZE:
      • With only 4 training observations and 2 predictors + intercept
      • OLS has high variance due to limited data
      • Ridge's constraint on coefficient magnitude prevents extreme estimates
      • Regularization acts as implicit prior information
   
   d) GENERALIZATION:
      • OLS minimizes training error but may not generalize well
      • Ridge's penalty helps the model learn more stable patterns
      • Lower test MSE indicates Ridge generalizes better to unseen data
""")
else:
    print("""
   OLS achieves lower test MSE due to:
   
   a) BIAS-VARIANCE TRADEOFF:
      • In this case, the bias introduced by Ridge (λ=10) is too large
      • The variance reduction does not compensate for the bias
      • OLS remains unbiased, which helps when true relationship is strong
      • Trade-off favors OLS when: Bias increase > Variance reduction
   
   b) LOW COLLINEARITY:
      • If predictors are not highly correlated, OLS estimates are stable
      • Ridge's penalty unnecessarily shrinks coefficients
      • Without multicollinearity, OLS's unbiasedness is more valuable
      • The regularization hurts more than it helps
   
   c) STRONG SIGNAL:
      • If the true relationship is strong and well-captured by training data
      • OLS's unbiased estimates better reflect the true coefficients
      • Ridge's shrinkage moves estimates away from true values
      • λ=10 may be too large for this dataset
   
   d) GENERALIZATION:
      • Test observations may be well-represented by training patterns
      • OLS's full utilization of training data benefits prediction
      • Ridge's conservatism (shrinkage) may be overly cautious here
""")

print("\n5. KEY TAKEAWAYS:")
print("-"*80)
print(f"""
   • Training MSE: OLS = {mse_train_OLS:.4f}, Ridge = {mse_train_ridge:.4f}
     → OLS always fits training data better (or equal) due to no penalty
   
   • Test MSE: OLS = {mse_test_OLS:.4f}, Ridge = {mse_test_ridge:.4f}
     → {winner} generalizes better to unseen data
   
   • Coefficient shrinkage: Ridge reduces magnitude of all coefficients
     → Helps when overfitting is a concern
   
   • Optimal λ selection: λ=10 may not be optimal
     → Cross-validation would help find best regularization strength
   
   • Bias-Variance: The estimator with lower test MSE found better balance
     → {winner} achieves optimal bias-variance tradeoff for this problem
""")

print("="*80)