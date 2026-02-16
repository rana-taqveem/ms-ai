# Assignment Solutions Guide

## Assessment of Current Work & What Needs to Be Added

---

## Part A: Data Preprocessing and Exploratory Analysis

### 1. Dataset Structure Description
**Status: Code exists, written summary missing**

Your `df.info()` and `df.describe()` calls produce the right output. What's missing is a **markdown cell** explicitly summarizing:

> The training dataset contains **41,348 samples** with **6 input features** and **1 target variable** (`price_class`).
> - 2 categorical features: `neighbourhood_group` (str), `room_type` (str)
> - 4 numerical features: `minimum_nights` (float64), `amenity_score` (float64), `number_of_reviews` (float64), `availability_365` (float64)
> - 1 integer target: `price_class` (int64, values 0-3)
>
> All features except `price_class` contain missing values, ranging from ~1.4% (`availability_365`) to ~3.2% (`minimum_nights`).

---

### 2. Missing Values Strategy & Justification
**Status: Code exists (pipeline handles it), written justification missing**

Your pipeline uses:
- `SimpleImputer(strategy='most_frequent')` for categoricals
- `SimpleImputer(strategy='median')` for numericals

Add a markdown cell:

> **Missing Value Strategy:**
> - **Categorical features** (`neighbourhood_group`, `room_type`): Imputed with **mode** (most frequent value). Since these are nominal categories with no ordinal relationship, mode is the only meaningful central tendency measure. The `add_indicator=True` flag creates binary columns tracking which rows were imputed, preserving the missingness signal for the model.
> - **Numerical features**: Imputed with **median** rather than mean. This choice is justified by the high skewness observed in `minimum_nights` (skew=22.02) and `number_of_reviews` (skew=3.56). Median is robust to outliers and extreme values, whereas mean would be heavily distorted by the long right tails in these distributions.
> - Missing rates are relatively low (1.4%–3.2% per feature, ~12.4% of rows have at least one missing value), so imputation is preferred over dropping rows, which would lose ~5,000 samples.

---

### 3. Class Distribution Visualization
**Status: You have `value_counts()` output but need a proper bar chart and written commentary**

You call `plot_feature_distribution('price_class')` which uses `sns.displot` — this works but a dedicated bar chart is cleaner for a categorical target. Add:

```python
plt.figure(figsize=(8, 5))
df_eda['price_class'].value_counts().sort_index().plot(kind='bar', color=['#2ecc71', '#3498db', '#e74c3c', '#9b59b6'])
plt.title('Distribution of Target Variable (price_class)')
plt.xlabel('Price Class')
plt.ylabel('Count')
for i, v in enumerate(df_eda['price_class'].value_counts().sort_index()):
    plt.text(i, v + 200, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
```

Then add a markdown cell:

> **Class Distribution Analysis:**
> | Class | Count | Proportion |
> |-------|-------|------------|
> | 0 | 5,567 | 13.5% |
> | 1 | 23,287 | 56.3% |
> | 2 | 9,844 | 23.8% |
> | 3 | 2,650 | 6.4% |
>
> The dataset exhibits **significant class imbalance**. Class 1 dominates with 56.3% of samples, while class 3 represents only 6.4%. This ~9:1 ratio between the majority and minority classes means a naive classifier predicting class 1 for everything would achieve ~56% accuracy. The model may struggle to learn patterns for underrepresented classes (especially class 3). Potential mitigations include class-weighted loss functions or oversampling, though these are not required for this assignment.

---

### 4. Categorical Encoding Justification
**Status: Code exists (OneHotEncoding in pipeline), written justification missing**

Add a markdown cell:

> **Encoding Choice: One-Hot Encoding**
>
> One-hot encoding was chosen for both categorical features because:
> 1. Both `neighbourhood_group` (5 categories) and `room_type` (3 categories) are **nominal** — there is no inherent ordering between Manhattan/Brooklyn/Queens etc., nor between Entire home/Private room/Shared room.
> 2. Label encoding would impose a false ordinal relationship that could mislead the model.
> 3. The cardinality is low (5 + 3 = 8 one-hot columns), so dimensionality explosion is not a concern.
> 4. `handle_unknown='ignore'` ensures robustness if test data contains unseen categories.

---

### 5. Normalization Method & Justification
**Status: Code exists (log+StandardScaler and StandardScaler), written justification missing**

Your pipeline applies:
- `log1p` + `StandardScaler` to `minimum_nights` and `number_of_reviews`
- `StandardScaler` only to `amenity_score` and `availability_365`

Add a markdown cell:

> **Normalization Strategy:**
>
> Two different pipelines were used based on feature skewness:
>
> | Feature | Skewness | Treatment |
> |---------|----------|-----------|
> | `minimum_nights` | 22.02 (highly skewed) | log1p → StandardScaler |
> | `number_of_reviews` | 3.56 (moderately skewed) | log1p → StandardScaler |
> | `amenity_score` | 0.08 (approximately symmetric) | StandardScaler only |
> | `availability_365` | 0.74 (mildly skewed) | StandardScaler only |
>
> **Why StandardScaler (z-score normalization)?** Neural networks with sigmoid/softmax activations are sensitive to input scale. StandardScaler centers features to mean=0, std=1, which helps gradient descent converge faster and prevents features with larger ranges from dominating.
>
> **Why log transform for skewed features?** `minimum_nights` has extreme skewness (22.02) with values ranging from 1 to 1000. Without log transformation, the StandardScaler would still leave a long tail that could cause numerical instability. `log1p` compresses the range and makes the distribution more Gaussian-like, which is better suited for gradient-based optimization. The same logic applies to `number_of_reviews` (skew=3.56).
>
> **Assessment:** This is a solid approach. One potential improvement would be to also apply log transform to `availability_365` (skew=0.74), though the benefit would be marginal. Another option would be `MinMaxScaler` to bound inputs to [0,1], but StandardScaler is generally preferred for neural networks as it doesn't constrain the range.

---

### 6. Feature vs Target Visualizations
**Status: EXISTS — you have both `countplot` (categorical) and `boxplot` (numerical) visualizations**

Your code already includes:
- `plot_distribution_by_feature('room_type')` and `plot_distribution_by_feature('neighbourhood_group')` — countplots showing categorical feature distributions by price class
- `numerical_feature_distribution(...)` for all 4 numerical features — boxplots grouped by price class
- A multi-variable boxplot of amenity_score by room_type and price_class

These are good. Add a markdown cell interpreting the key findings:

> **Feature-Target Relationship Analysis:**
>
> *Categorical features:*
> - `room_type` shows clear separation: "Entire home/apt" is heavily concentrated in higher price classes (2, 3), while "Private room" dominates class 1. "Shared room" is rare and mostly in class 0-1. This feature appears highly predictive.
> - `neighbourhood_group`: Manhattan has a higher proportion of expensive listings (classes 2-3) compared to other boroughs. Brooklyn is more balanced. Bronx and Staten Island are almost entirely in lower price classes.
>
> *Numerical features:*
> - `amenity_score`: Shows moderate separation between classes. Higher price classes tend to have slightly higher amenity scores, but there is significant overlap.
> - `minimum_nights`: Distributions are very similar across classes with many outliers. Limited predictive power expected.
> - `number_of_reviews`: Similar distributions across classes. Not strongly discriminative.
> - `availability_365`: Some separation — higher-priced listings tend to have higher availability, possibly because they are booked less frequently.

---

### 7. Correlation Matrix
**Status: EXISTS — you have the heatmap**

Your code computes and plots the correlation matrix for numerical features including `price_class`. Add interpretation:

> **Correlation Matrix Analysis:**
>
> The correlation values between numerical features are all weak (|r| < 0.2), indicating no significant multicollinearity issues. Key observations:
> - No pair of features is highly correlated, so all features provide relatively independent information.
> - Correlations with `price_class` are also weak, suggesting that no single numerical feature is a strong linear predictor of the target. This implies the classification boundary is likely non-linear, which justifies using a neural network.
> - The strongest correlation with `price_class` appears to be with `amenity_score` and `availability_365`, though both are modest.

---

### 8. Feature Importance & Suspicious Features Discussion
**Status: MISSING — this is the empty markdown cell**

Add:

> **Expected Feature Importance:**
>
> Based on the EDA above:
> 1. **`room_type`** — Expected to be the **most influential** feature. The countplot shows clear class separation: "Entire home/apt" strongly predicts higher price classes, while "Private room" predicts lower ones. This makes intuitive sense as room type directly affects pricing.
> 2. **`neighbourhood_group`** — Second most influential. Manhattan listings skew toward higher price classes, consistent with real-world NYC pricing.
> 3. **`amenity_score`** and **`availability_365`** — Moderate influence. Boxplots show some separation between classes.
> 4. **`minimum_nights`** and **`number_of_reviews`** — Least influential. Distributions are nearly identical across classes.
>
> **Suspicious/Dominant Features:**
> `room_type` appears **unusually predictive** — the class distributions are almost entirely determined by room type. This could be because the `price_class` labels were partially derived from room type during dataset construction. If so, the model may achieve high accuracy primarily by learning room type patterns, which would limit its generalization value. This is worth noting but not necessarily a problem for the assignment.

---

## Part B(a): Two-Layer Perceptron

### 9-11. Forward/Backward Propagation & Cross-Entropy Loss
**Status: Implementation exists and is correct, but cross-entropy loss is never computed in the training loop**

Your `CrossEntropyLoss` class exists but is never instantiated or called during training. The assignment explicitly requires "Cross-entropy loss computation." Fix:

```python
from cross_entropy_loss import CrossEntropyLoss

loss_fn = CrossEntropyLoss()

# Inside training loop, after forward pass:
loss = loss_fn.compute_loss(y_train, y_hat_train)
# Track it:
sigmoid_acc_stats['train_loss'].append(loss)
```

Also add `'train_loss': []` and `'val_loss': []` to both stats dictionaries.

---

### 12. Sigmoid vs ReLU for Hidden Layers
**Status: Done correctly — Network 1 uses Sigmoid, Network 2 uses ReLU**

---

### 13. Gradient Properties Explanation
**Status: MISSING**

Add a markdown cell:

> **Sigmoid vs ReLU: Gradient Properties and Optimization**
>
> **Sigmoid** activation: σ(x) = 1/(1+e^(-x)), outputs in (0,1). Its derivative is σ(x)·(1-σ(x)), which has a maximum of 0.25 at x=0 and approaches 0 for large |x|. This causes the **vanishing gradient problem**: during backpropagation, gradients are multiplied through layers, and since each layer's gradient contribution is at most 0.25, gradients shrink exponentially with depth. For a 2-hidden-layer network, the gradient reaching the first layer is at most 0.25² = 0.0625 of the output gradient. This makes learning slow, especially in early layers.
>
> **ReLU** activation: f(x) = max(0, x). Its derivative is 1 for x > 0 and 0 for x ≤ 0. This means gradients flow unchanged through active neurons (no shrinkage), solving the vanishing gradient problem. However, neurons with negative inputs have zero gradient ("dying ReLU" problem), which can cause some neurons to permanently stop learning.
>
> **Expected outcome:** The ReLU network should converge faster and achieve higher accuracy than the Sigmoid network, particularly because our network has 2 hidden layers where gradient degradation compounds.

---

### 14. Vanilla Batch Gradient Descent for 200+ Iterations
**Status: Done (200 iterations, full-batch)**

---

### 15. Final Accuracy Values
**Status: Values are tracked but never explicitly printed**

Add after the training loop:

```python
print(f'Sigmoid Network - Final Train Accuracy: {sigmoid_acc_stats["train_acc"][-1]:.4f}')
print(f'Sigmoid Network - Final Val Accuracy: {sigmoid_acc_stats["val_acc"][-1]:.4f}')
print(f'ReLU Network - Final Train Accuracy: {relu_acc_stats["train_acc"][-1]:.4f}')
print(f'ReLU Network - Final Val Accuracy: {relu_acc_stats["val_acc"][-1]:.4f}')
```

---

### 16. Combined Accuracy Plot
**Status: MISSING — this is explicitly required**

```python
plt.figure(figsize=(12, 6))
iterations = range(1, ITERATIONS + 1)

plt.plot(iterations, sigmoid_acc_stats['train_acc'], label='Sigmoid Train Acc', color='blue', linestyle='-')
plt.plot(iterations, sigmoid_acc_stats['val_acc'], label='Sigmoid Val Acc', color='blue', linestyle='--')
plt.plot(iterations, relu_acc_stats['train_acc'], label='ReLU Train Acc', color='red', linestyle='-')
plt.plot(iterations, relu_acc_stats['val_acc'], label='ReLU Val Acc', color='red', linestyle='--')

plt.xlabel('Iteration')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy: Sigmoid vs ReLU')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Overall EDA Assessment

**Rating: Good, bordering on very good**

**What you're doing well:**
- Thorough missing value analysis with percentages
- Smart preprocessing pipeline design — separating skewed vs symmetric features into different pipelines is a strong choice
- Using `add_indicator=True` in imputers to preserve missingness signal
- Good variety of visualizations (distributions, countplots, boxplots, correlation heatmap, multi-variable boxplot)
- Clean code organization with reusable plotting functions

**What's holding it back from "very good":**
- No written analysis/justification anywhere — the visualizations exist but the assignment explicitly asks you to "comment on," "justify," "discuss," and "explicitly state" findings. The empty markdown cell needs to be filled.
- The EDA is done on `df_eda` (a copy of the full dataset) but the actual preprocessing pipeline is applied to `X_train_raw`/`X_val_raw` (the train/val split). This is correct practice but worth noting explicitly.

**Transformation quality:**
Your normalization/standardization approach is well-suited to the data. The log+StandardScaler for skewed features and StandardScaler for symmetric features is a textbook-correct approach. No major improvements needed — the main gap is documentation, not methodology.

---

## Summary of Missing Items

1. ~~Bar chart for class distribution~~ (you have displot, but a dedicated bar chart is cleaner)
2. **Markdown justifications** for: missing value strategy, encoding choice, normalization choice
3. **Markdown analysis** of: feature-target relationships, correlation matrix findings, feature importance expectations
4. **Use CrossEntropyLoss** in training loop and track loss values
5. **Markdown explanation** of sigmoid vs ReLU gradient properties
6. **Print final accuracy values** explicitly
7. **Combined accuracy-vs-iterations plot** for both networks
