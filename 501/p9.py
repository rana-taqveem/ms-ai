import numpy as np
import matplotlib.pyplot as plt

# Data
patients = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
p_hat = np.array([0.95, 0.89, 0.76, 0.65, 0.55, 0.45, 0.35, 0.25, 0.15, 0.05])
y_true = np.array([1, 1, 1, 0, 1, 0, 0, 1, 0, 0])

print("="*80)
print("LOGISTIC REGRESSION CLASSIFICATION ANALYSIS")
print("="*80)

print("\nDATA:")
print(f"{'Patient':<10} {'p̂ (prob)':<15} {'y (true)':<10}")
print("-"*40)
for i in range(len(patients)):
    print(f"{patients[i]:<10} {p_hat[i]:<15.2f} {y_true[i]:<10}")

print(f"\nTrue Positives in dataset: {np.sum(y_true == 1)}")
print(f"True Negatives in dataset: {np.sum(y_true == 0)}")

# ============================================================================
# PART (a): THRESHOLD 0.5 - METRICS
# ============================================================================
print("\n" + "="*80)
print("PART (a): THRESHOLD t = 0.5 - CONFUSION MATRIX AND METRICS")
print("="*80)

threshold_a = 0.5
y_pred_a = (p_hat >= threshold_a).astype(int)

print(f"\nThreshold: t = {threshold_a}")
print(f"\nPredictions (p̂ ≥ {threshold_a} → ŷ = 1):")
print(f"{'Patient':<10} {'p̂':<15} {'ŷ (pred)':<15} {'y (true)':<15} {'Result':<20}")
print("-"*80)
for i in range(len(patients)):
    result = ""
    if y_pred_a[i] == 1 and y_true[i] == 1:
        result = "True Positive (TP)"
    elif y_pred_a[i] == 1 and y_true[i] == 0:
        result = "False Positive (FP)"
    elif y_pred_a[i] == 0 and y_true[i] == 1:
        result = "False Negative (FN)"
    else:
        result = "True Negative (TN)"
    print(f"{patients[i]:<10} {p_hat[i]:<15.2f} {y_pred_a[i]:<15} {y_true[i]:<15} {result:<20}")

# Confusion Matrix
TP = np.sum((y_pred_a == 1) & (y_true == 1))
FP = np.sum((y_pred_a == 1) & (y_true == 0))
FN = np.sum((y_pred_a == 0) & (y_true == 1))
TN = np.sum((y_pred_a == 0) & (y_true == 0))

print(f"\nCONFUSION MATRIX:")
print(f"\n                    Predicted")
print(f"                 Positive  Negative")
print(f"Actual Positive     {TP:2d}        {FN:2d}      (Total: {TP+FN})")
print(f"Actual Negative     {FP:2d}        {TN:2d}      (Total: {FP+TN})")
print(f"                 -----     -----")
print(f"Total              {TP+FP:2d}        {FN+TN:2d}      (Total: {TP+FP+FN+TN})")

print(f"\nConfusion Matrix Components:")
print(f"  TP (True Positives)  = {TP}")
print(f"  FP (False Positives) = {FP}")
print(f"  FN (False Negatives) = {FN}")
print(f"  TN (True Negatives)  = {TN}")

# Metrics
accuracy = (TP + TN) / (TP + FP + FN + TN)
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0  # Sensitivity
specificity = TN / (TN + FP) if (TN + FP) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print(f"\nMETRICS:")
print(f"  Accuracy    = (TP + TN) / Total = ({TP} + {TN}) / {TP+FP+FN+TN} = {accuracy:.4f}")
print(f"  Precision   = TP / (TP + FP) = {TP} / ({TP} + {FP}) = {precision:.4f}")
print(f"  Recall      = TP / (TP + FN) = {TP} / ({TP} + {FN}) = {recall:.4f}")
print(f"  Specificity = TN / (TN + FP) = {TN} / ({TN} + {FP}) = {specificity:.4f}")
print(f"  F1 Score    = 2 × (Precision × Recall) / (Precision + Recall)")
print(f"              = 2 × ({precision:.4f} × {recall:.4f}) / ({precision:.4f} + {recall:.4f})")
print(f"              = {f1_score:.4f}")

print(f"\nINTERPRETATION:")
print(f"  • Accuracy ({accuracy:.1%}): Overall correctness")
print(f"  • Precision ({precision:.1%}): Of predicted positives, {precision:.1%} are truly positive")
print(f"  • Recall/Sensitivity ({recall:.1%}): Of actual positives, {recall:.1%} are detected")
print(f"  • Specificity ({specificity:.1%}): Of actual negatives, {specificity:.1%} are correctly identified")
print(f"  • F1 Score ({f1_score:.4f}): Harmonic mean of precision and recall")

# ============================================================================
# PART (b): COST-SENSITIVE DECISION
# ============================================================================
print("\n" + "="*80)
print("PART (b): COST-SENSITIVE DECISION")
print("="*80)

CFN = 10  # Cost of False Negative
CFP = 1   # Cost of False Positive

print(f"\nCOST STRUCTURE:")
print(f"  C_FN (False Negative cost) = {CFN}")
print(f"  C_FP (False Positive cost) = {CFP}")
print(f"  Correct predictions cost = 0")

print(f"\n(i) OPTIMAL THRESHOLD DERIVATION:")
print("-"*80)
print(f"\nFor a patient with predicted probability p̂:")
print(f"\nExpected cost of predicting POSITIVE:")
print(f"  E[Cost | predict positive] = P(y=0) × C_FP + P(y=1) × 0")
print(f"                              = (1 - p̂) × C_FP")
print(f"                              = (1 - p̂) × {CFP}")
print(f"\nExpected cost of predicting NEGATIVE:")
print(f"  E[Cost | predict negative] = P(y=1) × C_FN + P(y=0) × 0")
print(f"                              = p̂ × C_FN")
print(f"                              = p̂ × {CFN}")
print(f"\nPredict POSITIVE when:")
print(f"  E[Cost | predict positive] < E[Cost | predict negative]")
print(f"  (1 - p̂) × C_FP < p̂ × C_FN")
print(f"  C_FP - p̂ × C_FP < p̂ × C_FN")
print(f"  C_FP < p̂ × (C_FN + C_FP)")
print(f"  p̂ > C_FP / (C_FN + C_FP)")

threshold_b = CFP / (CFN + CFP)
print(f"\nOPTIMAL THRESHOLD:")
print(f"  t* = C_FP / (C_FN + C_FP)")
print(f"     = {CFP} / ({CFN} + {CFP})")
print(f"     = {CFP} / {CFN + CFP}")
print(f"     = {threshold_b:.4f}")
print(f"\nDecision Rule: Predict POSITIVE if p̂ ≥ {threshold_b:.4f}")

print(f"\n(ii) CLASSIFICATION WITH OPTIMAL THRESHOLD:")
print("-"*80)

y_pred_b = (p_hat >= threshold_b).astype(int)

print(f"\nPredictions (p̂ ≥ {threshold_b:.4f} → ŷ = 1):")
print(f"{'Patient':<10} {'p̂':<15} {'ŷ (pred)':<15} {'y (true)':<15} {'Result':<20} {'Cost':<10}")
print("-"*90)
total_cost = 0
for i in range(len(patients)):
    result = ""
    cost = 0
    if y_pred_b[i] == 1 and y_true[i] == 1:
        result = "True Positive (TP)"
        cost = 0
    elif y_pred_b[i] == 1 and y_true[i] == 0:
        result = "False Positive (FP)"
        cost = CFP
    elif y_pred_b[i] == 0 and y_true[i] == 1:
        result = "False Negative (FN)"
        cost = CFN
    else:
        result = "True Negative (TN)"
        cost = 0
    total_cost += cost
    print(f"{patients[i]:<10} {p_hat[i]:<15.2f} {y_pred_b[i]:<15} {y_true[i]:<15} {result:<20} {cost:<10}")

# Confusion Matrix for optimal threshold
TP_b = np.sum((y_pred_b == 1) & (y_true == 1))
FP_b = np.sum((y_pred_b == 1) & (y_true == 0))
FN_b = np.sum((y_pred_b == 0) & (y_true == 1))
TN_b = np.sum((y_pred_b == 0) & (y_true == 0))

print(f"\nCONFUSION MATRIX (threshold = {threshold_b:.4f}):")
print(f"\n                    Predicted")
print(f"                 Positive  Negative")
print(f"Actual Positive     {TP_b:2d}        {FN_b:2d}")
print(f"Actual Negative     {FP_b:2d}        {TN_b:2d}")

print(f"\nConfusion Matrix Components:")
print(f"  TP (True Positives)  = {TP_b}")
print(f"  FP (False Positives) = {FP_b}")
print(f"  FN (False Negatives) = {FN_b}")
print(f"  TN (True Negatives)  = {TN_b}")

print(f"\nTOTAL EXPECTED COST:")
print(f"  Total Cost = (FN × C_FN) + (FP × C_FP)")
print(f"             = ({FN_b} × {CFN}) + ({FP_b} × {CFP})")
print(f"             = {FN_b * CFN} + {FP_b * CFP}")
print(f"             = {total_cost}")

print(f"\nCOMPARISON WITH t=0.5:")
cost_t05 = (FN * CFN) + (FP * CFP)
print(f"  Cost with t=0.5:     {cost_t05}")
print(f"  Cost with t*={threshold_b:.4f}: {total_cost}")
print(f"  Cost reduction:      {cost_t05 - total_cost} ({(cost_t05-total_cost)/cost_t05*100:.1f}%)")

# ============================================================================
# PART (c): ROC & AUC
# ============================================================================
print("\n" + "="*80)
print("PART (c): ROC CURVE AND AUC")
print("="*80)

print("\nROC CURVE CONSTRUCTION:")
print("Sweeping through thresholds based on predicted probabilities")

# Get unique thresholds - include boundaries
unique_probs = np.sort(np.unique(p_hat))[::-1]  # Descending order
thresholds = []
thresholds.append(1.1)  # Start above highest probability
for prob in unique_probs:
    thresholds.append(prob + 0.001)  # Just above
    thresholds.append(prob - 0.001)  # Just below
thresholds.append(-0.1)  # End below lowest probability

# Calculate TPR and FPR for each threshold
roc_data = []
for t in thresholds:
    y_pred_t = (p_hat >= t).astype(int)
    
    TP_t = np.sum((y_pred_t == 1) & (y_true == 1))
    FP_t = np.sum((y_pred_t == 1) & (y_true == 0))
    FN_t = np.sum((y_pred_t == 0) & (y_true == 1))
    TN_t = np.sum((y_pred_t == 0) & (y_true == 0))
    
    # Total actual positives and negatives
    P = TP_t + FN_t  # Total actual positives
    N = FP_t + TN_t  # Total actual negatives
    
    TPR = TP_t / P if P > 0 else 0  # True Positive Rate (Sensitivity/Recall)
    FPR = FP_t / N if N > 0 else 0  # False Positive Rate
    
    roc_data.append((t, FPR, TPR, TP_t, FP_t, FN_t, TN_t))

# Remove duplicates and sort by FPR
roc_unique = {}
for t, fpr, tpr, tp, fp, fn, tn in roc_data:
    key = (round(fpr, 6), round(tpr, 6))
    if key not in roc_unique:
        roc_unique[key] = (t, fpr, tpr, tp, fp, fn, tn)

roc_sorted = sorted(roc_unique.values(), key=lambda x: (x[1], x[2]))

print(f"\n{'Threshold':<12} {'FPR':<12} {'TPR':<12} {'TP':<6} {'FP':<6} {'FN':<6} {'TN':<6}")
print("-"*80)
for t, fpr, tpr, tp, fp, fn, tn in roc_sorted:
    print(f"{t:<12.4f} {fpr:<12.4f} {tpr:<12.4f} {tp:<6} {fp:<6} {fn:<6} {tn:<6}")

# Extract FPR and TPR for AUC calculation
fpr_values = np.array([x[1] for x in roc_sorted])
tpr_values = np.array([x[2] for x in roc_sorted])

# Calculate AUC using trapezoidal rule
auc = 0.0
print(f"\nAUC CALCULATION (Trapezoidal Rule):")
print(f"{'i':<6} {'FPR[i]':<12} {'TPR[i]':<12} {'ΔFPR':<12} {'Avg TPR':<12} {'Area':<12}")
print("-"*80)
for i in range(len(fpr_values) - 1):
    delta_fpr = fpr_values[i+1] - fpr_values[i]
    avg_tpr = (tpr_values[i] + tpr_values[i+1]) / 2
    area_i = delta_fpr * avg_tpr
    auc += area_i
    print(f"{i:<6} {fpr_values[i]:<12.4f} {tpr_values[i]:<12.4f} {delta_fpr:<12.4f} {avg_tpr:<12.4f} {area_i:<12.6f}")

print(f"\nAREA UNDER THE CURVE (AUC):")
print(f"  AUC = {auc:.6f}")
print(f"  AUC = {auc:.4f} (rounded)")

# Plot ROC Curve
plt.figure(figsize=(8, 8))
plt.plot(fpr_values, tpr_values, 'b-o', linewidth=2, markersize=6, label=f'ROC Curve (AUC = {auc:.4f})')
plt.plot([0, 1], [0, 1], 'r--', linewidth=1, label='Random Classifier (AUC = 0.5)')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.xlabel('False Positive Rate (FPR)', fontsize=12)
plt.ylabel('True Positive Rate (TPR)', fontsize=12)
plt.title('ROC Curve - Hospital Logistic Regression Model', fontsize=14, fontweight='bold')
plt.legend(loc='lower right', fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('roc_curve.png', dpi=150, bbox_inches='tight')
print(f"\nROC curve saved as 'roc_curve.png'")

print(f"\nINTERPRETATION OF AUC = {auc:.4f}:")
if auc >= 0.9:
    quality = "Excellent"
elif auc >= 0.8:
    quality = "Good"
elif auc >= 0.7:
    quality = "Fair"
elif auc >= 0.6:
    quality = "Poor"
else:
    quality = "Very Poor"
print(f"  • Model quality: {quality}")
print(f"  • AUC represents the probability that the model ranks a random")
print(f"    positive instance higher than a random negative instance")
print(f"  • AUC = 1.0 is perfect ranking, AUC = 0.5 is random guessing")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("SUMMARY AND KEY INSIGHTS")
print("="*80)

print(f"\n1. THRESHOLD COMPARISON:")
print(f"   {'Threshold':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<12} {'Cost':<10}")
print("   " + "-"*80)

# Metrics for t=0.5
acc_05 = (TP + TN) / (TP + FP + FN + TN)
prec_05 = TP / (TP + FP) if (TP + FP) > 0 else 0
rec_05 = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_05 = 2 * (prec_05 * rec_05) / (prec_05 + rec_05) if (prec_05 + rec_05) > 0 else 0
cost_05 = (FN * CFN) + (FP * CFP)

# Metrics for optimal threshold
acc_opt = (TP_b + TN_b) / (TP_b + FP_b + FN_b + TN_b)
prec_opt = TP_b / (TP_b + FP_b) if (TP_b + FP_b) > 0 else 0
rec_opt = TP_b / (TP_b + FN_b) if (TP_b + FN_b) > 0 else 0
f1_opt = 2 * (prec_opt * rec_opt) / (prec_opt + rec_opt) if (prec_opt + rec_opt) > 0 else 0
cost_opt = (FN_b * CFN) + (FP_b * CFP)

print(f"   {'t = 0.5':<20} {acc_05:<12.4f} {prec_05:<12.4f} {rec_05:<12.4f} {f1_05:<12.4f} {cost_05:<10}")
print(f"   {'t = ' + str(round(threshold_b, 4)):<20} {acc_opt:<12.4f} {prec_opt:<12.4f} {rec_opt:<12.4f} {f1_opt:<12.4f} {cost_opt:<10}")

print(f"\n2. KEY FINDINGS:")
print(f"   • Standard threshold (0.5) may not be optimal for clinical settings")
print(f"   • Cost-sensitive threshold ({threshold_b:.4f}) reduces total cost by {cost_05 - cost_opt}")
print(f"   • Lower threshold increases recall (fewer missed cases) at cost of more false alarms")
print(f"   • AUC = {auc:.4f} indicates {quality.lower()} discriminative ability")

print(f"\n3. CLINICAL IMPLICATIONS:")
print(f"   • Missing a serious condition (FN) costs {CFN}× more than a false alarm (FP)")
print(f"   • Optimal threshold {threshold_b:.4f} < 0.5 means: be more aggressive in flagging patients")
print(f"   • This increases sensitivity (recall) from {rec_05:.1%} to {rec_opt:.1%}")
print(f"   • Trade-off: More false positives ({FP} → {FP_b}) but fewer false negatives ({FN} → {FN_b})")
print(f"   • Net effect: Lower total expected cost in clinical practice")

print("\n" + "="*80)