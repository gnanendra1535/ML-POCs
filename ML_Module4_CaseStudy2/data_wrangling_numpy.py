# case study 2 - data wrangling with numpy

import pandas as pd
# Read the three CSV files

math_df = pd.read_csv("MathScoreTerm1.csv")
physics_df = pd.read_csv("PhysicsScoreTerm1.csv")
ds_df = pd.read_csv("DSScoreTerm1.csv")


# Handle missing scores with class average

for df in [math_df, physics_df, ds_df]:
    score_cols = [col for col in df.columns if "Score" in col]
    for col in score_cols:
        df[col].fillna(df[col].mean(), inplace=True)


# Convert Ethnicity → numeric codes (anonymized)

for df in [math_df, physics_df, ds_df]:
    if "Ethnicity" in df.columns:
        df["Ethnicity"] = df["Ethnicity"].astype("category").cat.codes


# Remove Name column (PII)

for df in [math_df, physics_df, ds_df]:
    if "Name" in df.columns:
        df.drop(columns=["Name"], inplace=True)


# Merge datasets on StudentID, Sex, Age, Ethnicity

merged_df = math_df.merge(physics_df, on=["StudentID", "Sex", "Age", "Ethnicity"], how="outer")
merged_df = merged_df.merge(ds_df, on=["StudentID", "Sex", "Age", "Ethnicity"], how="outer")


# Convert Sex (M/F → 1/2)

merged_df["Sex"] = merged_df["Sex"].map({"M": 1, "F": 2})


# Save final cleaned dataset

merged_df.to_csv("ScoreFinal_Enhanced.csv", index=False)

print(" Final enhanced dataset saved as 'ScoreFinal_Enhanced.csv'")
print("\nSample Data:")
print(merged_df.head())


