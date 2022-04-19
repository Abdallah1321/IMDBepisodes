import dash
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv("test.csv")

variable_labels = {
    'episode_rating': 'Numeric Rating',
    'votes': 'Number of user reviews',
    'year_of_release': 'Year of release',
    'watchtime_min': 'Length (minutes)'
}

app = dash.Dash(__name__, )
app.css.config.serve_locally = False

app.layout = html.Div([
    html.H1("Episodes Dashboard"),
    html.H2("Made by Abdallah"),
    html.Div([
        html.Label('Minimum number of user votes'),
        dcc.Slider(
            id = 'votes-count-slider',
            min = df.votes.min(),
            max = df.votes.max(),
            #marks={str(rvw): str(rvw) for rvw in range(int(df.votes.min()), len(df.votes.unique()), 30)},
            value = df.votes.min(),
            step = 5000
            ),
        html.Br(),
        html.Label('Year released'),
        dcc.RangeSlider(
            id='year-released-range-slider',
            min=df.year_of_release.min(),
            max=df.year_of_release.max(),
            marks={str(y): str(y) for y in range(int(df.year_of_release.min()), int(df.year_of_release.max()), 5)},
            value=[df.year_of_release.min(), df.year_of_release.max()]
        ),
        html.Br(),
        html.Label('Primary Genre'),
        dcc.Dropdown(
            id='genre1-dropdown',
            options=[
                {'label': str(genre), 'value': str(genre)} for genre in df.genre_1.unique()
            ],
            multi=False
        ),
                html.Br(),
        html.Label('Secondary Genre'),
        dcc.Dropdown(
            id='genre2-dropdown',
            options=[
                {'label': str(genre), 'value': str(genre)} for genre in df.genre_2.unique()
            ],
            multi=False
        ),
        html.Br(),
        html.Label('Tertiary Genre'),
        dcc.Dropdown(
            id='genre3-dropdown',
            options=[
                {'label': str(genre), 'value': str(genre)} for genre in df.genre_3.unique()
            ],
            multi=False
        ),
    ], style={'marginLeft': 25, 'marginRight': 25}
    ),
    html.Div([
        html.Br(),
        html.Label('X-axis variable'),
        dcc.Dropdown(
            id = 'x-axis-dropdown',
            options = [
                {'label': label, 'value': value} for value, label in variable_labels.items()
            ],
            multi=False,
            value='episode_rating'
        ),
        html.Br(),
        html.Label('Y-axis variable'),
        dcc.Dropdown(
            id='y-axis-dropdown',
            options=[
                {'label': label, 'value': value} for value, label in variable_labels.items()
            ],
            multi=False,
            value='votes'
        ),
        html.Br()
    ], style ={'marginLeft': 25, 'marginRight': 25}),
    html.Div([
        html.Label('Graph'),
        dcc.Graph(
            id='scatter-plot-graph',
            animate=True,
            figure={
                'data': [
                    go.Scatter(
                        x=df.episode_rating,
                        y=df.votes,
                        text=df.show_name + ", " + df.episode_name,
                        mode='markers',
                        opacity=0.5,
                        marker={
                            'color': 'orange',
                            'size': 10,
                            'line': {'width': 1, 'color': 'black'}
                        },
                        name ='Episodes rating'
                    ),
                ],
                'layout': go.Layout(
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    xaxis={'title': 'Episode Rating'},
                    yaxis={'title': 'Number of user votes'},
                    hovermode='closest'                    
                )
            }
        ),
        html.Br(),
        html.P('Number of rows selected: {}'.format(len(df.index)), id='dataset-rows-p')
    ], style = {'marginLeft': 25, 'marginRight': 25})
])

@app.callback(
    dash.dependencies.Output('scatter-plot-graph', 'figure'),
    [
        dash.dependencies.Input('votes-count-slider', 'value'),
        dash.dependencies.Input('year-released-range-slider', 'value'),
        dash.dependencies.Input('genre1-dropdown', 'value'),
        dash.dependencies.Input('genre2-dropdown', 'value'),
        dash.dependencies.Input('genre3-dropdown', 'value'),
        dash.dependencies.Input('x-axis-dropdown', 'value'),
        dash.dependencies.Input('y-axis-dropdown', 'value')
    ]
)
def update_scatter_plot(selected_vote_count, selected_year_of_release, selected_genre1, selected_genre2,
                        selected_genre3, x_axis_var, y_axis_var):
    nb_reviews = selected_vote_count or df.votes.min()
    year_of_release_min, year_of_release_max = selected_year_of_release or (df.year_of_release.min(), df.year_of_release.max())
    primary_genre = selected_genre1 or None
    secondary_genre = selected_genre2 or None
    tertiary_genre = selected_genre3 or None
    x_axis = x_axis_var or 'Rating'
    y_axis = y_axis_var or 'Votes'

    filtered_df = (
        df.pipe(lambda df: df[df['votes'] >= nb_reviews])
        .pipe(lambda df: df[(df['year_of_release'] >= year_of_release_min) & (df['year_of_release'] <= year_of_release_max)])
        .pipe(lambda df: df[df['genre_1'].str.contains(primary_genre)] if primary_genre else df)
        .pipe(lambda df: df[df['genre_2'].str.contains(secondary_genre)] if secondary_genre else df)
        .pipe(lambda df: df[df['genre_3'].str.contains(tertiary_genre)] if tertiary_genre else df)
    )

    return {
        'data': [
            go.Scatter(
                x=filtered_df[x_axis],
                y=filtered_df[y_axis],
# COME BACK HERE BECAUSE WEIRD ERROR
                text = filtered_df['episode_name'],
                mode = 'markers',
                opacity = 0.5,
                marker = {
                    'color': 'orange',
                    'size': 10,
                    'line': {'width': 1, 'color': 'black'}
                },
                name = 'episodes data'
            )
        ],
        'layout': go.Layout(
            margin={'l': 40, 'b': 40, 't': 10, 'r':10},
            xaxis = {
                'title': variable_labels[x_axis],
                'range': [
                    filtered_df[x_axis].min(),
                    filtered_df[x_axis].max()
                ]
            },
            yaxis={
                'title': variable_labels[y_axis],
                'range': [
                    filtered_df[y_axis].min(),
                    filtered_df[y_axis].max()
                ]},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('dataset-rows-p', 'children'),
    [
        dash.dependencies.Input('votes-count-slider', 'value'),
        dash.dependencies.Input('year-released-range-slider', 'value'),
        dash.dependencies.Input('genre1-dropdown', 'value'),
        dash.dependencies.Input('genre2-dropdown', 'value'),
        dash.dependencies.Input('genre3-dropdown', 'value'),
        dash.dependencies.Input('x-axis-dropdown', 'value'),
        dash.dependencies.Input('y-axis-dropdown', 'value')
    ]
)

def update_scatter_plot(selected_vote_count, selected_year_of_release, selected_genre1, selected_genre2,
                        selected_genre3, x_axis_var, y_axis_var):
    nb_reviews = selected_vote_count or df.votes.min()
    year_of_release_min, year_of_release_max = selected_year_of_release or (df.year_of_release.min(), df.year_of_release.max())
    primary_genre = selected_genre1 or None
    secondary_genre = selected_genre2 or None
    tertiary_genre = selected_genre3 or None
    x_axis = x_axis_var or 'Rating'
    y_axis = y_axis_var or 'Votes'

    filtered_df = (
        df.pipe(lambda df: df[df['votes'] >= nb_reviews])
        .pipe(lambda df: df[(df['year_of_release'] >= year_of_release_min) & (df['year_of_release'] <= year_of_release_max)])
        .pipe(lambda df: df[df['genre_1'].str.contains(primary_genre)] if primary_genre else df)
        .pipe(lambda df: df[df['genre_2'].str.contains(secondary_genre)] if secondary_genre else df)
        .pipe(lambda df: df[df['genre_3'].str.contains(tertiary_genre)] if tertiary_genre else df)
    )

    return 'Number of rows selected: {}'.format(len(filtered_df.index))

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})


if __name__ == '__main__':
    app.run_server(debug=True)
