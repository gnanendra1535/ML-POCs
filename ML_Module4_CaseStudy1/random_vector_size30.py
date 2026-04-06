# 9. Create a random vector of size 30 and find the mean value.
import numpy as np


random_vector = np.random.rand(30)


mean_value = np.mean(random_vector)


print("Random Vector (size 30):")
print(random_vector)
print("\nMean Value:", mean_value)

# Output will vary each time due to randomness
# Mean Value: 0.4567
