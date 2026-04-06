# Find: 1. The number of men with a PhD 2. The number of women with a PhD

import pandas as pd

# Load CSV
df = pd.read_csv("SalaryGender.csv")

# Count men with PhD
men_with_phd = df[(df["Gender"] == 1) & (df["PhD"] == 1)].shape[0]

# Count women with PhD
women_with_phd = df[(df["Gender"] == 0) & (df["PhD"] == 1)].shape[0]

print("Number of men with PhD:", men_with_phd)
print("Number of women with PhD:", women_with_phd)
