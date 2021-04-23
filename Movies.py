import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Load CSV file from Datasets folder
df1 = pd.read_csv('moviesData.csv')
genres = df1['Genres'].unique()
genreList = []
for genre in genres:
    try:
        sep_genre = genre.split(',')
    except:
        pass
    for singleGenre in sep_genre:
        if singleGenre not in genreList:
            genreList.append(singleGenre)
#df1 = pd.read_csv('CoronavirusTotal.csv')
#df2 = pd.read_csv('CoronaTimeSeries.csv')

app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1(children='PerfectMovie',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Streaming Service records', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of movies on a given streaming service'),
    dcc.Graph(id='graph1'),
    html.Div(className='toggleRow', children=[
        dcc.Checklist(
            id="percentToggle",
            options=[
            {'label': 'Toggle Percentage', 'value': 'Percentage'}
            ]
        )
    ]),
    html.Div(className = 'row', children = [
        html.Div(className = 'four columns', children = [
            dcc.Dropdown(
                id='select-Genre',
                options=[
                    {'label': genre, 'value': genre} for genre in genreList
                ],
                placeholder='Select Genre...',
                clearable = False,
                searchable = True
            ),
        ], style= {'width': '25%', 'margin-top': '6px'}),
        html.Div(className = 'four columns', children = [
            html.Div('Select Minimum Rating',
                     style={'textAlign': 'center',
                            'color': '#A9A9A9',
                            'font-size': 'medium',
                            'margin-bottom': '6px'}),
            dcc.Slider(
                id='select-Rating',
                min=0,
                max=100,
                step=1,
                value=0,
                marks={
                    0: {'label': '0%', 'style': {'color': '#77b0b1'}},
                    25: {'label': '25%', 'style': {'color': '#77b0b1'}},
                    50: {'label': '50%', 'style': {'color': '#77b0b1'}},
                    75: {'label': '75%', 'style': {'color': '#77b0b1'}},
                    100: {'label': '100%', 'style': {'color': '#77b0b1'}}
                },
                included = True
            ),
            html.Div(id='rating-output', style={'textAlign': 'center',
                                                'color': '#A9A9A9',
                                                'font-size': 'medium',
                                                'margin-bottom': '6px'})
        ], style={'width': '25%', 'margin-top': '6px'}),
        html.Div(className = 'four columns', children = [
            html.Div('Select length range',
                     style={'textAlign': 'center',
                            'color': '#A9A9A9',
                            'font-size': 'medium',
                            'margin-bottom': '6px'}),
            dcc.RangeSlider(
                id='select-Length',
                min=1,
                max=1256,
                step=1,
                value=[1, 1256],
                marks={
                    1: {'label': '1 min', 'style': {'color': '#77b0b1'}},
                    314: {'label': '314 mins', 'style': {'color': '#77b0b1'}},
                    628: {'label': '628 mins', 'style': {'color': '#77b0b1'}},
                    948: {'label': '948 mins', 'style': {'color': '#77b0b1'}},
                    1256: {'label': '1256 mins', 'style': {'color': '#77b0b1'}}
                },
                included=True,
                allowCross=False
            ),
            html.Div(id='length-output', style={'textAlign': 'center',
                                                'color': '#A9A9A9',
                                                'font-size': 'medium',
                                                'margin-bottom': '6px'})
        ], style= {'width': '25%', 'margin-top': '6px'}),
        html.Div(className = 'four columns', children = [
            html.Div('Select year range',
                     style={'textAlign': 'center',
                            'color': '#A9A9A9',
                            'font-size': 'medium',
                            'margin-bottom': '6px'}),
            dcc.RangeSlider(
                id='select-Age',
                min = 1902,
                max = 2020,
                step = 1,
                value = [1902, 2020],
                marks = {
                    1902: {'label': 1902, 'style': {'color': '#77b0b1'}},
                    1931: {'label': 1931, 'style': {'color': '#77b0b1'}},
                    1961: {'label': 1961, 'style': {'color': '#77b0b1'}},
                    1990: {'label': 1990, 'style': {'color': '#77b0b1'}},
                    2020: {'label': 2020, 'style': {'color': '#77b0b1'}}
                },
                included = True,
                allowCross = False
            ),
            html.Div(id='year-output', style={'textAlign': 'center',
                                                'color': '#A9A9A9',
                                                'font-size': 'medium',
                                                'margin-bottom': '6px'})
        ], style={'width': '25%', 'margin-top': '6px'})
    ], style={'display': 'flex'})
])

@app.callback(Output('rating-output', 'children'),
              [Input('select-Rating', 'drag_value')])
def display_value(drag_value):
    return 'More than {}%'.format(drag_value)

@app.callback(Output('length-output', 'children'),
              [Input('select-Length', 'drag_value')])
def display_value(drag_value):
    if drag_value is None:
        return 'Between {} and {} mins'.format(0, 0)
    return 'Between {} and {} mins'.format(drag_value[0], drag_value[1])

@app.callback(Output('year-output', 'children'),
              [Input('select-Age', 'drag_value')])
def display_value(drag_value):
    if drag_value is None:
        return 'Between {} and {} mins'.format(0, 0)
    return 'Created between {} and {}'.format(drag_value[0], drag_value[1])

@app.callback(Output('graph1', 'figure'),
              [Input('percentToggle', 'value'),
               Input('select-Genre', 'value'),
               Input('select-Age', 'drag_value'),
               Input('select-Length', 'drag_value'),
               Input('select-Rating', 'drag_value')])
def update_figure(togglePercentage, selected_genre, selected_years, selected_length, selected_rating):
    filtered_df1 = df1
    NetflixTotal = safeFilter(filtered_df1, "Netflix")
    HuluTotal = safeFilter(filtered_df1, "Hulu")
    PrimeTotal = safeFilter(filtered_df1, "Prime Video")
    DisneyTotal = safeFilter(filtered_df1, "Disney+")


    #filtered_df1 = filtered_df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    print(selected_genre)
    print(selected_years)
    print(selected_length)
    print(selected_rating)
    if selected_genre:
        filtered_df1 = df1[df1["Genres"].str.contains(selected_genre, na=False)]
    if selected_years:
        filtered_df1 = filtered_df1[
            (selected_years[0] <= filtered_df1["Year"]) & (filtered_df1["Year"] <= selected_years[1])]
    if selected_length:
        filtered_df1 = filtered_df1[
            ((selected_length[0] <= filtered_df1["Runtime"]) & (filtered_df1["Runtime"] <= selected_length[1]))] #| (filtered_df1["Runtime"].isnull())
    if selected_rating:
        #try:
        filtered_df1 = filtered_df1[
                (filtered_df1["Rotten Tomatoes"].notna())]
        filtered_df1 = filtered_df1[(selected_rating <= filtered_df1["Rotten Tomatoes"].str.rstrip("%").astype(int))]
        #except ValueError:
            #pass
    if togglePercentage:
        new_df1 = round((safeFilter(filtered_df1, "Netflix") / NetflixTotal), 2) * 100
        new_df2 = round((safeFilter(filtered_df1, "Hulu") / HuluTotal), 2) * 100
        new_df3 = round((safeFilter(filtered_df1, "Prime Video") / PrimeTotal), 2) * 100
        new_df4 = round((safeFilter(filtered_df1, "Disney+") / DisneyTotal), 2) * 100
        data_interactive_barchart = [
            go.Bar(x=['Netflix', 'Hulu', 'Prime Video', 'Disney+'], y=[new_df1, new_df2, new_df3, new_df4])]
        return {'data': data_interactive_barchart,
                'layout': go.Layout(title='percentage of films on each streaming service matching filter criteria',
                                    xaxis={'title': 'Service'},
                                    yaxis={'title': 'percentage of films'})}

    else:
        new_df1 = safeFilter(filtered_df1, "Netflix")
        new_df2 = safeFilter(filtered_df1, "Hulu")
        new_df3 = safeFilter(filtered_df1, "Prime Video")
        new_df4 = safeFilter(filtered_df1, "Disney+")
        data_interactive_barchart = [
            go.Bar(x=['Netflix', 'Hulu', 'Prime Video', 'Disney+'], y=[new_df1, new_df2, new_df3, new_df4])]
        return {'data': data_interactive_barchart,
                'layout': go.Layout(title='Number of movies on each streaming service',
                                    xaxis={'title': 'Filters'},
                                    yaxis={'title': 'Number of films'})}



def safeFilter(dataframe, service):
    try:
        filtered_df = dataframe[service].value_counts()[1]
    except KeyError:
        filtered_df = 0
    return filtered_df


if __name__ == '__main__':
    app.run_server()