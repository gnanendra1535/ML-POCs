# Write a program that accepts a sequence of whitespace-separated words as input
# and prints the words after removing all duplicate words and sorting them
# alphanumerically.
# Suppose the following input is supplied to the program:
#  hello world and practice makes perfect and hello world again
#  Then, the output should be:
#  again and hello makes perfect practice world


words = input("Enter words: ").split()

unique_sorted_words = sorted(set(words))

print(" ".join(unique_sorted_words))

# Example:
# Enter words: hello world and practice makes perfect and hello world again
# Output: again and hello makes perfect practice world
