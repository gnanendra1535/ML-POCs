# Write a program that calculates and prints the value according to the given formula:
# Q = Square root of [(2 * C * D)/H]
# Following are the fixed values of C and H: C is 50. H is 30.
# D is the variable whose values should be input to your program in a commaseparated sequence.
#  Example:
# Let us assume the following comma-separated input sequence is given to the
# program:
# 100,150,180
# The output of the program should be:
# 18,22,24


import math

# Fixed values
C = 50
H = 30

# Take comma-separated input for D
input_values = input("Enter values of D (comma-separated): ").split(',')

# Calculate Q for each D
results = []
for d in input_values:
    D = int(d)
    Q = int(round(math.sqrt((2 * C * D) / H)))
    results.append(str(Q))

# Output results
print(",".join(results))

# Example input:
# Enter values of D (comma-separated): 100,150,180
# Example output:
# 18,22,24