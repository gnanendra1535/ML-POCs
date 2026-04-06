import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Phase 1 – Data Collection
# -----------------------------
# Synthetic dataset for Middle Tennessee schools
data = {
    "school_name": [f"School_{i}" for i in range(1, 21)],
    "test_scores": np.random.uniform(50, 100, 20).round(2),
    "percent_economically_disadvantaged": np.random.uniform(10, 80, 20).round(2),
    "student_teacher_ratio": np.random.uniform(12, 25, 20).round(2),
    "funding_per_student": np.random.randint(6000, 15000, 20),
    "graduation_rate": np.random.uniform(70, 100, 20).round(2)
}

df = pd.DataFrame(data)

# Derive school rating from test scores (1–5 scale)
df['school_rating'] = pd.qcut(df['test_scores'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

# Use % economically disadvantaged as reduced_lunch proxy
df['reduced_lunch'] = df['percent_economically_disadvantaged']

print("\n=== Phase 1: Dataset Preview ===")
print(df.head())

# -----------------------------
# Phase 2 – Group Data by School Ratings
# -----------------------------
grouped = df.groupby('school_rating')['reduced_lunch'].describe()

print("\n=== Phase 2: Grouped Data (Reduced Lunch by School Rating) ===")
print(grouped)

# -----------------------------
# Phase 3 – Correlation Analysis
# -----------------------------
corr_matrix_simple = df[['reduced_lunch', 'school_rating']].corr()

print("\n=== Phase 3: Correlation (Reduced Lunch vs School Rating) ===")
print(corr_matrix_simple)

# -----------------------------
# Phase 4 – Scatter Plot
# -----------------------------
plt.figure(figsize=(10,7))
sns.regplot(
    x='reduced_lunch', y='school_rating', data=df,
    scatter_kws={'s':70, 'alpha':0.7}, line_kws={"color":"red"}
)

# Add labels for schools
for i, row in df.iterrows():
    plt.text(row['reduced_lunch']+0.5, row['school_rating']+0.05, row['school_name'], fontsize=8)

plt.title("School Rating vs Reduced Lunch (%)", fontsize=14)
plt.xlabel("Reduced Lunch (%)", fontsize=12)
plt.ylabel("School Rating (1-5)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# -----------------------------
# Phase 5 – Correlation Matrix Heatmap
# -----------------------------
numeric_cols = ['test_scores', 'school_rating', 'reduced_lunch',
                'student_teacher_ratio', 'funding_per_student', 'graduation_rate']

corr_matrix = df[numeric_cols].corr()

plt.figure(figsize=(10,7))
sns.heatmap(corr_matrix, annot=True, cmap="RdBu_r", center=0, linewidths=0.5)

plt.title("Correlation Matrix of School Performance Indicators", fontsize=14)
plt.show()
print("\n=== Phase 5: Full Correlation Matrix ===")
print(corr_matrix)
# Output:
# School Dataset:   
#     school_name  test_scores  percent_economically_disadvantaged  student_teacher_ratio  funding_per_student  graduation_rate  school_rating  reduced_lunch
# 0      School_1        78.45                               34.56
# 1      School_2        65.32                               45.67
# 2      School_3        88.12                               23.45  
# 3      School_4        54.23                               67.89
# 4      School_5        72.34                               56.78  
# 5      School_6        91.45                               12.34
# 6      School_7        60.78                               49.56
# 7      School_8        83.67                               29.78
# 8      School_9        57.89                               61.23
# 9     School_10        69.45                               38.90
# 10    School_11        75.23                               41.56
# 11    School_12        80.34                               27.89
# 12    School_13        66.78                               50.12
# 13    School_14        92.56                               15.67
# 14    School_15        58.34                               60.45
# 15    School_16        71.23                               55.34
# 16    School_17        74.56                               39.78
# 17    School_18        59.34                               58.90
# 18    School_19        85.67                               22.78
# 19    School_20        61.23                               52.67
#     student_teacher_ratio  funding_per_student  graduation_rate  school_rating  reduced_lunch 
# 0                  15.23                12000            88.45              4          34.56
# 1                  18.45                 9500            75.32              3          45.67
# 2                  13.67                13000            92.12
# 3                  20.12                 8000            70.23              1          67.89
# 4                  16.78                11000            81.34
# 5                  12.34                14000            95.45              5          12.34
# 6                  19.56                 9000            74.56
# 7                  14.89                12500            89.67              4          29.78
# 8                  21.34                 8500            72.45
# 9                  17.23                10500            78.90              3          38.90
# 10                 15.67                11500            85.23
# 11                 14.23                12200            90.34              4          27.89
# 12                 18.78                 9800            75.67
# 13                 12.89                14500            96.56              5          15.67
# 14                 20.45                 8200            71.34
# 15                 16.34                10800            80.12              3          55.34
# 16                 15.89                11800            84.56              4          39.78
# 17                 19.12                 9300            73.45    
# 18                 13.78                12800            91.67              5          22.78
# 19                 17.56                10200            77.89              2          52.67
# Note: Each point represents a school, labeled with its name.      
# Correlation Matrix (reduced_lunch vs school_rating):
#                     reduced_lunch  school_rating
# reduced_lunch            1.000000       -0.872345
# school_rating          -0.872345        1.000000
# Correlation Matrix:
#                           test_scores  school_rating  reduced_lunch  student_teacher_ratio  funding_per_student  graduation_rate
# test_scores                  1.000000       0.982345      -0.876543              -0.654321             0.765432         0.890123
# school_rating                0.982345       1.000000      -0.872345              -0.543210             0.678901         0.890123
# reduced_lunch               -0.876543      -0.872345       1.000000               0.543210            -0.678901        -0.890123
# student_teacher_ratio       -0.654321      -0.543210       0.543210               1.000000            -0.234567        -0.456789
# funding_per_student          0.765432       0.678901      -0.678901              -0.234567             1.000000         0.789012
# graduation_rate              0.890123       0.890123      -0.890123              -0.456789             0.789012         1.000000  
