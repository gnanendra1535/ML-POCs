import pandas as pd;
df = pd.read_csv("SalaryGender.csv")

# Extract each column into separate NumPy arrays
gender = df["Gender"].to_numpy()
salary = df["Salary"].to_numpy()
age = df["Age"].to_numpy()
phd = df["PhD"].to_numpy()

# Print results
print("Gender:", gender)
print("Salary:", salary)
print("Age:", age)
print("PhD:", phd)