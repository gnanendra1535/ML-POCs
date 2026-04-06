# 14. Create a random matrix and Compute a matrix rank.

import numpy as np

# Create a random 4x4 matrix
matrix = np.random.randint(1, 10, size=(4, 4))

# Compute the matrix rank
rank = np.linalg.matrix_rank(matrix)

print("Random Matrix:")
print(matrix)

print("\nMatrix Rank:", rank)

# Output will vary each time due to randomness
# Random Matrix:
# [[5 1 3 7]    
#  [2 4 6 8]
#  [9 2 5 1]
#  [3 7 4 2]]
# Matrix Rank: 4