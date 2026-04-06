# Write a program, which will find all the numbers between 1000 and 3000 (both
# included) such that each digit of a number is an even number. The numbers
# obtained should be printed in a comma-separated sequence on a single line.
# Hint: In the case of input data being supplied to the question, it should be
# assumed to be a console input. Divide each digit by 2 and verify whether is it
# even or not.

# find_nums-even_list.py

result = []

for num in range(1000, 3001):
    num_str = str(num)
    if all(int(digit) % 2 == 0 for digit in num_str):
        result.append(str(num))

# Print in comma-separated format
print(",".join(result))

# Example output for the range 1000 to 3000:
# 2000,2002,2004,2006,2008,2020....


