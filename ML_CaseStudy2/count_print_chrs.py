#. Please write a program that counts and prints the numbers of each character in a
# string input by the console.
#  Example: If the following string is given as input to the program:
#  abcdefgabc
#  Then, the output of the program should be:
# a,2
# c,2
# b,2
# e,1
# d,1
# g,1
# f,1

# count_print_chrs.py

text = input("Enter a string: ")

char_count = {}

for char in text:
    char_count[char] = char_count.get(char, 0) + 1

for char in dict.fromkeys(text): 
    print(f"{char},{char_count[char]}")

# Output the character counts
# Enter a string: abcdefgabc
# a,2
# b,2
# c,2
# d,1
# e,1
# f,1
# g,1
