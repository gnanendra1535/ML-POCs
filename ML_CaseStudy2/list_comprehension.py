# .By using list comprehension, please write a program to print the list after removing
# the 0th,4th, and 5th numbers in [12,24,35,70,88,120,155].

# comprehensive_list.py

# Given list
numbers = [12, 24, 35, 70, 88, 120, 155]

# Remove elements at indexes 0, 4, and 5
result = [num for i, num in enumerate(numbers) if i not in (0, 4, 5)]

print(result)

# Output the modified list
# [24, 35, 70, 155]