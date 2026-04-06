# 2. The dataset given, records data of city temperatures over the years 2014 and
# 2015. Plot the histogram of the temperatures over this period for the cities of
# San Francisco and Moscow.


import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
file_path = "CityTemps.csv"  
temps_df = pd.read_csv(file_path)

# Plot histogram of temperatures for San Francisco and Moscow
plt.figure(figsize=(12,6))

plt.hist(temps_df['San Francisco'], bins=15, alpha=0.6, 
         label='San Francisco', color='skyblue', edgecolor='black')

plt.hist(temps_df['Moscow'], bins=15, alpha=0.6, 
         label='Moscow', color='salmon', edgecolor='black')

plt.title("Temperature Distribution (2014-2015)", fontsize=14)
plt.xlabel("Temperature (°C)", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle="--", alpha=0.7)
plt.show()
