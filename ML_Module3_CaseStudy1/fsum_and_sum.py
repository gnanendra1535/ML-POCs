# Give an example of the fsum and sum function of the math library.

import math


numbers = [0.1] * 10

# Using built-in sum
sum_result = sum(numbers)

# Using math.fsum
fsum_result = math.fsum(numbers)

print("Using sum():", sum_result)
print("Using math.fsum():", fsum_result)

# Output:
# Using sum(): 1.0 
# Using math.fsum(): 1.0