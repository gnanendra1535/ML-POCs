# SVM classification on College.csv
# Steps:
# 1. Load data, encode target, 80-20 split
# 2. Fit Linear SVM (LinearSVC) on raw features
# 3. Standardize features and fit Linear SVM again
# 4. GridSearchCV to tune a non-linear SVM (RBF) and evaluate best model
# 5. Print classification reports and a summary table

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load data and prepare

df = pd.read_csv("/mnt/data/College.csv")

# Show columns (optional)
print("Columns in dataset:", df.columns.tolist())

# Encode target variable 'Private' -> numeric
le = LabelEncoder()
y = le.fit_transform(df['Private'])   # e.g., 'Yes'->1, 'No'->0
X = df.drop(columns=['Private'])

# Train-test split (80% train, 20% test), stratify to preserve class balance
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print("\nDataset sizes -> Total: {}, Train: {}, Test: {}".format(X.shape[0], X_train.shape[0], X_test.shape[0]))


# 2. Linear SVM on raw data

linear_raw = LinearSVC(max_iter=20000, random_state=42)
linear_raw.fit(X_train, y_train)
y_pred_raw = linear_raw.predict(X_test)

acc_raw = accuracy_score(y_test, y_pred_raw)
print("\n=== LinearSVC (raw features) ===")
print("Test Accuracy: {:.4f}".format(acc_raw))
print("Classification Report:\n", classification_report(y_test, y_pred_raw))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_raw))


# 3. Standardize features and refit LinearSVC

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

linear_scaled = LinearSVC(max_iter=20000, random_state=42)
linear_scaled.fit(X_train_scaled, y_train)
y_pred_scaled = linear_scaled.predict(X_test_scaled)

acc_scaled = accuracy_score(y_test, y_pred_scaled)
print("\n=== LinearSVC (StandardScaler applied) ===")
print("Test Accuracy: {:.4f}".format(acc_scaled))
print("Classification Report:\n", classification_report(y_test, y_pred_scaled))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_scaled))


# 4. Grid search to tune non-linear SVM (RBF kernel)

# Use a reasonably small grid so the search completes quickly.
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.01, 0.1, 1],
    'kernel': ['rbf']
}

# Perform GridSearchCV on scaled data (SVMs usually need scaling)
grid = GridSearchCV(SVC(), param_grid, cv=3, n_jobs=-1, verbose=1)
grid.fit(X_train_scaled, y_train)

best_model = grid.best_estimator_
best_params = grid.best_params_
best_cv_score = grid.best_score_

# Evaluate the tuned model on the test set
y_pred_grid = best_model.predict(X_test_scaled)
acc_grid = accuracy_score(y_test, y_pred_grid)

print("\n=== Non-linear SVM (GridSearchCV tuned, RBF) ===")
print("Best CV Score: {:.4f}".format(best_cv_score))
print("Best Parameters:", best_params)
print("Test Accuracy: {:.4f}".format(acc_grid))
print("Classification Report:\n", classification_report(y_test, y_pred_grid))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_grid))


# 5. Summary comparison

summary = pd.DataFrame({
    'Model': ['LinearSVC (raw)', 'LinearSVC (scaled)', 'SVC RBF (grid-best)'],
    'Test Accuracy': [acc_raw, acc_scaled, acc_grid]
})
print("\n=== Summary ===")
print(summary.to_string(index=False))
