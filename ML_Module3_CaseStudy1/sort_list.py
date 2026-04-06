# Data of XYZ company is stored in the sorted list. Write a program for searching
# specific data from that list.
# Hint: Use if/elif to deal with conditions.

# Sorted list of company data (Example: Employee IDs)
data = [101, 105, 110, 120, 125, 130, 140]

search_value = int(input("Enter the data to search: "))

low = 0
high = len(data) - 1
found = False

while low <= high:
    mid = (low + high) // 2
    if data[mid] == search_value:
        print(f"Data found at position {mid} (index starts from 0).")
        found = True
        break
    elif data[mid] < search_value:
        low = mid + 1
    else:
        high = mid - 1

if not found:
    print("Data not found in the list.")

# Example input:
# Enter the data to search: 120
# Data found at position 3 (index starts from 0).
# Example input:
# Enter the data to search: 150
# Data not found in the list.   
