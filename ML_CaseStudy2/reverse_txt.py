#Please write a program that accepts a string from the console and print it in reverse
#order.
#  Example: If the following string is given as input to the program:
#  rise to vote sir
#  Then, the output of the program should be:
#  ris etov ot

# reverse_txt.py
text = input("Enter a string: ")
reversed_text = text[::-1]
print(reversed_text)

# Output the reversed string
# Explanation: The slicing [::-1] reverses the string.
# Example:
# Enter a string: rise to vote sir      
# ris etov ot esir

