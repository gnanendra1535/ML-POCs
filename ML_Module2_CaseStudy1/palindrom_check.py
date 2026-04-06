# Design a code that will find whether the given number is a Palindrome number or
# not.
# Hint: Use built-in functions of string.

# Palindrome number check
num = input("Enter a number: ")
if num == num[::-1]:
    print(f"{num} is a Palindrome number.")
else:
    print(f"{num} is NOT a Palindrome number.")

# Example:
# Enter a number: 121   
# 121 is a Palindrome number.
# Enter a number: 123
# 123 is NOT a Palindrome number.
