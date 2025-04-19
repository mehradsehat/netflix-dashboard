import pandas as pd
from collections import Counter
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# ---------------------- Theme & Font ----------------------
THEME = dbc.themes.BOOTSTRAP
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.15.4/css/all.css"

# ---------------------- Dash App Setup ----------------------
app = dash.Dash(__name__, external_stylesheets=[THEME, FONT_AWESOME], suppress_callback_exceptions=True)
app.title = "Netflix Dashboard"
server = app.server

# ---------------------- Load & Clean Data ----------------------
df = pd.read_csv("netflix_titles.csv")
df['date_added'] = df['date_added'].str.strip()
df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y', errors='coerce')
df['added_year'] = df['date_added'].dt.year.astype('Int64')
df['country'] = df['country'].fillna('Unknown')
df = df.dropna(subset=['duration', 'rating'])
df['genres'] = df['listed_in'].apply(lambda x: [i.strip() for i in x.split(',')] if pd.notna(x) else [])

# ---------------------- Summary Stats ----------------------
num_movies = df[df['type'] == 'Movie'].shape[0]
num_shows = df[df['type'] == 'TV Show'].shape[0]
top_genre = Counter([genre for genres in df['genres'] for genre in genres]).most_common(1)[0][0]
avg_duration = int(df[df['type'] == 'Movie']['duration'].str.extract(r'(\d+)')[0].dropna().astype(int).mean())

# ---------------------- Donut Chart (Type Distribution) ----------------------
type_dist = df['type'].value_counts().reset_index()
type_dist.columns = ['Type', 'Count']
fig_donut = px.pie(type_dist, names='Type', values='Count', hole=0.5, title='Movies vs TV Shows')
fig_donut.update_layout(
    plot_bgcolor="#121212",
    paper_bgcolor="#121212",
    font=dict(color="white"),
    annotations=[dict(text='Type', x=0.5, y=0.5, font_size=20, showarrow=False)],
    colorway=["#7d3cff", "#f2d53c"]
)

# ---------------------- App Layout ----------------------
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Netflix Dashboard", style={
            "textAlign": "center",
            "fontWeight": "bold",
            "fontSize": "32px",
            "color": "white"
        }), md=12)
    ], className="my-3"),

    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H4("Movies", style={"fontWeight": "bold", "fontSize": "18px"}),
            html.H2(f"{num_movies}", style={"fontSize": "28px", "fontWeight": "600"})
        ]), color="dark", inverse=True), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H4("TV Shows", style={"fontWeight": "bold", "fontSize": "18px"}),
            html.H2(f"{num_shows}", style={"fontSize": "28px", "fontWeight": "600"})
        ]), color="dark", inverse=True), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H4("Top Genre", style={"fontWeight": "bold", "fontSize": "18px"}),
            html.H5(top_genre, style={"fontSize": "20px", "fontWeight": "500"})
        ]), color="dark", inverse=True), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H4("Avg. Movie Duration", style={"fontWeight": "bold", "fontSize": "18px"}),
            html.H5(f"{avg_duration} min", style={"fontSize": "20px", "fontWeight": "500"})
        ]), color="dark", inverse=True), md=3)
    ], className="mb-4"),

    dbc.Card([
        dbc.CardHeader("Filter by Type and Year"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Select Content Type:"),
                    dcc.Dropdown(
                        id='type-dropdown',
                        options=[{'label': t, 'value': t} for t in df['type'].unique()],
                        value='Movie',
                        clearable=False,
                        style={"zIndex": 1100, "position": "relative", "marginBottom": "100px"}
                    )
                ], md=6),

                dbc.Col([
                    html.Label("Select Year:"),
                    dcc.Slider(
                        id='year-slider',
                        min=int(df['added_year'].min()),
                        max=int(df['added_year'].max()),
                        step=1,
                        value=int(df['added_year'].max()),
                        marks={int(y): str(int(y)) for y in sorted(df['added_year'].dropna().unique())}
                    )
                ], md=6)
            ])
        ])
    ], className="mb-5"),

    dbc.Card([
        dbc.CardHeader([html.I(className="fas fa-circle-notch"), html.Span(" Content Type Distribution")]),
        dbc.CardBody(dcc.Graph(figure=fig_donut))
    ], className="mb-4"),

    dbc.Card([
        dbc.CardHeader([html.I(className="fas fa-globe"), html.Span(" Top Countries by Content")]),
        dbc.CardBody(dcc.Graph(id='country-bar'))
    ], className="mb-4"),

    dbc.Card([
        dbc.CardHeader([html.I(className="fas fa-star"), html.Span(" Rating Distribution in Selected Year")]),
        dbc.CardBody(dcc.Graph(id='yearly-content'))
    ], className="mb-4"),

    dbc.Card([
        dbc.CardHeader([html.I(className="fas fa-theater-masks"), html.Span(" Most Common Genres")]),
        dbc.CardBody(dcc.Graph(id='genre-bar'))
    ], className="mb-4"),

    html.Footer([
        html.Div("Designed & Developed by Mehrad Sehat | Netflix Data Dashboard © 2025",
                 style={"marginBottom": "8px", "fontSize": "14px", "color": "#aaaaaa"}),

        html.Div([
            html.A(html.I(className="fab fa-github"), href="https://github.com/mehradsehat", target="_blank",
                   style={"color": "#aaaaaa", "margin": "0 10px", "fontSize": "20px"}),

            html.A(html.I(className="fab fa-linkedin"), href="https://www.linkedin.com/in/mehradsehat/", target="_blank",
                   style={"color": "#aaaaaa", "margin": "0 10px", "fontSize": "20px"}),

            html.A(html.I(className="fas fa-envelope"), href="mailto:mehradsehat2002@gmail.com",
                   style={"color": "#aaaaaa", "margin": "0 10px", "fontSize": "20px"})
        ])
    ], style={
        "textAlign": "center",
        "padding": "30px 0 20px 0",
        "borderTop": "1px solid #333",
        "marginTop": "60px"
    })
], fluid=True, style={"backgroundColor": "#121212"})

# ---------------------- Callbacks ----------------------
@app.callback(
    [Output('country-bar', 'figure'),
     Output('yearly-content', 'figure'),
     Output('genre-bar', 'figure')],
    [Input('type-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_dashboard(selected_type, selected_year):
    filtered = df[df['type'] == selected_type]

    # Country chart
    top_countries = filtered['country'].value_counts().head(10).reset_index()
    top_countries.columns = ['country', 'count']
    fig_country = px.bar(top_countries, x='country', y='count',
                         labels={'country': 'Country', 'count': 'Number of Titles'},
                         title=f"Top 10 Countries for {selected_type}s")
    fig_country.update_layout(
        plot_bgcolor="#121212",
        paper_bgcolor="#121212",
        font=dict(color="white"),
        colorway=["#7d3cff"]
    )

    # Yearly rating chart
    year_data = filtered[filtered['added_year'] == selected_year]
    fig_year = px.histogram(year_data, x='rating', color='rating',
                            title=f"{selected_type}s Released in {selected_year} by Rating")
    fig_year.update_traces(marker_line_width=0.5)
    fig_year.update_xaxes(title_text='Rating', tickfont=dict(size=12))
    fig_year.update_layout(
        plot_bgcolor="#121212",
        paper_bgcolor="#121212",
        font=dict(color="white"),
        xaxis_title='Rating',
        colorway=["#f2d53c", "#c80e13", "#7d3cff"]
    )

    # Genre chart
    genre_list = [genre for genres in year_data['genres'] for genre in genres]
    top_genres = Counter(genre_list).most_common(10)
    genre_df = pd.DataFrame(top_genres, columns=['Genre', 'Count'])
    fig_genre = px.bar(genre_df, x='Genre', y='Count', title='Top Genres')
    fig_genre.update_layout(
        plot_bgcolor="#121212",
        paper_bgcolor="#121212",
        font=dict(color="white"),
        colorway=["#7d3cff"]
    )

    return fig_country, fig_year, fig_genre

# ---------------------- Run App ----------------------
if __name__ == '__main__':
    app.run(debug=True)