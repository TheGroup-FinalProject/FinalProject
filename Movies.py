import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

# Load CSV file from Datasets folder
df1 = pd.read_csv('moviesData.csv')

#create list of separate genres
genres = df1['Genres'].unique()
genreList = ["All"]
for genre in genres:
    try:
        sep_genre = genre.split(',')
    except:
        pass
    for singleGenre in sep_genre:
        if singleGenre not in genreList:
            genreList.append(singleGenre)

#initialize global variables to be used among all pages
global globalGenre
globalGenre = "All"

global globalRatingBool
globalRatingBool = None
global globalRating
globalRating = None

global globalLengthBool
globalLengthBool = None
global globalLengths
globalLengths = None

global globalYearBool
yearRangeBool = None
global globalYears
globalYears = None



app = dash.Dash(__name__)


# initializing layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#main page layout
page_1_layout = html.Div(children=[
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

    #create links to list pages#create links to list pages
    html.Div(className='row', children=[
        html.Div(className = 'four columns', children = [
            dcc.Link(
                html.Button('Show movie List'),
                href='/netList',
                style = {"position":"relative", "left":"12.5%"}),
            dcc.Link(
                html.Button('Show movie List'),
                href='/huList',
                style = {"position":"relative", "left":"28.5%"}),
            dcc.Link(
                html.Button('Show movie List'),
                href='/pvList',
                style = {"position":"relative", "left":"44.45%"}),
            dcc.Link(
                html.Button('Show movie List'),
                href='/disList',
                style = {"position":"relative", "left":"60%"})
            ], style = {"position": "relative", "top": "-60px"})

    ]),

    #create percentage toggle
    html.Div(className='toggleRow', children=[
        dcc.Checklist(
            id="percentToggle",
            options=[
            {'label': 'Toggle Percentage', 'value': 'Percentage'}
            ]
        )
    ]),

    #create filters
    html.Div(className = 'row', children = [

        #create genre dropdown
        html.Div(className = 'four columns', children = [
            dcc.Dropdown(
                id='select-Genre',
                options=[
                    {'label': genre, 'value': genre} for genre in genreList
                ],
                placeholder='Select Genre...',
                clearable = False,
                searchable = True
            )
        ], style= {'width': '25%', 'margin-top': '6px'}),

        #create minimum rating slider
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
                                                'margin-bottom': '6px'}),

            #create toggle for rating filter
            dcc.Checklist(
                id="ratingToggle",
                options=[
                    {'label': 'Toggle Rating', 'value': 'ratingSwitch'}
                ],
                value=['ratingSwitch'],
                style={'textAlign': 'center'}
            )
        ], style={'width': '25%', 'margin-top': '6px'}),

        #create runtime range slider
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
                                                'margin-bottom': '6px'}),
            #create toggle for runtime range filter
            dcc.Checklist(
                id="lengthToggle",
                options=[
                    {'label': 'Toggle Length', 'value': 'lengthSwitch'}
                ],
                value=['lengthSwitch'],
                style={'textAlign': 'center'}
            )
        ], style= {'width': '25%', 'margin-top': '6px'}),

        #create year range slider
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
                                                'margin-bottom': '6px'}),

            #create toggle for Year range filter
            dcc.Checklist(
                id="ageToggle",
                options=[
                    {'label': 'Toggle Years', 'value': 'yearSwitch'}
                ],
                value=['yearSwitch'],
                style={'textAlign': 'center'}
            )
        ], style={'width': '25%', 'margin-top': '6px'})
    ], style={'display': 'flex'})
])

#create layout for list of netflix movies
netflixBarList = html.Div(children=[
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
    html.H3('Netflix Barchart movie list with matching search criteria', style={'color': '#df1e56'}),
    html.Div('This searchable List represents all movies given your search criteria on netflix'),
    html.Br(),
    html.Br(),
    dcc.Checklist(
        id="listGen",
        options=[
            {'label': 'Create List', 'value': 'createList'}
        ],
        value=['createList'],
        style={'textAlign': 'center'}
    ),
    dt.DataTable(id='netflixTable',
                 columns=[{'name': movie, 'id': movie} for movie in (set(df1.columns) - set(["Netflix","Hulu", "Prime Video", "Disney+"]))],
                 style_cell={'textAlign': 'left'})

])

#create layout for list of hulu movies
huluBarList = html.Div(children=[
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
    html.H3('Hulu Barchart movie list with matching search criteria', style={'color': '#df1e56'}),
    html.Div('This searchable List represents all movies given your search criteria on netflix'),
    html.Br(),
    html.Br(),
    dcc.Checklist(
        id="listGen",
        options=[
            {'label': 'Create List', 'value': 'createList'}
        ],
        value=['createList'],
        style={'textAlign': 'center'}
    ),
    dt.DataTable(id='huluTable',
                 columns=[{'name': movie, 'id': movie} for movie in (set(df1.columns) - set(["Netflix","Hulu", "Prime Video", "Disney+"]))],
                 style_cell={'textAlign': 'left'})

])

#create layout for list of prime video movies
primeBarList = html.Div(children=[
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
    html.H3('Prime Video Barchart movie list with matching search criteria', style={'color': '#df1e56'}),
    html.Div('This searchable List represents all movies given your search criteria on netflix'),
    html.Br(),
    html.Br(),
    dcc.Checklist(
        id="listGen",
        options=[
            {'label': 'Create List', 'value': 'createList'}
        ],
        value=['createList'],
        style={'textAlign': 'center'}
    ),
    dt.DataTable(id='primeTable',
                 columns=[{'name': movie, 'id': movie} for movie in (set(df1.columns) - set(["Netflix","Hulu", "Prime Video", "Disney+"]))],
                 style_cell={'textAlign': 'left'})

])

#create layout for list of Disney+ movies
disneyBarList = html.Div(children=[
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
    html.H3('Disney Barchart movie list with matching search criteria', style={'color': '#df1e56'}),
    html.Div('This searchable List represents all movies given your search criteria on netflix'),
    html.Br(),
    html.Br(),
    dcc.Checklist(
        id="listGen",
        options=[
            {'label': 'Create List', 'value': 'createList'}
        ],
        value=['createList'],
        style={'textAlign': 'center'}
    ),
    dt.DataTable(id='disneyTable',
                 columns=[{'name': movie, 'id': movie} for movie in (set(df1.columns) - set(["Netflix","Hulu", "Prime Video", "Disney+"]))],
                 style_cell={'textAlign': 'left'})

])

#callback to dynamically update string value under rating filter
@app.callback(Output('rating-output', 'children'),
              [Input('select-Rating', 'drag_value')])
def display_value(drag_value):
    return 'More than {}%'.format(drag_value)

#callback to dynamically update string value under runtime range filter
@app.callback(Output('length-output', 'children'),
              [Input('select-Length', 'drag_value')])
def display_value(drag_value):
    if drag_value is None:
        return 'Between {} and {} mins'.format(0, 0)
    return 'Between {} and {} mins'.format(drag_value[0], drag_value[1])

#callback to dynamically update string value under Year range filter
@app.callback(Output('year-output', 'children'),
              [Input('select-Age', 'drag_value')])
def display_value(drag_value):
    if drag_value is None:
        return 'Between {} and {} mins'.format(0, 0)
    return 'Created between {} and {}'.format(drag_value[0], drag_value[1])

#callback to create the barchart
@app.callback(Output('graph1', 'figure'),
              [Input('percentToggle', 'value'),
               Input('select-Genre', 'value'),
               Input('select-Age', 'drag_value'),
               Input('select-Length', 'drag_value'),
               Input('select-Rating', 'drag_value'),
               Input('ratingToggle', 'value'),
               Input('lengthToggle', 'value'),
               Input('ageToggle', 'value')])
def update_figure(togglePercentage, selected_genre, selected_years, selected_length, selected_rating, toggle_rating, toggle_length, toggle_age):
    filtered_df1 = df1
    NetflixTotal = safeFilterCounts(filtered_df1, "Netflix")
    HuluTotal = safeFilterCounts(filtered_df1, "Hulu")
    PrimeTotal = safeFilterCounts(filtered_df1, "Prime Video")
    DisneyTotal = safeFilterCounts(filtered_df1, "Disney+")


    print(selected_genre)
    print(selected_years)
    print(selected_length)
    print(selected_rating)
    if selected_genre:
        if selected_genre != 'All':
            global globalGenre
            globalGenre = selected_genre
            filtered_df1 = df1[df1["Genres"].str.contains(selected_genre, na=False)]

    if toggle_age:
        global globalYearBool
        globalYearBool = True
        if selected_years:
            global globalYears
            globalYears = [selected_years[0], selected_years[1]]
            filtered_df1 = filtered_df1[
                (selected_years[0] <= filtered_df1["Year"]) & (filtered_df1["Year"] <= selected_years[1])]

    if toggle_length:
        global globalLengthBool
        globalLengthBool = True
        if selected_length:
            global globalLengths
            globalLengths = [selected_length[0], selected_length[1]]
            filtered_df1 = filtered_df1[
                (filtered_df1["Runtime"].notna())]
            filtered_df1 = filtered_df1[
                ((selected_length[0] <= filtered_df1["Runtime"]) & (filtered_df1["Runtime"] <= selected_length[1]))]

    if toggle_rating:
        global globalRatingBool
        globalRatingBool = True
        if selected_rating:
            global globalRating
            globalRating = selected_rating
            filtered_df1 = filtered_df1[
                    (filtered_df1["Rotten Tomatoes"].notna())]
            filtered_df1 = filtered_df1[(selected_rating <= filtered_df1["Rotten Tomatoes"].str.rstrip("%").astype(int))]

    new_df1 = safeFilterCounts(filtered_df1, "Netflix")
    new_df2 = safeFilterCounts(filtered_df1, "Hulu")
    new_df3 = safeFilterCounts(filtered_df1, "Prime Video")
    new_df4 = safeFilterCounts(filtered_df1, "Disney+")
    if togglePercentage:
        new_df1 = round((new_df1 / NetflixTotal), 2) * 100
        new_df2 = round((new_df2 / HuluTotal), 2) * 100
        new_df3 = round((new_df3 / PrimeTotal), 2) * 100
        new_df4 = round((new_df4 / DisneyTotal), 2) * 100
        data_interactive_barchart = [
            go.Bar(x=['Netflix', 'Hulu', 'Prime Video', 'Disney+'], y=[new_df1, new_df2, new_df3, new_df4])]
        return {'data': data_interactive_barchart,
                'layout': go.Layout(title='percentage of films on each streaming service matching filter criteria',
                                    xaxis={'title': 'Service'},
                                    yaxis={'title': 'percentage of films'})}

    else:
        data_interactive_barchart = [
            go.Bar(x=['Netflix', 'Hulu', 'Prime Video', 'Disney+'], y=[new_df1, new_df2, new_df3, new_df4])]
        return {'data': data_interactive_barchart,
                'layout': go.Layout(title='Number of movies on each streaming service',
                                    xaxis={'title': 'Service'},
                                    yaxis={'title': 'Number of films'})}

#callback to update the netflix movie list
@app.callback(Output('netflixTable', 'data'),
               Input('listGen', 'value'))
def update_table(genVal):
    filtered_df1 = df1

    if genVal:
        filtered_df1 = filterForBar(filtered_df1)

        netflixData = filtered_df1[filtered_df1['Netflix'] == 1]
        netflixData = netflixData[list(set(df1.columns) - set(["Netflix", "Hulu", "Prime Video", "Disney+"]))].to_dict('records')
        return netflixData

#callback to update the hulu movie list
@app.callback(Output('huluTable', 'data'),
              Input('listGen', 'value'))
def update_table(genVal):
    filtered_df1 = df1

    if genVal:
        filtered_df1 = filterForBar(filtered_df1)

        huluData = filtered_df1[filtered_df1['Hulu'] == 1]
        huluData = huluData[list(set(df1.columns) - set(["Netflix", "Hulu", "Prime Video", "Disney+"]))].to_dict('records')
        return huluData

#callback to update the prime video movie list
@app.callback(Output('primeTable', 'data'),
              Input('listGen', 'value'))
def update_table(genVal):
    primefiltered_df1 = df1.copy()

    if genVal:
        primefiltered_df1 = filterForBar(primefiltered_df1)

        primeData = primefiltered_df1[primefiltered_df1['Prime Video'] == 1]
        primeData = primeData[list(set(df1.columns) - set(["Netflix", "Hulu", "Prime Video", "Disney+"]))].to_dict('records')
        return primeData

#callback to update the disney movie list
@app.callback(Output('disneyTable', 'data'),
              Input('listGen', 'value'))
def update_table(genVal):
    filtered_df1 = df1

    if genVal:
        filtered_df1 = filterForBar(filtered_df1)

        disneyData = filtered_df1[filtered_df1['Disney+'] == 1]
        disneyData = disneyData[list(set(df1.columns) - set(["Netflix", "Hulu", "Prime Video", "Disney+"]))].to_dict('records')
        return disneyData

#function to filter dataframes
def filterForBar(df):
    if globalGenre != 'All':
        df = df[df["Genres"].str.contains(globalGenre, na=False)]

    if globalYearBool:
        if globalYears:
            df = df[
                (globalYears[0] <= df["Year"]) & (df["Year"] <= globalYears[1])]

    if globalLengthBool:
        if globalLengths:
            df = df[
                (df["Runtime"].notna())]
            df = df[
                ((globalLengths[0] <= df["Runtime"]) & (
                             df["Runtime"] <= globalLengths[1]))]

    if globalRatingBool:
        if globalRating:
            df = df[
                (df["Rotten Tomatoes"].notna())]
            df = df[
                (globalRating <= df["Rotten Tomatoes"].str.rstrip("%").astype(int))]

    return df

def safeFilterCounts(dataframe, service):
    try:
        filtered_df = dataframe[service].value_counts()[1]
    except KeyError:
        filtered_df = 0
    return filtered_df

#callback to change pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/netList':
        return netflixBarList
    elif pathname == '/huList':
        return huluBarList
    elif pathname == '/pvList':
        return primeBarList
    elif pathname == '/disList':
        return disneyBarList
    else:
        #set globals to initial valueswhen initila page is loaded
        global globalGenre
        globalGenre = "All"

        global globalRatingBool
        globalRatingBool = True

        global globalRating
        globalRating = 0
        global globalLengthBool
        globalLengthBool = True

        global globalLengths
        globalLengths = [0, 1256]

        global yearRangeBool
        yearRangeBool = None

        global globalYears
        globalYears = None

        return page_1_layout

if __name__ == '__main__':
    app.run_server()