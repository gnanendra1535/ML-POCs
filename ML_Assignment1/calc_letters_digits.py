sentence = input("Enter a sentence: ")
letters = 0
digits = 0
for char in sentence:
    if char.isalpha():  # Check if it's a letter
        letters += 1
    elif char.isdigit():  # Check if it's a digit
        digits += 1
print("LETTERS:", letters)
print("DIGITS:", digits)