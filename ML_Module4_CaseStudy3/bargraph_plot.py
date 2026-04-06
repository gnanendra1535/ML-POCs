# 1. You are given a dataset, which is present in the LMS, containing the number of
# hurricanes occurring in the United States along the coast of the Atlantic. Load the
# data from the dataset into your program and plot a Bar Graph of the data, taking
# the Year as the x-axis and the number of hurricanes occurring as the Y-axis. 

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "Hurricanes.csv"
hurricanes_df = pd.read_csv(file_path)


top5 = hurricanes_df.sort_values(by="Hurricanes", ascending=False).head(5)

# Plot bar graph
plt.figure(figsize=(12,6))
plt.bar(hurricanes_df['Year'], hurricanes_df['Hurricanes'], color='skyblue', edgecolor='black')

# Highlight top 5 years in red
plt.bar(top5['Year'], top5['Hurricanes'], color='red', edgecolor='black')

# Annotate top 5 values
for i, row in top5.iterrows():
    plt.text(row['Year'], row['Hurricanes']+0.3, str(row['Hurricanes']),
             ha='center', va='bottom', fontsize=9, fontweight='bold')

# Labels and title
plt.title("Number of Hurricanes in the US (Atlantic Coast)", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Hurricanes", fontsize=12)
plt.grid(axis='y', linestyle="--", alpha=0.7)
plt.show()
