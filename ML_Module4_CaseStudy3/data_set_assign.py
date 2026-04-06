# 3. Create CSV file from the data file available in LMS which goes by the name
# ‘M4_assign_dataset’ and read this file into a pandas data frame

import pandas as pd


file_path = "M4_assign_dataset.csv"


df = pd.read_csv(file_path)


print("Dataset Loaded Successfully!\n")
print(df.head())
