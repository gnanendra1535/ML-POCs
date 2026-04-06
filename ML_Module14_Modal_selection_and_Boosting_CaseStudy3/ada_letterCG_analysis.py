# ada_letterCG_analysis.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score

DATA_PATH = "letterCG.data"
PLOT_PATH = "ada_weak_learners.png"
RANDOM_STATE = 42


# Try a few common separators; fallback to whitespace
sep_candidates = [',', '\t', ';', r'\s+']
for sep in sep_candidates:
    try:
        if sep == r'\s+':
            df = pd.read_csv(DATA_PATH, header=None, delim_whitespace=True)
        else:
            df = pd.read_csv(DATA_PATH, header=None, sep=sep)
        # require at least 2 columns to accept
        if df.shape[1] >= 2:
            print(f"Loaded using separator: '{sep}' (shape={df.shape})")
            break
    except Exception as e:
        # continue trying other separators
        df = None

if df is None:
    raise RuntimeError("Failed to load the data. Check file path or delimiter.")

# Inspect first rows
print("Preview of data:")
print(df.head())

# Heuristics to pick target column:
# If first column is non-numeric (strings like letter classes), use it as target.
# Otherwise if last column non-numeric use it; else assume first column is target.
first_col_non_numeric = not pd.to_numeric(df.iloc[:, 0], errors='coerce').notna().all()
last_col_non_numeric  = not pd.to_numeric(df.iloc[:, -1], errors='coerce').notna().all()

if first_col_non_numeric:
    target_col = 0
    print("Detected non-numeric first column -> using column 0 as target.")
elif last_col_non_numeric:
    target_col = df.shape[1] - 1
    print("Detected non-numeric last column -> using last column as target.")
else:
    # fallback: use first column as target (common in letter datasets)
    target_col = 0
    print("No non-numeric columns detected; defaulting to column 0 as target.")

# Separate X and y
y = df.iloc[:, target_col].astype(str).str.strip()
X = df.drop(columns=[df.columns[target_col]]).copy()

# Convert remaining columns to numeric (if not already)
for c in X.columns:
    X[c] = pd.to_numeric(X[c], errors='coerce')

# If any NaNs introduced, we can fill them (median)
if X.isna().any().any():
    X = X.fillna(X.median())

print(f"Features shape: {X.shape}, Target shape: {y.shape}")
print("Target value counts:")
print(y.value_counts().head(10))

# ---------- 1b) Train-test split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
)
print("Train shape:", X_train.shape, "Test shape:", X_test.shape)

# ---------- 2 & 3) AdaBoost with varying number of weak learners ----------
n_weakers = list(range(1, 17))  # 1..16

def evaluate_adaboost_with_depth(max_depth):
    """
    Train AdaBoost with DecisionTree base learners of given max_depth,
    for n_estimators in n_weakers. Return list of test accuracies.
    """
    accuracies = []
    for n in n_weakers:
        base = DecisionTreeClassifier(max_depth=max_depth, random_state=RANDOM_STATE)
        ada = AdaBoostClassifier(estimator=base, n_estimators=n, random_state=RANDOM_STATE)
        ada.fit(X_train, y_train)
        y_pred = ada.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        accuracies.append(acc)
        print(f"depth={max_depth}, n_estimators={n} -> test accuracy: {acc:.4f}")
    return accuracies

print("\nEvaluating AdaBoost (base tree max_depth=1)...")
acc_depth1 = evaluate_adaboost_with_depth(max_depth=1)

print("\nEvaluating AdaBoost (base tree max_depth=2)...")
acc_depth2 = evaluate_adaboost_with_depth(max_depth=2)

# ---------- 4) Plot results ----------
plt.figure(figsize=(10,6))
plt.plot(n_weakers, acc_depth1, marker='o', label='max_depth=1')
plt.plot(n_weakers, acc_depth2, marker='o', label='max_depth=2')
plt.xticks(n_weakers)
plt.xlabel("Number of weak learners (n_estimators)")
plt.ylabel("Test set accuracy")
plt.title("AdaBoost Test Accuracy vs Number of Weak Learners\n(DecisionTree base, depths 1 and 2)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(PLOT_PATH)
plt.show()

print(f"\nPlot saved to: {PLOT_PATH}")