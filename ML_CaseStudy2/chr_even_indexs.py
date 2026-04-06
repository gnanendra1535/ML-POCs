#Please write a program that accepts a string from the console and print the
# characters that have even indexes.
#  Example: If the following string is given as input to the program:
#  H1e2l3l4o5w6o7r8l9d
#  Then, the output of the program should be:
#  Helloworld


text = input("Enter a string: ")


result = text[::2]

# Print the result
print(result)

# Output the characters at even indexes
# Explanation: The slicing [::2] takes every second character starting from index 0,
# which corresponds to the characters at even indexes.

# Example:
# Enter a string: H1e2l3l4o5w6o7r8l9d
# Helloworld

