# Write a program that accepts a sequence of comma separated 4 digit binary
# numbers as its input and then check whether they are divisible by 5 or not. The
# numbers that are divisible by 5 are to be printed in a comma-separated sequence.
# Example:
# 0100,0011,1010,1001
# Then the output should be:
# 1010

# Take comma-separated binary numbers as input
binary_numbers = input("Enter comma-separated 4-digit binary numbers: ").split(",")

divisible_by_5 = []

for b in binary_numbers:
    
    decimal_value = int(b, 2)
    
    if decimal_value % 5 == 0:
        divisible_by_5.append(b)

print(",".join(divisible_by_5))

# Example input:
# Enter comma-separated 4-digit binary numbers: 0100,0011,1010
# Example output:
# 1010