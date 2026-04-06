# Calculate the total number of people who have a Ph.D. degree from the
# SalaryGender CSV file.

import pandas as pd

# Load CSV
df = pd.read_csv("SalaryGender.csv")

# Count number of people with PhD
total_phd = df[df["PhD"] == 1].shape[0]

print("Total number of people with PhD:", total_phd)

# using only numpy

import numpy as np

# Load data (skip header row)
data = np.genfromtxt("SalaryGender.csv", delimiter=",", skip_header=1)

# Extract PhD column (4th column, index 3)
phd = data[:, 3]

# Count people with PhD
total_phd = np.sum(phd == 1)

print("Total number of people with PhD:", int(total_phd))
