# Write a program that accepts sequence of lines as input and prints the lines after
# making all characters in the sentence capitalized.
# Suppose the following input is supplied to the program:
#  Hello world
#  Practice makes perfect
#  Then, the output should be:
#  HELLO WORLD
#  PRACTICE MAKES PERFECT

# Accept multiple lines of input
lines = []
while True:
    try:
        line = input()
        if line.strip() == "":
            break
        lines.append(line.upper()) 
    except EOFError:
        break

for l in lines:
    print(l)

# Example:
# Input:    
# Hello world
# Practice makes perfect
# Output:
# HELLO WORLD
# PRACTICE MAKES PERFECT