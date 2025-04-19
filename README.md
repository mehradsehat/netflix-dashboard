# Netflix Dashboard

An interactive and visually engaging dashboard built with Dash, Plotly, and Bootstrap to explore and analyze the Netflix Titles Dataset.

## Features

- **Filterable Data**
  - Filter content by type (Movie or TV Show)
  - Filter by the year added to Netflix

- **Interactive Visualizations**
  - Bar chart: Top 10 countries with the most titles
  - Histogram: Rating distribution in a selected year
  - Bar chart: Most common genres
  - Donut chart: Distribution of content types

- **Summary Cards**
  - Total number of movies and TV shows
  - Most popular genre
  - Average movie duration

- **Modern UI Design**
  - Dark gradient background
  - Smooth animations and transitions
  - Fully responsive and mobile-friendly

## Dataset

This project uses the [Netflix Titles Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) from Kaggle.  
Make sure the `netflix_titles.csv` file is located in the root directory of the project.

## Technologies Used

- Dash  
- Plotly Express  
- Dash Bootstrap Components  
- Pandas  
- Font Awesome  
- Custom CSS (see `assets/style.css`)

## Installation

## 1. Clone the repository
git clone https://github.com/mehradsehat/netflix-dashboard.git
cd netflix-dashboard

## 2. (Optional) Create and activate a virtual environment
## Windows
python -m venv venv
venv\Scripts\activate

## macOS/Linux
python3 -m venv venv
source venv/bin/activate

## 3. Install the required dependencies
pip install -r requirements.txt

## 4. Make sure the dataset is present in the root directory
File needed: netflix_titles.csv

## 5. Run the app
python netflix_dashboard.py

## 6. Open in browser
Visit http://127.0.0.1:8050 in your browser


![Netflix Dashboard Screenshot](https://raw.githubusercontent.com/mehradsehat/netflix-dashboard/cc5da3b777062ecd3a7df8d090df2d4a238dc2f0/images/dashboard_screenshot.png.png)

