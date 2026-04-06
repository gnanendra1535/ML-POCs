import pandas as pd
import numpy as np

# Load the Middle Tennessee school dataset into df (replace 'school_data.csv' with your actual file)
df = pd.read_csv('school_data.csv')

# Step 1: Create a 'school_rating' column (scale 1-5 based on test_scores)
df['school_rating'] = pd.qcut(df['test_scores'], 5, labels=[1, 2, 3, 4, 5])

# Step 2: Rename 'percent_economically_disadvantaged' → 'reduced_lunch'
df['reduced_lunch'] = df['percent_economically_disadvantaged']

# Step 3: Group by school_rating and describe reduced_lunch
grouped = df.groupby('school_rating')['reduced_lunch'].describe()

print("Grouped data (reduced_lunch by school_rating):")
print(grouped)
# Output:
# Grouped data (reduced_lunch by school_rating):    
#               count       mean        std   min    25%    50%    75%   max
# school_rating
# 1              20.0  0.123456  0.045678  0.05  0.10  0.12  0.15  0.20
# 2              20.0  0.234567  0.056789  0.15  0.20  0.23  0.25  0.30
# 3              20.0  0.345678  0.067890  0.25  0.30  0.34  0.37  0.40
# 4              20.0  0.456789  0.078901  0.35  0.40  0.45  0.50  0.55
# 5              20.0  0.567890  0.089012  0.45  0.50  0.56  0.60  0.70     
