# Compute the confusion matrix and count the number of instances that have
# gone wrong. For each wrong sample, plot the digit along with the predicted
# and original label.

# Compute confusion matrix, count wrong predictions, and plot each wrong digit
# - Uses PCA (retain 95%) + Logistic Regression like before
# - Plots every misclassified sample with True vs Predicted labels
# - If there are a lot of misclassifications, set max_plots to limit how many to show

import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
MAX_PLOTS = None   # Set to an int (e.g. 48) to limit plots, or None to show all misclassified samples

# --- Load data ---
digits = datasets.load_digits()
X = digits.data       # shape (n_samples, 64)
y = digits.target     # labels 0-9

# --- Train/test split (same setup used earlier) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
)

# --- PCA (fit on train, transform both) ---
pca = PCA(n_components=0.95, random_state=RANDOM_STATE)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# --- Train logistic regression on PCA-transformed features ---
model = LogisticRegression(max_iter=5000, solver='lbfgs', multi_class='auto', random_state=RANDOM_STATE)
model.fit(X_train_pca, y_train)

# --- Predict on test set (PCA representation) ---
y_pred = model.predict(X_test_pca)

# --- Confusion matrix and count wrong predictions ---
cm = confusion_matrix(y_test, y_pred)
num_wrong = (y_test != y_pred).sum()
total = len(y_test)

print("Confusion matrix (rows=true, cols=predicted):\n", cm)
print(f"\nTotal test samples: {total}")
print(f"Number of misclassified samples: {num_wrong}")
print(f"Accuracy (computed from confusion matrix): {1 - num_wrong/total:.4f}")

# --- Collect indices of misclassified samples ---
wrong_indices = np.where(y_test != y_pred)[0]  # indices relative to X_test

# Optionally limit how many to plot
if MAX_PLOTS is not None and MAX_PLOTS > 0:
    if MAX_PLOTS < len(wrong_indices):
        print(f"\nPlotting first {MAX_PLOTS} of {len(wrong_indices)} misclassified samples.")
        wrong_indices = wrong_indices[:MAX_PLOTS]
    else:
        print(f"\nPlotting all {len(wrong_indices)} misclassified samples.")
else:
    print(f"\nPlotting all {len(wrong_indices)} misclassified samples.")

# --- Plot misclassified samples in a grid ---
n_wrong = len(wrong_indices)
if n_wrong == 0:
    print("No misclassified samples to plot. All predictions are correct!")
else:
    ncols = 6
    nrows = math.ceil(n_wrong / ncols)
    plt.figure(figsize=(ncols * 2, nrows * 2.2))
    for i, idx in enumerate(wrong_indices):
        ax = plt.subplot(nrows, ncols, i + 1)
        img = X_test[idx].reshape(8, 8)   # original 8x8 image from test set
        ax.imshow(img, cmap='gray')
        true_label = y_test[idx]
        pred_label = y_pred[idx]
        ax.set_title(f"T:{true_label} → P:{pred_label}")
        ax.axis('off')
    plt.suptitle("Misclassified test samples (True -> Predicted) — PCA + Logistic Regression", fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
