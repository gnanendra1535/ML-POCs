# 11.Create a random array of 3 rows and 3 columns and sort it according to 1st column, 2nd column, or 3rd column

import numpy as np


arr = np.random.randint(1, 100, size=(3, 3))

print("Original Array:")
print(arr)


sorted_by_first = arr[arr[:, 0].argsort()]


sorted_by_second = arr[arr[:, 1].argsort()]


sorted_by_third = arr[arr[:, 2].argsort()]

print("\nSorted by 1st column:")
print(sorted_by_first)

print("\nSorted by 2nd column:")
print(sorted_by_second)

print("\nSorted by 3rd column:")
print(sorted_by_third)

# Output will vary each time due to randomness
# Original Array:
# [[34 67 23]
#  [12 45 78]
#  [56 89 10]]
# Sorted by 1st column:
# [[12 45 78]
#  [34 67 23]
#  [56 89 10]]
# Sorted by 2nd column:

# [[12 45 78]
#  [34 67 23]
#  [56 89 10]]
# Sorted by 3rd column:
# [[56 89 10]
#  [34 67 23]   
#  [12 45 78]]

