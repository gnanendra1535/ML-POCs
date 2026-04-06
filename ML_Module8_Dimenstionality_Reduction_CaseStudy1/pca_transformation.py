# Using scikit learn perform a PCA transformation such that the transformed
# dataset can explain 95% of the variance in the original dataset. Find out the
# number of components in the projected subspace.
# [Hint: Refer to decomposition module of scikit learn]

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA

# Load digits dataset
digits = datasets.load_digits()
X = digits.data

# Perform PCA to retain 95% variance
pca = PCA(n_components=0.95, random_state=42)
X_pca = pca.fit_transform(X)

# Number of components chosen
print("Number of components to retain 95% variance:", pca.n_components_)

# Plot explained variance ratio
plt.figure(figsize=(8,5))
plt.plot(range(1, len(pca.explained_variance_ratio_)+1), 
         pca.explained_variance_ratio_.cumsum(), marker='o')
plt.xlabel("Number of Components")
plt.ylabel("Cumulative Explained Variance")
plt.title("PCA - Explained Variance vs Components")
plt.axhline(y=0.95, color='r', linestyle='--')
plt.grid(True)
plt.show()
