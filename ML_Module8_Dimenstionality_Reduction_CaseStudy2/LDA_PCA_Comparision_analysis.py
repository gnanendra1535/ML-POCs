# Transform the dataset and fit a logistic regression and observe the accuracy.
# Compare it with the previous model based on PCA in terms of accuracy and
# model complexity.
# [Hint: Project both the train and test samples to the new subspace]

# Compare Logistic Regression performance on LDA-transformed vs PCA-transformed digits dataset
# - 80-20 split
# - LDA: projects data into (n_classes - 1) = 9 dimensions
# - PCA: projects data to retain 95% variance (~29 dimensions)
# - Logistic Regression trained on both
# - Compare accuracy and complexity

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# --- Load dataset ---
digits = datasets.load_digits()
X = digits.data
y = digits.target

# --- Train-test split (80-20) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# --- PCA transformation (retain 95% variance) ---
pca = PCA(n_components=0.95, random_state=42)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)
pca_components = pca.n_components_

# Logistic Regression on PCA
model_pca = LogisticRegression(max_iter=5000, solver='lbfgs', multi_class='auto', random_state=42)
model_pca.fit(X_train_pca, y_train)
y_pred_pca = model_pca.predict(X_test_pca)
acc_pca = accuracy_score(y_test, y_pred_pca)

# --- LDA transformation ---
lda = LDA()
X_train_lda = lda.fit_transform(X_train, y_train)
X_test_lda = lda.transform(X_test)
lda_components = lda.n_components_

# Logistic Regression on LDA
model_lda = LogisticRegression(max_iter=5000, solver='lbfgs', multi_class='auto', random_state=42)
model_lda.fit(X_train_lda, y_train)
y_pred_lda = model_lda.predict(X_test_lda)
acc_lda = accuracy_score(y_test, y_pred_lda)

# --- Results ---
print("=== PCA Model ===")
print(f"Number of components: {pca_components}")
print(f"Accuracy: {acc_pca:.4f}\n")

print("=== LDA Model ===")
print(f"Number of components: {lda_components}")
print(f"Accuracy: {acc_lda:.4f}\n")

print("--- Comparison ---")
print(f"PCA (29D) -> Accuracy: {acc_pca:.4f}")
print(f"LDA (9D)  -> Accuracy: {acc_lda:.4f}")
print("Comment: LDA uses fewer dimensions (9 vs ~29) making it more compact, while accuracy remains comparable.")
