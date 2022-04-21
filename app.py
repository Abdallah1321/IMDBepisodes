import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_csv("test.csv")

df['id'] = df['show_name']
df.set_index('id', inplace=True, drop=False)

variable_labels = {
    'episode_rating': 'Episode Rating (out of 10)',
    'votes': 'Number of user votes',
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
        html.Br(),
        html.Label('Pick a show name'),
        dcc.Dropdown(
            id='showname-dropdown',
            options = 
                sorted([{'label': show, 'value': show} for show in df.show_name.unique()], key = lambda x: x['label'])
            
        )
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
    ], style = {'marginLeft': 25, 'marginRight': 25}),
    html.Div([
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
                if i == "show_name" or i == "id"
                else {"name": i, "id": i, "deletable": True, "selectable": True }
                for i in df.columns
            ],
            data = df.to_dict('records'),
            editable = True,
            filter_action= "native",
            sort_action = "native",
            sort_mode = "single",
            column_selectable="multi",
            row_selectable="multi",
            row_deletable=True,
            selected_columns = [],
            selected_rows = [],
            page_action="native",
            page_current=0,
            page_size = 20,
            style_cell={
                'minWidth': 95, 'maxWidth': 95, 'width': 95
            },
            style_cell_conditional=[
                {
                'if': {'column_id': s},
                'textAlign': 'left'
                } for s in ['show_name']
            ],
            style_data={
                'whitespace': 'normal',
                'height': 'auto'
            }
        ),

        html.Br(),
        html.Br(),
        html.Div(id='bar-container'),
        html.Div(id = 'choromap-container')
    ])
])

@app.callback(
    dash.dependencies.Output('scatter-plot-graph', 'figure'),
    [
        dash.dependencies.Input('votes-count-slider', 'value'),
        dash.dependencies.Input('year-released-range-slider', 'value'),
        dash.dependencies.Input('genre1-dropdown', 'value'),
        dash.dependencies.Input('genre2-dropdown', 'value'),
        dash.dependencies.Input('genre3-dropdown', 'value'),
        dash.dependencies.Input('showname-dropdown', 'value'),
        dash.dependencies.Input('x-axis-dropdown', 'value'),
        dash.dependencies.Input('y-axis-dropdown', 'value')
    ]
)
def update_scatter_plot(selected_vote_count, selected_year_of_release, selected_genre1, selected_genre2,
                        selected_genre3, selected_show,x_axis_var, y_axis_var):
    nb_reviews = selected_vote_count or df.votes.min()
    year_of_release_min, year_of_release_max = selected_year_of_release or (df.year_of_release.min(), df.year_of_release.max())
    primary_genre = selected_genre1 or None
    secondary_genre = selected_genre2 or None
    tertiary_genre = selected_genre3 or None
    show_name = selected_show or None
    x_axis = x_axis_var or 'Rating'
    y_axis = y_axis_var or 'Votes'

    filtered_df = (
        df.pipe(lambda df: df[df['votes'] >= nb_reviews])
        .pipe(lambda df: df[(df['year_of_release'] >= year_of_release_min) & (df['year_of_release'] <= year_of_release_max)])
        .pipe(lambda df: df[df['genre_1'].str.contains(primary_genre, na=False)] if primary_genre else df)
        .pipe(lambda df: df[df['genre_2'].str.contains(secondary_genre, na=False)] if secondary_genre else df)
        .pipe(lambda df: df[df['genre_3'].str.contains(tertiary_genre, na=False)] if tertiary_genre else df)
        .pipe(lambda df: df[df['show_name'].str.contains(show_name)] if show_name else df)
    )

    return {
        'data': [
            go.Scatter(
                x=filtered_df[x_axis],
                y=filtered_df[y_axis],
# COME BACK HERE BECAUSE WEIRD ERROR
                text=filtered_df.show_name + ", " + filtered_df.episode_name,
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
        dash.dependencies.Input('showname-dropdown', 'value'),
        dash.dependencies.Input('x-axis-dropdown', 'value'),
        dash.dependencies.Input('y-axis-dropdown', 'value')
    ]
)

def update_row_count(selected_vote_count, selected_year_of_release, selected_genre1, selected_genre2,
                        selected_genre3, selected_show, x_axis_var, y_axis_var):
    nb_reviews = selected_vote_count or df.votes.min()
    year_of_release_min, year_of_release_max = selected_year_of_release or (df.year_of_release.min(), df.year_of_release.max())
    primary_genre = selected_genre1 or None
    secondary_genre = selected_genre2 or None
    tertiary_genre = selected_genre3 or None
    show_name = selected_show or None
    x_axis = x_axis_var or 'Rating'
    y_axis = y_axis_var or 'Votes'

    filtered_df = (
        df.pipe(lambda df: df[df['votes'] >= nb_reviews])
        .pipe(lambda df: df[(df['year_of_release'] >= year_of_release_min) & (df['year_of_release'] <= year_of_release_max)])
        .pipe(lambda df: df[df['genre_1'].str.contains(primary_genre, na=False)] if primary_genre else df)
        .pipe(lambda df: df[df['genre_2'].str.contains(secondary_genre, na=False)] if secondary_genre else df)
        .pipe(lambda df: df[df['genre_3'].str.contains(tertiary_genre, na=False)] if tertiary_genre else df)
        .pipe(lambda df: df[df['show_name'].str.contains(show_name)] if show_name else df)
    )

    return 'Number of rows selected: {}'.format(len(filtered_df.index))



app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})


if __name__ == '__main__':
    app.run_server(debug=True)
