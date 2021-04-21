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
    html.Div(className = 'row', children = [
        html.Div(className = 'four columns', children = [
            dcc.Dropdown(
                id='select-Genre',
                options=[
                    {'label': genre, 'value': genre} for genre in genreList
                ],
                placeholder='Select Genre...',
                clearable = False,
                searchable = False
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
                value=[0],
                marks={
                    0: {'label': '0%', 'style': {'color': '#77b0b1'}},
                    100: {'label': '100%', 'style': {'color': '#77b0b1'}}
                },
                included = True
            ),
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
                    1256: {'label': '1256 mins', 'style': {'color': '#77b0b1'}}
                },
                included=True,
                allowCross=False
            ),
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
                    2020: {'label': 2020, 'style': {'color': '#77b0b1'}}
                },
                included = True,
                allowCross = False
            ),
        ], style={'width': '25%'})
    ], style={'display': 'flex'})
])




@app.callback(Output('graph1', 'figure'),
              [Input('select-continent', 'value')])
def update_figure(selected_continent):
    filtered_df1 = df1

    filtered_df1 = filtered_df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df1 = filtered_df1['Netflix'].value_counts()[1]
    new_df2 = filtered_df1['Hulu'].value_counts()[1]
    new_df3 = filtered_df1['Prime Video'].value_counts()[1]
    new_df4 = filtered_df1['Disney+'].value_counts()[1]
    #new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=['Netflix', 'Hulu', 'Prime Video', 'Disney+'], y=[new_df1, new_df2, new_df3, new_df4])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Number of movies on each streaming service',
                                                                   xaxis={'title': 'Service'},
                                                                   yaxis={'title': 'Number of films'})}


if __name__ == '__main__':
    app.run_server()