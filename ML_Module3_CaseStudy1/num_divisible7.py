# Write a program that will find all such numbers which are divisible by 7 but are not
# a multiple of 5, between 2000 and 3200 (both included). The numbers obtained
# should be printed in a comma-separated sequence on a single line.

# Find numbers divisible by 7 but not multiple of 5
numbers = []

for i in range(2000, 3201):  # 3200 included
    if (i % 7 == 0) and (i % 5 != 0):
        numbers.append(str(i))

# Join numbers with comma
result = ",".join(numbers)
print(result)

# Example output:
# 2002,2009,2016,2023,2030,2037,2044,2051,2058,2065,2072,2079,2086,2093,2100,