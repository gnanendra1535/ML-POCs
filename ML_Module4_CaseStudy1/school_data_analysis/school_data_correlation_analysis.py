import pandas as pd
import numpy as np

# -----------------------------
# Phase 1: Create synthetic dataset
# -----------------------------
data = {
    "school_name": [f"School_{i}" for i in range(1, 11)],
    "test_scores": np.random.uniform(50, 100, 10).round(2),
    "percent_economically_disadvantaged": np.random.uniform(10, 80, 10).round(2)
}

df = pd.DataFrame(data)

# -----------------------------
# Phase 2: Create 'school_rating' and 'reduced_lunch'
# -----------------------------
# Create school rating (scale 1–5) from test_scores
df['school_rating'] = pd.qcut(df['test_scores'], 5, labels=[1, 2, 3, 4, 5])

# Use percent_economically_disadvantaged as reduced_lunch
df['reduced_lunch'] = df['percent_economically_disadvantaged']

# Convert school_rating to integer for correlation
df['school_rating'] = df['school_rating'].astype(int)

# -----------------------------
# Phase 3: Correlation analysis
# -----------------------------
corr_matrix = df[['reduced_lunch', 'school_rating']].corr()

print("School Dataset:")
print(df)

print("\nCorrelation Matrix (reduced_lunch vs school_rating):")
print(corr_matrix)
