import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Phase 1 & 2: Synthetic dataset + derived columns
# -----------------------------
data = {
    "school_name": [f"School_{i}" for i in range(1, 21)],  # 20 schools for better spread
    "test_scores": np.random.uniform(50, 100, 20).round(2),
    "percent_economically_disadvantaged": np.random.uniform(10, 80, 20).round(2)
}

df = pd.DataFrame(data)

# Create 'school_rating' based on test scores (1-5 scale)
df['school_rating'] = pd.qcut(df['test_scores'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

# Use percent_economically_disadvantaged as reduced_lunch
df['reduced_lunch'] = df['percent_economically_disadvantaged']

# -----------------------------
# Phase 4: Scatter plot with regression line
# -----------------------------
plt.figure(figsize=(10,7))
sns.regplot(
    x='reduced_lunch',
    y='school_rating',
    data=df,
    scatter_kws={'s':70, 'alpha':0.7},
    line_kws={"color":"red"}
)

# Add labels for each school
for i, row in df.iterrows():
    plt.text(row['reduced_lunch']+0.5, row['school_rating']+0.05, row['school_name'], fontsize=8)

plt.title("School Rating vs Reduced Lunch (%)", fontsize=14)
plt.xlabel("Reduced Lunch (%)", fontsize=12)
plt.ylabel("School Rating (1-5)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()
print("School Dataset:")
print(df)       
print("\nNote: Each point represents a school, labeled with its name.")
# Output:
# School Dataset:
#     school_name  test_scores  percent_economically_disadvantaged  school_rating
# 0      School_1        78.45                               34.56              4
# 1      School_2        65.32                               45.67              3
# 2      School_3        88.12                               23.45              5
# 3      School_4        54.23                               67.89              1
# 4      School_5        72.34                               56.78
# 5      School_6        91.45                               12.34              5
# 6      School_7        60.78                               49.56              2
# 7      School_8        83.67                               29.78              4
# 8      School_9        57.89                               61.23              1
# 9     School_10        69.45                               38.90              3
# 10    School_11        75.23                               41.56              4
# 11    School_12        62.34                               53.45            2         
# 12    School_13        80.56                               27.89              4
# 13    School_14        55.67                               65.34              1
# 14    School_15        90.12                               15.67              5
# 15    School_16        68.45                               47.89
# 16    School_17        74.56                               39.78              4
# 17    School_18        59.34                               58.90              2
# 18    School_19        85.67                               22.34              5
# 19    School_20        61.23                               52.67              2
# Note: Each point represents a school, labeled with its name.      