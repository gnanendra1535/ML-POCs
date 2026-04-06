#
import pandas as pd
import numpy as np


# 5.1 Create DataFrame

data = {
    'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
    'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
    'age': [42, 52, 36, 24, 73],
    'preTestScore': [4, 24, 31, ".", "."],
    'postTestScore': ["25,000", "94,000", 57, 62, 70]
}

df = pd.DataFrame(data)
print("DataFrame created:\n", df, "\n")


# 5.2 Save to CSV

df.to_csv("example.csv", index=False)
print(" DataFrame saved as 'example.csv'\n")


# 5.3 Read example.csv

df_csv = pd.read_csv("example.csv")
print("DataFrame read from CSV:\n", df_csv, "\n")


# 5.4 Read CSV without column heading

df_no_header = pd.read_csv("example.csv", header=None)
print("Read CSV without header:\n", df_no_header, "\n")


# 5.5 Read CSV with index columns 'first_name' and 'last_name'

df_indexed = pd.read_csv("example.csv", index_col=['first_name', 'last_name'])
print("DataFrame with first_name & last_name as index:\n", df_indexed, "\n")


# 5.6 Print Boolean DataFrame for Null values

df_nulls = df_csv.isnull()
print(" Boolean DataFrame (True=NaN, False=Not NaN):\n", df_nulls, "\n")


# 5.7 Read CSV skipping first 3 rows

df_skip = pd.read_csv("example.csv", skiprows=3)
print("DataFrame skipping first 3 rows:\n", df_skip, "\n")


# 5.8 Load CSV interpreting ',' in numbers as thousands separator

df_thousands = pd.read_csv("example.csv", thousands=',')
print(" DataFrame with ',' treated as thousands separator:\n", df_thousands, "\n")
