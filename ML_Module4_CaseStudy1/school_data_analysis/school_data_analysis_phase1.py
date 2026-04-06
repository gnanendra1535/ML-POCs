# 
import pandas as pd

# Replace with your actual file name
df = pd.read_csv("middle_tennessee_schools.csv")

# Preview first 5 rows
print("First 5 rows of data:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values per Column:")
print(df.isnull().sum())

print("\nSummary Statistics:")
print(df.describe(include="all"))

print("\nColumn Names:")
print(df.columns.tolist())

