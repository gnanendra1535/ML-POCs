# By using list comprehension, please write a program to print the list after removing
# deleted numbers that are divisible by 5 and 7 in [12,24,35,70,88,120,155].

# comprehensive_rmv57.py
# Given list
numbers = [12, 24, 35, 70, 88, 120, 155]

# Remove numbers divisible by both 5 and 7
result = [num for num in numbers if not (num % 5 == 0 and num % 7 == 0)]

print(result)

# Output the modified list
# [12, 24, 35, 88, 120, 155]