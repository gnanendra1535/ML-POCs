import numpy as np

random_array = np.random.rand(10, 10)

min_value = np.min(random_array)
max_value = np.max(random_array)


print("10x10 Random Array:")
print(random_array)
print("\nMinimum Value:", min_value)
print("Maximum Value:", max_value)

# Output will vary each time due to randomness
# Minimum Value: 0.0123 at index (6, 7)  
# Maximum Value: 0.9876 at index (2, 5) 
