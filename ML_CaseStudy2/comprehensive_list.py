# By using list comprehension, please write a program to print the list after removing
# the value 24 in [12,24,35,24,88,120,155].

# comprehensive_list.py

# Given list
numbers = [12, 24, 35, 24, 88, 120, 155]

# Remove value 24 using list comprehension
result = [x for x in numbers if x != 24]

print(result)

# Output the modified list

# [12, 35, 88, 120, 155]

