# File Operations and DataFrame Manipulations using Pandas
import pandas as pd
import numpy as np
# 6.1 Create Series and apply string methods
s1 = pd.Series(['Amit', 'Bob', 'Kate', 'A', 'b', np.nan, 'Car', 'dog', 'cat'])
print("6.1 a) Lower case:\n", s1.str.lower())
print("6.1 b) Upper case:\n", s1.str.upper())
print("6.1 c) Length of elements:\n", s1.str.len())

# 6.2 Strip spaces

s2 = pd.Series([' Atul', 'John ', ' jack ', 'Sam'])
print("\n6.2 a) Strip both sides:\n", s2.str.strip())
print("6.2 b) Strip left only:\n", s2.str.lstrip())
print("6.2 c) Strip right only:\n", s2.str.rstrip())

# 6.3 Split by '_'

s3 = pd.Series(['India_is_big', 'Population_is_huge', np.nan, 'Has_diverse_culture'])
print("\n6.3 a) Split by '_':\n", s3.str.split('_'))
print("6.3 b) Access element 0 of split list:\n", s3.str.split('_').str[0])
print("6.3 c) Expand split into columns:\n", s3.str.split('_', expand=True))

# 6.4 Replace X or dog with XX-XX

s4 = pd.Series(['A', 'B', 'C', 'AabX', 'BacX','', np.nan, 'CABA', 'dog', 'cat'])
print("\n6.4 Replace X or dog:\n", s4.str.replace('X|dog', 'XX-XX', regex=True))

# 6.5 Remove dollars

s5 = pd.Series(['12', '-$10', '$10,000'])
print("\n6.5 Remove dollars:\n", s5.str.replace(r'[\$,]', '', regex=True).astype(float))

# 6.6 Reverse all lower case words

s6 = pd.Series(['India 1998', 'big country', np.nan])
print("\n6.6 Reverse lower case words:\n", s6.str.replace(r'\b[a-z]+\b', 
      lambda x: x.group()[::-1], regex=True))

# 6.7 Check alphanumeric

s7 = pd.Series(['1', '2', '1a', '2b', '2003c'])
print("\n6.7 Alphanumeric check:\n", s7.str.isalnum())

# 6.8 Check containing 'A'

s8 = pd.Series(['1', '2', '1a', '2b', 'America', 'VietnAm','vietnam', '2003c'])
print("\n6.8 Contains 'A':\n", s8.str.contains('A', case=False, na=False))

# 6.9 Split values into a/b/c indicator columns

s9 = pd.Series(['a', 'a|b', np.nan, 'a|c'])
df9 = pd.DataFrame({
    'a': s9.str.contains('a', na=False).astype(int),
    'b': s9.str.contains('b', na=False).astype(int),
    'c': s9.str.contains('c', na=False).astype(int)
})
print("\n6.9 Indicator columns:\n", df9)

# 6.10 Merge tables

left = pd.DataFrame({'key': ['One', 'Two'], 'ltable': [1, 2]})
right = pd.DataFrame({'key': ['One', 'Two'], 'rtable': [4, 5]})
merged = pd.merge(left, right, on='key')
print("\n6.10 Merged DataFrame:\n", merged)
