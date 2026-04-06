# Naive Bayes classification on "run_or_walk.csv"
# Compare: (1) All features, (2) Only acceleration, (3) Only gyro

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# --- Load dataset ---
df = pd.read_csv("/mnt/data/run_or_walk.csv")

# --- Target variable ---
y = df['activity']

# --- 1. All predictors (acceleration + gyro) ---
X_all = df[['acceleration_x', 'acceleration_y', 'acceleration_z', 'gyro_x', 'gyro_y', 'gyro_z']]
X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42, stratify=y)

nb_all = GaussianNB()
nb_all.fit(X_train, y_train)
y_pred_all = nb_all.predict(X_test)

acc_all = accuracy_score(y_test, y_pred_all)
print("\n=== GaussianNB with ALL features ===")
print("Accuracy:", acc_all)
print(classification_report(y_test, y_pred_all))

# --- 2. Only acceleration predictors ---
X_acc = df[['acceleration_x', 'acceleration_y', 'acceleration_z']]
X_train_acc, X_test_acc, y_train_acc, y_test_acc = train_test_split(X_acc, y, test_size=0.2, random_state=42, stratify=y)

nb_acc = GaussianNB()
nb_acc.fit(X_train_acc, y_train_acc)
y_pred_acc = nb_acc.predict(X_test_acc)

acc_acc = accuracy_score(y_test_acc, y_pred_acc)
print("\n=== GaussianNB with ACCELERATION features ===")
print("Accuracy:", acc_acc)
print(classification_report(y_test_acc, y_pred_acc))

# --- 3. Only gyro predictors ---
X_gyro = df[['gyro_x', 'gyro_y', 'gyro_z']]
X_train_gyro, X_test_gyro, y_train_gyro, y_test_gyro = train_test_split(X_gyro, y, test_size=0.2, random_state=42, stratify=y)

nb_gyro = GaussianNB()
nb_gyro.fit(X_train_gyro, y_train_gyro)
y_pred_gyro = nb_gyro.predict(X_test_gyro)

acc_gyro = accuracy_score(y_test_gyro, y_pred_gyro)
print("\n=== GaussianNB with GYRO features ===")
print("Accuracy:", acc_gyro)
print(classification_report(y_test_gyro, y_pred_gyro))

# --- Summary ---
print("\n--- Accuracy Comparison ---")
print(f"All features:       {acc_all:.4f}")
print(f"Acceleration only:  {acc_acc:.4f}")
print(f"Gyro only:          {acc_gyro:.4f}")

print("\nComment: Acceleration is the most important predictor for distinguishing running vs walking. Gyro alone performs poorly.")
