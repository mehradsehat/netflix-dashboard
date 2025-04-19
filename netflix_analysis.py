import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# === Load and Prepare Data === #
df = pd.read_csv("netflix_titles.csv")

# Basic info
print("Dataset shape:", df.shape)
print("Column names:", df.columns.tolist())

# Missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Content type distribution
print("\nContent type distribution:")
print(df['type'].value_counts())

# Strip whitespace and convert to datetime
df['date_added'] = df['date_added'].str.strip()
df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y', errors='coerce')
df['added_year'] = df['date_added'].dt.year
df['added_month'] = df['date_added'].dt.month

# Fill missing values
df['director'] = df['director'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')

# Drop rows with missing duration or rating
df.dropna(subset=['duration', 'rating'], inplace=True)

# Duration split
df['duration_minutes'] = df['duration'].apply(lambda x: int(x.split()[0]) if 'min' in x else None)
df['duration_seasons'] = df['duration'].apply(lambda x: int(x.split()[0]) if 'Season' in x else None)

# Preview cleaned data
print("\nCleaned data preview:")
print(df.head())

# === Plots === #

# 1. Number of Titles Added per Year
content_per_year = df['added_year'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
plt.plot(content_per_year.index, content_per_year.values, marker='o')
plt.title('Number of Netflix Titles Added per Year')
plt.xlabel('Year')
plt.ylabel('Number of Titles')
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Movies vs TV Shows Distribution
type_counts = df['type'].value_counts()
plt.figure(figsize=(6, 4))
type_counts.plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Distribution of Content Type')
plt.xlabel('Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 3. Top 10 Countries
top_countries = df['country'].value_counts().head(10)
plt.figure(figsize=(10, 6))
top_countries.plot(kind='bar')
plt.title('Top 10 Countries with Most Netflix Content')
plt.xlabel('Country')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Top 10 Genres
genres = df['listed_in'].dropna().apply(lambda x: [g.strip() for g in x.split(',')])
flat_genres = [genre for sublist in genres for genre in sublist]
genre_counts = Counter(flat_genres).most_common(10)
genre_df = pd.DataFrame(genre_counts, columns=['Genre', 'Count'])

plt.figure(figsize=(10, 6))
plt.bar(genre_df['Genre'], genre_df['Count'], color='purple')
plt.title('Top 10 Most Common Genres on Netflix')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Top 10 Content Ratings
rating_counts = df['rating'].value_counts().head(10)
plt.figure(figsize=(8, 5))
rating_counts.plot(kind='bar', color='teal')
plt.title('Top 10 Content Ratings on Netflix')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6. Movie Duration Distribution
movie_durations = df[df['type'] == 'Movie']['duration_minutes'].dropna()
plt.figure(figsize=(10, 5))
plt.hist(movie_durations, bins=30, color='orange', edgecolor='black')
plt.title('Distribution of Movie Durations')
plt.xlabel('Duration (minutes)')
plt.ylabel('Number of Movies')
plt.tight_layout()
plt.show()

# 7. Top 10 Directors (excluding 'Unknown')
top_directors = df['director'].value_counts().drop('Unknown').head(10)
plt.figure(figsize=(10, 5))
top_directors.plot(kind='barh', color='green')
plt.title('Top 10 Most Frequent Netflix Directors')
plt.xlabel('Number of Titles')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 8. Content Added by Month
monthly_additions = df['added_month'].value_counts().sort_index()
plt.figure(figsize=(10, 5))
plt.plot(monthly_additions.index, monthly_additions.values, marker='o')
plt.title('Content Added by Month')
plt.xlabel('Month')
plt.ylabel('Number of Titles')
plt.xticks(range(1, 13))
plt.grid(True)
plt.tight_layout()
plt.show()

# 9. Movie vs TV Show by Country (Top 10)
country_type = df.groupby(['country', 'type']).size().unstack().fillna(0)
top_countries = df['country'].value_counts().head(10).index
country_type_top10 = country_type.loc[top_countries]

country_type_top10.plot(kind='bar', figsize=(12, 6))
plt.title('Movie vs TV Show by Country (Top 10)')
plt.xlabel('Country')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
