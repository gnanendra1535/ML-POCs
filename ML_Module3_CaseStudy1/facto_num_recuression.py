# Write a program that can compute the factorial of a given numb. Use recursion to
# find it.
# Hint: Suppose the following input is supplied to the program: 8
# Then, the output should be:
# 40320

def factorial(n: int) -> int:
    # Base case
    if n == 0 or n == 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)

num = int(input("Enter a number: "))

result = factorial(num)
print(result)

# Example:
# Enter a number: 8
# 40320

