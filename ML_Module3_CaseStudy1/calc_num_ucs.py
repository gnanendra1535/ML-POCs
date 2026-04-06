# .Write a program that accepts a sentence and calculates the number of upper case
# letters and lower case letters.
#  Suppose the following input is supplied to the program:
#  Hello world!
#  Then, the output should be:
#  UPPER CASE 1
#  LOWER CASE 9

def count_case(sentence):
    upper_count = 0
    lower_count = 0
    
    for char in sentence:
        if char.isupper():
            upper_count += 1
        elif char.islower():
            lower_count += 1
    
    print(f"UPPER CASE {upper_count}")
    print(f"LOWER CASE {lower_count}")


# Example
input_sentence = input("Enter a sentence: ")
count_case(input_sentence)

# Example:
# Enter a sentence: Hello world!    
# UPPER CASE 1
# LOWER CASE 9

