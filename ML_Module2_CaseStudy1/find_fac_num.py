# Write a program that will find factors of the given number and find whether the
# factor is even or odd.
# Hint: Use Loop with if-else statements

# Program to find factors of a number and check if they are even or odd

# Take input from user
num = int(input("Enter a number: "))

print(f"Factors of {num} and their type (Even/Odd):")

# Loop to find factors
for i in range(1, num + 1):
    if num % i == 0:  # i is a factor
        if i % 2 == 0:
            print(f"{i} → Even")
        else:
            print(f"{i} → Odd")

# Output the factors and their type

# Example:
# Enter a number: 12
# Factors of 12 and their type (Even/Odd):
# 1 → Odd
# 2 → Even
# 3 → Odd
# 4 → Even
# 6 → Even
# 12 → Even
