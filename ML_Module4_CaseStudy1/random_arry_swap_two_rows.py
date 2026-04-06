# 13. Create a random array and swap two rows of an array.

import numpy as np

# Create a random 2D array (5x5 for example)
arr = np.random.randint(1, 100, size=(5, 5))

print("Original Array:")
print(arr)

# Swap row 1 and row 3 (index 0 and 2)
arr[[0, 2]] = arr[[2, 0]]

print("\nArray after swapping row 1 and row 3:")
print(arr)

# Output will vary each time due to randomness
# Original Array:
# [[34 67 23 45 89]
#  [12 45 78 56 90]
#  [56 89 10 23 67]
#  [78 12 34 56 23]
#  [90 34 67 89 12]]
# Array after swapping row 1 and row 3:
# [[56 89 10 23 67]
#  [12 45 78 56 90]
#  [34 67 23 45 89]
#  [78 12 34 56 23]
#  [90 34 67 89 12]]

