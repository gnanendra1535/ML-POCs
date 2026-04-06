# We shall use the same dataset used in the previous assignment - digits. Make
# an 80-20 train/test split.
# [Hint: Explore datasets module from scikit learn]

# Load the digits dataset and perform an 80-20 train/test split

from sklearn import datasets
from sklearn.model_selection import train_test_split

# Load dataset
digits = datasets.load_digits()
X = digits.data       # Flattened 8x8 images (64 features)
y = digits.target     # Labels (0–9)

# 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Print dataset info
print("Total samples:", X.shape[0])
print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])
