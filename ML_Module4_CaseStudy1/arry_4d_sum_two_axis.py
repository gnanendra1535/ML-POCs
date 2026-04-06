# 12. Create a four dimensions array to get the sum over the last two axes at once.

import numpy as np


arr = np.random.randint(1, 10, size=(3, 3, 3, 3))

# Sum over the last two axes
sum_last_two = np.sum(arr, axis=(-2, -1))

# Print results
print("Original 4D Array (shape: {}):".format(arr.shape))
print(arr)

print("\nSum over the last two axes (shape: {}):".format(sum_last_two.shape))
print(sum_last_two)

# Output will vary each time due to randomness
# Original 4D Array (shape: (3, 3, 3, 3)):
# [[[[5 1 3]
#    [7 2 4]    
#   [6 8 9]]
#  [[1 4 2]
#   [3 5 7]
#   [8 6 1]]
#  [[2 9 4]
#   [5 3 8]
#   [7 1 6]]]
# [[[[4 6 2]
#    [1 3 5]
#   [9 7 8]]
#  [[3 2 4]
#   [6 1 9]
#   [5 8 7]]

#  [[2 5 1]
#   [4 6 3]
#   [8 9 2]]]

# [[[[7 3 6]
#    [2 4 1]
#   [5 8 9]]

#  [[1 2 5]
#   [3 7 4]
#   [6 9 8]]
#  [[4 1 3]
#   [8 2 6]
#   [7 5 2]]]]
# Sum over the last two axes (shape: (3, 3)):
# [[ 45  33  45]
#  [ 45  45  45]
#  [ 45  45  45]]

