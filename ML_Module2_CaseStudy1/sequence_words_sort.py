# Write a code that accepts a sequence of words as input and prints the words in a
# sequence after sorting them alphabetically.
# Hint: In the case of input data being supplied to the question, it should be
# assumed to be a console input.


words = input("Enter words separated by spaces: ")
word_list = words.split()
word_list.sort()
print("Sorted words:")
print(" ".join(word_list))

# Example input: "banana apple cherry"
# Example output: "apple banana cherry"

