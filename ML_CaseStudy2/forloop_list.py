#Write a for loop that prints all elements of a list and their position in the list.
# a = [4,7,3,2,5,9]
#Hint: Use Loop to iterate through list elements.

a = [4, 7, 3, 2, 5, 9]

for index in range(len(a)):
    print(f"Position {index}: {a[index]}")

#output:    
# Position 0: 4
# Position 1: 7
# Position 2: 3
# Position 3: 2
# Position 4: 5
# Position 5: 9

#alternative way using enumerate
for index, value in enumerate(a):
    print(f"Position {index}: {value}") 
#output:
# Position 0: 4
# Position 1: 7
# Position 2: 3
# Position 3: 2
# Position 4: 5
# Position 5: 9