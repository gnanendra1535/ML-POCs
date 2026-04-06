# Using scikit learn to perform an LDA on the dataset. Find out the number of
# components in the projected subspace.
# [Hint: Refer to a discriminant analysis module of scikit learn]

# Perform Linear Discriminant Analysis (LDA) on the digits dataset
# and find the number of components in the projected subspace

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# Load dataset
digits = datasets.load_digits()
X = digits.data       # (n_samples, 64 features)
y = digits.target     # labels 0–9

# Train-test split (80-20 as before)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Apply LDA
lda = LDA()
X_train_lda = lda.fit_transform(X_train, y_train)
X_test_lda = lda.transform(X_test)

# Number of components in LDA
n_components = lda.n_components_

print("Number of components in the projected LDA subspace:", n_components)
print("Original feature dimension:", X.shape[1])
print("Reduced feature dimension:", X_train_lda.shape[1])