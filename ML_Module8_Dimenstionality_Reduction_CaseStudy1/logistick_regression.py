
# Transform the dataset and fit a logistic regression and observe the accuracy.
# Compare it with the previous model and comment on the accuracy.
# [Hint: Project both the train and test samples to the new subspace]

# Compare Logistic Regression on original vs PCA-reduced digits dataset
# - 20% test split
# - PCA to retain 95% variance (fit on train, transform both train & test)
# - Train logistic regression on both representations
# - Print accuracy + classification reports and show side-by-side confusion matrices

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# --- Load data ---
digits = datasets.load_digits()
X = digits.data         # (n_samples, 64)
y = digits.target       # (n_samples,)

# --- Train-test split (keep stratify to preserve class proportions) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# --- Model on original data ---
model_orig = LogisticRegression(max_iter=5000, solver='lbfgs', multi_class='auto', random_state=42)
model_orig.fit(X_train, y_train)
y_pred_orig = model_orig.predict(X_test)

acc_orig = accuracy_score(y_test, y_pred_orig)
report_orig = classification_report(y_test, y_pred_orig, digits=4)
cm_orig = confusion_matrix(y_test, y_pred_orig)

print("=== Original Data ===")
print(f"Test accuracy: {acc_orig:.4f}")
print("Classification report:\n", report_orig)

# --- PCA: retain 95% variance (fit on training set) ---
pca = PCA(n_components=0.95, random_state=42)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)
n_components = pca.n_components_

print(f"Number of PCA components to retain 95% variance: {n_components}")

# --- Model on PCA-transformed data ---
model_pca = LogisticRegression(max_iter=5000, solver='lbfgs', multi_class='auto', random_state=42)
model_pca.fit(X_train_pca, y_train)
y_pred_pca = model_pca.predict(X_test_pca)

acc_pca = accuracy_score(y_test, y_pred_pca)
report_pca = classification_report(y_test, y_pred_pca, digits=4)
cm_pca = confusion_matrix(y_test, y_pred_pca)

print("\n=== PCA-Transformed Data ===")
print(f"Test accuracy: {acc_pca:.4f}")
print("Classification report:\n", report_pca)

# --- Comparison summary ---
print("\n--- Summary ---")
print(f"Accuracy (original 64-d): {acc_orig:.4f}")
print(f"Accuracy (PCA {n_components}-d): {acc_pca:.4f}")
print("Note: PCA reduced dimensionality from 64 ->", n_components)

# --- Plot side-by-side confusion matrices ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, cm, title in zip(axes, [cm_orig, cm_pca], ["Confusion Matrix (Original)", f"Confusion Matrix (PCA {n_components}D)"]):
    im = ax.imshow(cm, interpolation='nearest')
    ax.set_title(title)
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    ax.set_xticks(np.arange(10))
    ax.set_yticks(np.arange(10))
    # Annotate cells
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, cm[i, j], ha="center", va="center")
fig.colorbar(im, ax=axes.ravel().tolist())
plt.tight_layout()
plt.show()

# --- (Optional) Show a few test images with predicted vs true labels for PCA model ---
def plot_sample_predictions(X_test_raw, X_test_repr, y_true, y_pred, n=12):
    """
    X_test_raw: original flattened pixels (for plotting 8x8)
    X_test_repr: representation used for prediction (not used for plotting but kept for clarity)
    """
    idxs = np.random.choice(len(y_true), size=n, replace=False)
    ncols = 6
    nrows = int(np.ceil(n / ncols))
    plt.figure(figsize=(12, 2 + 2*nrows))
    for i, idx in enumerate(idxs):
        ax = plt.subplot(nrows, ncols, i + 1)
        img = X_test_raw[idx].reshape(8, 8)
        ax.imshow(img, cmap='gray')
        ax.axis('off')
        ax.set_title(f"T:{y_true[idx]} / P:{y_pred[idx]}")
    plt.suptitle("Random test samples: True (T) vs Predicted (P) — PCA-model")
    plt.tight_layout()
    plt.show()

plot_sample_predictions(X_test, X_test_pca, y_test, y_pred_pca, n=12)
