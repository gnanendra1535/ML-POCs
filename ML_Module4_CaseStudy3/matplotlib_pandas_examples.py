# 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data for plotting
X = [1, 2, 3, 4]
y = [20, 21, 20.5, 20.8]
y_error = [0.12, 0.13, 0.2, 0.1]

# 5.1 Simple Plot

plt.figure()
plt.plot(X, y)
plt.show()


# 5.2 Configure line and markers

plt.figure()
plt.plot(X, y, color='blue', marker='o', linestyle='--', linewidth=2, markersize=8)
plt.show()


# 5.3 Configure axes

plt.figure()
plt.plot(X, y, color='green', marker='s')
plt.axis([0, 5, 19, 22])  # [xmin, xmax, ymin, ymax]
plt.show()


# 5.4 Title and axis labels

plt.figure()
plt.plot(X, y, marker='o')
plt.title("Simple Line Plot", fontsize=14)
plt.xlabel("X-axis Values", fontsize=14)
plt.ylabel("Y-axis Values", fontsize=14)
plt.show()

# 5.5 Error bars
plt.figure()
plt.errorbar(X, y, yerr=y_error, fmt='o-', color='red', ecolor='black', capsize=5)
plt.title("Line Plot with Error Bars", fontsize=14)
plt.show()


# 5.6 Define figsize and DPI

plt.figure(figsize=(4, 5), dpi=100)
plt.plot(X, y, marker='o', color='purple')
plt.title("Custom Size & DPI Plot", fontsize=14)
plt.show()

# 5.7 Font size = 14 already applied above

# 5.8 Scatter graph of 50 random values

x_rand = np.random.rand(50)
y_rand = np.random.rand(50)

plt.figure()
plt.scatter(x_rand, y_rand, color='orange')
plt.title("Scatter Plot of 50 Random Points", fontsize=14)
plt.show()


# 5.9 Scatterplot from DataFrame with point size = age

data = {
    'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
    'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze'],
    'female': [0, 1, 1, 0, 1],
    'age': [42, 52, 36, 24, 73],
    'preTestScore': [4, 24, 31, 2, 3],
    'postTestScore': [25, 94, 57, 62, 70]
}
df = pd.DataFrame(data)

plt.figure()
plt.scatter(df['preTestScore'], df['postTestScore'], s=df['age']*10, alpha=0.6)
plt.title("Scatter: Pre vs Post Test (Size by Age)", fontsize=14)
plt.xlabel("Pre Test Score", fontsize=14)
plt.ylabel("Post Test Score", fontsize=14)
plt.show()


# 5.10 Scatterplot with size=300 and color=sex

plt.figure()
plt.scatter(df['preTestScore'], df['postTestScore'], s=300, 
            c=df['female'], cmap='bwr', alpha=0.6, edgecolor='k')
plt.title("Scatter: Pre vs Post Test (Color by Sex)", fontsize=14)
plt.xlabel("Pre Test Score", fontsize=14)
plt.ylabel("Post Test Score", fontsize=14)
plt.show()
