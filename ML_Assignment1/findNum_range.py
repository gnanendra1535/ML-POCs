result = []
for num in range(1000, 3001):
    num_str = str(num)  # Convert number to string to check each digit
    if all(int(digit) % 2 == 0 for digit in num_str):  # Check if all digits are even
        result.append(str(num))
        print(",".join(result))