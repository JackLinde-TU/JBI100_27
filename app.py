# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig2 = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")



app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    #First Graph
    html.Div([
        html.Div('Graph 1'),
        dcc.Graph(
        id='example-graph',
        figure=fig,
        ),
    ]),
    
    # Second Graph
    html.Div([
        html.Div('Graph 2'),
        dcc.Graph(
        id='example-graph2',
        figure=fig2
        ),
    ]),

    # First Dropdown Menu
    html.Div([
        html.Label('Choose a city:'),
        dcc.Dropdown(
            id = 'dropdown menu 1',
            # first you specify the label which the user sees, then specify the value which you return to the callback. 
            options = [
                {'label': 'San Francisco', 'value': 'SF'},
                {'label': 'New York City', 'value':'NY'},
                {'label': 'Amsterdam', 'value':'AM'},
            ],
            #value = 'NYC', # Default value
            
        ),
        html.Div(id='output-text 1'), # output coming from the callback
    ]),

    # Second Dropdown Menu, using pandas dataframe
    html.Div([
        html.Br(), # extra space
        html.Label('Choose a Fruit:'),
        dcc.Dropdown(df.Fruit.unique(), id = 'dropdown menu 2'),
        html.Div(id='output-text 2'), # output coming from the callback
    ]),

    # Slider example
    html.Div([
        html.Br(), # extra space
        html.Label('Choose how many beds:'),
        dcc.Slider(0, 20, 1, value = 0, id = 'slider-1'),
        html.Div(id='slider-output'),    
    ]),

    # Range slider example
    html.Div([
        html.Br(), #extra space
        html.Label('Choose the range of listings per host'),
        dcc.RangeSlider(0,100,5,value=[0,5], id='range-slider 1'),
        html.Div(id='range-slider-output'), # output coming from the callback
    ]),

    # Checkbox example using pandas dataframe
    html.Div([
        html.Br(), #extra space
        dcc.Checklist(df.Fruit.unique(), id = 'chechlist menu 1'),
        html.Div(id='output-text checkmark'), # output coming from the callback
    ]),
])

# Callback of first drop down menu
@app.callback(
    Output('output-text 1', 'children'),
    Input('dropdown menu 1', 'value')
)

# Return value of first callback (Dropdown menu 1)
def update_output(value):
    return f'You have selected {value}'

# Callback of second drop down menu
@app.callback(
    Output('output-text 2', 'children'),
    Input('dropdown menu 2', 'value')
)

# Return value of second callback (Dropdown menu 2)
def update_output(value):
    return f'You have selected {value}'

# return value of slider
@app.callback(
    Output('slider-output', 'children'),
    Input('slider-1', 'value')
)

def update_output(value):
    return f'You have selected {value}'

# return value of range slider
@app.callback(
    Output('range-slider-output', 'children'),
    [Input('range-slider 1', 'value')])

def update_output(value):
    return 'You have selected "{}"'.format(value)

# Callback of checkbox menu
@app.callback(
    Output('output-text checkmark', 'children'),
    Input('chechlist menu 1', 'value')
)

# Return value of second callback (Dropdown menu 2)
def update_output(value):
    return f'You have selected {value}'

if __name__ == '__main__':
    app.run_server(debug=True)
