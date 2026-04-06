# Cancer detection (malignant vs benign) with fewer features while maintaining high accuracy.
# Using LDA for dimensionality reduction and Logistic Regression for classification.
# Dataset: Breast Cancer Wisconsin (Diagnostic) Dataset from sklearn    


# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load Data
data = pd.read_csv("breast-cancer-data.csv")
print(data.head())
print(data.info())

# Split Features and Target
X = data.drop(columns=['diagnosis'])   # assuming 'diagnosis' column = Malignant/Benign
y = data['diagnosis'].map({'M':1, 'B':0})  # Encode: M=1, B=0

# Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Standardize features (important for PCA/LDA)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# PCA (retain 95% variance)
pca = PCA(n_components=0.95, random_state=42)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

print("Original features:", X.shape[1])
print("PCA reduced features:", pca.n_components_)

# Logistic Regression with PCA
model_pca = LogisticRegression(max_iter=5000, random_state=42)
model_pca.fit(X_train_pca, y_train)
y_pred_pca = model_pca.predict(X_test_pca)

print("\n=== PCA Results ===")
print("Accuracy:", accuracy_score(y_test, y_pred_pca))
print(classification_report(y_test, y_pred_pca))

# LDA (supervised dimensionality reduction, 1 component for binary classification)
lda = LDA(n_components=1)
X_train_lda = lda.fit_transform(X_train_scaled, y_train)
X_test_lda = lda.transform(X_test_scaled)

model_lda = LogisticRegression(max_iter=5000, random_state=42)
model_lda.fit(X_train_lda, y_train)
y_pred_lda = model_lda.predict(X_test_lda)

print("\n=== LDA Results ===")
print("Accuracy:", accuracy_score(y_test, y_pred_lda))
print(classification_report(y_test, y_pred_lda))

# Confusion Matrix (PCA)
cm_pca = confusion_matrix(y_test, y_pred_pca)
sns.heatmap(cm_pca, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix - PCA Model")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
