import numpy as np

# Load CSV (skip header if present)
data = np.genfromtxt("SalaryGender.csv", delimiter=",", skip_header=1)

# Extract columns into arrays
gender = data[:, 0]   # 1st column
salary = data[:, 1]   # 2nd column
age = data[:, 2]      # 3rd column
phd = data[:, 3]      # 4th column

print("Gender:", gender)
print("Salary:", salary)
print("Age:", age)
print("PhD:", phd)