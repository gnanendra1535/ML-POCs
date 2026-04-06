# .Write a program to compute 1/2+2/3+3/4+...+n/n+1 with a given n input by
# console (n>0).
# Example:
# If the following n is given as input to the program:
# 5
# Then, the output of the program should be:
# 3.55


n = int(input("Enter a positive integer (n > 0): "))

total = sum(i / (i + 1) for i in range(1, n + 1))

print(round(total, 2))

# Output the computed series    

# Enter a positive integer (n > 0): 5
# 3.55
