num = int(input("Enter a number: "))
print(f"Factors of {num}:")

for i in range(1, num + 1):
    if num % i == 0:
        if i % 2 == 0:
            print(f"{i} is an even factor")
        else:
            print(f"{i} is an odd factor")