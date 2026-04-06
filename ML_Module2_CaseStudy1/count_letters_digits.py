# Write a program that accepts a sentence and calculates the number of letters and
# digits.
# Suppose the entered string is: Python0325
# Then the output will be:
# LETTERS: 6
# DIGITS:4
# Hint: Use built-in functions of string.

# Program to count letters and digits in a string

sentence = input("Enter a sentence: ")

letters = 0
digits = 0

for char in sentence:
    if char.isalpha():
        letters += 1
    elif char.isdigit():
        digits += 1

# Print the results
print(f"LETTERS: {letters}")
print(f"DIGITS: {digits}")

# Output the counts
# Example:          
# Enter a sentence: Python0325
# LETTERS: 6                                
# DIGITS: 4

