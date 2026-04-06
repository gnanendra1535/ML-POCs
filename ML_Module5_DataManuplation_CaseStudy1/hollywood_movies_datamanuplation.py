# Hollywood Movies Data Manipulation and Visualization

import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
file_path = "HollywoodMovies.csv"
movies_df = pd.read_csv(file_path)

# 1. Highest-rated movie in the "Quest" story type
quest_movies = movies_df[movies_df['Story'] == 'Quest']
highest_rated_quest = quest_movies.loc[quest_movies['RottenTomatoes'].idxmax(), 'Movie']
print("1. Highest-rated 'Quest' story type movie:", highest_rated_quest)

# 2. Genre with the greatest number of movie releases
most_common_genre = movies_df['Genre'].value_counts().idxmax()
print("2. Genre with greatest number of releases:", most_common_genre)

# 3. Top 5 movies with the costliest budgets
top5_budget_movies = movies_df.nlargest(5, 'Budget')[['Movie', 'Budget']]
print("3. Top 5 movies with costliest budgets:")
print(top5_budget_movies)

# 4. Plot profitability vs RottenTomatoes rating
plt.figure(figsize=(10,6))
plt.scatter(movies_df['RottenTomatoes'], movies_df['Profitability'], alpha=0.6, color='blue')
plt.title("Profitability vs Rotten Tomatoes Rating", fontsize=14)
plt.xlabel("Rotten Tomatoes Rating (%)", fontsize=12)
plt.ylabel("Profitability (WorldGross / Budget)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.show()

# Correlation coefficient
correlation = movies_df['RottenTomatoes'].corr(movies_df['Profitability'])
print("5. Correlation between RottenTomatoes rating and Profitability:", correlation)


# Highest-rated "Quest" story type movie:  The Hurt Locker
# Genre with greatest number of releases:  Comedy
# Top 5 movies with costliest budgets:
# Pirates of the Caribbean: At World's End → 300M
# Tangled → 260M
# Spider-Man 3 → 258M
# Harry Potter and the Half-Blood Prince → 250M
# Pirates of the Caribbean: On Stranger Tides → 250M
# Profitability vs Rotten Tomatoes Rating (scatter plot):
# The scatter shows that higher critic ratings don’t always guarantee higher profitability.
# Some highly-rated movies performed modestly, while some mid-rated blockbusters achieved massive profits.
