import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


df = pd.read_csv("test.csv")
sentimentData = pd.read_csv('sentimentData.csv')

years = df.groupby('year_of_release')['episode_rating'].mean().reset_index()
fig = px.scatter(years, x = 'year_of_release', y = 'episode_rating')

average_rating1 = df.groupby('genre_1')['episode_rating'].mean()
average_rating2 = df.groupby('genre_2')['episode_rating'].mean()
average_rating3 = df.groupby('genre_3')['episode_rating'].mean()


fig6 = px.line(average_rating1,
             y =['episode_rating'])

fig3 = px.histogram(df, x = 'episode_rating', title = 'Rating of Episodes')

fig2 = px.pie(df, 
             values = df['genre_1'].value_counts(),
            names = df['genre_1'].value_counts().index)

fig4 = px.pie(df, 
             values = df['genre_2'].value_counts(),
            names = df['genre_2'].value_counts().index)

fig5 = px.pie(df, 
             values = df['genre_3'].value_counts(),
            names = df['genre_3'].value_counts().index)

fig7 = px.line(average_rating2,
             y =['episode_rating'])

fig8 = px.line(average_rating3,
             y =['episode_rating'])


df['id'] = df['show_name']
df.set_index('id', inplace=True, drop=True)
sentimentData['id'] = sentimentData['show_name']
sentimentData.set_index('id', inplace=True, drop=True)

variable_labels = {
    'episode_rating': 'Episode Rating (out of 10)',
    'votes': 'Number of user votes',
    'year_of_release': 'Year of release',
    'watchtime_min': 'Length (minutes)'
}

app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.JOURNAL])
server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.css.config.serve_locally = False
suppress_callback_exceptions=True

sidebar = html.Div(
    [
        html.H2("", className="display-4"),
        html.H6(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Static Graphs", href="/page-1", active="exact"),
                dbc.NavLink("Interactive Graphs", href="/page-2", active="exact"),
                dbc.NavLink("Data Table", href = "/page-3", active = "exact"),
                dbc.NavLink("Sentiment Scores Data Table ", href = "/page-4", active = "exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([

    dcc.Location(id="url"),
    sidebar,
    content,
    
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1("Episodes Dashboard"),
                html.H2("Made by Abdallah"),
                html.P("This dashboard was made for part of my big data programming project where I was tasked with collecting data and getting analytics of said data"),
                html.P("The data in this dashboard was collected by me by webscraping IMDB, using Python and R, to get all the data for the episodes along with the top review for each episode. Sentiment analysis was also done to determine whether the review was positive, negative, or neutral."),
                html.P("The contents of the dashboard include static graphs, which shows analytics which was found through an exploratory data analysis. It also has an interactive graph which allows you to filter out the data you want to see, and finally data tables so you can view the data I have collected yourself and also filter through it"),
                html.P("This was done using dash and I hope you enjoy it :D"),
                html.Br(),
                html.H6("My links:"),
                html.B("Github: "),
                html.A("https://github.com/Abdallah1321/IMDBepisodes", href="https://github.com/Abdallah1321/IMDBepisodes"),
                html.Br(),
                html.B("LinkedIn: "),
                html.A("https://www.linkedin.com/in/abdallah-ibrahim37/", href="https://www.linkedin.com/in/abdallah-ibrahim37/", target = "_blank"),
                html.Br(),
                html.B("Kaggle link for Sentiment Analysis: "),
                html.A("https://www.kaggle.com/abdallah185/sentiment-analysis-for-show-episode-reviews-imdb", href="https://www.kaggle.com/abdallah185/sentiment-analysis-for-show-episode-reviews-imdb", target="_blank"),
                html.Br(),
                html.B("Kaggle link for EDA: " ),
                html.A("https://www.kaggle.com/code/abdallah185/eda-for-tv-show-episodes-imdb/notebook", href = "https://www.kaggle.com/code/abdallah185/eda-for-tv-show-episodes-imdb/notebook", target="_blank"),
                ]
    elif pathname == "/page-1":
        return [
            html.Div([
                html.H1('Analytics',
                        style={'textAlign':'center'}),
            ]),
            html.Div([
                html.H2('Occurences Of Episode Ratings For All Shows', style = {'textAlign': 'center'}),
                html.P('This is a histogram which shows the occurences of episode ratings. This helps us visualise and see what rating range episodes tend to be in, and what is the most common episode rating. ', style = {'textAlign': 'center'}),
                dcc.Graph(
                    id = 'avg-graph',
                    figure = fig3
                ),
                html.H2('Average Episode Rating Throughout The Years', style = {'textAlign': 'center'}),
                html.P('This scatter graph shows the average episode rating for each year. This lets us see which year had the best episodes.', style = {'textAlign': 'center'}),
                dcc.Graph(
                    id = "year-graph",
                    figure = fig
                ),
                html.H2("Counts Of Primary Genre For Each Episode", style = {'textAlign': 'center'}),
                html.P("Episodes can have up to three main genres, the primary genre, secondary genre, and tertiary genre. The pie charts below show the occurences of each genre respectively.", style = {'textAlign': 'center'}),
                dcc.Graph(
                    id= 'fig2-graph',
                    figure = fig2
                ),
                html.H2("Counts Of Secondary Genre For Each Episode", style = {'textAlign': 'center'}),
                dcc.Graph(
                    id= 'fig4-graph',
                    figure = fig4
                ),
                html.H2("Counts Of Tertiary Genre For Each Episode", style = {'textAlign': 'center'}),
                dcc.Graph(
                    id= 'fig5-graph',
                    figure = fig5
                ),
                html.H2("Average Rating For Primary Genres", style = {'textAlign': 'center'}),
                html.P("The line graphs show the average rating for each genre respectively.", style = {'textAlign': 'center'}),
                dcc.Graph(
                    id = 'fig6-graph',
                    figure = fig6
                ),
                html.H2("Average Rating For Secondary Genres", style = {'textAlign': 'center'}),
                dcc.Graph(
                    id = 'fig6-graph',
                    figure = fig7
                ),
                html.H2("Average Rating For Tertiary Genres", style = {'textAlign': 'center'}),
                dcc.Graph(
                    id = 'fig6-graph',
                    figure = fig8
                ),
            ])
                ]
    elif pathname == "/page-2":
        return [
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
                        options=
                            sorted([{'label': str(genre), 'value': str(genre)} for genre in df.genre_1.unique()], key = lambda x: x['label'])
                        ,
                        multi=False,
                        value = "Animation"
                    ),
                            html.Br(),
                    html.Label('Secondary Genre'),
                    dcc.Dropdown(
                        id='genre2-dropdown',
                        options=
                            sorted([{'label': str(genre), 'value': str(genre)} for genre in df.genre_2.unique()], key = lambda x: x['label'])
                        ,
                        multi=False
                    ),
                    html.Br(),
                    html.Label('Tertiary Genre'),
                    dcc.Dropdown(
                        id='genre3-dropdown',
                        options=
                            sorted([{'label': str(genre), 'value': str(genre)} for genre in df.genre_3.unique()], key = lambda x: x['label'])
                        ,
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
                            )
                        }
                    ),
                    html.Br(),
                    html.P('Number of rows selected: {}'.format(len(df.index)), id='dataset-rows-p')
                ], style = {'marginLeft': 25, 'marginRight': 25})
                ]
    elif pathname == "/page-3":
        return [
                html.Div([
                html.H1("Dataset With All Episodes", style = {'textAlign': 'center'}),
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
                )
            ])
        ]
    elif pathname == "/page-4":
                return [
                html.Div([
                html.H1("Dataset With Sentiment For Reviews", style = {'textAlign': 'center'}),
                dash_table.DataTable(
                    id='datatable2-interactivity',
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
                        if i == "show_name" or i == "id"
                        else {"name": i, "id": i, "deletable": True, "selectable": True }
                        for i in sentimentData.columns
                    ],
                    data = sentimentData.to_dict('records'),
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
                )
            ])
        ]

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        dbc.Container(
        [
            html.H1("404: Not found", className="display-3"),
            html.Hr(className="my-2"),
            html.P(f"The pathname {pathname} was not recognised...", className="lead"),
        ],
        fluid=True,
        className="h-100 p-5 bg-light border rounded-3",
        ),
        className="p-3 bg-light rounded-3"
    )

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
    x_axis = x_axis_var or 'episode_rating'
    y_axis = y_axis_var or 'votes'

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
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
