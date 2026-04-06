# Use SalaryGender CSV file. Store the “Age” and “Ph.D.” columns in one DataFrame
# and delete the data of all people who don’t have a PhD

import pandas as pd

# Load the CSV file
df = pd.read_csv("SalaryGender.csv")

# Select only Age and PhD columns
df_new = df[["Age", "PhD"]]

# Keep only people with PhD (PhD = 1)
df_phd = df_new[df_new["PhD"] == 1]

print("DataFrame with only Age & PhD (PhD holders only):")
print(df_phd)

