# Create a numpy array having elements 0 to 10 And negate all the elements between
# 3 and 9

import numpy as np

arr = np.arange(11)

arr[(arr >= 3) & (arr <= 9)] *= -1

print("Array after negating elements between 3 and 9:")
print(arr)

# Output:
# Array after negating elements between 3 and 9:    
# [ 0  1  2 -3 -4 -5 -6 -7 -8 -9 10]
