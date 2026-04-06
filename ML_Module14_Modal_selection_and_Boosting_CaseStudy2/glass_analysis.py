# glass_analysis.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Path to your uploaded file (adjust if needed)
DATA_PATH = "glass.csv"

# 1) Load data and inspect
df = pd.read_csv(DATA_PATH)
print("Loaded data shape:", df.shape)
print("Columns:", df.columns.tolist())
display(df.head())

# Detect target column (common glass dataset name is 'Type'); fallback to last column
target_col = None
for c in df.columns:
    if c.lower() == 'type' or 'glass' in c.lower():
        target_col = c
        break
if target_col is None:
    target_col = df.columns[-1]
print("Using target column:", target_col)
print(df[target_col].value_counts())

# Bar plot of different glass types
type_counts = df[target_col].value_counts().sort_index()
plt.figure(figsize=(8,4))
plt.bar(type_counts.index.astype(str), type_counts.values)
plt.title("Counts of Glass Types")
plt.xlabel("Glass Type")
plt.ylabel("Count")
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.show()

# Prepare features and labels
X = df.drop(columns=[target_col]).copy()
y = df[target_col].copy()

# Convert non-numeric columns if any (this dataset generally numeric)
for col in X.columns:
    if X[col].dtype == object:
        X[col] = pd.to_numeric(X[col], errors='coerce')

# Train/test split and Decision Tree
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
y_pred = dt.predict(X_test)
acc_dt = accuracy_score(y_test, y_pred)
print(f"Decision Tree Test Accuracy: {acc_dt:.4f}")
print("Classification report (Decision Tree):")
print(classification_report(y_test, y_pred))

# KFold with 3 splits — measure accuracy for each split
kf = KFold(n_splits=3, shuffle=True, random_state=42)
fold_accuracies = []
for fold, (train_idx, val_idx) in enumerate(kf.split(X), start=1):
    X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_tr, y_tr)
    y_val_pred = model.predict(X_val)
    acc = accuracy_score(y_val, y_val_pred)
    fold_accuracies.append(acc)
    print(f"Fold {fold} accuracy: {acc:.4f}")
print("Mean 3-fold accuracy:", np.mean(fold_accuracies))

# GridSearchCV for RandomForest n_estimators with 10-fold CV
rfc = RandomForestClassifier(random_state=42)
param_grid = {'n_estimators': [10, 50, 100, 200, 300]}
grid = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=10, scoring='accuracy', n_jobs=-1)
grid.fit(X, y)
print("GridSearch best params:", grid.best_params_)
print("Best CV accuracy:", grid.best_score_)

# Show grid results as DataFrame
cv_results = pd.DataFrame(grid.cv_results_)
display(cv_results[['param_n_estimators','mean_test_score','std_test_score']].sort_values('param_n_estimators'))

# Plot mean CV accuracy vs n_estimators
plt.figure(figsize=(8,4))
plt.plot(cv_results['param_n_estimators'].astype(int), cv_results['mean_test_score'], marker='o')
plt.title("GridSearchCV: Mean CV Accuracy vs n_estimators (RandomForest)")
plt.xlabel("n_estimators")
plt.ylabel("Mean CV Accuracy")
plt.grid(True)
plt.show()

# Save outputs
out_dir = "/glass_outputs"
os.makedirs(out_dir, exist_ok=True)
cv_results.to_csv(os.path.join(out_dir, "rf_grid_cv_results.csv"), index=False)
pd.DataFrame({'kf3_fold_accuracies': fold_accuracies}).to_csv(os.path.join(out_dir, "kf3_fold_accuracies.csv"), index=False)
pd.DataFrame({'y_test': y_test.reset_index(drop=True), 'dt_pred': y_pred}).to_csv(os.path.join(out_dir, "dt_test_predictions.csv"), index=False)
print("Saved outputs to", out_dir)
