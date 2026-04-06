# Create a numpy array [[0, 1, 2], [ 3, 4, 5], [ 6, 7, 8],[ 9, 10, 11]]) and filter the elements
# greater than 5.
import numpy as np

# Create the array
arr = np.array([[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [9, 10, 11]])

# Filter elements greater than 5
result = arr[arr > 5]

print("Original array:\n", arr)
print("Elements greater than 5:", result)